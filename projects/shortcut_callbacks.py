# For a complete list, see https://www.tcl.tk/man/tcl8.6/TkCmd/keysyms.html
example_keysyms = {
    'unprintable' : {'Alt_L', 'Alt_R', 'Caps_Lock', 'Control_L', 'Control_R', 'Shift_L',
    'Shift_R', 'Super_L', 'Super_R', 'BackSpace', 'Delete', 'Home', 'End', 'Left', 'Up',
    'Right', 'Down', 'Escape'},
    'simple_keys' : {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E',
         'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
         'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z'},
    'keys_with_other_names' : {'Return': 'Enter', 'Tab': '\t', 'ampersand': '&',
     'apostrophe': "'", 'asciicircum': '^', 'asciitilde': '~', 'asterisk': '*',
     'at': '@', 'backslash': '\\', 'bar': '|', 'braceleft': '{', 'braceright': '}',
     'bracketleft': '[', 'bracketright': ']', 'colon': ':', 'comma': ',',
     'dollar': '$', 'equal': '=', 'exclam': '!', 'grave': '`', 'greater': '>',
     'less': '<', 'minus': '-', 'numbersign': '#', 'parenleft': '(',
     'parenright': ')', 'percent': '%', 'period': '.', 'plus': '+',
     'question': '?', 'quotedbl': '"', 'semicolon': ';', 'slash': '/',
     'space': ' ', 'underscore': '_', 'Prior':'PageUp', 'Next':'PageDown'}
}

# Conman does not support modifiers at this time.
# That may change if I can figure out something less hacky.
# You can mimic the shift modifier by putting in a capital letter (so 'W' == 'Shift-w')

dummy_post = {'id':511799,
 'file':
    {'url':'https://static1.e621.net/data/0d/36/0d3696a0ea38de0df42536f48807b464.png'}
}


def say_keysym(editor, post, key_event):
    print(key_event.keysym)

def say_enter(editor, post, key_event): print('You just pressed enter!')
def say_n(editor, post, key_event): print('You just pressed n!')
def say_N(editor, post, key_event): print('You just pressed N!')
def say_left_control(editor, post, key_event): print('You just pressed the left control key!')

def say_dummy_message(editor, post, key_event):
    print('Press any of the following keys to test the print function:')
    print('[n, N, enter, left control]')
    print('Press the l key to load an image!')
    print('Press escape to exit.')

def do_quit(editor, post, key_event):
    editor.quit()
def do_dummy_load(editor, post, key_event):
    editor.set_post(dummy_post)

def do_arrow_key(editor, post, key_event):
    if key_event.keysym == 'Right':
        #print('Right arrow key')
        editor.next()
    elif key_event.keysym == 'Left':
        #print('Left arrow key')
        editor.previous()
    else:
        print('Unknown arrow key:', key_event)


