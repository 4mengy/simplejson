#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint

from lexer import Lexer


class SyntaxError(Exception):
    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        return ''.join([i for i in self.args])


class Parser:
    def __init__(self, _input, k=1):
        self._input = Lexer(_input)
        self.k = k
        self.p = 0
        self.look_ahead = []
        for i in range(k):
            token = self._input.next_token()
            self.look_ahead.append(token)
            self.p = (self.p + 1) % self.k

    def consume(self):
        token = self.look_ahead[self.p]
        self.look_ahead[self.p] = self._input.next_token()
        self.p = (self.p + 1) % self.k
        return token

    def lt(self, i):
        token = self.look_ahead[(self.p + i - 1) % self.k]
        return token

    def la(self, i=1):
        token = self.lt(i)
        return token.type

    def match(self, token_type):
        _type = self.la()
        if _type == token_type:
            return True
        return False

    def object(self):
        if self.match(Lexer.L_PARENTHESES):
            token = self.consume()
            if self.match(Lexer.R_PARENTHESES):
                self.consume()
                return {}
            else:
                mem = self.members()
                self.match(Lexer.R_PARENTHESES)
                self.consume()
                return mem

    def members(self):
        d = {}
        d.update(self.pair())
        if self.match(Lexer.COMMA):
            self.consume()
            d.update(self.members())
        return d

    def pair(self):
        if self.match(Lexer.STRING):
            token = self.consume()
            key = token.val
            if self.match(Lexer.COLON):
                self.consume()
                val = self.value()
                return {key: val}

    def value(self):
        if self.match(Lexer.STRING):
            val = self.consume().val
        elif self.match(Lexer.NUMBER):
            val = self.consume().val
        elif self.match(Lexer.TRUE):
            val = self.consume().val
        elif self.match(Lexer.FALSE):
            val = self.consume().val
        elif self.match(Lexer.NULL):
            val = self.consume().val
        elif self.match(Lexer.L_PARENTHESES):
            val = self.object()
        elif self.match(Lexer.L_BRACKETS):
            val = self.array()
        return val

    def array(self):
        if self.match(Lexer.L_BRACKETS):
            self.consume()
            if self.match(Lexer.R_BRACKETS):
                self.consume()
                return []
            else:
                val = self.elements()
                if self.match(Lexer.R_BRACKETS):
                    self.consume()
                    return val

    def elements(self):
        elem = []
        elem.append(self.value())
        if self.match(Lexer.COMMA):
            self.consume()
            elem.extend(self.elements())
        return elem

