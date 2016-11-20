#-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson as json

class KorzipTest(TestCase):
    def data_test(self):
        c = Client()
        response = c.get('/korzip/search?keyword=1')
        data = json.loads(response.content)
        self.assertEquals(data["status"], True)