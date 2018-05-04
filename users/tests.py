from django.test import TestCase
from django.test import Client
from .views import index
from .models import Person

# Test methods from users app
class UserTestCase(TestCase):
	# Create some users for testing purposes
	def setUp(self):
		user_boss = Person.objects.create_user(username = 'temp_boss', password = 'temp_boss', position = "BOS" )
		user_manager = Person.objects.create_user(username = 'temp_manager', password = 'temp_manager', position = "MAN")
		user_worker = Person.objects.create_user(username = 'temp_worker', password = 'temp_worker', position = "WOR")



	# Test index method
	def test_index(self):
		url = ''
		response = self.client.get(url)
		# Check response code - if 200 then its ok
		self.assertEqual(response.status_code, 200)
		# Check if correct template has been used
		self.assertTemplateUsed(response,  'user_views/uniformed_view.html')
		# Check if returned template contains 'Login here'
		self.assertContains(response, 'Login here')

		# Login as temporary boss user
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)

		# Check if template containt 'Recruit' option
		self.assertContains(response, 'Recruit')
		# Check if template contains ' Assing Task' option
		self.assertContains(response, 'Assign Task')

		c.logout()

		# Login as temporary manager user
		c = Client()
		c.login(username = 'temp_manager', password = 'temp_manager')
		response = c.get(url)

		# Check if template contains 'Edit subordinate' option
		self.assertContains(response, 'Edit subordinate')

		c.logout()

		# Login as temporary worker user
		c = Client()
		c.login(username = 'temp_worker', password = 'temp_worker')
		response = c.get(url)

		# Check if template does not contain 'Recruit' option
		self.assertNotContains(response, 'Recruit')

		c.logout()


	# Test logout function
	def test_logout_user(self):
		url = '/logout/'
		response = self.client.get(url)
		# Check if code is 302 - redirection found
		self.assertEqual(response.status_code, 302)


	# Test login function
	def test_login_user(self):
		url = '/login/'
		# Test when user is loged in
		c = Client()
		c.login(username = 'temp_worker', password = 'temp_worker')
		response = c.get(url)
		self.assertRedirects(response, "/" )
		c.logout()





