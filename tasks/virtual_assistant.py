# -*- coding: utf-8 -*-"

"""
Core functions for virtual assistant
"""

import signal
import functools
from typing import Optional, Any, Callable
from pathlib import Path

from .cutil import console_style_reset, print_error, print_welcome, print_exit, print_help, print_colored
from .cutil import ERROR_TEXT_COLOR
from .futil import get_absolute_path, load_json_file_data, write_json_file_data


HELP: str = """
1. Command "hello" – displays the phrase "How can I help you?"

Example:
Input: "hello"
Output: "How can I help you?"

---

2. Command "add [name] [phone number]" – adds a contact

Example:
Input: "add John 1234567890"
Output: "Contact added."

---

3. Command "change [name] [new phone number]" – updates the contact's phone number

Example:
Input: "change John 0987654321"
Output: "Contact updated." or an error message if the name is not found

---

4. Command "phone [name]" – returns the phone number for the contact

Example:
Input: "phone John"
Output: [phone number] or an error message if the name is not found

---

5. Command "delete [name]" – deletes the contact

Example:
Input: "delete John"
Output: "Contact deleted." or an error message if the name is not found

---

6. Command "all" – returns the list of all contacts

Example:
Input: "all"
Output: all saved contacts with their phone numbers

---

7. Command "quit", "exit", or "close" – ends the bot session

Example:
Input: any of these words
Output: "Good bye!" and the bot stops running
"""


CONTACTS_FILE: Path = get_absolute_path(Path(__file__).parent / "data" / "__contacts__.json")


def exit_by_terminate_by_signals(number: int, stack: Any) -> None:
    """Exit by the SIGTERM/SIGINT signal

    :param number: signal number (number, mandatory)
    :param stack: current stack frame (number, mandatory)
    """

    print()
    print_exit("Good bye!")


def read_contacts_from_file() -> dict[str, str]:
    """Read contacts from a file

    :return contacts data (dictionary)
    """
    contacts: Optional[dict[str, str]] = load_json_file_data(CONTACTS_FILE, ignore_if_not_exist=True)
    return contacts if contacts is not None else {}


def write_contacts_to_file(contacts: dict[str, str]) -> None:
    """Write contacts to a file

    :param contacts: contacts data (dictionary, mandatory)
    """
    write_json_file_data(CONTACTS_FILE, contacts if contacts is not None else {})


def parse_input(user_input: str) -> tuple[str, ...]:
    """Parse user input data

    :param user_input: user input data (string, mandatory)
    :return command and arguments (tuple of strings)
    """
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args
    except ValueError:
        return ("", )

def input_error(
        value_error_message: Optional[str] = None,
        key_error_message: Optional[str] = None,
        index_error_message: Optional[str] = None,
) -> Callable:
    """Decorator functions with exceptions processing

    :param value_error_message: value error message (string, optional)
    :param key_error_message: key error message (string, optional)
    :param index_error_message: index error message (string, optional)
    :return exceptions processing function (Callable)
    """

    def _input_error(func: Callable):

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> tuple:
            try:
                return func(*args, **kwargs)
            except IndexError as e:
                return ERROR_TEXT_COLOR, index_error_message or str(e)
            except KeyError as e:
                return ERROR_TEXT_COLOR, key_error_message or str(e)
            except ValueError as e:
                return ERROR_TEXT_COLOR, value_error_message or str(e)

        return wrapper

    return _input_error


def show_all(contacts: dict[str, str]) -> str:
    """Return all contacts as string

    :param contacts: contacts data (dictionary, mandatory)
    :return contacts as string (string)
    """

    return "\n".join([f"{name}\t{phone}" for name, phone in contacts.items()])


@input_error(
    index_error_message="Give me the name, please.",
    key_error_message="Contact does not exist.",
)
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """Return the phone for contact

    :param args: arguments with contact name (list of string, mandatory)
    :param contacts: contacts data (dictionary, mandatory)
    :return contact's phone (string)
    """

    # Verify the number of arguments
    if len(args) < 1:
        raise IndexError("Invalid command arguments")

    # Unpack the arguments to the name
    name, *_ = args

    # Verify if the contact exists
    if name not in contacts:
        raise KeyError("Contact does not exist")

    return contacts.get(name, "")


@input_error(
    index_error_message="Give me the name and phone number, please.",
)
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Add contact to the contacts

    :param args: arguments with contact name and phone number (list of string, mandatory)
    :param contacts: contacts data (dictionary, mandatory)
    :return Operation status string (string)
    """

    # Verify the number of arguments
    if len(args) < 2:
        raise IndexError("Invalid command arguments")

    # Unpack the arguments to the name and phone number
    name, phone, *_ = args

    # Verify if the contact already exists
    if name in contacts:
        raise ValueError("Contact already exists")

    # Add contact
    contacts[name] = phone

    # Save contacts to the file
    write_contacts_to_file(contacts)

    return "Contact added."


@input_error(
    index_error_message="Give me the name and phone number, please.",
    key_error_message="Contact does not exist.",
)
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Change the contact phone number

    :param args: arguments with contact name and phone number (list of string, mandatory)
    :param contacts: contacts data (dictionary, mandatory)
    :return Operation status string (string)
    """

    # Verify the number of arguments
    if len(args) < 2:
        raise IndexError("Invalid command arguments")

    # Unpack the arguments to the name and phone number
    name, phone, *_ = args

    # Verify if the contact exists
    if name not in contacts:
        raise KeyError("Contact does not exist")

    # Change contact
    contacts[name] = phone

    # Save contacts to the file
    write_contacts_to_file(contacts)

    return "Contact updated."


@input_error(
    index_error_message="Give me the name, please.",
    key_error_message="Contact does not exist.",
)
def delete_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Delete the contact

    :param args: arguments with contact name (list of string, mandatory)
    :param contacts: contacts data (dictionary, mandatory)
    :return Operation status string (string)
    """

    # Verify the number of arguments
    if len(args) < 1:
        raise IndexError("Invalid command arguments")

    # Unpack the arguments to the name
    name, *_ = args

    # Verify if the contact exists
    if name not in contacts:
        raise KeyError("Contact does not exist")

    # Delete contact
    contacts.pop(name, None)

    # Save contacts to the file
    write_contacts_to_file(contacts)

    return "Contact deleted."


def main() -> None:
    # Interceptors for the SIGINT and SIGTERM signals (for example Ctrl + c exit)
    signal.signal(signal.SIGINT, exit_by_terminate_by_signals)
    signal.signal(signal.SIGTERM, exit_by_terminate_by_signals)

    try:
        # Init contacts data
        contacts: dict[str, str] = read_contacts_from_file()

        print_welcome("Welcome to the assistant bot!")
        print_help("Enter 'help' for a list of built-in commands.")

        while True:
            command: Optional[str] = None
            args: list[str] = []
            try:
                command, *args = parse_input(input("Enter a command: "))
            except EOFError:
                break

            if command in {"close", "exit", "quit", }:
                print_exit("Good bye!")
                break

            try:
                match command:
                    case "hello":
                        print_colored("How can I help you?")
                    case "help":
                        print_help(HELP)
                    case "all":
                        print_colored(show_all(contacts))
                    case "phone":
                        print_colored(show_phone(args, contacts))
                    case "add":
                        print_colored(add_contact(args, contacts))
                    case "change":
                        print_colored(change_contact(args, contacts))
                    case "delete":
                        print_colored(delete_contact(args, contacts))
                    case _:
                        print_error("Invalid command.")
            except Exception as e:
                print_error("An unexpected error occurred: {error}.".format(error=repr(e)))
    except Exception as e:
        print_error("An unexpected error occurred: {error}.".format(error=repr(e)))

    # Reset console styles to default
    console_style_reset()

    exit(0)


if __name__ == "__main__":
    main()
