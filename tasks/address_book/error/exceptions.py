# -*- coding: utf-8 -*-"

"""
Exceptions for address book implementation
"""


class ObjectNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class ObjectAlreadyExist(Exception):
    def __init__(self, message):
        super().__init__(message)


class ObjectValueError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ContactNotFound(ObjectNotFound):
    def __init__(self):
        super().__init__("The contact not found")


class ContactAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The contact already exists")


class ContactNameMandatory(ObjectValueError):
    def __init__(self):
        super().__init__("The contact name is required")


class ContactPhoneNotFound(ObjectNotFound):
    def __init__(self):
        super().__init__("The contact phone number not found")


class ContactPhoneAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The contact phone number already exists")


class ContactPhoneValueError(ObjectValueError):
    def __init__(self):
        super().__init__(
            "The contact phone number must consist of exactly ten digits " \
            "and must not contain any letters or other characters, " \
            "except for phone number formatting symbols"
        )


class ContactEmailNotFound(ObjectNotFound):
    def __init__(self):
        super().__init__("The contact email not found")


class ContactEmailAlreadyExist(ObjectAlreadyExist):
    def __init__(self):
        super().__init__("The contact email already exists")


class ContactEmailValueError(ObjectValueError):
    def __init__(self):
        super().__init__("The contact email must be a valid email address")
