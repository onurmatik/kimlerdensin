# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models, connection
from django.contrib.auth.models import User
from commonutils.slug import slugify


class VerbManager(models.Manager):
    def get_verb_list(self):
        return

    def get_cloud(self):
        return

class Verb(models.Model):
    verb = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)
    negative = models.CharField(max_length=50)
    negative_slug = models.SlugField(editable=False)
    type = models.PositiveSmallIntegerField(choices=((1, 'lardan mısın?'),
                                                     (2, 'lerden misin?')))
    
    objects = VerbManager()
    
    def save(self):
        self.slug = slugify(self.verb)
        self.negative_slug = slugify(self.negative)
        super(Verb, self).save()
    
    def __unicode__(self):
        return u'%s%s' % (self.verb,
                          self.get_type_display())
    
    class Meta:
        ordering = ['verb']
    

class QuestionManager(models.Manager):
    def get_not_answered(self):
        not_answered=Question.objects.filter(answer__isnull=True).distinct()
        
        return not_answered

class Question(models.Model):
    question = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150,
                            editable=False)
    verb = models.ForeignKey(Verb)
    added = models.DateTimeField(editable=False)
    user = models.ForeignKey(User)
    
    objects = QuestionManager()
    
    def __unicode__(self):
        return u'%s %s' % (self.question,
                           self.verb)
    
    def save(self):
        self.added = datetime.now()
        self.slug = slugify(self.question)
        super(Question, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('questions.views.question_detail', (),
                {'verb_slug': self.verb.slug,
                 'question_slug': self.slug})
    
    class Meta:
        unique_together = (('question', 'verb'),)
        ordering = ['-added']
    

class AnswerManager(models.Manager):
    def get_answer_list(self):
        return

    def get_cloud(self):
        return

class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.PositiveSmallIntegerField(choices=((1, 'Evet'),
                                                       (2, 'Hayır')))
    user = models.ForeignKey(User)
    added = models.DateTimeField(editable=False)
    
    objects = AnswerManager()
    
    def __unicode__(self):
        if self.answer == 1:
            verb = self.question.verb.verb
        else:
            verb = self.question.verb.negative
        if self.question.verb.type == 1:
            ending = 'lardan'
        else:
            ending = 'lerden'
        return '%s %s %s%s' % (self.user.username,
                               self.question.question,
                               verb,
                               ending)
    
    @models.permalink
    def get_absolute_url(self):
        if self.answer == 1:
            verb_slug = self.question.verb.slug
        else:
            verb_slug = self.question.verb.negative_slug
        return ('users.views.browse_user_by_answer', (),
                {'verb_slug': verb_slug,
                 'question_slug': self.question.slug})
    
    def save(self):
        self.added = datetime.now()
        super(Answer, self).save()
    
    class Meta:
        unique_together = (('question', 'user'),)
    



