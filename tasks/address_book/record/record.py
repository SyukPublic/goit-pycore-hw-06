# -*- coding: utf-8 -*-"

"""
Record class for address book implementation
"""

import re
from typing import Optional


from ..error import (
    ContactNameMandatory,
    ContactPhoneNotFound,
    ContactPhoneAlreadyExist,
    ContactPhoneValueError,
    ContactEmailNotFound,
    ContactEmailAlreadyExist,
    ContactEmailValueError,
)


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
    value_clear_pattern = re.compile(r"[()-]|\s")
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
        # Clear the phone number from formatting symbols and whitespaces
        value = re.sub(cls.value_clear_pattern, '', value)
        # Verify the phone number
        if not re.match(cls.value_match_pattern, value):
            raise ContactPhoneValueError()
        return value


class Email(Field):
    value_clear_pattern = re.compile(r"\s")
    value_match_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def __init__(self, value: str):
        """ Initialize the Email field with the specified value

        :param value: the value (string, mandatory)
        """
        super().__init__(self.prepare(value))

    @classmethod
    def prepare(cls, value: str) -> str:
        """ Email number validation and sanitization

        :param value: email (string, mandatory)
        :return: sanitized email (string)
        """

        # Check whether the email is empty or None
        if not value:
            raise ContactEmailValueError()
        # Clear the email from whitespaces
        value = re.sub(cls.value_clear_pattern, '', value)
        # Verify the email
        if not re.match(cls.value_match_pattern, value):
            raise ContactEmailValueError()
        return value


class Record:
    def __init__(self, name: str, phones: Optional[list[str]] = None, emails: Optional[list[str]] = None):
        """ Initialize the Contact record for the specified Name and with Phone numbers oe Emails, if given

        :param name: the name value (string, mandatory)
        :param phones: the phone numbers (list of strings, optional)
        :param emails: the emails (list of strings, optional)
        """
        self.name = Name(name)
        self.phones = []
        self.emails = []
        # Add phone numbers if given, removing duplicates
        if isinstance(phones, list):
            for phone in phones:
                if self.__find_phone(phone) is None:
                    self.add_phone(phone)
        # Add emails if given, removing duplicates
        if isinstance(emails, list):
            for email in emails:
                if self.__find_email(email) is None:
                    self.add_email(email)

    def __find_phone(self, phone: str) -> Optional[Phone]:
        """ Private method for searching the phone number

        :param phone: phone number (string, mandatory)
        :return: phone field, if found (Phone, optional)
        """
        # Clear the phone number from formatting symbols and whitespaces
        phone = Phone.prepare(phone)
        # Find and return by phone number
        return next((p for p in self.phones if p.value == phone), None)

    def __find_email(self, email: str) -> Optional[Email]:
        """ Private method for searching the email

        :param email: email (string, mandatory)
        :return: email field, if found (Email, optional)
        """
        # Clear the email fom whitespaces
        email = Email.prepare(email)
        # Find and return by email
        return next((p for p in self.emails if p.value == email), None)

    def find_phone(self, phone: str) -> Phone:
        """ Search and return the phone number, or raise the phone number not found exception

        :param phone: phone number (string, mandatory)
        :return: phone field, if found (Phone)
        """
        phone_object: Optional[Phone] = self.__find_phone(phone)
        if phone_object is None:
            # Phone number not found - raise the phone number not found exception
            raise ContactPhoneNotFound
        # Return the phone number field
        return phone_object

    def add_phone(self, phone: str) -> None:
        """ Add the phone number, or raise the phone number already exists exception

        :param phone: phone number (string, mandatory)
        """
        if self.__find_phone(phone):
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

    def find_email(self, email: str) -> Phone:
        """ Search and return the email, or raise the email not found exception

        :param email: email (string, mandatory)
        :return: email field, if found (Email)
        """
        email_object: Optional[Phone] = self.__find_email(email)
        if email_object is None:
            # Email not found - raise the email not found exception
            raise ContactEmailNotFound()
        # Return the phone number field
        return email_object

    def add_email(self, email: str) -> None:
        """ Add the email, or raise the email already exists exception

        :param email: email (string, mandatory)
        """
        if self.__find_email(email):
            # Email found - raise the email already exists exception
            raise ContactEmailAlreadyExist()
        # Add the email
        self.emails.append(Email(email))

    def remove_email(self, email: str) -> None:
        """ Remove the email, or raise the email not found exception

        :param email: email (string, mandatory)
        """
        self.emails.remove(self.find_email(email))

    def edit_email(self, existing_email: str, email: str) -> None:
        """ Edit the email, or raise the email not found exception

        :param existing_email: email (string, mandatory)
        :param email: new email (string, mandatory)
        """
        self.emails[self.emails.index(self.find_email(existing_email))] = Email(email)


    def __str__(self) -> str:
        """ Create a readable string for the class instance

        :return: readable string (string)
        """
        return "Contact name: {name}, phones: {phones}, emails: {emails}".format(
            name=self.name.value,
            phones="; ".join(p.value for p in self.phones),
            emails="; ".join(p.value for p in self.emails),
        )
