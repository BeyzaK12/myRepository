#!/bin/bash

    DIALOG=${DIALOG=dialog}

    USERDATE=`$DIALOG --stdout --title "CALENDAR" --calendar "Please choose a date..." 0 0 1 1 2018`

    case $? in
      0)
        echo "Date: $USERDATE."
        ;;
      1)
        echo "Cancel pressed."
        ;;
      *)
        echo "Box closed."
        ;;
    esac

    day="$(cut -d'/' -f1 <<<$USERDATE)"
    month="$(cut -d'/' -f2 <<<$USERDATE)"
    year="$(cut -d'/' -f3 <<<$USERDATE)"



    DIALOG1=${DIALOG1=dialog}

    $DIALOG1 --title "What do you want?" --clear \
            --yesno "Writing(yes) or Reading(no)?" 10 30

    case $? in
      0)
        # yes(writing)

		zip="./journal.zip"

		# bash check if zip exists
		if [ -e $zip ]; then

			#zip exists

			echo "A journal entry is found.";

			unzip journal.zip $day$month$year.txt
			gedit $day$month$year.txt

			DIALOG2=${DIALOG2=dialog}

			$DIALOG2 --title "Please save your journal" --clear \
				    --yesno "Do you want to save changes?" 10 30

			case $? in
			  0)
				#yes
				zip journal.zip $day$month$year.txt
				rm $day$month$year.txt
				;;
			  1)
				#no
				echo "Please turn back after making a decision."
				exit
				;;
			  *)
				echo "ESC pressed."
				rm $day$month$year.txt;;
			esac

		else 
			touch $day$month$year.txt
			gedit $day$month$year.txt

			DIALOG3=${DIALOG3=dialog}

			$DIALOG3 --title "Please save your journal." --clear \
				    --yesno "Do you want to save your journal?" 10 30

			case $? in
			  0)
				#yes
				zip -e journal.zip $day$month$year.txt
				rm $day$month$year.txt
				;;
			  1)
				#no
				echo "Please turn back after making a decision."
				exit
				;;
			  *)
			   echo "ESC pressed.";;
			esac

		fi
        ;;

      1)
        # no(reading)
		
		unzip journal.zip $day$month$year.txt
		file="./$day$month$year.txt"

		if [ -f $day$month$year.txt ]; then
			clear
			more $day$month$year.txt
			rm $day$month$year.txt

		else 
			echo "There is no journal."
		fi 

        ;;
      *)
       echo "ESC pressed.";;
    esac


