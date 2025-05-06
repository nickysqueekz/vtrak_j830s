# vtrak_j830s

🔧 Python Script: vtrak_serial_logger.py
This script:

Opens the serial port to the JBOD
Logs the enclosure status every 60 seconds
Sends structured logs to local syslog
Compatible with Graylog via rsyslog forwarding

requirements:  
python3-serial rsyslog


output to Grafana dash:
+------+------+------+------+------+------+
| sda  | sdb  | sdc  | sdd  | sde  | sdf  |
| 32°C | 34°C | 36°C | 33°C | 35°C | 30°C |
| 62%  | 80%  | 70%  | 41%  | 95%  | 20%  |
+------+------+------+------+------+------+
| sdg  | sdh  | sdi  | sdj  | sdk  | sdl  |
...
