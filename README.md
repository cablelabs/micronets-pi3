# Proto-Pi Installation, Configuration & Operation

The Proto-Pi hardware platform is a general purpose iOT prototype device that can easily be modified to suit your needs.
The application software for this device is used to demonstrate frictionless onboarding of a consumer wifi device.

This focus of this implementation is the provisioning of secure subnets (Micronets) in the subscriber home using one of the following onboarding mechanisms.
- The automated installation of wifi security certificates (Clinic Mode)
- DPP QRCode based device onboarding (DPP Mode)

![](https://github.com/cablelabs/micronets-pi3/blob/master/proto-pi.png)

Using python3/Tkinter, the application framework provides the following:
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
The installation script will install/configure all of the required packages with minimal user interaction.

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
 - Applies Raspbian version specific settings

#### Installer notes:
 - The installer can be run successively to pull in updates from micronets-hostap
 - The python application is updated with `git pull`. (No need to re-run installer)
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
   + Either this one (has ssh/vi preinstalled)
      * https://www.dropbox.com/s/37ygauo02ltxirf/raspbian-buster-ssh-updates.zip?dl=0
   + Or grab the lastest `Buster` distro and install packages yourself
 - Insert the SD card and connect power using a micro-usb cable
 - Connect a keyboard/monitor to the Pi
   - Open the terminal application
 - Or, connect from a remote machine using SSH
   - You'll need to figure out the ethernet ipaddress of the Pi device
   - ssh pi@[ipaddress] (password is `micronets` if you are using the CableLabs distro)

 - Optionally create/use a different user account

 Then, from the user home directory:
 ```
 #
 cd ~
 git clone https://git@github.com/cablelabs/micronets-pi3.git
 # Optionally change to desired branch (e.g. git checkout nccoe-build-3)
 cd micronets-pi3/deploy
 ./install
 # (take default prompts and reboot)
```
 After installation, you can (optionally) change the application to run fullscreen (320x240) using `./deploy/bin/_fullscreen.sh` [on/off]

 (This is only necessary if you will be using the touchscreen instead of an external monitor or VNC as the user interface.)


## Configuration
A default configuration file (`config/config.json`) is generated on first run, which can be subsequently edited. It will not be overwritten when pulling from the repo.
### Configuration settings
```
mode                      [dpp, clinic]
splashAnimationSeconds    [default: 10]
onboardAnimationSeconds   [default: 5]
messageTimeoutSeconds     [default: 45] (clinic)
registrationServer        [default: https://alpineseniorcare.com/micronets] (clinic)
device-profile            [default: device-0] (clinic) # Select from several profiles in /devices
vendor-code               [default: DAWG] (dpp) # Used to identify a vendor when looking up MUD urls
channel                   [default: 1] (dpp) # Channel for DPP OOB messages
channelClass              [default: 81] (dpp) # Channel class for DPP OOB messages
qrcodeCountDown           [default: 30] (dpp) # Number of seconds to display QRCode
dppMUDUrl                 [default: https://registry.micronets.in/mud/v1/model/mud-url/$VENDOR/$MODEL] (dpp)
                          # MUD file URL passed via DPP (future)
dppName                   [default: myDevice] (dpp) # Device name passed via DPP (future)
deviceModelUID            [default: AgoNDQcDDgg] (dpp) # Device model used to lookup MUD file
dppProxy/msoPortalUrl     [default: https://mso-portal-api.micronets.in] (dpp) # Proxy Onboard Only
dppProxy/username         [default: grandma] (dpp) # Proxy Onboard Only, valid subscriber username
dppProxy/password         [default: grandma] (dpp) # Proxy Onboard Only, valid subscriber password
disableMUD                [default: false] (dpp) # Do not auto register MUD url or pass via DPP
```
#### Clinic Mode Default Networks
You will need to edit `config/networks.json` for the default networks to be provisioned on reset. (Note that DPP Mode has no default networks)

#### Clinic Mode Device Profile
In the `config/devices` folder are several device profiles to choose from. This is to facilitate having several advertised devices in a demo. The selection for your device is made in `config/config.json`. The default is `device-0`

## Runtime environment
This application is run full screen on the PiTFT device (320x240) and is a TKinter application that runs on the desktop (lightdm), using the desktop configuration file `~/.config/autostart/proto-pi.desktop`. You can also run it on an external monitor or remotely using VNC - in these cases it is best to change the screen resolution to 640x480. (see above)

The application runs in user space and does not require **sudo**. It gets its required privileges from membership in the `gpio` and `netdev` groups and from sudoer privileges for `shutdown, reboot, and restarting the desktop`.

## Developer environment
You can easily run the application without a PiTFT or external HDMI monitor using VNC. (install VNC client on your host machine)
You will want to change the screen resolution in `/boot/config.txt` to 640x480 or greater. (see above)

If you are developing on a Mac and want to edit the files directly from the host machine, you can use [osxfuse and sshfs](https://osxfuse.github.io/)

## Operation
### General Operation
There are (4) buttons used for general operation. These are both hardware buttons that are part of the TFT display and onscreen buttons on the right side of the screen. You can use either set of buttons.

- Buttons
  + Onboard: Initiate the onboard sequence or cancel in progress onboard operation
  + Cycle: Turns wifi off/on to reconnect to the configured SSID
  + Settings:
    * Mode: DPP or Clinic. Changing the mode requires a restart
    * Reset: Clears wifi credentials. In clinic mode, it restores credentials for the clinic (default) wifi.
    * Reboot: Reboots the Pi
    * Done: Exit the settings screen
  + Power:
    * Tap will restart application
    * Hold will shutdown the Pi
- Clicking on the Header will toggle the PiTFT backlight
- Clicking on the icon in the Header will take an application screenshot
- Clicking on the Status window or Message window will toggle between these two windows

#### General Notes:
- A key pair will be generated on first run. The `keys` folder contains key pairs in both DER and DPP specific formats.
- You can interrupt an animation (splash or fireworks) by tapping the animation or using any of the hardware buttons to select an action
- Settings screen buttons are onscreen buttons only (left side)
- When shutting down, wait for the "Goodbye!" screen to appear AND wait for disk activity to finish before unplugging

### Clinic Mode Operation
- Open a web browser to the Clinic Registration Portal (https://alpineseniorcare.com/micronets/portal/device-list)
- Click/Tap the Onboard button (on the device)
- Select the advertised device in the browser and follow onscreen prompts

### DPP Mode Operation
- Click/Tap the Onboard button
- Using the Micronets mobile (iOS/Android) application, scan the QRCode and submit the onboard request

#### DPP Notes:
- (Optional) Clicking the QRCode will cause the Pi to initiate onboarding (Proxy Onboard) as if the QRCode was scanned by a mobile device.
  + Requires an ethernet connection
  + The `dppProxy` settings need to be configured in `config.json`
    * Valid micronets subscriber credentials
    * MSO Portal URL
  + If the onboard request was successfully submitted, a green border appears around the QRCode.
- If an ethernet connection is available on startup, and if MUD is not disabled, the device pubkey/model will be automatically registered
- If MUD is not disabled, the MUD URL is provided to wpa_supplicant for future DPP MUD support.

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
