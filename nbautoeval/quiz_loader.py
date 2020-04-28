from pathlib import Path

# pip install PyYAML
import yaml

from .content import TextContent, MarkdownContent, CodeContent, CssContent
from .quiz import (
    Option, CodeOption, MathOption, MarkdownOption,
    QuizQuestion, Quiz,
)

class YamlLoader:
    
    """
    allows to parse a YAML file
    do some high-levels checks
    and build a Quiz object given its name
    """
    
    def __init__(self, filename_or_path):
        self.path = Path(filename_or_path)
        # self.raw is the yaml content as-is
        with self.path.open() as feed:
            self.raw = yaml.safe_load(feed.read())
        
    def iterate_on(self, typename):
        for name, item in self.raw.items():
            if 'type' in item and item['type'] == typename:
                yield name, item

    def rain_check(self):
        # at least one of each
        assert(list(self.iterate_on('Quiz')))
        questions = list(self.iterate_on('QuizQuestion'))
        assert(questions)
        
        for _, quiz in self.iterate_on('Quiz'):
            for qname in quiz['questions']:
                assert qname in self.raw
        # xxx 
        # check for the class names used in the various _type fields

    # build (real instance) object from the 
    # dictionary that comes out of yaml
    # opt_type_field_name is meant to allow the yaml desc. to
    # chose another class than the default
    # use opt_type_field_name=None if that's not a flexible option
    def object_from_dict(self, yaml_dict, default_class, opt_type_field_name):
        args = yaml_dict.copy()
        cls = default_class
        if opt_type_field_name in args:
            # locate class
            cls = globals()[args[opt_type_field_name]]
            del args[opt_type_field_name]
        # the 'type' attribute is to be removed throughout
        # not only when opt_type_field_name == 'type'
        if 'type' in args:
            del args['type']
        # what remains is passed as parameters to the constructor
        if self.debug:
            print(f"building a {cls.__name__} instance, attributes {list(args.keys())}")
        return cls(**args)

    def build_quiz(self, exoname, debug):
        self.debug = debug
        # first make sure the exoname makes sense
        yaml_quiz = self.raw[exoname]
        
        # stage1 on questions: build QuizQuestion instances
        processed_questions = {
            name: self.object_from_dict(
                yaml_question, QuizQuestion, None)
            for name, yaml_question in self.iterate_on('QuizQuestion')
        }
        for question in processed_questions.values():
            # stage2: post-process 'question' and 'question2' 
            # attributes
            for attribute in ('question', 'question2'):
                if getattr(question, attribute):
                    setattr(question, attribute,
                            self.object_from_dict(
                                getattr(question, attribute),
                                MarkdownContent,
                                "type"
                            ))
            # also process the options attribute
            question.options = [self.object_from_dict(
                option, MarkdownOption, "type"
            ) for option in question.options]
            # and option_none if present
            if question.option_none:
                question.option_none = self.object_from_dict(
                    question.option_none, MarkdownOption, "type")
        
        # artificially inject exoname from YAML id
        if 'exoname' not in yaml_quiz:
            yaml_quiz['exoname'] = exoname
        quiz = self.object_from_dict(
            # quiz_type not yet used but well
            yaml_quiz, Quiz, "type")
        quiz.questions = [
            processed_questions[qname] for qname in quiz.questions
        ]

        return quiz            
        
            
    
def run_yaml_quiz(filename_or_path, exoname, debug=False):
    """
    one-liner convenience helper function, and main entry point

    in a single pass:
    * parse the file (or Path)
    * build a Quiz object corresponding to exoname
    * create and return widget
    
    use debug=True until you get the YAML file right
    """
    try:
        loader = YamlLoader(filename_or_path)
        loader.rain_check()
        return loader.build_quiz(exoname, debug).widget()
    except yaml.parser.ParserError as exc:
        print(f"Could not parse {filename_or_path}\n{exc}")
    except Exception as exc:
        print(f"OOPS - something wrong with quiz {type(exc)}, {exc}")
        import traceback
        print(traceback.format_exc())
        return exc
