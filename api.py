#!/usr/bin/env python
#encoding: UTF-8

import re 
import json
import requests

class Api:
    def __init__(self):
        self.header = {
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip,deflate,sdch',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            # 'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 'DNT': 1,
            # 'Host': 'music.163.com',
            # 'Origin': 'http://music.163.com',
            'Referer': 'http://music.163.com/search/',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
                
                }

        self.cookies = {
                'appver':'1.5.2'
                }

        self.data = {
                's':'',
                'type':1,
                'offset':0,
                'total':'true',
                'limit':60
                
                }

        def httpRequest(self,method,action,query=None,urlencoded= None,callback=None,timeout=None):
            try:
                if(method == 'GET'):
                    url = action if (query==None)else(action + '?'+query)
                    connection = requests.get(url,headers=self.header,timeout=5)

                elif(method == 'POST'):
                    connection = requests.post(
                            action,
                            data = query,
                            #cookies = self.cookies,
                            headers = self.header,
                            timeout=5
                            
                            )
                    connection.encoding = "UTF-8"

            except requests.exceptions.Timeout:
                print('Request Time Out，Please Try Later...')

            except requests.exceptions.ConnectionError:
                print('Invalib Connection')


            else:
                connection.encoding = 'UTF-8'

                connection = json.loads(connection.text)
                return connection

        def search(self,s,stype = 1):
            action = 'http://music.163.com/api/search/get/web'
            self.data['s']=s
            self.data['type']= stype
            return self.httpRequest('POST',action,self.data)

        def new_albums(self,offset=0,limit=10):
            action = 'http://music.163.com/api/album/new?area=ALL&offset='+ str(offset)+'&total= true&limit='+str(limit)
            return self.httpRequest('GET',action)

        def top_playlists(self,order='hot',offset=0,limit=8):
            action = 'http://music.163.com/api/playlist/list?order=' + str(order) + '&offset=' + str(offset) + '&total=' + ('true' if offset else 'false') + '&limit=' + str(limit)
            return self.httpRequest('GET',action)

        def playlist_detail(self,playlist_id):
            action = 'http://music.163.com/api/playlist/detail?id='+str(playlist_id)
            return self.httpRequest('GET',action)

        def top_artists(self,offset=0,limit=20):
            action = 'http://music.163.com/api/artist/top?offset=' + str(offset) + '&total=false&limit=' + str(limit)
            return self.httpRequest('GET',action)

        def top_songlist(self,offset=0,limit=20):
            action = 'http://music.163.com/discover/toplist'
            connection = requests.get(action,headers = self.header,timeout=5)
            connection.encoding = 'UTF-8'
            songids = re.findall(r'/song\?id=(\d+)',connection.text)
            return self.songs_detail(songids)

        def artists(self,artist_id):
            action = 'http://music.163.con/api/artist/'
            return self.httpRequest('GET',action)
        # connection = requests.get(action, headers=self.header, timeout=5)
        # connection.encoding = 'UTF-8'
        # connection = connection.text.split('g_hotsongs = ')[1].split(';</script>')[0]
        # return json.loads(connection)


        def album(self,album_id):
            action = 'http://music.163.com/api/album/'+str(album_id)
            return self.httpRequest('GET',action)


        def songs_detail(self,ids,offset=0):
            tmpids = ids[offset:]
            tmpids = tmpids[0:100]
            tmpids = map(str,tmpids)
            action = 'http://music.163.com/api/song/detail?ids=[' + (',').join(tmpids) + ']'
            return self.httpRequest('GET',action)

        def song_detail(self,music_id):
            action = "http://music.163.com/api/song/detail/?id="+music_id + "&ids=[" + music_id + "]"
            return self.httpRequest('GET',action)


