# -*- coding: utf-8 -*-"


class ContactNotFound(Exception):
    def __init__(self):
        super().__init__("The contact not found")


class ContactAlreadyExist(Exception):
    def __init__(self):
        super().__init__("The contact already exists")


class ContactNameMandatory(Exception):
    def __init__(self):
        super().__init__("The contact name is required")


class ContactPhoneNotFound(Exception):
    def __init__(self):
        super().__init__("The contact phone number not found")


class ContactPhoneAlreadyExist(Exception):
    def __init__(self):
        super().__init__("The contact phone number already exists")


class ContactPhoneValueError(Exception):
    def __init__(self):
        super().__init__(
            "The contact phone number must consist of exactly ten digits " \
            "and must not contain any letters or other characters, " \
            "except for phone number formatting symbols"
        )
