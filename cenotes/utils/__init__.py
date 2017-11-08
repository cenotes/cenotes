class CENParams(object):
    def __init__(self, plaintext=None, key=None, expiration_date=None,
                 visits_count=None, max_visits=None, no_store=False,
                 payload=None, **kwargs):
        self.plaintext = plaintext
        self.key = key
        self.payload = payload
        self.expiration_date = expiration_date
        self.visits_count = visits_count
        self.max_visits = max_visits
        self.no_store = no_store
