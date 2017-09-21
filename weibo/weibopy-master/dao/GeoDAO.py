from DBHandler import DBHandler


class GeoDAO:
    @staticmethod
    def store(geo):
        cur = DBHandler.getConn().cursor()

        if GeoDAO.isStored(cur, geo) is True:
            print 'Geo({0},{1}) is already stored.'.\
                format(geo.longitude, geo.latitude)
            return

        sql = '''insert into geo(longitude,latitude,city,province,city_name,
                 province_name,address,address_pinyin,more)
                 values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        value = []
        value.append('longitude' in geo and geo.longitude or None)
        value.append('latitude' in geo and geo.latitude or None)
        value.append('city' in geo and geo.city or None)
        value.append('province' in geo and geo.province or None)
        value.append('city_name' in geo and geo.city_name or None)
        value.append('province_name' in geo and geo.province_name or None)
        value.append('address' in geo and geo.address or None)
        value.append('address_pinyin' in geo and geo.address or None)
        value.append('more' in geo and geo.more or None)
        cur.execute(sql, value)
        cur.close()

        return DBHandler.getConn().insert_id()

    @staticmethod
    def isStored(cur, geo):
        if 'longitude' in geo is False:
            return False
        sql = 'select * from geo where longitude={0} and latitude={0}'.\
            format(geo.longitude, geo.latitude)
        return cur.execute(sql) > 0
