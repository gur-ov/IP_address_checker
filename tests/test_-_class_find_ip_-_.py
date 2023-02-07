import sys
import argparse

sys.path.append('/home/gurov/code/chatGPT/ip_checker/ip_checker/')
from find_ip import GetMyIP

class Tests_GetMyIP():
    def __init__(self):
        pass

    def getArgv(self):
        """
        If argument details is enabled - will return 1.
        """
        parser = argparse.ArgumentParser(description="Getting a command line argument.")
        parser.add_argument("-d", "--details", action="store_true",\
                            help="Displaying detailed information on the tests performed.")
        args = parser.parse_args()
        if args.details:
            return 1
        else:
            return None

    def runningTests(self):
        """
        All tests should be run here in turn. 
        Don't forget to add new tests here!
        """
        results: list = []
        tests: tuple = (
                # Make a new test challenge!
                self.test_GetMyIP_positiveScenario(),
                )
        quantity_tests = range(len(tests))
        for i in tests:
            results.append(i)
        args = self.getArgv()
        if args == 1: 
            for i,q in zip(results,quantity_tests):
                print(f'Test №{q} have results: {i[1]}, and test description: {i[2]}\n')
        elif args == None:
            for i in results:
                if i[0] == True:
                    print(f'OK')
                elif i[0] == False:
                    print(f'WRONG!')
                else:
                    exit()
        else:
            exit()
        
    def test_GetMyIP_positiveScenario(self):
        """
        This is a test for a positive scenario of working 
        function "manager" from class GetMyIP from module find_ip.
        """
        obj = GetMyIP()
        ipv4 = obj.get()
        discription = self.test_GetMyIP_positiveScenario.__doc__
        discription_string = discription.replace('\n', '').strip().replace('         ', '')
        if ipv4 is None:
            result = (True, f'OK. IPv4 is {ipv4}', discription_string)
            return result
        elif ipv4.version == 4:
            result = (True, f'OK. IPv4 is {ipv4}, type is {type(ipv4)}', discription_string)
            return result
        else: 
            result = (False, f'WRONG! {ipv4}, type is {type(ipv4)}', discription_string)
            return result



# Check
test = Tests_GetMyIP()
test.runningTests()

