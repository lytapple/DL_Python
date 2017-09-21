class Comment:
	def __init__(self):
		self.cid = None
		self.mid = None
		self.idstr = None
		self.text = None
		self.source = None
		self.create_at = None

	def setReply2Comment(self, comment):
		self.reply2Comment = comment

	def setUser(self, user):
		self.user = user

if __name__ == '__main__':
	comment = Comment()
	print "Comment Info: %s %s" % (comment.cid, comment.text)
