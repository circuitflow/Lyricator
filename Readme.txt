This is the README file for Lyricator

################################################################################

Contact: meyers[at]media.mit.edu
URL: http://www.media.mit.edu/~meyers/lyricator.html

################################################################################

Files:
lyricator.sh (main script)
lyricator.py (used by lyricator.sh to process the lyric files)
emotuslite.pickle (data file used by lyricator.py)
lyrics (folder containing several examples of lyric files)

################################################################################

System requirements:
This script was designed to run in the Bash shell, and also 
requires that you have Python installed on your system.

Get Bash @ http://www.gnu.org/software/bash/bash.html
Get Python @ http://www.python.org/

################################################################################

To run, type this at the command line prompt:
%> sh lyricator.sh
(or however you would normally run a shell script)

Please note that only a small number of lyric files have been included in 
this demo to keep it relatively small. If you wish to analyze lyric files of 
your own, simply create a plain text file in a similar format to those listed 
in the 'lyrics' directory. Be sure to place the file in the 'lyrics' directory. 
As well, include the artist/band in the first line of your file and the song 
name in the second line. 
