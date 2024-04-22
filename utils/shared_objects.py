from pydantic import BaseModel

class AmericanQuestionObject(BaseModel):
    question: str
    answers: list[str]
    right_answer: int
    assistant_id: str
    thread_id: str

class AmericanQuestionObjectWithFileName(AmericanQuestionObject):
    file_name: str

class AnswerObject:
    def __init__(self, content, assistant_id, thread_id):
        self.content = content
        self.thread_id = thread_id
        self.assistant_id = assistant_id
