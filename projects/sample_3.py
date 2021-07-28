# Sample number 3. An actual tagging project I use (besides a real auth tuple, of course)
auth = ('xX_420_Panda_Vapelord_420_Xx', '1234567890abcdef1234567890abcdef')
search = '-solo -duo -trio -group -none_pictured -set:conman_test order:id_asc'

default_text = 'No image here.\nLooks like you finished your project!\nCONGLATURATION !!!'

SHIFT                = 0b000000000001
CAPS_LOCK            = 0b000000000010
CONTROL              = 0b000000000100
ALT                  = 0b000000001000
NUMBER_LOCK          = 0b000000010000
POSSIBLY_SCROLL_LOCK = 0b000000100000         # I haven't verified this.
WINDOWS              = 0b000001000000
UNKNOWN              = 0b000010000000       # No clue what this could be.
LEFT_MOUSE_BUTTON    = 0b000100000000
MIDDLE_MOUSE_BUTTON  = 0b001000000000
RIGHT_MOUSE_BUTTON   = 0b010000000000
OTHERS_MAYBE         = 0b100000000000
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
    's':'solo', 'd':'duo', 'g':'group', 'n':'none_pictured', 't':'trio'
}

focus_tags = ['solo', 'duo', 'group', 'none_pictured', 'trio', 'male', 'female']

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
    elif symbol == 'return':
        editor.go_to_review()
    elif symbol == 'p':
        print(editor.changes)
#    else:
#        print(symbol)


