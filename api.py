#!/usr/bin/env python
#encoding: UTF-8


import re
import json
import requests


class Api:
    def __init__(self):
        self.header ={
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
                's': '',
                'type': 1,
                'offset': 0,
                'total': 'true',
                'limit': 60
                
                
                }
    def httpRequest(self,method,action,query = None,urlencoded= None,callback= None,timeout= None):
        try:
            if (method == 'GET'):
                url = action if (query==None)else(action+'?'+query)

                connection = requests.get(url,headers=self.header,timeout=5)

            elif(method=='POST'):
                connection = requests.post(
                        action,
                        data = query,
                        headers= self.header,
                        timeout=5
                         )

                connection.encoding = 'UTF-8'

        except requests.exceptions.Timeout:
            print('Request time out .please try later...')
            

        except requests.exceptions.ConnectionError:
            print('Invalid Connection')

        else:
            connection.encoding = "UTF-8"
            connection = json.loads(connection.text)
            return connection


    def search(self,s,stype=1):
        action = 'http://music.163.com/api/search/get/web'
        self.data['s'] = s
        self.data['type'] = stype
        return self.httpRequest('POST',action,self.data)

    def new_albums(self,offset=0,limit=50):
        action = 'http://music.163.com/api/album/new?area=ALL&offset=' + str(offset) + '&total=true&limit=' + str(limit)
        return self.httpRequest('GET',action)

    def top_playlists(self,order='hot',offset=0,limit=50):
        action = 'http://music.163.com/api/playlist/list?order=' + str(order) + '&offset=' + str(offset) + '&total=' + ('true' if offset else 'false') + '&limit=' + str(limit)

        return self.httpRequest('GET',action)

    def playlist_detail(self,playlist_id):
        action = 'http://music.163.com/api/playlist/detail?id='+str(playlist_id)
        return self.httpRequest('GET',action)


    
    def top_artists(self,offset=0,limit=100):
        action = 'http://music.163.com/api/artist/top?offset='+str(offset)+'&total=false&limit='+str(limit)
        return self.httpRequest('GET',action)

    
    def top_songlist(self,offset=0,limit=100):
        action = 'http://music.163.com/discover/toplist'
        connection = requests.get(action,header=self.header,timeout=5)
        connection.encoding = 'UTF-8'
        songids = re.findall(r'/song\?id=(\d+)',connection.text)
        return self.songs_detail(songids)


    def artists(self,artist_id):
        action = 'http://music.163.com/api/artist/'+str(arist_id)
        return self.httpRequest('GET',action)


    def album(self,album_id):
        action = 'http://music.163.com/api/album/'+str(album_id)
        return self.httpRequest('GET',action)

    def songs_detail(self,ids,offset = 0):
        tmpids = ids[offset:]
        tmpids = tmpids[0:100]
        tmpids = map(str,tmpids)
        action = 'http://music.163.com/api/song/detail?ids=['+(',').join(tmpids)+']'
        return self.httpRequest('GET',action)

    def song_detail(self,music_id):
        action =  action = "http://music.163.com/api/song/detail/?id=" + music_id + "&ids=[" + music_id + "]"
        return self.httpRequest('GET',action)

    def dig_info(self,data,dig_type):
        if dig_type == 'songs':
            temp = []
            for i in range(0,len(data)):
                song_info ={
                    'song_id': data[i]['id'],
                    'artist': [],
                    'song_name': data[i]['name'],
                    'album_name': data[i]['album']['name'],
                    'mp3_url': data[i]['mp3Url'] 
                        
                        }
                if 'artist' in data[i]:
                    song_info['artist']= data[i]['artist']
                elif 'artist' in data[i]:
                    for j in range(0,len(data[i]['artists'])):
                        song_info['artist'].append(data[i]['artists'][j]['name'])
                    song_info['artist'] = ','.join(song_info('artist'))
                else:
                    song_info['artist']='艺术家'

                temp.append(song_info)

            return temp

        if dig_type == 'artists':
            temp = []

            for i in range(0,len(data)):
                artists_info = {
                        'artist_id':data[i]['id'],
                        'artist_name':data[i]['name'],
                        'alias':''.join(data[i]['alias'])

                        
                        
                        }
                temp.append(artists_info)

            return temp

        if dig_type == 'alumbs':
            temp = []
            for i in range(0,len(data)):
                albums_info = {
                        'albums_info':data[i]['id'],
                        'albums_name':data[i]['name'],
                        'artists_name':data[i]['artist']['name']

                        
                        }
                temp.append(albums_info)
            return temp

        if dig_type == 'playlists':
            temp = []
            for i in range(0,len(data)):
                playlists_info = {
                        'playlist_id':data[i]['id'],
                        'playlists_name':data[i]['name'],
                        'creator_name':data[i]['creator']['nickname']

                        
                        }

                temp.append(playlists_info)

            return temp

