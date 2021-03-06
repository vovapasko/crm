# contains mock data for populate command

TEST_SUPERUSER_EMAIL = "super@superuser.com"
TEST_SUPERUSER_PASSWORD = "superuser"

TEST_ADMIN_EMAIL = "admin@admin.com"
TEST_ADMIN_PASSWORD = "admin"

TEST_MANAGER_EMAIL = "manager@manager.com"
TEST_MANAGER_PASSWORD = "manager"

TEST_CLIENT_EMAIL = "client@client.com"
TEST_CLIENT_PASSWORD = "client"

MOCK_USERS = [
    {
        "email": TEST_SUPERUSER_EMAIL,
        "password": TEST_SUPERUSER_PASSWORD,
        "is_confirmed": True
    },
    {
        "email": TEST_ADMIN_EMAIL,
        "password": TEST_ADMIN_PASSWORD,
        "is_confirmed": True
    },
    {
        "email": TEST_MANAGER_EMAIL,
        "password": TEST_MANAGER_PASSWORD,
        "is_confirmed": True
    },
    {
        "email": TEST_CLIENT_EMAIL,
        "password": TEST_CLIENT_PASSWORD,
        "is_confirmed": True
    }
]

MOCK_CONTRACTORS_DATA = [
    {
        "editor_name": "Editor 1",
        "contact_person": "Contact 1",
        "phone_number": "Number 1",
        "email": "contractor@contr.com",
    },
    {
        "editor_name": "Editor 2",
        "contact_person": "Contact 2",
        "phone_number": "Number 2",
        "email": "contractor2@contr.com",
    },
    {
        "editor_name": "Editor 3",
        "contact_person": "Contact 3",
        "phone_number": "Number 3",
        "email": "contractor3@contr.com",
    },
]

NEWS_CHARACTER = [{"character": "плюс"}, {"character": "минус"}]
CURRENCIES = [
    {
        "name": "Доллар",
        "sign": "$"
    },
    {
        "name": "Гривна",
        "sign": "₴"
    }
]
HASHTAGS = [
    {
        "name": "mytag1"
    },
    {
        "name": "mytag2"
    },
    {
        "name": "mytag3"
    }
]
BURST_METHODS = [
    {"method": "на прямую"},
    {"method": "на прямую через байера"},
    {"method": "топ сикрет"}
]

MOCK_EMAILS = [
    {
        "email": "mail1@mail.com",
        "template": "My template 1",
        "signature": "My signature 1",
        "codeword": "Publisher 1"
    },
    {
        "email": "mail2@mail.com",
        "template": "My template 2",
        "signature": "My signature 2",
        "codeword": "Publisher 2"
    },
    {
        "email": "mail3@mail.com",
        "template": "My template 3",
        "signature": "My signature 3",
        "codeword": "Publisher 3"
    }
]

MOCK_CLIENTS = [
    {
        "name": "John",
        "numbers": "+380501112233",
        "emails": "john@client.com",
        "price": 8400,
        "amount_publications": 150
    },
    {
        "name": "Peter",
        "numbers": "+380501112233",
        "emails": "peter@client.com",
        "price": 9400,
        "amount_publications": 250
    },
    {
        "name": "Vasya",
        "numbers": "+380501112233",
        "emails": "vasya@client.com",
        "price": 7400,
        "amount_publications": 50
    }
]

MOCK_NEWS_PROJECTS = [
    {
        "name": "Test project 1",
        "budget": 1234,
    },
    {
        "name": "Test project 2",
        "budget": 5678,
    },
    {
        "name": "Test project 3",
        "budget": 9012,
    },
]

MOCK_NEWS_WAVES = [
    {
        "title": "Test Title 1",
        "post_format": "test format 1"
    },
    {
        "title": "Test Title 2",
        "post_format": "test format 2"
    },
    {
        "title": "Test Title 3",
        "post_format": "test format 3"
    }
]
