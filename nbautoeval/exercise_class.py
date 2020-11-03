# -*- coding: utf-8 -*-

# pylint: disable=c0111, c0103, r1705, w0703

from ipywidgets import GridBox, Layout

from .args import Args
from .content import TextContent, CssContent, ResultContent
from .callrenderer import Call, CallRenderer
from .renderer import Renderer
from .helpers import default_font_size, default_header_font_size
from .storage import log_correction, log2_correction


DEBUG = False
#DEBUG = True


default_column_headers = (
    "scénario {n}", 
    "appel",
    "attendu",
    "obtenu",
)
# same order
column_span_classes = (
    ["span-1-to-4", "scenario"], [], [], ["span-3-to-4"],
)
# simpler in example mode
example_column_span_classes = (
    ["span-1-to-2", "scenario"], [], [],
)

###
CSS = """
.nbae-cls {
    width: max-content;
/*    border-top: .1em solid black;  */
    border-bottom: .1em solid black;
    padding: 0.1em 0em;
    row-gap: 0.4em;
    column-gap: .4em;
}
.nbae-cls .header {
    padding: 0em 0em 0.3em 0em;
    background-color: #f1fcfc;
    border-bottom: .1em solid #888;
    font-weight: bold;
    border-top-left-radius: .4em;
    border-top-right-radius: .4em;
}
.nbae-cls .header > .widget-html-content {
    justify-content: center;
}

.nbae-cls .scenario.header {
    padding: 0.3em 0em 0em 0em; 
    border-bottom: none;
    border-top: 3px solid darkcyan;
}
.nbae-cls .span-1-to-4 {
    grid-column: 1 / span 4;
}
.nbae-cls .span-3-to-4 {
    grid-column: 3 / span 2;
}
.nbae-cls .span-2-to-3 {
    grid-column: 2 / span 2;
}
.nbae-cls .span-1-to-2 {
    grid-column: 1 / span 2;
}
div.nbae-cls div.widget-html-content pre {
    padding: 0px;
    line-height: 1.15;
}
.nbae-cls .ok, .nbae-cls .ok code {
    background-color: #d4f8e8;
} 
.nbae-cls .ok.even, .nbae-cls .ok code.even {
    background-color: #c4f8d8;
}
.nbae-cls .ko, .nbae-cls .ko code {
    background-color: #ffc6c9;
}
.nbae-cls .ko.even, .nbae-cls .ko code.even {
    background-color: #ffb6b9;
}
.nbae-cls .cell {
    padding: .2em .4em;
    border-radius: .4em;
}
.nbae-cls .cell.example {
    background-color: #f8f8f8;
    padding: .5em 1em;
}
.nbae-cls .cell.example.even {
    background-color: #e8e8e8;
    padding: .5em 1em;
}
.nbae-cls .result {
    padding: 0em .6em 0em .6em;
}
.nbae-cls .ko.result {
    font-weight: bold;
    font-size: '120%';
}
.nbae-cls div.widget-html-content {
    display: flex;
}
"""


class ClassExpression:
    """
    this utility class is used to model a step in a class scenario
    it is basically built from a string where
        'INSTANCE' is the object created in the first step, and
        'CLASS' is the class object itself
    """
    
    def __init__(self, code, statement=False):
        self.code = code
        self.statement = statement
        
    def __repr__(self):
        #  return f"<{type(self).__name__} {self.statement=} {self.code=}>"
        return f"<{type(self).__name__} statement={self.statement} code={self.code}>"
        
        
    def replace(self, varname, classname):
        return self.code.replace("INSTANCE", varname).replace("CLASS", classname)


class ClassStatement(ClassExpression):
    """
    a shortcut to create statements
    """
    def __init__(self, code):
        ClassExpression.__init__(self, code, True)

##########
class ClassScenario:
    """
    Describes a scenario that can be applied to a class

    Typically we want to create an instance (using some args),
    and then run some methods (still with some args)

    So a scenario is defined from
      * one Args instance that is passed to the constructor
      * a list of ClassExpression (or mere str) objects
        
    Example:
      for a Polynom class created from a set of coefficients
      ClassScenario(
          Args(1, 2, 3),
          ClassExpression("INSTANCE"),
          ClassExpression("INSTANCE.derivative()"),
          ClassExpression("INSTANCE + CLASS(3, 4, 5)"),
      )
      
      the expressions will be evaluated for 
      both the reference class and the student's class
      and the results compared with == 
      (unless the validate method is redefined on the Exercise class)
    """

    def __init__(self, init_args, *expressions):
        self.init_args = init_args
        def step(exp):
            return ClassExpression(exp) if isinstance(exp, str) else exp
        self.steps = [step(exp) for exp in expressions]
        if not isinstance(self.init_args, Args):
            print(f"ERROR ClassScenario first parameter needs to be an Args instance")
        for index, step in enumerate(self.steps, 1):
            if not isinstance(step, ClassExpression):
                print(f"ERROR ClassScenario, step #{index}, needs to be a ClassExpression instance")


##########
class ExerciseClass:                                    # pylint: disable=r0902
    """
    Much like the ExerciseFunction class, this allows to define
    an exercise as
    (*) a solution which is a Python class that provides the correct implementation
    (*) a list of scenarios that will be executed on that class

    From that plus a few accessories for fine-grained customization
    we can generate online example and correction.
    
    the check_init flag mostly targets very simple and early exos,
    given to students who do not yet know how to write their own repr();
    of course this assumes to not use a statement in the scenario, as that
    would still trigger repr()
    """

    def __init__(self, solution, scenarios,                     # pylint: disable=r0913
                 *,
                 copy_mode='deep',
                 nb_examples=1,
                 # how to render
                 result_renderer=None,
                 #
                 obj_name='X',
                 #
                 column_headers=None,
                 font_size=default_font_size,
                 header_font_size=default_header_font_size,
                 check_init=True,
                 ):
        # the 'official' solution
        self.solution = solution
        # the inputs - actually Scenario instances
        self.scenarios = scenarios
        # how to copy args
        self.copy_mode = copy_mode
        # how many examples
        self.nb_examples = nb_examples
        # a - preferrably uppercase - string to refer to 
        # current object in the scenarios
        self.obj_name = obj_name
        # 
        self.result_renderer = result_renderer or Renderer()
        # header names 
        self.column_headers = column_headers or default_column_headers
        #
        self.header_font_size = header_font_size
        self.font_size = font_size
        # see above
        self.check_init = check_init
        # computed
        self.name = solution.__name__
        

    def correction(self, stu_class, print_exceptions=False): # pylint: disable=r0914, r0915

        overall = True
        ref_class = self.solution

        headers_props = {'font-size': self.header_font_size}
        body_props = {'font-size': self.font_size}
        contents = []

        for index, scenario in enumerate(self.scenarios, 1):

            classes = ['cell']

            init_args = scenario.init_args
                                 

            # header for scenario
            contents += [TextContent(x.format(n=index))
                         .add_css_properties(headers_props)
                         .add_class('header')
                         .add_classes(span_classes)
                        for (x, span_classes) in zip(self.column_headers, 
                                                     column_span_classes)]
        
            call_renderer = CallRenderer(show_function=self.name, 
                                         prefix=f"{self.obj_name} = ",
                                         postfix=f"; repr({self.obj_name})") 
            init_rendered = call_renderer.render(Call(None, init_args))
            # clone args for both usages
            ref_args = init_args.clone(self.copy_mode)
            stu_args = init_args.clone(self.copy_mode)
                
            # initialize both objects
            try:
                # initialize both objects
                REF = ref_args.init_obj(ref_class)  
                STU = stu_args.init_obj(stu_class)
                
                if not self.check_init:
                    ref_repr = stu_repr = '--unchecked--'
                    is_ok = True
                else:
                    ref_repr, stu_repr = repr(REF), repr(STU)
                    is_ok = self.validate(REF, STU, ref_class, stu_class)
                    if not is_ok:
                        overall = False
                # render that run
                result_content = ResultContent(is_ok)

                contents.append(init_rendered
                                .add_classes(classes)
                                .add_css_properties(body_props))
                contents.append(self.result_renderer.render(ref_repr)
                                .add_classes(classes).add_class('ok')
                                .add_css_properties(body_props))
                contents.append(self.result_renderer.render(stu_repr)
                                .add_classes(classes)
                                .add_class(result_content.the_class())
                                .add_css_properties(body_props))
                contents.append(result_content
                                .add_classes(classes)
                                .add_css_properties(body_props))
                
            except Exception as exc:
                if print_exceptions:
                    import traceback
                    traceback.print_exc()
                error = f"Exception {type(exc)} {exc}"
                contents.append(init_rendered
                                .add_classes(classes)
                                .add_css_properties(body_props))
                contents.append(TextContent(error)
                                .add_classes(classes)
                                .add_class('ko')
                                .add_class('span-2-to-3')
                                .add_css_properties(body_props))
                contents.append(ResultContent(False)
                                .add_css_properties(body_props))
                overall = False
                continue

            # other steps of that scenario; first step was __init__
            for step_index, step in enumerate(scenario.steps, 2):
                code_ref = step.replace("REF", "ref_class")
                code_stu = step.replace("STU", "stu_class")
                display = step.replace(self.obj_name, ref_class.__name__)
                if step.statement:
                    display += f"; {self.obj_name}"

                classes = ['cell']
                if step_index % 2 == 0:
                    classes.append('even')
                # the function to use to run code, whether it's a statement
                # or an expression; in the former case of course, there is no need 
                # to cmpare results as they are None, but that's not important
                code_runner = exec if step.statement else eval
                ref_result = code_runner(code_ref)
                try:
                    stu_result = code_runner(code_stu)
                    if step.statement:
                        stu_result = repr(STU)
                        ref_result = repr(REF)
                    is_ok = self.validate(ref_result, stu_result, ref_class, stu_class)
                    if not is_ok:
                        overall = False
                    result_content = ResultContent(is_ok)

                except Exception as exc:
                    result_content = ResultContent(False)
                    overall = False
                    stu_result = f"Exception {type(exc)}: {exc}"
                    if step.statement:
                        ref_result = repr(REF)

                contents.append(TextContent(display)
                                .set_is_code(True)
                                .add_classes(classes)
                                .add_css_properties(body_props))
                contents.append(self.result_renderer.render(ref_result)
                                .add_classes(classes).add_class('ok')
                                .add_css_properties(body_props))
                contents.append(self.result_renderer.render(stu_result)
                                .add_classes(classes)
                                .add_class(result_content.the_class())
                                .add_css_properties(body_props))
                contents.append(result_content
                                .add_classes(classes)
                                .add_css_properties(body_props))

        log_correction(self.name, overall)
        # xxx would make sense to expose how many examples were right or wrong
        log2_correction(self.name, success=overall)

        contents.append(CssContent(CSS))

        gridbox_layout  = Layout(grid_template_columns = 'max-content 1fr 1fr max-content',
                                 max_width="100%")
        grid = GridBox([content.widget() for content in contents],
                       layout=gridbox_layout).add_class("nbae-cls")
        return grid


    def example(self):                                  # pylint: disable=r0914
        """
        display a table with example scenarios
        """
        ref_class = self.solution

        headers_props = {'font-size': self.header_font_size}
        body_props = {'font-size': self.font_size}
        contents = []

        how_many_samples = self.nb_examples if self.nb_examples \
                           else len(self.scenarios)

        sample_scenarios = self.scenarios[:how_many_samples]
        for index, scenario in enumerate(sample_scenarios, 1):

            classes = ['cell', 'example']
            # start of scenario
            contents += [
                TextContent(x.format(n=index))
                .add_css_properties(headers_props)
                .add_class('header')
                .add_classes(span_classes)
                for (x, span_classes) in zip(self.column_headers,
                                             example_column_span_classes)]

            # object construction
            init_args = scenario.init_args.clone(self.copy_mode)
            SAMPLE = init_args.init_obj(ref_class)      # pylint: disable=unused-variable

            call_renderer = CallRenderer(show_function=self.name, 
                                         prefix=f"{self.obj_name} = ",
                                         postfix=f"; repr({self.obj_name})") 
            init_rendered = call_renderer.render(Call(None, init_args))
            contents.append(init_rendered
                            .add_classes(classes)
                            .add_css_properties(body_props))
            contents.append(self.result_renderer.render(repr(SAMPLE))
                            .add_classes(classes)
                            .add_css_properties(body_props))

            for step_index, step in enumerate(scenario.steps, 2):
                display = step.replace(self.obj_name, ref_class.__name__)
                code = step.replace("SAMPLE", "ref_class")
                code_runner = exec if step.statement else eval
                ref_result = code_runner(code)
                classes = ['cell', 'example']
                if step_index % 2 == 0:
                    classes.append('even')
                
                ### display
                if step.statement:
                    display += f"; repr({self.obj_name})"
                    ref_result = repr(SAMPLE)
                contents.append(TextContent(display)
                                .set_is_code(True)
                                .add_classes(classes)
                                .add_css_properties(body_props))
                contents.append(self.result_renderer.render(ref_result)
                                .add_classes(classes)
                                .add_css_properties(body_props))

        contents.append(CssContent(CSS))

        gridbox_layout  = Layout(grid_template_columns = 'max-content max-content')
        grid = GridBox([area.widget() for area in contents],
                       layout=gridbox_layout).add_class("nbae-cls")
        return grid
    

    def validate(self, ref_res, stu_res, ref_class, stu_class):
        """
        how to compare the results as obtained from
        * the solution instance
        * the student instance
        * the solution class
        * the student class 
        
        it is not possible in the general case to use == on objects
        since the 2 classes are different, and so == will always return False
        """
        if not isinstance(ref_res, ref_class) and not isinstance(stu_res, stu_class):
            # assuming both are regular Python objects 
            # use ==
            return ref_res == stu_res
        if isinstance(ref_res, ref_class) and isinstance(stu_res, stu_class):
            # compare repr's
            return repr(ref_res) == repr(stu_res)
        else:
            # something is wrong
            return False
