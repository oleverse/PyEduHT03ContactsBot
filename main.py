import re

GOOD_BYE_MSG = "Good bye!"
COMMAND_ARGS_MAX_COUNT = 2
INDEX_NOT_FOUND = -1

CONTACTS = []


# utilities
def contact_index(name):
    """Returns the index of a contact in the CONTACTS list"""

    try:
        return [item["name"] for item in CONTACTS].index(name)
    except ValueError:
        return INDEX_NOT_FOUND


def contact_exists(name):
    """Returns whether a contact exists"""
    return contact_index(name) != INDEX_NOT_FOUND


def sanitize_phone_number(phone):
    """Cleans phone numbers"""

    ptrn = re.compile(r"[^+\d]")

    new_phone = re.sub(pattern=ptrn, repl="", string=phone)
    new_phone = (
        new_phone[0] +
        new_phone[1:].replace("+", "")
    )

    return new_phone


def input_error(handler):
    """Errors handler"""

    def decorate_handler(data):
        warning = ""
        if handler.__name__  == "call_handler":
            command = data[0]
            
            if data[1]:
                args_count = len(data[1])
                if args_count > COMMANDS[command]["args_count"]:
                    warning = "Extra arguments discarded.\n"
        try:
            return f"{warning}{handler(data)}"
        except KeyError:
            if handler.__name__  == "call_handler":
                return "Unknown command."
        except ValueError:
            if handler.__name__  == "call_handler":
                return "Too many arguments."
        except IndexError:
            if handler.__name__ in(
                    "add_handler",
                    "change_handler"
                ):
                if not data:
                    return "Specify a name and a phone please."
                else:
                    return "Phone number is not specified."
            else:
                if not data:
                    return "Specify a name please."
    return decorate_handler


# command handlers
@input_error
def hello_handler(data=None):
    return "How can I help you?"


@input_error
def add_handler(data):
    if contact_exists(data[0]):
        return 'Contact exists, use "change" command'

    phone = sanitize_phone_number(data[1])

    CONTACTS.append({
        "name": data[0],
        "phone": phone
    })
    
    return "Contact successfully added."


@input_error
def change_handler(data):
    if (index := contact_index(data[0])) != INDEX_NOT_FOUND:
        phone = sanitize_phone_number(data[1])
        CONTACTS[index]["phone"] = phone
        return "Contact successfully changed."
    else:
        return "Contact not found."


@input_error
def phone_handler(data):
    if (index := contact_index(data[0])) != INDEX_NOT_FOUND:
        return CONTACTS[index]["phone"]
    else:
        return "Contact not found."


@input_error
def show_all_handler(data=None):
    result = []

    for contact in CONTACTS:
        result.append(": ".join((contact["name"], contact["phone"])))

    if result:
        return "\n".join(result)
    else:
        return "I do not have any contacts yet."


@input_error
def exit_handler(data=None):
    return GOOD_BYE_MSG


COMMANDS = {
    "hello": {
        "handler": hello_handler,
        "args_count": 0
    },
    "add": {
        "handler": add_handler,
        "args_count": 2
    },
    "change": {
        "handler": change_handler,
        "args_count": 2
    },
    "phone": {
        "handler": phone_handler,
        "args_count": 1
    },
    "show all": {
        "handler": show_all_handler,
        "args_count": 0
    },
    "good bye": {
        "handler": exit_handler,
        "args_count": 0
    },
    "goodbye": {
        "handler": exit_handler,
        "args_count": 0
    },
    "close": {
        "handler": exit_handler,
        "args_count": 0
    },
    "exit": {
        "handler": exit_handler,
        "args_count": 0
    }
}


@input_error
def call_handler(command_data):
    if command_data[1] and len(command_data[1]) > COMMAND_ARGS_MAX_COUNT:
        raise ValueError
    return COMMANDS[command_data[0]]["handler"](command_data[1])


def main():
    while True:
        try:
            command_with_args = input("Enter command: ").strip()
        except KeyboardInterrupt:
            print(f"\n{GOOD_BYE_MSG}")
            return False
        
        if command_with_args:
            command_parts = command_with_args.split(' ')
            
            command = None
            data = None
            for i, _ in enumerate(command_parts):
                if (command := ' '.join(command_parts[:i+1])) in list(COMMANDS.keys()):
                    data = command_parts[i+1:]
                    break

            handler_result = call_handler((command, data))

            print(handler_result)

            if handler_result == GOOD_BYE_MSG:
                break


if __name__ == "__main__":
    main()