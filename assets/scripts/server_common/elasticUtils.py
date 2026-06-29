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
    INDEX_NAME = str(gameconfig.serverId()) + '_' + 'friend_ik'
    TYPE_NAME = '_doc'

    @staticmethod
    @functools.lru_cache(10)
    def getRequestHeaders(user='', authStr='', isWithJson=False):
        _headers = {}
        if authStr:
            _userpass = '{}:{}'.format(user, authStr) if user else authStr
            auth = base64.b64encode(_userpass.encode('utf-8')).decode('utf-8')

            _headers['Authorization'] = 'Basic {}'.format(auth)

        if isWithJson:
            _headers['Content-Type'] = 'application/json'

        return _headers

    @staticmethod
    def methodPOSTHeaders():
        return ElasticUtils.getRequestHeaders(gameconfig.elasticUser(), gameconfig.elasticAuth(), True)

    @staticmethod
    def methodGETHeaders():
        return ElasticUtils.getRequestHeaders(gameconfig.elasticUser(), gameconfig.elasticAuth())

    @staticmethod
    def uriBase():
        _host = gameconfig.elasticServer()
        _port = str(gameconfig.elasticPort())
        return ''.join((
            'http://', 
            _host,
            ':', 
            _port,
        ))

    @staticmethod
    def join(*args):
        return '/'.join(args)

    @classmethod
    def init(cls, func, timeoutSec = 1):
        data = FRIEND_AVATAR_INIT_STR_NGRAM
        uri = cls.join(cls.uriBase(), cls.INDEX_NAME)
        KBEngine.urlopenv2(uri, func, method='PUT',
                           postData=data.encode('utf-8'),
                           headers=cls.methodPOSTHeaders(),
                           timeoutSec=timeoutSec)

    @classmethod
    def checkInitSuccess(cls, func, timeoutSec = 1):
        url = cls.join(cls.uriBase(), cls.INDEX_NAME)
        KBEngine.urlopenv2(url, func, method='GET',
                           headers=cls.methodGETHeaders(),
                           timeoutSec=timeoutSec)

    @classmethod
    def addAvatarElasticInfo(cls, name, gbId, obId, timeoutSec = 1):
        data = {
            'name': name,
            'gbId': gbId,
        }

        data = json.dumps(data)
        uri = cls.join(cls.uriBase(), cls.INDEX_NAME, cls.TYPE_NAME, str(obId))

        def _func(httpcode, data, headers, success, url):
            LOG_DBG('ckz: elastic add:', httpcode, data, headers, success, url)

        KBEngine.urlopenv2(uri, _func, method='POST',
                           headers=cls.methodPOSTHeaders(),
                           postData=data.encode('utf-8'),
                           timeoutSec=timeoutSec)

    @classmethod
    def deleteById(cls, dbId, timeoutSec=1):
        uri = cls.join(cls.uriBase(), cls.INDEX_NAME, cls.TYPE_NAME, str(dbId))

        def _func(*args):
            LOG_DBG('delete:', *args)

        KBEngine.urlopenv2(uri, _func, method='DELETE',
                    headers=cls.methodGETHeaders(),
                    timeoutSec=timeoutSec)

    @classmethod
    def indexAvatarObId(cls, obId, callback, failedFunc, timeoutSec = 1):
        uri = cls.join(cls.uriBase(), cls.INDEX_NAME, cls.TYPE_NAME, obId) + '?pretty=true'

        def _innerFunc(httpcode, data, headers, success, url):
            if not (httpcode == 200 and success):
                failedFunc()
                return

            try:
                _jsonData = json.loads(data)
                callback(True, _jsonData)
            except Exception as e:
                LOG_WARN('indexAvatarObId failed:', e)
                failedFunc()

        KBEngine.urlopenv2(uri, _innerFunc, method='GET',
            headers=cls.methodGETHeaders(),
            timeoutSec=timeoutSec)

    @classmethod
    def reqSearchAvatarName(cls, roleName, callback, failedFunc, timeoutSec=1):
        _data = {
            'query': {
                'bool': {
                    'should': [
                        {
                            'match': {
                                'name': {
                                    'query': roleName,
                                    'operator': 'and'
                                }
                            }
                        },
                        {
                            'match': {
                                'name.raw': {
                                    'query': roleName,
                                    'operator': 'and'
                                }
                            }
                        },
                    ]
                }
            },
            'size': 50
        }
        _data = json.dumps(_data)
        uri = cls.join(cls.uriBase(), cls.INDEX_NAME, cls.TYPE_NAME, '_search')

        def _func(httpcode, data, headers, success, url):
            if not (httpcode == 200 and success):
                failedFunc('search avatar failed', httpcode, success)
                return

            try:
                _jsonData = json.loads(data)
                hits = _jsonData['hits']['hits']
                callback(hits)
            except Exception as e:
                LOG_WARN('reqSearchAvatarName:', e)
                failedFunc('search avatar meet exception', e)

        KBEngine.urlopenv2(
            uri, 
            _func, 
            method='POST', 
            postData=_data.encode('utf-8'), 
            headers=cls.methodPOSTHeaders(), 
            timeoutSec=timeoutSec,
        )

    @staticmethod
    def _getRetData(data):
        _retData = data['_source']
        _retData['obId'] = int(data['_id'])
        return _retData

    @classmethod
    def searchAvatarByName(cls, name, cb):
        def _failedFunc(*args):
            LOG_ERR('searchAvatarByName failed:', args)

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
            LOG_ERR('_searchAvatarByNameAfterIndex failed:', args)

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



def searchAvatarByFuzzyNameAfter(cls,func,hits):
    _retDict = {}
    for data in hits:
        retData = cls._getRetData(data)
        _retDict[retData['gbId']] = retData

    redisUtils.RedisUtils.getUsersInfo(list(_retDict.keys()), functools.partial(getFuzzyNameUserInfo,func))

def getFuzzyNameUserInfo(func,retList):
    func(retList)
