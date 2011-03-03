
import eyeD3
import os
import fnmatch
#from sqlite3 import *
import tempfile
import shutil
import sys

#conn = connect('IDE.db')
#curs = conn.cursor()

#curs.execute(
#"create table if not exists songs(id integer primary key autoincrement,title varchar(30),artist varchar(30),album varchar(30),year varchar(4),comment varchar(30),genre varchar(30),filepath varchar(100))"
#)

def createDir(dirName,dirPath=''):
    dir = dirPath+dirName
    if not os.path.exists(dir):
        os.makedirs(dir)
        return 1
    else:
        return 0
        
musicPath = ""
#musicPath = input('Enter path of music Folder: ')
#musicPath = '/users/mayanksaini/desktop/'
def locate(pattern, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files,pattern):
            yield os.path.join(path,filename)





def createDirStructure():
    for musicFiles in locate("*.mp3",musicPath):
        #curs.execute("SELECT * FROM songs WHERE filepath='"+musicFiles+"';")
        #x = 0
        #for row in curs:
        #    x+=1
        #if(x == 0):
        tag = eyeD3.Tag()
        tag.link(musicFiles)
        currentSongTitle= 'Unknown'
        currentSongArtist= 'Unknown'
        currentSongAlbum= 'Unknown'
        currentSongYear= 'Unknown'
        currentSongComment= 'librman'
        currentSongGenre = 'Unknown'
        if(tag.getTitle() != None):
            currentSongTitle = tag.getTitle()
        if(tag.getArtist() != None):
            currentSongArtist = tag.getArtist()
        if(tag.getAlbum() != None):
            currentSongAlbum = tag.getAlbum()
        if(tag.getYear() != None):    
            currentSongYear = tag.getYear()
        tag.addComment(currentSongComment)
        if tag.getGenre() != None:
            currentSongGenre = tag.getGenre()
        tag.update()
        currentSongFilePath = musicFiles
        #insertQuery = "INSERT INTO songs (title,artist,album,year,comment,filepath) VALUES ('"+currentSongTitle+"','"+currentSongArtist+"','"+currentSongAlbum+"','"+currentSongYear+"','"+currentSongComment+"','"+currentSongFilePath+"')"
        #curs.execute(insertQuery)
        #conn.commit()
        createDir('librmanSongs')
        createDir(currentSongArtist,'librmanSongs/')
        fob = open('librmanSongs'+'/'+currentSongArtist+'/.lman','w')
        fob.write('Artist='+currentSongArtist)
        fob.close()
        createDir(currentSongAlbum,'librmanSongs/'+currentSongArtist+'/')
        fob = open('librmanSongs'+'/'+currentSongArtist+'/'+currentSongAlbum+'/.lman','w')
        fob.write('Album='+currentSongAlbum)
        fob.close()
        shutil.copy2(currentSongFilePath, 'librmanSongs/'+currentSongArtist+'/'+currentSongAlbum+'/'+currentSongTitle+'.mp3')
        content = ""
        try:
            fob = open('librmanSongs'+'/'+currentSongArtist+'/'+currentSongAlbum+'/.lmant','r')
            content = fob.read()
            fob.close()
        except:
            None
        fob = open('librmanSongs'+'/'+currentSongArtist+'/'+currentSongAlbum+'/.lmant','w')
        content += currentSongTitle
        content += ".mp3\n"
        fob.write(content)
        fob.close()
    try:
        shutil.rmtree(musicPath+'/librmanSongs')
    except:
        None
    shutil.move('librmanSongs/',musicPath)

def checkDirectories():    
    for librmanFiles in locate('.lman',musicPath):
        fob = open(librmanFiles,'r')
        content = fob.read()
        fob.close()
        contentArray = content.split('=')
        dirName = contentArray[1]
        fileNameArray = librmanFiles.split('/')
        restPath = ''
        i=0
        while(i<len(fileNameArray)-1):
            restPath = restPath + fileNameArray[i] + "/"
            i+=1
        compareDirName = fileNameArray[-2]
        if(dirName != compareDirName):
            for music in locate('*.mp3',restPath):
                tag = eyeD3.Tag()
                tag.link(music)
                if(contentArray[0]=='Artist'):
                    tag.setArtist(compareDirName)
                    fob = open(librmanFiles,'w')
                    fob.write("Artist="+compareDirName)
                    fob.close()
                else:
                    tag.setAlbum(compareDirName)
                    fob = open(librmanFiles,'w')
                    fob.write("Album="+compareDirName)
                    fob.close()
                tag.update()


def checkFileNames():
    for librmanTitles in locate('.lmant',musicPath):
        fob = open(librmanTitles,'r')
        listOfTitles = fob.readlines()
        fob.close()
        titlesPathArray = librmanTitles.split('/')
        titlesPath = ""
        i=0
        ito = len(titlesPathArray)-1
        while(i<ito):
            titlesPath += titlesPathArray[i]
            titlesPath += "/"
            i+=1
        
        #for titleName in listOfTitles:
        for mp3File in locate("*.mp3",titlesPath):
            mp3FilePathArray = mp3File.split("/")
            mp3FileName = mp3FilePathArray[-1]
            tag = eyeD3.Tag()
            tag.link(mp3File)
            comment = tag.getComment()
            if(comment != "librman"):
                #add to lmant file
                listOfTitles.append(mp3FileName+"\n")
                fob = open(librmanTitles,"w")
                fob.writelines(listOfTitles)
                fob.close()
                tag.addComment("librman")
                tag.update()
            else:
                #get title; set tag = title; update lmant file
                foundInList = 0
                for item in listOfTitles:
                    if(item == mp3FileName+"\n"):
                        foundInList = 1
                if(foundInList == 0):
                    listOfTitles.append(mp3FileName+"\n")
                    fob = open(librmanTitles,"w")
                    fob.writelines(listOfTitles)
                    fob.close()
                    tag.setTitle(mp3FileName[0:-4])
                    tag.update()
                    
        
#createDirStructure()
#checkDirectories()
#checkFileNames()

if(len(sys.argv) > 2):
    if(sys.argv[1] == "-createDir="):
        musicPath = sys.argv[2]
        createDirStructure()
    else:
        if(sys.argv[1] == "-checkEnteries="):
            musicPath = sys.argv[2]
            checkDirectories()
            checkFileNames()
        else:
            print """Invalid Argument passed\nUsage : python librman.py -createDir= <Path to music directory to rearrange music>\npython librman.py -checkEnteries= <Path to music directory to check for modifications>\n"""
else:
    print """Invalid Argument passed\nUsage : python librman.py -createDir= <Path to music directory to rearrange music>\npython librman.py -checkEnteries= <Path to music directory to check for modifications>\n"""
    