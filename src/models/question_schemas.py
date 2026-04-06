from typing import List, Optional
from pydantic import BaseModel, Field, validator

class MCQQuestions(BaseModel):

    question:str = Field(description="The question to be asked")
    options:List[str] = Field(description="The options for the question")
    correct_answer:str = Field(description="The correct answer for the question")

    @validator('question',pre=True)
    def check_question(cls,v):
        if isinstance(v,dict):
            return v.get("description",str(v))
        return str(v)

class FillInTheBlanksQuestion(BaseModel):

    question:str = Field(description="he question text with '___' for the blank")
    correct_answer:str = Field(description="The correct answer for the question")

    @validator('question',pre=True)
    def check_question(cls,v):
        if isinstance(v,dict):
            return v.get("description",str(v))
        return str(v)