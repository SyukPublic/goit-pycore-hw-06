# -*- coding: utf-8 -*-"

"""
Address Book class implementation
"""


from collections import UserDict


from .error import ContactNotFound, ContactAlreadyExist
from .record import Record


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
