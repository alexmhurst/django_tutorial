from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	question_author = models.CharField(max_length=200, default='Alex Hurst')
	pub_date = models.DateTimeField('date published')
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	def __str__(self):
		return(self.question_text)
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.description = 'Published Recently?'

class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length = 200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return(self.choice_text)
