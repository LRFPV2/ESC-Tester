# ESC-Tester
Step Response and Efficiency tester code for multirotor ESCs. Compatible with AM32 Firmware.

HOW IT WORKS:
Computer sends automated MSP commands via Python to Betaflight FC
Python will specify what throttle values to send to motors and at what time. Code modified for each different test
Python simultaneously logs telmetry data
At end of test or keyboard interrupt (Ctrl-C), data is saved as .CSV and plotted

HOW TO USE
1. Connect Betaflight FC Motor 1 output to ESC Signal
2. Connect ESC Telemetry Tx pad to Rx pad of FTDI Adapter
3. Plug in battery to ESC. Ensure FC and FTDI adpater are connected to ESC ground
WARNING: ENSURE PROPELLERS ARE OFF UNTIL READY

FTDI serial port is specified in run command, as shown below:
python ESC-tester-v1.py COM8 --> Telemtry serial port

Example of final motor test data:
![Screenshot_46](https://github.com/user-attachments/assets/06c57eaa-0f48-49bb-a961-72d9ef524359)
