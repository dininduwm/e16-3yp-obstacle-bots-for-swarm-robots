from django.test import  TestCase, Client
from django.urls import reverse
from schedules.models import BotServer, Schedule
from django.contrib.auth import get_user_model
import json

class TestViews(TestCase):   

    # checking for redirection if the user is not authenticated
    def test_schedule_list_GET_not_authenticated(self):
        client = Client()
        response = client.get(reverse('schedules:list'))
        # checking for redirect if we does not logged in
        # cheking for redirects if user is not logged in
        self.assertEquals(response.status_code, 302)

    
    # try the same with authenticated user
    def test_schedule_list_GET_authenticated(self):
        # create a tempory user
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        # do a login
        self.client.login(username='temporary', password='temporary')
        # try to enter to the shedule list as normal user
        response = self.client.get(reverse('schedules:list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedules/schedule_list.html')

    
    # checking for redirection if the user is not authenticated
    def test_schedule_create_GET_not_authenticated(self):
        client = Client()
        response = client.get(reverse('schedules:create'))
        # checking for redirect if we does not logged in
        # cheking for redirects if user is not logged in
        self.assertEquals(response.status_code, 302)

    
    # try the same with authenticated user
    def test_schedule_create_GET_authenticated(self):
        # create a tempory user
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        # do a login
        self.client.login(username='temporary', password='temporary')
        # try to proceed to create schedule page 
        response = self.client.get(reverse('schedules:create'))
        self.assertEquals(response.status_code, 200)
        # TODO: change the html render page
        self.assertTemplateUsed(response, 'schedules/unauthorized.html')
        

    # try admin page with a normal user this should fail
    def test_botServer_create_GET_with_normal_authenticated(self):
        # create a normal user
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/admin/schedules/botserver/')
        # server should issue a redirection if normal user tries to add a server
        self.assertEquals(response.status_code, 302)