from pathlib import Path

# pip install PyYAML
import base64
import binascii
import yaml

# need to import them all here even when not explicitly used
# so that yaml code can refer to these classes
from .content import (TextContent, CodeContent, MathContent,
                      MarkdownContent, MarkdownMathContent)
from .quiz import (Quiz, QuizQuestion, Explanation,
                   Option, CodeOption, MathOption, MarkdownOption, MarkdownMathOption,
                   DEFAULT_OPTION_CLASS)


from .quiz import DEFAULT_CONTENT_CLASS

# quite straightforward, we build Python objects
# from a YAML regular Python object
# the purpose of object_from_dict to build
# is to create Python objects from the YAML (dict) data
# so the `type` field allows to chose the Python class name
#
#
# for more convenience some components in the Quiz structure
# may be entered as either a plain str, or a Content object
# example
# the-quiz:
#   type: Quiz
#   # one can either do
#   explanation: some text right here
#   # // or //
#   explanation:
#     type: MarkdownMathContent
#     text: |
#       here you have specified the content type
#
# this goes for
# . QuizQuestion.question            - the main question asked
# . QuizQuestion.question_sequel     - optional question follow-up
# . quizQuestion.option_none         - optional option object for 'none of the others'
# . QuizQuestion.explanation         - optional related explanation
# . all the QuizQuestion.option's              - the main text of the option
#   all the QuizQuestion.option.explanation's  - optional related explanation

class YamlLoader:

    """
    allows to parse a YAML file
    do some high-levels checks
    and build a Quiz object given its name
    """

    def __init__(self, filename_or_path):
        self.path = Path(filename_or_path)
        with self.path.open('rb') as feed:
            binary_content = feed.read()
        # first try, yaml-read as-is
        try:
            self.raw = yaml.safe_load(binary_content.decode(encoding="utf-8"))
            # somehow the exception does not always trigger
            # and in that case we receive a str
            if not isinstance(self.raw, dict):
                raise binascii.Error(None)
        except binascii.Error:
            self.raw = yaml.safe_load(base64.standard_b64decode(binary_content))
        except Exception:
            print(f"Cannot load quiz from yaml {self.path}")
            raise

    def iterate_on(self, typename):
        for name, item in self.raw.items():
            if 'type' in item and item['type'] == typename:
                yield name, item

    def check(self, boolean, message):
        if not boolean:
            raise ValueError(message)

    def rain_check(self):
        # at least one of each
        assert(list(self.iterate_on('Quiz')))
        questions = list(self.iterate_on('QuizQuestion'))
        assert(questions)

        for quizname, quiz in self.iterate_on('Quiz'):
            self.check('questions' in quiz, "Quiz must have questions")
            if isinstance(quiz['questions'], str):
                quiz['questions'] = quiz['questions'].split()
            for qname in quiz['questions']:
                if qname not in self.raw:
                    raise ValueError(
                        f"question named `{qname}` is used in "
                        f"quiz {quizname} "
                        f"but not found in YAML")

        # xxx
        # check for the class names used in the various _type fields

    # build (real instance) object from the
    # dictionary that comes out of yaml
    # opt_type_field_name is meant to allow the yaml desc. to
    # chose another class than the default
    # use opt_type_field_name=None if that's not a flexible option
    def object_from_dict(self, yaml_dict, default_class, opt_type_field_name):
        if not isinstance(yaml_dict, dict):
            print(f"WARNING: expecting a dict, got a {type(yaml_dict).__name__} "
                  f"object {yaml_dict} instead")
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
        # troubleshoot - we have no line number to offer, so
        # try to be helpful so users can pinpoint their mistake
        if self.debug:
            if cls.__name__ == 'QuizQuestion':
                print(f"building a {cls.__name__} : "
                      f"question={args['question'].text[:20]}...")
            elif 'Option' in cls.__name__:
                print(f"building a {cls.__name__} : "
                      f"text={args['text'][:20]}...")
            elif self.debug == 2:
                print(f"building a {cls.__name__} from "
                      f"attributes {list(args.keys())}")
        # what remains is passed as parameters to the constructor
        return cls(**args)

    def flexible_object(self, str_or_dict, cls):
        if isinstance(str_or_dict, str):
            return cls(str_or_dict)
        elif isinstance(str_or_dict, dict):
            return self.object_from_dict(str_or_dict, cls, "type")
        else:
            raise TypeError(f"expecting str or dict, "
                            f"got {type(str_or_dict.__name__)} {str_or_dict}")

    # recursively browse a yaml structure to apply the transformation to objects
    # logic is depth-first scan, and when coming back up apply any additional
    # change
    def process(self, yaml_dict):
        if not isinstance(yaml_dict, dict):
            return yaml_dict
        for k, v in yaml_dict.items():
            if isinstance(v, dict):
                self.process(v)
            elif isinstance(v, list):
                yaml_dict[k] = [self.process(x) for x in v]
            if k == 'explanation':
                # try this
                explanation = self.flexible_object(v, Explanation)
                # but if there was a type specified we still need the Explanation
                if not isinstance(explanation, Explanation):
                    explanation = Explanation(explanation)
                yaml_dict[k] = explanation
            elif k in ('question', 'question_sequel'):
                yaml_dict[k] = self.flexible_object(v, DEFAULT_CONTENT_CLASS)
            elif k in ('option_none'):
                yaml_dict[k] = self.flexible_object(v, DEFAULT_OPTION_CLASS)
            elif k in ('options'):
                yaml_dict[k] = [
                    self.flexible_object(opt, DEFAULT_OPTION_CLASS)
                    for opt in v
                ]
            elif k in ('questions'):
                yaml_dict[k] = [
                    self.object_from_dict(self.process(q), QuizQuestion, 'type')
                    for q in v
                ]
            elif isinstance(v, dict) and 'type' in v:
                yaml_dict[k] = self.object_from_dict(v, None, 'type')
        return yaml_dict


    def build_quiz(self, exoname, debug):
        import pdb
        # pdb.set_trace()
        self.debug = debug
        # first make sure the exoname makes sense
        self.check(exoname in self.raw, f"quiz {exoname} not found")
        yaml_quiz = self.raw[exoname]

        # stage1 on questions: build QuizQuestion instances
        processed_questions = {
            name: self.object_from_dict(self.process(yaml_question), QuizQuestion, None)
            for (name, yaml_question) in self.iterate_on('QuizQuestion')
        }
        """
        for qname, question in processed_questions.items():
            print(f"question {qname} -> {question}")
            break
        """

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

#
# a little salt to make it not completey obvious
# how to cheat by looking into the quiz source
# typically using $HOME/.yaml to store source might be
# a good idea
# typically search {radical}, {radical}.yaml {radical}.yml
# in the following dirs (if under HOME)
# .  ./yaml  ./.yaml
# .. ../yaml ../.yaml
# ../.. ../../yaml ../../.yaml
# HOME HOME/yaml HOME/.yaml
#
def locate_from_radical(filename_or_path, debug):

    # skip heuristics if its an existing filename
    checking = Path(filename_or_path)
    if checking.exists():
        return checking
    if checking.is_absolute():
        if debug:
            print(f"cannot use absolute but non existing path {filename_or_path}")
        return None

    # if provided a relative path, use only basename
    radical = checking.parts[-1]

    def is_under(root, potential_subdir):
        return root in potential_subdir.parents

    home = Path.home()
    # main locations where to start searching
    anchors = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd().parent.parent,
        Path.home()
    ]
    # the subdirs where to search from the anchors
    def iter_derivatives(path):
        yield path
        yield path / "yaml"
        yield path / ".yaml"
        yield path / ".quiz"

    # possible extensions added to the radical
    extensions = ["", ".yaml", ".yml", ".yamlb" ]

    # search it
    anchors = [ path for path in anchors if is_under(home, path) ]

    paths = [ d for path in anchors for d in iter_derivatives(path)]

    failed = []
    for path in paths:
        for extension in extensions:
            candidate = path / (radical + extension)
            if candidate.exists():
                return candidate
            elif debug:
                failed.append(candidate)

    print(f"could not spot quiz {filename_or_path}")
    if debug:
        for candidate in failed:
            print(f"have tried {candidate}")


def run_yaml_quiz(filename_or_path, exoname, debug=False):
    """
    one-liner convenience helper function, and main entry point

    in a single pass:
    * locate quiz from just its name, see heuristics above
    * parse the file (or Path)
    * build a Quiz object corresponding to exoname
    * create and return widget

    use debug=True until you get the YAML file right
    """

    actual_path = locate_from_radical(filename_or_path, debug)
    if not actual_path:
        raise ValueError(f"could not spot quiz {filename_or_path}")

    try:
        loader = YamlLoader(actual_path)
        loader.rain_check()
        return loader.build_quiz(exoname, debug).widget()
    except yaml.parser.ParserError as exc:
        print(f"Could not parse {filename_or_path}\n{exc}")
    except Exception as exc:
        print(f"OOPS - something wrong with quiz {type(exc)}, {exc}")
        debug = True
        if debug:
            import traceback
            print(traceback.format_exc())
        return exc
