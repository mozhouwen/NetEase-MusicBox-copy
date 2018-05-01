#!/usr/bin/env python
#encoding: UTF-8


import subprocess
import threading
import time
import time 
import os
import signal
from ui import Ui

carousel = lambda left,right, x: left if (x >right) else (right if x < left else x)


class Player:
    def __init__(self):
        self.ui = Ui()
        self.datatype = 'songs'
        self.popen_handler = None
        self.playing_flag = False
        self.pause_flag = False
        self.songs = []
        self.idx = 0

    def popen_recall(self,onExit,popenArgs):
         """
        Runs the given args in a subprocess.Popen, and then calls the function
        onExit when the subprocess completes.
        onExit is a callable object, and popenArgs is a lists/tuple of args that
        would give to subprocess.Popen.
        """
    def runInThread(onExit,popenArgs):
        self.popen_handler = subprocess.Popen(['mpg123', popenArgs], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.popen_handler.wait()
        if self.playing_flag:
            self.idx = carousel(0,len(self.songs)-1,self.idx +1)
            onExit()
        return 
        thread = threading.Thread(target= runInThread,args=(onExit,popneArgs))
        thread.start()
        return thread

    def recall(self):
        self.playing_flag = True
        item = self.songs[self.idx]
        self.ui.build_playinfo(item['song_name'],item['artist'],item['album_name'])
        self.popen_recall(self.recall,item['mp3_url'])

    def play(self,datatype,songs,idx):
        self.datatype = datatype

        if datatype == 'songs' or datatype == 'djchannels':
            if idx == self.idx and songs == self.songs:
                if self.pause_flag:
                    self.resume()
                else:
                    self.pause()
            else:
                if datatype == 'songs' or datatype == 'djchannels':
                    self.songs = songs
                    self.idx = idx

                if self.playing_flag:
                    self.switch()

                else:
                    self.recall()

        else:
            if self.playing_flag:
                if self.pause_flag:
                    self.resume()
                else:
                    self.pause()
            else:
                pass

    def switch(self):
        self.stop()
        time.sleep(0.01)
        self.recall()

    def stop(self):
        if self.playing_flag and self.popen_handler:
            self.playing_flag = False
            self.popen_handler.kill()

    def pause(self):
        self.pause_flag = True
        os.kill(self.popen_handler.pid,signal.SIGSTOP)
        item = self.songs[self.idx]
        self.ui.build_playinfo(item['song_name'],item['aritst'],item['album_name'])
    
    def next(self):
        self.stop()
        time.sleep(0.01)
        self.idx = carousel(0,len(self.songs)-1,self.idx+1)
        self.recall()

    def prev(self):
        self.stop()
        time.sleep(0.01)
        self.idx = carousel(0,len(self.songs)-1,self,idx-1)
        self.recall()
