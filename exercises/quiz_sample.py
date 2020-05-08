#
# see also yaml/quiz-sample.yaml that builds the same quizzes
# but much more conveniently imho if you are ok with yaml
# if not - like me before I wrote this - 
# you may want to spend 10' learning YAML 
# thanks to this awesome and super effective tuto
# https://www.youtube.com/watch?v=cdLNKUoMc6c
#
from nbautoeval import TextContent, MarkdownContent, MathContent
from nbautoeval import Quiz, QuizQuestion, Option, CodeOption, MathOption, Explanation

### 
questions1 = []

questions1.append(
    QuizQuestion(
question=MarkdownContent(
        """a *question* can be written in **markdown**, 
        with a `MarkdownContent` object."""),
explanation=Explanation(MarkdownContent("""
There is no reason why a question could not be attached am explanation

#### level 4 title

markdown should **work** *out* `of` ***the box***; note however that ~~strike-through~~ 
does not seem to be supported
""")),
options=[
    Option("a correct option, with explanation", correct=True,
            explanation=Explanation("some words about why it is so")),
    Option("not right, with explanation",
           explanation=Explanation("some words about why it is not")),
],
))


questions1.append(
    QuizQuestion(
question=MarkdownContent("""a question can be created with
<br>`exactly_one_option=True`, in which case
<br>you get a radio buttons behaviour
<br>and the question has no ♧"""),
options=[
    Option("a yes", correct=True,
            explanation=Explanation(MarkdownContent("some words about why it is so"))),
    Option("no",
            explanation=Explanation(MathContent(r"$\forall x\in\mathbb{R}$"))),
    Option("don't know",
            explanation=Explanation("this question can only have one option selected")),
    ],
    exactly_one_option=True,
    horizontal_layout=True,
))

# questions can be phrased as a raw str as well
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
    question=MarkdownContent("""Easy math
<br>just use `MathOption`
<br>to create the options
"""),
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


quiz1 = Quiz(
    exoname="quiz-sample-one",
    questions=questions1,
    max_attempts=3,
    # shuffling can be disturbing for this intro
    shuffle=False,
)

######

questions2 = []

# attempt to show code as options is currently broken
questions2.append(QuizQuestion(
    question="""it is easy to create an option that contains
<br>code - and only code - with a <code>CodeOption</code> instance""",
    options=[
        CodeOption("a = sorted(x for x in list if x.is_valid())", correct=True),
        CodeOption("b = sort(x for x in list if x.is_valid())"),
    ],
    score = 32,
    horizontal_options=True,
))

questions2.append(QuizQuestion(
    question="""code options should work on multiple-answers cases
provided that <code>CodeOption</code> is used
this is to illustrate a vertical layout that could be a better fit in some cases""",
    options=[
        CodeOption("a = sorted(x for x in list if x.is_valid())", correct=True),
        CodeOption("b = sort(x for x in list if x.is_valid())"),
    ],
    score = 64,
))


questions2.append(QuizQuestion(
    
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
))

questions2.append(QuizQuestion(
    question="you can provide your own scale, here we want grades / 20",
    options = [
        Option("a yes", correct=True),
        Option("no"),
    ],
    exactly_one_option=True,
))

quiz2 = Quiz(
    exoname="quiz-sample-two",
    questions=questions2,
    # again, it's hard to write a tutorial quiz if shuffled
    shuffle=False,
    max_attempts=3,
    # we want a grade / 20
    max_grade=20,
)
