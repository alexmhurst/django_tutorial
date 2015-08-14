from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from .models import Question

class QuestionMethodTests(TestCase):
	
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return false for questions
		whose pub_date is in the future.
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date = time)
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return false for questions
		whose pub_date is more than 1 day ago.
		"""		
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date = time)
		self.assertEqual(old_question.was_published_recently(), False)
	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() should return true for questions
		whose pub_date is within the past day.
		"""		
		time = timezone.now() - datetime.timedelta(hours=12)
		recent_question = Question(pub_date = time)
		self.assertEqual(recent_question.was_published_recently(), True)
