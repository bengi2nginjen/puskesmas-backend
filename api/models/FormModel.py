class FormModel :
    def __init__(self) :
        self.id = None
        self.name = None
        self.date_created = None
        self.created_by = None
        self.description = None
        self.questions = []

class Question:
    def __init__(self):
        self.id = None
        self.question = None
        self.number = None
        # self.required = False
        self.input = []
    
class Input:
    def __init__(self):
        self.id = None
        self.text = None
        self.type = None
    
class InputType:
    Text = "TEXT"
    LongText = "LONG_TEXT"
    Select = "SELECT_OPTION"
    Radiobutton = "RADIO"
    Checkbox = "CHECK"
    Date = "DATE"

class FormResponse:
    def __init__(self):
        self.id = None
        self.form_id = None
        self.user_id = None
        self.date_created = None
        self.user_response = None

class Response:
    def __init__(self):
        self.id = None
        self.question_id = None
        self.response_value = None
    
