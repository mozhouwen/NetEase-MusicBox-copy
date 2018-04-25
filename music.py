#!/usr/bin/env python
#encoding: UTF-8

import curses
import locale
from api import Api
from player import Player
from ui import Ui
import sys


locale.setlocale(locale.LC_ALL,"")

code = locale.getpreferredencoding()

keymap = {
        'q':'quit',
        'j':'Next',
        'k':'Previous',
        'h':'Back',
        'l':'Forward',
        '[':'Previous Track',
        ']':'Next Track',
        'u':'Previous Page',
        'd':'Next Page',
        'f':'Next page',
        'space':'Play/Pause',
        'enter':'select'
        
        
        }


stack = []
step = 10

carousel = lambda left,right,x:left if (x>right) else (right if x < left else x)

class Menu:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('UTF-8')
        self.menus = {
                'title':'网易云音乐Python版',
                'curr':'main',
                'main':['排行榜','艺术家','新碟上架','网易精选集','DJ电台','搜索','登录'],
                'songs':[],
                'artists':[],
                'albums':[],
                'playlists':[]
                
                }

        self.menu_index = 0
        self.menu_offset = 0
        self.build = 'main'


        self.player = Player()
        self.ui = Ui()
        self.api = Api()
        self.screen = curses.initscr()
        self.screen.keypad(1)

    def menu_crtl(self):
        key = ''
        self.ui.build_menu(self.menus,self.menu_offset,self.menu_index,self.build,step)
        stack.append(['main',self.menus['title'],self.menus['main'],0,0])
        while key!= ord('q'):
            menus = self.menus
            build = self.build
            menu_index = self.menu_index
            menu_offset = self.menu_offset
            idx = menu_index
            key = self.screen.getch()
            self.ui.screen.refresh()

            if key == ord('k'):
                self.menu_index = carousel(menu_offset, min( len(menus[build]), menu_offset + step) - 1, idx-1 )

            elif key == ord('u'):
                if menu_offset == 0:
                    continue

                self.menu_offset -= step

                self.menu_index = (menu_index-step)//step*step


            elif key == ord('d'):
                if menu_offset + step >= len(menus[build]):
                    continue

                self.menu_offset += step

                self.menu_index = (menu_index+step)//step*step

            elif key == ord('\n') or key == ord(' '):
                if build == 'songs':
                    self.player.play(menus['songs',idx])
                    continue

            elif key == ord('l'):
                if self.build == 'songs':
                    continue
                self.dispatch_enter(idx)
                self.menu_index = 0
                self.menu_offset = 0

            elif key == ord('h'):
                if self.build =='main':
                    continue

                last = stack.pop()
                self.build = last[0]
                self.menus['title'] = last[1]
                self.menus[self.build] = last[2]
                self.menu_offset = last[3]
                self.menu_index = last[4]


            elif key == ord('f'):
                self.search()

            elif key == ord(']'):
                self.player.next()

            elif key == ord('['):
                self.player.prev()

            self.ui.build_menu(self.menus,self.menu_offset,self.menu_index,self.build.step)

        self.player.stop()

        curses.endwin()

    def diapatch_enter(self,idx):
        api = self.api
        menus = self.menus
        build = self.build
        menu_index = self.menu_index
        menu_offset = self.menu_offset

        stack.append([build,menus['title'],menus[build],menu_offset,menu_index])
        if build == 'main':
            self.choice_channel(idx)
            return 
        elif build == 'artists':
            artist_id = menus['artists'][idx]['artist_id']
            data = api.artists[artist_id]
            songs = data['hotSongs']
            self.build = 'songs'
            menus['songs'] = api.dig_info(songs,'songs')
            menus['title'] = '艺术家>'+menus['artists'][idx]['artists_name']
        elif build == 'albums':
            album_id = menus['albums'][idx]['album_id']
            data = api.album(album_id)
            songs = data['album']['songs']
            menus['songs'] = api.dig_info(songs,'songs')
            menus['title'] = '专辑>'+menus['albums'][idx]['albums_name']

        elif build == 'playlists':
            playlist_id = menus['playlists'][idx]['playlist_id']
            data = api.playlist_dateil(playlist_id)
            songs = data['result']['tracks']
            self.build = 'songs'
            menus['songs'] = api.dig_info(songs,'songs')
            menus['title'] = '网易精选集>'+menus['playlists'][oidx]['playlists_name']

    def choice_channel(self,idx):
        api = self.api
        if idx == 0:
            data = api.top_songlist()
            songs = data['songs']
            self.menus['songs']=api.dig_info(songs,'songs')
            self.menus['title'] = '排行版'
            self.build = 'songs'


        elif idx == 1:
            data = api.top_artists()
            artists = data['artists']
            self.menus['artists']= api.dig_info(artists,'aritsts')
            self.menus['title']='艺术家'
            self.build = 'artists'

        elif idx == 3:
            data = api.top_playlists()
            playlists = data['playlists']
            self.menus['playlists'] = api.dig_info(playlists,'playlists')
            self.menus['title']= '网易精选集'
            self.build = 'playlists'

        elif idx == 4:
            pass
        elif idx == 5:
            self.search()

        elif idx == 6:
            self.ui.build_login()


    def search(self):
        ui = self.ui
        x = ui.build_search_menu()
        if x in range(ord('1'),ord('5')):
            stack.append([self.build,self.menus['title'],self.menus[self.build],self.menu_offset,self.menu_index])
        if x == ord('1'):
            self.build = 'songs'
            self.menus['songs'] = ui.build_search('songs')
            self.menus['title'] = '歌曲搜索结果：'
            self.menu_index = 0
            self.menu_offset = 0

        elif x == ord('2'):
            self.build = 'artists'
            self.menus['artists'] = ui.build_search('artists')
            self.menus['title'] = '艺术家搜索结果'

        elif x == ord('3'):
            self.build = 'albums'
            self.menus['albums'] = ui.build_search('albums')
            self.menus['title'] = '专辑搜索结果：'
            self.menu_index =0
            self.menu_offset = 0

        elif x == ord('4'):
            self.build = 'playlists'
            self.menus['playlists'] = ui.build_search('playlists')
            self.menus['title']= '网易精选集搜索结果：'
            self.menu_index =0
            self.menu_offset = 0

Menu().menu_ctrl()

