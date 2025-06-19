# -*- coding: utf-8 -*-"

import re
from collections import UserDict
from typing import Optional


from .error import *


class Field:
    def __init__(self, value: str):
        """ Initialize the field with the specified value

        :param value: the value (string, mandatory)
        """
        self.value = value

    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        """ Initialize the Name field with the specified value

        :param value: the value (string, mandatory)
        """
        # Check whether the name is empty or None
        if not value:
            raise ContactNameMandatory()
        super().__init__(value)

class Phone(Field):
    value_clear_pattern = re.compile(r"[ ()-]")
    value_match_pattern = re.compile(r"^\d{10}$")

    def __init__(self, value: str):
        """ Initialize the Phone number field with the specified value

        :param value: the value (string, mandatory)
        """
        super().__init__(self.prepare(value))

    @classmethod
    def prepare(cls, value: str) -> str:
        """ Phone number validation and sanitization

        :param value: phone number (string, mandatory)
        :return: sanitized phone number (string)
        """

        # Check whether the phone number is empty or None
        if not value:
            raise ContactPhoneValueError()
        # Clear the phone number from formatting symbols
        value = re.sub(cls.value_clear_pattern, '', value)
        # Verify the phone number
        if not re.match(cls.value_match_pattern, value):
            raise ContactPhoneValueError()
        return value


class Record:
    def __init__(self, name: str, *args):
        """ Initialize the Contact record for the specified Name and with Phone numbers, if given

        :param name: the name value (string, mandatory)
        :param args: the phone numbers (string, optional)
        """
        self.name = Name(name)
        self.phones = []
        # Add phone numbers if given, removing duplicates
        for phone in args:
            if self._find_phone(phone) is None:
                self.add_phone(phone)

    def _find_phone(self, phone: str) -> Optional[Phone]:
        """ Protected method for searching the phone number

        :param phone: phone number (string, mandatory)
        :return: phone field, if found (Phone, optional)
        """
        # Clear the phone number from formatting symbols
        phone = Phone.prepare(phone)
        # Find and return by phone number
        return next((p for p in self.phones if p.value == phone), None)

    def find_phone(self, phone: str) -> Phone:
        """ Search and return the phone number, or raise the phone number not found exception

        :param phone: phone number (string, mandatory)
        :return: phone field, if found (Phone)
        """
        phone_object: Optional[Phone] = self._find_phone(phone)
        if phone_object is None:
            # Phone number not found - raise the phone number not found exception
            raise ContactPhoneNotFound
        # Return the phone number field
        return phone_object

    def add_phone(self, phone: str) -> None:
        """ Add the phone number, or raise the phone number already exists exception

        :param phone: phone number (string, mandatory)
        """
        if self._find_phone(phone):
            # Phone number found - raise the phone number already exists exception
            raise ContactPhoneAlreadyExist()
        # Add the phone number
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """ Remove the phone number, or raise the phone number not found exception

        :param phone: phone number (string, mandatory)
        """
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, existing_phone: str, phone: str) -> None:
        """ Edit the phone number, or raise the phone number not found exception

        :param existing_phone: phone number (string, mandatory)
        :param phone: new phone number (string, mandatory)
        """
        self.phones[self.phones.index(self.find_phone(existing_phone))] = Phone(phone)


    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self, *args):
        """ Initialize an Address Book with the specified Contacts, if given

        :param args: the contact records (Record, optional)
        """
        super().__init__()
        # Add contact records if given, removing duplicates
        for contact in args:
            if str(contact.name) not in self:
                self.add_record(contact)

    def find(self, name: str) -> Record:
        """ Search and return the contact record, or raise the contact not found exception

        :param name: contact name (string, mandatory)
        :return: contact record, if found (Record)
        """
        if name not in self:
            # Contact found - raise the contact not found exception
            raise ContactNotFound
        # Return the contact
        return self.get(name, None)

    def add_record(self, contact: Record) -> None:
        """ Add the contact record, or raise the contact already exists exception

        :param contact: contact record (Record, mandatory)
        """
        if str(contact.name) in self:
            # Contact found - raise the contact already exists exception
            raise ContactAlreadyExist()
        # Add the contact
        self.data[str(contact.name)] = contact

    def delete(self, name: str) -> None:
        """ Remove the contact record, or raise the contact not found exception

        :param name: contact name (string, mandatory)
        """
        if name not in self:
            # Contact found - raise the contact not found exception
            raise ContactNotFound()
        # Remove the contact
        self.pop(name, None)
