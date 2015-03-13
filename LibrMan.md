# Introduction #

LibrMan (Library Manager) will manage your music library:

  1. physically organise your music library into custom directory structure based on the ID3 Information
  1. constantly monitor your physical music library for file system changes and accordingly update your ID3 information

Initial release as a standalone utility. Future releases as plugins for popular music players.

## Dependency ##

  * Python 2.6 - http://python.org
  * Mutagen - http://code.google.com/p/mutagen/

## Usage ##

` > librman manage <source> <destination> <parameters> `

The _manage_ command helps with creating a new file system organisation of MP3's in a source folder to the specified path inside the the destination folder.

Where:
  * 

&lt;source&gt;

 folders with mp3 files to be managed
  * 

&lt;destination&gt;

 folder where the library will be managed
  * 

&lt;parameters&gt;

 application parameters
    1. --nd = No Duplicates, will remove duplicate file names of type x-1.mp3, x\_1.mp3, x(1).mp3, where original file is x.mp3
    1. --path:%ar|%al|%gr|%lg where %ar = artist, %al = album, %gr = genre, %lg = language. eg: --path:%ar/%al would organise the mp3 files in the path destination/artist/album


{{{ > librman update 

&lt;lib-path&gt;

