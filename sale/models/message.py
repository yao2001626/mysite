
from .auth import Account


class BaseModel(models.Model):
	owner = models.ForeignKey(Account, verbose_name=u'账户')
	name = models.CharField(u'显示名称', max_length=100, help_text=u'该名称仅用于列表显示')
	created = models.DateTimeField(u'创建时间', auto_now_add=True)
	
	def __unicode__(self):
		return self.name
		
	class Meta:
		abstract = True
		
class NewsMsgItem(BaseModel):
	title = models.CharField(u'标题', max_length=100)
    description = models.CharField(u'描述', max_length=2000)
    pic_large = models.ImageField(upload_to=news_large_pic_rename, verbose_name=u'大图', help_text=u'为保证显示效果，请上传大小为360*200（或同比例）的图片')
    pic_small = models.ImageField(upload_to=news_small_pic_rename, verbose_name=u'小图', help_text=u'为保证显示效果，请上传大小为200*200（或同比例）的图片')
    url = models.URLField(u'跳转链接')
    
    def __unicode__(self):
    	return self.title
	class Meta:
		app_label = 'weixin'
		verbose_name = u'图文消息主体'
		verbose_name_plural = u'图文消息主体'
		
class MediaItem(BaseModel):
	
	title = models.CharField(u'标题', max_length=100)
	description = models.CharField(u'描述', max_length=2000)
	file = models.FileField(upload_to=media_file_rename, verbose_name=u'文件', help_text=u'上传的文件不大于5M')

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'weixin'
		verbose_name = u'媒体文件'
		verbose_name_plural = u'媒体文件'
		
class NewsMsg(BaseModel):
	items = models.ManyToManyField(NewsMsgItem, verbose_name=u'图文消息', through='NewsMsgItemMapping', help_text=u'消息主体，最多支持10个。')
	def __unicode__(self):
		return self.name
	class Meta:
		app_label = 'weixin'
		verbose_name = u'图文消息'
		verbose_name_plural = u'图文消息'
		
class NewsMsgItemMapping(models.Model):
	newsmsg = models.ForeignKey(NewsMsg)
	newsmsgitem = models.ForeignKey(NewsMsgItem, verbose_name=u'消息')
	position = models.IntegerField(default=1, verbose_name=u'排序')
	
	def __unicode__(self):
		return u'{0} --> {1}'.format(self.newsmsg, self.newsmsgitem)
	
	class Meta:
		app_label = 'weixin'
		db_table = 'weixin_msg_newsmsg_items'
		ordering = ['position']
		verbose_name = u'图文消息关联'
		verbose_name_plural = u'图文消息关联'
		
class TextMsg(BaseModel):

	content = models.CharField(u'内容', max_length=2000,
	                           help_text=u'消息内容')
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'weixin'
		verbose_name = u'文字消息'
		verbose_name_plural = u'文字消息'
		
class MsgReplyRule(BaseModel):
	agent = models.ForeignKey(QyAgent, verbose_name=u'企业应用', null=True, blank=True)
	
	# 消息响应类型
	res_msg_type = models.CharField(u'响应处理方式', max_length=10, choices=RES_MSG_TYPE,
	                                help_text=u'内部处理表示由本应用通过指定的返回内容对消息进行响应，'
	                                          u'外部处理表示由外部应用对消息进行处理，再交由本应用回复到用户。'
	                                          u'其中同步处理表示本应用会等待处理接口并实时返回，'
	                                          u'异步处理表示本应用会直接返回用户空信息，在接收到处理结果后再向用户返回。'
	                                          u'注意外部异步处理需要使用到微信客服接口，如无该接口权限，则该模式无法实现。')
	# 当消息在外部处理时，需要指定此队列池编号
	pool = models.CharField(u'队列池编号', max_length=4, null=True, blank=True)
	
	# 消息主体
	msg_object_content_type = models.ForeignKey(ContentType, related_name='msg_obj', limit_choices_to=msg_limit,
	                                            verbose_name=u'响应消息类型', null=True, blank=True,
	                                            help_text=u'指定返回的消息类型')
	msg_object_object_id = models.CharField(max_length=255, verbose_name=u'关联消息', null=True, blank=True,
	                                        help_text=u'要返回的消息主体')
	msg_object = generic.GenericForeignKey('msg_object_content_type', 'msg_object_object_id')
	
	is_valid = models.BooleanField(u'是否生效', default=True)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'weixin'
		verbose_name = u'消息响应规则'
		verbose_name_plural = u'消息响应规则'
		
class Keyword(BaseModel):
    """
    关键字，每个关键字都会对应一个消息响应规则
    """

	rule = models.ForeignKey(MsgReplyRule, verbose_name=u'关联规则')
	exact_match = models.BooleanField(u'完全匹配')
	
	def __unicode__(self):
		return self.name
		
class EventReplyRule(BaseModel):
	agent = models.ForeignKey(QyAgent, verbose_name=u'企业应用', null=True, blank=True)
	event_type = models.CharField(u'事件类型', choices=EVENT_TYPE, max_length=20)
	event_key = models.CharField(u'事件KEY值', max_length=50, blank=True)
	
	# 消息响应类型
	res_msg_type = models.CharField(u'响应处理方式', max_length=10, choices=RES_MSG_TYPE,
	                                help_text=u'内部处理表示由本应用通过指定的返回内容对消息进行响应，'
	                                          u'外部处理表示由外部应用对消息进行处理，再交由本应用回复到用户。'
	                                          u'其中同步处理表示本应用会等待处理接口并实时返回，'
	                                          u'异步处理表示本应用会直接返回用户空信息，在接收到处理结果后再向用户返回。'
	                                          u'注意外部异步处理需要使用到微信客服接口，如无该接口权限，则该模式无法实现。')
	# 当消息在外部处理时，需要指定此队列池编号
	pool = models.CharField(u'队列池编号', max_length=4, null=True, blank=True)
	
	# 消息主体
	msg_object_content_type = models.ForeignKey(ContentType, related_name='event_msg_obj', limit_choices_to=msg_limit,
	                                            verbose_name=u'响应消息类型', null=True, blank=True,
	                                            help_text=u'指定返回的消息类型')
	msg_object_object_id = models.CharField(max_length=255, verbose_name=u'关联消息', null=True, blank=True,
	                                        help_text=u'要返回的消息主体')
	msg_object = generic.GenericForeignKey('msg_object_content_type', 'msg_object_object_id')
	
	is_valid = models.BooleanField(u'是否生效', default=True)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'weixin'
		verbose_name = u'事件响应规则'
		verbose_name_plural = u'事件响应规则'
