import logging
import os
import re
import socket
import sys

from logging.handlers import RotatingFileHandler
from time import sleep


def main():
    logger = _build_logger()
    ip, port = _input_port_ip()

    while True:
        message = udp_server(ip, port, logger)
        logger.info(f"Covert Transfer Complete | Message is {''.join(message)}")

def udp_server(ip, port, logger):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    message = []

    while True:
        try:
            server.bind((ip, int(port)))
            break

        except WindowsError as e:
            if e.winerror == 10049:
                logger.warning(f"Thread 1: Server IP of {ip} is invalid when establishing socket. Check interface IP "
                               f"Address")
                sleep(1)
        ip, port = _input_port_ip()


    logger.info(f"Server: {ip} | Port: {port} | Status: Listening...")

    while True:
        data, address = server.recvfrom(int(port))
        if data.decode() == "END":
            return message

        covert_element = chr(int(address[0].split(".")[3]))
        logger.info(f"Found covert element: {covert_element}")
        message.append(covert_element)



def _input_port_ip():
    server_ip = input("Enter IP Address for the listening interface for this TCP Server: ")
    while not _validate_ip(server_ip):
        server_ip = input("Invalid IP Address. Please specify a valid IP i.e. 192.168.0.10: ")

    listening_port = input("Enter the Port this TCP Server will listen on: ")
    while not _validate_port(listening_port):
        listening_port = input("Invalid port number. Please specify a valid port between 1-65535: ")

    return server_ip, listening_port


def _build_logger():
    """ Build Logger for the program """
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler_info = RotatingFileHandler('../logs/TCPServer_info.log', maxBytes=1048576)
    file_handler_warning = RotatingFileHandler('../logs/TCPServer_warning.log', maxBytes=1048576)
    file_handler_error = RotatingFileHandler('../logs/TCPServer_error.log', maxBytes=1048576)
    stream_handler = logging.StreamHandler(stream=sys.stdout)

    file_handler_info.setLevel(logging.INFO)
    file_handler_warning.setLevel(logging.WARNING)
    file_handler_error.setLevel(logging.ERROR)
    stream_handler.setLevel(logging.DEBUG)

    handlers = [file_handler_info, file_handler_warning, file_handler_error, stream_handler]
    formatter = logging.Formatter('%(asctime)s || %(levelname)s || %(message)s || %(name)s')

    for handler in handlers:
        logger.addHandler(handler)
        handler.setFormatter(formatter)
    return logger


def _validate_port(port):
    regex = re.compile(r'(\d)+')
    if regex.fullmatch(port) and 1 <= int(port) <= 65535:
        return True
    return False


def _validate_ip(ip):
    regex = re.compile(r"""
                        \b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3} # Match first 3 ocetets
                        (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b          # Match final octet. No period at end
                        """, re.VERBOSE)
    if regex.search(ip):
        return True
    return False


if __name__ == '__main__':
    main()
