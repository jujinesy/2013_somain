#-*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)


from models import SomaUser

class MemberTest(TestCase):
    def setUp(self):
        # 유저를 몇개 추가한다.
        self.mentor_user1 = SomaUser.objects.create_user("test_mentor","te","st","test@test.com","2",
                100,"M","1999-01-01","111111-1111111", '02-111-1111',
                '010-111-1111', '1', '20', '/static/img/logo.gif', 'SW Maestro', '20',
                '20', '20', '1', '1', '1', 'SW Maestro', 'SW Maestro', 'SW Maestro' )

    def test_create_mentor_user(self):
        self.assertEqual(self.mentor_user1.username , "test_mentor")

    def test_mentor_user_type(self):
        self.assertEqual(self.mentor_user1.type , "2")
