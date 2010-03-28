"""
gmail.py -- Python interface to Gmail (http://www.gmail.com/)

Known to work with Python 2.3+.

Sample usage:

>>> c = GmailClient()
>>> c.login('username', 'password')
>>> c.get_inbox_conversations()
['free viagra', 'welcome to css-discuss', 'hey, how are you?']
>>> c.get_inbox_conversations(is_unread=True)
['free viagra', 'hey, how are you?']
>>> c.get_inbox_conversations(subject='css')
['welcome to css-discuss']
>>> c.get_inbox_conversations()[2]
'hey, how are you?'
>>> c.get_inbox_conversations()[2].get_messages()
[<email.Message.Message instance at 0xf6bbad4c>, <email.Message.Message instance at 0xf6bbad8a>]
>>> print c.get_inbox_conversations()[2].get_messages()[0]
# outputs raw e-mail source
>>> c.get_contacts()
[['jlennon@gmail.com', 'John Lennon'], ['billy@hotmail.com', 'Billy Shears']]
>>> c.add_contact('George', 'george@yahoo.com')
>>> c.delete_contact('jlennon@gmail.com')
"""

# Copyright (C) 2004, Adrian Holovaty
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA

# Changelog:
#
# 0.1 (2004-06-18)
#     Initial version. Support for login() and get_inbox_messages().
# 0.2 (2004-06-20)
#     Added get_contacts(), add_contact() and delete_contact().
#     Changed get_inbox_messages() to get_inbox_conversations().
#     Made get_inbox_conversations() subject parameter case-insensitive.
# 0.3 (2004-06-24) -- Patch from Gustavo Sverzut Barbieri (Thanks, Gustavo!)
#     GmailClient.login() now raises LoginFailure on failure.
#     Added socket.setdefaulttimeout(30).
#     Added UTF-8 support (GmailClient._encode()).
#
# To do:
# * Optionally mark messages as read when they're retrieved.
# * Clean HTML in Conversation subjects.
# * Add GmailClient.get_conversations_by_label() method.


__version__ = "0.3"
__date__ = "2004-06-24"
__author__ = "Adrian Holovaty (holovaty@gmail.com)"

from Cookie import SimpleCookie
import email, random, re, socket, time, urllib, urllib2

EMAILS_RE = re.compile('\nD\((\["t",.*?\])\n\);', re.DOTALL)
MESSAGE_INFO_RE = re.compile('\nD\((\["mi",.*?\])\n\);', re.DOTALL)
# Gmail says this when it complains
FAILURE_MESSAGE = 'Your action was not successful'
LOGIN_FAILURE_MESSAGE = 'Username and password do not match.'

class BadGmailTransaction(Exception):
    "Base exception raised when Gmail transactions don't work"
    pass

class ContactCouldNotBeAdded(BadGmailTransaction):
    pass

class ContactCouldNotBeDeleted(BadGmailTransaction):
    pass

class LoginFailure(BadGmailTransaction):
    pass

socket.setdefaulttimeout(30)

class GmailClient:
    def __init__(self):
        self._cookies = SimpleCookie()
        self._folder_cache, self._message_cache = {}, {}
        self._contacts = []

    def login(self, username, password):
        """
        Logs into Gmail with the given username and password.
        Raises LoginFailure if the login fails.
        """
        epoch_secs = int(time.time())
        self._cookies["GMAIL_LOGIN"] = "T%s/%s/%s" % (epoch_secs-2, epoch_secs-1, epoch_secs)
        p = self._get_page("https://www.google.com/accounts/ServiceLoginBoxAuth",
            post_data="continue=https://gmail.google.com/gmail&service=mail&Email=%s&Passwd=%s&submit=null" % (username, password))
        c = p.read()
        p.close()
        r = re.search('var cookieVal\s*=\s*"([^"]+)"', c)
        if not r or c.find(LOGIN_FAILURE_MESSAGE) > -1:
            raise LoginFailure, "Wrong username or password."
        self._cookies['GV'] = r.groups()[0]
        p = self._get_page("https://www.google.com/accounts/CheckCookie?continue=http%3A%2F%2Fgmail.google.com%2Fgmail&service=mail&chtml=LoginDoneHtml")
        p.close()
        p = self._get_page("http://www.google.com/")
        p.close()
        p = self._get_page("http://gmail.google.com/gmail?view=page&name=js")
        c = p.read()
        p.close()
        r = re.search("var js_version\s*=\s*'([^']+)'", c)
        if not r:
            raise LoginFailure, "Gmail might have redesigned."
        self._js_version = r.groups()[0]

    def get_inbox_conversations(self, is_unread=None, is_starred=None, label=None, subject=None):
        """
        Returns a list of all the messages in the inbox matching the given
        search parameters, as GmailMessageStub objects.

        Parameters:
            is_unread:  Boolean (or just 1 or 0). Limits the results to read
                        vs. unread conversations. A conversation is read if
                        *every one* of its messages has been read.
            is_starred: Boolean (or just 1 or 0). Limits the results to starred
                        vs. unstarred conversations.
            label:      String. Limits the results to conversations having the
                        exact given label.
            subject:    String. Limits the results to conversations containing
                        the given string in their subject. (Case-insensitive.)
        """
        message_stubs = []
        for stub in self._get_message_stubs(folder='inbox'):
            if is_unread is not None and stub.is_unread != is_unread:
                continue
            if is_starred is not None and stub.is_starred != is_starred:
                continue
            if label is not None and label not in stub.label_list:
                continue
            if subject is not None and stub.subject.lower().find(subject.lower()) == -1:
                continue
            message_stubs.append(stub)
        return message_stubs

    def add_contact(self, name, email, notes=''):
        """
        Adds a contact with the given name, e-mail and notes to this Gmail
        account's address book. Raises ContactCouldNotBeDeleted on error.
        """
        p = self._get_page("https://gmail.google.com/gmail?view=address&act=a",
            post_data="at=%s&name=%s&email=%s&notes=%s&ac=Add+Contact&operation=Edit" % \
            (self._cookies['GMAIL_AT'].value, self._url_quote(name),
            self._url_quote(email), self._url_quote(notes)))
        if p.read().find(FAILURE_MESSAGE) > -1:
            raise ContactCouldNotBeAdded, "Gmail might have redesigned."

    def delete_contact(self, email):
        """
        Deletes the contact with the given e-mail address from this Gmail
        account's address book. Raises ContactCouldNotBeDeleted on error.
        """
        contact_index = None
        for i, c in enumerate(self.get_contacts()):
            if c[0] == email:
                contact_index = i + 1
                break
        if contact_index is None:
            raise ContactCouldNotBeDeleted, "The e-mail address '%s' wasn't in your Gmail address book." % email
        p = self._get_page("https://gmail.google.com/gmail?view=address&act=a",
            post_data="operation=Delete&at=%s&email%s=%s" % \
            (self._cookies['GMAIL_AT'].value, contact_index, urllib.quote_plus(email)))
        if p.read().find(FAILURE_MESSAGE) > -1:
            raise ContactCouldNotBeDeleted, "Gmail might have redesigned."

    def get_contacts(self, clear_cache=False):
        """
        Returns a list of lists representing all the contacts for this Gmail
        account, in the format ['email', 'contact name'].
        """
        if clear_cache or not self._contacts:
            p = self._get_page("https://gmail.google.com/gmail?view=page&name=contacts&zx=%s%s" % \
                (self._js_version, self._get_random_int()))
            # The returned page contains only a JavaScript data structure that
            # looks like this:
            # [["jlennon@gmail.com","John Lennon"]
            # ,["billy@hotmail.com","Billy Shears"]
            # ,["percy@yahoo.com","Percy Thrillington"]
            # ]
            # Because this is exactly the same syntax as Python lists, we can
            # use an eval() on it to suck it into Python. THIS IS A SECURITY
            # RISK, THOUGH, because it blindly trusts Gmail's page isn't going
            # to include evil Python code.
            self._contacts = eval(p.read())
        return self._contacts

    def _get_page(self, url, post_data=None):
        """
        Helper method that gets the given URL, handling the sending and storing
        of cookies. Returns the requested page as a file-like object in the
        format returned by urllib2.urlopen().
        """
        req = urllib2.Request(self._encode(url))
        if post_data is not None:
            req.add_data(self._encode(post_data))
        req.add_header('Cookie', self._encode(self._cookies.output(attrs=[], header='').strip()))
        req.add_header('Charset', 'utf-8')
        f = urllib2.urlopen(req)
        if f.headers.dict.has_key('set-cookie'):
            self._cookies.load(f.headers.dict['set-cookie'])
        return f

    def _get_random_int(self):
        """
        Helper method that returns a random number suitable for Gmail's "zx"
        query parameter, which is needed (required?) in some cases.
        """
        return random.randint(0, 1000000000)

    def _get_message_stubs(self, folder, offset=0):
        """
        Helper method that retrieves the given folder from a Gmail account
        and returns a list of Conversation objects, each representing a
        conversation in the folder. Saves its result in a cache the first time
        it's called.

        KNOWN LIMITATION: If a folder spans more than one page, this method
        will only return the messages on the first page.
        """
        if not self._folder_cache.has_key(folder):
            html = self._get_page("http://gmail.google.com/gmail?search=%s&view=tl&start=%d&init=1&zx=%s%s" % \
                (folder, offset, self._js_version, self._get_random_int())).read()
            # We can use Python's eval() on the JavaScript source Gmail spits
            # out, because it's in Python-friendly list syntax. This IS a
            # slight security risk, of course.
            stub_list = []
            for match in EMAILS_RE.findall(html):
                for msg_bits in eval(match)[1:]:
                    stub_list.append(Conversation(self, *msg_bits))
            self._folder_cache[folder] = stub_list
        return self._folder_cache[folder]

    def _get_raw_email(self, message_id):
        """
        Retrieves the message with the given message ID and returns it as an
        email.Message.Message. Saves its result in a cache the first time an
        e-mail is retrieved.
        """
        if not self._message_cache.has_key(message_id):
            f = self._get_page("http://gmail.google.com/gmail?view=om&th=%s&zx=%s%s" % \
                (message_id, self._js_version, self._get_random_int()))
            self._message_cache[message_id] = email.message_from_string(f.read().lstrip())
        return self._message_cache[message_id]

    def _url_quote(self, value):
        """
        Helper method that quotes the given value for insertion into a query
        string. Also encodes into UTF-8, which Google uses, in case of
        non-ASCII characters.
        """
        value = self._encode(value)
        return urllib.quote_plus(value)

    def _encode(self, value):
        """
        Helper method. Google uses UTF-8, so convert to it, in order to allow
        non-ASCII characters.
        """
        if isinstance(value, unicode):
            value = value.encode("utf-8")
        return value

class Conversation:
    """
    Represents the minimal information known about an conversation from
    scraping a Gmail folder list page and provides a way of retrieving the full
    messages.
    """
    def __init__(self, client, thread_id, is_unread, is_starred, date_html,
            authors_html, flags, subject_html, snippet_html, label_list,
            attach_html, matching_msgid, extra_snippet):
        self.client, self.thread_id = client, thread_id
        self.is_unread, self.is_starred = is_unread, is_starred
        self.date_html, self.authors_html = date_html, authors_html
        self.flags, self.subject = flags, subject_html
        self.snippet_html, self.label_list = snippet_html, label_list
        self.attach_html, self.matching_msgid = attach_html, matching_msgid
        self.extra_snippet = extra_snippet
        self._message_id_cache = []

    def __repr__(self):
        return self.subject

    def get_messages(self):
        """
        Returns a list of all messages in this conversation, in chronological
        order, as email.Message.Message objects.
        """
        if not self._message_id_cache:
            html = self.client._get_page("https://gmail.google.com/gmail?view=cv&search=inbox&th=%s&zx=%s%s" % \
                (self.thread_id, self.client._js_version, self.client._get_random_int())).read()
            message_ids = []
            for match in MESSAGE_INFO_RE.findall(html):
                # Note the eval(), which is a security risk.
                message_ids.append(eval(match)[3])
            self._message_id_cache = message_ids
        return [self.client._get_raw_email(i) for i in self._message_id_cache]
