from django.test import TestCase
from django.test import Client
from django.utils import timezone 
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from .models import Task
from gensim.models import Doc2Vec
from users.models import Person
from .apps import TasksConfig
from .views import task_add
from .forms import TaskForm
from .utils import calculate_productivity_index
import pytz
from django.forms.fields import DateTimeField

from .text_dimensionality_reduction import textdimensionalityreduction as tdr

class TaskViewsTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.date = timezone.now()
		cls.person = Person.objects.create_user(username = 'temp', password = 'temp', position = 'BOS')
		cls.task1 = Task.objects.create(priority = 'LOW',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskViewsTestCase.date, 
			deadline_date = TaskViewsTestCase.date) 
		cls.factory = RequestFactory()

	def test_tasks_list(self):
		url = '/tasks/'
		# Test if unauthorized user - should redirect
		response = self.client.get(url)
		self.assertEquals(response.status_code, 302)
		# Test if authorized user
		c = Client()
		c.login(username = 'temp', password = 'temp')
		response = c.get(url)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, "tasks/tasks_list.html")
		c.logout()
		
	def test_task_add(self):
		url = "/tasks/add/"
		# Test if unauthorized user
		response = self.client.get(url)
		self.assertEquals(response.status_code, 302)
		# Test if authorized user
		c = Client()
		c.login(username = 'temp', password = 'temp')
		response = c.get(url)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'tasks/task_form.html')
		c.logout()
		# Test using Request Factory
		request = TaskViewsTestCase.factory.post(url) # POST
		request.user = AnonymousUser()
		response = task_add(request)
		self.assertEqual(response.status_code, 302)


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

	def test_cleanseWords(self):
		test = ["aaa", "bbb"]
		self.assertEquals(tdr.cleanseWords(test), None)

	


class TaskModelTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.date = timezone.now()
		cls.person = Person.objects.create_user(username = 'temp', password = 'temp', position = 'BOS')
		cls.task1 = Task.objects.create(priority = 'LOW',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskModelTestCase.date, 
			deadline_date = TaskModelTestCase.date) 

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
		self.assertEquals(self.task1.created_date, TaskModelTestCase.date)
		self.assertEquals(self.task1.deadline_date, TaskModelTestCase.date)


class TaskAppsTestCase(TestCase):
	'''Test apps module'''
	def test_TasksConfig(self):
		''' Test task name'''
		self.assertEquals(TasksConfig.name, 'tasks')

class TaskUtilsTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		''' Set up localized deadline-date for tasks, create dummy tasks '''
		cls.deadline_date = DateTimeField().clean('2030-06-04 13:00')
		TaskUtilsTestCase.deadline_date = TaskUtilsTestCase.deadline_date.replace(tzinfo=None)
		tz = pytz.timezone('Europe/Berlin')
		tz.localize(TaskUtilsTestCase.deadline_date)
		cls.date = timezone.now()
		cls.person = Person.objects.create_user(username = 'temp', password = 'temp', position = 'BOS')
		cls.task1 = Task.objects.create(priority = 'LOW',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskUtilsTestCase.date, 
			deadline_date = TaskUtilsTestCase.deadline_date)
		cls.task2 =  Task.objects.create(priority = 'LOW',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskUtilsTestCase.date, 
			deadline_date = TaskUtilsTestCase.date)

	def test_calculate_productivity_index(self):
		TaskUtilsTestCase.task1.end_date = TaskUtilsTestCase.date
		TaskUtilsTestCase.task2.end_date = TaskUtilsTestCase.date
		self.assertIsInstance(calculate_productivity_index(TaskUtilsTestCase.task1), float)
		self.assertIsInstance(calculate_productivity_index(TaskUtilsTestCase.task2), int)
		self.assertEquals(calculate_productivity_index(TaskUtilsTestCase.task2), 0)
		


