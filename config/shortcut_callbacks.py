dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}

# For a complete list, see https://www.tcl.tk/man/tcl8.6/TkCmd/keysyms.html
example_keysyms = {
    'unprintable' : {'Alt_L', 'Alt_R', 'Caps_Lock', 'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Super_L', 'Super_R', 'BackSpace', 'Delete'},
    'simple_keys' : {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E',
         'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
         'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z'},
    'keys_with_strange_names' : {'Return': '\n', 'Tab': '\t', 'ampersand': '&',
     'apostrophe': "'", 'asciicircum': '^', 'asciitilde': '~', 'asterisk': '*',
     'at': '@', 'backslash': '\\', 'bar': '|', 'braceleft': '{', 'braceright': '}',
     'bracketleft': '[', 'bracketright': ']', 'colon': ':', 'comma': ',',
     'dollar': '$', 'equal': '=', 'exclam': '!', 'grave': '`', 'greater': '>',
     'less': '<', 'minus': '-', 'numbersign': '#', 'parenleft': '(',
     'parenright': ')', 'percent': '%', 'period': '.', 'plus': '+',
     'question': '?', 'quotedbl': '"', 'semicolon': ';', 'slash': '/',
     'space': ' ', 'underscore': '_'}
}

# Conman does not support modifiers at this time.
# That may change if I can figure out something less hacky.
# You can mimic the shift modifier by putting in a capital letter (so 'W' == 'Shift-w')
'''
# For an event to happen when you have a modifier key, like ctrl + w,
# list the keysym as `Control-w`.
# If you want multiple modifier keys, they must be in alphabetical order,
# like `Alt-Control-Shift-Return`. That's not a tkinter problem, that's a Conman problem.
# Keep in mind that the Shift modifier will also invert your capitalization.
# So `Control-Shift-w` will not work (because Shift turns the `w` keystroke into `W`).
# Use `Control-Shift-W` instead. Unless you're messing around with Caps_Lock...'''

def say_enter(conman, post, key_event):
    print('You just pressed enter!')
def say_n(conman, post, key_event):
    print('You just pressed n!')
def say_N(conman, post, key_event):
    print('You just pressed N!')
def say_left_control(conman, post, key_event):
    print('You just pressed the left control key!')
def say_help(conman, post, key_event):
    print('Press any of the following keys to test the print function:')
    print('[n, N, enter, left control]')
    print('Press the l key to load an image!')
def do_load(conman, post, key_event):
    conman.set_post(dummy_post)

