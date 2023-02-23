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
        if self.argv.details:
            self.argv = 'details'
        elif self.argv.setnote:
            self.argv = 'set_note'
        elif self.argv.details and self.argv.setnote:
            self.argv = 'set_note'
        else:
            pass # Нужно обработать этот сценарий

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
        args = parser.parse_args()
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
        results: list = []
        tests = ( # Don't forget to add a new test here!
               self.test_1(), # Index[0] is results.
               self.test_2(),
               self.test_3(),
               self.test_4(),
               self.test_5(),
               self.test_6(),
                )
        for i in tests:
            results.append([i.test_result, i.details, i.test_doc])
        # variable "i" is possibly unbound if use this messages incorrectly
        head_message = (f'\nOn {self.time_variable.time_str_for_title},\
 unit tests were launched to\n'
                        f'test the functionality of module "check_ip.py".\n'
                        f'_________________________________________________'),
        success_message = (f'\nThe test "{i.test_name}" was passed SUCCESSFULLY.\n\n'
                           f'Test details:\n{i.details}\n\n'
                           f'Test documentation: {i.test_doc}'
                           f'_________________________________________________'),
        fail_message = (f'The test {i.test_name} was passed FAIL.\n\n'
                        f'Test details:\n{i.details}\n\n'
                        f'Test documentation: {i.test_doc}'
                        f'_________________________________________________'),
        reports = {
                "head": head_message,
                "success": success_message,
                "fail": fail_message,
                "ok": "OK",
                "no": "FAIL",
                }

        if self.argv == 'details':
            print(reports['head'][0])
            for i in tests:
                if i.test_result:
                    print(reports['success'][0])
                else:
                    print(reports['fail'][0])
        elif self.argv == 'set_note':
            pass # send report to file
        else:
            for i in tests:
                if i.test_result:
                    print(reports['ok'])
                else:
                    print(reports['no'])

    def running_only_one_test(self,test_name: Callable[[], TestReturn]) -> None:
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
        args = self.get_argv()
        i = test_name() # i is a short synonym-variable
        if args == 1:
            if i.test_result:
                print(
                        f'The test {i.test_name} was passed SUCCESSFULLY.\n\n'
                        f'Test details:\n{i.details}\n\n'
                        f'Test documentation: {i.test_doc}'
                        )
            else:
                print(
                        f'The test {i.test_name} was passed FAIL.\n\n'
                        f'Test details:\n{i.details}\n\n'
                        f'Test documentation: {i.test_doc}'
                        )
        else:
            if i.test_result: # If True
                print("OK")
            else:
                print("FAIL")

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
                f'\tTest was started in {self.time_variable.time_str_for_simple_test}.\n'
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
                f'\tTest was started in {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True: # Если есть соотвествие адресов
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
                f'\tTest was started in {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True: # Если есть соотвествие адресов
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
                f'\tTest was started in {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True: # Если есть соотвествие адресов
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
                f'\tTest was started in {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True: # Если есть соотвествие адресов
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
                f'\tTest was started in {self.time_variable.time_str_for_simple_test}.\n'
                f'\tUser input is "{ipv4_address_for_verification}"\
 (after normalize "{result[1]}")\n'
                f'\tand current external IPv4-address is {result[2]}.\n'
                f'\tComparing these data, the program returned {result[0]}.\n'
                )
        if result[0] is True: # Если есть соотвествие адресов
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

if __name__ == '__main__':
    test = TestsIPAddressVerification()

    # START ALL TESTS
    test.running_tests()

    # START ONLY ONE TEST
    # test.running_only_one_test(test.test_1)
