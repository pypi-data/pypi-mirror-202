import json
import requests

class goosu:
    session = requests.session()
    param = {
        'url': None,
        'is_public': 1,
        'alias': None,
        'password': None
    }
    @classmethod
    def shorted_url(cls, url: str):
        cls.param['url'] = url
        r = cls.session.get('https://goo.su/frontend-api/convert',params=cls.param).text
        r = json.loads(r)['short_url']
        return r










