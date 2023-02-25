# -*- coding: utf-8 -*-
"""This module is used to test the IPAddressVerification module.

Example
-------
To run the module, you need to configure. You need to specify at the bottom
which type of launch is preferable - launching all tests or a single launch of
the selected test. By default, all tests are configured to run.

To select to run all tests, you should write:

    if __name__ == '__main__':
        test = TestsIPAddressVerification()
        # START ALL TESTS
        test.running_tests()

To run one test, you need to pass the name of the selected test method to the
running_only_one_test method (in this example, test_1 is passed):

    if __name__ == '__main__':
        test = TestsIPAddressVerification()
        # START ONLY ONE TEST
        test.running_only_one_test(test.test_1)

After configuration, launch is carried out from the command line. If you want
to get only the test result without details:

    $ python test_check_ip

If you need details, you need to start it like this:

    $ python test_check_ip -d

"""

import sys
import argparse
import os
from dataclasses import dataclass
from typing import Optional, Callable, NamedTuple
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
    """
    """
    time_str_for_title: str
    time_str_for_simple_test: str

class TestsIPAddressVerification():
    """Collection and management of unit tests for IPAddressVerification.

    This class is a collection of unit tests to test the operation of the
    IPAddressVerification class.

    Unit tests can be run at the request of the tester as a group, using the
    running_tests control method, or individually, by calling them using the
    running_only_one_test method, passing the name of the method responsible for
    a particular test as an argument.

    Test results can be presented both in a simple "OK/FAIL" form and in
    expanded form, for which you need to pass the "-d" or "--details" command
    line argument when starting the test.

    methods
    -------
    __init__
        The class initialization method. Not used.
    get_argv
        Receiving and processing command line arguments.
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

    def run(self):
        """
        """
        if self.argv.alone:
            self.running_only_one_test()
        else:
            self.running_tests()

    def current_time(self) -> TimeReturn:
        my_locale = "Europe/Bratislava" # Enter you city!
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

        If testing is carried out with the -d or --details option, then details
        are displayed, and not just the result of passing the test.

        returns
        _______
        int
            1 if the use of the -d or --details command line argument was detected.

        """
        parser = argparse.ArgumentParser(\
                description="Getting a command line argument.")
        parser.add_argument("-d", "--details", action="store_true",\
                            help="Displaying detailed info on the tests performed.")
        parser.add_argument("-s", "--setnote", action="store_true",\
                            help="Write a detailed test report to a file.")
        parser.add_argument("-q", "--quickly", action="store_true",\
                            help="XXX.") # XXX
        parser.add_argument("-a", "--alone", action="store_true",\
                            help="XXX.") # XXX
        parser.add_argument("message", nargs="?", type=str, default="",\
                            help="XXX.") # XXX
        args = parser.parse_args()
        print(f'Print in module get_argv {args}')
        print(f'Print in module get_argv (type) {type(args)}')
        return args

    def running_tests(self) -> None:
        """All tests should be run here in turn.

        Run all tests. The result of the method operation depends on the command
        line parameters. If there are no parameters, a short information about
        the results of the tests will be displayed in the console. If the -d or
        --details parameter is present, detailed information about the results
        of the tests will be displayed in the console.

        There is no return statement in the method. The method prints the test
        results to the console.

        Note
        ____
        Don't forget to add new tests here!

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
        if self.argv == 'details': # For verbose console output
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
            print("\n                        Testing completed.\n")

        elif self.argv == 'set_note' or\
                (self.argv == 'details' and self.argv == 'set_note'):
            try:
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
                print("Testing completed. Results written to file XXX")
            except: # Handle possible errors!
                print("WOW!")
        elif self.argv == 'quickly': # To the console OK if all tests pass
            all_test_results = tuple(result_one_test['result'] for\
                    result_one_test in results)
            if all(i == all_test_results[0] for i in all_test_results):
                print('All tests passed SUCCESSFULLY.')
            else:
                print("At least one test returned FAIL.")
        else: # Outputting the result of each test to the console without details
            all_test_results = tuple(result_one_test['result'] for\
                    result_one_test in results)
            print(all_test_results)

    def running_only_one_test(self) -> None:
        """Run an individual test.

        The result of the method operation depends on the command line
        parameters. If there are no parameters, a short information about the
        results of the tests will be displayed in the console. If the -d or
        --details parameter is present, detailed information about the results
        of the tests will be displayed in the console.

        There is no return statement in the method. The method prints the test
        results to the console.

        Parameters
        __________
        test_name : Callable
            The name of the function that contains the unit test from the
            TestsIPAddressVerification class.

        """
        message = self.argv.message
        if not message:
            print("ERROR: Please enter test name.")
            return None
        test_names = tuple(i.__name__ for i in self.tests)
        if not message in test_names:
            print("ERROR: The test name entered does not exist.")
            return None
        test_name_to_num_map= {}
        # Give meaningful names to variables!
        for i, q in zip(test_names, range(len(test_names))): # No extra numbers in q?
            test_name_to_num_map[i] = q
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
        """Test for input '8.8.8.8'

        The test sends for verification an IP address written without errors in
        the format of the drain. The result of the comparison must be False.

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
                test_doc = discription) # Type hinting wrong?

    def test_2(self) -> TestReturn:
        """Test for input '   8,8.8.8,   '

        The test sends for verification an IP address written without errors in
        the format of the drain. The result of the comparison must be False.

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
                test_doc = discription) # Type hinting wrong?

    def test_3(self) -> TestReturn:
        """Test for input '8.8.777.8'

        The test sends for verification an IP address written without errors in
        the format of the drain. The result of the comparison must be False.

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
                test_doc = discription) # Type hinting wrong?

    def test_4(self) -> TestReturn:
        """Test for input '8.8.-777.8'

        The test sends for verification an IP address written without errors in
        the format of the drain. The result of the comparison must be False.

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
                test_doc = discription) # Type hinting wrong?

    def test_5(self) -> TestReturn:
        """Test for input 8,8,8,8

        The test sends for verification an IP address written without errors in
        the format of the drain. The result of the comparison must be False.

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
        """Test for input (8,8,8,8)

        The test sends for verification an IP address written without errors in
        the format of the drain. The result of the comparison must be False.

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
