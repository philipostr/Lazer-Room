# Lazer-Room
 Visual of all possible directions for a laser to be shot in order to hit its target.

This project was inspired by a level 4 foobar challenge question with a few slight changes, but overall the same concept. I also wanted to learn a GUI library, so
I ended up using tkinter in Python.

Basically, you create a room with an incidence (start) point and a target point. The program will then proceed to generate all possible paths that a laser between
the two points can take, given a maximum amount of reflections off the walls of the room. These paths are then drawn in the GUI for you to see and marvel in
its lasery glory.

Notes:
 - To run this program, simply run the tk_gui.py file by double clicking it or running it through your terminal with the Python CLI.
 - Once you make changes to the physical room (changing the dimensions or points), the 'Set Room Changes' button becomes available to click.
   After clicking this button, the room will visually display your newly created room.
 - Perfect corner hits are counted as two reflections, as it is essentially a simultaneous reflection on the two walls forming that corner.
 - Coordinates are relative to the top-left of the room (aka a positive y value will mean down, not up like you are probably familiar with).
 - The two most interesting algorithms in this program are the ones that:
   - Find all possible lasers, returning the initial shot direction from the incidence point and the amount of
     reflections that path will take (located in lazer_sim.simulate).
   - Draws the laser path itself, given its initial direction and amount of reflections (located in tk_gui.create_sim).