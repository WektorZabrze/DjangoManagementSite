from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.utils import timezone
from django.forms.fields import DateTimeField
from django.contrib.auth.models import AnonymousUser
from gensim.models import Doc2Vec
from users.models import Person
from .apps import TasksConfig
from .models import Task
from .views import task_add, basic_view
from .forms import TaskForm
from .utils import calculate_productivity_index
import pytz


from .text_dimensionality_reduction import textdimensionalityreduction as tdr

class TaskViewsTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.date = timezone.now()
		cls.person = Person.objects.create_user(username = 'temp', password = 'temp', position = 'BOS')
		cls.person2 = Person.objects.create_user(username = 'temp2', password = 'temp2', position = 'WOR')
		cls.person3 = Person.objects.create_user(username = 'temp3', password = 'temp3', position = 'WOR')
		cls.person.subordinates.add(cls.person2)
		cls.task1 = Task.objects.create(priority = 'LOW',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskViewsTestCase.date, 
			deadline_date = TaskViewsTestCase.date) 
		cls.task2 = Task.objects.create(priority = 'LOW',assigned_employee = cls.person2,  task_name = 'dummy task2', 
			task_description = 'dummy_task2', created_date = TaskViewsTestCase.date, 
			deadline_date = TaskViewsTestCase.date) 
		cls.factory = RequestFactory()

	def test_basic_view(self):
		# Test response 
		request = TaskViewsTestCase.factory.get('/2/')
		request.user = TaskViewsTestCase.person
		response = basic_view(request, 2)
		self.assertEquals(response.status_code, 200)
		# Test redirect - request user not associated with task given by pk (primary key)
		request = TaskViewsTestCase.factory.get('/2/')
		request.user = TaskViewsTestCase.person3
		response = basic_view(request, 2)
		self.assertEquals(response.status_code, 302)


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
		client = Client()
		response = client.post(url)
		self.assertEqual(response.status_code, 302)

	def test_get_chart(self):
		url = '/tasks/chart/'
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'tasks/chart/chart.html')

	def test_user_tasks(self):
		url = '/tasks/user_tasks/'
		# Test situation when user is not logged in
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)
		# Test situation when user is logged in
		client = Client()
		client.login(username = 'temp', password = 'temp')
		response = client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'tasks/user_tasks.html')


	# TODO : Finish
	def test_task_edit(self):
		url = '/tasks/edit/1/'
		# Test if unauthorized user
		response = self.client.get(url)
		self.assertEquals(response.status_code, 302)
		# Test if autorized - if using GET method
		# client = Client()
		# client.login(username = 'temp', password = 'temp')
		# response = client.post(url)
		# self.assertEqual(response.status_code, 200)
		# self.assertTemplateUsed(response, 'tasks/task_edit.html')

		


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
		cls.task3 = Task.objects.create(priority = 'HIG',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskUtilsTestCase.date, 
			deadline_date = TaskUtilsTestCase.deadline_date)
		cls.task4 = Task.objects.create(priority = 'CRI',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskUtilsTestCase.date, 
			deadline_date = TaskUtilsTestCase.deadline_date)
		cls.task5 = Task.objects.create(priority = 'MED',assigned_employee = cls.person,  task_name = 'dummy task', 
			task_description = 'dummy_task', created_date = TaskUtilsTestCase.date, 
			deadline_date = TaskUtilsTestCase.deadline_date)

	def test_calculate_productivity_index(self):
		TaskUtilsTestCase.task1.end_date = TaskUtilsTestCase.date
		TaskUtilsTestCase.task2.end_date = TaskUtilsTestCase.date
		TaskUtilsTestCase.task3.end_date = TaskUtilsTestCase.date
		TaskUtilsTestCase.task4.end_date = TaskUtilsTestCase.date
		TaskUtilsTestCase.task5.end_date = TaskUtilsTestCase.date
		self.assertIsInstance(calculate_productivity_index(TaskUtilsTestCase.task1), float)
		self.assertIsInstance(calculate_productivity_index(TaskUtilsTestCase.task3), float)
		self.assertIsInstance(calculate_productivity_index(TaskUtilsTestCase.task4), float)
		self.assertIsInstance(calculate_productivity_index(TaskUtilsTestCase.task5), float)
		self.assertIsInstance(calculate_productivity_index(TaskUtilsTestCase.task2), int)
		self.assertEquals(calculate_productivity_index(TaskUtilsTestCase.task2), 0)
		


