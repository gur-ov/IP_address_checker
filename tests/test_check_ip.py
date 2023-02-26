# -*- coding: utf-8 -*-
"""This module is used to test the IPAddressVerification module.

Example
-------
The launch is carried out from the command line. If you want to get only the
results of all tests without details:

      $ Python test_check_ip

If you want details, you need to start it like this:

      $ Python test_check_ip -d

If you want a short answer about whether all tests passed, you can do this:

      $ Python test_check_ip -q

To write the result of passing all tests to a file, you can do this:

      $ Python test_check_ip -s

To run one test, you can do this:

      $ Python test_check_ip -a test_name

"""

import sys
import argparse
import os
from dataclasses import dataclass
from typing import Optional, NamedTuple
import datetime
import pytz

current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, '..', 'ip_checker')
sys.path.append(module_dir)

from check_ip import IPAddressVerification
from find_ip import GetMyIP

@dataclass
class TestReturn():
    """This class is a template for return methods.

    This class is used by the test methods of the TestsIPAddressVerification
    class for their further processing in other methods, as well as for the
    correct use of type hinting.

    Example
    -------
    You can style the return method like this:

        return TestReturn(
                test_result = True, # True is a successful.
                details = 'Any details about the test and its results',
                test_doc = class_name.test_name.__doc__)

    """
    test_name: str
    test_result: bool
    details: Optional[str]
    test_doc: Optional[str]

class TimeReturn(NamedTuple):
    """ This class is a template for return method "self.current_time".

     This class, as well as the self.current_time method, are not supposed to
     be changed in while using this module.

    """
    time_str_for_title: str
    time_str_for_simple_test: str

class TestsIPAddressVerification():
    """Collect and manage unit tests for IPAddressVerification.

    This class is a set of unit tests for verifying the operation of the
    IPAddressVerification class, as well as methods for controlling the launch
    of these tests.

    The class implements various return test results. Details of usage are
    written in the doctrine of this module.

    methods
    -------
    __init__
        The class initialization method. Not used.
    current_time
        Getting the current time and creating strings for later use.
    get_argv
        Receiving and processing command line arguments.
    run
        Test start control method.
    running_only_one_test
        Running and holding one text.
    running_tests
        Run and run all unit tests of the class.
    test_1, test_2, ... test_n
        Individual unit tests.

    """
    def __init__(self):
        self.time_variable = self.current_time()
        self.argv = self.get_argv()

        self.tests = ( # Don't forget to add a new test here!
               self.test_1,
               self.test_2,
               self.test_3,
               self.test_4,
               self.test_5,
               self.test_6,
                )

    def run(self) -> None:
        """ The method that controls the launch of testing.

         If necessary, change the "my_locale" variable.
        """
        if self.argv.alone:
            self.running_only_one_test()
        else:
            self.running_tests()

    def current_time(self) -> TimeReturn:
        my_locale = "Europe/Bratislava" # Add you city!
        timezone = pytz.timezone(my_locale)
        now = datetime.datetime.now()
        now_with_timezone = timezone.localize(now)
        datetime_for_title = now_with_timezone.strftime("%B %d, %Y at %H:%M")
        datetime_for_test = now_with_timezone.strftime("%Y.%m.%d, %H:%M")
        return TimeReturn(
                time_str_for_title = datetime_for_title,
                time_str_for_simple_test = datetime_for_test,
                )

    def get_argv(self) -> argparse.Namespace:
        """Description and processing of command line arguments.

        If testing is carried out with the -d or --details option, then
        details are displayed, and not just the result of passing the test.

        Possible command line arguments to use are described in the "help"
        options.

         returns
         _______
         argparse.namespace
             This is the class that contains the argument flags as well as the
             "message" variable string.

        """
        parser = argparse.ArgumentParser(\
                description="Getting a command line argument.")
        parser.add_argument("-d", "--details", action="store_true",\
                            help="Displaying detailed info on the tests\
                            performed.")
        parser.add_argument("-s", "--setnote", action="store_true",\
                            help="Write a detailed test report to a file.")
        parser.add_argument("-q", "--quickly", action="store_true",\
                            help="Get a quick report on all tests at once.")
        parser.add_argument("-a", "--alone", action="store_true",\
                            help="Run a single test. Be sure to use the name\
                            of the test as the next argument..")
        parser.add_argument("message", nargs="?", type=str, default="",\
                            help="An argument that takes the name of the test\
                            to be run.")
        args = parser.parse_args()
        return args

    def running_tests(self) -> None:
        """Run all tests.

        The result of the method operation depends on the command line
        parameters.

        There is no return statement in the method. Data output is produced
        either to the console or written to a file.

        """
        # Violation of the DRY principle!
        results: list = []
        for one_test in self.tests:
            result_one_test = one_test()
            results.append(
                    {
                        'name'    : result_one_test.test_name,
                        'result'  : result_one_test.test_result,
                        'details' : result_one_test.details,
                        'doc'     : result_one_test.test_doc
                        }
                    )
        if self.argv.details: # For verbose console output
            print(
                    f'\nOn {self.time_variable.time_str_for_title},\
 unit tests were launched to\n'
                    f'test the functionality of module "check_ip.py".\n'
                    f'_________________________________________________')
            for result_one_test in results:
                if result_one_test['result'] is True:
                    print(
                    f'\n\nThe test "{result_one_test["name"]}" was passed\
 SUCCESSFULLY.\n\n'
                    f'Test details:\n{result_one_test["details"]}\n\n'
                    f'Test documentation: {result_one_test["doc"]}'
                    f'_________________________________________________')
                else:
                    print(
                            f'\n\nThe test {result_one_test["name"]} was\
 passed FAIL.\n\n'
                            f'Test details:\n{result_one_test["details"]}\n\n'
                            f'Test documentation: {result_one_test["doc"]}'
                            f'_________________________________________________')
            print('\n                        Testing completed.\n')
        elif self.argv.setnote  or\
                (self.argv.details and self.argv.setnote):
            with open("unittest_check_ip.log", "a", encoding='utf8') as file:
                file.write(
                        f'\nOn {self.time_variable.time_str_for_title},\
unit tests were launched to\n'
                        f'test the functionality of module "check_ip.py".\n'
                        f'_________________________________________________')
                for result_one_test in results:
                    if result_one_test['result'] is True:
                        file.write(
                        f'\n\nThe test "{result_one_test["name"]}" was\
passed SUCCESSFULLY.\n\n'
                        f'Test details:\n{result_one_test["details"]}\n\n'
                        f'Test documentation: {result_one_test["doc"]}'
                        f'_________________________________________________')
                    else:
                        file.write(
                                f'\n\nThe test {result_one_test["name"]}\
was passed FAIL.\n\n'
                                f'Test details:\n{result_one_test["details"]}\n\n'
                                f'Test documentation: {result_one_test["doc"]}'
                                f'_______________________________________\
__________')
                file.write("\n                        Testing completed.\n")
            print('Testing completed. Results written to file\
 "unittest_check_ip.log".')
        elif self.argv.quickly: # To the console OK if all tests pass
            all_test_results = tuple(result_one_test['result'] for\
                    result_one_test in results)
            if all(i == all_test_results[0] for i in all_test_results):
                print('All tests passed SUCCESSFULLY.')
            else:
                print('At least one test returned FAIL.')
        else: # Outputting the result of each test to console without details
            all_test_results = tuple(result_one_test['result'] for\
                    result_one_test in results)
            print(all_test_results)

    def running_only_one_test(self) -> None:
        """Run an individual test.
        """
        message = self.argv.message
        if not message:
            print('ERROR: Please enter test name.')
            return None
        test_names = tuple(i.__name__ for i in self.tests)
        if not message in test_names:
            print('ERROR: The test name entered does not exist.')
            return None
        test_name_to_num_map= {}
        for one_test, test_serial_number in zip(test_names, range(len(test_names))):
            test_name_to_num_map[one_test] = test_serial_number
        result_one_test = self.tests[test_name_to_num_map[message]]()
        result_dict = {
                'name'    : result_one_test.test_name,
                'result'  : result_one_test.test_result,
                'details' : result_one_test.details,
                'doc'     : result_one_test.test_doc
                }
        print(
                f'\nOn {self.time_variable.time_str_for_title},\
 unit tests were launched to\n'
                f'test the functionality of module "check_ip.py".\n'
                f'_________________________________________________')
        if result_dict['result'] is True:
            print(
            f'\n\nThe test "{result_dict["name"]}" was passed\
 SUCCESSFULLY.\n\n'
            f'Test details:\n{result_dict["details"]}\n\n'
            f'Test documentation: {result_dict["doc"]}'
            f'_________________________________________________')
        else:
            print(
                    f'\n\nThe test {result_dict["name"]} was\
 passed FAIL.\n\n'
                    f'Test details:\n{result_dict["details"]}\n\n'
                    f'Test documentation: {result_dict["doc"]}'
                    f'_________________________________________________')

    def test_1(self) -> TestReturn:
        """Test for input '8.8.8.8'.
        """
        test_method_name = 'test_1'
        test_method = getattr(TestsIPAddressVerification, test_method_name)
        discription = test_method.__doc__
        current_ip = str(GetMyIP().get())
        obj = IPAddressVerification()
        obj.user_ip = '8.8.8.8' # Must be FALSE (Are you in California? :)
        obj.current_ip = current_ip
        result = obj.run()
        test_details = (
                f'\tTest was started in\
 {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is {result[1]} and current external\n'
                f'\tIPv4-address is {result[2]}. Comparing these data,\n'
                f'\tthe program returned {result[0]}.'
                )
        if result[0]:
            test_result = False
        test_result = True
        return TestReturn(
                test_name = test_method_name,
                test_result = test_result,
                details =  test_details,
                test_doc = discription)

    def test_2(self) -> TestReturn:
        """Test for input '   8,8.8.8,   '.
        """
        test_method_name = 'test_2'
        test_method = getattr(TestsIPAddressVerification, test_method_name)
        discription = test_method.__doc__
        current_ip = str(GetMyIP().get())
        obj = IPAddressVerification()
        ipv4_address_for_verification = '   8,8.8.8,   '
        obj.user_ip = ipv4_address_for_verification
        obj.current_ip = current_ip
        result = obj.run()
        test_details = (
                f'\tTest was started in\
 {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True:
            test_result = False
        elif result[0] is False and str(ipv4_address_for_verification)\
                != str(result[1]):
            test_result = True
        else:
            test_result = False
        return TestReturn(
                test_name = test_method_name,
                test_result = test_result,
                details =  test_details,
                test_doc = discription)

    def test_3(self) -> TestReturn:
        """Test for input '8.8.777.8'.
        """
        test_method_name = 'test_3'
        test_method = getattr(TestsIPAddressVerification, test_method_name)
        discription = test_method.__doc__
        current_ip = str(GetMyIP().get())
        obj = IPAddressVerification()
        ipv4_address_for_verification = '8.8.777.8'
        obj.user_ip = ipv4_address_for_verification
        obj.current_ip = current_ip
        result = obj.run()
        test_details = (
                f'\tTest was started in\
 {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True:
            test_result = False
        elif result[0] is False and str(ipv4_address_for_verification)\
                != str(result[1]):
            test_result = True
        else:
            test_result = False
        return TestReturn(
                test_name = test_method_name,
                test_result = test_result,
                details =  test_details,
                test_doc = discription)

    def test_4(self) -> TestReturn:
        """Test for input '8.8.-777.8'.
        """
        test_method_name = 'test_4'
        test_method = getattr(TestsIPAddressVerification, test_method_name)
        discription = test_method.__doc__
        current_ip = str(GetMyIP().get())
        obj = IPAddressVerification()
        ipv4_address_for_verification = '8.8.-777.8'
        obj.user_ip = ipv4_address_for_verification
        obj.current_ip = current_ip
        result = obj.run()
        test_details = (
                f'\tTest was started in\
 {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True:
            test_result = False
        elif result[0] is False and str(ipv4_address_for_verification)\
                != str(result[1]):
            test_result = True
        else:
            test_result = False
        return TestReturn(
                test_name = test_method_name,
                test_result = test_result,
                details =  test_details,
                test_doc = discription)

    def test_5(self) -> TestReturn:
        """Test for input 8,8,8,8.
        """
        test_method_name = 'test_5'
        test_method = getattr(TestsIPAddressVerification, test_method_name)
        discription = test_method.__doc__
        current_ip = str(GetMyIP().get())
        obj = IPAddressVerification()
        ipv4_address_for_verification = 8,8,8,8
        obj.user_ip = ipv4_address_for_verification
        obj.current_ip = current_ip
        result = obj.run()
        test_details = (
                f'\tTest was started in\
 {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True:
            test_result = False
        elif result[0] is False and str(ipv4_address_for_verification)\
                != str(result[1]):
            test_result = True
        else:
            test_result = False
        return TestReturn(
                test_name = test_method_name,
                test_result = test_result,
                details =  test_details,
                test_doc = discription)

    def test_6(self) -> TestReturn:
        """Test for input (8,8,8,8).

        The test sends for verification an IP address written without errors
        in the format of the drain. The result of the comparison must be False.

        """
        test_method_name = 'test_6'
        test_method = getattr(TestsIPAddressVerification, test_method_name)
        discription = test_method.__doc__
        current_ip = str(GetMyIP().get())
        obj = IPAddressVerification()
        ipv4_address_for_verification = (8,8,8,8)
        obj.user_ip = ipv4_address_for_verification
        obj.current_ip = current_ip
        result = obj.run()
        test_details = (
                f'\tTest was started in\
 {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True:
            test_result = False
        elif result[0] is False and str(ipv4_address_for_verification)\
                != str(result[1]):
            test_result = True
        else:
            test_result = False
        return TestReturn(
                test_name = test_method_name,
                test_result = test_result,
                details =  test_details,
                test_doc = discription)


if __name__ == '__main__':
    test = TestsIPAddressVerification()
    test.run()
