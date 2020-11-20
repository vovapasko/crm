FAKE_CREDENTIALS = {
    "token": "fake",
    "refresh_token": "fake",
    "token_uri": "fake",
    "client_id": "fake",
    "client_secret": "fake",
    "scopes": [
        'scope1',
        'scope2',
        'scope3',
    ]
}

example_email_inbox_response = {
    "messages": [
        {
            "id": "",
            "threadId": "",
            "labelIds": [
                "SENT"
            ],
            "snippet": "Great, thanks! пн, 5 окт. 2020 г. в 16:24, Petro Bylyk &lt;petro307302@gmail.com&gt;: Yes, I got your email. пн, 5 окт. 2020 г. в 16:23, Vitaly Lymar &lt;vitlym0107@gmail.com&gt;: Hi, Let&#39;s try to",
            "payload": {
                "mimeType": "multipart/alternative",
                "headers": [
                    {
                        "name": "MIME-Version",
                        "value": "1.0"
                    },
                    {
                        "name": "Date",
                        "value": "Mon, 5 Oct 2020 16:24:25 +0300"
                    },
                    {
                        "name": "References",
                        "value": "<CAHtF18PTpiFxm+P7StYv0T6TnGFUo1e=k8AgXqjD8nGKPd5n0w@mail.gmail.com> <CAFOWzxZRXt_28X3e2CwZHKWX5SDwMnx=GkSk+D-mGNZJLvFhbw@mail.gmail.com>"
                    },
                    {
                        "name": "In-Reply-To",
                        "value": "<CAFOWzxZRXt_28X3e2CwZHKWX5SDwMnx=GkSk+D-mGNZJLvFhbw@mail.gmail.com>"
                    },
                    {
                        "name": "Message-ID",
                        "value": "<CAHtF18OKLRcD8NkXBi5fBauMJxGSXqMWLq5DuPV+swB7S-XbgQ@mail.gmail.com>"
                    },
                    {
                        "name": "Subject",
                        "value": "Re: Meeting"
                    },
                    {
                        "name": "From",
                        "value": "Vitaly Lymar <vitlym0107@gmail.com>"
                    },
                    {
                        "name": "To",
                        "value": "Petro Bylyk <petro307302@gmail.com>"
                    },
                    {
                        "name": "Content-Type",
                        "value": "multipart/alternative; boundary=\"0000000000006fa40e05b0ec6609\""
                    }
                ]
            },
            "sizeEstimate": 2095,
            "historyId": "1838",
            "internalDate": "1601904265000"
        }
    ],
    "resultSizeEstimate": 4,
    "labels": [
        {
            "id": "CHAT",
            "name": "CHAT",
            "messageListVisibility": "hide",
            "labelListVisibility": "labelHide",
            "type": "system"
        }
    ],
    "emailAddress": "adress@gmail.com",
    "messagesTotal": 8,
    "threadsTotal": 6,
    "historyId": "2108"
}
