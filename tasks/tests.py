from django.test import TestCase
from .models import Task
from gensim.models import Doc2Vec
from users.models import Person
from .apps import TasksConfig

from .text_dimensionality_reduction import textdimensionalityreduction as tdr

class TaskViewsTestCase(TestCase):

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


class TextReductionTestCase(TestCase):

	def test_createSentenceVectors(self):
		gatheredWords = []
		tdr.gatherSentences(gatheredWords)
		model = Doc2Vec.load("tasks/text_dimensionality_reduction/doc2vecmodel")
		self.assertIsInstance(tdr.createSentenceVectors(gatheredWords, model), list)

class TaskModelTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.person = Person.objects.create_user(username = 'temp', password = 'temp', position = 'BOS')
		cls.task1 = Task.objects.create(priority = 'LOW',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = '1900-01-01', 
			deadline_date = '2030-01-01') 

	def test_get_absolute_url(self):
		self.assertIsInstance(self.task1.get_absolute_url(), str)
		self.assertEquals(self.task1.get_absolute_url(), '/tasks/')

	def test__str__(self):
		self.assertEquals(str(self.task1), self.task1.task_name)

	def test_fields(self):
		self.assertEquals(self.task1.priority, 'LOW')
		self.assertEquals(self.task1.assigned_employee, self.person)
		self.assertEquals(self.task1.task_name, 'dummy task')
		self.assertEquals(self.task1.task_description, 'dummy_task')
		self.assertEquals(self.task1.created_date, '1900-01-01')
		self.assertEquals(self.task1.deadline_date, '2030-01-01')


class TaskAppsTestCase(TestCase):
	'''Test apps module'''
	def test_TasksConfig(self):
		''' Test task name'''
		self.assertEquals(TasksConfig.name, 'tasks')