from conf.conf import conf
from lib.parse_dialogs import get_dialogs

dialogs = get_dialogs(conf)

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
        r = f"There are {len(machines)} machines on your network:\n"
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
            return "Already logged to this machine."
        elif args[0] == "info":
            return level.connection
        elif args[0] == "back":
            if len(level.connection) > 1:
                level.connection.pop()
                return "Disconnected"
            else:
                return "Already on your host machine."
        else:
            for m in machines:
                if m.ip == args[0]:
                    level.connection.append(m)
                    return f"Haxxed into {m.hostname}"
            return f"Found no machine with ip {args[0]}."

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


class HackerMachine0(Machine):
    def command_self_destruct(self, *args, **kwargs):
        level = kwargs["level"]
        pwd = input("Please enter password\n-> ")
        if pwd == "verynoob":
            level.done = True
            return "Self destructing..."
        else:
            return "Wrong password"


class HackerMachine1(Machine):
    def command_temper_code(self, *args, **kwargs):
        level = kwargs["level"]
        for m in level.machines:
            if "trojan.code" in m.files:
                m.files["trojan.code"] = "while True:\n\tsend_data_destroyer()  # leet move\n\tsend_troll_face()"
                level.tempered = True
                return "Tempered the code !"
        return "Nothing to temper with..."

    def command_update_code(self, *args, **kwargs):
        level = kwargs["level"]
        if "tempered" in level.__dict__:
            level.done = True
            return "Pushing the code online..."
        else:
            return "This has no effect..."


class Level():
    def __init__(self, machines, start_dialogs, end_dialogs):
        self.done = False
        self.machines = machines
        self.connection = [self.machines[0]]
        self.start_dialogs = start_dialogs
        self.end_dialogs = end_dialogs

    def play(self, game):
        player_input = input("> ")
        r = self.connection[-1].input_command(player_input, game, self)
        print(r)


level_0 = Level(
    machines = [
        Machine(conf["player_name"], "10.100.100.1337"),
        HackerMachine0("Hacker", "10.100.100.noob", {"README.md": "pwd: verynoob"}),
        ],
    start_dialogs = dialogs["start_level_0"],
    end_dialogs = dialogs["end_level_0"],
)

level_1 = Level(
    machines = [
        Machine(conf["player_name"], "10.100.100.1337", {"logs.txt": "*Utterly unreadible russian, bullshit. Don't even look at it, hack away!*"}),
        HackerMachine1("Hacker", "10.100.100.logger", {"trojan.code": "while True:\n\tsteal_data()\n\ttry_to_destroy_logs()"}),
        ],
    start_dialogs = dialogs["start_level_1"],
    end_dialogs = dialogs["end_level_1"],
)


class Game():
    def __init__(self):
        self.on = True
        print(dialogs["splash"])
        self.levels = [
            #level_0,
            level_1
        ]
        self.level_index = 0

    def play(self):
        # Start level
        self.level = self.levels[self.level_index]
        print(self.level.start_dialogs)
        # Play level
        while self.on and not self.level.done:
            self.level.play(self)
        if not self.on:
            return
        # End level
        print(self.level.end_dialogs)
        if self.level_index < len(self.levels) - 1:
            self.level_index += 1
        else:
            print("You finised the whole game!")
            print("Hoped you liked it")
            self.on = False


def main():
    g = Game()
    while g.on:
        g.play()


if __name__ == "__main__":
    main()

