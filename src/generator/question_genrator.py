from langchain.output_parsers import PydanticOutputParser
from src.models.question_schemas import FillInTheBlanksQuestion, MCQQuestions
from src.prompts.templats import fill_blank_prompt_template, mcq_prompt_template
from src.llm.groq_client import get_groq_client
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException

# logger = get_logger(__name__)

class QuestionGenerator:

    """Generates questions based on provided topics and difficulty levels."""
    def __init__(self):
        self.llm = get_groq_client()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self,prompt,parser,topic,difficulty):

        for attempts in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Attempt {attempts + 1} for topic '{topic}' with difficulty '{difficulty}'")
                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty))
                parsed = parser.parse(response.content)
                self.logger.info(f"Successfully parsed response on attempt {attempts + 1}")
                return parsed
            
            except Exception as e:
                self.logger.error(f"Error on attempt {attempts + 1}: {e}")
                if attempts == settings.MAX_RETRIES - 1:
                    raise CustomException(f"Failed to generate question after {settings.MAX_RETRIES} attempts: {e}")
                

    def generate_mcq(self,topic:str,difficulty:str='medium')->MCQQuestions:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestions)
            self.logger.info(f"Generating MCQ for topic '{topic}' with difficulty '{difficulty}'")
            question =self._retry_and_parse(mcq_prompt_template,parser,topic,difficulty)
            if len(question.options) != 4 and question.correct_answer not in question.options:
                raise ValueError(f"invalid MCQ structure")
            self.logger.info(f"Generated a valid MCQ")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {e}")
            raise CustomException(f"Failed to generate MCQ: {e}")

    def generate_fill_in_blank(self,topic:str,difficulty:str='medium')->FillInTheBlanksQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillInTheBlanksQuestion)
            self.logger.info(f"Generating fill-in-the-blank question for topic '{topic}' with difficulty '{difficulty}'")
            question = self._retry_and_parse(fill_blank_prompt_template,parser,topic,difficulty)
            if '_____' not in question.question:
                raise ValueError("The question must contain '_____' to indicate the blank.")
            self.logger.info(f"Generated a valid fill-in-the-blank question")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate fill-in-the-blank question: {str(e)}")
            raise CustomException(f"Failed to generate fill-in-the-blank question: {e}")
