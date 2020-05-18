from django.urls import reverse
from rest_framework import status
from rest_framework.test import RequestsClient
import unittest
from rest_framework.test import APITestCase, APIClient

class TestMethods(APITestCase):

    def test_post(self):
        self.client = APIClient()
        self.url = 'http://localhost:8000/parking'
        self.data = {'plate': 'AAA-9999'}
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
    
    def test_put_pay(self):
        self.client = APIClient()
        self.url = 'http://localhost:8000/parking/1/pay'
        self.response = self.client.put(self.url)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        
    def test_put_out(self):
        self.client = APIClient()
        self.url = 'http://localhost:8000/parking/1/out'
        self.response = self.client.put(self.url)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_hist(self):
        self.client = APIClient()
        self.url = 'http://localhost:8000/parking/AAA-9999'
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
