# Tumblr archiver

How to backup the pictures, GIFs, and videos **you** liked



## Getting Started
This guide is for Windows, Mac, and Linux user. 

### Step 1: Register as Developer
1. Got to your Tumblr **settings** (can be found after clicking on the pencil symbol on the top right)
2. On the right side click on **apps**
3. At the bottom of the white box you can register for the Tumblr API. Click on it.
4. Add an application.
5. Fill the form. What you actually fill out does not matter
6. Go back to **settings** and then to **apps**
7. You see the same white box as in step 3 but with your app now. You will later need the **OAuth Consumer Key** and **OAuth Consumer Secret**

### Step 2: Install Python
1. The program we are going to run is a **python file** (indicated by the .py). Python is a programming language and you need to install it in order to execute the file.

2. Go to the [Python website](https://www.anaconda.com/download/). We are downloading Python **3.7**. This programm should work in the same way on all operating systems


### Step 3: Download tumblr_archiver.py

1. Download and unzip this file: [tumblr-archiver.zip](https://github.com/aauss/tumblr_archiver/zipball/master)

2. Unzip the file somewhere easy to find, e.g. in your Downloads folder. 


### Step 4. Use the Command Line

1. The command line is the bit of the computer which makes you feel like you're a hacker. 

2. 
- **Windows**: To find the command line, go to your system search and type in "Anaconda Prompt". Click it.
- **Mac and Linux**: Open the program Terminal

3. Your next step is to navigate the prompt to the file archive.py. I explain the most crucial commands to use the command line. But feel free to look up things elsewhere

4. On the left hand side of the screen is part your current path. On Windows it shows `C:\Users\yourusername>` or just `C:\>` , and then there is a blinky cursor. On mac it shows `NameOfYourMac:~ yourusername.`.

5. Type `cd Downloads` and then press enter. Your screen now reads `C:\Users\Unmutual\yourusername>` or on Mac `NameOfYourMac:Downlaods yourusername.`. "cd" stands for "change directory". You have gone one directory down! This is equivalent to just double clicking on the downloads folder. If you go wrong, typing `cd ..` will go up one directory again (`back to C:\Users\yourusername>`). 
- **Windows**: "dir" will give you the content of the folder you are in.
- **Mac and Linux**: use "ls" instead
6. Once you're done pretending to be a hacker, navigate to the folder the file archive.py is in. So:
`cd C:\Users\yourusername\Downloads\tumblr_archiver` OR `cd yourusername\Downloads\tumblr_archiver`


### Step 5. Run!

1. Plug in your laptop charger, and make sure you have a stable internet connection, and that the laptop won't auto shutdown, sleep or screensaver. This program will run for a while and I did not finish testing the restart function. Though, it should work. 

2. Where the blinky cursor is, type `pip install -r requirements.txt`. This will install some other stuff to make the archiver finally work. Then, type `python archive.py`. The first bit tells your computer to run Python, the second bit tells Python to run the archiver.

3. Your command prompt will start spitting fancy sentences onto the screen. Read it to understand what is currently happening! You can do other stuff while you wait, just leave the black command prompt box open and running.

### Step 6. Extras
1. You can run `python try_failed.py` to try downloading failed downlaods again at some other point in time.

2. If you want to see your liking behavior, run `python plot_likes.py`

### Error
Since I wrote this script just recently there might be be still some things I did not think about. Write an issue on [Github](https://github.com/aauss/tumblr_archiver/issues), where you also have the script from. If the error is caused by a weak internet connection or your computer suddenly turns of, restart the script as in step 5
