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
from typing import Optional, Callable

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
    test_result: bool
    details: Optional[str]
    test_doc: Optional[str]

class TestsIPAddressVerification():
    """ Collection and management of unit tests for IPAddressVerification.

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
        pass

    def get_argv(self) -> Optional[int]:
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
        args = parser.parse_args()
        if args.details: # Type hinting wrong?
            return 1
        return None

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
        tests = ( # Don't forget to add a new test here.
               self.test_1(), # Index[0] in results.
                )
        for i in tests:
            results.append([i.test_result, i.details, i.test_doc])
        args = self.get_argv()
        if args == 1:
            for i in tests:
                if i.test_result:
                    print(
                            f'The test was passed SUCCESSFULLY.\n\n'
                            f'Test details:\n{i.details}\n\n'
                            f'Test documentation:{i.test_doc}'
                            )
                else:
                    print(
                            f'The test was passed FAIL.\n\n'
                            f'Test details:\n{i.details}\n\n'
                            f'Test documentation:{i.test_doc}'
                            )
        else:
            for i in tests:
                if i.test_result: # If True
                    print("OK")
                else:
                    print("FAIL")

    def running_only_one_test(self,test_name: Callable[[], TestReturn]) -> None:
        """ Run an individual test.

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
                        f'The test was passed SUCCESSFULLY.\n\n'
                        f'Test details:\n{i.details}\n\n'
                        f'Test documentation:{i.test_doc}'
                        )
            else:
                print(
                        f'The test was passed FAIL.\n\n'
                        f'Test details:\n{i.details}\n\n'
                        f'Test documentation:{i.test_doc}'
                        )
        else:
            if i.test_result: # If True
                print("OK")
            else:
                print("FAIL")

    def test_1(self) -> TestReturn:
        """ Test for input '1.1.1.1'

        The test sends for verification an IP address written without errors in
        the format of the drain. The result of the comparison must be False.

        """
        discription = TestsIPAddressVerification.test_1.__doc__

        current_ip = str(GetMyIP().get())
        obj = IPAddressVerification()
        obj.user_ip = '8.8.8.8' # Must be FALSE (Are you in California? :)
        obj.current_ip = current_ip
        result = obj.run()
        test_details = (
                f'\t    User input is {result[1]} and current external\n'
                f'\tIPv4-address is {result[2]}. Comparing these data,\n'
                f'\tthe program returned {result[0]}.'
                )
        if result[0]:
            test_result = False
        test_result = True
        return TestReturn(
                test_result = test_result,
                details =  test_details,
                test_doc = discription) # Type hinting wrong?


if __name__ == '__main__':
    test = TestsIPAddressVerification()

    # START ALL TESTS
    test.running_tests()

    # START ONLY ONE TEST
    # test.running_only_one_test(test.test_1)
