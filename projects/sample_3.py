# Sample number 3. An actual tagging project I use (with a real auth tuple, of course)
auth = ('xX_420_Panda_Vapelord_420_Xx', '1234567890abcdef1234567890abcdef')
search = '-solo -duo -group -none_pictured -set:trickytagscharactercount order:id_asc'

default_text = 'No image here.\nLooks like you finished your project!\nCONGLATURATION !!!'

def on_key(editor, key_event):
    if key_event.keysym == "Left" or key_event.keysym == "Right":
        do_arrow_key(editor, key_event)
    elif key_event.keysym == "Escape":
        do_quit(editor)
    else:
        print(key_event.keysym)

def do_quit(editor):
    editor.quit()

def do_arrow_key(editor, key_event):
    if key_event.keysym == 'Right':
        editor.next()
    else:
        editor.previous()

