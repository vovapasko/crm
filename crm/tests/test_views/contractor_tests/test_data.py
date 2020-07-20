mock_contractor = {
    "editor_name": "Editor 4",
    "contact_person": "Contact 4",
    "phone_number": "Number 4",
    "email": "contractor@contr.com",
    "news_amount": 50,
    "arranged_news": 20,
    "one_post_price": 140,
}
keys_to_check = ['previous', 'next', 'results', 'count']
correct_put_data = {
    "editor_name": "New Editor 4"
}
wrong_put_data_minus_number = {
    "news_amount": -50,
}
wrong_put_data_nan = {
    "news_amount": "five",
}
