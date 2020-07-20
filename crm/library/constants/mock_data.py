# contains mock data for populate command

TEST_SUPERUSER_EMAIL = "super@superuser.com"
TEST_SUPERUSER_PASSWORD = "superuser"

TEST_ADMIN_EMAIL = "admin@admin.com"
TEST_ADMIN_PASSWORD = "admin"

TEST_MANAGER_EMAIL = "manager@manager.com"
TEST_MANAGER_PASSWORD = "manager"

TEST_CLIENT_EMAIL = "client@client.com"
TEST_CLIENT_PASSWORD = "client"

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

NEWS_CHARACTER = [{"character": "standard"}, {"character": "negative"}]
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
    {"method": "direct"},
    {"method": "bayer"}
]

MOCK_EMAILS = [
    {
        "email": "mail1@mail.com",
        "template": "My template 1",
        "signature": "My signature 1"
    },
    {
        "email": "mail2@mail.com",
        "template": "My template 2",
        "signature": "My signature 2"
    },
    {
        "email": "mail3@mail.com",
        "template": "My template 3",
        "signature": "My signature 3"
    }
]
