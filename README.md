# Proto-Pi Installation and Configuration

The Proto-Pi is a general purpose iOT prototype device that can easily be modified to suit your needs. 

A python3/Tkinter application, it provides the following:
 - UI with Touchscreen
 - 4 hardware GPIO buttons
 - Network connectivity, both ethernet and wifi
 - Linux environment
 - DPP enabled onboarding (with the Alfa adapter)

It includes a Tkinter base class for the application, and widget wrappers to make UI management easy. 

This code runs on a Raspberry Pi 3B+, with the following components:

 - [PiTFT 320x240 Capacitive Touchscreen](https://www.adafruit.com/product/2423)
 - [PiTFT Faceplate and buttons kit](https://www.adafruit.com/product/2807)
 - [Pi 3 Matching Case](https://www.adafruit.com/product/2253)
 - [Alfa AWUS036NHA External USB Adapter](https://www.amazon.com/gp/product/B004Y6MIXS/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) (Required for DPP operation)

Note: THIS APPLICATION REQUIRES PYTHON 3.5+!!

## Repository Layout
 - config - Application settings
 - deploy - Installation scripts
 - python3 - Source code
 	- tk - Tkinter GUI component wrappers
 	- utils - Supporting modules
 	- images - Application images
 	- tools - command line python scripts
 - scripts - Useful tools

## Installation

#### Installer actions:
 - Installs and configures the PiTFT display
 - Installs build prerequisites for wpa_supplicant
 - Builds and installs wpa_supplicant from micronets-hostap
 - Disables onboard wifi (optional, y/N prompt)
 - Creates an auxilliary sudoers file for shutdown, reboot, and restarting the desktop
 - Creates a lightdm desktop entry to autostart the python app
 - Installs all python modules required by the app
 - Installs system services (boot/shutdown splash screens)
 - Disables factory wpa_supplicant service (/sbin)
 - Adds current user to gpio and netdev groups

#### Installer notes:
 - The installer can be run successively to pull in updates from micronets-hostap
 - Application is updated with `git pull`
 - A key pair that works for both clinic and DPP is created on first run
 - A default application configuration file is generated on first run
 - Application is run as user (no sudo required)
 - All code/files live in user directory except installed services and wpa_supplicant.conf
 - A Raspbian (buster) image is available/recommended for this install that has:
   + support for the new Pi 4
   + ssh & vnc enabled
   + pi password changed to `micronets`
   + vim installed
   + all system updates installed
   + desktop initialization run (timezone, language, keyboard, etc)

#### Installation instructions:
 - Download and burn raspbian image onto SD card:
   https://www.dropbox.com/s/37ygauo02ltxirf/raspbian-buster-ssh-updates.zip?dl=0
 - You'll need to figure out the ethernet ipaddress
 - ssh pi@[ipaddress] (password is micronets)
 - optionally create/use a different user account

 Then, from the user home directory:
 ```
 #
 cd ~
 git clone https://git@github.com/cablelabs/micronets-pi3.git
 cd micronets-pi3/deploy
 ./install
 # (take default prompts and reboot)
```
 - After installation, optionally change the application to run fullscreen (320x240) using `./deploy/bin/_fullscreen.sh` [on/off]

## Configuration
A default configuration file (`config/config.json`) is generated on first run, which can be subsequently edited. It will not be overwritten when pulling from the repo.
#### Clinic Mode Settings
You will need to edit `config/networks.json` for the default networks to be provisioned and restored on reset.
In the `config/devices` folder are several device profiles to choose from. The selection is made in `config/config.json`. The default is `device-0`

## Runtime environment
This application is run full screen on the PiTFT device (320x240) and is a TKinter application that runs on the desktop (lightdm), using the desktop configuration file `~/.config/autostart/proto-pi.desktop`

It runs in user space and does not require **sudo**. It gets its required privileges from membership in the `gpio` and `netdev` groups and from sudoer privileges for `shutdown, reboot, and restarting the desktop`.

## Developer environment
You can easily run the application without a PiTFT or external HDMI monitor using VNC. (install VNC client on your host machine)
You will want to change the screen resolution in `/boot/config.txt` to 640x480 or greater.
If you are developing on a Mac and want to edit the files on the host machine, you can use [osxfuse and sshfs](https://osxfuse.github.io/)

## Operational Notes
- Clicking on the Header will toggle the PiTFT backlight
- Clicking on the icon in the Header will take an application screenshot
- Clicking on the Status window or Message window will toggle between these two windows
- You can interrupt an animation (splash or fireworks) by tapping the animation or using any of the hardware buttons to select an action

## File System
All of the code for this application lives in the folder where the repository was cloned. Additional application folders/files created at runtime:
 - ./keys - public/private key pairs in formats required by the system
 - ./certs - wifi certificates generated for this device as part of the clinic mode onboarding process
 - ./screenshots - application screenshots (tap the icon in the upper left of the screen) are stored here.

Additional components/files required by the application (created/modified at installation time)

**wpa_supplicant**
 - /usr/local/bin/wpa_supplicant
 - /usr/local/bin/wpa_cli
 - /etc/wpa_supplicant/wpa_supplicant.conf

**splash screens**
 - /etc/systemd/system/splashscreen.service
 - /usr/lib/systemd/system-shutdown/goodbyescreen.service
 - /usr/local/images/splash.png
 - /usr/local/images/goodbye.png
 - /usr/local/images/rebooting.png
 - /usr/local/bin/splash.sh
 - /usr/local/bin/goodbye.sh

**application**
 - ~/.config/autostart/proto-pi.desktop - Application startup file
 - /etc/sudoers.d/010-username - sudo privileges for application

**system**
 - /boot/config.txt - HDMI screen resolution and onboard wifi disable flag
