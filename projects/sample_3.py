# Sample number 3. An actual tagging project I use (with a real auth tuple, of course)
auth = ('xX_420_Panda_Vapelord_420_Xx', '1234567890abcdef1234567890abcdef')
search = '-solo -duo -group -none_pictured -set:trickytagscharactercount order:id_asc'

default_text = 'No image here.\nLooks like you finished your project!\nCONGLATURATION !!!'

SHIFT = 0b1
CAPS_LOCK = 0b10
CONTROL = 0b100
ALT = 0b1000
NUMBER_LOCK = 0b10000
POSSIBLY_SCROLL_LOCK = 0b100000 # I haven't verified this.
WINDOWS = 0b1000000
UNKNOWN = 0b10000000            # No clue what this could be.
LEFT_MOUSE_BUTTON = 0b100000000
MIDDLE_MOUSE_BUTTON = 0b1000000000
RIGHT_MOUSE_BUTTON = 0b10000000000
# This is kind of awkward, but it's how tk returns key event modifiers.
# So we have to live with it.
# To check if x button was held down while the key was pressed, do
#   if NAME & key_event.state:
# where NAME is, for example, ALT.
# So to find key events that are control + w, do
#   if CONTROL & key_event.state and key_event.keysym == 'w':
# Note that shift will still toggle the case of the keysym!
# So compare against key_event.keysym.lower() to standardize as lowercase.

toggle_list = { # Python dict. Very handy structure, lots of uses.
    's':'solo', 'd':'duo', 'g':'group', 'n':'none_pictured'
}

def on_key(editor, key_event):
    symbol = key_event.keysym.lower()
    if symbol == "left":
        editor.previous()
    elif symbol == "right":
        editor.next()
    elif symbol == "escape" or (CONTROL & key_event.state and symbol == 'w'):
        editor.quit()
    elif symbol in toggle_list.keys():  # s, d, g for character count
        tag = toggle_list[symbol]
        if SHIFT & key_event.state:             # shift + s and shift + d
            tag += '_focus'
        editor.toggle_tag(tag)
    elif symbol == 'space':
        editor.toggle_tag('set:conman_test')
    elif symbol == 'p':
        print(editor.changes)
#    else:
#        print(symbol)


