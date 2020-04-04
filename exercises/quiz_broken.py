from nbautoeval import Quiz, QuizQuestion, Option, CodeOption, MathOption 
from nbautoeval import TextContent, MarkdownContent

### 
questions = [
    QuizQuestion(
        question="should be fine",
        options=[
            Option("yes1", correct=True),
            Option("yes2", correct=True),
            Option("no1"),
            Option("no2"),
        ],
    ),
    QuizQuestion(
        question="broken because 2 options and exactly_one_option",
        options=[
            Option("yes1", correct=True),
            Option("yes2", correct=True),
            Option("no1"),
            Option("no2"),
        ],
        exactly_one_option=True,
    ),
    QuizQuestion(
        question="broken because no correct option", 
        options=[
            Option("no1"),
            Option("no2"),
        ],
    ),
    QuizQuestion(
        question="broken too, has no correct option, and exactly_one_option on top", 
        options=[
            Option("no1"),
            Option("no2"),
        ],
        exactly_one_option=True,
    ),
]

broken_quiz = Quiz(
    exoname="quiz-broken",
    questions=questions,
    max_attempts=1,
)
