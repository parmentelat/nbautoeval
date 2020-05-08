import random

from typing import List, Union
from enum import Enum

from ipywidgets import Layout, HBox, VBox, Checkbox, Button, HTML, HTMLMath

from .content import TextContent, MarkdownMathContent, CssContent
from .storage import log2_quiz, storage_read, storage_save
from .helpers import truncate

CSS = """
:root {
    /* these two are for unanswered */
    --question-bg-odd: #d6e4f0; 
    --question-bg-even: #ddebf8;
    --question-bg-right: #dafcf0;
    --question-bg-wrong: #ffd6d9;
    /* individual options after revealed */
    --option-wrong: #ff2e63;
    --explanation-right: #f8f8f8;
    --explanation-wrong: #f0f0f0;
    /* misc */
    --question-header-bg: white;
    --submit-bg: #c2f0fc;
    /* borders */
    --border-question: 2px solid #084177;
    --border-code: 1px solid #a0a0a0;
    --border-explanation: 1px solid #b0b0b0;
    --border-submit: 2px solid #084177;
}

.widget-vbox.nbae-question, .widget-hbox.nbae-question {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
}
.nbae-question .question {
    border: var(--border-question);
    border-radius: 6px;
    width: max-content;
    max-width: 100%;
    padding: 4px 8px;
    background-color: var(--question-header-bg);
}
/* question in a QuizQuestion with a vertical layout */
.nbae-question.widget-vbox>.question {
    width: 100%;
}

.nbae-question .index {
    font-weight: bold;
}

.nbae-question .question:not(.exactly-one) .question-header::after {
    content: "♧";
    align-self: center;
    font-weight: bold;
    font-size: 125%;
}
.nbae-question .question-header {
    border-bottom: 1px solid #084177;
}
.nbae-question .score::before {
    content: "|";
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
.nbae-question hr {
    height: 1px;
    background-color: #202020;
}
.nbae-question .code {
    border: var(--border-code);
}

.nbae-question .widget-checkbox {
    width: auto;
    padding-left: 10px;
}

.nbae-question .question-sequel {
    width: auto;
    margin-left: 10px;
    padding: 8px 10px;
    /*border: var(--border-question);*/
    background-color: var(--question-header-bg);
    border-radius: 6px;
}

.nbae-question.right, .nbae-quiz .summary.ok {
    background-color: var(--question-bg-right);
}
.nbae-question.wrong, .nbae-quiz .summary.ko {
    background-color: var(--question-bg-wrong);
}
.nbae-question.unanswered {
    background-color: var(--question-bg-odd);
}
.nbae-question.unanswered:nth-child(2n) {
    background-color: var(--question-bg-even);
}

.nbae-quiz .submit {
    margin: 10px;
    border-radius: 10px;
    background-color: var(--submit-bg);
    border: var(--border-submit);
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
    background-color: var(--option-wrong);
    border-radius: 6px;
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
    padding: 4px;
}
.nbae-question.unanswered span.unanswered {
    background-color: var(--question-bg-odd);
}
.nbae-question.unanswered:nth-child(2n) span.unanswered {
    background-color: var(--question-bg-even);
}
.nbae-question.right span.right {
    background-color: var(--question-bg-right);
}
.nbae-question.wrong span.wrong {
    background-color: var(--question-bg-wrong);
}
 
.nbae-question div.options>div.wrong-answer {
    margin-top: 8px;
}
.nbae-question div.options.widget-vbox>div {
    border-bottom: 0.8px solid #d0d0d0;
}
.nbae-question div.options.widget-hbox>div {
    border-right: 0.8px solid #d0d0d0;
}

.nbae-question .explanation::before {
    content: "☛";
    margin-right: 10px;
    font-size: 150%;
}
.nbae-question .explanation {
    border-radius: 6px;
    padding: 10px;
    background-color: var(--explanation-right);
    display: none;
    border: var(--border-explanation);
}

.nbae-question .wrong-answer .explanation {
    background-color: var(--explanation-wrong);
}

.nbae-question:not(.revealed) .explanation {
    display: none;
}
.nbae-question.revealed .explanation {
    display: inherit;
}
.nbae-question /*div.widget-html-content*/ pre {
    line-height: 1.2;
}
.nbae-question div.widget-html-content {
    line-height: 1.6;
}
.nbae-question div.option-box div {
    align-self: center;
}
"""

# unless specified otherwise in yaml
DEFAULT_CONTENT_CLASS = MarkdownMathContent


# a flexible content can be defined either with a plain str
# or with a Content object
FlexibleContent = Union[str, TextContent]

class Flexible:
    # it's important for the YAML loader that this parameter be called text
    def __init__(self, text: FlexibleContent):
        if isinstance(text, TextContent):
            self.content = text
        elif isinstance(text, str):
            self.content = DEFAULT_CONTENT_CLASS(text)
        else:
            raise ValueError(f"unexpected type {type(text).__name__}"
                             f" for flexible {text}")
    def widget(self):
        return self.content.widget()


class Explanation(Flexible):
    def widget(self):
        w = super().widget()
        return w.add_class('explanation') if w else None


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
    def __init__(self, text, explanation=None, **kwds):
        super().__init__(**kwds)
        self.text = text
        self.explanation = explanation
    def render(self):
        return TextContent(self.text)
    def explanation_widget(self):
        return None if not self.explanation else self.explanation.widget()
    

class CodeOption(Option):
    def render(self):
        return super().render().set_is_code(True).add_class('code')
    
class MathOption(Option):
    def render(self):
        return super().render().set_needs_math(True)
    
class MarkdownOption(Option):
    def render(self):
        return super().render().set_has_markdown(True)

class MarkdownMathOption(Option):
    def render(self):
        return super().render().set_has_markdown(True).set_needs_math(True)
    
DEFAULT_OPTION_CLASS = MarkdownMathOption


# this class captures the order in which options are provided
# in the QuizQuestion object     
class _TeacherOptions:
    def __init__(self, options: List[GenericBooleanOption]):
        self.options = options
    def append(self, option_none):
        self.options.append(option_none)
    def __iter__(self):
        return iter(self.options)
    

# this class captures the order in which options or questions 
# actually displayed, which is randomized from the input list
# (as defined in the YAML code) when shuffle is True
class _DisplayedItems:
    def __init__(self, input_list, shuffle):
        self.displayed = input_list[:]
        if shuffle:
            random.shuffle(self.displayed)
    def append(self, option_none):
        self.displayed.append(option_none)
    def __iter__(self):
        return iter(self.displayed)

class _DisplayedOptions(_DisplayedItems):
    def correct_indices(self):
        return [i for (i, opt) in enumerate(self.displayed) if opt.correct]

class _DisplayedQuestions(_DisplayedItems):
    pass



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
        # accept lists for the yaml loader
        ok_types = (tuple, list)
        if single_arg is None:
            pass
        elif isinstance(single_arg, int):
            self.if_right = single_arg
        elif isinstance(single_arg, ok_types) and len(single_arg) == 2:
            self.if_right, self.if_wrong = single_arg
        elif isinstance(single_arg, ok_types) and len(single_arg) == 3:
            self.if_right, self.if_wrong, self.if_unanswered = single_arg
        else:
            raise ValueError(f"Score constructor expects a single int\n"
                             f"or a {ok_types} of 2 or 3 ints")


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
    question can be a str, or a TextContent object for more complex inputs; 
    it may include html tags and/or math content between '$$'

    options is a list of Option objects; if exactly_one_option is set, 
    then obviously exactly one of these options must have correct=True
    (this needs to be explicit, an options list with one correct option 
    is not deemed enough a condition)
    when exactly_one_option is set, the checkboxes behave like radio buttons
    
    if option_none is provided, it should be an Option object, that will
    be guaranteed to appear last even when options are shuffled; it is designed
    so that a teacher can create a 'none of the above' option
    
    shuffle is a boolean indicating if the options must be shuffled 
    around for each student
    
    when horizontal_layout is set, the answers appear on the right of the question, 
    otherwise they appear below
    
    when horizontal_options is set, the answers are displayed in a horizontal box
    instead of a vertical one    
    """
    
    # constructor is kept as slight as possible for the yaml loader
    # in that context options is not yet a list of Options objects
    # but just plain Python dicts as outcome from yaml
    def __init__(self, *,
                 question: FlexibleContent,
                 options: List, 
                 # if defined, show up on top of the alternatives
                 question_sequel: FlexibleContent=None,
                 explanation=None, 
                 # do we want to shuffle the options
                 shuffle=True, 
                 # set this to True to mak it plain 
                 # that there is exactly one option to select
                 exactly_one_option=False,
                 option_none=None,
                 # how to display 
                 # for now, this is simple
                 score=1,
                 horizontal_layout=False,
                 horizontal_options=False):
        self.question = question
        self.options = options
        self.question_sequel = question_sequel
        self.explanation = explanation
        self.shuffle = shuffle
        self.exactly_one_option = exactly_one_option
        self._score_object = Score(score)
        self.horizontal_layout = horizontal_layout
        self.horizontal_options = horizontal_options
        self.option_none = option_none
        #
        self.feedback_area = None
        self._widget_instance = None
        # the rank in the Quiz object
        self.index = None
        # 
        self._post_inited = False
        

    # post-processing once options has been elaborated
    def post_init(self):
        if self._post_inited:
            return
        # shuffle if requested
        self._displayed_options = _DisplayedOptions(self.options, self.shuffle)
        # add 'none of the above' option as last option if requested
        if self.option_none is not None:
            self.options.append(self.option_none)
            self._displayed_options.append(self.option_none)
        self.sanity_check()
        self._post_inited = True
        

    def sanity_check(self):
        def report(*messages):
            print(f"**WARNING** : question `{truncate(str(self.question), 70)}`\n\t", *messages)
        nb_correct_options = len(self._displayed_options.correct_indices())
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
            return (Answer.RIGHT if set(selected) == set(self._displayed_options.correct_indices())
                    else Answer.WRONG)


    def score(self):
        return self._score_object.score(self.answer())
    def max_score(self):
        return self._score_object.if_right


    def widget(self):
        
        self.post_init()
        
        if self._widget_instance:
            return self._widget_instance
        
        # header area
        header_widget = HBox([
            HTML(f'Question # {self.index}').add_class('index'),
            HTML(f'{self._score_object.html()}').add_class('score')
        ]).add_class('question-header')
        question_widget = Flexible(self.question).widget()
        header_widgets = [header_widget, question_widget]
        if self.explanation:
            header_widgets.append(self.explanation.widget()) 
        question = VBox(header_widgets).add_class('question')
        if self.exactly_one_option:
            question.add_class('exactly-one')
        
        # the options per se    
        # it's important that we have as many checkboxes as option_boxes
        self.checkboxes = [Checkbox(value=option.selected, disabled=False,
                                    description='', indent=False)
                           for option in self._displayed_options]
        # radio-box behaviour
        if self.exactly_one_option:
            for checkbox in self.checkboxes:
                checkbox.observe(lambda event: self.radio_button_callback(event))
        labels = [option.render().widget() for option in self._displayed_options]
        
        # explanations contains, for each option, either a widget, or None
        explanations = [option.explanation_widget() 
                             for option in self._displayed_options]
        
        options_box = HBox if self.horizontal_options else VBox
        def make_option(checkbox, label, explanation):
            main = HBox([checkbox, label]).add_class('option-box')
            return (main if not explanation
                    else VBox([main, explanation]))
        self.option_boxes = [
            make_option(checkbox, label, explanation)
            for (checkbox, label, explanation) 
            in zip(self.checkboxes, labels, explanations)]
        if not self.question_sequel:
            actual_sons = self.option_boxes
        else:
            actual_sons = [Flexible(self.question_sequel).widget()
                           .add_class('question-sequel')]
            actual_sons += self.option_boxes
        options = options_box(actual_sons)
        options.add_class('options')

        css_widget = CssContent(CSS).widget()
        
        # putting it all together
        layout_box = HBox if self.horizontal_layout else VBox
        self._widget_instance = layout_box(
            [question, options, css_widget])
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
        for option, option_box, checkbox in zip(
            self._displayed_options, self.option_boxes, self.checkboxes):
            checkbox.disabled = True            
            # good answer ?
            if option.correct == checkbox.value:
                option_box.remove_class('wrong-answer')
            else:
                option_box.add_class('wrong-answer')
        self._widget_instance.add_class('revealed')


    def preserve(self) -> List[bool]:
        for option, checkbox in zip(self._displayed_options, self.checkboxes):
            option.selected = checkbox.value
        return [option.selected for option in self.options]
            
    def restore(self, bools: List[bool]):
        for option, boolean in zip(self.options, bools):
            option.selected = boolean
        if self._widget_instance:
            for checkbox, option in zip(self.checkboxes, self._displayed_options):
                checkbox.value = option.selected


class Quiz:
    """
    a quiz is made of several questions
    one can only submit a full Quiz, not just one question at a time
    """    
    
    # same approach to hyper-light constructor
    # the questions attribute might temporarily be a list of
    # plain Python objects, not QuizQuestion instances yet
    def __init__(self,
                 *,
                 exoname, 
                 questions: List[QuizQuestion], 
                 shuffle=True,
                 max_attempts=2,
                 max_grade=None):
        self.exoname = exoname
        self.questions = questions
        self.shuffle = shuffle
        self.max_attempts = max_attempts
        self.max_grade = max_grade
        
        # private - for updating the UI
        self.submit_button = None
        self.submit_summary = None
        #
        self._post_inited = False        


    def post_init(self):
        if self._post_inited:
            return
        # this is tricky and not quite right
        # we need to have the questions post-init'ed
        # this early because of the restoration below
        # otherwise questions won't have their option_none appended
        # and restore would fail to restore the option_none option
        for question in self.questions:
            question.post_init()
        self.displayed_questions = _DisplayedQuestions(self.questions, self.shuffle)
        # needs to be saved somewhere
        self.current_attempts = storage_read(self.exoname, 'current_attempts', 0)
        preserved = storage_read(self.exoname, "answers", [])
        if preserved: 
            self.restore(preserved)
        # set question rank
        for index, question in enumerate(self.displayed_questions, 1):
            question.set_index(index)
        self._post_inited = True


    def widget(self):
        self.post_init()
        sons = [question.widget() for question in self.displayed_questions]

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
        # because of possible load/network latency,
        #  we need to disable this until the event is processed
        # update() will re-enable it later on if needed
        self.submit_button.disabled = True
        self.update()
        storage_save(self.exoname, 'current_attempts', self.current_attempts)
        storage_save(self.exoname, "answers", self.preserve())
        (current_score, max_score,
         normalized_score, normalized_max_score) = self.total_score()
        log_kwds = {}
        if self.max_grade:
            log_kwds = dict(normalized_score=normalized_score,
                            normalized_max_score=normalized_max_score)
        log2_quiz(self.exoname, 
                  attempt=self.current_attempts, max_attempts=self.max_attempts,
                  score=current_score, max_score=max_score,
                  **log_kwds)


    def preserve(self) -> List[List[bool]]:
        return [question.preserve() for question in self.questions]
            
    def restore(self, list_of_list_of_bools):
        for question, list_of_bools in zip(self.questions, list_of_list_of_bools):
            question.restore(list_of_bools)


    def final_score_html(self):
        s, m, ns, nm = self.total_score()
        final = "final score "
        if self.max_grade is None:
            final += f"<span class='final'>{s}</span> / {points(m)}"
        else:
            final += f"{s} / {m}"
            final += f" = <span class='final'>{ns:.2f}</span> / {points(nm)}"
        return final
        

    def update(self):
        # there may be latency if the host is loaded
        self.answers = [question.answer() 
                        for question in self.displayed_questions]
        right_answers = [answer for answer in self.answers if answer == Answer.RIGHT]
        all_right = (len(right_answers) == len(self.answers))
        if all_right or self.current_attempts >= self.max_attempts:
            # materialize all questions
            for question in self.displayed_questions:
                question.feedback(question.answer())
                question.individual_feedback()
            # disable submit button
            self.submit_button.description = "quiz over"
            summary = self.final_score_html()
            if self.max_attempts > 1:
                summary += (f" ⎯⎯⎯ after {self.current_attempts}"
                            f" / {self.max_attempts} attempts")
            self.submit_summary.value = summary
            if all_right:
                self.submit_summary.add_class('ok')
            else:
                self.submit_summary.add_class('ko')
            # not really needed (it's been disable already in submit)
            # but for consistency
            self.submit_button.disabled = True
        else:
            # so here we know that self.current_attempts < self.max_attempts:
            left = self.max_attempts - self.current_attempts
            self.submit_button.description = (
                f"submit ({left}/{self.max_attempts} attempts left)")
            if self.current_attempts >= 1:
                self.submit_summary.value = (
                    f"{len(right_answers)}/{len(self.answers)} questions OK")
            self.submit_button.disabled = False

    def total_score(self):
        """
        returns a tuple current_score, max_score
        """
        current_score = sum(q.score() for q in self.questions)
        max_score = sum(q.max_score() for q in self.questions)
        if self.max_grade is not None:
            normalized_max_score = self.max_grade
            normalized_score = current_score/max_score * normalized_max_score
        else:
            normalized_max_score, normalized_score = max_score, current_score
        return current_score, max_score, normalized_score, normalized_max_score
