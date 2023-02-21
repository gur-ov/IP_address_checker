import sys
from loguru import logger
from ipaddress import ip_address
from typing import Callable, Union, Tuple, NamedTuple, TypeVar
from find_ip import GetMyIP

#Synonyms of data types for type hinting
IPV4 = str
OCTET = int
IPV4_ADDRESS_STR = str
IPV4_ADDRESS_TUPLE_WITH_STR = Tuple[IPV4_ADDRESS_STR]
IPV4_ADDRESS_TUPLE_WITH_INT = Tuple[OCTET, OCTET, OCTET, OCTET]
# Переменная для указания на self класса IPAddressVerification для type hinting
IPAddressVerificationType = TypeVar(\
        'IPAddressVerificationType', bound='IPAddressVerification')

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

def validate_input(func:\
        Callable[[IPAddressVerificationType, IPV4_ADDRESS_STR], None])\
        -> Callable[[IPAddressVerificationType, IPV4_ADDRESS_STR], None]:
    """
    Decorator for setters: set_current_ip, set_user_input_ip.
    Performs the function of validation and possible normalization of incoming data.

    Parameters (only one of the options below is allowed):
        "255.255.255.255" - str without errors as ipv4 address;
        " 1,1,1.1. " - str with typos in the form of an ipv4 address with
            commas instead of dots, a dot or comma at the end and extra spaces
            from the beginning and end;
        1,1,1,1 - four digits separated by commas;
        ipv4="1.1.1.1" - dict with str as value as IPv4 address without errors;
        ipv4=" 1,1.1,1. " - dict with str as value as an IPv4 address with
            typos as commas instead of dots, dot or comma at the end and extra
            spaces at the beginning and end.

    Returns:
         str: Validated data containing a valid IPv4 address.
    """
    def wrapper(self, *args, **kwargs) -> None:

        if bool(kwargs):
            if len(kwargs) == 1:
                for value in kwargs.values():
                    ipv4_not_verified = value
            else:
                return None
        else:
            if len(args) == 1:
                ipv4_not_verified = args[0]
            elif len(args) == 4:
                ipv4_not_verified_list = list(args)
                ipv4_not_verified = \
                        '.'.join(str(i) for i in ipv4_not_verified_list)
            else:
                return None
        try:
            # ipv4_not_verified is posibly unbound! Why?
            ipv4_not_verified_striped =  ipv4_not_verified.strip()
            ipv4_not_verified_normalized = ipv4_not_verified_striped.replace(',', '.')
            if ipv4_not_verified_normalized[-1] == '.':
                ipv4_not_verified = ipv4_not_verified_normalized[:-1]
            else:
                ipv4_not_verified = ipv4_not_verified_normalized
        except AttributeError as exc:
            logger.error(f'ipv4_not_verified variable is not a string: {exc}')
            return None
        except NameError as exc:
            logger.error(f'ipv4_not_verified variable is not exist: {exc}')
            return None
        try:
            ipv4 = ip_address(ipv4_not_verified)
        except ValueError as exc:
            logger.warning(f'Variable does not contain an IP address.\
                    Value: {ipv4_not_verified}. {exc}')
            return None
        try:
            ipv4.version
        except AttributeError as exc:
            return None
        return func(self, str(ipv4)) # OK
    return wrapper


class IPAddressVerification():
    """
    Comparison of external external IPv4 addresses with another presented
    to compare with an IPv4 address.

    Methods:
        __init__: class initialization;
        get_current_ip: get the current external IPv4 address;
        set_current_ip: pass the current external IPv4 address to the class;
        get_user_input_ip: get the IPv4 address entered by the user;
        set_user_input_ip: pass the address from the user to the IPv4 class;
        comparison_ipv4: compare IPv4 addresses;
        run: Run a process method.

    Properties:
        user_ip = for get_user_input_ip and set_user_input_ip
        current_ip = for get_current_ip and set_current_ip

    Class level variables:
        self._hidden_user_input_ip = string from the user suspected IPv4 address;
        self._hidden_current_ip = the device's current external IPv4 address.

    Exceptions:
        In developing.

    External resources:
        GetMyIP module - external external IPv4 addresses of the device.
    """
    def __init__(self):
        """
        """
        self._hidden_user_input_ip = ''
        self._hidden_current_ip = ''

    def get_current_ip(self) -> IPV4_ADDRESS_STR:
        """
        Getter method for safe access to variable _hidden_current_ip.
        """
        return self._hidden_current_ip

    @validate_input
    def set_current_ip(self, *args: IPV4_ADDRESS_STR):
        """
        Setter method for safely changing variable _hidden_current_ip.
        """
        self._hidden_current_ip = args[0]

    def get_user_input_ip(self) -> IPV4_ADDRESS_STR:
        """
        Getter method for safe access to variable _hidden_user_input_ip.
        """
        return self._hidden_user_input_ip

    @validate_input
    def set_user_input_ip(self, *args: IPV4_ADDRESS_STR):
        """
        Setter method for safely changing variable _hidden_user_input_ip.
        """
        self._hidden_user_input_ip = args[0]

    user_ip = property(get_user_input_ip, set_user_input_ip)
    current_ip = property(get_current_ip, set_current_ip)

    @logger.catch
    def comparison_ipv4(self, ipv4_to_check:str,current_ipv4_address:str)\
            -> Union[bool, None]:
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
        result_of_checking = self.comparison_ipv4(\
                self._hidden_user_input_ip, self._hidden_current_ip)

        if result_of_checking is None:
            logger.warning('Method (comparison_ipv4) returned None')
            return None

        return IPComparisonResult(
                result = result_of_checking,
                user_input = self._hidden_user_input_ip,
                current_ip = self._hidden_current_ip
                )


if __name__ == '__main__':
    if len(sys.argv) == 2:
        #Here, input is expected in the format python "name_module.py 1.1.1.1".
        USER_INPUT = sys.argv[1]
    else:
        USER_INPUT = input('Enter the IPv4 to compare: ')
    ip = GetMyIP()
    CURRENT_EXTERNAL_IP = str(ip.get())
    obj = IPAddressVerification()
    obj.current_ip = CURRENT_EXTERNAL_IP
    obj.user_ip = USER_INPUT
    result = obj.run()
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
        Your input '{USER_INPUT}' after normalizing '{result[1]}'
        and comparison with the current IPv4 address '{result[2]}'
        allows you to report that the address you entered is {CHOSEN_WORD}.
          """)
