from conf.conf import conf
from lib.parse_dialogs import get_dialogs

dialogs = get_dialogs(conf)

def dialog(name):
    print(dialogs[name])

class Machine():
    def __init__(self, hostname, ip, files={}):
        self.hostname = hostname
        self.ip = ip
        self.files = files

    def __repr__(self):
        return f"{self.hostname}: {self.ip}"

    def input_command(self, player_input, game, level):
        command = player_input.split(" ")
        command_function = f"command_{command[0]}"
        if command_function not in self.__dir__():
            r = f"No command named {command[0]}. Try 'help'."
        else:
            args = command[1:]
            r = self.__getattribute__(command_function)(args, level=level, game=game)
        return r

    def command_quit(self, *args, **kwargs):
        game = kwargs["game"]
        game.on = False
        return "Goodbye"

    def command_help(self, *args, **kwargs):
        commands = [c[8:] for c in self.__dir__() if c[:7] == "command"]
        return commands

    def command_network_scan(self, *args, **kwargs):
        level = kwargs["level"]
        machines = level.machines
        r = f"There are {len(machines)} machines on your network\n"
        for m in machines:
            r += str(m) + '\n'
        return r

    def command_sshaxxx(self, *args, **kwargs):
        level = kwargs["level"]
        machines = level.machines
        args = args[0]
        if len(args) != 1:
            return "usage: sshaxxx [ip to haxxx into] | back | info"
        elif args[0] == level.connection[-1].ip:
            return "Already logged to this machine"
        elif args[0] == "info":
            return level.connection
        elif args[0] == "back":
            if len(level.connection) > 1:
                level.connection.pop()
                return "Disconnected"
            else:
                return "Already on your host machine"
        else:
            for m in machines:
                if m.ip == args[0]:
                    level.connection.append(m)
                    return f"Haxxed into {m.hostname}"
            return f"Found no machine with ip {args[0]}"

    def command_ls(self, *args, **kwargs):
        return '\n'.join(self.files)

    def command_cat(self, *args, **kwargs):
        args = args[0]
        if len(args) != 1:
            return "usage: cat [file to cat]"
        if args[0] in self.files:
            return self.files[args[0]]
        else:
            return f"No file named {args[0]}"

class HackerMachine(Machine):
    def command_self_destruct(self, *args, **kwargs):
        level = kwargs["level"]
        pwd = input("Please enter password\n-> ")
        if pwd == "verynoob":
            level.done = True
            return "Self destructing..."
        else:
            return "Wrong password"


class Level_0():
    def __init__(self, game):
        #self.game = game
        self.done = False
        self.machines = [
            Machine(conf["player_name"], "10.100.100.1337"),
            HackerMachine("Hacker", "10.100.100.noob", {"README.md": "pwd: verynoob"}),
        ]
        self.connection = [self.machines[0]]
        dialog("level_1")


class Game():
    def __init__(self):
        self.on = True
        dialog("splash")
        self.levels = [Level_0]
        self.level = self.levels[0](self)
        self.level_index = 0

    def play(self, player_input):
        r = self.level.connection[-1].input_command(player_input, self, self.level)
        if self.level.done:
            r += "\nYou win"
            if self.level_index < len(self.levels) - 1:
                self.level_index += 1
                self.level = self.levels[self.level_index](self)
            else:
                r += "\nYou finised the whole game!"
                r += "\nHoped you liked it"
                self.on = False
        return r

def main():
    g = Game()
    while g.on:
        player_input = input("> ")
        r = g.play(player_input)
        print(r)


if __name__ == "__main__":
    main()

