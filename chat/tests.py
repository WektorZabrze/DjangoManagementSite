from django.test import TestCase
from django.test import Client
from .apps import ChatConfig
from .views import*
from users.models import Person


class ChatAppsTestCase(TestCase):

	def test_app_name(self):
		self.assertEqual(ChatConfig.name, 'chat')

class ChatViewsTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_boss = Person.objects.create_user(username = 'temp_boss', password = 'temp_boss', position = "BOS" )

	def test_chat_list(self):
		url = '/chat/'
		# Test if loged in
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'chat/chat_list.html')
		c.logout()

		# Test if not loged in
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)

	def test_chat_add(self):
		url = '/chat/add/'
		# Test if loged in
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'chat/chat_form.html')
		c.logout()

		# Test if not loged in
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)

	def test_chat_view(self):
		url = '/chat/view/'
		# Test if loged in
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertEqual(response.status_code, 200)
		#self.assertTemplateUsed(response, 'chat/chat_room.html')
		c.logout()

		# Test if not loged in
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)		