from pydantic import BaseModel
from openai import OpenAI
from django.conf import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class MCQChoice(BaseModel):
    text_en: str
    text_hi: str
    is_correct: bool


class MCQQuestion(BaseModel):
    text_en: str
    text_hi: str
    choices: list[MCQChoice]


class ListOfMCQQuestions(BaseModel):
    questions: list[MCQQuestion]


def generate_mcqs(content):
    """Generate 10 MCQs using OpenAI's API based on the provided content."""
    try:
        # System message with optimized instructions
        system_message = """
        You are an exam preparation assistant. Your task is to generate multiple-choice questions (MCQs) based on the provided content.
        The questions should comprehensively cover the key concepts of the content, and each question should be objective, clear, and unambiguous.
        Ensure that the options provided for each question are plausible, with only one correct answer that cannot be easily guessed by random chance.
        The questions should be challenging and require understanding of the content, not simple factual recall.
        Avoid common patterns that make the correct answer too obvious.
        Provide four options per question, clearly distinguishing the correct answer from the incorrect ones.
        For each question and option, provide the text in both **English** and **Hindi (Devanagari)**.
        Your goal is to generate 10 MCQs based on the following content.
        """

        user_message = f"""
        Generate 10 multiple-choice questions based on the following content, ensuring that they comprehensively cover the material and are suitable for someone preparing for an exam.
        For each question and option, provide the text in **both English and Hindi (Devanagari)**.
        Content:
        {content}
        """

        # Request completion from OpenAI API using the new client and system+user prompt structure
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            response_format=ListOfMCQQuestions,  # Bind the response to the MCQQuestion Pydantic model
        )

        # Extract the generated questions from the response
        # Accessing the questions field directly from the ListOfMCQQuestions model
        list_of_questions = response.choices[0].message.parsed
        questions = list_of_questions.questions
        questions_list = [question.model_dump() for question in questions]
        print(questions_list)
        return questions_list

    except Exception as e:
        print(f"Error generating MCQs: {e}")
        return []
