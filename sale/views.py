from django.shortcuts import render
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.core.exceptions import PermissionDenied
import hashlib

class Hello(View):
	token = "shucaiyao"
	@csrf_exempt
	def dispatch(self, *args, **kwargs):
		return super(Hello, self).dispatch(*args, **kwargs)

	def validate(self, request):
		signature = request.GET.get('signature' , None)
		timestamp = request.GET.get('timestamp', None)
		nonce = request.GET.get('nonce',  None)
		echo_str = request.GET.get('echostr', None)
		l = [self.token, timestamp, nonce]
		l.sort()
		tmp_str = "%s%s%s"%tuple(l)
		tmp_str = hashlib.sha1(tmp_str).hexdigest()
		
		if tmp_str == signature: #failed ==? signature and tmp_str
			return True
		raise PermissionDenied
		
	def get(self, request):
		if self.validate(request):
			echo_str = request.GET.get('echostr', '')
			return HttpResponse(echo_str)
		raise PermissionDenied
		