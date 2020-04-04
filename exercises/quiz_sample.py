from nbautoeval import Quiz, QuizQuestion, Option, CodeOption, MathOption 
from nbautoeval import TextContent, MarkdownContent
questions1 = []
### 
question_basic_multiple = QuizQuestion(
    question="Choose the right fruits<br>(several correct options)",
    options=[ 
        Option("apple", correct=True),
        Option("apricot", correct=True),
        Option("azur", correct=True),
        Option("banana"),
        Option("pear"),
        Option("pineapple"),
    ],
    score = 2,
    horizontal_layout=True,
)
questions1.append(question_basic_multiple)

question_unshuffle = QuizQuestion(
    question="Choose the right fruits<br>not shuffled",
    options=[
        Option("apple", correct=True),
        Option("apricot", correct=True),
        Option("azur", correct=True),
        Option("banana"),
        Option("pear"),
        Option("pineapple"),
    ],
    shuffle=False,
    score = 4,
    horizontal_layout=True,
)
questions1.append(question_unshuffle)

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
        MathOption(r"multiple double dollars $$\forall x\in\mathbb{R}$$ $$\forall x\in\mathbb{R}$$ $$\forall x\in\mathbb{R}$$"),
    ],
    score = 8,
    horizontal_layout=True,
)
questions1.append(question_math)

# no correct answer
question_none = QuizQuestion(
    question="""At least one option must be correct""",
    options=[
        Option("banana"),
        Option("pear"),
        Option("none of the above", correct=True),
    ],
    # for now if we want to make sure the last option 
    # indeed appears last, we need to turn shuffle off
    shuffle = False,
    score = 16,
    horizontal_layout=True,
    horizontal_options=True,
)
questions1.append(question_none)

questions1.append(
    QuizQuestion(
question=MarkdownContent("""a question can be created with
<br>`exactly_one_answer=True`, in which case
<br>you get a radio buttons behaviour
<br>and the question has no ♧"""),
options=[
    Option("yes", correct=True),
    Option("no"),
    Option("don't know")
],
    exactly_one_option=True,
    horizontal_layout=True,
))



quiz1 = Quiz(
    exoname="quiz-sample-one",
    questions=questions1,
    max_attempts=3,
)

######

questions2 = []

# attempt to show code as options is currently broken
questions2.append(QuizQuestion(
    question="""code options should work
<br>on multiple-answers cases
<br>provided that <code>CodeOption</code> is used""",
    options=[
        CodeOption("a = sorted(x for x in list if x.is_valid())", correct=True),
        CodeOption("b = sort(x for x in list if x.is_valid())"),
    ],
    score = 32,
    horizontal_options=True,
))


question_vertical = QuizQuestion(
    question="""code options should work on multiple-answers cases
provided that <code>CodeOption</code> is used
this is to illustrate a vertical layout that could be a better fit in some cases""",
    options=[
        CodeOption("a = sorted(x for x in list if x.is_valid())", correct=True),
        CodeOption("b = sort(x for x in list if x.is_valid())"),
    ],
    score = 64,
)
questions2.append(question_vertical)


question_vertical_code = QuizQuestion(
    
    question="""we also need to be able to show large code fragments, 
    using <code>CodeOption</code> and multi-line code, and it feels like vertical 
    is what will best fit""",
    options=[
        CodeOption("""def multi(n, m):
    # comments should be fine
    x, y = some_fun(n, m)
    message = ("an input string that has multi-line"
               " pieces just for the fun of it")
    comprehension = [foo(z) for z in x]
    return sum(comprehension)**2"""),

        CodeOption("""# a correct answer that 
# badly looks like the other one but for the comment
def multi(n, m):
    # comments should be fine
    x, y = some_fun(n, m)
    message = ("an input string that has multi-line"
               " pieces just for the fun of it")
    comprehension = [foo(z) for z in x]
    return sum(comprehension)**2""", correct=True),

        CodeOption("b = sort(x for x in list if x.is_valid())"),
    ],
    score = 128,
)
questions2.append(question_vertical_code)

questions2.append(
    QuizQuestion(
question=MarkdownContent(
        """a *question* can be written in **markdown**, 
        with a `MarkdownContent` object."""),
options=[
    Option("yes", correct=True),
    Option("no"),
],
))


quiz2 = Quiz(
    exoname="quiz-sample-two",
    questions=questions2,
    max_attempts=3,
)
