#! /bin/bash

# Author:	Owen Meyers
# Date:		October 11, 2005

clear

# Input from the user:
echo "Welcome to Lyricator - An emotional indicator of lyrics"
echo


echo -n "Please enter the name of an artist or band: "
read artist
echo -n "Please enter the name of a song: "
read song

echo
echo "Searching for your song..."

# Search for artist & song in database (courtesy of www.lyricsfreak.com)
artists=`grep -ilr "$artist" ./lyrics/`

if [ "$artists" != "" ] ; then
	
	songs=`grep -il "$song" $artists`

	if [ "$songs" != "" ] ; then
		
		# count the number of elements in $songs
		d=0
		for e in $songs
		do
			d=`expr $d + 1`
		done
		
		# One song found, process it
		if [ $d -eq 1 ]; then
			
			info=`head -n 2 "$songs"`
			
			echo
			echo "I found this song:" $info 
			echo -n "Is this correct? (y/n) "
			read correct
			
			if [ ${correct:0:1} = 'y' ] || [ ${correct:0:1} = 'Y' ] ; then
				echo "I'm now emotionalizing your song..."
				echo
			
				python lyricator.py $songs scores.txt
			
				echo
			else
				echo ; echo "Exiting..." ; echo
			fi
		
		# Multiple songs, wait for user input	
		else
			echo "I found several songs: "
			echo
			
			# Display the songs to the user in a readable form
			d=0
			for e in $songs
			do
	
				info=`head -n 2 "$e"`			
				d=`expr $d + 1`
				echo $d "- [" $info "]"
	
			done
		
			echo
			echo "What would you like to do?"
			echo "1) Process all songs"
			echo "2) Choose a specific song"
			echo "3) Exit"
			read choice
		
			case "$choice" in
			"1" )
				echo
				echo "Now emotionalizing all songs..."
				echo
				
				# Generate files containing pleasure, arousal and dominance values 
				# for this song, or multiple songs
				for f in $songs
				do
					python lyricator.py $f scores.txt
					
					echo
					
				done 
			;;
			
			"2" )
				echo
				echo -n "Please choose a song from the above list (1, 2, 3, etc.): "
				read songposition
				
				for g in $songs
				do
					if [ $songposition -eq 1 ] 
					then
						break
					else
						songposition=`expr $songposition - 1`
					fi
				done
		
				echo
				echo "Please wait while I emotionalize your song," $g"..."
				echo
				
				python lyricator.py $g scores.txt
						
				echo
			;;
			
			
			* )
				echo
				echo "Exiting..." 
				echo
			;;
			
			esac
		fi
	
	# Song not found
	else
		echo "Sorry, I couldn't find the song," $song"."
		echo
	fi
	
# Artist not found
else 
	echo "Sorry, I couldn't find any songs by" $artist"."
	echo
fi
