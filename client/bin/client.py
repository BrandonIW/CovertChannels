import argparse
import logging
import os
import random
import re
import socket
import struct
import sys

from collections import deque
from logging.handlers import RotatingFileHandler
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send
from scapy.packet import Raw
from time import sleep


def main():
    logger = _build_logger()
    args = _build_parser()
    ip, port = _input_port_ip()

    packets = build_packets(args.message, logger, ip, port)
    send_packets(packets, ip, port, logger)


def send_packets(stack, ip, port, logger):
    logger.info(f"Connected to Server: {ip} Port: {port}")

    while stack:
        packet = stack.popleft()
        send(packet)
        sleep(3)
    send(IP(dst=ip) \
         / UDP(sport=random.randrange(1024, 65535), dport=int(port)) \
         / Raw(b"END"))


def build_packets(msg, logger, ip, port):
    stack = deque()

    logger.info(f"Message: {msg} | Creating Packets to send message...")

    for ele in msg:
        random_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))).split(".")
        covert_data = str(ord(ele))
        random_ip[3] = covert_data
        ip_and_covert = ".".join(random_ip)

        logger.info(f"Covert Element: {ele} | Forged IP Address: {ip_and_covert}")

        packet = IP(dst=ip, src=ip_and_covert) \
                 / UDP(sport=random.randrange(1024, 65535), dport=int(port)) \
                 / Raw(b"Assignment 5")
        stack.append(packet)

    return stack


def _input_port_ip():
    server_ip = input("Enter the IP Address of TCP Server to Connect to: ")
    while not _validate_ip(server_ip):
        server_ip = input("Invalid IP Address. Please specify a valid IP i.e. 192.168.0.10: ")

    target_port = input("Enter Target Port to Connect to on TCP Server: ")
    while not _validate_port(target_port):
        target_port = input("Invalid port number. Please specify a valid port between 1-65535: ")

    return server_ip, target_port


def _build_logger():
    """ Build Logger for the program """
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler_info = RotatingFileHandler('../logs/client_info.log', maxBytes=1048576)
    file_handler_warning = RotatingFileHandler('../logs/client_warning.log', maxBytes=1048576)
    file_handler_error = RotatingFileHandler('../logs/client_error.log', maxBytes=1048576)
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


def _build_parser():
    """ Build Parser to accept user-defined arguments """
    parser = argparse.ArgumentParser(description="Covert Channels")
    required_args = parser.add_argument_group('Required Arguments')
    required_args.add_argument('-m', '--message', required=True, type=str, help="Please enter covert message"
                                                                                " to be sent")

    args = parser.parse_args()
    print(f"Parameters Inputted: Plaintext Message = {args.message}")
    return args


def _validate_port(port):
    """Ensure valid port number via regex"""
    regex = re.compile(r'(\d)+')
    if regex.fullmatch(port) and 1 <= int(port) <= 65535:
        return True
    return False


def _validate_ip(ip):
    """Ensure valid IP Address via regex"""
    regex = re.compile(r"""
                        \b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3} # Match first 3 ocetets
                        (?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b          # Match final octet. No period at end
                        """, re.VERBOSE)
    if regex.search(ip):
        return True
    return False


if __name__ == "__main__":
    main()
