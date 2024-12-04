# MCQ Generator for Exam Preparation

This Django-based application generates **Multiple Choice Questions (MCQs)** for exam preparation using **OpenAI API**. It is designed to create challenging, objective questions that test a user's understanding of a given content. The application also generates questions in **both English and Hindi (Devanagari)** to cater to diverse audiences.

## Key Features

- **Generate MCQs for Subunits**: Generate MCQs for a specific subunit or for all subunits within a unit. 
- **Dual Language Support**: Questions and options are provided in both **English** and **Hindi (Devanagari)**.
- **Comprehensive Coverage**: The questions are designed to cover the content holistically and are crafted to be challenging, reducing the chances of guessing the correct answer.
- **Django Integration**: This tool seamlessly integrates with a Django application, storing the generated questions and choices in a PostgreSQL database.

## Technologies Used

- **Django**: A high-level Python web framework used for backend development, including handling models and API endpoints.
- **OpenAI GPT-4 API**: Used to generate MCQs based on the given content, ensuring the questions are contextually relevant and well-crafted.
- **Pydantic**: Used to validate and parse the API responses in a structured format.
- **PostgreSQL**: The database for storing books, units, subunits, questions, and choices.
- **Python**: The primary programming language used in the backend for data handling and API integration.

## How It Works

1. **Content Input**: The user provides content for a book’s unit or subunit.
2. **MCQ Generation**: The content is passed to the OpenAI GPT-4 model, which generates **10 multiple-choice questions** for each subunit.
3. **Dual Language Output**: The questions and their choices are provided in both **English** and **Hindi (Devanagari)**. 
4. **Database Storage**: The questions and options are stored in the database for further use and analysis.

### Example Use Case

- **Book**: `Mathematics`
- **Unit**: `Algebra`
- **SubUnit**: `Linear Equations`

The system generates MCQs like:
1. **Question**: What is the solution to the equation \(2x + 5 = 15\)?
   - **Options**:
     1. x = 5
     2. x = 7
     3. x = 10
     4. x = 3
   - **Correct Answer**: x = 5
   - **In Hindi**: \(2x + 5 = 15\) समीकरण का हल क्या है?
     - **Options**:
       1. x = 5
       2. x = 7
       3. x = 10
       4. x = 3
   - **Correct Answer**: x = 5

### Example Output Format

```json
{
  "questions": [
    {
      "text_en": "What is the solution to the equation 2x + 5 = 15?",
      "text_hi": "समीकरण 2x + 5 = 15 का हल क्या है?",
      "choices": [
        {"text_en": "x = 5", "text_hi": "x = 5", "is_correct": true},
        {"text_en": "x = 7", "text_hi": "x = 7", "is_correct": false},
        {"text_en": "x = 10", "text_hi": "x = 10", "is_correct": false},
        {"text_en": "x = 3", "text_hi": "x = 3", "is_correct": false}
      ]
    }
  ]
}
