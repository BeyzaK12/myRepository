#!/bin/bash

startLoc=$(pwd)
cd Kurt_Beyza_Final

if [ ! -f SystemAnalysisReport.gpg ]; then
	echo "There is no file to read!"
	exit 0;
elif [ ! -f SystemAnalysisReport.last.gpg ]; then
	num="1"
else
	echo "There are 2 record:"
	echo "[1] SystemAnalysisReport.gpg"
	echo "[2] SystemAnalysisReport.last.gpg"
	read -p "Choose one to read with num: " num
	
	if [ $num != "1" ] && [ $num != "2" ]; then
		echo "This is not an option. Try again!"
		exit 0;
	fi
fi

echo ""
echo "can be decrypted and be saved"
echo "[1] just decrypt and show, then delete decrypted form"
echo "[2] save and show"
read -p "choose one with num: " ans

if [ $ans != "1" ] && [ $ans != "2" ]; then
	echo "This is not an option. Try again!"
	exit 0;
fi

case $num in
	"1")
		file_name="SystemAnalysisReport"
		;;
	"2")
		file_name="SystemAnalysisReport.last"
		;;

esac

gpg --batch --output $file_name --passphrase mypassword --decrypt $file_name.gpg
read -p "(press enter to continue)"

clear
if [ $ans == "1" ]; then
	cat $file_name
	rm $file_name
elif [ $ans == "2" ]; then
	cat $file_name
	echo "$file_name can be found at home directory."
fi


