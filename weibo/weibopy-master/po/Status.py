class Status:
    def __init__(self):
        self.sid = None
        self.mid = None
        self.idstr = None
        self.text = None
        self.source = None
        self.create_at = None
        self.reposts_count = 0
        self.comments_count = 0
        self.attitude_count = 0
        self.favorited = False
        self.truncated = False
		self.bmiddle_pic = None
    def setStatus(self, status):
        self.status = status
    def setUser(self, user):
        self.user = user
    def setGeo(self, geo):
        self.geo = geo
    def setComments(self, comments):
        self.comments = comments

if __name__ == '__main__':
    status = Status()
    print "Status Info: %s %s"% (status.sid, status.reposts_count)


