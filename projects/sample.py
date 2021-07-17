################################# Very Important Stuff  #######################
# Auth is a tuple of ('your username', 'your api key')
# Not totally necessary if you're just browsing,
# but some images are default blacklisted and you obviously can't make edits.
auth = ('xX_420_Panda_Vapelord_420_Xx', '1234567890abcdef1234567890abcdef')

# search is the search. It is optional, though you can't do much without it.
# Don't use id:<=x; put x in the last_touched field.
search = "asdffhgghasldgfh -solo -duo -group -none_pictured"



################################# Important Stuff #############################

# When a key is pressed, Conman will look in this file for a function called "on_key".
# on_key() must accept two arguments: The editor itself, and the key event object
#  (which records what key was pressed, what modifiers were held down, and some other stuff).
# Use this function for basically all the interaction in your project.
# Make sure you indent consistently! In Python, formatting is syntax. Use 4 spaces instead of tab.
# I've included a bunch of sample functions you can call like "do_arrow_key" and "do_quit".
# See more in the Example functions section.
# You can copy and paste them to make new functions;
# just be sure to change the names so Python doesn't get confused which one is which.
def on_key(editor, key_event):
    if key_event.keysym == "Escape":
        do_quit(editor)
    elif key_event.keysym == "Return":
        say_enter()
    elif key_event.keysym == "n":   # Both key events and variables are case sensitive.
        say_n()
    elif key_event.keysym == "N":   # 'N' is not the same as 'n'
        say_N()
    elif key_event.keysym == "Control_L":
        say_left_control()
    elif key_event.keysym == "l":
        do_dummy_load(editor)
    elif key_event.keysym == "h" or key_event.keysym == 'H':
        say_dummy_message()
    else:
        print("You pressed a key I don't know!")
        print("  It looks like this:", key_event)


############################# Other crap Conman can do ########################
# default_text is what shows up when the search has no images left. Optional.
default_text = 'This is the first sample project.\nPress h for a help message in the terminal.\nPress escape to exit.'


################################# Other documentation #########################
# If you want to know what the keysym is for a given key,
# load this project and press the key. It should get printed.
# For a complete list of keysyms you can use, see https://www.tcl.tk/man/tcl8.6/TkCmd/keysyms.html
# Local list:
example_keysyms = {
    'unprintable' : {'Alt_L', 'Alt_R', 'Caps_Lock', 'Control_L', 'Control_R', 'Shift_L',
    'Shift_R', 'Super_L', 'Super_R', 'BackSpace', 'Delete', 'Home', 'End', 'Left', 'Up',
    'Right', 'Down', 'Escape'},
    'simple_keys' : {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E',
         'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
         'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z'},
    'keys_with_special_names' : {'Return': 'Enter', 'Tab': '\t', 'ampersand': '&',
     'apostrophe': "'", 'asciicircum': '^', 'asciitilde': '~', 'asterisk': '*',
     'at': '@', 'backslash': '\\', 'bar': '|', 'braceleft': '{', 'braceright': '}',
     'bracketleft': '[', 'bracketright': ']', 'colon': ':', 'comma': ',',
     'dollar': '$', 'equal': '=', 'exclam': '!', 'grave': '`', 'greater': '>',
     'less': '<', 'minus': '-', 'numbersign': '#', 'parenleft': '(',
     'parenright': ')', 'percent': '%', 'period': '.', 'plus': '+',
     'question': '?', 'quotedbl': '"', 'semicolon': ';', 'slash': '/',
     'space': ' ', 'underscore': '_', 'Prior':'PageUp', 'Next':'PageDown'}
}

# Just an example post so you can test if you can load posts at all.
# See do_dummy_load in Example Functions.
dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}

#################################### Example functions ########################
def say_enter(): print('You just pressed enter!')
def say_n(): print('You just pressed n!')
def say_N(): print('You just pressed N!')
def say_left_control(): print('You just pressed the left control key!')

def say_dummy_message():
    print('Press any of the following keys to test the print function:')
    print('  [n, shift + n, enter, left control]')
    print('  Press the l key to load an image!')
    print('  Press escape to exit.')

def do_quit(editor):
    editor.quit()
def do_dummy_load(editor):
    editor.set_post(dummy_post)



