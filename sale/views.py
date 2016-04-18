from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import HttpResponse
from django.core.exceptions import PermissionDenied


class Hello(View):
	token="yaoshucai";
	
	def validate(self, request):
        signature = request.REQUEST.get('signature', '')
        timestamp = request.REQUEST.get('timestamp', '')
        nonce = request.REQUEST.get('nonce',  '')
        echo_str = request.REQUEST.get('echostr', '')

        l = [self.token, timestamp, nonce]
        l.sort()
        tmp_str = hashlib.sha1(''.join(l)).hexdigest()
        if tmp_str == signature:
            return True

        return False

def get(self, request):
        if self.validate(request):
            echo_str = request.REQUEST.get('echostr', '')
            return HttpResponse(echo_str)
        raise PermissionDenied
# Create your views here.
