from MasterInstaller import *
from LaunchCondition import *
import os
import sys


class SampleInstaller(MasterInstaller):
    def __init__(self):
        self.launch_condition_table.append(LaunchCondition('MinimumWindowsVersion:6.1',
                                                           'This program requires Windows 7 or later'))
        self.launch_condition_table.append(LaunchCondition('MinimumPythonVersion:3',
                                                           'This program requires Python 3 or later'))

    def is_upgrade(self):
        file_to_test = os.path.join(os.environ['ProgramFiles'], 'SampleProgram', 'README.txt')
        return os.path.exists(file_to_test)


if __name__ == '__main__':
    # TODO parse command-line params
    setup = SampleInstaller()
    result = setup.run(user_interface_level=UILevel.UI_NONE, logging_level=logging.INFO)
    sys.exit(result)
