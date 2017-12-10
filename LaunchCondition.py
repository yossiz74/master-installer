import platform

#
# Define a condition in the format: variable:value
# Currently supported variables:
# - MinimumWindowsVersion
#   (as reported by the 'ver' command. For example, use '6.1' for Windows 7)
# - MinimumPythonVersion
#


class LaunchCondition:
    condition = ''  # Expression that must evaluate to True for installation to begin
    description = ''  # Localizable text to display when the condition fails and the installation must be terminated

    def __init__(self, condition, description):
        self.condition = condition
        self.description = description

    def evaluate(self):
        variable, value = self.condition.split(':')
        if variable.lower() == 'MinimumWindowsVersion'.lower():
            win_ver = platform.version()
            return win_ver >= value
        elif variable.lower() == 'MinimumPythonVersion'.lower():
            python_ver = platform.python_version()
            return python_ver >= value
        elif self.condition:
            return True
        else:
            return False
