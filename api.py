#!/usr/bin/env python
#encoding: UTF-8


import re
import json
import requests
import hashlib

def uniq(arr):
    arr2 = list(set(arr))
    arr2.sort(key=arr.index)
    return arr2

default_timeout = 10

class NetEase:
    def __init__(self):
        self.header = {
                'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
                }
        self.cookies = {
                'apppver':'1.5.2'
                
                }

        def httpRequest(self,method,action,query=None,urlencodes=None,callback=None,timeout=None):
            if(method=='GET'):
                url = action if (query==None) else(action+'?'+query)
                connection = requests.get(url,headers=self.header,timeout=default_time)

            elif(method == 'POST'):
                connection = requests.post(
                        action,
                        data = query,
                        headers = self.header,
                        timeout = default_timeout
                        
                        )

            connection.encoding = "UTF-8"
            connection = json.loads(connection.text)
            return connection

    def login(self,username,password):
        action = 'http://music.163.com/api/login/'
        data ={
                'username':username,
                'password':hashlib.md5(password).hexdigest(),
                'rememberLogin':'true'
                
                }
        try:
            return self.httpRequest('POST',action,data)
        except:
            return {'code':501}


    def user_playlist(self,uid,affset=0,limit=100):
        action = 'http://music.163.com/api/user/playlist/?offset=' + str(offset) + '&limit=' + str(limit) + '&uid=' + str(uid)
        try:
            data = self.httpRequest('GET',action)
            return data['playlist']

        except:
            return []


    def search(self,s,stype=1,offset=0,total='true',limit=60):
        action = 'http://music.163.com/api/search/get/web'
        data ={
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': 60
                
                }
        return self.httpRequest('POST',action,data)


    def new_albums(self,offset=0,limit=50):
        action = 'http://music/163.com/api/album/new?area=ALL&offset=' + str(offset) + '&total=true&limit=' + str(limit)
        try:
            data= self.httpRequest('GET',action)
            return data['albums']
        except:
            return []

    def top_playlists(self,category='全部',order='hot',offset=0,limit=50):
        action = 'http://music.163.com/api/playlist/list?cat=' + category + '&order=' + order + '&offset=' + str(offset) + '&total=' + ('true' if offset else 'false') + '&limit=' + str(limit)
        try:
            data = self.httpRequest('GET',action)
            return data['playlists']

        except:
            return []

    def playlist_detail(self,playlist_id):
        action = 'http://music.163.com/api/playlist/detail?id='+str(playlist_id)
        try:
            data = self.httpRequest('GET',action)
            return data['result']['track']
        except:
            return[]


    def top_artists(self,offset=0,limit=100):
        action = 'http://music.163.com/api/artist/top?offset=' + str(offset) + '&total=false&limit=' + str(limit)

        try:
            data = self.httpRequest('GET',action)
            return data['artists']
        except:
            return []


    def top_songlist(self,offset=0,limit=100):
        action = 'http://music.163.com/discover/toplist'
        try:
            connection = requests.get(action,headers=self.header,timeout=default_timeout)

            connection.encoding = 'UTF-8'
            songids = re.findall (r'/song\?id=(\d+)',connection.text)
            if songids == []:
                return []
            songids = uniq(songids)
            return self.songs_detail(songids)
        except:
            return []

    def artists(self,artist_id):
        action = 'http://music.163.com/api/artist/'+str(artist_id)
        try:
            data = self.httpRequest('GET',action)
            return data['hotSongs']
        except:
            return []

    def album(self,album_id):
        action = 'http://music.163.com/api/album/'+str(album_id)
        try:
            data = self.httpRequest('GET',action)
            return data['album']['songs']
        except:
            return []

    def songs_detail(self,ids,offset=0):
        tmpids = ids[offset:]
        tmpids = tmpids[0:100]
        tmpids = map(str,tmpids)
        action = 'http://music.163.com/api/song/detail?ids=['+(',').join(tmpids)+']'
        try:
            data = self.httpRequest('GET',action)
            return data['songs']
        except:
            return []


    def song_detail(self,music_id):
        action = "http://music.163.com/api/song/detail/?id="+str(music_id)+"&ids=[" + str(music_id) + "]"
        try:
            data = self.httpRequest('GET',action)
            return data['songs']

        except:
            return []

    def djchannels(self,stype=0,offset=0,limit=50):
        action = 'http://music.163.com/discover/djchannel?type='+str(stype)+'&offset=' + str(offset) + '&limit=' + str(limit)

        try:
            connection = requests.get(action,headers=self.header,timeout=default_timeout)
            connection.encoding = 'UTF-8'
            channelids = re.findall(r'/dj\?id=(\d+)',connection.text)
            channelids = uniq(channelids)
            return self.channel_detail(channelids)

        except:
            return []


    def channel_detail(self,channelids,offset=0):
        channels = []
        for i in range(0,len(channelids)):
            action = 'http://music.163.com/api/dj/program/detail?id=' + str(channelids[i])

            try:
                data = self.httpRequest('GET',action)
                channel = self.dig_info(data['program']['mainSong'],'channels')
                channel.append(channel)
            except:
                continue

        return channels
    def dig_info(self,data,dig_type):
        temp = []

        if dig_type == 'songs':
            for i in range(0,len(data)):
                song_info= {
                        
                        
                    'song_id': data[i]['id'],
                    'artist': [],
                    'song_name': data[i]['name'],
                    'album_name': data[i]['album']['name'],
                    'mp3_url': data[i]['mp3Url']
                    }

                if 'artist' in data[i]:
                    song_info['artist']= data[i]['artist']

                elif 'artists' in data[i]:
                    for j in range(0,len(data[i]['artists'])):
                        song_info['artist'].append(data[i]['artists'][j]['name'])
                    song_info['artist'] = ', '.join(song_info['artist'])

                else:
                    song_info['artist'] = '未知艺术家'
                temp.append(song_info)


        elif dig_type == 'artists':
            temp = []

            for i in range(0,len(data)):
                artists_info = {
                            'artist_id':data[i]['id'],
                            'artists_name':data[i]['name'],
                            'alias':''.join(data[i]['alias'])

                            }
                temp.append(artists_info)

            return temp

        elif dig_type == 'albums':
            for i in range(0,len(data)):
                albums_info = {
                        'album_id':data[i]['id'],
                        'albums_name':data[i]['name'],
                        'artists_name':data[i]['artist'][name]
                            }
                temp.append(albums_info)


        elif dig_type == 'playlists':
            for i in range(0,len(data)):
                playlists_info = {
                        'playlist_id':data[i]['id'],
                        'playlists_name':data[i]['name'],
                        'creator_name':data[i]['creator']['nickname']}
                temp.append(playlists_info)
                            
        elif dig_type == 'channels':
            channel_info = {
                    'song_id': data['id'],
                    'song_name': data['name'],
                    'artist': data['artists'][0]['name'],
                    'album_name': 'DJ节目',
                    'mp3_url': data['mp3Url']

                
                
                }
                            
                
            temp = channel_info

        return temp
