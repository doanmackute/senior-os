#!/bin/bash
user=$(echo $SUDO_USER)

disable_autologin_debian_to_user(){
text_delete1="AutomaticLoginEnable=true"
text_delete2="AutomaticLogin=$user"
##add comment befor AutomaticLoginEnable=true and delete AutomaticLogin
sed "s/${text_delete1}//;s/${text_delete2}//" /etc/gdm/custom.conf > temp
		mv temp /etc/gdm/custom.conf
}

rm -rf /home/srun
rm -rf /home/stext
rm -rf /home/sweb
rm -rf /home/smail
rm -rf /home/$user/.config/autostart
		
disable_autologin_debian_to_user
echo "You should set a new password"
