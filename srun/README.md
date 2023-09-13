
# Operating system for seniors
--------

**Developer:** Tarik Alkanan (xalkan02@vutbr.cz) :mortar_board:

## Requirements

1. Modify Linux operating system distribution.
2. This distribution should start from the USB disk
3. The distribution should have a simple graphical interface for seniors.
4. Create an application that allows running the specified application for seniors.
5. Create the application in the Python programming language.

---------

## Video demonstration


https://user-images.githubusercontent.com/78847793/232056626-6aaba425-c330-40d6-94e1-ccc751704719.mp4

---------

### Initial desktop design

<img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/desktop_design.png" width=75% height=75%>

<a name="SeniorOS_Desktop"></a>
### SeniorOS Desktop
<img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/1_senioros_desktop.png" width=80% height=80%>

<a name="Shutdown_window"></a>
### Shutdown window
<img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/2_Shutdown_window.png" width=80% height=80%>

<a name="Check_administrator_window"></a>
### Check administrator window
<img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/3_Check_administartor_window.png" width=30% height=30%>

<a name="Administrator_window"></a>
### Administrator window
<img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/4_Administartor_window.png" width=30% height=30%>

<a name="Change_passwd_window"></a>
### Change Administrator's password window
<img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/5_Change_passwd_window.png" width=30% height=30%>

---------


## Tasks

 <div style="border: 1px solid gray; padding: 10px; background-color: lightgray;">
    <p><strong>:notebook: Notice:</strong>  All tasks and configurations have been implemented in OS Fedora workstation 36 and Debian 11, User is senior :exclamation:.</p>
   
</div>

**1- Prepare a simple desktop environment**
   - [x] On Fedora [deactivate overview on startup](https://fostips.com/prevent-overview-at-login-gnome-40/)  
The goal of this step is. Simplify the desktop environment for seniors, by disabled the overview so that the program runs immediately after logging on to the desktop. The steps below explain how to do this:

        - Download [gnome-shell-extensios](https://extensions.gnome.org/)
             ```bash
               dnf install gnome-shell-extensios*
             ```
        - Reload Gnome by the below command
           ```bash
              killall -u username
           ```
       - Open GNOME Extensions
       
        <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/Extensions.png" width=50% height=50%>
        
        
       - Enable Dash to Dock extension
       
        <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/Extensions_Settings.png" width=40% height=40%>
        
        
       - Disable Show overview on startup **Setting** -> **Appearance**
       
        <img src="https://github.com/forsenior/os/blob/main/srun/Screenshots/Dash_to_Dock.png" width=40% height=40%>
        
   <div style="border: 1px solid gray; padding: 10px; background-color: lightgray;">
    <p><strong>:notebook: Notice:</strong>   For Debian is not needed to disable overview because it is disabled by default :exclamation:.</p>
   
</div> 
 
   
  

**2- Create [simple desktop app](#SeniorOS_Desktop) using python**

The user interface program was created using several Python libraries, including Tkinter, pygame and pillow
1. [Tkinter](https://docs.python.org/3/library/tkinter.html) was used to create GUI window, buttons and labels
2. [pygame](https://realpython.com/pygame-a-primer/) used to run wav file
3. [pillow]() used to modify the image's size

Install packages for Fedora 36
```bash
$ dnf install python3-tkinter
$ pip install pygame
$ pip install pillow
```
Install packages for Debian 11
```bash
$ apt-get install python3-tk
$ pip install pygame
$ pip install pillow
```
---------
   - [x] Create main desktop window
      ```python      
      window = Tk()                                      #create window
      screen_width = window.winfo_screenwidth()          #get screen width
      screen_height= window.winfo_screenheight()         #get screen height
      button_width = int(screen_width/2 - 10)            #set button width
      button_height = int(screen_height/2 - 10)          #set button height
      window.geometry("%dx%d" % (screen_width,screen_height))   
      window.attributes('-fullscreen',True)              #disable the close button on window
      window.resizable(0,0)                              #disable resize the window
      ```
   - [x] Add the necessory buttons to the main window
        
      The function of each button is to run a specific Python application. the application will be run under its [virtual      environment](https://developer.fedoraproject.org/tech/languages/python/multiple-pythons.html).
      By installing virtualenv the Python environment can be created for each app. The command below is for installing  virtualenv, creating env and activate new virtualenv env, where will be installed the necessary packages for each app
      
      Install virtualenv for Fedora 36
       ```bash
       $ sudo dnf install virtualenv
       $ virtualenv /home/srun/env
       $ source /home/srun/env/bin/activate
       (env)$ pip install pygame  
       ```
       Install virtualenv for Debian 11
       ```bash
       $ sudo apt-get install python3-virtualenv
       $ virtualenv /home/srun/env
       $ . /home/srun/env/bin/activate
       (env)$ pip install pygame     
       ```
        - [x] web button (to open sweb app)
             ```python
              #function to open sweb app
              def sweb_window():
                 os.chdir("/home/sweb")
                 try:
                     if os.system('/home/sweb/env/bin/python /home/sweb/main.py') != 0 :
                           raise Exception()
                 except (Exception) :
                        messagebox.showerror('Error','Can not open sweb app')
              # sweb button            
               swebButton=Button(window,image = img_sweb_resized,
                        activebackground=SWEB_ACTIVEBACKGROUND,background=SWEB_BACKGROUND,
                        bd=5,overrelief = GROOVE,
                        command=sweb_window) 
             ```
        - [x] Email button (to open smail app)
            ```python
            #function to open smail app     
            def smail_window():
                os.chdir("/home/smail")
                try:
                    if os.system('/home/smail/env/bin/python /home/smail/main.py') != 0 :
                          raise Exception()
                except (Exception) :
                       messagebox.showerror('Error','Can not open smail app') 
            #smail button  
            smailButton=Button(window,image =img_smail_resized,
                    activebackground=SMAIL_ACTIVEBACKGROUND,background=SMAIL_BACKGROUND,
                    overrelief = GROOVE,
                    bd=5, command = smail_window)
            ```
        - [x] Text editor button (to open stext app)
            ```python
            #function to open stext app
            def stext_window():
                os.chdir("/home/stext")
                try:
                    if os.system('/home/stext/env/bin/python3 /home/stext/main.py') != 0 :
                          raise Exception()
                except (Exception) :
                     messagebox.showerror('Error','Can not open stext app')
            #stext button        
            stextButton=Button(window,image = img_stext_resized,
                        activebackground=STEXT_ACTIVEBACKGROUND,background=STEXT_BACKGROUND,
                        bd=5,overrelief = GROOVE,
                        command=stext_window)         
            ```        
        - [x] Shutdown button (to open shutdown window)
            ```python
            #function to shutdown window
            def shutdown_window():
                confirm_win = Toplevel(window)
                confirm_win.title('Shut down window')
                confirm_win.geometry("%dx%d" % (screen_width,screen_height))
                confirm_win.attributes('-fullscreen',True)
                confirm_win.resizable(0,0)
                .......
                .....
            #shutdown button
            shutdownButton =Button(window,image =img_shutdown_resized,
                    activebackground=SHUTDOWN_ACTIVEBACKGROUND,background=SHUTDOWN_BACKGROUND,
                    overrelief = GROOVE,
                    bd=5,command=shutdown_window)
            ```        
   - [x] Set four buttons size to full screen
       ```python
   
       window = Tk()
       screen_width = window.winfo_screenwidth()          #get screen width
       screen_height= window.winfo_screenheight()         #get screen height
       button_width = int(screen_width/2 - 10)
       button_height = int(screen_height/2 - 10)
       x_side =int( screen_width/2 - ((screen_width/2)*0.95))
       y_side = int(screen_height/2 -((screen_height/2)*0.95))
       .....
       .....
       swebButton.grid(row = 0, column= 0, padx = x_side , pady = y_side)
       stextButton.grid(row = 0, column= 1)
       smailButton.grid(row = 1, column= 0)
       shutdownButton.grid(row = 1, column= 1)
    
      ```

---------

   - [x] Create [shutdown window](#Shutdown_window)
   
       In this window, the user can:
       
        - Confirm shutdown
        - Cancel shutdown
        - Open settings
          
       ```python
        #shutdown window
        def shutdown_window():
            confirm_win = Toplevel(window)
            confirm_win.title('Shut down window')
            confirm_win.geometry("%dx%d" % (screen_width,screen_height))
            confirm_win.attributes('-fullscreen',True)
            confirm_win.resizable(0,0)
       ```
   - [x] Add the necessory buttons to the shutdown window 
        - [x] Shutdown button (to confirm shutdown)
             ```python
              # shutdown function
              def shutdown_system():  
                  os.system("systemctl poweroff")
              #ok button
              ok_btn =Button(confirm_win,  bd=5,overrelief = SUNKEN,
              image=img_shutdown_resized,background=SHUTDOWN_BACKGROUND,
              activebackground=SHUTDOWN_ACTIVEBACKGROUND,                   
              command=shutdown_system)
              ok_btn.image=img_shutdown_resized
             ```
        - [x] Cancel button (to cancel shutdown)
             ```python 
              #cancel button
              cancel_btn =Button(confirm_win, fg="#7d2811",bd=5,overrelief = SUNKEN,
                        image=image_cancel_resized,background=CANCEL_BACKGROUND,
                        activebackground=CANCEL_ACTIVEBACKGROUND,
                        command=confirm_win.destroy)
              cancel_btn.image=image_cancel_resized             
             ```
        - [x] Settings button  (to open check administrator window)
             ```python
              #settings button 
              settings_btn=Button(confirm_win, text='Settings',
                        font=('Times', 20),
                        bd=0,bg = CANCEL_BACKGROUND,
                        activebackground=CANCEL_ACTIVEBACKGROUND,
                        command=lambda:[confirm_win.destroy(),check_administrator_window()])             
             ```
	     
---------  

   - [x] Create [Check administrator window](#Check_administrator_window)
     
        This window is a step before the user gets to the settings, here the user must enter a valid username and password         (by default the username is **senior** and the password is **senior**).

  	  - The entered username and password will compare with saved user data in JSON file under the name user_data, 		    where the password was hashed by sha 256. 
  	  
  	       
	 ```python
          check_root_win = Toplevel(window)
          check_root_win.title('Permission only for Administrator')
          check_root_win_width = 400
          check_root_win_height = 200        
          #set window to be in center
          x_point=(screen_width/2)-(check_root_win_width/2)
          y_point=(screen_height/2)-(check_root_win_height/2)
          check_root_win.geometry("%dx%d+%d+%d"%(check_root_win_width,
          check_root_win_height,x_point,y_point))
          check_root_win.resizable(0,0)
         ```

	
   - [x] Entry for username  
      ```python
      username_label = Label(check_root_win, text="User Name",font=("None 10 bold"))
      username_label.grid(row=0, column=0, pady = 10)
      username_entry = Entry(check_root_win, textvariable=check_username)
      username_entry.grid(row=0, column=1, pady = 10)
      ```           
   - [x] Entry for password
      ```python
      password_label = Label(check_root_win,text="Password",font=("None 10 bold"))
      password_label.grid(row=1, column=0, pady = 8)
      password_entry = Entry(check_root_win, textvariable=check_password, show='*')
      password_entry.grid(row=1,column=1, pady = 8)
       ```   	    
   - [x] Login button (if the username and password are correct => open Administrator window) 
      ```python
      login_button = Button(check_root_win, text="Login",bd = 2,font=("None 10 bold"),
                   overrelief = SUNKEN, command=get_data)
      ``` 	  
   - [x] Close button (to close check administrator window) 
      ```python
      close_button = Button(check_root_win, text="Close",bd = 2,font=("None 10 bold"),
                   overrelief = SUNKEN, command=check_root_win.destroy  
      ```	  
       
---------  

   - [x] Create [Administrator window](#Administrator_window)   
   
        The user be able to open this window only by entering a valid username and password in the Check Administrator 	     	   window. This window allows the user to :
   
	 - Turn off/on button Reader
	 - change the color style of the buttons
	 - Change sound languages between Czech and English
 	 - Close srun app (main Window)
 	 - Reboot the operating system
 	 - Change username and password
 	 
       ```python
       #create Administrator window
       Administrator_win = Toplevel(window)
       Administrator_win.title('Administrator window')
       root_win_width = 430
       root_win_height = 500
       x_point_root_win = (screen_width/2)-(root_win_width/2)
       y_point_root_win = (screen_height/2)-(root_win_height/2)
       Administrator_win.geometry("%dx%d+%d+%d"%(root_win_width,
                   root_win_height,x_point_root_win,y_point_root_win))
       Administrator_win.resizable(0,0)  	
       ```
	
        - [x] Sound button (to turn on/off button Reader)
        
             ```python
       	      sound_btn = Button(Administrator_win,image= sound_toggle_img,borderwidth=0,
	      command= toggle_json_sound)
	      sound_btn.grid(row=1, column=2,sticky = E,padx = 10, pady=8)
	      ```
	      
        - [x] Color style button (to switch between colorful and monochrome mode)
        
             ```python
	      color_btn = Button(Administrator_win,image= color_toggle_img,borderwidth=0,
	      command = toggle_json_color)
              color_btn.grid(row=3, column=2,sticky = E,padx = 10, pady=8)
	      ```
	      
        - [x] Language button (to switch language between Czech and English)
        
             ```python
	      language_btn = Button(Administrator_win,image=language_toggle_img,borderwidth=0,
	      command=toggle_json_language)
              language_btn.grid(row=5, column=2,sticky = E,padx = 10, pady=8)
	      ```
	      
        - [x] Close button (to close the main window)
             ```python     
       	      close_btn=Button(Administrator_win,image = close_img,borderwidth= 0, 
	      command = lambda:[enable_window_key(), window.destroy()])                
              close_btn.grid(row=7, column=2,sticky = E,padx = 10, pady=8)
	      ```
        - [x] Change user's password button (to open change passwd window)
             ```python
	      change_btn=Button(Administrator_win,image = change_img,borderwidth= 0,
              command=lambda:[Administrator_win.destroy(),change_password()]) 
              change_btn.grid(row=9, column=2,sticky = E,padx = 10, pady=8) 
	      ```
        - [x] Reboot button (to reboot the system)
             ```python
	      reboot_btn=Button(Administrator_win,image=reboot_img,borderwidth=0,
              command=lambda:[Administrator_win.destroy(),reboot_sys()]) 
              reboot_btn.grid(row=11, column=2,sticky = E,padx = 10, pady=8)
	      ```
   - [x] Create [Change passwd window](#Change_passwd_window)
    
    	By this window, the user can change username and password, and the new data will write to JSON file (data_user)
	
     ```python
      change_password_win = Toplevel(window)
      change_password_win.title("Set new password")

      change_password_win.configure(bg=COLOR_BG)
      change_password_win.resizable(0,0) 
     ```
	
   - [x] Entry for username
      ```python
      user_lbl = Label(change_password_win, text="Enter your new username:", bg=COLOR_BG, font="none 12 bold")
      user_lbl.grid(row=1, column=0, sticky=EW, pady=8)
      username_box = Entry(change_password_win, width=40, bg="white")
      username_box.grid(row=2, column=0)
      ```  
   - [x] Entry for new password
      ```python
      pass_lbl = Label(change_password_win, text="Enter your password:", bg=COLOR_BG, font="none 12 bold")
      pass_lbl.grid(row=3, column=0, sticky=EW, pady=8)
      pw_box = Entry(change_password_win, width=40, bg="white",show='*')
      pw_box.grid(row=4, column=0)
      ```  
  
   - [x] Entry to confirm new password
      ```python
      cpass_lbl = Label(change_password_win, text="Confirm password:", bg=COLOR_BG, font="none 12 bold")
      cpass_lbl.grid(row=5, column=0, sticky=EW, pady=8)
      pw_confirm_box = Entry(change_password_win, width=40, bg="white",show='*')
      pw_confirm_box.grid(row=6, column=0)
      ```  

   - [x] Change button (to set new password)
      ```python
      sub_btn=Button(change_password_win, text="Change", width=6, command=click)
      sub_btn.grid(row=7, column=0, pady=10)
      ```  

  

Still under development
