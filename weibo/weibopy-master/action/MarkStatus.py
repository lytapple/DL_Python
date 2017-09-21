#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
#import numpy as np
import time
import os.path

import optparse


def printStatus(status):
    print '''
    微博ID: {0}, 转发微博ID: {2}
    用户名: {1}, ＊用户可信度＊: {10}
    --------------------------------------------------------------
    内容: {3}
    --------------------------------------------------------------
    创建时间: {5}, 发布终端: {4}
    缩略图: {9}
    转发数: {6}, 评论数: {7}, 表态数: {8}
    '''.format(*status)


def printComment(comment):
    print '''
    评论ID : {0}, 回复的评论ID: {3}
    用户名: {2}, ＊用户可信度＊: {7}
    --------------------------------------------------------------
    内容： {4}
    --------------------------------------------------------------
    发布终端: {5}, 创建时间: {6}
    '''.format(*comment)


def main():

    parser = optparse.OptionParser(
        'usage %prog -s statuses_file -c comments_file')
    parser.add_option('-s', dest='sfile', type='string',
                      help="specify statuses file")
    parser.add_option('-c', dest='cfile', type='string',
                      help="specify comments file")
    (options, args) = parser.parse_args()
    if options.sfile is None or options.cfile is None:
        print parser.print_help()
        exit(0)

    comments = pd.read_csv(options.cfile, index_col=0)
    statuses = pd.read_csv(options.sfile, index_col=0)

    header = True
    if os.path.exists(os.path.dirname(options.sfile) + '/tmpt_file'):
        with open(os.path.dirname(options.sfile) + 'tmpt_file', 'r') as f:
            begin = int(f.readline()) + 1
        header = False
    else:
        begin = 0

    tmpt_file = open(os.path.dirname(options.sfile) + 'tmpt_file', 'w')

    if not 'DD' in statuses.columns:
        statuses['DD'] = None

    for sindex in statuses.index[begin:]:

        printStatus(statuses.ix[sindex])
        if (comments['sid'] == int(statuses.ix[sindex, 'sid'])).any():
            answer = raw_input("＊＊＊＊＊＊Show its comments?"
                               "(yes[y]/no[n])＊＊＊＊＊＊: ")

            if answer[0] == 'y':
                for cindex in comments[comments['sid'] ==
                                       statuses.ix[sindex, 'sid']].index:
                    time.sleep(4)
                    printComment(comments.ix[cindex])
        else:
            print "No comments Grabbed."

        if statuses.ix[sindex, 'DD'] is not None:
            print ('The DD of the status is {0}'.
                   format(statuses.ix[sindex, 'DD']))
            ic = raw_input("Please input the Credibility of the Status: ")
            statuses.ix[sindex, 'IC'] = ic
        else:
            DD = raw_input("Please input the DD of the Status: ")
            statuses.ix[sindex, 'DD'] = DD

        answer2 = raw_input("Continue next status?(yes[y]/no[n]): ")
        if answer2[0] == 'n':
            tmpt_file.write(str(sindex) + '\n')
            tmpt_file.flush()
            tmpt_file.close()
            break

    statuses.ix[begin:sindex].to_csv(os.path.dirname(options.sfile) +
                                     '/statuses-uc-dd.csv', mode='a',
                                     header=header)

if __name__ == '__main__':
    main()
