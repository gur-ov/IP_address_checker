"""
Comparison of external external IPv4 addresses with another presented to
compare with an IPv4 address.

Author: Mikhail Gurov
Last Modified: Feb 06, 2023
"""
#!/usr/bin/env python3.10
# -- coding: utf-8 --

from ipaddress import ip_address
from typing import Union, NamedTuple
from loguru import logger
from find_ip import GetMyIP

logger.add(
        'check_ip.log.txt',
        format='{time}, {level}, {module}:{line} -> {message}. {exception}',
        level='ERROR',
        rotation='10MB', compression='zip',
        serialize=False,
        )

class IPComparisonResult(NamedTuple):
    """
    This class of descriptions for the type of data that should be obtained
    as a result of the successful operation of the "run" method
    """
    result: bool
    user_input: str
    current_ip: str

class IPAddressVerification():
    """
    Comparison of external external IPv4 addresses with another presented
    to compare with an IPv4 address.

     Methods:
         __init__: class initialization;
         ipv4_type_check: check data against IPv4m data characteristics;
         data_normalization: string normalization;
         data_type_check: data check for page data check;
         comparison_ipv4: compare IPv4 addresses;
         run: Run a process method.

     Class level variables:
         self.user_input: string from the user suspected IPv4 address;
         self.current_ip: the device's current external IPv4 address.

     Exceptions:
         In developing.

     External resources:
         GetMyIP module - external external IPv4 addresses of the device.
    """


    def __init__(self,
            user_input:str = '127.0.0.1',
            current_ip:str = '127.0.0.1'):
        """
        """
        self.user_input = user_input
        self.current_ip = current_ip


    @logger.catch
    def ipv4_type_check(self, ipv4_to_check:str) -> Union[bool, None]:
        """
        Checking if the contents of a string is an IPv4 address.

        Parameters:
            ipv4_to_check (str): string with IPv4 addresses.

        Returns:
            bool: True if ipv4_to_check is IPv4 address;
            None: if any error occurred.
        """
        try:
            ipv4 = ip_address(ipv4_to_check)
        except ValueError as exc:
            logger.warning(f'Variable does not contain an IP address.\
                    Value: {ipv4_to_check}. {exc}')
            return None
        try:
            if ipv4.version == 4:
                return True
        except AttributeError as exc:
            logger.error(f'The variable does not contain an IPv4 address. Value: {ipv4}. {exc}')
            return None
        return False


    @logger.catch
    def data_normalization(self, user_string:str) -> Union[str, None]:
        """
        Attempt to normalize user input. An IPv4 address is expected,
        but several typical input errors are expected:
            - Spaces at the beginning and end of the line;
            - Commas instead of dots.
        The method must take a string, normalize it,
        and return it to its normalized form.

        Parameters:
            user_string (str): string entered by the user.

        Returns:
            str: normalized string;
            None: if any error occurred.
        """
        #if type(user_string) is not str:
        if not isinstance(user_string, str):
            logger.error(f'The data from the user is not a string. Value: {user_string}')
            return None
        user_string_strip =  user_string.strip()
        normalized_input = user_string_strip.replace(',', '.')
        return normalized_input


    @logger.catch
    def data_type_check(self, user_input: Union[str, int, float]) -> Union[str, None]:
        """
        Checking if the information received by the module is a string.
        If the received data is not a string, the method should try to make
        a string out of it.

        Parameters:
             user_input: data of arbitrary type passed to the module.

        Returns:
            str: checked string;
            None: if any error occurred.
        """
        if isinstance(user_input, str):
            return user_input
        try:
            user_input = str(user_input)
            return user_input
        except TypeError as exc:
            logger.error(f'An attempt to create a string from a user variable failed. {exc}')
            return None


    @logger.catch
    def comparison_ipv4(self, current_ipv4_address:str, ipv4_to_check:str) -> Union[bool, None]:
        """
        This method is responsible for comparing the user input
        IPv4 address with the current external IPv4 address.

        Parameters:
            current_ipv4_address (str): current IPv4 address;
            ipv4_to_check (str): IPv4 address to compare against.

        Returns:
            bool: True if a match;
            None: if any error occurred.
        """
        try:
            if current_ipv4_address == ipv4_to_check:
                return True
            return False
        except TypeError as exc:
            logger.error(f'Failed to compare variables. {exc}')
            return None


    @logger.catch
    def run(self) -> Union[IPComparisonResult, None]:
        """
        The method that controls the class.
        Sequentially calling class methods to perform a comparison between
        the received and current external IPv4 addresses.

        Returns:
            class: IPComparisonResult:
                result: bool
                user_input: str
                current_ip: str
            None: if any error occurred.
        """
        current_ip = self.data_type_check(self.current_ip)
        user_input = self.data_type_check(self.user_input)
        if user_input is None or current_ip is None:
            logger.warning('Method (data_type_check) returned None')
            return None
        normalized_user_input = self.data_normalization(user_input)
        normalized_current_ip = self.data_normalization(current_ip)
        if normalized_user_input is None or normalized_current_ip is None:
            logger.warning('Method (data_normalization) returned None')
            return None
        user_input_result_type_checking = self.ipv4_type_check(normalized_user_input)
        current_ip_result_type_checking = self.ipv4_type_check(normalized_current_ip)

        # Сиправить воложенность!
        if user_input_result_type_checking and current_ip_result_type_checking is True:
            result_of_checking = self.comparison_ipv4(normalized_current_ip, normalized_user_input)
        else:
            return None

        if result_of_checking is None:
            logger.warning('Method (comparison_ipv4) returned None')
            return None

        return IPComparisonResult(
                result = result_of_checking,
                user_input = normalized_user_input,
                current_ip = normalized_current_ip
                )

if __name__ == '__main__':
    string_input_from_user = input('Enter the IPv4 to compare: ')
    ip = GetMyIP()
    CURRENT_EXTERNAL_IP = str(ip.get())
    comparison = IPAddressVerification(string_input_from_user, CURRENT_EXTERNAL_IP)
    result = comparison.run()
    if result is None:
        print('Something went wrong - no result.')
    else:
        if result[0] is True:
            CHOSEN_WORD = 'matches'
        elif result[0] is False:
            CHOSEN_WORD = 'does not matches'
        else:
            CHOSEN_WORD = '(ERROR! Something wrong)'
        print(f"""
        Your input '{string_input_from_user}' after normalizing '{result[1]}'
        and comparison with the current IPv4 address '{result[2]}'
        allows you to report that the address you entered is {CHOSEN_WORD}.
          """)
