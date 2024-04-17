import PySimpleGUI as sg
import pytube as pt
from pytube import YouTube
from pytube import Playlist
import os
import re
from moviepy.editor import *
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

#Mp3Converstion: Converts Youtube Object to MP3 and outputs to file destination
#LinkList: list of Youtube links
#VideoNames: list of video names corrisponding to linklist p.s. i ended up not needing it but left it in anyway
#FileDestination: Where to put all mp3s when downloaded
def Mp3Conversion(linkList, VideoNames, FileDestination):
    destination = FileDestination or os.getcwd()
    for i in range(len(linkList)):
        audio = YouTube(linkList[i]).streams.get_audio_only()
        #audio = YouTube(linkList[i]).streams.filter(only_audio=True).first()
        #out_file = audio.download(output_path=destination)
        mp3 = AudioFileClip(audio.url)
        mp3.write_audiofile("output" + ".mp3")
        mp3.close()
        #title = audio.title.encode('ascii','ignore')
        #title = title.decode()
        title = audio.title
        title = title.replace("<",'').replace('>','').replace(':','').replace('\\','').replace('/','').replace('|','').replace('"','').replace('?','').replace('*','')
        os.rename('output.mp3', FileDestination + '/' + title + '.mp3')
        #base, ext = os.path.splitext(out_file)
        #new_file = base + '.mp3'
        #os.rename(out_file, new_file)
    return

#FindVideoName: takes link and returns the name of the video/ pretty simple func
#link: link of video
def FindVideoName(link):
    #print (link)
    video = YouTube(link)
    return video.title
    #video = Null
    #print(video.title)


#main: handles window operations as well as some logic for links and its a mess but still works as intended for windows 10 it kinda works for 11 idk
def main():
    window = sg.Window('Dank\'s Youtube to MP3 Converter', Layout)  #initializes the GUI
    VideoNames = []                                                 #List of video names to be passed to conversion
    ConvertButton = window['Convert All']                           #Assigns convertall button to a variable for easier access
    SongBox = window['SongBox']                                     #^^^^^^ same as above but for the box of songs
    SelectedSong = ''                                               #holds the value of the selected song from the songbox
    FileDestination = ''                                            #records the file destination for where to download to
    noCopy = True                                                   #bool flag for purpose of checking if song exists in the list already. starts at false
 
    while True:
        event, entires = window.read() 
        if event == sg.WIN_CLOSED or event == 'Exit':               #exits program
            break
        elif event == 'Add':
            if entires[0] in YoutubeLinks:
                noCopy = False
                window['CopyError'].update(visible = True)
            if noCopy == True:
                window['CopyError'].update(visible = False)
                if "music" in entires[0]:                           #checks for "music" in link in case of youtube music links and removes it as without it the link redirects to the actual youtube video
                        entires[0].replace("music.", '')
                if "playlist" in entires[0] or "Playlist" in entires[0]: #playlist handler
                    p = Playlist(entires[0])
                    playlist = p.video_urls
                    for i in range(len(playlist)):                       #loops playlish and adds each song
                        VideoNames.append(FindVideoName(playlist[i]))
                        YoutubeLinks.append(playlist[i])
                else:                                                    #single song link handler
                    VideoNames.append(FindVideoName(entires[0]))         
                    YoutubeLinks.append(entires[0])
                #print(YoutubeLinks)
                #print(VideoNames)
                SongBox.update(values=VideoNames)
                if(ConvertButton.Disabled == True):                     #waits until song is added to list before any conversion can be done
                    ConvertButton.update(disabled=False)
            noCopy = True
        elif event == 'SongBox':                                        #if song is selected in "songbox" it gets assigned to "SelectedSong"
            SelectedSong = SongBox.get()
            pass
        elif event == 'Remove':                                         #using "SelectedSong" it removes the link and name from lists as well as updates the songbox
            del YoutubeLinks[VideoNames.index(SelectedSong[0])]
            VideoNames.remove(SelectedSong[0])
            SongBox.update(values=VideoNames)
        elif event == 'Convert All':                                    #starts the mp3 conversion
            Mp3Conversion(YoutubeLinks, VideoNames, FileDestination)
        elif event == '-IN-':                                           #assigns file destination when downloading
            FileDestination = window['-IN-'].Get()
            #print(FileDestination)
        


main()

