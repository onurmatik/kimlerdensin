# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from questions.models import Question, Answer, Verb
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.paginator import Paginator

site = Site.objects.get_current()


class QuestionForm (forms.ModelForm):
    def clean(self):
        try:
            q = Question.objects.get(slug=slugify(self.cleaned_data['question']),
                                     verb=self.cleaned_data['verb'])
        except:
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Bu soru sorulmuş: <a href="%s">%s</a>' % (q.get_absolute_url(),
                                                                                    q))
    class Meta:
        model = Question


@login_required
def add_question(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = request.user.id
        form = QuestionForm(data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = QuestionForm()
    return render_to_response('questions/add_question.html',
                              {'form': form,
                               'form_errors_all': form.errors.get('__all__', None),
                               'selected_tab': 'questions'},
                               context_instance = RequestContext(request))

def apply_answer(question, answer, user):
    try:
        a = Answer.objects.get(question = question,
                               user = user)
    except:
        if answer != '0':
            a = Answer(question = question,
                       user = user,
                       answer = answer)
            a.save()
    else:
        if answer == '0':
            a.delete()
        else:
            a.answer = answer
            a.save()

@login_required
def answer_question(request, question_id, answer):
    q = get_object_or_404(Question, id=question_id)
    apply_answer(q, answer, request.user)
    return HttpResponseRedirect(q.get_absolute_url())

def ajax_answer_question(request, question_id, answer):
    if request.user.is_authenticated():
        q = get_object_or_404(Question, id=question_id)
        apply_answer(q, answer, request.user)
        return HttpResponse(answer, content_type='text/plain')
    else:
        redirect_url = reverse('questions.views.answer_question',
                               kwargs = {'question_id': question_id,
                                         'answer': answer})
        return HttpResponse(redirect_url, content_type='text/plain')

def question_detail(request, verb_slug, question_slug):
    q = get_object_or_404(Question, verb__slug=verb_slug, slug=question_slug)
    answers_yes = Answer.objects.filter(question=q, answer=1)
    answers_no = Answer.objects.filter(question=q, answer=2)
    if request.user.is_authenticated():
        try:
            a = Answer.objects.get(question = q,
                                   user = request.user)
        except:
            pass
        else:
            q.user_answer = a.answer
    return render_to_response('questions/question_detail.html',
                              {'question': q,
                               'selected_tab': 'questions',
                               'answers_yes': answers_yes,
                               'answers_no': answers_no},
                               context_instance = RequestContext(request))

def question_list(request, verb_slug=None, page=1):
    p = int(page) - 1
    verb_cloud_cache_key = '%s_verb_cloud' % (site.domain)
    verb_cloud = cache.get(verb_cloud_cache_key)
    if not verb_cloud:
        print "if1"
        verb_cloud = Verb.objects.get_cloud()
        cache.set(verb_cloud_cache_key, verb_cloud, 60*60*24)
    
    if verb_slug:
        print "if2"
        verb = get_object_or_404(Verb, slug=verb_slug)
        query_set = Question.objects.filter(verb=verb)
        not_answered = Question.objects.get_not_answered().filter(verb=verb).distinct()[:8]
    else:
        print "else"
        verb = None
        query_set = Question.objects.all()
        not_answered = Question.objects.get_not_answered()[:8]
    
    paginator = Paginator(query_set, 10)
    questions = paginator.page(p)
    
    if request.user.is_authenticated():
        for i in xrange(len(questions)):
            try:
                a = Answer.objects.get(question = questions[i],
                                       user = request.user)
            except:
                pass
            else:
                questions[i].user_answer = a.answer

    next_page, previous_page = None, None
    if paginator.has_next_page(p):
        next_page = p + 2
    if paginator.has_previous_page(p):
        previous_page = p
    
    return render_to_response('questions/question_list.html',
                              {'object_list': questions,
                               'page': page,
                               'is_paginated': paginator.pages > 1,
                               'has_next': paginator.has_next_page(p),
                               'has_previous': paginator.has_previous_page(p),
                               'next': next_page,
                               'previous': previous_page,
                               'pages': paginator.pages,
                               'selected_tab': 'questions',
                               'verb': verb,
                               'verb_cloud': verb_cloud,
                               'not_answered': not_answered},
                               context_instance=RequestContext(request))

