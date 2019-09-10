#! /usr/bin/python
# -*- coding: utf-8 -*-

__metaclass__ = type

import base64

class HTTPAuthorization:
    def __init__(self, username, password):
        self.username = username.encode()
        self.password = password.encode()

    def gen_authheader(self):
        # base64string = base64.encodestring('%s:%s' %(self.username, self.password))[:-1]

        # print(type(self.username))
        base64string = base64.b64encode(b'%s:%s' %(self.username, self.password))
        # print("base64string: ", base64string)
        # base64string = base64.b64encode('%s:%s' %(self.username, self.password))[:-1]
        # print("base64string: ", base64string)
        # base64string = base64.b64encode('%s:%s' %(self.username, self.password))
        self.authheader = "Basic %s" % base64string
        return self.authheader

if __name__ == '__main__':
    pass
