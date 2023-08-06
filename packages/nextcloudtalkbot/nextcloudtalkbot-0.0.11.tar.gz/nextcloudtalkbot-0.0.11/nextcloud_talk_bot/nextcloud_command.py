import sys
import importlib
from docopt import docopt
from . import *

class NextcloudCommand:
    def __init__(self, script_name):
        self.script_name = script_name
        self.script_module = self._import_script()
        self.docstrings = self._get_docstrings()

    def _import_script(self):
        script_module = importlib.import_module(self.script_name)
        return script_module

    def _get_docstrings(self):
        return self.script_module.__doc__

    def execute(self, argv):
        arguments = docopt(self.docstrings, argv=argv, help=True)
        print(arguments)

if __name__ == "__main__":
    script_name = "your_script_name"  # Replace with the name of your script (without the .py extension)
    nextcloud_command = NextcloudCommand("first_run_setup.py")
    nextcloud_command.execute(sys.argv[1:])