from MasterInstaller import *


class SampleInstaller(MasterInstaller):
    def __init__(self):
        self.launch_condition_table.append(LaunchCondition('sample condition', 'sample condition message'))


if __name__ == '__main__':
    # TODO parse command-line params
    setup = SampleInstaller()
    setup.run()
