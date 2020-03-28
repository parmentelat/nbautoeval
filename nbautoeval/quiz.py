import random

from typing import List

from ipywidgets import Layout, HBox, VBox, Checkbox, Button, HTML, HTMLMath

from .content import Content, TextContent, CssContent
from .storage import log_quiz, storage_read, storage_save


"""
an Option instance represents one of the possible answers
by default it is a wrong answer
"""
class GenericBooleanOption:
    def __init__(self, *, correct=False):
        self.correct = correct
        self.selected = None
    def render(self):
        print(f"Option classes must implement render()")
        
        
class Option(GenericBooleanOption):
    def __init__(self, text, **kwds):
        super().__init__(**kwds)
        self.text = text
    def render(self):
        return TextContent(self.text)
    

class CodeOption(Option):
    def render(self):
        return super().render().set_is_code(True).add_class("code")
    
class MathOption(Option):
    def render(self):
        return super().render().set_needs_math(True)
    

     
class _OptionsList:
    def __init__(self, options: List[GenericBooleanOption]):
        self.options = options
    def __iter__(self):
        return iter(self.options)
    

# usually options are displayed in some random order
class _DisplayedOptionsList:
    def __init__(self, options: List[GenericBooleanOption], shuffle):
        self.displayed = options[:]
        if shuffle:
            random.shuffle(self.displayed)
    def correct_indices(self):
        return [i for (i, opt) in enumerate(self.displayed) if opt.correct]
    def __iter__(self):
        return iter(self.displayed)


CSS = """
.widget-vbox.nbae-question, .widget-hbox.nbae-question {
    padding: 10px;
    border-radius: 4px;
    background-color: #d1f5d3;
    border: 1px solid black;
}

.nbae-question .question {
    border: 2px solid #084177;
    border-radius: 4px;
    width: max-content;
    max-width: 100%;
    padding: 4px 8px;
}

.nbae-question .score::before, .nbae-question .score::after {
    content: "⁇";
    font-weight: bold;
    font-size: 125%;
}
.nbae-question .score::before {
    padding-right: 5px;
}
.nbae-question .score::after {
    padding-left: 5px;
}

.nbae-question .code pre {
    line-height: 1.3;
    padding: 5px;
}
.nbae-question .code {
    border: 1px solid #aaa;
}

.nbae-question .widget-checkbox {
    width: auto;
    padding-left: 10px;
}

.nbae-question.ok, .nbae-quiz .summary.ok {
    background-color: #d4f8e8;
}
.nbae-question.ko, .nbae-quiz .summary.ko {
    background-color: #ffd6d9;
}
.nbae-question.ok-ko {
    background-color: #f8f8f8;
}

.nbae-quiz .submit {
    margin: 10px 0px 0px 0px;
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
"""

def points(score):
    return f"{score} {'pt' if score<=1 else 'pts'}"



class QuizQuestion:
    """
    question may include html tags and/or math content between '$$'
    
    initially planned on supporting 2 flavours of selection
    * multiple_answers=False would mean to enforce exactly one answer
      i.e. using radio buttons to unselect any previously selected answer
      upon a user's click
    * multiple_answers=True would mean, user selects exactly how many
      options she wishes (including 0 btw)
    however, due to limitations with ipywidgets' RadioButtons that
    only takes plain text as options, for now we only have
    one mode which is multiple_answers=True
    """
    
    def __init__(self, question: str, options: List, 
                 *,
                 score = 1,
                 shuffle=True, 
                 horizontal_layout=False,
                 horizontal_options=False):
        self.question = question
        self.options_list = _OptionsList(options)
        self.displayed = _DisplayedOptionsList(options, shuffle)
        self.score = score
        self.horizontal_layout = horizontal_layout
        self.horizontal_options = horizontal_options
        self.feedback_area = None
        self._widget_instance = None
        

    def widget(self):
        
        if self._widget_instance:
            return self._widget_instance
    
        points_question = f'<div class="score">{points(self.score)}</div>{self.question}'

        question = HTMLMath(points_question)
        question.add_class('question')

        self.checkboxes = [Checkbox(value=option.selected, disabled=False, description='', indent=False)
                           for option in self.displayed]
        labels = [option.render().widget() for option in self.displayed]
        options_box = HBox if self.horizontal_options else VBox
        answers = options_box(
                  [HBox([checkbox, label]) 
                   for (checkbox, label) in zip(self.checkboxes, labels)])
        answers.add_class("answers")

        css_widget = CssContent(CSS).widget()
        
        layout_box = HBox if self.horizontal_layout else VBox
        self._widget_instance = layout_box(
            [question, answers, css_widget])
        self._widget_instance.add_class("nbae-question")
        self.feedback_area = self._widget_instance
        self.feedback(None)
        return self._widget_instance            


    def is_correct(self):
        selected = [i for (i, checkbox) in enumerate(self.checkboxes)
                    if checkbox.value]
        return set(selected) == set(self.displayed.correct_indices())


    def feedback(self, none_or_true_or_false):
        """
        assuming the widget was created already, of course
        """
        if self.feedback_area is None:
            return
        if none_or_true_or_false is None:
            on, offs = ("ok-ko", ["ok", "ko"])
        elif none_or_true_or_false is True:
            on, offs = ("ok", ["ok-ko", "ko"])
        else:
            on, offs = ("ko", ["ok", "ok-ko"])
        self.feedback_area.add_class(on)
        for off in offs:
            self.feedback_area.remove_class(off)


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
                 quiz_questions: List[QuizQuestion], 
                 max_attempts = 2):
        self.exoname = exoname
        self.quiz_questions = quiz_questions
        
        # needs to be saved somewhere
        self.max_attempts = max_attempts
        self.current_attempts = storage_read(self.exoname, 'current_attempts', 0)
        preserved = storage_read(self.exoname, "answers", [])
        if preserved: 
            self.restore(preserved)
            
        # for updates
        self.submit_button = None
        self.submit_summary = None


    def widget(self):
        sons = [question.widget() for question in self.quiz_questions]

        self.submit_button = Button(description='submit').add_class("submit")
        self.submit_summary = HTML('no result yet').add_class("summary")
        self.submit_button.on_click(lambda button: self.submit(button))
        sons.append(HBox([self.submit_button, self.submit_summary])
                    .add_class("result-area"))
        toplevel = VBox(sons).add_class("nbae-quiz")
        self.update()
        return toplevel

    
    def submit(self, _button):
        self.current_attempts += 1
        self.update()
        storage_save(self.exoname, 'current_attempts', self.current_attempts)
        storage_save(self.exoname, "answers", self.preserve())
        current_score, max_score = self.score()
        log_quiz(self.exoname, current_score, max_score)
        
        
        
    def preserve(self) -> List[List[bool]]:
        return [question.preserve() for question in self.quiz_questions]
            
    def restore(self, list_of_list_of_bools):
        for question, list_of_bools in zip(self.quiz_questions, list_of_list_of_bools):
            question.restore(list_of_bools)


    def update(self):        
        self.answers = [question.is_correct() 
                        for question in self.quiz_questions]
        self.right_answers = [answer for answer in self.answers if answer]
        if all(self.answers) or self.current_attempts >= self.max_attempts:
            # materialize all questions
            for question in self.quiz_questions:
                question.feedback(question.is_correct())
            # disable submit button
            self.submit_button.disabled = True
            self.submit_button.description = "quiz over"
            current_score, max_score = self.score()
            self.submit_summary.value = (
                f"final score {current_score} / {points(max_score)} "
                f" -- after {self.current_attempts} / {self.max_attempts} attempts"
            )
            if all(self.answers):
                self.submit_summary.add_class("ok")
            else:
                self.submit_summary.add_class("ko")
        else:
            # so here we know that self.current_attempts < self.max_attempts:
            left = self.max_attempts - self.current_attempts
            self.submit_button.description = (
                f"submit ({left}/{self.max_attempts} attempts left)")
            if self.current_attempts >= 1:
                self.submit_summary.value = (
                    f"{len(self.right_answers)}/{len(self.answers)} questions OK")

    def score(self):
        """
        returns a tuple current_score, max_score
        """
        current_score = sum(q.score for q in self.quiz_questions if q.is_correct())
        max_score = sum(q.score for q in self.quiz_questions)
        return current_score, max_score
