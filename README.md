BLE_HCI
=======

Allows external systems or MCUs to control BLE chip (CC2540) using Bluetooth HCI mode such as Windows/Linux/Mac, Arduino (AVR), Teensy 3.0 (ARM Cortex M4), Respberry Pi (ARM11), etc.

The libraries was written for Python and Arduino. Tested on Windows, Linux and Mac OS X This is in beta and still a work in progress, not all HCI commands and events have been implemented or fully tested.

The HCI firmware is built from TI CC254x SDK, refer to the HostTestApp project if you want to study the firmware code.

Example 1
=========

PC/Mac as BLE central role and via the BLE link, connecting to BLE Mini running Biscuit firmware as peripheral role

Typical connections:<br/>
1. PC <-> USB <-> BLE Mini (HCI) <----- BLE Link ------> BLE Mini (Biscuit) <-> Serial <-> Ardino<br/>
2. Mac <-> USB <-> BLE Mini (HCI) <----- BLE Link ------> BLE Mini (Biscuit) <-> USB <-> Raspberry Pi<br/>
3. Raspberry Pi <-> USB <-> BLE Mini (HCI) <----- BLE Link -----> BLE Mini (Biscuit) <-> Serial <-> Arduino

Requirements:<br/>
1. A PC running Windows, Linux or a Mac running Mac OS X<br/>
2. Raspberry Pi with Linux is also possible<br/>
3. HCI firmware (USB) and Biscuit firmware (USB or Serial)<br/>
4. Two BLE Mini boards, first one running the HCI firmware, another one running the Biscuit firmware<br/>
5. Install Python 2.7.2 32-bit<br/>
6. Install PySerial 2.5<br/>
7. For Windows, install USB CDC driver<br/> 
8. Biscuit central Python script

How it works:<br/>
When you connect the BLE Mini (HCI) to your PC via the USB port, it will function as an USB CDC (Virtual COM Port). On Windows, it will ask for a device driver, so you need to install the USB CDC driver. It shows as a COM port (e.g. COM5). For Linux or Mac OS X, it will work as a tty device (e.g. ttyACM0 or tty.usbmodem1311).<br/>

The Biscuit central Python script controls the virtual COM port, sending BLE command over the port, and listening to the HCI events.<br/>

You need to change the following lines to match your COM port and bardrate:<br/>
if os.name == 'posix':<br/>
  TX.port = '/dev/tty.usbmodem1431'<br/>
else:<br/>
  TX.port = 'COM5'<br/>
TX.baudrate = 115200<br/>

Press 'd' to start discovery, it will show if any device is found, and then press 'e' to establish a BLE link with the device, you need then enable the notification before you can receive data from the device.

Press '1', it will send a string 'Hello World!' to the device and press '2' will send 'I love BLE!'.

You can do many other interesting things as you want with BLE.

Supported systems:<br/>
1. Windows<br/>
2. Linux (includes Raspberry Pi)<br/>
3. Mac OS X<br/>

Example 2
=========

Arduino as BLE central role and via the BLE link, connecting to BLE Mini running Biscuit firmware as peripheral role

Typical connections:<br/>
1. Arduino (A) <-> Serial <-> BLE Mini (A) <----- BLE Link -----> BLE Mini (B) <-> Serial <-> Arduino (B)<br/>
2. Arduino (A) <-> Serial <-> BLE Mini (A) <----- BLE Link -----> BLE Mini (C) <-> USB <-> Raspberry Pi

* Suggest to use Arduino Leonardo or other boards with more than one serial to try this example.
* We use the USB CDC serial for debug/UI and one for connecting to the BLE Mini on Leonardo board.
* Uno has only one serial and we do not use SoftwareSerial because sometimes data recevied incorrectly.<br/>
  -> We used AltSoftSerial, so Uno works now, but the baudrate limited to 57600bps.<br/>
  -> http://www.pjrc.com/teensy/td_libs_AltSoftSerial.html<br/>
* Tested with Uno (use pin 8, 9), Leonardo (use pin 0, 1), Mega 2560 (use TX1, RX1)

Requirements:<br/>
1. BLE HCI library for Arduino<br/>
2. Arduino (A) running HCI library<br/>
3. AltSoftSerial (requred for Arduino Uno)<br/>
4. BLE Mini (A) running HCI firmware (Serial)<br/>
5. BLE Mini (B or C) running Biscuit firmware (Serial or USB)

How it works:<br/>
Similar to the Example 1, the Arduino will keep tracks of HCI events from the serial port. You can see those events and send command using the Arduino IDE's Serial Monitor.

Supported Arduino boards or compatible:
1. Arduino UNO (R3)<br/>
2. Arduino Leonardo (R3)<br/>
3. Arduino Mega 2560 (R3)<br/>
4. Seeeduino V3.0 (Atmega 328P)<br/>
3. Teensy 3.0<br/>
Write to us if any other boards you tested.<br/>
