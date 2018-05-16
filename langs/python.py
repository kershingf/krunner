import os

from krunner.utils.shell import Shell
from krunner.validates.validate import Validate
from .lang_loader import StandardClass


class Python(StandardClass):

    virtualenv = None

    def __init__(self, window, krunner_settings):
        self.validation = Validate(krunner_settings)

        self.validation.TYPES.update({
            'virtualenv': (str, False, )
        })

        if not self.validation.is_valid():
            return

        super(Python, self).__init__(window, krunner_settings)
        self.virtualenv = krunner_settings.get('virtualenv', None)

    def run(self):
        python = "python"
        if self.virtualenv is not None:
            python = os.path.join(self.virtualenv, python)

        command = "%s \"%s\"" % (python, self.main_file)
        Shell(self.window, self.shell, command, self.main_file).run()
