## Tab Testing Notes
1) Look at the [tab testing](https://umsae.miraheze.org/wiki/Formula_Electric_Tab_Testing) wiki page for more information about the setup 
2) Make sure the welder we modified to be our high current supply is connected positive to positive, negative to negative
- If they're swapped, the ADC will read nothing/garbage data
3) Check that the jumpers near the top of the board are ON
- If they are off, then any code you try to flash to the microcontroller won't actually be stored in memory
4) Make sure ADC is connected to the proper pins
5) Make sure the PuTTY output is setup with the right baud rate, COM port, and you enable message time stamping