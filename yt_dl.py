#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 2019

@author: OscarShiang
"""

import wx
import os
import json
import youtube_dl

file = open('setting_en.json', 'r', encoding = 'utf-8')
setting = json.loads(file.read())
file.close()

size = setting['size']

#### need to be revised
def getVideo(url, des):
    # load the setting in
    setup = setting['download']

    print(des)
    # dealing with the progress bar
    global progress
    progress = wx.GenericProgressDialog(title = setup['on_progress'], message = setup['init'], maximum = 100, style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)

    # starting to download the video
    opts = {
        'format': 'bestvideo+m4a',
        'outtmpl': des + '%(title)s.%(ext)s',
        'progress_hooks': [progress_Check],
        'merge_output_format': 'mp4',
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        result = ydl.extract_info(url, download = True)

def getAudio(url, des): 
    # load the setting in
    setup = setting['download']

    print(des)
    # dealing with the progress bar
    global progress
    progress = wx.GenericProgressDialog(title = setup['on_progress'], message = setup['init'], maximum = 100, style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)

    # starting to download the audio
    opts = {
        'format': 'm4a',
        'outtmpl': des + '%(title)s.%(ext)s',
        'progress_hooks': [progress_Check],
        'merge_output_format': 'mp4',
    }
    with youtube_dl.YoutubeDL(opts) as ydl:
        result = ydl.extract_info(url, download = True)
    
    
def progress_Check(data):
    setup = setting['download']

    downloaded = data['downloaded_bytes']
    total = data['total_bytes']
    if not total:
        total = data['total_bytes_estimate']
    #Gets the percentage of the file that has been downloaded.
    percent = 100 * downloaded / total
    progress.Update(percent, '{:00.0f}% '.format(percent) + setup['downloaded'])
    print("{:00.0f}% downloaded".format(percent))

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop', '')

class ytFrame(wx.Frame):
    def __init__(self, parent, name):
        wx.Frame.__init__(self, parent = parent, title = name, size = (size['width'], size['height']))
        self.SetMaxSize((size['width'], size['height']))
        self.SetMinSize((size['width'], size['height'])) #To set the frame size unchangable
        
        panel = wx.Panel(self)
        
        gui = setting['gui']

        #textDiv
        text_url = wx.StaticText(panel, label = gui['url'])
        text_des = wx.StaticText(panel, label = gui['des'])
        text_type = wx.StaticText(panel, label = gui['type'])
        
        #inputDiv
        self.space_url = wx.TextCtrl(panel, size = (200, 25))
        self.space_des = wx.TextCtrl(panel, size = (200, 25), value = GetDesktopPath())
        
        #functionDiv
        button_paste = wx.Button(panel, label = gui['paste'], size = (65, 30))
        self.Bind(wx.EVT_BUTTON, self.paste, button_paste)
        button_opt = wx.Button(panel, label = gui['option'], size = (65, 30))
        self.Bind(wx.EVT_BUTTON, self.option, button_opt)
        
        #optionDiv
        self.button_video = wx.RadioButton(panel, label = gui['video'])
        self.button_video.SetValue(True)
        self.button_audio = wx.RadioButton(panel, label = gui['audio'])
        self.button_audio.SetValue(False)
        
        #controlDiv
        button_ok = wx.Button(panel, label = gui['ok'], size = (50, 30))
        button_ok.Bind(wx.EVT_BUTTON, self.buttonYt)
        button_quit = wx.Button(panel, label = gui['quit'], size = (50, 30))
        button_quit.Bind(wx.EVT_BUTTON, self.Quit)
        
        
        #SeparatePart Adding
        urlDiv = wx.BoxSizer(wx.HORIZONTAL)
        urlDiv.Add((10, 10))
        urlDiv.Add(text_url)
        urlDiv.Add(self.space_url)
        urlDiv.Add((5, 10))
        urlDiv.Add(button_paste)
        
        # load the user-defined space in
        space = setting['space']

        desDiv = wx.BoxSizer(wx.HORIZONTAL)
        desDiv.Add((10, 10))
        desDiv.Add(text_des)
        desDiv.Add((space['des'], 10))
        desDiv.Add(self.space_des)
        desDiv.Add((5, 10))
        desDiv.Add(button_opt)
        
        typeDiv = wx.BoxSizer(wx.HORIZONTAL)
        typeDiv.Add((10, 10))
        typeDiv.Add(text_type)
        typeDiv.Add((space['type'], 10))
        typeDiv.Add(self.button_video)
        typeDiv.Add(self.button_audio)
        
        controlDiv = wx.BoxSizer(wx.HORIZONTAL)
        controlDiv.Add((145, 10))
        controlDiv.Add(button_ok)
        controlDiv.Add((5, 10))
        controlDiv.Add(button_quit)
        
        frameDiv = wx.BoxSizer(wx.VERTICAL)
        frameDiv.Add((1, 20))
        frameDiv.Add(urlDiv)
        frameDiv.Add((10, 10))
        frameDiv.Add(desDiv)
        frameDiv.Add((10, 10))
        frameDiv.Add(typeDiv)
        frameDiv.Add((10, 15))
        frameDiv.Add(controlDiv)
        
        panel.SetSizerAndFit(frameDiv)
 
        #icon setting       Run these code on Windows platform
        #icon = wx.Icon()
        #icon.LoadFile(name = 'logo.ico', type = wx.BITMAP_TYPE_ANY)
        #self.SetIcon(icon)

        self.Show(True)
    
    def paste(self, event):
        copy = wx.TextDataObject()
        if wx.TheClipboard.Open(): #only when there is something in the clipboard the code will start to run
            flag = wx.TheClipboard.GetData(copy)
            wx.TheClipboard.Close()
            if flag:
                self.space_url.SetValue(copy.GetText())
    
    def option(self, event):
        options = setting['options']
        with wx.DirDialog(self, options['dialog'], style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as win:
            if win.ShowModal() == wx.ID_OK:
                mes = win.GetPath()
                print(mes)
                self.space_des.SetValue(os.path.join(mes, ''))
            else:
                wx.MessageBox(options['dinied'])
                print('denied')
    

    ##### need to be revised
    def buttonYt(self, event):
        #load in the settings
        box_empty = setting['box_empty']

        url = self.space_url.GetValue()
        des = self.space_des.GetValue()
        if (url == '') and (des == ''):
            wx.MessageBox(box_empty['both'])
        elif url == '':
            wx.MessageBox(box_empty['url'])
        elif des == '':
            wx.MessageBox(box_empty['dst'])
        else:
            try:
                if 'www.youtube.com' in url:
                    # switch if user want to download whole video or not
                    if self.button_video.GetValue():
                        print('Start to Download the Video')
                        getVideo(url, des)
                    else:
                        print('Start to Download the Audio')
                        getAudio(url, des)

                    # delete the progress bar and show up the successful message
                    global progress
                    del progress
                    print('Download successfully')
                    wx.MessageBox(setting['success'])
                else:
                    wx.MessageBox(setting['url_error'])
            except:
                # if progress:
                # del progress
                wx.MessageBox(setting['error'], style = wx.STAY_ON_TOP)
    
    def Quit(self, event):
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.App()
    top  = ytFrame(None, setting['title'])
    app.MainLoop()
