class CENParams(object):
    def __init__(self, note_id=None, note_id_key=None, note_key=None,
                 note=None, expiration_date=None, visits_count=None,
                 max_visits=None, no_store=False, **kwargs):
        self.note_id = note_id
        self.note_id_key = note_id_key
        self.note_key = note_key
        self.note = note
        self.expiration_date = expiration_date
        self.visits_count = visits_count
        self.max_visits = max_visits
        self.no_store = no_store
