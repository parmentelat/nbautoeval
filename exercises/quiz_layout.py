from nbautoeval import Quiz, QuizQuestion, Option, CodeOption, MathOption, MarkdownContent


############
quiz_horizontal = Quiz(

    # needs a unique name for storing progress and marks
    exoname="quiz-sample-horizontal",

    questions=[
        QuizQuestion(
            question=MarkdownContent("""
`horizontal_layout=True` means to have the question
<br> and the options appear side by side (in a horizontal box)"""),
            options=[
                Option('<img src="../media/image1.png">', correct=True),
                Option('<img src="../media/image2.png" width="250px">'),
            ],  
            horizontal_layout=True,
        ),


        QuizQuestion(question=MarkdownContent("""
`horizontal_options` means the options appear side by side like here,
because `horizontal_layout` is `False`, the question spans 100% of the page width
"""),
            options=[
                Option('<img src="../media/image1.png">', correct=True),
                Option('<img src="../media/image2.png" width="250px">'),
            ],  
            horizontal_options=True,
        ),
        

        QuizQuestion(question="""
the default is to have none of these 2 horizontal flags 
""",
            options=[
                Option('<img src="../media/image1.png">', correct=True),
                Option('<img src="../media/image2.png" width="250px">'),
            ],  
        ),
        
        QuizQuestion(question="""
of course they can be used together as well""",
            options=[
                Option('<img src="../media/image1.png">', correct=True),
                Option('<img src="../media/image2.png" width="250px">'),
            ],  
            horizontal_layout=True,
            horizontal_options=True,
        ),
        

    ],
    max_attempts = 3,
    )

# this is demonstrate some quizzes that have something wrong
broken_quiz1 = Quiz(
    "broken-quiz-1",
    
)
