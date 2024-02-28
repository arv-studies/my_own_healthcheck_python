import pyfiglet
import argparse
from termcolor import colored


def create_ascii_art(text):
    if not text:
        text = "WELCOME"
    ascii_art = pyfiglet.figlet_format(text, font='ansi_shadow')
    startup = pyfiglet.figlet_format('Starting Up .......', font='big')
    texttoPrint1 = colored(f"{ascii_art}\n", "green", attrs=["bold"])
    texttoPrint2 = colored(f"{startup}\n", "red", attrs=["bold"])

    with open('/var/log/paj_logs/health_check.log', 'w') as f:
        f.write(texttoPrint1+texttoPrint2)
        print(texttoPrint1+texttoPrint2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Ascii representation')
    parser.add_argument(
        '--text', help='Text to write as ASCII', required=False)
    args = parser.parse_args()

    create_ascii_art(args.text)
