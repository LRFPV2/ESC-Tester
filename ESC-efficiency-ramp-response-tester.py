# ESC Tester Code, V1
# Lawrence Ro
# April 12, 2025

# HOW IT WORKS:
# Computer sends automated MSP commands via Python to Betaflight FC
# Python will specify what throttle values to send to motors and at what time. Code modified for each different test
# Python simultaneously logs telmetry data
# At end of test or keyboard interrupt (Ctrl-C), data is saved as .CSV and plotted

# HOW TO USE
# 1. Connect Betaflight FC Motor 1 output to ESC Signal
# 2. Connect ESC Telemetry Tx pad to Rx pad of FTDI Adapter
# 3. Plug in battery to ESC. Ensure FC and FTDI adpater are connected to ESC ground
# WARNING: ENSURE PROPELLERS ARE OFF UNTIL READY

# FTDI serial port is specified in run command, as shown below:
# python ESC-tester-v1.py COM8 --> Telemtry serial port

# Betaflight serial port is specified below:
betaflight_serial_port = "COM9"

from yamspy import MSPy
import struct
import time
import serial
import struct
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
from datetime import datetime

# ANSI escape codes for coloring
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
debug = True

def set_motors(motor_values = None):
    payload = struct.pack('<' + 'H' * 4, *motor_values)
    # Send MSP_SET_MOTOR command
    if board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_MOTOR'], data=payload):
        # Receive and process response (if any)
        dataHandler = board.receive_msg()
        if dataHandler:
            board.process_recv_data(dataHandler)
        #print(f"Set motor levels: {motor_values}")
    else:
        print("Failed to send MSP_SET_MOTOR command")

def update_crc8(data, crc):
    crc ^= data
    for _ in range(8):
        if crc & 0x80:
            crc = (crc << 1) ^ 0x07
        else:
            crc <<= 1
        crc &= 0xFF  # Ensure crc is 8-bit
    return crc

def get_crc8(buf):
    crc = 0
    for byte in buf:
        crc = update_crc8(byte, crc)
    return crc

def gather_data(telem_data):
    if debug:
        print("Saving data to file...")
        df = pd.DataFrame(telem_data)
        df.to_csv("Si-efficiency-0-v5.csv")
        print("Done")
        print("Plotting")

        # Set dark mode with Georgia Tech colors
        plt.style.use('dark_background')  # Dark mode background
        sns.set_style("darkgrid", {
            "axes.facecolor": "#1C2526",  # Dark gray background
            "grid.color": "#4A4A4A",      # Subtle gray grid
            "axes.edgecolor": "#FFFFFF",  # White edges
            "text.color": "#FFFFFF",      # White text
            "axes.labelcolor": "#FFFFFF",
            "xtick.color": "#FFFFFF",
            "ytick.color": "#FFFFFF"
        })

        # Georgia Tech color palette
        gt_colors = {
            "gold1": "#B3A369",
            "gold2": "#EAAA00",
            "navy_blue": "#003087",
            "white": "#FFFFFF",
            "black": "#000000"
        }

        # Create the plot
        plt.figure(figsize=(12, 6))
        sns.lineplot(x="timestamp", y="eRPM", data=df, color=gt_colors["gold2"], linewidth=3.5)

        # Customize the plot
        plt.title("eRPM Over Time", color=gt_colors["black"], fontsize=16, pad=15)
        plt.xlabel("Time", color=gt_colors["black"], fontsize=14)
        plt.ylabel("eRPM", color=gt_colors["black"], fontsize=14)

        # Format x-axis timestamps for better readability
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45, color=gt_colors["black"], fontsize=12)
        plt.yticks(color=gt_colors["black"], fontsize=12)

        # Customize grid and spines
        ax = plt.gca()
        ax.spines['top'].set_color(gt_colors["black"])
        ax.spines['right'].set_color(gt_colors["black"])
        ax.spines['left'].set_color(gt_colors["black"])
        ax.spines['bottom'].set_color(gt_colors["black"])

        # Show the plot
        plt.tight_layout()
        plt.show()
        print("End of Test")
            
def main(port, baud):
    try:
        esc_telem = serial.Serial(port, baud)
        esc_telem.flushInput()
        telemetry_data = []
        
        while True:
            elapsed = time.perf_counter() - start
            # Ramp up: 0 to 10 seconds
            if elapsed < 10:
                # 100 steps over 10 seconds, increment by ~5 per 0.1s
                step = int(elapsed / 0.1)  # 0 to 99
                throttle = 1001 + step * 5
                if throttle > 1500:
                    throttle = 1500  # Cap at 1500
                set_motors([throttle, 1000, 1000, 1000])

            # Hold: 10 to 15 seconds
            elif elapsed < 15:
                set_motors([1500, 1000, 1000, 1000])

            # Ramp down: 15 to 25 seconds
            elif elapsed < 25:
                # 100 steps over 10 seconds, decrement by ~5 per 0.1s
                time_since_ramp_down = elapsed - 15  # 0 to 10
                step = int(time_since_ramp_down / 0.1)  # 0 to 99
                throttle = 1500 - step * 5
                if throttle < 1001:
                    throttle = 1001  # Cap at 1001
                set_motors([throttle, 1000, 1000, 1000])

            # End test after 25 seconds
            else:
                set_motors([1000, 1000, 1000, 1000])
                raise Exception("End of Test")
            


            buf = esc_telem.read(10)
            data = struct.unpack('10B', buf)
            
            # Calculate CRC for the received data (excluding the last byte which is the received CRC)
            calculated_crc = get_crc8(data[:-1])
            received_crc = data[-1]
            
            if calculated_crc == received_crc:
                temp = data[0]
                voltage = ((data[1] << 8) | data[2]) * 10
                current = ((data[3] << 8) | data[4]) * 10
                consumption = ((data[5] << 8) | data[6]) * 10
                e_rpm = ((data[7] << 8) | data[8]) * 10
                #P_in = round(voltage * current / 1000 / 1000, 5)
                #P_out = round(current / 1000 * e_rpm * 0.00007598787, 5)
                #efficiency = round(P_out / P_in * 100, 5)
                try:
                    # P_in = round(e_rpm / 1000, 5)
                    # P_out = round(voltage * current / 1000.0 / 1000.0, 3)
                    efficiency = e_rpm / voltage * current
                except ZeroDivisionError:
                    print("Zero power output")
                    efficiency = 0

                timestamp = datetime.now()
                telemetry_data.append({'timestamp': timestamp, 'eRPM': e_rpm, 'Voltage': voltage, 'Current': current, 'Relative-Efficiency': efficiency})
                
                print(f"\rTemperature: {GREEN}{temp:3}{RESET} °C  Voltage: {GREEN}{voltage:5}{RESET}mV  Current: {GREEN}{current:5}{RESET}mA  Consumption: {GREEN}{consumption:5}{RESET}mAh  eRPM: {GREEN}{e_rpm:5}{RESET} Relative Efficiency (eRPM / W): {GREEN}{efficiency:5}{RESET}", end='')
            else:
                print("\rCRC mismatch! Data may be corrupted.", end='')
                esc_telem.flushInput()
            
    except KeyboardInterrupt:
        gather_data(telemetry_data)
    
    except Exception:
        if(debug):
            gather_data(telemetry_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telemetry Data Monitor")
    parser.add_argument("port", help="Serial port to read telemetry data from")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate for the serial connection (default: 115200)")
    args = parser.parse_args()
    with MSPy(device=betaflight_serial_port, loglevel='DEBUG', baudrate=115200) as board:
        print(f"Connected to {betaflight_serial_port}")
        set_motors([1001, 1000, 1000, 1000])
        time.sleep(1.0)
        print("Finished initialization")
        start = time.perf_counter()  # Get current time
        print("Starting Test...")
        main(args.port, args.baud)


