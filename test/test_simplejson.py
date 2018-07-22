#!/usr/bin/python
# -*- coding: utf-8 -*-


import unittest
from simplejson import SimpleJson


class TestSimpleJson(unittest.TestCase):
    def test_load(self):
        test = {
            '1': [1, True, [1, {'1': 45, '2': [5, 'dfsdfsdf']}]],
            '3': False,
            '5': None
        }
        s = '{"1":[1, true  , [1, {"1":45, "2": [5, "dfsdfsdf"]}]], ' \
            '"3":false , "5": null  }'
        json = SimpleJson.load(s)
        self.assertEqual(test, json)


if __name__ == '__main__':
    unittest.main()
