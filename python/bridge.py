#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Benjamin Milde'

import requests
import json
import redis

red = redis.StrictRedis()

def idFromTitle(title):
    return title.replace(' ','_').replace("'",'_')

#Abstracts away the details of communicating with the ambient server
class KeywordClientHttp():

    def __init__(self,server_url):
        self.server_url = server_url
        self.request_header = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def getSettings():
        r = requests.get(self.server_url+'getSettings')
        return r.json()
        
    def addRelevantEntry(self, type, title, text, url, score):
        data = {'handle':'addRelevantEntry','type':type,'entry_id': idFromTitle(title),'title':title,'text':text,'url':url,'score':score, 'insert_before': idFromTitle(title)}
        r = requests.post(self.server_url+'addRelevantEntry', data=json.dumps(data), headers=self.request_header)
        return r.status_code

    def delRelevantEntry(self, type, title):
        data = {'handle':'delRelevantEntry','type':type,'title': title, 'entry_id': idFromTitle(title)}
        r = requests.post(self.server_url+'delRelevantEntry', data=json.dumps(data), headers=self.request_header)
        return r.status_code

    def addUtterance(self, utterance,speaker):
        data = {'handle':'addUtterance','utterance':utterance,'speaker':speaker}
        r = requests.post(self.server_url+'addUtterance', data=json.dumps(data), headers=self.request_header)
        return r.status_code

    def replaceLastUtterance(self, old_utterance,new_utterance,speaker):
        data = {'handle':'replaceLastUtterance','old_utterance':old_utterance,'utterance':new_utterance,'speaker':speaker}
        r = requests.post(self.server_url+'replaceLastUtterance', data=json.dumps(data), headers=self.request_header)
        return r.status_code

    def completeUtterance(self, utterance, speaker):
        data = {'handle':'completeUtterance','utterance':utterance,'speaker':speaker}
        red.publish('ambient_transcript_only', json.dumps(data))

    def reset(self):
        data = {'handle':'reset'}
        red.publish('ambient_transcript_only', json.dumps(data))
        r = requests.post(self.server_url+'reset', data=json.dumps(data), headers=self.request_header)
        return r.status_code

#Do most of the message passing with redis, now standard version
class KeywordClient():

    def __init__(self,server_url):
        self.server_url = server_url
        self.request_header = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def getSettings():
        r = requests.get(self.server_url+'getSettings')
        return r.json()
        
    def addRelevantEntry(self, type, title, text, url, score):
        data = {'handle':'addRelevantEntry','type':type,'entry_id': idFromTitle(title),'title':title,'text':text,'url':url,'score':score, 'insert_before': idFromTitle(title)}
        red.publish('ambient', json.dumps(data))

    def delRelevantEntry(self, type, title):
        data = {'handle':'delRelevantEntry','type':type,'title': title, 'entry_id': idFromTitle(title)}
        red.publish('ambient', json.dumps(data))

    def addUtterance(self, utterance,speaker):
        data = {'handle':'addUtterance','utterance':utterance,'speaker':speaker}
        red.publish('ambient', json.dumps(data))

    def replaceLastUtterance(self, old_utterance,new_utterance,speaker):
        data = {'handle':'replaceLastUtterance','old_utterance':old_utterance,'utterance':new_utterance,'speaker':speaker}
        red.publish('ambient', json.dumps(data))

    def completeUtterance(self, utterance, speaker):
        data = {'handle':'completeUtterance','utterance':utterance,'speaker':speaker}
        red.publish('ambient_transcript_only', json.dumps(data))

    def reset(self):
        data = {'handle':'reset'}
        red.publish('ambient_transcript_only', json.dumps(data))
        r = requests.post(self.server_url+'reset', data=json.dumps(data), headers=self.request_header)
        return r.status_code