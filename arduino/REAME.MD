
This folder contains Arduino library and examples.

The BLE_HCI_BiscuitCentral is for BLE Mini (Central) to connect to BLE Mini (Peripheral).

The BLE_HCI_BLEShieldCentral is for BLE Mini (Central) to connect to BLE Shield (Peripheral).<br/>

This example will send data to the BLE Shield and turn on the LED connected to Arduino UNO pin 7.
You need to load the BLEFirmata to the UNO board.

Use the Serial Monitor on Leonardo board, and press 'd' for discovery, after it shows 1 device discovered, press 'e' for establish a link to the BLE Shield, after that press '1' or '2' to trun on or off the LED.

The connection is:<br/>
Arduino Leonardo <-> UART <-> BLE Mini <--- BLE Link ---> BLE Shield <-> SPI <-> Arduino UNO<br/>






