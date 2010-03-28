from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from sitemaps import *
from feeds import RssLatestQuestions, AtomLatestQuestions, RssLatestAnswers, AtomLatestAnswers

admin.autodiscover()

rss_feeds = {'soru': RssLatestQuestions,
             'cevap': RssLatestAnswers}

atom_feeds = {'soru': AtomLatestQuestions,
              'cevap': AtomLatestAnswers}

sitemaps = {'lists': ListPagesSitemap,
            'question': QuestionSitemap,
            'answer': AnswerSitemap,
            'user': UserSitemap}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
     
    (r'^$', 'index.views.index'),
     
    (r'^ajax-ans/(?P<question_id>\d+)/(?P<answer>[012])/$', 'questions.views.ajax_answer_question'),
    (r'^ans/(?P<question_id>\d+)/(?P<answer>[012])/$', 'questions.views.answer_question'),
    
    url(r'^soru/ekle/$', 'questions.views.add_question', name='question_add'),
    (r'^soru/$', 'questions.views.question_list'),
    url(r'^soru/(?P<page>\d+)/$', 'questions.views.question_list', name='question_list'),
    url(r'^soru/(?P<verb_slug>[-\w]+)/$', 'questions.views.question_list', name='question_list_by_verb'),
    (r'^soru/(?P<verb_slug>[-\w]+)/(?P<page>\d+)/$', 'questions.views.question_list'),
    (r'^soru/(?P<verb_slug>[-\w]+)/(?P<question_slug>[-\w]+)/$', 'questions.views.question_detail'),

    url(r'^xml/$', 'django.views.generic.simple.direct_to_template', {'template': 'feed_index.html'}, name='feed_index'),
    url(r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_feeds}, name='rss_feeds'),
    url(r'^atom/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': atom_feeds}, name='atom_feeds'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>.*\.(?i)(css|js|jpg|png|gif|ico|swf|html))$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

