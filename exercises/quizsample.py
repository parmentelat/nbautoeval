from nbautoeval import Quiz, QuizQuestion, Option, CodeOption, MathOption 

### 
# most basic single-answer

question_basic_single = QuizQuestion(
    "Pick the right fruit\n(one correct option)",
    options=[
        Option("banana"),
        Option("pear"),
        Option("apple", correct=True),
    ]
)
single_quiz = Quiz([question_basic_single])


questions = []
### 
question_basic_multiple = QuizQuestion(
    "Choose the right fruits<br>(several correct options)",
    options=[ 
        Option("apple", correct=True),
        Option("apricot", correct=True),
        Option("azur", correct=True),
        Option("banana"),
        Option("pear"),
        Option("pineapple"),
    ]
)
questions.append(question_basic_multiple)

question_unshuffle = QuizQuestion(
    "Choose the right fruits<br>not shuffled",
    options=[
        Option("apple", correct=True),
        Option("apricot", correct=True),
        Option("azur", correct=True),
        Option("banana"),
        Option("pear"),
        Option("pineapple"),
    ],
    shuffle=False,
)
questions.append(question_unshuffle)

### 
question_math = QuizQuestion(
    question="""Choose the right fruit
<br>only one correct answer
<br>but you don't want 
<br>to give that away""",
     options=[
        MathOption(r"some code and then double dollars $$\forall x\in\mathbb{R}$$"),
        MathOption(r"idem with single dollars $\forall x\in\mathbb{R}$"),
        MathOption(r"$\alpha = \beta^{p^k}$", correct=True),
        MathOption(r"$$\forall x_2\in\mathbb{R}, \alpha = \beta^{p^k}$$"),
        MathOption(r"$\forall x_1\in\mathbb{R}, \alpha = \beta^{p^k}$"),
    ],
)
questions.append(question_math)

# no correct answer
question_none = QuizQuestion(
    """It is possible that
no answer is valid""",
    options=[
        Option("banana"),
        Option("pear"),
    ]
)
questions.append(question_none)


# attempt to show code as options is currently broken
question_code = QuizQuestion(
    """code options should work
<br>on multiple-answers cases
<br>provided that <code>CodeOption</code> is used""",
    [
        CodeOption("a = sorted(x for x in list if x.is_valid())", correct=True),
        CodeOption("b = sort(x for x in list if x.is_valid())"),
    ]
)
questions.append(question_code)


question_vertical = QuizQuestion(
    """code options should work on multiple-answers cases
provided that CodeOption is used
this is to illustrate a vertical layout that could be a better fit in some cases""",
    [
        CodeOption("a = sorted(x for x in list if x.is_valid())", correct=True),
        CodeOption("b = sort(x for x in list if x.is_valid())"),
    ],
    vertical=True,
)
questions.append(question_vertical)


quiz = Quiz(questions)



# test_math = QuizQuestion(
#     """ideally options can contain math
# here again single-choice tests
# are problematic""",
#     [
#         MathOption(r"Some math and <i>HTML</i>: \(x^2\) and $$\frac{x+1}{x-1}$$", correct=True),
#         MathOption(r"\foreach x\in\mathbb{R}, \exists y, x^{y^2} = \pi"),
#     ],
#     multiple_answers=True,
# )
