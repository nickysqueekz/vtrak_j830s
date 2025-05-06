#!/usr/bin/env python3

import serial
import time
import logging
import logging.handlers

# ===== Configuration =====
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
COMMAND = 'enclosure -a list\r\n'
POLL_INTERVAL_SEC = 60
LOG_TAG = 'vtrak_jbod'

# ===== Syslog Setup =====
logger = logging.getLogger(LOG_TAG)
logger.setLevel(logging.INFO)
syslog = logging.handlers.SysLogHandler(address='/dev/log')
formatter = logging.Formatter('%(name)s: %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

# ===== Serial Session =====
def open_serial():
    return serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=3,
        write_timeout=3
    )

# ===== Poll Loop =====
def main():
    try:
        ser = open_serial()
        logger.info("Serial connection to JBOD established.")
        while True:
            ser.write(COMMAND.encode('ascii'))
            time.sleep(1)
            output = []
            while True:
                line = ser.readline()
                if not line:
                    break
                decoded = line.decode('utf-8', errors='ignore').strip()
                if decoded:
                    output.append(decoded)

            if output:
                for line in output:
                    logger.info(line)
            else:
                logger.warning("No data received from JBOD.")

            time.sleep(POLL_INTERVAL_SEC)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        try:
            ser.close()
        except:
            pass

if __name__ == "__main__":
    main()
