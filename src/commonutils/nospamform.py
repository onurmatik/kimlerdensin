# based on http://www.djangosnippets.org/snippets/417/

from django.newforms.util import ValidationError
from django.utils.translation import ugettext as _
from time import time
from django.conf import settings
from Crypto.Cipher import Blowfish
from base64 import b64encode, b64decode
from django import newforms as forms


def get_key():
    cobj = Blowfish.new(settings.SECRET_KEY)
    text = unicode(time())
    text += "".join(["_" for i in xrange(8-len(text)%8)])
    return b64encode(cobj.encrypt(text))

class FormWithKeyField(forms.Form):
    def __init__(self, *args, **kwargs):
        self.base_fields['key'] = forms.CharField(max_length=100,
                                                  widget=forms.widgets.HiddenInput(),
                                                  initial=get_key())
        super(FormWithKeyField, self).__init__(*args, **kwargs)
    
    def clean_key(self):
        def validation_error():
            self.data['key'] = get_key()
            raise ValidationError(_('Incorrect key.'))
        
        cobj = Blowfish.new(settings.SECRET_KEY)
        text = cobj.decrypt(b64decode(self.cleaned_data['key'])).rstrip('_')
        try:
            key = float(text)
        except:
            validation_error()
        now = time()
        if now - key < 10 or now - key > 60*60*6: # valid for 6 hours
            validation_error()
        return
    
