from django.shortcuts import render
from .models import Question

# Create your views here.

from django.http import HttpResponse

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	output = ', '.join ([p.question_text for p in latest_question_list])
	return HttpResponse(output)

def detail(request, question_id):
	return HttpResponse("You're looking at the detail page for question %s." % question_id)

def results(request, question_id):
	result = "You're looking at the results of question %s."
	return HttpResponse(result % question_id)

def vote(request, question_id):
	question_id_int = int(question_id)
	return HttpResponse("You're voting on question %s." % question_id)
