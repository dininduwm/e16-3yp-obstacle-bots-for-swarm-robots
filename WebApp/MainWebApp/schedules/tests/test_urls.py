from django.test import SimpleTestCase
from django.urls import reverse, resolve
from schedules.views import schedule_list, schedule_create

class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('schedules:list')
        self.assertEquals(resolve(url).func, schedule_list)

    def test_create_url_is_resolved(self):
        url = reverse('schedules:create')
        self.assertEquals(resolve(url).func, schedule_create)