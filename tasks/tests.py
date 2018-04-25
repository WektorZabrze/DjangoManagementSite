from django.test import TestCase
from .models import Task

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
