from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from tasks.models import Task
from .views import index
from .views import recruit
from .views import subordinates_list
from .views import edit, logout_user
from .models import Person
from .forms import PersonForm
from .forms import PersonChangeForm
from .apps import UsersConfig
from .utils import calculate_productivity_index

class UserViewsTestCase(TestCase):
	# Create some users for testing purposes
	@classmethod
	def setUpTestData(cls):
		cls.user_boss = Person.objects.create_user(username = 'temp_boss', password = 'temp_boss', position = "BOS" )
		cls.user_manager = Person.objects.create_user(username = 'temp_manager', password = 'temp_manager', position = "MAN")
		cls.user_worker = Person.objects.create_user(username = 'temp_worker', password = 'temp_worker', position = "WOR")
		cls.user_supervisor = Person.objects.create_user(username = 'temp_supervisor', password = 'temp_supervisor', position = "SUP")
		cls.factory = RequestFactory()

	
	def test_subordinates_list(self):
		client = Client()
		client.login(username = 'temp_boss', password = 'temp_boss')
		request = UserViewsTestCase.factory.get('/users/edit/')
		request.user = UserViewsTestCase.user_boss
		# Test when user has no subordinates - returns empty list
		self.assertIsInstance(subordinates_list(request), list)
		self.assertEqual(subordinates_list(request), [])
		# Test when added subordinates
		UserViewsTestCase.user_boss.subordinates.add(UserViewsTestCase.user_worker)
		request.user = UserViewsTestCase.user_boss
		self.assertIsInstance(subordinates_list(request), list)
		self.assertEqual(subordinates_list(request), [(str(UserViewsTestCase.user_worker.personal_id), UserViewsTestCase.user_worker.first_name) ])
		client.logout()



	def test_index_page(self):
		'''Testing index page - our starting page '''
		url = ''
		response = self.client.get(url)
		#Check response code - if 200 then its ok
		self.assertEqual(response.status_code, 200)
		# Check if correct template has been used
		self.assertTemplateUsed(response,  'user_views/uniformed_view.html')

	def test_index_page_boss(self):
		''' Testing index page with boss user loged in '''
		url = ''
		response = self.client.get(url)
		# When user is loged in, he has some options to choose
		# Now testing those options

		# Login as temporaty boss user
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)

		# Test apperence of six main functionalities 
		# that are available for boss

		# Check if template containt 'Recruit' option
		self.assertContains(response, 'Recruit')
		# Check if template contains 'Edit subordinate' option
		self.assertContains(response, 'Edit Subordinate')
		# Check if template contains 'Chat' option
		self.assertContains(response, 'Chat')
		# Check if template contains 'Logout' option
		self.assertContains(response, 'Logout')

		# Logout from boss account
		c.logout()

	def test_index_page_manager(self): 
		''' Testing index page with manager user loged in '''
		url = ''
		response = self.client.get(url)

		#  Login as temporary manager user
		c = Client()
		c.login(username = 'temp_manager', password = 'temp_manager')
		response = c.get(url)

		# Check if template containt 'Recruit' option
		self.assertContains(response, 'Recruit')
		# Check if template contains 'Edit subordinate' option
		self.assertContains(response, 'Edit Subordinate')
		# Check if template contains 'Chat' option
		self.assertContains(response, 'Chat')
		# Check if template contains 'Logout' option
		self.assertContains(response, 'Logout')

		# Logout from manager account
		c.logout()

	def test_index_page_supervisor(self):
		''' Testing index page with supervisor user loged in '''
		url = ''
		response = self.client.get(url)

		#  Login as temporary supervisor user
		c = Client()
		c.login(username = 'temp_supervisor', password = 'temp_supervisor')
		response = c.get(url)

		# Check if template contains 'Chat' option
		self.assertContains(response, 'Chat')
		# Check if template contains 'Logout' option
		self.assertContains(response, 'Logout')

		# Check if template does not contain higher lever options
		self.assertNotContains(response, 'Edit Subordinate')
		self.assertNotContains(response, 'Recruit')

		# Logout from manager account
		c.logout()

	def test_index_page_worker(self):
		''' Testing index page with worker user loged in '''
		url = ''
		response = self.client.get(url)

		#  Login as temporary worker user
		c = Client()
		c.login(username = 'temp_worker', password = 'temp_worker')
		response = c.get(url)
		
		# Check if template contains 'Chat' option
		self.assertContains(response, 'Chat')
		# Check if template contains 'Logout' option
		self.assertContains(response, 'Logout')

		# Check if template does not contain higher lever options
		self.assertNotContains(response, 'Edit Subordinate')
		self.assertNotContains(response, 'Recruit')

		# Logout from manager account
		c.logout()

	def test_login(self):
		c = Client()
		# Check id existing user can log in correctly
		is_logged_in = c.login(username = 'temp_worker', password = 'temp_worker')
		self.assertTrue(is_logged_in)
		response = self.client.get('/login/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/login/')
		self.assertRedirects(response, "/")
		self.assertEqual(response.status_code, 302)
		c.logout()
		# Check if non-existing user can not log in
		is_logged_in = c.login(username = 'aaa', password = 'aaa')
		self.assertFalse(is_logged_in)


	def test_logout(self):
	 	url = '/logout/'
	 	c = Client()
	 	c.login(username = 'temp_worker', password = 'temp_worker')
	 	response = self.client.get(url)
	 	self.assertEqual(response.status_code, 302)
	 	c.logout()

	def test_edit_view(self):
		url = '/edit/'
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertTemplateUsed(response, 'user_views/edit.html')
		self.assertEqual(response.status_code, 200)

	def test_recruit_view(self):
		url = '/recruit/'
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertTemplateUsed(response, 'user_views/recruit.html')
		self.assertEqual(response.status_code, 200)
		c.logout()
		# Test POST
		request = self.factory.post('/users/recruit/')
		request.user = UserViewsTestCase.user_boss
		response = recruit(request)
		self.assertEqual(response.status_code, 200)
		request = self.factory.post('/users/recruit/')
		request.user = AnonymousUser()
		response = recruit(request)
		self.assertEqual(response.status_code, 302)
		
	def test_productivity_index(self):
		url = '/productivity_index/'
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertTemplateUsed(response, 'user_views/productivity_index.html')
		self.assertEqual(response.status_code, 200)
		c.logout()
	

class UserFormsTestCase(TestCase):
	''' Test forms in users app'''
	def test_PersonForm_valid(self):
		data = {'username' : 'temp', 'email' : 'temp@temp.pl',
		 'first_name' : 'temp', 'surname' : 'temp',
		 'date_of_birth' : '1900-01-01', 'position' : 'BOS'
		 , 'password' : 'aaaa', 'password_confirm': 'aaaa'}
		form = PersonForm(data = data)
		self.assertTrue(form.is_valid())

	def test_PersonForm_invalid_password(self):
		''' No password confirm '''
		data = {'username' : 'temp', 'email' : 'temp@temp.pl',
		 'first_name' : 'temp', 'surname' : 'temp',
		 'date_of_birth' : '1900-01-01', 'position' : 'BOS'
		 , 'password' : 'aaaa'}
		form = PersonForm(data = data)
		self.assertFalse(form.is_valid())

	def test_PersonForm_invalid_incomplete(self):
		''' Username not provided '''
		data = {'username' : '', 'email' : 'temp@temp.pl',
		 'first_name' : 'temp', 'surname' : 'temp',
		 'date_of_birth' : '1900-01-01', 'position' : 'BOS'
		 , 'password' : 'aaaa', 'password_confirm': 'aaaa'}
		form = PersonForm(data = data)
		self.assertFalse(form.is_valid())

	def test_PersonForm_save(self):
		''' Test save method '''
		data = {'username' : 'temp', 'email' : 'temp@temp.pl',
		 'first_name' : 'temp', 'surname' : 'temp',
		 'date_of_birth' : '1900-01-01', 'position' : 'BOS'
		 , 'password' : 'aaaa', 'password_confirm': 'aaaa'}
		form = PersonForm(data = data)
		self.assertIsInstance(form.save(), Person)

	def test_PersonChangeForm_valid(self):
		data = {'username' : 'temp', 'email' : 'temp@temp.pl',
		 'first_name' : 'temp', 'surname' : 'temp',
		 'date_of_birth' : '1900-01-01', 'position' : 'BOS'
		 , 'subordinates' : ''}
		form = PersonChangeForm(data = data)
		self.assertTrue(form.is_valid())

	def test_PersonChangeForm_invalid(self):
		''' No username '''
		data = {'username' : '', 'email' : 'temp@temp.pl',
		 'first_name' : 'temp', 'surname' : 'temp',
		 'date_of_birth' : '1900-01-01', 'position' : 'BOS'
		 , 'subordinates' : ''}
		form = PersonChangeForm(data = data)
		self.assertFalse(form.is_valid())

class PersonModelTestCase(TestCase):

	def test_Person_creation(self):
		person = Person.objects.create_user(username = 'temp_boss', password = 'temp_boss', position = "BOS" )
		self.assertIsInstance(person, Person)

	def test_Person_fields(self):
		person = Person.objects.create_user(username = 'temp_boss', password = 'temp_boss', position = "BOS" )
		self.assertEqual(person.username, "temp_boss")
		self.assertEqual(person.position, 'BOS')
		self.assertEqual(person.date_of_birth, '1900-01-01')
		self.assertIsInstance(person.personal_id, int)
		self.assertFalse(person.is_admin)

		
class AppsTestCase(TestCase):

	def test_apps(self):
		self.assertEqual(UsersConfig.name, 'users')

class UtilsTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_manager = Person.objects.create_user(username = 'temp_manager', password = 'temp_manager', position = "MAN")

	def test_calculate_productivity_index(self):
		''' Test if 0 if no tasks done and if user does not exist '''
		self.assertIsInstance(calculate_productivity_index(UtilsTestCase.user_manager.personal_id), int)
		self.assertEqual(calculate_productivity_index(UtilsTestCase.user_manager.personal_id), 0)
		self.assertEqual(calculate_productivity_index(30), 0)
