"""
This module searches for an external IP address.

Author: Mikhail Gurov
Last Modified: Feb 06, 2023
"""
#!/usr/bin/env python3.10
# -- coding: utf-8 --

import sys
from typing import Union
from ipaddress import IPv4Address, ip_address
import requests
from bs4 import BeautifulSoup
from loguru import logger

logger.add(
        'find_ip.log.txt',
        format='{time}, {level}, {module}:{line} -> {message}.',
        level='ERROR',
        rotation='10MB', compression='zip',
        serialize=False,
        )

class FailedToGetIP(Exception):
    """
    This exception is raised if an error occurs in obtaining an external IPv4 address.

    It occurs:
        Internet connection error on the part of the user;
        Error getting IPv4 in all modules.
    """

class GetMyIP():
    """
    Calling different sites on the Internet to get the device's
    external IPv4 address.

    Methods:
        __init__: class initialization;
        get: running the remaining methods of the class to get the result of its work.
            Control class method;
        get_external_ipv4_1: the first method is to get the user's external IPv4 address;
        get_external_ipv4_2: the following method is to get the user's external IPv4 address.
            Used as a fallback method in case the previous method fails;
        get_external_ipv4_3: the following method is to get the user's external IPv4 address.
            Used as a fallback method in case the previous method fails;
        make_control: Helper method to check if a variable contains an IPv4 address;
        make_requests: A method for receiving a response from a web page before parsing.

    Exceptions:
        In developing.

    External resources:
        The class uses 3 web sites, from where it gets the external IPv4 address of the user
            using the parsing method: "http://checkip.dyndns.org", "https://www.ipaddress.com",
            "https://www.iplocation.net".
    """

    def __init__(self):
        """
        """

    def get(self) -> Union[IPv4Address, None]:
        """
        Sequentially calling other class methods to get the external
        IP address. If one of the called methods returns None, the next
        method is requested until the current external
        IPv4 address is obtained.

        Returns:
            IPv4Address: external IPv4 address.
            None: if any error occurred.
        """
        for func in [self.get_external_ipv4_1, self.get_external_ipv4_2,
                     self.get_external_ipv4_3]:
            try:
                ipv4 = func()
            except FailedToGetIP as exc:
                logger.warning(f'Method {func.__name__} returned an error: {exc}')
                raise
            except Exception as exc:
                logger.error(f'An unknown error was found in the\
                             method {str(func.__name__)}: {exc}')
                raise
            if ipv4 is not None:
                return ipv4
            logger.warning('Failed one attempt to find an IPv4 address')
        raise FailedToGetIP('All attempts to get an IPv4 address failed:\
                            all methods returned None')


    def make_requests(self, url:str, headers:dict|None = None) -> Union[requests.Response, None]:
        """
        Receiving a response and checking the result.

        Parameters:
            url (str): a string containing a link to the site that will be
                subsequently processed by this method;
            headers (dict | None): additional information for the http request,
                in this case the "User-Agent" header.

        Returns:
            class 'requests.model.Response': HTTP response body and other supporting information;
            None: if any error occurred.
        """
        try:
            response = requests.get(url, headers=headers, timeout=5)
        except requests.exceptions.ConnectionError as exc:
            raise FailedToGetIP('Failed to get IP: connection error') from exc
        except requests.exceptions.MissingSchema as exc:
            logger.error(f'Failed to get IP: invalid URL. Value: ({url}). {exc}')
            return None # Positive scenario - website is off
        if response.status_code != 200:
            logger.info(f'Expected server response (200) was not received.\
                        Value: ({str(response.status_code)})')
            return None # Positive scenario - response is not 200
        if response is not None:
            return response
        return None


    def make_control(self, line_with_ip_address:str) -> Union[IPv4Address, None]:
        """
        Checking the contents of a variable to see if it contains an
        IPv4 address and creating another variable based on this
        variable with the IPv4Address data type.

        Parameters:
            ip (str): external IPv4 address of the user.

        Returns:
            class 'ipaddress.IPv4Address': the user's external IPv4 address
                in IPv4Address format after checking against this data type;
            None: if any error occurred.
        """
        try:
            ipv4 = ip_address(line_with_ip_address)
        except ValueError as exc:
            logger.error(f'The variable does not contain an IP address.\
                         Value: ({line_with_ip_address}). {exc}')
            return None
        try:
            if ipv4.version == 4:
                return ipv4 # Positive scenario
        except AttributeError as exc:
            logger.error(f'The variable does not contain an IPv4 address. Value: {ipv4}. {exc}')
            return None
        return None


    def get_external_ipv4_1(self) -> Union[IPv4Address, None]:
        """
        Request to site 1 to get the device's external IPv4 address.

        Returns:
            IPv4Address: external IPv4 address.
            None: if any error occurred.
        """
        url = 'http://checkip.dyndns.org'
        def do_parsing(response):
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
            except AttributeError as exc:
                logger.error(f'{exc}')
                return None
            find = soup.find('body')
            if find is None:
                logger.error('The parsing function returned None')
                return None
            find_string = find.text
            prefix = 'Current IP Address: '
            ipv4 = find_string.replace(prefix, "")
            return ipv4
        response = self.make_requests(url)
        if response is None:
            return None
        ipv4 = do_parsing(response)
        if ipv4 is None:
            return None
        ipv4 = self.make_control(ipv4)
        return ipv4


    def get_external_ipv4_2(self) -> Union[IPv4Address, None]:
        """
        Request to site 1 to get the device's external IPv4 address.

        Returns:
            IPv4Address: external IPv4 address.
            None: if any error occurred.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        url = 'https://www.ipaddress.com'
        def do_parsing(response):
            try:
                soup = BeautifulSoup(response, 'html.parser')
            except AttributeError as exc:
                logger.error(f'{exc}')
                return None
            find = soup.find('div', {'id' : 'ipv4'})
            if find is None:
                logger.error('The parsing function returned None')
                return None
            find_string = find.text
            prefix = 'My IPv4 Address'
            ipv4 = find_string.replace(prefix, "")
            return ipv4
        response = self.make_requests(url, headers)
        if response is not None:
            response = response.content
        else:
            return None
        ipv4 = do_parsing(response)
        if ipv4 is None:
            return None
        ipv4 = self.make_control(ipv4)
        if ipv4 is None:
            return None
        return ipv4


    def get_external_ipv4_3(self) -> Union[IPv4Address, None]:
        """
        Request to site 1 to get the device's external IPv4 address.

        Returns:
            IPv4Address: external IPv4 address.
            None: if any error occurred.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        url = 'https://www.iplocation.net'
        def do_parsing(response):
            try:
                soup = BeautifulSoup(response, 'html.parser')
            except AttributeError as exc:
                logger.error(f'{exc}')
                return None
            find = soup.find('span', class_ = 'home-ip')
            if find is None:
                logger.error('The parsing function returned None')
                return None
            ipv4 = find.text
            return ipv4
        response = self.make_requests(url, headers)
        if response is not None:
            response = response.content
        else:
            return None
        ipv4 = do_parsing(response)
        if ipv4 is None:
            return None
        ipv4 = self.make_control(ipv4)
        if ipv4 is None:
            return None
        return ipv4


if __name__ == '__main__':
    @logger.catch
    def start_module():
        """
        The function of launching the program and preparing 
        a report for the user.
        """
        ip_search = GetMyIP()
        try:
            ipv4 = ip_search.get()
        except FailedToGetIP as exc:
            logger.error(f'{exc}')
            sys.exit()
        if ipv4 is None:
            print('The program could not find your external IPv4 address.')
        print(f'Your external IPv4 address is {ipv4}.')

    start_module()
