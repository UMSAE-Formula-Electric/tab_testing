## Tab Testing Notes
1) Look at the [tab testing](https://umsae.miraheze.org/wiki/Formula_Electric_Tab_Testing) wiki page for more information about the setup 
2) Make sure the welder we modified to be our high current supply is connected positive to positive, negative to negative
- If they're swapped, the ADC will read nothing/garbage data
3) Check that the jumpers near the top of the board are ON
- If they are off, then any code you try to flash to the microcontroller won't actually be stored in memory
4) Make sure ADC is connected to the proper pins
5) Make sure the PuTTY output is setup with the right baud rate, COM port, and you enable message time stamping

## Python Data Processing
- Once you run a successful test you'll need to run the python script "getCurrentAndTime.py" and pass it the PuTTY file name you just generated
  - Note that this file needs to be copied to the same workspace as the python script
- The script calculates:
  - The average current flowing through the tab 
    - measured from the ADC and read from the I2C1 bus
  - The time it took to blow the tab
    - We make some assumptions for a min current value here. Would be good to change in the future but works for now.
    - Data quantization from the ADC means that the min value we picked doesn't really affect the start time
- After running the script you need to put that data into an excel graph
  - This should match the expected output in the ESF
  - You'll know you're done when the graph matches the expected ESF output

### Trial Notes
- You'll most likely need to do a lot of test trials to get enough data to match the ESF output
  - Repeat the steps above until you get enough times in each category! :)