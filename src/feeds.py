from questions.models import Question, Answer
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed


class RssLatestQuestions(Feed):
    title = "En son sorular"
    link = "/rss/soru/"
    description = "Kimlerdensin?'e eklenen son sorular"
    
    def get_object(self):
        if len(bits) != 1:
            raise ObjectDoesNotExist

    def items(self):
        return Question.objects.filter(answer__isnull=False).distinct()[:10]
    
class AtomLatestQuestions(RssLatestQuestions):
    link = '/atom/soru/'
    subtitle = RssLatestQuestions.description
    
class RssLatestAnswers(Feed):
    title = "En son cevaplar"
    link = "/rss/cevap/"
    description = "Kimlerdensin?'e eklenen son cevaplar"
    
    def items(self):
        return Answer.objects.all().order_by('-added')[:10]

class AtomLatestAnswers(RssLatestAnswers):
    link = "/atom/cevap/"
    subtitle = RssLatestAnswers.description

