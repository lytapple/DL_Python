class User:
	def __init__(self):
		self.uid = None
		self.idstr = None
		self.screen_name = None
		self.name = None
		self.province = None
		self.city = None
		self.location = None
		self.description = None
		self.url = None
		self.profile_url = None
		self.domain = None
		self.weihao = None
		self.gender = None
		self.followers_count = 0
		self.bi_followers_count = 0
		self.friends_count = 0
		self.statuses_count = 0
		self.favourites_count = 0
		self.creat_at = None
		self.allow_all_act_msg = False
		self.geo_enabled = False
		self.verified = False
		self.allow_all_comment = False
		self.verified_reason = None
	def setStatuses(self, statuses):
		self.statuses = statuses

if __name__ == '__main__':
	user = User()
	print "User Info: %s %s" % (user.screen_name, user.verified_reason)
