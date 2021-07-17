# Sample number 2. Shows a basic, working search. Use left and right arrow keys for navigation.

auth = ('xX_420_Panda_Vapelord_420_Xx', '1234567890abcdef1234567890abcdef')
search = "ears_up rating:s feral -text duo"

def on_key(editor, key_event):
    if key_event.keysym == "Left" or key_event.keysym == "Right":
        do_arrow_key(editor, key_event)
    elif key_event.keysym == "Escape":
        do_quit(editor)
#    else:
#        print("You pressed a key I don't know!")
#        print("It looks like this:", key_event)


default_text = 'No image here.\nLooks like you finished your project!\nCONGLATURATION !!!'

def do_quit(editor):
    editor.quit()

def do_arrow_key(editor, key_event):
    if key_event.keysym == 'Right':
        #print('Doing right arrow key.')
        editor.next()
    elif key_event.keysym == 'Left':
        #print('Doing left arrow key')
        editor.previous()
    else:
        print('I don\'t know that arrow key?', key_event)



