class Geo:
	def __init__(self):
		self.longitude = None
		self.latitude = None
		self.city = None
		self.province = None
		self.city_name = ''
		self.province_name = ''
		self.address = ''
		self.address_pinyin = ''
		self.more = ''

	def setSatuses(self, statuses):
		self.statuses = statuses
	

if __name__ == '__main__':
	geo = Geo()
	print "Geo Info: %s %s" % (geo.longitude, geo.latitude)
