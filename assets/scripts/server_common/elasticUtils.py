# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import gameconfig
import json
import redisUtils
import base64
import functools

FRIEND_AVATAR_INIT_STR = '''{
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "gbId": {
                "type": "long"
            }
        }
    }
}'''

FRIEND_AVATAR_INIT_STR_NGRAM = """
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ngram_analyzer": {
          "tokenizer": "ngram_tokenizer"
        }
      },
      "tokenizer": {
        "ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 3,
          "token_chars": ["letter", "digit"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "analyzer": "ngram_analyzer",
        "fields": {
            "raw": {
                "type": "keyword"
            }
        }
      },
      "gbId": {
        "type": "long"
      }
    }
  }
}
"""


class ElasticUtils(object):
    indexName = str(gameconfig.serverId()) + '_' + 'friend_ik'
    typeName = '_doc'

    @staticmethod
    @functools.lru_cache(4)
    def getRequestHeaders(user='', authStr='', isWithJson=False):
        headers = {}
        if authStr:
            userpass = '{}:{}'.format(user, authStr) if user else authStr
            auth = base64.b64encode(userpass.encode('utf-8')).decode('utf-8')

            headers['Authorization'] = 'Basic {}'.format(auth)

        if isWithJson:
            headers['Content-Type'] = 'application/json'

        return headers

    @staticmethod
    def methodGETHeaders():
        return ElasticUtils.getRequestHeaders(gameconfig.elasticUser(), gameconfig.elasticAuth())

    @staticmethod
    def methodPOSTHeaders():
        return ElasticUtils.getRequestHeaders(gameconfig.elasticUser(), gameconfig.elasticAuth(), True)

    @staticmethod
    def join(*args):
        return '/'.join(args)

    @staticmethod
    def uriBase():
        return ''.join(('http://', gameconfig.elasticServer(), ':', str(gameconfig.elasticPort())))

    @classmethod
    def init(cls, func, timeoutSec = 1):
        data = FRIEND_AVATAR_INIT_STR_NGRAM
        uri = cls.join(cls.uriBase(), cls.indexName)
        KBEngine.urlopenv2(uri, func, method='PUT',
                           postData=data.encode('utf-8'),
                           headers=cls.methodPOSTHeaders(),
                           timeoutSec=timeoutSec)

    @classmethod
    def checkInitSuccess(cls, func, timeoutSec = 1):
        url = cls.join(cls.uriBase(), cls.indexName)
        KBEngine.urlopenv2(url, func, method='GET',
                           headers=cls.methodGETHeaders(),
                           timeoutSec=timeoutSec)

    @classmethod
    def addAvatarElasticInfo(cls, name, gbId, obId, timeoutSec = 1):
        data = {'name': name,
                'gbId': gbId}

        data = json.dumps(data)
        uri = cls.join(cls.uriBase(), cls.indexName, cls.typeName, str(obId))

        def _func(httpcode, data, headers, success, url):
            DEBUG_MSG('ckz: elastic add:', httpcode, data, headers, success, url)

        KBEngine.urlopenv2(uri, _func, method='POST',
                           headers=cls.methodPOSTHeaders(),
                           postData=data.encode('utf-8'),
                           timeoutSec=timeoutSec)

    @classmethod
    def deleteById(cls, dbId, timeoutSec=1):
        uri = cls.join(cls.uriBase(), cls.indexName, cls.typeName, str(dbId))

        def _func(*args):
            DEBUG_MSG('delete:', *args)

        KBEngine.urlopenv2(uri, _func, method='DELETE',
                    headers=cls.methodGETHeaders(),
                    timeoutSec=timeoutSec)

    @classmethod
    def indexAvatarObId(cls, obId, callback, failedFunc, timeoutSec = 1):
        uri = cls.join(cls.uriBase(), cls.indexName, cls.typeName, obId) + '?pretty=true'

        def _func(httpcode, data, headers, success, url):
            if not (httpcode == 200 and success):
                failedFunc()
                return

            try:
                jsonData = json.loads(data)
                callback(True, jsonData)
            except Exception as e:
                WARNING_MSG('indexAvatarObId failed:', e)
                failedFunc()

        KBEngine.urlopenv2(uri, _func, method='GET',
            headers=cls.methodGETHeaders(),
            timeoutSec=timeoutSec)

    @classmethod
    def reqSearchAvatarName(cls, name, callback, failedFunc, timeoutSec=1):
        data = {
            'query': {
                'bool': {
                    'should': [
                        {
                            'match': {
                                'name': {
                                    'query': name,
                                    'operator': 'and'
                                }
                            }
                        },
                        {
                            'match': {
                                'name.raw': {
                                    'query': name,
                                    'operator': 'and'
                                }
                            }
                        },
                    ]
                }
            },
            'size': 50
        }
        data = json.dumps(data)
        uri = cls.join(cls.uriBase(), cls.indexName, cls.typeName, '_search')

        def _func(httpcode, data, headers, success, url):
            if not (httpcode == 200 and success):
                failedFunc()
                return

            try:
                jsonData = json.loads(data)
                hits = jsonData['hits']['hits']
                callback(hits)
            except Exception as e:
                WARNING_MSG('reqSearchAvatarName:', e)
                failedFunc()

        KBEngine.urlopenv2(uri, _func, method='POST', postData=data.encode('utf-8'), headers=cls.methodPOSTHeaders(), timeoutSec=timeoutSec)

    @staticmethod
    def _getRetData(data):
        retData = data['_source']
        retData['obId'] = int(data['_id'])
        return retData

    @classmethod
    def searchAvatarByName(cls, name, cb):
        def _failedFunc(*args):
            ERROR_MSG('searchAvatarByName failed:', args)

        if name.isdigit():
            cls.indexAvatarObId(
                name,
                lambda isSuccess, jsonData: cls._searchAvatarByNameAfterIndex(isSuccess, jsonData, name, cb),
                _failedFunc)
        else:
            cls._searchAvatarByNameAfterIndex(False, None, name, cb)

    @classmethod
    def _searchAvatarByNameAfterIndex(cls, isSuccess, jsonData, name, cb):
        _list = []
        if isSuccess:
            retData = cls._getRetData(jsonData)
            _list = [retData['gbId']]

        def _failedFunc(*args):
            ERROR_MSG('_searchAvatarByNameAfterIndex failed:', args)

        cls.reqSearchAvatarName(
            name,
            lambda hits: cls._searchAvatarByNameOnGetRet(hits, _list, name, cb),
            _failedFunc)

    @classmethod
    def _searchAvatarByNameOnGetRet(cls, hits, retList, name, cb):
        for data in hits:
            retData = cls._getRetData(data)
            retList.append(retData['gbId'])

        cb(retList)

    # 按照名字分词搜索部分
    # @classmethod
    # def _searchAvatarByName(cls, name, curList, cb):
    #     def _userInfoCB(retList):
    #         sendList = []
    #         for fcVal in retList:
    #             retData = retDict[fcVal.gbId]
    #             retData['school'] = fcVal.school
    #             retData['level'] = fcVal.level
    #             retData['sex'] = fcVal.sex
    #             sendList.append(retData)
    #
    #         box.onGetSearchFriendResult(sendList)
    #
    #     def _callback(hits):
    #         for data in hits:
    #             retData = cls._getRetData(data)
    #             if name not in retData['name']:
    #                 continue
    #
    #             retData['gbId'] = int(retData['gbId'])
    #
    #             retDict[retData['gbId']] = retData
    #
    #         if not retDict:
    #             box.onGetSearchFriendResult([])
    #             return
    #
    #         redisUtils.RedisUtils.getUsersInfo(list(retDict.keys()), _userInfoCB)
    #
    #     cls.reqSearchAvatarName(name, _callback, failedFunc)

    # idip按照名字分词搜索部分
    @classmethod
    def searchAvatarByFuzzyName(cls,fuzzyName,func,failedFunc):
        cls.reqSearchAvatarName(fuzzyName, functools.partial(searchAvatarByFuzzyNameAfter, cls,func), failedFunc)

def searchAvatarByFuzzyNameAfter(cls,func,hits):
    retDict = {}
    for data in hits:
        retData = cls._getRetData(data)
        retDict[retData['gbId']] = retData

    redisUtils.RedisUtils.getUsersInfo(list(retDict.keys()), functools.partial(getFuzzyNameUserInfo,func))

def getFuzzyNameUserInfo(func,retList):
    func(retList)
