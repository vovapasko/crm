init_user_data = {
    "email": "newuser@mail.com",
    "password": "old_password"
}
no_number_data = {
    "password_data": {
        "password": "new_password"
    },
    # we provide such key because ValidationError returns error message exactly in this format
    "password": ["Password must contain at least one number"]
}
short_password_data = {
    "password_data": {
        "password": "password1"
    },
    # we provide such key because ValidationError returns error message exactly in this format
    "password": ["Password must be at least 12 characters"]
}
no_symbols_data = {
    "password_data": {
        "password": "new_password1new_password1new_password1"
    },
    # we provide such key because ValidationError returns error message exactly in this format
    "password": ["Password must contain at least one symbol"]
}
no_letters_data = {
    "password_data": {
        "password": "0123445456542213123"
    },
    # we provide such key because ValidationError returns error message exactly in this format
    "password": ["Password must contain at least one symbol"]
}
no_letters_with_symbol_data = {
    "password_data": {
        "password": "01&3445456542213123"
    },
    # we provide such key because ValidationError returns error message exactly in this format
    "password": ["Password must contain at least one letter"]
}
one_case_data = {
    "password_data": {
        "password": "pubuiebbiuv@234_"
    },
    # we provide such key because ValidationError returns error message exactly in this format
    "password": ["Password must contain letters of different cases"]
}
new_user_correct_password = {
    "password": "PubuiebBIUV@234_"
}
