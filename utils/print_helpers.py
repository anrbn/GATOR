# utils/print_helper.py

from termcolor import colored

def red(message):
    print(colored(message, 'red'))

def green(message):
    print(colored(message, 'green'))

def yellow(message):
    print(colored(message, 'yellow'))

def blue(message):
    print(colored(message, 'blue'))

def bluebold(message):
    print(colored(message, 'blue', attrs=['bold']))

def magenta(message):
    print(colored(message, 'magenta'))

def cyan(message):
    print(colored(message, 'cyan'))

def white(message):
    print(colored(message, 'white'))

def grey(message):
    print(colored(message, 'grey'))

def print_error(message):
    print(colored('ERROR:', 'red') + f" {message}")

def print_success(message):
    print(colored('SUCCESS:', 'green') + f" {message}")

def print_info(message):
    print(colored('INFO:', 'yellow') + f" {message}")