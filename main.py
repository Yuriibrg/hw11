import re
from collections import UserDict
from datetime import datetime


class AddressBook(UserDict):

    def __init__(self):
        self.data = {}
        self.listdata = []

    def show_all(self):
        counter = 0
        for k, v in self.data.items():
            counter += 1
            print(v)
        return f'List has {counter} profile(s)'

    def add_record(self, record):
        self.data[record.name.value] = record
        self.listdata.append(record)


    def iterator(self, num):
        counter = 0
        while counter < num:
            print(self.listdata[counter])
            counter += 1


class Record:

    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone != None:
            self.phones.append(phone)

    def change(self, phone1, phone2):
        for i in self.phones:
            if i.value == phone1:
                i.value = phone2
                return f'Number {phone1} from {self.name}`s list changed to {phone2}'
        return f'Number {phone1} is not exist in {self.name} list'

    def delete(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)
                return f'Number {phone} deleted from {self.name}`s number list'
        return f'Number {phone} is not exist in {self.name} list'

    def add_number(self, phone):
        for i in self.phones:
            if i.value == phone.value:
                return f'This number is already in database'
        self.phones.append(phone)

    def days_to_birthday(self):
        if self.birthday == None:
            return f'{self.name.value}`s birth date is not exist in this database.'
        else:
            d_now = datetime.now()
            if datetime(day=d_now.day, month=d_now.month, year=d_now.year) > datetime(day=self.birthday.value.day,
                                                                                      month=self.birthday.value.month,
                                                                                      year=d_now.year):
                diff = (datetime(day=d_now.day, month=d_now.month, year=d_now.year) - datetime(
                    day=self.birthday.value.day, month=self.birthday.value.month, year=d_now.year)).days
                return f'{diff} days to {self.name.value}`s birthday'
            elif datetime(day=d_now.day, month=d_now.month, year=d_now.year) < datetime(day=self.birthday.value.day,
                                                                                        month=self.birthday.value.month,
                                                                                        year=d_now.year):
                diff = (datetime(day=d_now.day, month=d_now.month, year=d_now.year + 1) - datetime(
                    day=self.birthday.value.day, month=self.birthday.value.month, year=d_now.year)).days
                return f'{diff} days to {self.name.value}`s birthday'
            elif datetime(day=d_now.day, month=d_now.month, year=d_now.year) == datetime(day=self.birthday.value.day,
                                                                                         month=self.birthday.value.month,
                                                                                         year=d_now.year):
                return f'Today is {self.name.value}`s birthday'

    def __str__(self) -> str:
        self.phones_show = None
        if len(self.phones) == 0:
            self.phones_show = 'not exist in this database'
        elif len(self.phones) == 1:
            self.phones_show = str(self.phones[0])
        elif len(self.phones) > 1:
            self.phones2 = [*self.phones]
            self.phones_show = [*self.phones2]
        if self.birthday == None:
            return f'{self.name.value} phone(s) is {self.phones_show}.'
        else:
            return f'{self.name.value} phone(s) is {self.phones_show}, his/here birth date is {self.birthday}.'


class Field:
    pass


class Name(Field):
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'


class Phone(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if is_number_valid(value):
            self.__value = value
        else:
            raise ValueError

    def __repr__(self) -> str:
        return f'{self.value}'


class Birthday(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if is_birthday_valid(value):
            d, m, y = value.split('.')
            new_value = datetime(day=int(d), month=int(m), year=int(y))
            self.__value = new_value
        else:
            raise ValueError

    def __repr__(self) -> str:
        return f'{self.value.strftime("%d %B %Y")}'


############### Функції валідації дня нарордження і номеру ####################
def is_birthday_valid(value):
    searcher = re.findall('\d{2}\.\d{2}\.\d{4}', value)
    if value == searcher[0]:
        d, m, y = value.split('.')
        try:
            new_value = datetime(day=int(d), month=int(m), year=int(y))
            return True
        except ValueError:
            return False
    else:
        return False


def is_number_valid(value):
    searcher = re.findall('\d{10}', str(value))
    if value == searcher[0]:
        return True
    else:
        return False
    #######################################################################


phone_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except TypeError:
            return 'TypeError! Try to type command again.'
        except IndexError:
            return 'IndexError! Try to type command again.'
        except KeyError:
            return 'KeyError! Try to type command again.'
        except ValueError:
            return 'ValueError! Try to type command again.'

    return wrapper


def exit(*args):
    return "Good bye!"


@input_error
def add_contact(
        *args):
    for k, v in phone_book.items():
        if k == args[0]:
            return f'{args[0]} is already in list'
    name = Name(args[0])
    if len(args) == 2:
        phone = Phone(args[1])
    if len(args) == 3:
        phone = Phone(args[1])
        birthday = Birthday(args[2])
    if len(args) == 1:
        rec = Record(name)
    elif len(args) == 2:
        rec = Record(name, phone)
    else:
        rec = Record(name, phone, birthday)

    phone_book.add_record(rec)
    # print(phone_book, 'after')
    return f'Contact {name.value} added successfuly'


@input_error
def add_number(*args):  # Для add_number потрібно ввести Ім'я і Новий номер, який ви хочете додати
    rec = phone_book[args[0]]
    # print(rec)
    new_number = Phone(args[1])
    # print(rec.phones)
    if rec.add_number(new_number) == None:
        return f'Number {new_number.value} added to {rec.name}`s list of numbers successfuly'
    else:
        return rec.add_number(new_number)


@input_error
def add_birthday(*args):
    rec = phone_book[args[0]]
    rec.birthday = Birthday(args[1])
    return f'Birthday is updated to {rec.birthday.value.strftime("%d %B %Y")}'


@input_error
def change(*args):
    for k, v in phone_book.items():
        if k == args[0]:
            rec = phone_book[args[0]]
            return rec.change(args[1], args[2])
    return f'{args[0]} isn`t exist in list of names'


@input_error
def delete(*args):
    for k, v in phone_book.items():
        if k == args[0]:
            rec = phone_book[args[0]]
            return rec.delete(args[1])
    return f'{args[0]} isn`t exist in list of names'


@input_error
def phone(*args):
    rec = phone_book[args[0]]
    return rec


@input_error
def show_all(*args):
    return phone_book.show_all()


@input_error
def days_to_birthday(*args):
    for k, v in phone_book.items():
        if k == args[0]:
            rec = phone_book[args[0]]
            return rec.days_to_birthday()
    return f'{args[0]} isn`t exist in list of names'


@input_error
def show_num(*args):
    phone_book.iterator(int(args[0]))
    return f'{args[0]} profile(s) showed'


COMMANDS = {
    exit: ["good bye", "close", "exit", "."],
    add_contact: ["add contact", "add c"],
    add_number: ["add number", "add n"],
    show_all: ["show all"],
    phone: ["phone"],
    change: ["change", "change phone"],
    delete: ["delete"],
    add_birthday: ["add birthday", "add b"],
    days_to_birthday: ["days to birthday", "d t b"],
    show_num: ["show num"]
}


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")
    return 'continue', user_input


@input_error
def main():
    while True:
        user_input = input(">>>")
        result, data = parse_command(user_input)
        if result == 'continue':
            continue
        print(result(*data))
        if result is exit:
            break


if __name__ == "__main__":
    main()

