from DBHandler import DBHandler


class UserDAO:
    @staticmethod
    def store(user):
        cur = DBHandler.getConn().cursor()
        cur.execute('SET NAMES utf8mb4;')
        if UserDAO.isStored(cur, user) is True:
            print 'user{0} is already stored.'.format(user.id)
            cur.close()
            return

        sql = '''insert into users(userid,idstr,screen_name,name,province,city,
                 location,description,url,profile_url,user_domain,weihao,
                 gender,followers_count,bi_followers_count,friends_count,
                 statuses_count,favourites_count,ucreate_at,allow_all_act_msg,
                 geo_enabled,verified,allow_all_comment,verified_reason)
                 values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        value = []
        value.append(user.id)
        value.append('idstr' in user and user.idstr or None)
        value.append(user.screen_name)
        value.append(user.name)
        value.append('province' in user and user.province or None)
        value.append('city' in user and user.city or None)
        value.append('location' in user and user.location or None)
        value.append('description' in user and user.description or None)
        value.append(user.url)
        value.append('profile_url' in user and user.profile_url or None)
        value.append('domain' in user and user.domain or None)
        value.append('weihao' in user and user.weihao or None)
        value.append(user.gender)
        value.append(user.followers_count)
        value.append(user.bi_followers_count)
        value.append(user.friends_count)
        value.append(user.statuses_count)
        value.append(user.favourites_count)
        value.append('created_at' in user and user.created_at or None)
        value.append(user.allow_all_act_msg)
        value.append(user.geo_enabled)
        value.append(user.verified)
        value.append(user.allow_all_comment)
        value.append(user.verified_reason)

        cur.execute(sql, value)
        cur.close()

    @staticmethod
    def isStored(cur, user):
        sql = 'select * from users where userid={0}'.format(user.id)
        return cur.execute(sql) > 0