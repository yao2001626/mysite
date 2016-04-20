

'''
api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
'''
class ConnectMixin(object):
	host = 'api.weixin.qq.com'
	port = '443'
	# configs for requesting access_token
	get_access_token_path = '/cgi-bin/token'
	req_access_token_method = 'GET'

    # configs for the specified request
	method = 'GET'
	path = ''
	params = {}
	data = {}

	num_retry = 3