from nbautoeval import Quiz, QuizQuestion, Option, CodeOption, MathOption, MarkdownContent


############
quiz_extras = Quiz(

    # needs a unique name for storing progress and marks
    exoname="quiz-sample-extras",

    questions=[
        QuizQuestion(
            question=MarkdownContent("""
A question must have at least one correct option
<br> if no option is valid, then use
<br>`option_none` to provide 
<br> one artificial valid option"""),
            options=[
                Option('nope'),
                Option('neither'),
            ],  
            option_none = Option("none of the above", correct=True),
            horizontal_layout=True,
        ),

        QuizQuestion(
            question=MarkdownContent("""
Of course that artificial bullet is not always correct"""),
            options=[
                Option('a correct option'),
                Option('not right'),
            ],  
            option_none = Option("none of the above"),
            horizontal_layout=True,
        ),

        QuizQuestion(
            question=MarkdownContent("""
by default the questions in a Quiz are shuffled
so that each student gets them in a different order

same for options in a question btw; in both cases you can turn off
that feature by setting `shuffle=False` on the `QuizQuestion` or `Quiz` objects.

so for example this one is the last one in the present quiz.
"""),
            options=[
                Option("this will come out"),
                Option("in the right order"),
            ],
            shuffle=False,
        )
    ],
    max_attempts = 3,
    shuffle=False,
)
