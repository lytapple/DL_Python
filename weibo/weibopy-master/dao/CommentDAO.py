from DBHandler import DBHandler


class CommentDAO:
    @staticmethod
    def store(comment):
        cur = DBHandler.getConn().cursor()
        cur.execute('SET NAMES utf8mb4;')
        if CommentDAO.isStored(cur, comment) is True:
            print "Comment{0} is already stored.".format(comment.id)
            cur.close()
            return

        sql = '''insert into comments(cid,sid,userid,reply2Id,mid_num, \
        idstr,ctext,csource,create_at) \
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        value = []
        value.append(comment.id)
        value.append('status' in comment and comment.status.id or None)
        value.append(comment.user.id)
        value.append('reply_comment' in comment and
                     comment.reply_comment.id or None)
        value.append('mid' in comment and comment.mid or None)
        value.append('idstr' in comment and comment.idstr or None)
        value.append(comment.text)
        value.append('source' in comment and comment.source or None)
        value.append('created_at' in comment and comment.created_at or None)
        cur.execute(sql, value)
        cur.close()

    @staticmethod
    def isStored(cur, comment):
        sql = 'select * from comments where cid={0}'.format(comment.id)
        return cur.execute(sql) > 0
