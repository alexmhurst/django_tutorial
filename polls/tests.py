from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from .models import Question, Choice
from django.core.urlresolvers import reverse

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

class ChoiceMethodTests(TestCase):
	def test_choice_returns_correct_string(self):
		"""
		choice.__to_str__() should return the text of the choice.
		"""
		q = create_question("Question 1.", 0)
		c = q.choice_set.create(choice_text="Choice 1.", votes=0)
		self.assertEqual(c.__str__(), "Choice 1.")
	def test_choice_starts_with_no_votes(self):
		"""
		When a choice is created, it should have a vote count of 0.
		"""
		q = create_question("Question 1.", 0)
		c = q.choice_set.create(choice_text="Choice 1.",)
		self.assertEqual(c.votes, 0)

def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, 
					pub_date = time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		"""
		If no questions exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_past_question(self):
		"""
		If a past question exists, it should be displayed on the index page.
		"""
		create_question("Past question.", -1)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Past question.')
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

	def test_index_view_with_future_question(self):
		"""
		If a future question exists, it should not be displayed on the index page.
		"""
		create_question("Future question.", 1)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No polls are available.', status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_past_and_future_questions(self):
		"""
		If both past and future questions exist, only the past question should be shown on the index page.
		"""
		create_question("Past question.", -1)
		create_question("Future question.", 1)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, 'Past question.', status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])


	def test_index_view_with_two_past_questions(self):
		"""
		If two past questions exist, they should both show.
		"""
		create_question("Past question 1.", -1)
		create_question("Past question 2.", -2)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, 'Past question 1.', status_code=200)
		self.assertContains(response, 'Past question 2.', status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 1.>', '<Question: Past question 2.>'])
		


	def test_index_view_with_more_than_five_past_questions(self):
		"""
		If two past questions exist, they should both show.
		"""
		create_question("Past question 1.", -1)
		create_question("Past question 2.", -2)
		create_question("Past question 3.", -3)
		create_question("Past question 4.", -4)
		create_question("Past question 5.", -5)
		create_question("Past question 6.", -6)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(len(Question.objects.all()), 6)
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 1.>', '<Question: Past question 2.>',  '<Question: Past question 3.>',  '<Question: Past question 4.>',  '<Question: Past question 5.>'])

class voteViewTests(TestCase):
	
	def test_voting_once_increments_vote(self):
		"""
		When the vote view is loaded, the vote count for a choice should increase by 1.
		"""

		myq = create_question("Question 1.", -1)
		myc_id = myq.choice_set.create(choice_text="Choice 1.").id
		response = self.client.post(reverse("polls:vote", kwargs={'question_id': myq.id}), data={'choice': myc_id})
		self.assertEqual(Choice.objects.get(id=myc_id).votes, 1)



