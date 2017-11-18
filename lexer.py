#!/usr/bin/python
# -*- coding: utf-8 -*-


class EndOfFile(Exception):
    pass


class UnCompleteToken(Exception):
    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        return ''.join([i for i in self.args])


_EOF = object()


class Token:
    def __init__(self, _type, val):
        self.type = _type
        self.val = val

    def __repr__(self):
        return '< {}, {} >'.format(self.val, Lexer.get_token_name(self.type))


class Lexer:
    EOF = 0
    L_PARENTHESES = 1
    R_PARENTHESES = 2
    STRING = 3
    NUMBER = 4
    TRUE = 5
    FALSE = 6
    NULL = 7
    L_BRACKETS = 8
    R_BRACKETS = 9
    COLON = 10
    COMMA = 11

    TOKEN_NAME = ['EOF', 'Left Parentheses', 'Right Parentheses', 'String', 'Number',
                  'True', 'False', 'Null', 'Left Brackets', 'Right Brackets', 'Colon',
                  'Comma']

    @staticmethod
    def get_token_name(token_type):
        return Lexer.TOKEN_NAME[token_type]

    def __init__(self, _input):
        self._input = _input
        self._pos = 0
        self._current_char = self._input[0]

    def __iter__(self):
        return self

    def __next__(self):
        _next = self.next_token()
        if _next.type == Lexer.EOF:
            raise StopIteration
        return _next

    def _consume(self):
        self._pos = self._pos + 1
        if len(self._input) > self._pos:
            self._current_char = self._input[self._pos]
        else:
            self._current_char = _EOF

    def _is_ws(self, char):
        if char.isspace():
            return True
        elif char == '\n' or char == '\r':
            return True
        return False

    def _is_digit(self, char):
        if ord('0') <= ord(char) <= ord('9'):
            return True
        return False

    def next_token(self):
        if self._current_char == _EOF:
            return Token(self.EOF, 'EOF')

        if self._is_ws(self._current_char):
            while self._is_ws(self._current_char):
                self._consume()

        if self._current_char == '{':
            self._consume()
            return Token(self.L_PARENTHESES, '{')
        elif self._current_char == '}':
            self._consume()
            return Token(self.R_PARENTHESES, '}')
        elif self._current_char == '[':
            self._consume()
            return Token(self.L_BRACKETS, '[')
        elif self._current_char == ']':
            self._consume()
            return Token(self.R_BRACKETS, ']')
        elif self._current_char == ':':
            self._consume()
            return Token(self.COLON, ':')
        elif self._current_char == ',':
            self._consume()
            return Token(self.COMMA, ',')
        elif self._current_char == '"':
            self._consume()
            string = []
            while True:
                if self._current_char == '\\':
                    self._consume()
                    if self._current_char == 't':
                        self._current_char = '\t'
                elif self._current_char == '"':
                    break
                elif self._current_char == _EOF:
                    raise UnCompleteToken('Expecting "}", get end of file.')
                string.append(self._current_char)
                self._consume()
            self._consume()
            return Token(self.STRING, ''.join(string))
        elif self._current_char == 't':
            self._consume()
            for i in ('r', 'u', 'e'):
                if self._current_char == i:
                    self._consume()
                    if i == 'e':
                        return Token(self.TRUE, True)
                else:
                    break
        elif self._current_char == 'f':
            self._consume()
            for i in ('a', 'l', 's', 'e'):
                if self._current_char == i:
                    self._consume()
                    if i == 'e':
                        return Token(self.FALSE, False)
                else:
                    break
        elif self._current_char == 'n':
            self._consume()
            for index, e in enumerate(('u', 'l', 'l')):
                if self._current_char == e:
                    self._consume()
                    if e == 'l' and index == 2:
                        return Token(self.NULL, None)
                else:
                    break
        elif self._is_digit(self._current_char):
            number = self._current_char
            self._consume()
            while self._is_digit(self._current_char):
                number += self._current_char
                self._consume()
            return Token(self.NUMBER, int(number))

        raise ValueError('Invalid character "{}" in pos {}.'.format(self._current_char, self._pos))