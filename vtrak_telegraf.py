#!/usr/bin/env python3
import serial
import re
import time

serial_port = '/dev/ttyUSB0'
baud_rate = 115200
command = "enclosure -a list"
timeout_seconds = 10

def read_full_output(ser, end_marker=b"cli>"):
    buffer = b""
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        if ser.in_waiting:
            chunk = ser.read(ser.in_waiting)
            buffer += chunk
            if end_marker in buffer:
                break
        else:
            time.sleep(0.1)
    return buffer.decode("ascii", errors="ignore")

def parse_enclosure(raw_data):
    lines = []

    # Uptime
    uptime_match = re.search(r'Time since system powerup:\s*(.+)', raw_data)
    if uptime_match:
        uptime = uptime_match.group(1).strip()
        lines.append(f'enclosure_status uptime="{uptime}"')

    # PSU Status
    psu_matches = re.findall(r'PSU (\d+)\s+Operational', raw_data)
    for num in psu_matches:
        lines.append(f'psu_status,psu={num} status="Operational"')

    # Fan Status
    fan_matches = re.findall(r'(\d+)\s+PSU \d+\s+(\d+)\s+(\w+)', raw_data)
    for fan_id, rpm, status in fan_matches:
        lines.append(f'fan_status,fan={fan_id} rpm={rpm},status="{status}"')

    # Temperature Sensors
    temp_matches = re.findall(r'\d+\s+([^\d]+)\s+(\d+)C/\s*(\d+)F', raw_data)
    for loc, c, f in temp_matches:
        tag = loc.strip().replace(" ", "_")
        if tag: 
            lines.append(f'temperature,sensor={tag} celsius={c},fahrenheit={f}')

    # Voltage Sensors
    volt_matches = re.findall(r'\d+\s+([^\d]+)\s+([\d\.]+)V', raw_data)
    for loc, volt in volt_matches:
        tag = loc.strip().replace(" ", "_")
        if tag: 
            lines.append(f'voltage,sensor={tag} voltage={volt}')

    # Attached SAS addresses
    sas_matches = re.findall(r'Slot(\d+)\s+([\w ]{23})', raw_data)
    for slot, sas in sas_matches:
        sas_clean = sas.strip().replace(" ", "_")
        lines.append(f'drive_slots,slot={slot.strip()} sas_address="{sas_clean}"')

    return lines

def main():
    try:
        print(f"Opening serial connection to {serial_port} at {baud_rate} baud...")
        ser = serial.Serial(serial_port, baud_rate, timeout=2)
        time.sleep(1)

        print(f"Sending command: {command}")
        ser.write((command + "\r\n").encode("ascii"))
        time.sleep(1)

        print("Reading response...")
        output = read_full_output(ser)

        print("\n===== VTrak Enclosure Output Start =====")
        print(output)
        print("===== VTrak Enclosure Output End =====\n")

        print("\n===== Parsed Metrics (for Telegraf) =====")
        timestamp = int(time.time() * 1e9)
        metrics = parse_enclosure(output)
        for line in metrics:
            print(f"{line} {timestamp}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()
