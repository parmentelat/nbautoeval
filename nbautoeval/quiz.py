import random

from typing import List, Union
from enum import Enum

from ipywidgets import Layout, HBox, VBox, Checkbox, Button, HTML, HTMLMath

from .content import Content, TextContent, CssContent
from .storage import log_quiz, storage_read, storage_save
from .helpers import truncate

CSS = """
.widget-vbox.nbae-question, .widget-hbox.nbae-question {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
}
.nbae-question .question {
    border: 2px solid #084177;
    border-radius: 4px;
    width: max-content;
    max-width: 100%;
    padding: 4px 8px;
}
/* question in a QuizQuestion with a vertical layout */
.nbae-question.widget-vbox>.question {
    width: 100%;
}

.nbae-question .index {
    font-weight: bold;
}

.nbae-question .question:not(.exactly-one) .header::after {
    content: "♧";
    align-self: center;
    font-weight: bold;
    font-size: 125%;
}
.nbae-question .score::before {
    content: "⎯⎯";
    align-self: center;
    margin-right: 10px;
}
.nbae-question .score {
    margin-left: 10px;
    margin-right: 10px;
}

.nbae-question .code pre {
    line-height: 1.3;
    padding: 5px;
}
.nbae-question .code {
    border: 1px solid #aaa;
}

.nbae-question .widget-checkbox, .nbae-question .question2 {
    width: auto;
    padding-left: 10px;
}

.nbae-question.right, .nbae-quiz .summary.ok {
    background-color: #d4f8e8;
}
.nbae-question.wrong, .nbae-quiz .summary.ko {
    background-color: #ffd6d9;
}
.nbae-question.unanswered {
    background-color: #f0f0f0;
}
.nbae-question.unanswered:nth-child(2n) {
    background-color: #e8e8e8;
}

.nbae-quiz .submit {
    margin: 10px;
    border-radius: 10px;
    background-color: #c2f0fc;
    border: 2px solid #084177;
    width: max-content;
}

.nbae-quiz .result-area {
    align-items: center;
}

.nbae-quiz .summary {
    padding: 5px 20px;
    width: fit-content;
}

.nbae-quiz .wrong-answer {
    background-color: #ff2e63;
}

.nbae-quiz .final {
    font-weight: bold;
    font-size: larger;
    padding-left: 6px;
    padding-right: 6px;
}

.nbae-question.unanswered span.unanswered,
.nbae-question.right span.right,
.nbae-question.wrong span.wrong {
    font-weight: bold;
    font-size: larger;    
}
"""



class GenericBooleanOption:
    """
    an Option instance represents one of the possible answers
    by default it is not a correct answer
    """
    def __init__(self, *, correct=False):
        self.correct = correct
        self.selected = None
    def render(self):
        print(f"Option classes must implement render()")
        
        
class Option(GenericBooleanOption):
    """
    the most basic kind of Option allows to enter a simple text
    see more specialized classes for other kinds of inputs, 
    like CodeOption, MathOption and MarkdownOption

    correct=True should be set on options that are valid and 
    that students should check as such
    
    """
    def __init__(self, text, **kwds):
        super().__init__(**kwds)
        self.text = text
    def render(self):
        return TextContent(self.text)
    

class CodeOption(Option):
    def render(self):
        return super().render().set_is_code(True).add_class('code')
    
class MathOption(Option):
    def render(self):
        return super().render().set_needs_math(True)
    
class MarkdownOption(Option):
    def render(self):
        return super().render().set_has_markdown(True)


# this class captures the order in which options are provided
# in the QuizQuestion object     
class _OptionsList:
    def __init__(self, options: List[GenericBooleanOption]):
        self.options = options
    def __iter__(self):
        return iter(self.options)
    

# this class captures the order in which options are 
# actually displayed, which is randomized from _OptionsList 
# when shuffle is True
class _DisplayedOptionsList:
    def __init__(self, options: List[GenericBooleanOption], shuffle):
        self.displayed = options[:]
        if shuffle:
            random.shuffle(self.displayed)
    def correct_indices(self):
        return [i for (i, opt) in enumerate(self.displayed) if opt.correct]
    def __iter__(self):
        return iter(self.displayed)


# one can define a question from a plain str or a Content object
QuestionType = Union[str, Content]
def question_to_widget(question: QuestionType):
    if isinstance(question, Content):
        return question.widget()
    else:
        return HTMLMath(question)
    

class Answer(Enum):
    UNANSWERED = -1
    WRONG = 0
    RIGHT = 1


def points(score):
    return f"{score} {'pt' if score<=1 else 'pts'}"

# to allow for QuizQuestion(... score=1)
# or           QuizQuestion(... score=(6, -1))
# or           QuizQuestion(... score=(6, -3, 1))
class Score:
    # in points
    def __init__(self, single_arg=None):
        self.if_right = 1
        self.if_wrong = -1
        self.if_unanswered = 0
        if single_arg is None:
            pass
        elif isinstance(single_arg, int):
            self.if_right = single_arg
        elif isinstance(single_arg, tuple) and len(single_arg) == 2:
            self.if_right, self.if_wrong = single_arg
        elif isinstance(single_arg, tuple) and len(single_arg) == 3:
            self.if_right, self.if_wrong, self.if_unanswered = single_arg
        else:
            raise ValueError("Score constructor expects an int or a tuple of 2/3 ints")


    def score(self, answer):
        return (self.if_right if answer == Answer.RIGHT
                else self.if_wrong if answer == Answer.WRONG
                else self.if_unanswered)

    def html(self):
        return (f"<span class='right'>{points(self.if_right)}</span>"
                f" / <span class='wrong'>{points(self.if_wrong)}</span>"
                f" / <span class='unanswered'>{points(self.if_unanswered)}</span>")
    def __str__(self):
        return f"{self.if_right}/{self.if_wrong}/{self.if_unanswered}"
        

class QuizQuestion:
    """
    question can be a str, or a Content object for more complex inputs; 
    it may include html tags and/or math content between '$$'

    options is a list of Option objects; if exactly_one_option is set, 
    then obviously exactly one of these options must have correct=True
    (this needs to be explicit, an options list with one correct option 
    is not deemed enough a condition)
    when exactly_one_option is set, the checkboxes behave like radio buttons
    
    shuffle is a boolean indicating if the options must be shuffled 
    around for each student
    
    when horizontal_layout is set, the answers appear on the right of the question, 
    otherwise they appear below
    
    when horizontal_options is set, the answers are displayed in a horizontal box
    instead of a vertical one    
    """
    
    def __init__(self, *,
                 question: QuestionType,
                 options: List, 
                 # if defined, show up on top of the alternatives
                 question2: str=None,
                 # do we want to shuffle the options
                 shuffle=True, 
                 # set this to True to mak it plain 
                 # that there is exactly one option to select
                 exactly_one_option = False,
                 # how to display 
                 # for now, this is simple
                 score = 1,
                 horizontal_layout=False,
                 horizontal_options=False):
        self.question = question
        self.options_list = _OptionsList(options)
        self.question2 = question2
        self.displayed = _DisplayedOptionsList(options, shuffle)
        self.exactly_one_option = exactly_one_option
        self._score_object = Score(score)
        self.horizontal_layout = horizontal_layout
        self.horizontal_options = horizontal_options
        self.feedback_area = None
        self._widget_instance = None
        # the rank in the Quiz object
        self.index = None
        self.sanity_check()
        

    def sanity_check(self):
        def report(*messages):
            print(f"question {truncate(str(self.question), 70)}\n\t", *messages)
        nb_correct_options = len(self.displayed.correct_indices())
        if self.exactly_one_option:
            if  nb_correct_options != 1:
                report(f"has {nb_correct_options} correct answers, expected 1 b/c exactly_one_option")
        else:
            if  nb_correct_options == 0:
                report(f"has no correct answers, this is not supported,\n"
                       f"\tplease add an option like 'none of the other answers'")

        
    def set_index(self, index):
        self.index = index


    def answer(self):
        selected = [i for (i, checkbox) in enumerate(self.checkboxes)
                    if checkbox.value]
        if not selected:
            return Answer.UNANSWERED
        else:
            return (Answer.RIGHT if set(selected) == set(self.displayed.correct_indices())
                    else Answer.WRONG)


    def score(self):
        return self._score_object.score(self.answer())
    def max_score(self):
        return self._score_object.if_right


    def widget(self):
        
        if self._widget_instance:
            return self._widget_instance
        
        header_widget = HBox([
            HTML(f'Question # {self.index}').add_class('index'),
            HTML(f'{self._score_object.html()}').add_class('score')
        ]).add_class('header')
        question_widget = question_to_widget(self.question)
        question = VBox([header_widget,
                         question_widget]).add_class('question')
        if self.exactly_one_option:
            question.add_class('exactly-one')
            
        # it's important that we have as many checkboxes as option_boxes
        self.checkboxes = [Checkbox(value=option.selected, disabled=False, description='', indent=False)
                           for option in self.displayed]
        if self.exactly_one_option:
            for checkbox in self.checkboxes:
                checkbox.observe(lambda event: self.radio_button_callback(event))
        labels = [option.render().widget() for option in self.displayed]
        options_box = HBox if self.horizontal_options else VBox
        self.option_boxes = [HBox([checkbox, label]) 
                             for (checkbox, label) in zip(self.checkboxes, labels)]
        if not self.question2:
            actual_sons = self.option_boxes
        else:
            actual_sons = [question_to_widget(self.question2).add_class('question2')]
            actual_sons += self.option_boxes
        answers = options_box(actual_sons)
        answers.add_class('answers')

        css_widget = CssContent(CSS).widget()
        
        layout_box = HBox if self.horizontal_layout else VBox
        self._widget_instance = layout_box(
            [question, answers, css_widget])
        self._widget_instance.add_class('nbae-question')
        self.feedback_area = self._widget_instance
        self.feedback(Answer.UNANSWERED)
        return self._widget_instance            


    # this will be bound to the checkbox widgets through observe()
    # which passes along an event object 
    def radio_button_callback(self, event):
        # only interested in that sort of events
        if event['name'] != 'value':
            return
        # locate the checkbox that is being changed
        checkbox = event['owner']
        # we only react on changes that set value=True
        if checkbox.value == False:
            return
        if checkbox not in self.checkboxes:
            print("WHOOPS - s/t wrong !")
            return
        for other in self.checkboxes:
            if other is not checkbox:
                other.value = False
        

    def feedback(self, answer: Answer):
        """
        assuming the widget was created already, of course
        """
        if self.feedback_area is None:
            return
        if answer == Answer.UNANSWERED:
            on, offs = ('unanswered', ['right', 'wrong'])
        elif answer == Answer.RIGHT:
            on, offs = ('right', ['unanswered', 'wrong'])
        else:
            on, offs = ('wrong', ['right', 'unanswered'])
        self.feedback_area.add_class(on)
        for off in offs:
            self.feedback_area.remove_class(off)


    def individual_feedback(self):
        for option, checkbox, option_box in zip(
            self.displayed, self.checkboxes, self.option_boxes):
            checkbox.disabled = True            
            # good answer ?
            if option.correct == checkbox.value:
                option_box.remove_class('wrong-answer')
            else:
                option_box.add_class('wrong-answer')


    def preserve(self) -> List[bool]:
        for option, checkbox in zip(self.displayed, self.checkboxes):
            option.selected = checkbox.value
        return [option.selected for option in self.options_list]
            
    def restore(self, bools: List[bool]):
        for option, boolean in zip(self.options_list, bools):
            option.selected = boolean
        if self._widget_instance:
            for checkbox, option in zip(self.checkboxes, self.displayed):
                checkbox.value = option.selected


class Quiz:
    """
    a quiz is made of several questions
    one can only submit a full Quiz, not just one question at a time
    """    
    
    def __init__(self,
                 exoname, 
                 *,
                 questions: List[QuizQuestion], 
                 max_attempts = 2):
        self.exoname = exoname
        self.quiz_questions = questions
        
        # needs to be saved somewhere
        self.max_attempts = max_attempts
        self.current_attempts = storage_read(self.exoname, 'current_attempts', 0)
        preserved = storage_read(self.exoname, "answers", [])
        if preserved: 
            self.restore(preserved)
            
        # for updates
        self.submit_button = None
        self.submit_summary = None
        
        # set question rank
        for index, question in enumerate(self.quiz_questions, 1):
            question.set_index(index)


    def widget(self):
        sons = [question.widget() for question in self.quiz_questions]

        self.submit_button = Button(description='submit').add_class('submit')
        self.submit_summary = HTML('no result yet').add_class('summary')
        self.submit_button.on_click(lambda button: self.submit(button))
        sons.append(HBox([self.submit_button, self.submit_summary])
                    .add_class('result-area'))
        toplevel = VBox(sons).add_class('nbae-quiz')
        self.update()
        return toplevel

    
    def submit(self, _button):
        self.current_attempts += 1
        self.update()
        storage_save(self.exoname, 'current_attempts', self.current_attempts)
        storage_save(self.exoname, "answers", self.preserve())
        current_score, max_score = self.total_score()
        log_quiz(self.exoname, current_score, max_score)
        
        
        
    def preserve(self) -> List[List[bool]]:
        return [question.preserve() for question in self.quiz_questions]
            
    def restore(self, list_of_list_of_bools):
        for question, list_of_bools in zip(self.quiz_questions, list_of_list_of_bools):
            question.restore(list_of_bools)


    def update(self):
        self.answers = [question.answer() 
                        for question in self.quiz_questions]
        right_answers = [answer for answer in self.answers if answer == Answer.RIGHT]
        all_right = (len(right_answers) == len(self.answers))
        if all_right or self.current_attempts >= self.max_attempts:
            # materialize all questions
            for question in self.quiz_questions:
                question.feedback(question.answer())
                question.individual_feedback()
            # disable submit button
            self.submit_button.disabled = True
            self.submit_button.description = "quiz over"
            current_score, max_score = self.total_score()
            self.submit_summary.value = (
                f"final score <span class='final'>{current_score}</span> / {points(max_score)} "
                f" ⎯⎯⎯ after {self.current_attempts} / {self.max_attempts} attempts"
            )
            if all_right:
                self.submit_summary.add_class('ok')
            else:
                self.submit_summary.add_class('ko')
        else:
            # so here we know that self.current_attempts < self.max_attempts:
            left = self.max_attempts - self.current_attempts
            self.submit_button.description = (
                f"submit ({left}/{self.max_attempts} attempts left)")
            if self.current_attempts >= 1:
                self.submit_summary.value = (
                    f"{len(right_answers)}/{len(self.answers)} questions OK")

    def total_score(self):
        """
        returns a tuple current_score, max_score
        """
        current_score = sum(q.score() for q in self.quiz_questions)
        max_score = sum(q.max_score() for q in self.quiz_questions)
        return current_score, max_score
