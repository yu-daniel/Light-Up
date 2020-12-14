# CS325


# Important Note: 
- The program is implemented in Python with GUI (Pygame) & hosted by Repl.it for easy grading.


# Try Playing on Repl.it!

- https://repl.it/@DanielYu5/lightup


# How to Play the Game & Rules

## Rules:
- The game is played on a n x n Board.

- On the Board there are White squares and Black squares.

- Light bulbs are objects that the player can place on White squares.

- When a light bulb is placed, it will illuminate all other White squares from the current square’s adjacent sides (vertically and horizontally), until reaching the end of the Board or a Black square.

- A placed light bulb may be removed from the Board by re-selecting it. This would also de-illuminate any White squares that were affected by the light bulb.

- A light bulb cannot be illuminated by another light bulb

- Black squares may contain a number (0 – 4) within them.

- The number indicates exact number of light bulbs that need to be adjacent to the Black square.

- If a Black square has no number, then any number of Light Bulbs may be placed around it. Black square that has a 0 assigned cannot have any adjacent light bulb(s).

- Only placements in the north, east, south, or west edges around the Black square counts toward the number requirement. Diagonal placements are possible but does not contribute to the count.

## How to Win:
- All Black squares that have numbers includes the correct number of surrounding Light Bulb(s).

- All White squares are illuminated

- No Light Bulb(s) are placed in White squares that are readily illuminated



# Want to Run the Game Locally?

## Required files: 
 - lightup.py
 - lightbulb.png
 - lightbulb2.png


## Dependencies: 
 - pygame 2.0.0 (or newest version)
 - Python 3.8 
 - pip 20.2.4 (or newer)


## For Windows users:


Make sure Python is already added to the PATH variable in Windows.
(If not, follow this tutorial: https://www.educative.io/edpresso/how-to-add-python-to-path-variable-in-windows)


### Install virtualenv & virtualenvwrapper-win

If you don't have virtualenv installed yet, begin at step 1). Otherwise, begin at step 3).

1) Open the Command Prompt (terminal), and type the following command in your terminal:

        python -m pip install virtualenv

2) After virtualenv is installed, type the following command in your terminal:
    
        python -m pip install virtualenvwrapper-win

3) Create a directory/folder at a location of your choice - Let us call this new folder 'myproject', or name you like.

4) Use cd commands to navigate to the 'myproject' folder.

5) Once you are at this folder, type the following commands to create a Python virtual environment in there,

        python -m virtualenv venv

6) The folder should contain a new folder named 'venv' with additional files inside.

    While in the new folder, cd into \venv\Scripts, and once inside Scripts, type the following in the terminal to activate the virtual environment:

        activate

7) When the virtual environment is activated, install the pygame package by typing the following in the terminal:

        pip install pygame

8) Once pygame is successfully installed, cd out of the Scripts folder and back to the 'myproject' folder.

8) Now we can run the Python script by typing the following into the terminal:

        python -m lightup.py

9) You should be able to see the puzzle's GUI and able to play the game. 

    See the PDF for Player Instructions. Enjoy!




## For Linux users:

1) Create a virtual environment in the directory of your choice by entering the following command in the terminal: 

        python3.8 -m venv my_project

    A folder named 'my_project' that contains various files and subfolders should be generated. You may need to 'refresh' to see these new changes.

2) In the terminal (bash shell), enter the following command:

        source my_project/bin/activate

3) Next, we need to install the Python module "pygame", by entering the following command in the terminal:

        python3 -m pip install -U pygame

4) Unzip the zipped files into the "my_project" folder

5) cd into the "my_project" folder

6) Launch the game by typing the following command in the terminal:

        python3 lightup.py

    The game's GUI should pop up. See the PDF for Player Instructions. Enjoy!

7) Optional - when finished with the game, type "deactivate" in the terminal.

