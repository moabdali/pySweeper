# pySweeper
 minesweeper clone for practice


v0.6:
	Better code readability, added comments.  Removed debug notes.  Better in game prompts (took away a lot of text and hid it behind a "type ? for more details" option.
	Todo: 
	The text overflows on smaller consoles.  Need to either manually format the text to look better, or find a module that can autosize it.  
	Add a GUI
v0.5:
	Now have the ability to place down bomb flags (and removing them) by adding an optional third argument (b for bomb flag, r for remove flag).  To do: Add a GUI. Clean up debug messages inside of code; more comments.

v0.4:
	Properly autocascades 0 bomb locations (if a spot has 0 bombs around it, it "clicks" all the surrounding locations.  There are also a win and lose condition now and the map is revealed upon death/winning.  Added a clear screen feature to make it look a little prettier.
	Todo: ability to flag locations by typing in a third input as a modifier.  Add a GUI. Clean up debug messages inside of code; more comments.

v0.3:
	Reveals the number of bombs around where you are standing (and kills you if you stand on it).  Also fixed an error due to forgetting that -1 is a valid input for list indexing, which lead to phantom bombs.  Added an extra check to avoid that.

v0.2:
	calculates the number of bombs correctly according to a few tests.
	immediate todo for next version: allow user to click for bombs, and reveal the number of surrounding bombs.
	automatic revealing of 'zero squares' will be done in a future build.

v0.1: 
	places mines and shows the playing field
	immediate todo for the next version: calculate and show the number of bombs surrounding any spot that isn't a bomb 
	
