import json, os

wave_with_attachments_filename = 'news_with_attachments.json'
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), wave_with_attachments_filename)
f = open(path)
wave = json.load(f)
