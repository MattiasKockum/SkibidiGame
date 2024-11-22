def fill_template(vars_dict, template):
    for key, value in vars_dict.items():
        template = template.replace(key, str(value))
    return template

def get_dialogs(conf):
    with open("lib/dialogs.txt", 'r') as f:
        dialogs = f.readlines()
    dialogs = ''.join(dialogs)
    dialogs = dialogs.split("\n\n")
    dialogs = [l.split("\n") for l in dialogs]
    dialogs = {l[0]: fill_template(conf, '\n'.join(l[1:])) for l in dialogs}
    return dialogs
