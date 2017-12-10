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


class MasterInstaller:
    installation_script = []
    rollback_script = []
    installation_type = SetupType.FRESH
    user_interface_level = UILevel.UI_FULL
    launch_condition_table = []  # array of LaunchCondition instances

    # Product-specific functions - must override
    # TODO: use abstract classes
    def is_upgrade(self):
        return False

    # General-purpose functions
    def _display_error_message(self, msg):
        logging.error(msg)
        if self.user_interface_level != UILevel.UI_NONE:
            # TODO: show message to user
            pass

    def _check_launch_conditions(self):
        logging.debug("[Action start] LaunchConditions")
        return_value = 0
        err_msg = ''
        for condition in self.launch_condition_table:
            logging.debug("Evaluating launch condition: {}".format(condition.condition))
            result = condition.evaluate()
            # logging.debug(str(result))
            if not result:
                err_msg = condition.description
                return_value = -1
                break
        logging.debug("[Action ended] LaunchConditions. Return value {}".format(return_value))
        return return_value, err_msg

    def _file_costing(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _ui_wizard(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _ui_modify_repair_remove(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _ui_notify_installation_type(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _run_required_user_interface(self):
        if self.installation_type == SetupType.FRESH:
            self._ui_wizard()
        elif self.installation_script == SetupType.MAINTENANCE:
            self._ui_modify_repair_remove()
        else:
            self._ui_notify_installation_type()

    def _user_pressed_cancel(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        return False

    def _execute_action(self, action):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        return False

    def _add_action_to_rollback_script(self, action):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _execute_installation_script(self):
        result = True
        for action in self.installation_script:
            if self._user_pressed_cancel():
                break
            result = self._execute_action(action)
            if result:
                self._add_action_to_rollback_script(action)
            else:
                break
        return result

    def _extract_files_to_temp_folder(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _run_actions_from_ui_sequence(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _application_search(self):
        if self.is_upgrade():
            # TODO detect installed related products
            logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        else:
            logging.info("Product not registered: beginning first-time install")

    def _show_progress_dialog(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _create_installation_script(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _elevate_privileges(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _run_all_commit_custom_actions(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _execute_rollback_script(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _run_all_actions_after_install_finalize(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _run_all_actions_after_execute_action(self):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def _display_installation_status(self, result):
        logging.warning(sys._getframe().f_code.co_name + " UNIMPLEMENTED YET")
        pass

    def run(self, user_interface_level=UILevel.UI_FULL, logging_level=logging.DEBUG):
        # Preparation
        logging.basicConfig(format='%(asctime)s\t\t%(levelname)s\t\t%(message)s', level=logging_level)
        logging.debug("Verbose logging started")
        self.user_interface_level = user_interface_level
        is_ui_none_or_basic = self.user_interface_level in [UILevel.UI_BASIC, UILevel.UI_NONE]
        if is_ui_none_or_basic:
            logging.info("UI is none or basic")
        result = 0
        try:
            self._extract_files_to_temp_folder()
            # Acquisition (no changes to the system)
            if not is_ui_none_or_basic:
                self._run_actions_from_ui_sequence()
            self._application_search()
            result, err_msg = self._check_launch_conditions()
            if result != 0:
                raise RuntimeError(err_msg)
            self._file_costing()
            if not is_ui_none_or_basic:
                self._run_required_user_interface()
                self._show_progress_dialog()
            self._create_installation_script()
            # Execution (apply changes to the system)
            self._elevate_privileges()
            result = self._execute_installation_script()
            if result == SetupStatus.SUCCESS:
                self._run_all_commit_custom_actions()
            else:
                self._execute_rollback_script()
            # Finalize (no changes to the system)
            self._run_all_actions_after_install_finalize()
            self._run_all_actions_after_execute_action()
            self._display_installation_status(result)
        except RuntimeError as e:
            self._display_error_message(str(e))
        logging.info("Result: {}".format(result))
        return result
