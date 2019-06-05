# -*- coding: utf-8 -*-
import unittest

from app.admin.services.GeoSN import *


class GeoSnTest(unittest.TestCase):
    def test_UpdateUrl(self):
        geosn = GeoSN("C:/Users/user/Downloads/geosn/")
        print(geosn.update())