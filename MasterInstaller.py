from enum import Enum
import sys
import logging


class UILevel(Enum):
    UI_FULL = 0
    UI_REDUCED = 1
    UI_BASIC = 2
    UI_NONE = 3


class SetupStatus(Enum):
    SUCCESS = 0
    FAILED = 1
    CANCELLED = 2


class SetupType(Enum):
    FRESH = 0
    MAINTENANCE = 1
    PATCH = 2
    RESUMED = 3


class LaunchCondition:
    condition = ''  # Expression that must evaluate to True for installation to begin
    description = ''  # Localizable text to display when the condition fails and the installation must be terminated

    def __init__(self, condition, description):
        self.condition = condition
        self.description = description

    def evaluate(self):
        if self.condition:
            return True
        else:
            return False


class MasterInstaller:
    installation_script = []
    rollback_script = []
    installation_type = SetupType.FRESH
    user_interface_level = UILevel.UI_FULL
    launch_condition_table = []  # array of LaunchCondition instances

    @staticmethod
    def _display_error_message(msg):
        logging.error(msg)

    def _check_launch_conditions(self):
        for condition in self.launch_condition_table:
            result = condition.evaluate()
            if not result:
                self._display_error_message(condition.description)
                sys.exit(1)

    def _file_costing(self):
        pass

    def _run_required_user_interface(self):
        if self.installation_type == SetupType.FRESH:
            ui_wizard()
        elif self.installation_script == SetupType.MAINTENANCE:
            ui_modify_repair_remove()
        else:
            ui_notify_installation_type()

    def _execute_installation_script(self):
        result = True
        for action in self.installation_script:
            if user_pressed_cancel():
                break
            result = execute_action(action)
            if result:
                add_action_to_rollback_script(action)
            else:
                break
        return result

    def _extract_files_to_temp_folder(self):
        pass

    def _run_actions_from_ui_sequence(self):
        pass

    def run(self, user_interface_level=UILevel.UI_FULL, logging_level=logging.DEBUG):
        # Preparation
        logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logging_level)
        self.user_interface_level = user_interface_level
        self._extract_files_to_temp_folder()

        # Acquisition (no changes to the system)
        if self.user_interface_level not in [UILevel.UI_BASIC, UILevel.UI_NONE]:
            self._run_actions_from_ui_sequence()
        self._check_launch_conditions()
        application_search()
        self._file_costing()
        if user_interface_level not in [UILevel.UI_BASIC, UILevel.UI_NONE]:
            self._run_required_user_interface()
            show_progress_dialog()
        create_installation_script()

        # Execution (apply changes to the system)
        elevate_privileges()
        result = self._execute_installation_script()
        if result == SetupStatus.SUCCESS:
            run_all_commit_custom_actions()
        else:
            execute_rollback_script()

        # Finalize (no changes to the system)
        run_all_actions_after_install_finalize()
        run_all_actions_after_execute_action()
        display_installation_status(result)
