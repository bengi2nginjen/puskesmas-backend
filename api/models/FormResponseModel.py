class FormResponseModel :
    def __init__(self) :
        self.id = None
        self.form_id = None
        self.user_id = None
        self.date_created = None
        self.responses = []

class ResponseAnswer:
    def __init__(self) :
        self.id = None
        self.question_id = None
        self.response_value = None