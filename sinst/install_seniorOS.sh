#!/bin/bash
#user who run the script
user=$(echo $SUDO_USER)
#installation directory
dir_to_install="/home/"$user
echo The user is $user
echo Installation direction $dir_to_install

#function to check if the command passed or not
check_command_success(){
#first input
command_run="$1"
#second input
message_to_user="$2"
#run the first input(command)
$command_run
#check if the command passed (0), or not (!0)
if [ $? -eq 0 ]	
then
	echo  "--->  $message_to_user was successful <---"
else
	echo  "***  $message_to_user failed :( ***"
	exit 0
fi
}

#function to check if the OS folder exists in directory /tmp
#if yes -> download the github repository with name OS1....
check_if_os_exists(){

downloaded_file="OS"
#is "/tmp/OS" exists
if [ -e "/tmp/$downloaded_file" ]
then
	i=1
	while [ -e "/tmp/OS_$i" ]
	do 
		i=$((i+1))
	done
	
	new_dir="OS_$i"
	
	else
	new_dir="OS"

fi

}

#function to delete old folders, in case install the Srun again
delete_existing_dir(){
dis_dir="$1"

if [ -e "/home/$1" ]
then 
	rm -rf /home/$1
fi
}

#function to if the system is already installed, and ask for replace it.
check_if_system_exists(){

if [ -e "/home/srun" ]
then
	echo "One of the diractories: 
(/home/srun or /home/smail or /home/stext or /home/sweb) exists."
	echo "Do you want to replace it? [y/N] " 
	read confirmation
	#if yes, delete the old directories
	if [ "$confirmation" = "y" ]
		then
			echo "The old folder will be replaced"
				delete_existing_dir "srun"
				delete_existing_dir "stext"
				delete_existing_dir "sweb"
				delete_existing_dir "smail"
		else	
			echo "The installation has stoped"
			
			exit 0
	fi
else 
	echo "The check was successful"

fi
}

#function to auto-start srun after login
#by creating autostart in ~.config
auto_start_srun(){
mkdir -p /home/$user/.config/autostart && echo "[Desktop Entry]
Type=Application
Name=Pyapp
Exec=/home/srun/env/bin/python /home/srun/main.py
Terminal=false" >/home/$user/.config/autostart/autostart.desktop
chmod +x /home/$user/.config/autostart/autostart.desktop

}
#function to add below commands to custom.conf file, to enable auto-login 
#without the need for a username and password
auto_login_to_gnome(){
gdm="$1"
custom="$2"
custom_path="/etc/$gdm/$custom"
Config1="AutomaticLoginEnable=true"
Config2="AutomaticLogin=$user"

#if the file custom.conf exists
if [ -f $custom_path ]
then
	echo "File custom  found"
	#prevent setting auto-login twoic
	if grep -E "$Config1" $custom_path && grep -E "$Config2" $custom_path 
	then

	echo "The autoLogin was setted"

	else

	echo "Set auto login"
	echo "[daemon]
AutomaticLoginEnable=true
AutomaticLogin=$user" >> $custom_path
	fi
else
	#ask user to create custom.conf file, if it is not exist
	echo "File custom NOT found,
	 Create custom.conf file in directory /etc/$gdm/$custom, and run this script again"
	 exit 0
fi
}

#function ask user to restart the system
request_restart(){

echo "Need to restart? [y/N] " 
	read answer
	 
	if [ "$answer" = "y" ]
	then
		reboot
	else
		echo "The App will start after first restart"
	fi
}

#check if the Operating system is Linux
if [ "$(uname -s)" = "Linux" ]
then 
	#if the distribution is Debian
    if [ -f /etc/debian_version ]
      then	
        echo "The running operating system is Debian"
		#update the system
		#apt-get update -y

       		#install git
	        check_command_success "apt-get install git -y" "Install git"
	
	        #install virtualenv for python
	        check_command_success "apt-get install python3-virtualenv -y" "Install virtualenv"
		#install package libqt5gui5
		apt install libqt5gui5 -y
	        #check if the Senior system was installed
        	check_if_system_exists 

	        #check if the source code from Github is downloaded
		check_if_os_exists

		#Download source code from Githut
		check_command_success "git clone https://github.com/forsenior/os.git /tmp/$new_dir" "Download source code"
	
		#Move srun, stext, sweb, smail to /home/
		check_command_success "sudo mv /tmp/$new_dir/sinstal/srun /home" "move srun to /home"
		check_command_success "sudo mv /tmp/$new_dir/sinstal/stext /home" "move stext to /home"
		check_command_success "sudo mv /tmp/$new_dir/sinstal/sweb /home" "move sweb to /home"
		check_command_success "sudo mv /tmp/$new_dir/sinstal/smail /home" "move smail to /home"
	
		#Create virtual env inside srun,stext,sweb,smail.
		check_command_success "virtualenv /home/srun/env" "Create srun env"
		check_command_success "virtualenv /home/stext/env" "Create stext env"
		check_command_success "virtualenv /home/sweb/env" "Create sweb env"
		check_command_success "virtualenv /home/smail/env" "Create smail env"
	
		#change OS owner
		check_command_success "sudo chown -R $user /home/srun /home/stext /home/sweb /home/smail" "Change owner to $user"
	
		#install needed packages for stext app
		. /home/stext/env/bin/activate && pip install pyqt5 xhtml2pdf  bs4 markdown && deactivate
		#install needed packages for srun app
		. /home/srun/env/bin/activate && pip install pillow pygame && apt-get install python3-tk -y && deactivate
		#install needed packages for sweb app
		. /home/sweb/env/bin/activate && apt-get install python3-tk -y && deactivate
		#install needed packages for smail app
		. /home/smail/env/bin/activate && apt-get install python3-tk -y && deactivate
	
		#Create autostart file to run srun
		auto_start_srun

		#change autostart owner
		check_command_success "sudo chown -R $user /home/$user/.config/autostart" "Change autostart owner to $user"
		#Allow the user to automatically log in to their account without having to manually enter their username and password
		auto_login_to_gnome "gdm3" "daemon.conf"
		#command to disable the automatic Screen Lock
		dconf write /org/gnome/desktop/screensaver/lock-enabled false
		#ask for restart
		request_restart
	
	
    elif [ -f /etc/fedora-release ]
       then
		echo "The running operating system is Fedora"
		#update the system
		#dnf update -y

      	        #install virtualenv for python
	        check_command_success "dnf install virtualenv -y" "Install virtualenv"
        
       	  	#check if the Senior system was installed
	        check_if_system_exists
	        #check if the source code from Github is downloaded
		check_if_os_exists
	
		#Download source from Githut
		check_command_success "git clone https://github.com/forsenior/os.git /tmp/$new_dir" "Download source code"
	
		#Move srun, stext, sweb, smail to /home/
		check_command_success "sudo mv /tmp/$new_dir/sinstall/srun /home" "move srun to /home"
		check_command_success "sudo mv /tmp/$new_dir/sinstall/stext /home" "move stext to /home"
		check_command_success "sudo mv /tmp/$new_dir/sinstall/sweb /home" "move sweb to /home"
		check_command_success "sudo mv /tmp/$new_dir/sinstall/smail /home" "move smail to /home"
	
		#Create virtual env inside srun,stext,sweb,smail.
		check_command_success "virtualenv /home/srun/env" "Create srun env"
		check_command_success "virtualenv /home/stext/env" "Create stext env"
		check_command_success "virtualenv /home/sweb/env" "Create sweb env"
		check_command_success "virtualenv /home/smail/env" "Create smail env"
	
		#Change OS owner
		check_command_success "sudo chown -R $user /home/srun /home/stext /home/sweb /home/smail" "Change owner to $user"
	
		#install needed packages for stext app
		source /home/stext/env/bin/activate && pip install pyqt5 xhtml2pdf  bs4 markdown && deactivate
		#install needed packages for srun app
		source /home/srun/env/bin/activate && pip install pillow pygame && dnf install python3-tkinter -y && deactivate
		#install needed packages for sweb app
		source /home/sweb/env/bin/activate && dnf install python3-tkinter -y && deactivate
		#install needed packages for smail app
		source /home/smail/env/bin/activate && dnf install python3-tkinter -y && deactivate
	
	
		#Create autostart file to run srun
		auto_start_srun
		#change autostart owner
		check_command_success "sudo chown -R $user /home/$user/.config/autostart" "Change autostart owner to $user"
		#Allow the user to automatically log in to their account without having to manually enter their username and password
		auto_login_to_gnome "gdm" "custom.conf"
		#command to disable the automatic Screen Lock in Fedora Workstation
		dconf write /org/gnome/desktop/screensaver/lock-enabled false
		#ask for restart
		request_restart
	
		   
	else
    	echo "The System is not Linux"
    
	fi
fi


