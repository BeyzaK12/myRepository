#!/bin/bash

startLoc=$(pwd)

folder_name="Kurt_Beyza_Final"
if [ ! -d "$folder_name" ]; then
	mkdir $folder_name
fi

cd $folder_name
home="$startLoc/Kurt_Beyza_Final"

declare -a arr=("syslog" "auth.log" "kern.log" "messages")
if [ ! -f report.gpg ]; then
	#---first time-----------------------------------------------------------
	echo "I can work in a planned way at certain time intervals!"
	read -p "If you want me to work in the background every 3 hours, just say yes: " y
	echo ""
	if [ ${y,,} == "y" ] || [ ${y,,} == "yes" ]; then
		echo "add this line to the end of the file:"
		echo "0 0,3,6,9,12,15,18,21 * * * $startLoc/final.sh"
		read -p "(if you copied the line, press enter)" enter
		crontab -e
		echo ""
	else
		echo "Okay. If you want it later"
		echo "run 'crontab -e' and add this line to end of the file:"
		echo "0 0,3,6,9,12,15,18,21 * * * $startLoc/final.sh"
		read -p "(press enter to continue)" enter
		echo ""
	fi

	mkdir REPORT
	cd REPORT

	for x in "${arr[@]}"
	do
   		sudo cp /var/log/$x $x.last
		sudo chmod +rwx $x.last
		sudo sha256sum /var/log/$x >> control.sha
	done
	
	sudo cp /etc/passwd passwd.last
	sudo chmod +rwx passwd.last
	sudo sha256sum /etc/passwd >> control.sha
	
	cd ~
	sudo tree -a > $home/REPORT/files.last
	sudo df -h > $home/REPORT/diskspaces.last
	sudo ps -aux > $home/REPORT/processes.last
	sudo systemctl list-unit-files --type service --all > $home/REPORT/services.last
	for user in `cat /etc/passwd | cut -d":" -f1`;
	do
		sudo crontab -l -u $user &>> $home/REPORT/tasks.last
	done
	
	# Encrypt folder
	cd $home
	tar czf report.tar.gz REPORT/
	sudo rm -r REPORT/
	#gpg --batch --output report.gpg --symmetric report.tar.gz
	gpg --batch --output report.gpg --passphrase mypassword --symmetric report.tar.gz
	#echo RELOADAGENT | gpg-connect-agent
	rm report.tar.gz
	
	# Run code again
	cd $startLoc
	ScriptLoc=$(readlink -f "$0")
	exec "$ScriptLoc"
	
else
	#gpg --batch --output report.tar.gz --decrypt report.gpg
	gpg --batch --output report.tar.gz --passphrase mypassword --decrypt report.gpg
	rm report.gpg
	#echo RELOADAGENT | gpg-connect-agent
	tar xzf report.tar.gz
	rm report.tar.gz
	cd REPORT
fi

#------------------------------------------------------------------------------------------------------------------

echo "SYSTEM ANALYSIS REPORT" > SystemAnalysisReport

#------------------------------------------------------------------------------------------------------------------

echo "" >> SystemAnalysisReport
echo "" >> SystemAnalysisReport
echo "********************** BENCHMARKS **********************" >> SystemAnalysisReport
echo ""
echo "'sysbench' is installing..."
echo ""
sudo apt install -y sysbench
echo "" >> SystemAnalysisReport
echo "sysbench' is installed." >> SystemAnalysisReport
echo "" >> SystemAnalysisReport
echo "***** CPU Benchmark *****" >> SystemAnalysisReport
echo ""
echo "CPU benchmark is running..."
sysbench cpu run >> SystemAnalysisReport
echo "" >> SystemAnalysisReport
echo "***** Memory Benchmark *****" >> SystemAnalysisReport
echo ""
echo "Memory benchmark is running..."
echo "" >> SystemAnalysisReport
sysbench memory run >> SystemAnalysisReport

echo ""
echo "" >> SystemAnalysisReport
echo "********************** NETWORK **********************" >> SystemAnalysisReport
echo "'vnstat' is installing..."
echo ""
sudo apt install -y vnstat
echo "" >> SystemAnalysisReport
echo "'vnstat' is installed." >> SystemAnalysisReport
echo "" >> SystemAnalysisReport
vnstat >> SystemAnalysisReport
echo "" >> SystemAnalysisReport
#------------------------------------------------------------------------------------------------------------------

logAnalysis () {
	echo "" >> SystemAnalysisReport
	case $1 in 
	"syslog")
		echo "********************** SYSLOG **********************" >> SystemAnalysisReport

		o=$(grep "Out of memory" /var/log/syslog)
		if [ -z $o ]; then
			echo "" >> SystemAnalysisReport
			echo "Good news! There is no 'Out of memory' error." >> SystemAnalysisReport
		else
			echo "" >> SystemAnalysisReport
			echo "There is 'Out of memory' error(s):" >> SystemAnalysisReport	
			echo "" >> SystemAnalysisReport
			echo $o >> SystemAnalysisReport	
		fi
		;;
	"auth.log")
		echo "********************** AUTH.LOG **********************" >> SystemAnalysisReport

		i=$(grep "invalid user" /var/log/auth.log)
		if [ -z $i ]; then
			echo "" >> SystemAnalysisReport
			echo "Good news! There is no 'Invalid user' error." >> SystemAnalysisReport
		else
			echo "" >> SystemAnalysisReport
			echo "There is 'Invalid user' error(s):" >> SystemAnalysisReport	
			echo "" >> SystemAnalysisReport
			echo $i >> SystemAnalysisReport
		fi

		s=$(grep "shutdown" /var/log/auth.log)
		if [ -z $s ]; then
			echo "" >> SystemAnalysisReport
			echo "Good news! There is no 'shutdown' error." >> SystemAnalysisReport
		else
			echo "" >> SystemAnalysisReport
			echo "There is 'shutdown' error(s):" >> SystemAnalysisReport	
			echo "" >> SystemAnalysisReport
			echo $s >> SystemAnalysisReport
		fi
		;;
	"kern.log")
		echo "********************** KERN.LOG **********************" >> SystemAnalysisReport
		;;
	"messages")
		echo "********************** MESSAGES **********************" >> SystemAnalysisReport
		;;
	"passwd")
		echo "********************** PASSWD **********************" >> SystemAnalysisReport
		
		echo "" >> SystemAnalysisReport
		echo "Things that have changed since the last check:" >> SystemAnalysisReport
		echo "" >> SystemAnalysisReport
		diff /etc/$1 $1.last >> SystemAnalysisReport
		echo "----------------------------------------------------------------------------------------------------" >> SystemAnalysisReport
		return 0
		;;
	esac


	echo "" >> SystemAnalysisReport
	echo "Things that have changed since the last check:" >> SystemAnalysisReport
	echo "" >> SystemAnalysisReport
	diff /var/log/$1 $1.last >> SystemAnalysisReport
	echo "----------------------------------------------------------------------------------------------------" >> SystemAnalysisReport
}

#------------------------------------------------------------------------------------------------------------------

sudo sha256sum -c control.sha &> results.txt

while IFS= read -r line
do
	s=$(echo "$line" | cut -d':' -f 2)
	
	if [ $s == "FAILED" ]; then
		f=$(echo "$line" | cut -d':' -f 1)
		if [ $f == "/etc/passwd" ]; then
			f=$(echo $f | cut -d'/' -f 3)
		else
			f=$(echo $f | cut -d'/' -f 4)
		fi
		logAnalysis "$f"
		
		if [ $f == "passwd" ]; then
			sudo cp /etc/$f $f.last
			sudo chmod +rwx $f.last
		else
			sudo cp /var/log/$f $f.last
			sudo chmod +rwx $f.last
		fi
	fi

done < "results.txt"

sudo rm results.txt

#------------------------------------------------------------------------------------------------------------------

sudo rm control.sha
for y in "${arr[@]}"
do
	sudo sha256sum /var/log/$y >> control.sha
done
sudo sha256sum /etc/passwd >> control.sha

#------------------------------------------------------------------------------------------------------------------
declare -a arr2=("files" "diskspaces" "processes" "services" "tasks")

for z in "${arr2[@]}"
do
	cd ~
	case $z in
	"files")
		sudo tree -a > $home/REPORT/files.now
		;;
	"diskspaces")
		sudo df -h > $home/REPORT/diskspaces.now
		;;
	"processes")
		sudo ps -aux > $home/REPORT/processes.now
		;;
	"services")
		sudo systemctl list-unit-files --type service --all > $home/REPORT/services.now
		;;
	"tasks")
		for user in `cat /etc/passwd | cut -d":" -f1`;
		do 
			sudo crontab -l -u $user &>> $home/REPORT/tasks.now
		done
		;;
	esac
	
	cd $home/REPORT
	diff $z.now $z.last > diff.temp
	
	if [ -s diff.temp ]; then
		echo "" >> SystemAnalysisReport
		echo "**********************" ${z^^} "**********************" >> SystemAnalysisReport
		
		echo "" >> SystemAnalysisReport
		echo "Things that have changed since the last check:" >> SystemAnalysisReport
		echo "" >> SystemAnalysisReport
		cat diff.temp >> SystemAnalysisReport
		echo "----------------------------------------------------------------------------------------------------" >> SystemAnalysisReport
	fi
	
	mv $z.now $z.last
	
	rm diff.temp
done


#--FINISH---------------------------------------------------------------------
if [ -f $home/SystemAnalysisReport.gpg ]; then
	if [ -f $home/SystemAnalysisReport.last.gpg ]; then
		rm $home/SystemAnalysisReport.last.gpg
	fi
	mv $home/SystemAnalysisReport.gpg $home/SystemAnalysisReport.last.gpg
fi
mv SystemAnalysisReport $home

cd $home
echo ""
gpg --batch --output SystemAnalysisReport.gpg --passphrase mypassword --symmetric SystemAnalysisReport
rm SystemAnalysisReport

tar czf report.tar.gz REPORT/
rm -r REPORT/
#gpg --batch --output report.gpg --symmetric report.tar.gz
gpg --batch --output report.gpg --passphrase mypassword --symmetric report.tar.gz
#echo RELOADAGENT | gpg-connect-agent
rm report.tar.gz
