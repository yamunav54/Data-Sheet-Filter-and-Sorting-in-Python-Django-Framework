from django.shortcuts import render, get_list_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import openpyxl
from datetime import datetime
import os
from django.conf import settings

from os import listdir
from os.path import isfile, join
import csv
import pandas as pd



import unittest

from views import sort
from views import filter

class Test_sort_filter(unittest.TestCase):

    def test_1(self):
        response_expected = HttpResponseRedirect("/")
        response = sort(request, pa= "sorting/{{ file }}:Flight Number")
        self.assertEqual(response, response)


if __name__ == '__main__':
    unittest.main()
