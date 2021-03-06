﻿from django.db import models

from .auth import Account


class User(models.Model):
	"""
	微信用户
	"""
	belonging = models.ForeignKey(Account, verbose_name=u'账户')
	openid = models.CharField(u'OpenID', max_length=64)
	created = models.DateTimeField(u'创建日期', auto_now_add=True)

	is_valid = models.BooleanField(u'是否有效', default=True)
	# 当用户取消关注时，此项为 True
	is_deleted = models.BooleanField(u'取消关注', default=False)

	def __unicode__(self):
		return self.openid

	class Meta:
		app_label = 'weixin'
		verbose_name = u'微信用户'
		verbose_name_plural = u'微信用户'
