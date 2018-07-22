#!/usr/bin/python
# -*- coding: utf-8 -*-


from parser import Parser


class SimpleJson:
    @staticmethod
    def load(text):
        parser = Parser(text)
        return parser.object()
