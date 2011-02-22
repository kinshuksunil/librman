
import eyeD3
import os
import fnmatch
from sqlite3 import *
import tempfile
import shutil

conn = connect('IDE.db')
curs = conn.cursor()

curs.execute(
"create table if not exists songs(id integer primary key autoincrement,title varchar(30),artist varchar(30),album varchar(30),year varchar(4),comment varchar(30),genre varchar(30),filepath varchar(100))"
)

def createDir(dirName,dirPath=''):
    dir = dirPath+dirName
    if not os.path.exists(dir):
        os.makedirs(dir)
        return 1
    else:
        return 0
        
    
musicPath = input('Enter path of music Folder: ')
#musicPath = '/users/mayanksaini/desktop/'
def locate(pattern, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files,pattern):
            yield os.path.join(path,filename)





def createDirStructure():
    for musicFiles in locate("*.mp3",musicPath):
        curs.execute("SELECT * FROM songs WHERE filepath='"+musicFiles+"';")
        x = 0
        for row in curs:
            x+=1
        if(x == 0):
            tag = eyeD3.Tag()
            tag.link(musicFiles)
            currentSongTitle= 'Unknown'
            currentSongArtist= 'Unknown'
            currentSongAlbum= 'Unknown'
            currentSongYear= 'Unknown'
            currentSongComment= 'Unknown'
            currentSongGenre = 'Unknown'
            if(tag.getTitle() != None):
                currentSongTitle = tag.getTitle()
            if(tag.getArtist() != None):
                currentSongArtist = tag.getArtist()
            if(tag.getAlbum() != None):
                currentSongAlbum = tag.getAlbum()
            if(tag.getYear() != None):    
                currentSongYear = tag.getYear()
            if(tag.getComment() != None):
                currentSongComment = tag.getComment()
            
            if tag.getGenre() != None:
                currentSongGenre = tag.getGenre()
            currentSongFilePath = musicFiles
            insertQuery = "INSERT INTO songs (title,artist,album,year,comment,filepath) VALUES ('"+currentSongTitle+"','"+currentSongArtist+"','"+currentSongAlbum+"','"+currentSongYear+"','"+currentSongComment+"','"+currentSongFilePath+"')"
            curs.execute(insertQuery)
            conn.commit()
            createDir('test')
            createDir(currentSongArtist,'test/')
            fob = open('test'+'/'+currentSongArtist+'/.lman','w')
            fob.write('[Artist]='+currentSongArtist)
            fob.close()
            createDir(currentSongAlbum,'test/'+currentSongArtist+'/')
            fob = open('test'+'/'+currentSongArtist+'/'+currentSongAlbum+'/.lman','w')
            fob.write('[Album]='+currentSongAlbum)
            fob.close()
            shutil.copy2(currentSongFilePath, 'test/'+currentSongArtist+'/'+currentSongAlbum+'/'+currentSongTitle+'.mp3')
            
    shutil.rmtree(musicPath+'/test')
    shutil.move('test/',musicPath)
    
createDirStructure()
        