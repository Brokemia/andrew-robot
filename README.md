# andrew-robot

Opening up our AndrewBot Pipette Robot by removing the corresponding screws located around the body we were able to identify the internal modules. 

The three main areas of interest are
1.	The mainboard and IO
2.	The upper servo, LED and Camera Fixture
3.	The robotic arm servo bus, LED and Camera Fixture

INSERT PICTURES

Due to the enumeration of webcams and flash storage on a consumer OS such as windows when connected to the AndrewBot via USB, we hypothesized that the internals were repurposed COTS (Consumer Off The Shelf) devices. 

INSERT PICTURE

Taking a closer look at the camera modules and servos, this was quickly confirmed. The camera modules were repurposed Logitech webcams and the servos were standard Dynamixel, a brand very commonly used for hobbyist robotics. 

INSERT PICTURE

Due to the enumeration of the webcams, we were very curious about the hardware software split of the device with regards to its computer vision and control. Taking a closer look at the Mainboard allowed us to answer this question.
By tracking PCB traces and identifying the surface mount components, we were able to create a functional block diagram for the AndrewBot (VERSION NUM ######).

INSERT PICTURE

The host computer is connected directly to a SMSC USB2517 USB Hub IC which allows the PC to access all 7 channels of the hub. The first 2 channels are connected to female USB connectors such that USB Memory Sticks are able to be plugged in. This is the flash memory that gets enumerated by windows and mostly contains .xml files that contain device specific parameters for initialization, including servo position information in addition to other various resorces.
For our device, we had a USB Memory Stick inserted into the first channel, with the second channel left populated, but empty. This may be used in other models. 

INSERT PICTURES

The next 2 channels are connected to the Logitech webcams via #### connectors. These webcams are located in the neck of the device, for reading the numeric setting of the pipettes, and below the claw of the robot, for scanning QR codes to determine the arrangement of the official AndrewBot modules and to aid in alignment. 
Channels 5, 6 and 7 are all routed to FDTI FT232RL USB to serial converter ICs, with 5 and 6 being routed towards the servo connectors and 7 being routed to an ATMega168PA Microcontroller.

The Tx and Rx lines for channel 5 are connected to a network of logic gates allowing for the Tx and Rx lines to be connected to the motor bus with one trace, to follow the Dynamixel protocol. This network utilizes the CBUS2 pin of the FDTI IC which by default is configured to go high when data is being transmitted over Tx. To Achieve this, a TI HC126 Quad 3-State Buffer IC is used in combination with a 74AHC1G04 Single Inverter Gate.

Channel 6 does not have a populated FDTI IC, however information from the silkscreen and other unpopulated components suggests that this is used for RS-485 servo communication. In our model #### none of this is populated.

INSERT PICTURE

Channel 7 is connected to the ATMega168PA microcontroller. This microcontroller does not handle any logic for the servos or cameras and is exclusively used to drive the LED modules from a serial command from the host PC via digital pins D3 and (D4?). D3 is connected to a #### LED Driver IC which is then connected to (both?) LED banks.
(D4?) is routed to an unpopulated LED Driver IC which may be used to drive additional LEDs in other models.

INSERT PICTURE

Though understanding the functional block diagram of the main board, i.e. that almost the entirety of the processing was handled by the host computer. We were able to send direct serial commands to control the servos and Cameras, which were both following their standard manufacturer protocols. We were also able to control the LEDs by sending a 1 byte integer to the virtual COM port assigned to the microcontroller’s FDTI IC to adjust the intensity. 

(The Mainboard overall is driven by 12V with a buck converter used to generate 5V to power the ICs)

# LINKS TO DATASHEETS:
  

SMSC USB2517 (7-Port USB 2.0 Hub Controller) : 

https://ww1.microchip.com/downloads/en/DeviceDoc/USB2517-USB2517i-Data-Sheet-00001598C.pdf

TI HC126 (Quad 3-State Buffer) : 

https://www.ti.com/lit/ds/symlink/sn54hc126.pdf

Diodes Inc 74AHC1G04 (Single Inverter Gate) : 

https://www.diodes.com/assets/Datasheets/74AHC1G04.pdf

Microchip ATMega168pa (8-bit AVR Microcontroller): 

https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-9223-Automotive-Microcontrollers-ATmega48PA-ATmega88PA-ATmega168PA_Datasheet.pdf

FDTI FT232RL (USB to Serial Converter) : 

https://ftdichip.com/wp-content/uploads/2020/08/DS_FT232R.pdf

(LED Driver) : 

