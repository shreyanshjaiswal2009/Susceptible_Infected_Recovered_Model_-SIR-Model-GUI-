# Susceptible_Infected_Recovered_Model_-SIR-Model-GUI-
A Graphic User Interface showing the Susceptible Infected Recovered Model (SIR Model) of disease analysis

This code is having some few interfraces, 
1. Sliders for number of initial susceptible people, number of initail infected people, Contact rate , a slider for the total population, and a slider for the controlling the animation speed (0.5x to 2.5x) 
2. It has some buttons, as follows, button for clearing the graph (won't work during animation), a button for Starting animation (simulate), one for pausing the animation, one for resuming, one Reset button (defaults the sliders to zero and clears the graph, won't work during animation) and finally, one for credits. _(You may remove it if you wish_) 

The graph has 3 lines (green - recovered, orange-infected,blue-susceptible) for representing the number of suceptible,infected and recovered.
The title of the graph gives us some information.
a. N = Total population
b. SO,IO = Number of Initial susceptible people , Number of inital infected people,
c. CR, RR = Contact rate (0-5) Recovery Rate - 0.1 (Predefined - average 10 days for infected individuals to recover.)  
d. Rnot = Gives us the value of CR/RR, tells us how many individuals, on average an infected person can infect before they recover

We have 3 files, _**Slider_GUI_Copy.py**_ (Main code) **_pyinstaller_start.bat_** (For using pyinstaller to convert code to .exe) and _**setup.py**_ (for using cx_FREEZE to convert code to .exe; Go to the directory where the Slider_GUI_Copy.py is located and also have setup.py there and run in terminal/cmd ```**python setup.py build**```)

Please make sure to install all the required libraries. **_The cx_FREEZE, sys and pyinstaller libraries are for conversion of .py to .exe_** you may not install them if you wish not to convert your .py to .exe
Use the requirements.txt file to install all the libraries. 
```pip install -r requirements.txt ```
Please make sure to be in the folder where this file (requirements.txt) is located and then run the command.

Some errors/bugs ⚠️
Could show this error in the GUI while using sliders.
``` ERROR: Float division by zero```
Please click clear graph to get rid of this. I will fix this later.
