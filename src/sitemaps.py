from django.conf import settings
from django.contrib.sitemaps import Sitemap
from questions.models import Question, Answer
from django.contrib.auth.models import User


class ListPagesSitemap(Sitemap):
    priority = 0.8

    def items(self):
        items = (('index', '/'),
                 ('questions', '/soru/'),
                 ('answers', '/cevap/'),
                 ('users', '/uyeler/'),)
        return items
    
    def location(self, item):
        return item[1]

class QuestionSitemap(Sitemap):
    priority = 1

    def items(self):
        return Question.objects.all()

    def lastmod(self, item):
        return item.added

class AnswerSitemap(Sitemap):
    priority = 0.8

    def items(self):
        return Answer.objects.all()

    def lastmod(self, item):
        return item.added

class UserSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return User.objects.filter(is_active=True).order_by('-date_joined')

    def lastmod(self, item):
        return item.date_joined

