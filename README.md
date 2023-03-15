![Pololu 3pi+ 2040 Robot](https://a.pololu-files.com/picture/0J12003.300.jpg)<br>
My explorations with [Pololu's 3pi+ 2040 early adopter robot kit](https://www.pololu.com/product/5004) just [released on March 7th, 2023](https://www.pololu.com/blog/937/introducing-the-3pi-plus-2040-robot).



## Notable Page Sections
* [My Notes for Pololu](#my-notes-for-pololu)



## Pololu Links
* [*EARLY ADOPTER* 3pi+ 2040 Robot Kit with 30:1 MP Motors (Standard Edition Kit) Pololu Product Page](https://www.pololu.com/product/5004)
* [Pololu 3pi+ 2040 User’s Guide](https://www.pololu.com/docs/0J86)
* [Pololu 3pi+ 2040 Robot Libraries and Example Code on GitHub](https://github.com/pololu/pololu-3pi-2040-robot)



---
## March 15th, 2023
### Notching for Debug Header
![Debug header notch added to chassis](images/20230315-01.jpg)

I installed a 1x6 female 0.1" header on the debug port while soldering parts down to the control board. Unfortunately I didn't have low-profile headers like Pololu used for the included OLED and this resulted in the header not fitting underneath the top edge of the plastic bumper skirt. I also think the top of the skirt would make it hard to connect anything to this header even if I had used a low profile version. I used an X-Acto knife and filing board to cut a notch in the top of the skirt to make room for my taller debug header and allow the skirt to properly clip down around the right motor. The plastic wasn't that hard and didn't put up much of a fight during this process. It only took a few minutes.

### Shared Project Possibility from Personal Robotics Discord
This new [3pi+ 2040 Robot](https://www.pololu.com/product/5004) was first brought to my attention on the Personal Robotics Discord server last week and a few of the members, including myself, ordered one. We started receiving them and discussing them on Discord this week. One of the recent topics has been the ability to run MicroPython code on the robot. This ability has been well received by the group. @shurik179 [Island Robotics] mentioned that he has some IMU sensor fusion C code that he has run on robots in the past and was wondering if the RP2040 would have enough grunt to run such math heavy code from within the MicroPython interpreter. This made me think of a potential fun and challenging project for me to work on:
* Take what I learned from my [i2cperipheral project](https://github.com/adamgreen/i2cperipheral#readme) and apply it to building a native MicroPython library to implement the sensor fusion code used by shurik179. Maybe this library could even take advantage of the RP2040's second core to run this sensor fusion code in the background?

### Inside 3pi+ 2040 MicroPython
I have also started looking at the code included with Pololu's custom MicroPython image. This has me looking at the following Pololu repositories up on GitHub:
* https://github.com/pololu/pololu-3pi-2040-robot
* https://github.com/pololu/micropython-build
* https://github.com/pololu/micropython/tree/3pi



---
## March 14th, 2023
### 3pi+ 2040 Robot Kit Arrived Today
![Pololu 3pi+ 2040 Unopened Box](images/20230314-01.jpg)

My [Pololu 3pi+ 2040 Early Adopter Robot Kit](https://www.pololu.com/product/5004) arrived via UPS earlier this afternoon. Upon opening the robot kit I found a welcome letter from Pololu, thanking the early adopters for ordering their first RP2040 based robot and asking for feedback. This repository is my answer for that feedback request.
![Pololu 3pi+ Box with Letter](images/20230314-02.jpg)

The kit was very well packed. The box is quite rigid and ready to take on the typical handling dealt out by UPS/Fedex/USPS employees. The robot parts inside the box were well wrapped in multiple bubble wrap bags. The following photo shows the kit parts laid out on my living room floor, mere minutes after it arrived at my front door.
![Pololu 3pi+ Parts](images/20230314-03.jpg)

### Kit Assembly
I started reading and following the assembly instructions from [Chapter 3](https://www.pololu.com/docs/0J86/all#3) of the [Pololu 3pi+ 2040 User’s Guide](https://www.pololu.com/docs/0J86) so that I could see my new little bot up and running by the end of the day. I skipped the assembly video and just jumped into the written instructions since that is just more compatible with how my mind works.

#### Initial PCB Test
![Initial PCB Blinking](images/20230314-11.gif)

#### Some Photos Taken During the Assembly Process
![Prepared Motor/Wheels](images/20230314-04.jpg)
![Battery Pack](images/20230314-05.jpg)
![Motors Mounted](images/20230314-06.jpg)
![Enclosure Top](images/20230314-07.jpg)
![Enclosure Bottom](images/20230314-08.jpg)
![OLED w/ Soldered Headers](images/20230314-09.jpg)
![Enclosure Bottom w/ Batteries](images/20230314-10.jpg)

#### Included MicroPython Samples
Once I completed the assembly of the robot I booted it up and ran through the MicroPython samples preinstalled by Pololu. The following animation shows the spin.py sample running on my newly assembled robot.

![Spin sample](images/20230314-12.gif)

### Next Steps
* ~~I installed a 1x6 female 0.1" header on the debug port while soldering parts down to the control board. Unfortunately I didn't have low-profile headers like Pololu used for the included OLED and this resulted in the header not fitting underneath the top edge of the plastic bumper skirt. I will need to cut a notch in the top of this skirt to make room for my taller header and allow the skirt to properly clip down around the right motor.~~<br>
![Close up of debug header](images/20230314-13.jpg)
* Explore the MicroPython support on the robot a bit more and try writing some code to have it bounce around and explore its new home.
* Dream up additional future projects for this cool little bot.



---
## March 8th, 2023
![Pololu 3pi+ 2040 Robot](https://a.pololu-files.com/picture/0J12003.300.jpg)<br>
I saw a link for this new [Pololu 3pi+ 2040 Early Adopter Robot Kit](https://www.pololu.com/product/5004) show up on the **Personal Robotics** Discord Server yesterday and it really caught my eye:
* I really like the look of it. It reminds me of the [RugRover project](https://github.com/adamgreen/rugrover#readme) that I have been working on recently but much nicer than anything I could design myself.
* I also like that it uses the RP2040 microcontroller as its brain. I have done some experimenting in the past with the RP2040. Some of my previous RP2040 projects include:
  * https://github.com/adamgreen/i2cperipheral
  * https://github.com/adamgreen/QuadratureDecoder
* Gives me an opportunity to continue with a little bit more MicroPython exploration and then go deeper into C/C++ programming of the RP2040.
* Quite a bit of bang for the buck.

In the end I decided it looked so cool that I purchased one this evening and started this GitHub repository to document my time with the bot once it arrives.



## My Notes for Pololu
If anyone at Pololu ever happens to read the dribble I post here then this sections lists some comments/notes that I have based on my early adopter experience:
* Cool bot!
  * I love the look of the 3pi+ bots.
  * The RP2040 is a very cool microcontroller and really nice to see it now available on the 3pi+ series of Pololu robots.
  * One advantage of using the RP2040 over the AVR is the ability to run MicroPython on the robot. I think this will make the 3pi+ series of robots accessible to even more robot builders/programmers.
* Would be good if the [Pololu 3pi+ 2040 User’s Guide](https://www.pololu.com/docs/0J86) noted its last update date/time somewhere since it is currently under construction. This would allow early adopters know if and when we should go back and read any new content and/or updates made since the last time we read it.
* In section 1.1 of the [User’s Guide](https://www.pololu.com/docs/0J86) it contains the following part description, "two 1/4″ #2-56 standoffs <u>(OLED version only)</U>". The OLED note in parenthesis isn't required as the 3pi+ 2040 only ships with the OLED.
* The debug port is too close to the edge of the bumper skirt. It is difficult to fit the header and any required cabling without notching the skirt. That said it isn't too hard for the user to make this notch themselves.
* The buttons on the 3pi+ 2040 control board are awfully small and can be tricky to press.
* If you don't solder on headers for the expansion ports while building up the kit, it would be tricky to do it later as this will require desoldering the motor and battery connections so that the bottom battery compartment can be removed from the PCB.