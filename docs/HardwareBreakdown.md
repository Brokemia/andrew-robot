# Hardware Reverse Engineering
Opening up our AndrewBot Pipette Robot by removing the corresponding screws located around the body we were able to identify the internal modules. 
![IMG_2555](https://github.com/Brokemia/andrew-robot/assets/41448451/5ba3fd15-212f-46bd-b568-ff20800d759a)

The three main areas of interest were
## 1.	The mainboard and IO

![IMG_2551cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/6b541efe-700b-4078-8abc-ffa692f5047e)
![IMG_2550cpy2](https://github.com/Brokemia/andrew-robot/assets/41448451/26fed4e6-fabf-4d02-a0ce-488e1c41d7d6)
![IMG_2549cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/29161ba5-72ec-4530-a3fd-7797ad287298)
![IMG_2548cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/f9489d58-3d9a-4f50-8cdc-e1e452d3d7a4)

## 2.	The upper servo, LED and Camera Fixture

![IMG_2556](https://github.com/Brokemia/andrew-robot/assets/41448451/5410ebbf-e636-4098-a5aa-4d54afb0d9bd)
![IMG_2558](https://github.com/Brokemia/andrew-robot/assets/41448451/82996486-4e8f-45ea-9a3c-8f7f4fe6cf09)

## 3.  The robotic arm servo bus, LED and Camera Fixture

![IMG_2559](https://github.com/Brokemia/andrew-robot/assets/41448451/795cdee9-69d0-4d98-921f-bdce11624530)
![IMG_2560](https://github.com/Brokemia/andrew-robot/assets/41448451/2b0d2159-6bd0-48e8-9756-b5da6cbafd2a)
![IMG_2552](https://github.com/Brokemia/andrew-robot/assets/41448451/16c97e72-8d60-4846-9124-4510a1b669ce)
![IMG_2553](https://github.com/Brokemia/andrew-robot/assets/41448451/dd68143b-160f-40a9-9706-469170fce33e)
![IMG_2554](https://github.com/Brokemia/andrew-robot/assets/41448451/0943a9c3-33a6-429e-a1a6-27b54aab4e90)

## Process

Due to the enumeration of webcams and flash storage on a consumer OS such as windows when connected to the AndrewBot via USB, we hypothesized that the internals were COTS (Consumer Off The Shelf) devices. 

INSERT PICTURE

Taking a closer look at the camera modules and servos, this was quickly confirmed. The camera modules were repurposed Logitech webcams and the servos were standard Dynamixel, a brand very commonly used for hobbyist robotics. 

![IMG_2553cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/9cfbd7c9-3806-430b-9982-474658d40297)
![IMG_2561cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/b5461e59-4129-4c1b-a083-50d84abe6bc4)

Due to the enumeration of the webcams, we were very curious about the hardware software split of the device with regards to its computer vision and control. Taking a closer look at the Mainboard allowed us to answer this question.
By tracking PCB traces and identifying the surface mount components, we were able to create a functional block diagram for the AndrewBot (#### Mainboard V10).

![AndrewBot (1)](https://github.com/Brokemia/andrew-robot/assets/41448451/0e052e5e-68ab-4bb9-9885-2a58f8b3782f)

The host computer is connected directly to a SMSC USB2517 USB Hub IC which allows the PC to access all 7 channels of the hub. The first 2 channels are connected to female USB connectors such that USB Memory Sticks are able to be plugged in. This is the flash memory that gets enumerated by windows and mostly contains .xml files that contain device specific parameters for initialization, including servo position information in addition to other various resorces.
For our device, we had a USB Memory Stick inserted into the first channel, with the second channel left populated, but empty. This may be used in other models. 

![IMG_2548cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/f9489d58-3d9a-4f50-8cdc-e1e452d3d7a4)

The next 2 channels are connected to the Logitech webcams via 4 pin connectors. These webcams are located in the neck of the device, for reading the numeric setting of the pipettes, and below the claw of the robot, for scanning QR codes to determine the arrangement of the official AndrewBot modules and to aid in alignment. 
Channels 5, 6 and 7 are all routed to FDTI FT232RL USB to serial converter ICs, with 5 and 6 being routed towards the servo connectors and 7 being routed to an ATMega168PA Microcontroller.

The Tx and Rx lines for channel 5 are connected to a network of logic gates allowing for the Tx and Rx lines to be connected to the motor bus with one trace, to follow the Dynamixel protocol. This network utilizes the CBUS2 pin of the FDTI IC which by default is configured to go high when data is being transmitted over Tx. To Achieve this, a TI HC126 Quad 3-State Buffer IC is used in combination with a 74AHC1G04 Single Inverter Gate.

Channel 6 does not have a populated FDTI IC, however information from the silkscreen and other unpopulated components suggests that this is used for RS-485 servo communication. In our model (###) none of this is populated.

![IMG_2565cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/a87f4c81-0378-461b-862d-28b5c1ff4eac)

Channel 7 is connected to the ATMega168PA microcontroller. This microcontroller does not handle any logic for the servos or cameras and is exclusively used to drive the LED modules from a serial command from the host PC via digital pins D3 and (D4?). D3 is connected to a AP8800 LED Driver IC which is then connected to both LED banks.
(D4?) is routed to an unpopulated LED Driver IC which may be used to drive additional LEDs in other models.

![IMG_2550cpy](https://github.com/Brokemia/andrew-robot/assets/41448451/92d9e7e1-dce2-41b6-9243-2033969d63f8)

Though understanding the functional block diagram of the main board, i.e. that almost the entirety of the processing was handled by the host computer. We were able to send direct serial commands to control the servos and Cameras, which were both following their standard manufacturer protocols. We were also able to control the LEDs by sending a 1 byte integer to the virtual COM port assigned to the microcontroller’s FDTI IC to adjust the intensity. 


### LINKS TO DATASHEETS:
  

SMSC USB2517 (7-Port USB 2.0 Hub Controller) : 

https://ww1.microchip.com/downloads/en/DeviceDoc/USB2517-USB2517i-Data-Sheet-00001598C.pdf

TI HC126 (Quad Tri-State Buffer) : 

https://www.ti.com/lit/ds/symlink/sn54hc126.pdf

Diodes Inc 74AHC1G04 (Single Inverter Gate) : 

https://www.diodes.com/assets/Datasheets/74AHC1G04.pdf

Microchip ATMega168pa (8-bit AVR Microcontroller): 

https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-9223-Automotive-Microcontrollers-ATmega48PA-ATmega88PA-ATmega168PA_Datasheet.pdf

FDTI FT232RL (USB to Serial Converter) : 

https://ftdichip.com/wp-content/uploads/2020/08/DS_FT232R.pdf

Diodes Inc AP8800 (Step-down DC/DC LED Driver) : 

https://www.diodes.com/assets/Datasheets/products_inactive_data/AP8800.pdf

