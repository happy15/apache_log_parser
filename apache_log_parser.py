#!/usr/bin/env python
#coding: utf-8
#
# What's this?
# ============
# This module is intent to parse the most common log pattern 
# for apache, nginx, etc.
#
# Here we got two implementations:
# 1) use regex to parse the log, which is elegent, but slow
# 2) use string split to parse the log, which is way faster then 1)
#
# How to use it?
# ==============
# To parse a line of log, do:
#
# parse('123.126.50.69 - - [03/Jan/2012:00:00:02 +0800] ' +
#       '"GET /some/url/on/your/site HTTP/1.1" ' +
#       '200 5876 "-" ' +
#       '"User agent like Mozilla chrome or even spider(+http://www.spider.com/docs/help/webmasters.htm#07)"'))')
# or:
# fast_parse('123.126.50.69 - - [03/Jan/2012:00:00:02 +0800] ' +
#       '"GET /some/url/on/your/site HTTP/1.1" ' +
#       '200 5876 "-" ' +
#       '"User agent like Mozilla chrome or even spider(+http://www.spider.com/docs/help/webmasters.htm#07)"'))')
# 
# Thanks to
# =========
# Inspired by https://github.com/watsonian/apache_log_parser
# and kennethreitz's concept of 'python for human'.
#
# Reach me at
# ===========
# LUO Sheng
# sheng.peisi.luo@gmail.com
# @happy15sheng

import re


def parse(line):
    fmt = ('^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s' +
            '(.+)\s' +
            '(.+)\s' +
            '\[((.*)/(.*)/(.*)):(.*:.*:.*)\s(.*)]\s' +
            '\"(.*)\"\s' +
            '(\d+)\s' +
            '(\d+)\s' +
            '\"(.+)\"\s' +
            '\"(.*)\"$')
    m = re.search(fmt, line)

    try:
        return {'ip': m.group(1),
                'foo': m.group(2),
                'bar': m.group(3),
                'date': m.group(4),
                'day': m.group(5),
                'month': m.group(6),
                'year': m.group(7),
                'time': m.group(8),
                'timezone': m.group(9),
                'resource': m.group(10),
                'status': m.group(11),
                'size': m.group(12),
                'referer': m.group(13),
                'user_agent': m.group(14),
               }
    except:
        return None


def fast_parse(line):
    a = line.split()
    
    try:
        if len(a) >= 12:
            s = {'ip': a[0],
                    'foo': a[1],
                    'bar': a[2],
                    'date': a[3].split(':')[0][1:],
                    'time': ':'.join(a[3].split(':')[1:]),
                    'timezone': a[4][:-1],
                    'resource': (' '.join(a[5:8]))[1:-1],
                    'status': a[8],
                    'size': a[9],
                    'referer': a[10][1:-1],
                    'user_agent': (' '.join(a[11:]))[1:-1],
                }
        else:
            s = {'ip': a[0],
                    'foo': a[1],
                    'bar': a[2],
                    'date': a[3].split(':')[0][1:],
                    'time': ':'.join(a[3].split(':')[1:]),
                    'timezone': a[4][:-1],
                    'resource': (' '.join(a[5]))[1:-1],
                    'status': a[6],
                    'size': a[7],
                    'referer': a[8][1:-1],
                    'user_agent': (' '.join(a[9:]))[1:-1],
                }

        s['day'] = s['date'].split('/')[0]
        s['month'] = s['date'].split('/')[1]
        s['year'] = s['date'].split('/')[2]
        return s
    except:
        return None


def parse_resource(res):
    fmt = ('^([A-Z]+)\s(.+)\sHTTP/(\d+\.\d+)')
    m = re.search(fmt, res)

    try:
        return {'method': m.group(1),
                'url': m.group(2),
                'http_ver': m.group(3)
               }
    except:
        return None


def fast_parse_resource(res):
    a = res.split()
    
    if len(a) != 3:
        return None

    try:
        return {'method': a[0],
                'url': a[1],
                'http_ver': a[2][5:]
               }
    except:
        return None


if __name__ == "__main__":

    from pprint import pprint

    pprint(parse('123.126.50.69 - - [03/Jan/2012:00:00:02 +0800] ' +
                '"GET /some/url/on/your/site HTTP/1.1" ' +
                '200 5876 "-" ' +
                '"User agent like Mozilla chrome or even spider(+http://www.spider.com/docs/help/webmasters.htm#07)"'))
    pprint(parse('110.83.152.234 - - [03/Jan/2012:23:45:25 +0800] "-" 400 0 "-" "-"'))

    pprint(fast_parse('123.126.50.69 - - [03/Jan/2012:00:00:02 +0800] ' +
                '"GET /some/url/on/your/site HTTP/1.1" ' +
                '200 5876 "-" ' +
                '"User agent like Mozilla chrome or even spider(+http://www.spider.com/docs/help/webmasters.htm#07)"'))
    pprint(fast_parse('110.83.152.234 - - [03/Jan/2012:23:45:25 +0800] "-" 400 0 "-" "-"'))
   
    pprint(parse_resource('GET /some/url/on/your/site HTTP/1.1'))
    pprint(parse_resource('-'))

    pprint(fast_parse_resource('GET /some/url/on/your/site HTTP/1.1'))
    pprint(fast_parse_resource('-'))
