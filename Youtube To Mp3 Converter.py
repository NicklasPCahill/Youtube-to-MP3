import PySimpleGUI as sg
import pytube as pt
from pytube import YouTube
from pytube import Playlist
import os
import re
#from tkinter import *
#import requests

YoutubeLinks = []
#GUI Layout

Layout = [
    [sg.Text('Enter the link you would like to convert')],
    [sg.Text('Youtube Link:'), sg.InputText()],
    [sg.Button('Add'), sg.Button('Remove'), sg.Button('Convert All' ,disabled=True)],
    [sg.Listbox("",size=(60,8), enable_events=True, key='SongBox',horizontal_scroll=True, select_mode='LISTBOX_SELECT_MODE_SINGLE')],
    [sg.InputText(key='-IN-', enable_events=True), sg.FolderBrowse(target='-IN-', key='folder', enable_events=True)],
    [sg.Text('Link already in list' , visible=False, key='CopyError', colors='red')],
    [sg.Button('Exit')]
]

def Mp3Conversion(linkList, VideoNames, FileDestination):
    destination = FileDestination or '.'
    for i in range(len(linkList)):
        audio = YouTube(linkList[i]).streams.get_audio_only()
        out_file = audio.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    return

def FindVideoName(link):
    #print (link)
    video = YouTube(link)
    return video.title
    #video = Null
    #print(video.title)

def main():
    window = sg.Window('Dank\'s Youtube to MP3 Converter', Layout)
    VideoNames = []
    ConvertButton = window['Convert All']
    SongBox = window['SongBox']
    SelectedSong = ''
    SongList = ''
    FileDestination = ''
    noCopy = True
 
    while True:
        event, entires = window.read() 
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Add':
            if entires[0] in YoutubeLinks:
                noCopy = False
                window['CopyError'].update(visible = True)
            if noCopy == True:
                window['CopyError'].update(visible = False)

                if "playlist" in entires[0] or "Playlist" in entires[0]:
                    p = Playlist(entires[0])
                    playlist = p.video_urls
                    for i in range(len(playlist)):
                        if "music" in playlist[i]:
                            playlist[i].replace("music.", '')
                        VideoNames.append(FindVideoName(playlist[i]))
                        YoutubeLinks.append(playlist[i])
                else:
                    entires[0].replace("music.", '')
                    VideoNames.append(FindVideoName(entires[0]))
                    YoutubeLinks.append(entires[0])
                #print(YoutubeLinks)
                #print(VideoNames)
                SongBox.update(values=VideoNames)
                if(ConvertButton.Disabled == True):
                    ConvertButton.update(disabled=False)
            noCopy = True
        elif event == 'SongBox':
            SelectedSong = SongBox.get()
            pass
        elif event == 'Remove':
            del YoutubeLinks[VideoNames.index(SelectedSong[0])]
            VideoNames.remove(SelectedSong[0])
            SongBox.update(values=VideoNames)
        elif event == 'Convert All':
            Mp3Conversion(YoutubeLinks, VideoNames, FileDestination)
        elif event == '-IN-':
            FileDestination = window['-IN-'].Get()
            print(FileDestination)
        


main()

