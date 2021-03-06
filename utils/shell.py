import subprocess


class Shell:

    def __init__(self, window, shell, command, main_file=str()):
        self.window = window
        self.shell = shell
        self.command = command
        self.main_file = main_file

    def __get_shell_command(self):
        folder = self.window.extract_variables()['folder']
        if self.shell == 'deepin-terminal':
            return (
                "%s -w \"%s\" -e \"%s\"" %
                (self.shell, folder, "\" \"".join(self.command))
            )
        elif self.shell == 'gnome-terminal':
            return (
                "%s --working-directory=\"%s\" -- \"%s\"" %
                (self.shell, folder, "\" \"".join(self.command))
            )
        elif self.shell == 'xfce4-terminal':
            return (
                "%s --working-directory=\"%s\" -H -e '\"%s\"'" %
                (self.shell, folder, "\" \"".join(self.command))
            )
        elif self.shell == 'xterm':
            return (
                "%s -hold -T 'Running' -e 'cd %s && \"%s\" && echo \"\
                \t****Finished****\"'" %
                (self.shell, folder, "\" \"".join(self.command))
            )
        elif self.shell == 'konsole':
            return (
                "%s --hold --workdir \"%s\" -e \"%s\"" %
                (self.shell, folder, "\" \"".join(self.command))
            )
        #  elif self.shell == 'pantheon-terminal':
        #     return (
        #         "%s --working-directory=\"%s\" -e \"%s\"" %
        #         (self.shell, folder, "ls")
        #     )

        return None

    def __input_args(self, args=None):
        if args is None:
            self.window.show_input_panel(
                "args", str(), self.__input_args, None, None
            )
            return
        else:
            self.command += args.split()
            self.__run()

    def __run(self):
        execute = self.__get_shell_command()

        if execute is None:
            return

        print(execute)
        subprocess.Popen(execute, shell=True)
        self.window.status_message(
            "\tPlease wait... Running %s" % self.main_file
        )

    def show_menu(self, item_selected=None):
        """ Recursive function """
        if item_selected is None:
            self.window.show_quick_panel(
                [' '.join([self.main_file, item]) for item in self.menu_items],
                self.show_menu
            )
            return
        elif item_selected > -1:
            if item_selected > 0 and item_selected != len(self.menu_items) - 1:
                self.command += [self.menu_items[item_selected]]
            else:
                self.__input_args()
                return
            self.__run()
