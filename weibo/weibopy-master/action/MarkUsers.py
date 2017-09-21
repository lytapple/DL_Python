#!/usr/bin/python
# -*- coding: utf-8 -*-

#import numpy as np
import pandas as pd
import os.path
import time

import optparse


def printUserInfo(user):
    print '''
    用户 ID: {0}
    用户名称: {1}
    个人描述: {2}
    用户博客地址: {3}
    用户的个性化域名: {4}
    微号: {5}
    性别: {6}
    粉丝数: {7}
    互粉数: {8}
    关注数: {9}
    微博数: {10}
    收藏数: {11}
    注册时间: {12}
    是否允许所有人给我发私信: {13}
    是否允许所有人对我的微博进行评论: {16}
    是否允许标识用户的地理位置: {14}
    是否认证: {15}
    认证原因: {17}
    '''.format(*user)


def mark(filepath, order, raw_users):
    tmpt_file_path = os.path.dirname(filepath) + '/mark_tmp'

    begin = 0
    if os.path.exists(tmpt_file_path):
        with open(tmpt_file_path, 'r') as f:
            # last finished position
            begin = f.readline()

    begin = raw_users.index.get_loc(int(begin)) + 1 if bool(begin) else 0
    mark_tmp = open(tmpt_file_path, 'w')

    start = time.time()

    print '''
    What is his/her credibility level ?
    ( 3 : almost certainly unbelievable,
      2 : likely to be unbelievable,
      1 : likely to be believable,
      0 : almost certainly believable)
    '''

    # sentinel for to_csv
    last = begin
    for index in raw_users.index[begin:]:
        printUserInfo(raw_users.ix[index, :])
        credibility = raw_input('What is his/her credibility level ?\n')
        raw_users.ix[index, 'credibility' + order] = credibility
        if (index + 1 - begin) % 20 == 0:
            mark_tmp.seek(0)
            mark_tmp.write(str(index) + '\n')
            mark_tmp.flush()
            if begin == 0 and last - begin == 0:
                header = True
            else:
                header = False
            raw_users.ix[index - 20 + 1: index].to_csv(filepath, mode='a',
                                                       header=header)

            last = index

            print "Current record {0} has been written down".format(index)
            print "Cost Time: {0} minute(s).".format((time.time() - start)/60)
            if (raw_input("Continue(yes[y]/no[n]): ")[0] == 'n'):
                mark_tmp.close()
                return

    mark_tmp.close()

    if begin == 0 and last - begin == 0:
        header = True
    else:
        header = False

    raw_users.ix[last: index + 1].to_csv(filepath, mode='a', header=header)
    print "The Task has been finished. Thank you!"
    print "Cost Time: {0}".format(time.time() - start)


def main():
    parser = optparse.OptionParser('usage %prog '
                                   '-f <data_file>')
    parser.add_option('-f', dest='dfile', type='string',
                      help="specify data_file")
    (options, args) = parser.parse_args()
    if options.dfile is None:
        print parser.print_help()
        exit(0)

    raw_users = pd.read_csv(options.dfile, index_col=0)
    raw_users.index = raw_users.index.astype(int)

    if 'credibility1' not in raw_users.columns:
        raw_users['credibility1'] = None
        order = '1'
    elif 'credibility2' not in raw_users.columns:
        raw_users['credibility2'] = None
        order = '2'
    else:
        raw_users['credibility3'] = None
        order = '3'
    mark(options.dfile.replace('.csv', '.' + order + '-m.csv'), order,
         raw_users)

if __name__ == '__main__':
    main()
