# -*- coding: utf-8 -*-
# @Author  : summer
import time


def application(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-Type', 'text/static')]
	start_response(status, response_headers)
	return str(environ) + '==Hello world from a simple WSGI application!--->%s\n' % time.ctime()
