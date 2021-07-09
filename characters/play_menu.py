def main(caller, raw_string, **kwargs):
    char_dic = dict(caller.db.chars)
    text = "Choose a character to play."
    options = []
    for char in char_dic.values():
        if char is not None:
            options.append({'desc': f'{char}',
                        'goto': (_puppet_char, {'char': f'{char}'})})
    return text, options

def _puppet_char(caller, raw_string, **kwargs):
    char = kwargs.get('char')
    cmd = f"ic {char}"
    caller.execute_cmd(cmd)
    return 'exit'

def exit(caller, raw_string, **kwargs):
    options = None
