from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.core.cache import cache
from questions.models import Question, Answer

site = Site.objects.get_current()

def index(request):
    group_cloud_cache_key = '%s_group_cloud' % (site.domain)
    group_cloud = cache.get(group_cloud_cache_key)
    if not group_cloud:
        group_cloud = Answer.objects.get_cloud()
        cache.set(group_cloud_cache_key, group_cloud, 60*1)
    
#    questions = Question.objects.filter(answer__isnull=False).distinct()[:5]
    questions = Question.objects.all().distinct()[:5]
    if request.user.is_authenticated():
        for i in xrange(len(questions)):
            try:
                a = Answer.objects.get(question = questions[i],
                                       user = request.user)
            except:
                pass
            else:
                questions[i].user_answer = a.answer
    
    return render_to_response('index.html',
                              {'questions': questions,
                               'answers': Answer.objects.all().order_by('-added')[:10],
                               'members': User.objects.filter(is_active=True).order_by('-date_joined')[:12],
                               'question_count': Question.objects.count(),
                               'answer_count': Answer.objects.count(),
                               'user_count': User.objects.filter(is_active=True).count()},
                               context_instance = RequestContext(request))


