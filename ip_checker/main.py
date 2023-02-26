"""
The module manages the graphical interface of the program (gtk3) and
the main logic.

Author: Mikhail Gurov
Last Modified: Feb 06, 2023
"""
#!/usr/bin/env python3.10
# -- coding: utf-8 --

from find_ip import GetMyIP, FailedToGetIP
from check_ip import IPAddressVerification
import languages
from loguru import logger

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

logger.add(
        'main.log.txt',
        format='{time}, {level}, {module}:{line} -> {message}. {exception}',
        level='ERROR',
        rotation='10MB', compression='zip',
        serialize=False,
        )

class VisibleWindow(gtk.Window):
    """
    Provides drawing of the application window and all its
    elements, and also contains the logic of the application.

    Methods:
        __init__: class initialization;
        add_button_toggle_start: adding a control button to the program;
        add_display_upper: adding a display to a program;
        add_display_middle: adding a display to a program;
        add_display_lower: adding a display to a program;
        add_entry_ip: adding a text input field to a program;
        add_stable_text: adding a line of text to a program;
        main: application logic management.
        on_close: the method of disabling the program, triggered by pressing the cross.
        start: method for launching the program logic module.
        template_main: creation of the main window of the application.

    Exceptions:
        In developing...
    """

    def __init__(self, *args, **kwargs):
        """
        Program initialization, graphics launch, creation of global variables.

        Parameters:
            *args, **kwargs:
        """
        super().__init__(*args, **kwargs)

        # Rules for rendering the main window and getting the global variable window
        self.template_main()
        WINDOW.show() # Starting the rendering of the main window
        WINDOW.connect('delete-event', self.on_close) # Cross click event

        # Add all displays
        self.display_upper = self.add_display_upper()
        self.display_middle = self.add_display_middle()
        self.display_lower = self.add_display_lower()
        self.stable_text = self.add_stable_text()

        # Add input field
        self.entry_ip = self.add_entry_ip()

        # Set default interface language
        self.user_language = 1 # 0=en, 1=ru
        # Passing a language dictionary to a variable
        self.lang_dict = languages.lang

        # Setting up buttons
        self.button = self.add_button_toggle_start() # Add button
        self.button.connect('clicked', self.start) # Button click event

        # Default value of displays
        self.stable_text.set_label(
                self.lang_dict['program_description'][self.user_language])
        self.display_upper.set_text(
                self.lang_dict['vpn_status_unknown'][self.user_language])
        self.display_middle.set_text(
                self.lang_dict['waiting_for_incoming_data'][self.user_language])
        self.display_lower.set_text('')
        self.button.set_label(
                self.lang_dict['make_comparison'][self.user_language])

        # Initialization of the program name in the top line
        WINDOW.set_title(self.lang_dict['program_name'][self.user_language])

        # Initialization of parameters for the input string
        self.entry_ip.set_max_length(16) # Maximum number of characters to enter
        self.entry_ip.set_placeholder_text(
                self.lang_dict['default_input_field_value'][self.user_language])
        self.entry_ip.set_text('') # Default search value

        #  TODO: need to fix
        self.your_request_is_user_input = ''

    def main(self):
        """
        Application logic management.
        """
        logger.info('The button was pressed, exiting the standby mode')

        # Default value of displays
        self.stable_text.set_label(
                self.lang_dict['program_description'][self.user_language])
        self.display_upper.set_text(
                self.lang_dict['vpn_status_unknown'][self.user_language])
        self.display_middle.set_text(
                self.lang_dict['waiting_for_incoming_data'][self.user_language])
        self.display_lower.set_text('')
        self.button.set_label(
                self.lang_dict['make_comparison'][self.user_language])

        # Getting data from the user
        input_field_data  = self.entry_ip.get_text()
        self.entry_ip.set_text('') # Clearing the input field

        logger.info('Read user data, input field cleared')

        # Preparing compound strings for displays
        your_request_is = self.lang_dict['your_request_is'][self.user_language]
        user_input = str(input_field_data)
        self.your_request_is_user_input = your_request_is + user_input

        # Check for empty input
        if input_field_data  == '':
            logger.info('The user has entered nothing')
            # Customization of displays and button
            self.display_upper.set_text(
                    self.lang_dict['vpn_status_unknown'][self.user_language])
            self.display_middle.set_text(
                    self.lang_dict['no_data_entered'][self.user_language])
            self.display_lower.set_text(
                    self.lang_dict['try_again'][self.user_language])
            self.button.set_label(
                    self.lang_dict['make_comparison'][self.user_language])
            return None

        logger.info('Preliminary data checks passed')

        # Customization of displays and button
        self.display_upper.set_text(
                self.lang_dict['vpn_status_checked'][self.user_language])
        self.display_middle.set_text(
                self.lang_dict['wait_for_information'][self.user_language])
        self.display_lower.set_text(
                self.your_request_is_user_input)
        self.button.set_label(
                self.lang_dict['stop'][self.user_language])

        logger.info('We begin the procedure for obtaining the current external IPv4 address')

        try:
            ip_search = GetMyIP()
        except NameError  as exc:
            logger.error(f'An attempt to create an instance of the GetMyIP class failed: {exc}')
            return None

        try:
            # DEBUG: If there is connection problem - the process slows down the program
            current_ip = str(ip_search.get())
            logger.info(f'External IP lookup module returned result: {current_ip}')
        except FailedToGetIP as exc:
            logger.error(f'Attempt to get IP failed: {exc}')
            # Customization of displays and button
            self.display_upper.set_text(
                    self.lang_dict['vpn_status_unknown'][self.user_language])
            self.display_middle.set_text(
                    self.lang_dict['failed_to_get_ip'][self.user_language])
            self.display_lower.set_text(
                    self.lang_dict['network_problem'][self.user_language])
            self.button.set_label(
                    self.lang_dict['make_comparison'][self.user_language])
            return None

        if current_ip is None:
            logger.info('Failed to get external IP address')
            # Customization of displays and button
            self.display_upper.set_text(
                    self.lang_dict['vpn_status_checked'][self.user_language])
            self.display_middle.set_text(
                    self.lang_dict['failed_to_get_ip'][self.user_language])
            self.display_lower.set_text(
                    self.lang_dict['try_again'][self.user_language])
            self.button.set_label(
                    self.lang_dict['make_comparison'][self.user_language])
            return None

        # Starting the comparison process
        logger.info('Starting the comparison process')
        try:
            comparison = IPAddressVerification()
            comparison.current_ip = current_ip
            comparison.user_ip = input_field_data
        except NameError as exc:
            logger.info('An attempt to instantiate the\
                        IPAddressVerification class failed.')
            return None
        result = comparison.run()
        logger.info(f'The comparison procedure is completed.\
                    Comparison result obtained: {str(result)}')

        if result is None:
            logger.warning('Comparison failed.')
            # Customization of displays and button
            self.display_upper.set_text(
                    self.lang_dict['vpn_status_unknown'][self.user_language])
            self.display_middle.set_text(
                    self.lang_dict['failed_to_ip_check'][self.user_language])
            self.display_lower.set_text(
                    self.lang_dict['try_again'][self.user_language])
            self.button.set_label(
                    self.lang_dict['make_comparison'][self.user_language])
            return None

        # Returned IPComparisonResult - normal scenario
        try:
            if result[0] is True:
                self.display_upper.set_text(
                        self.lang_dict['vpn_status_active'][self.user_language])
                self.display_middle.set_text(f'{str(result[1])} = {result[2]}')
                self.display_lower.set_text('')
                self.button.set_label(
                        self.lang_dict['make_comparison'][self.user_language])
            elif result[0] is False:
                self.display_upper.set_text(
                        self.lang_dict['vpn_status_not_active'][self.user_language])
                self.display_middle.set_text(f'{str(result[1])} ≠ {result[2]}')
                self.display_lower.set_text('')
                self.button.set_label(
                        self.lang_dict['make_comparison'][self.user_language])
        except IndexError as exc:
            logger.warning(f'Attempt to contact IPComparisonResult by index failed: {exc}')
            return None
        return None


    def template_main(self):
        """
        Creation of the main window of the application.
        """
        layout_main = 'template'
        self.builder = gtk.Builder()
        self.builder.add_from_file(layout_main)
        global WINDOW
        WINDOW = self.builder.get_object('id_window_main')


    def add_display_upper(self):
        """
        Adding a display to a program.
        """
        value = self.builder.get_object('id_display_upper')
        return value


    def add_display_middle(self):
        """
        Adding a display to a program.
        """
        value = self.builder.get_object('id_display_middle')
        return value

# Passing a language dictionary to a variable
    def add_display_lower(self):
        """
        Adding a display to a program.
        """
        value = self.builder.get_object('id_display_lower')
        return value


    def add_stable_text(self):
        """
        Adding a line of text to a program.
        """
        value = self.builder.get_object('id_program_description')
        return value


    def add_entry_ip(self):
        """
        Adding a text input field to a program.
        """
        value = self.builder.get_object('id_entry_ip')
        return value


    def add_button_toggle_start(self):
        """
        Adding a control button to the program.
        """
        value = self.builder.get_object('id_button_compare-stop')
        return value


    def on_close(self, widget, event):
        """
        The method of disabling the program, triggered by pressing
        the cross.

        Parameters:
            widget: will be written...
            event: will be written...
        """
        logger.info('The cross has been pressed.')
        gtk.main_quit() # Close window


    @logger.catch # Tracking Uncaught Exceptions
    def start(self, button):
        """
        Method for launching the program logic module.
        Issued separately in order to catch exceptions with a logger.

        Parameters:
            button: will be written...
        """
        self.main()

class Activate:
    """
    Creating an instance of the program class for the further launch procedure.
    """
    def __init__(self):
        self.WINDOW = VisibleWindow()

if __name__ == '__main__':
    Activate()
    gtk.main()
