
# Install operating system for seniors on USB flash
--------
**Developer:** Tarik Alkanan (xalkan02@vutbr.cz) :mortar_board:
-------
# Tasks
## Steps to install SeniorOS on bootable USB flash.
1. [Install the Linux operating system Fedora on a USB flash](#Install_the_Linux_operating)
    - [1.Download Fedora](#Download_Fedora)
    - [2.Prepare the USB flash drive](#Prepare)
    - [3.Create a bootable USB flash drive](#Create)
    - [4.Boot from the USB flash drive](#Boot)
    - [5.Install Fedora from bootable USB to USB](#Install_Fedora)
    - [6.Complete the installation](#Complete)
2. [Install senior apps ](#Install_senior)
    - 1. [Prepare the environment for Fedora Workstation 36](#environment_for_Fedora)
    - 2. [Prepare the environment for Debian](#environment_for_Debian)
    - 3. [Install senior App](#Install_senior)

-------    
-------

# Install the Linux operating system Fedora on a USB flash
<a name="Install_the_Linux_operating"></a>
## 1. Download Fedora
<a name="Download_Fedora"></a>

   - From the official Fedora website [https://getfedora.org/](https://getfedora.org/cs/workstation/download/) download the latest version of Fedora (in my case **Fedora workstation 36**) that you want to install on the USB flash drive. And download the ISO file.

   <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/Fedora%20workstation.png" width=85% height=85%>

-------

-------

## 2. Prepare the USB flash drive
<a name="Prepare"></a>

   - Insert the USB flash drive into your computer and make sure it is properly formatted. If you have any important data on the USB flash drive, make sure you back it up because the installation process will erase all data on the USB flash drive.

-------
-------

## 3. Create a bootable USB flash drive
<a name="Create"></a>

   - You can create a bootable USB flash drive using a tool such as Rufus [https://rufus.ie/](https://rufus.ie/en/)in Windows, or [Fedora Media Writer](https://mojefedora.cz/fedora-media-writer-nastroj-na-vytvareni-bootovacich-flash-disku/) in Fedora GNOME Disks or the [dd (terminal)](https://docs.fedoraproject.org/en-US/quick-docs/creating-and-using-a-live-installation-image/) command on Linux. When creating a bootable USB flash drive with a Fedora ISO file, follow the instructions provided by the tool of your choice.

**In this case, the rufus was used [(Watch video tutorial)](https://www.youtube.com/watch?v=iWBYHRsI-Qs&ab_channel=startbeIT).**

**After download rufus and the Fedora workstation:**

   1. Run Rufus
      
      - Run Rufus by double-clicking on the downloaded executable file. Rufus does not require installation and can be run directly from the downloaded file.
   
   2. Select USB Drive (the USB flash, where the live iso image will installed)
   
      -  In Rufus, under the "Device" section, select the USB drive that you inserted in Step 2 from the drop-down menu. Make sure you select the correct USB drive, as Rufus will erase all data on the selected drive.
   
    
   3. Choose Bootable Image
    
      - Under the "Boot selection" section, click on the "SELECT" button and browse to the location of the bootable image file (usually an ISO file "***Fedora-Workstation-Live-x86_64-36-1.5***") on your computer that you want to create a bootable USB for. Select the file and click "Open".
   
| :warning: Wait for Rufus to complete the process, which may take a few minutes :exclamation:.|
| --- |

<img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/rufus%201.png" width=50% height=50%>
   
   4. Configure Rufus Settings

      - Leave the other settings in Rufus at their default values.
   
   5. Start Creating Bootable USB
   
      - Once you have configured the settings, click on the "START" button in Rufus to begin creating the bootable USB. Rufus will format the USB drive, copy the files from the bootable image to the USB drive, and make it bootable.
      -  Once Rufus completes the process, you will see a "READY" notification. You can now safely eject the USB drive from your computer.
      

:speech_balloon: **Recapitulation**
| You have successfully created a bootable USB drive using Rufus. |
| --- |   

-------
-------

## 4. Boot from the USB flash drive
<a name="Boot"></a>

   1. Insert Bootable USB Drive
    
       - Insert the bootable USB drive that you created using Rufus or any other tool into a USB port on the computer. 
      
   2. Restart on the Computer 
       - Restart the computer, and quickly access the boot menu or the **BIOS/UEFI** setup. The specific method to access the boot menu or **BIOS/UEFI** setup may vary depending on the computer's manufacturer and model. Common keys to access the boot menu or **BIOS/UEFI** setup are **F2, F8, F10, F12, or Del**. Refer to the computer's manual or the manufacturer's website for instructions.
   
   3. Select Boot from USB
       - In the boot menu or BIOS/UEFI setup, use the arrow keys to navigate to the "Boot" or "Boot Order" section, and select the option that corresponds to the USB drive you inserted in Step 1. Move it to the top of the boot order to prioritize booting from the USB drive. Save and exit the BIOS/UEFI setup.

  <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/set%20BIOS.png" width=50% height=50%>
  
   4. Restart Computer
       - Restart the computer, and it should now boot from the USB drive. The bootable operating system on the USB drive will start loading.
 
 :speech_balloon: **Recapitulation**
| You have successfully booted your computer from a bootable USB drive. Remember to remove the USB drive and change the boot order back to the original settings in the BIOS/UEFI setup if you want to boot from the computer's regular internal drive in the future. |
| --- |   

-------
-------

## 5. Install Fedora from ***bootable USB*** to another USB (***flash2***)
<a name="Install_Fedora"></a>
 **[(Watch video tutorial)](https://www.youtube.com/watch?v=bpJ08pmj2IQ&ab_channel=startbeIT)**

   1. Select Operating System Installation Option
      
      - When the computer boots from the bootable USB drive, you will typically see a menu or interface that allows you to select the installation option for the operating system you want to install. 
   
   2. Choose Target USB Drive
      - Once the installation option is selected, you may be prompted to choose the target USB drive (***flash2***) where you want to install the operating system. Select the USB drive that you want to use as the installation destination (in our case is (***flash2***)).
     
   | :warning: Be careful to choose the correct USB drive, as the installation process will erase all data on the selected USB drive. |
   | --- |
   
   | :heavy_exclamation_mark: The USB's capacity should be 16GB or more |
   | --- |
   
   3. Start Installation
      - Start the installation process by following the on-screen instructions. This may involve selecting the desired installation settings, such as language, keyboard layout, time zone, and other configuration options. Confirm your selections and proceed with the installation.
   4. Wait for Installation to Complete
      - Wait for the installation process to complete, which may take some time depending on the size of the operating system and the speed of your USB drives. Once the installation is finished, you may be prompted to restart the computer.
   5. Remove Bootable USB Drive
      - After the installation is complete, shutdown the computer, you can safely remove the bootable USB drive from the computer. 
   6. Boot from Installed USB Drive (***flash2***)
      - Insert the USB drive where you installed the operating system into a USB port on a computer. Power on the computer, and ensure that it is set to boot from USB in the BIOS/UEFI setup. Once the computer boots from the USB drive, the operating system should now be installed and ready to use.
   
:speech_balloon: **Recapitulation**
| You have successfully installed the operating system from the bootable USB drive to another USB drive. You can now use the USB drive with the installed operating system as a portable operating system on different computers. Remember to change the boot order in the BIOS/UEFI setup if you want to boot from the USB drive with the installed operating system in the future. |
 | --- |

-------
-------

# 2 Install senior apps 
<a name="Install_senior"></a>

### 1. Prepare the environment for **Fedora Workstation 36**
<a name="environment_for_Fedora"></a>
    The goal of this step is. Simplify the desktop environment for seniors, by disabled the overview so that the program runs immediately after logging on to the desktop. The steps below explain how to do this [(Watch video tutorial)](https://www.youtube.com/watch?v=DYqOQHWN4Do&list=PLoV7yJYwn_xEwnXb4NRSQRF0lBRGiQe0p&ab_channel=startbeIT):  
    
   - Disable Automatic Screen Lock     
       ```bash
         gsettings set org.gnome.desktop.screensaver lock-enabled false
       ```   	
| Do not run the above command with **sudo** :exclamation:|
| --- |
   - Download [gnome-shell-extensios](https://extensions.gnome.org/)
     ```bash
         sudo dnf install gnome-shell-extension* -y
      ```
   - Reload Gnome by the below command
     ```bash
        killall -u username
     ```
   - Open GNOME Extensions
   
     <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/Extensions.png" width=50% height=50%>
     
   - Scroll down and find "Dash to Dock" in the list of installed extensions.
   
     <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/Extensions_Settings.png" width=40% height=40%>      
   - Click on the gear icon next to "***Dash to Dock***" to open its settings.
   - In the "***Appearance***" tab, look for the option "***Show overview on startup***" and toggle it off to disable the overview.
   
     <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/Dash_to_Dock.png" width=40% height=40%>
     
   - Close the GNOME Tweaks window.
    
-------

### 2. Prepare the environment for **Debian 11**
<a name="environment_for_Debian"></a>

In Debian, the user by default Can not run sudo command. Below is a step-by-step guide on how to add a user to the sudoers file in Debian, which will allow the user to run commands with administrative privileges using the **sudo** command, we need this to be able to run script [**install_seniorOS.sh**](https://github.com/forsenior/os/blob/sinstall/sinstall/install_seniorOS.sh):
    
   - Switch to the root account using the **su** command and providing the root password.
     ```bash
      $ su 
     ```
   - Run the following command, replacing <username> with the username of the user you want to add to the sudoers list:
     ```bash
     # echo "username ALL=(ALL:ALL) ALL" >> /etc/sudoers
     ```
| :warning: Be careful when editing the sudoers file, as incorrect syntax or entries can potentially lock you out of the system. Always double-check your changes. :exclamation:.|
| --- |

-------

### 3. Install senior App 
<a name="Install_senior"></a>
The installation of senior app on **Fedora/Debian** is easy, just download the [***install_seniorOS.sh***](https://github.com/forsenior/os/blob/sinstall/sinstall/install_seniorOS.sh) and run it as below [(Watch video tutorial)](https://www.youtube.com/watch?v=3Ft7CJibPM8&list=PLoV7yJYwn_xEwnXb4NRSQRF0lBRGiQe0p&index=2&ab_channel=startbeIT).

```bash
sudo sh install_seniorOS.sh
```
#### What does this script do?
    
   1. Install virtualenv for python
   2. Install necessary packages 
   3. Download source code from Githut
   4. Move srun, stext, sweb, smail to /home/
   5. Create virtual env inside srun,stext,sweb,smail.
   6. Install needed packages for each application
   7. Create autostart file to run srun
   8. Allow the user to automatically log in to their account without enter their username and password
   9. command to disable the automatic Screen Lock
   

--------
### Ideas to improve the program
```  
-------------------------------------------------------
| * create a script to simplify the steps to install  |
|   an operating system on a USB drive.               |
| * edit the install_senioros.sh script to be able to | 
|   install the senior application on all popular     |
|   distributions                                     | 
-------------------------------------------------------
```  
