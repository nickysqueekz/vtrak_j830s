# vtrak_j830s

🔧 Python Script: vtrak_telegraf.py
This script:

Opens the serial port to the JBOD
Logs the enclosure status every 60 seconds
Sends structured logs to local syslog
Compatible with Graylog via rsyslog forwarding

requirements:  
python3-serial rsyslog

run via telegraf:
[[inputs.exec]]
  commands = ["/usr/local/bin/vtrak_telegraf.py"]
  timeout = "10s"
  data_format = "influx"
  interval = "300s"  # 5 minutes


output to Grafana dash:
|   |    |   |   |   |    |
| ----- | ----- | ----- | ----- | ----- | ------ |
| sda  | sdb  | sdc  | sdd  | sde  | sdf  |
| 32°C | 34°C | 36°C | 33°C | 35°C | 30°C |
| 62%  | 80%  | 70%  | 41%  | 95%  | 20%  |
| ----- | ----- | ----- | ----- | ----- | ------ |
| sdg  | sdh  | sdi  | sdj  | sdk  | sdl  |
...


Serial connection info:
How to set up a serial connection to a VTrak and collect all logs using the command line interface
You may encounter a situation where you need to collect information from a VTrak system for troubleshooting, and network access to the VTrak may be unavailable. The VTrak product line controllers have embedded serial data connection to allow access to the system’s Command Line Interface.

Each VTrak system includes two RJ11-to-DB9F cables in the Accessories box. These cables are used to establish a connection between the VTrak and any computer (PC, Mac, Linux) that has an embedded serial port or can use a USB-to-Serial adapter.

Promise RJ11-to-DB9F Cable
![image](https://github.com/user-attachments/assets/f4c0736b-1343-4249-9a35-e60d71c7bba6)


Note that you will need to have a terminal emulation application on your computer, or be familiar with any system tools that will allow you to access the serial port.

Serial Pinout

If you would like to build your own cable, follow the pinout diagram below:

![image](https://github.com/user-attachments/assets/34a1ad27-f35d-4199-be80-7da2e83923cd)


Setting up a serial cable connection

First, plug the RJ11 end of the serial data cable in to the RJ11 serial connector on the left VTrak RAID controller.

VTrak system rear view - RJ11 serial connectors

![image](https://github.com/user-attachments/assets/5c066fe9-d419-47b3-b72d-0eca07c9a805)


Then, plug the DB9F end of the serial data cable in to either a computer serial port or a USB-Serial adapter.

USB-Serial Adapter
![image](https://github.com/user-attachments/assets/7d8a4dcc-d9e2-48c1-8999-618d1a1ce84e)


Computer Serial Port
![image](https://github.com/user-attachments/assets/977dfdb9-6d96-4ae1-9863-e30f689ba3cc)


Setting up a Terminal Emulator connection

To establish a serial connection between the computer and the VTrak, you have to use a Terminal emulation application. You have to determine which ‘COM’ port is being used by the serial port, and configure that port in the terminal application using the following serial protocol settings.
```
Baud rate = 115200
Data Bits = 8 bits
Parity = None
Stop Bits: 1
Flow Control: None
```
Press the Enter or Return key and you should see a login prompt in the terminal application. Use your login name and password to gain access. You should see the CLI prompt where you will enter the necessary commands:
```
administrator@cli
```
Collecting the log data

If the Terminal application has the ability to capture the session, enabling the logging to a file. Otherwise, you can copy the output from the Terminal and paste it in to a text file.

Below is a list of commands used to view the various configuration parameters and event logs of a VTrak system.

Once you have logged in, type each command separately and hit Enter between each command.
```
subsys -v
ctrl -v
enclosure -v
battery -v
net -v
bga
fc -v
fc -a list -t device
fc -a list -t initiator
phydrv
phydrv -v
array
array -v
logdrv
logdrv -v
lunmap
event
event -l nvram
```
Please note that the last command contains a lowercase L(l) and not the number one (1).
Once you have completed issuing all of these commands, Close and Save the Terminal session, or copy all of the session and paste it in to a text document.
