from django.test import TestCase
from django.test import Client
from django.test import RequestFactory
from channels import Group
from .apps import ChatConfig
from .views import*
from .forms import ChatForm
from users.models import Person
from .models import ChatRoom
from .exceptions import ClientError
from .utils import get_room_or_error
from django.contrib.auth.models import AnonymousUser

# Views fully tested
class ChatViewsTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_boss = Person.objects.create_user(username = 'temp_boss', password = 'temp_boss', position = "BOS" )
		cls.test_chat_room = ChatRoom.objects.create(room_name = 'test_room')
		cls.test_chat_room.allowed_users.add(cls.user_boss)


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
		url = '/chat/1/'
		# Test if loged in and room exists (should display correct template)
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'chat/chat_room.html')
		# Test when there is no such room (should give 404 status code - not found)
		url = '/chat/30/'
		response = c.get(url)
		self.assertEqual(response.status_code, 404)
		c.logout()
		# Test if not loged in (should redirect)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)

	def test_chat_remove(self):
		url = '/chat/end/1/'
		# Test if loged in
		c = Client()
		c.login(username = 'temp_boss', password = 'temp_boss')
		response = c.get(url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/chat/')
		c.logout()


# Apps fully tested
class ChatAppsTestCase(TestCase):

	def test_app_name(self):
		self.assertEqual(ChatConfig.name, 'chat')


# Model fully tested
class ChatModelsTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.test_user = Person.objects.create_user(username = 'temp', password = 'temp', position = 'BOS')
		cls.test_chat_room = ChatRoom.objects.create(room_name = 'test_room')

	def test_str(self):
		''' Test __str__() method '''
		self.assertEqual(str(ChatModelsTestCase.test_chat_room), 'test_room')

	def test_ChatRoom_creation(self):
		''' Tests if ChatRoom object if created properly '''
		temp_test_chat_room = ChatRoom.objects.create(room_name = 'temp_test_room')
		self.assertIsInstance(temp_test_chat_room, ChatRoom)

	def test_ChatRoom_fields(self):
		ChatModelsTestCase.test_chat_room.allowed_users.add(ChatModelsTestCase.test_user)
		self.assertIsInstance(ChatModelsTestCase.test_chat_room.allowed_users.all()[0], Person)
		self.assertIsInstance(ChatModelsTestCase.test_chat_room.room_name, str)
		self.assertEqual(ChatModelsTestCase.test_chat_room.room_name, 'test_room')

	def test_send_message(self):
		message = 'test_message'
		self.assertEqual(ChatModelsTestCase.test_chat_room.send_message(message, ChatModelsTestCase.test_user), None)

	def test_websocket_group(self):
		self.assertIsInstance(ChatModelsTestCase.test_chat_room.websocket_group, Group)


# One method to go
class ChatExceptionsTestCase(TestCase):

	def test_creation(self):
		error = ClientError('USER_HAS_TO_LOGIN')
		self.assertIsInstance(error, ClientError)
		self.assertEqual(error.code, 'USER_HAS_TO_LOGIN' )

# One method to go
class ChatUtilsTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_boss = Person.objects.create_user(username = 'temp_boss', password = 'temp_boss', position = "BOS" )
		cls.test_chat_room = ChatRoom.objects.create(room_name = 'test_room')
		cls.test_chat_room.allowed_users.add(cls.user_boss)

	def test_get_room_or_error(self):
		# Test when not loged in - should raise ClientError
		temp_user = AnonymousUser()
		self.assertRaises(ClientError, get_room_or_error, ChatUtilsTestCase.test_chat_room.id, temp_user)
		self.assertRaisesRegex(ClientError, "USER_HAS_TO_LOGIN", get_room_or_error, ChatUtilsTestCase.test_chat_room.id, temp_user)
		# Test when no such room exists - should raise ClientError
		self.assertRaises(ClientError, get_room_or_error, 4, ChatUtilsTestCase.user_boss)
		self.assertRaisesRegex(ClientError, 'INVALID_ROOM', get_room_or_error, 4, ChatUtilsTestCase.user_boss)
		# Test if ok
		self.assertIsInstance(get_room_or_error(ChatUtilsTestCase.test_chat_room.id, ChatUtilsTestCase.user_boss), ChatRoom)
		self.assertEqual(get_room_or_error(ChatUtilsTestCase.test_chat_room.id, ChatUtilsTestCase.user_boss), ChatUtilsTestCase.test_chat_room)

