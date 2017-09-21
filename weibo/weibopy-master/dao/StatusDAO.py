from DBHandler import DBHandler


class StatusDAO:
    @staticmethod
    def store(status):
        cur = DBHandler.getConn().cursor()
        cur.execute('SET NAMES utf8mb4;')
        if StatusDAO.isStored(cur, status) is True:
            print 'Status{0} has already been stored, try to update...'.\
                format(status.id)
            sql = '''update status set reposts_count=%s,comments_count=%s,
            attitude_count=%s where sid={0}'''.format(status.id)
            value = []
            value.append(status.reposts_count)
            value.append(status.comments_count)
            value.append(status.attitudes_count)
            cur.execute(sql, value)
            cur.close()
            return

        sql = '''insert into status(sid,userid,retweetOfId,gid,mid_num,
        idstr,text,source,create_at,reposts_count, comments_count,
        attitude_count,favorited,truncated,bmiddle_pic)
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        value = []
        value.append(status.id)
        value.append(status.user.id)
        value.append('retweeted_status' in status and status.
                     retweeted_status.id or None)
        value.append('geo' in status and status.geo is not None
                     and status.geo.gid or None)
        value.append('mid' in status and status.mid or None)
        value.append('idstr' in status and status.idstr or None)
        value.append(status.text)
        value.append('source' in status and status.source or None)
        value.append('created_at' in status and status.created_at or None)
        value.append(status.reposts_count)
        value.append(status.comments_count)
        value.append(status.attitudes_count)
        value.append('favorited' in status and status.favorited or None)
        value.append('truncated' in status and status.truncated or None)
        value.append('bmiddle_pic' in status and status.bmiddle_pic or None)
        cur.execute(sql, value)
        cur.close()

    @staticmethod
    def isStored(cur, status):
        sql = 'select * from status where sid={0}'.format(status.id)
        return cur.execute(sql) > 0
