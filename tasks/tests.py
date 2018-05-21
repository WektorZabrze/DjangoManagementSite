from django.test import TestCase
from .models import Task
from gensim.models import Doc2Vec

from .text_dimensionality_reduction import textdimensionalityreduction as tdr

class TaskTestCase(TestCase):

	def test_get_chart(self):
		url = '/tasks/chart/'
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'tasks/chart/chart.html')

	def test_user_tasks(self):
		url = '/tasks'
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)
		# Test situation when user is not logged in
		self.assertTemplateUsed(response, 'user_views/uniformed_view.html')


class TextReductionTestCaset(TestCase):

	def test_createSentenceVectors(self):
		gatheredWords = []
		tdr.gatherSentences(gatheredWords)
		model = Doc2Vec.load("tasks/text_dimensionality_reduction/doc2vecmodel")
		self.assertIsInstance(tdr.createSentenceVectors(gatheredWords, model), list)

# class TaskModelTestCase(TestCase):
# 	@classmethod
# 	def setUpTestData(cls):
# 		task1 = Task.objects.create() 

# 	def test_get_absolute_url(self):
# 		self.assertIsInstance(Task.get_absolute_url(), str)
# 		self.assertEquals(Task.get_absolute_url(), '/tasks/')