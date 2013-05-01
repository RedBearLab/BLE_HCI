BLE_HCI
=======

Allows external MCU to connect BLE (CC2540) using Bluetooth HCI such as Windows/Linux/Mac, Arduino, Respberry Pi, etc.

The libraries was written for Python and Arduino. Tested on Windows and Mac OS X, but this is still a work in progress, not all HCI commands and events have been implemented or fully tested.

Example 1
=========

PC/Mac as BLE central role connecting to BLE Mini running Biscuit firmware as peripheral role

Typical connections:
1. PC <-> USB <-> BLE Mini (HCI) <----- BLE Link ------> BLE Mini (Biscuit) <-> Serial <-> Ardino
2. Mac <-> USB <-> BLE Mini (HCI) <----- BLE Link ------> BLE Mini (Biscuit) <-> USB <-> Raspberry Pi
3. Raspberry Pi <-> USB <-> BLE Mini (HCI) <----- BLE Link -----> BLE Mini (Biscuit) <-> Serial <-> Arduino

Requirements:
1. A PC running Windows, Linux or a Mac running Mac OS X
2. Raspberry Pi with Linux is also possible
3. HCI firmware (USB) and Biscuit firmware (USB or Serial)
4. Two BLE Mini boards, first one running the HCI firmware, another one running the Biscuit firmware
5. Install Python 2.7.2 32-bit
6. Install PySerial 2.5
7. For Windows, install USB CDC driver 
8. Biscuit central Python script

How it works:
When you connect the BLE Mini (HCI) to your PC via the USB port, it will function as an USB CDC (Virtual COM Port). On Windows, it will ask for a device driver, so you need to install the USB CDC driver. It shows as a COM port £¨e.g. COM5). For Linux or Mac OS X, it will work as an tty device (e.g. ttyACM0 or tty.usbmodem1311).

The Biscuit central Python script controls the virtual COM port, sending BLE command over the port, and listening to the HCI events.

Example 2
=========

Arduino as BLE central connecting to BLE Mini running Biscuit firmware as peripheral role

Typical connections:
1. Arduino (A) <-> Serial <-> BLE Mini (A) <----- BLE Link -----> BLE Mini (B) <-> Serial <-> Arduino (B)
2. Arduino (A) <-> Serial <-> BLE Mini (A) <----- BLE Link -----> BLE Mini (C) <-> USB <-> Raspberry Pi

* Suggest to use Arduino Leonardo or other boards with more than one serial to try this example.
* We use the USB CDC serial for debug and one for connecting to the BLE Mini on Leonardo board.
* Uno has only one serial and we do not use SoftwareSerial because it only has 64-byte buffer, not enough to receive HCI data.

Requirements:
1. BLE HCI library for Arduino
2. Arduino (A) running HCI library
3. BLE Mini (A) running HCI firmware (Serial)
4. BLE Mini (B or C) running Biscuit firmware (Serial or USB)
