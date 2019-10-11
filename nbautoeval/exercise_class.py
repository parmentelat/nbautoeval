# -*- coding: utf-8 -*-

# pylint: disable=c0111, c0103, r1705, w0703

from IPython.display import HTML

from .log import log_correction

from .rendering import (
    Table, TableRow, TableCell, CellLegend,
    font_style, default_font_size, default_header_font_size,
    ok_style, ko_style,
    center_text_style, left_text_style,
    top_border_style, top_border_style2, bottom_border_style,
    left_border_thick_style, left_border_thin_style,
)


########## defaults for columns widths - for FUN
# this historically was called 'columns' as it was used to specify
# the width of the 3 columns (in correction mode)
# or of the 2 columns (in example mode)
# however when adding new layouts like 'text', the argument passed to the layout
# function ceased to be a column width, so we call this layout_args instead
# but in most cases this does represent column widths
DEFAULT_LAYOUT_ARGS = (50, 25, 25)

class ClassStep:
    """
    this utility class is used to model a step in a class scenario
    it is basically built from a string where
        'INSTANCE' is the object created in the first step, and
        'CLASS' is the class object itself
    """
    
    def __init__(self, exp, statement=False):
        self.exp = exp
        self.statement = statement
        
    def replace(self, varname, classname):
        return self.exp.replace("INSTANCE", varname).replace("CLASS", classname)

##########
class ClassScenario:
    """
    Describes a scenario that can be applied to a class

    Typically we want to create an instance (using some args),
    and then run some methods (still with some args)

    So a scenario is defined from
      * one Args instance that is passed to the constructor
      * a list of ClassStep (or mere str) objects
        
    Example:
      for a Polynom class created from a set of coefficients
      ClassScenario(
          Args(1, 2, 3),
          ClassStep("repr(INSTANCE)"),
          "INSTANCE.derivative()",
          "INSTANCE + CLASS(3, 4, 5)",
      )
      
      the expressions will be evaluated for 
      both the reference class and the student's class
      and the results compared with ==
    """

    def __init__(self, init_args, *expressions):
        self.init_args = init_args
        def step(exp):
            return exp if isinstance(exp, ClassStep) else ClassStep(exp)
        self.steps = [step(exp) for exp in expressions]


##########
import operator

class ExerciseClass:                                    # pylint: disable=r0902
    """
    Much like the ExerciseFunction class, this allows to define
    an exercise as
    (*) a solution which is the correct implementation of a class
    (*) a list of scenarios that will be executed on that class

    From that plus a few accessories for fine-grained customization
    we can generate online example and correction.
    """

    def __init__(self, solution, scenarios, *,          # pylint: disable=r0913
                 compare=operator.eq,
                 copy_mode='deep',
                 layout=None,
                 call_layout=None,
                 nb_examples=1,
                 obj_name='X',
                 layout_args=None,
                 font_size=default_font_size,
                 header_font_size=default_header_font_size,
                 ):
        self.solution = solution
        self.scenarios = scenarios
        self.compare = compare
        self.copy_mode = copy_mode
        self.layout = layout
        self.call_layout = call_layout
        self.nb_examples = nb_examples
        self.obj_name = obj_name
        self.layout_args = layout_args
        # sizes for the table
        self.font_size = font_size
        self.header_font_size = header_font_size
        # 
        # computed
        self.name = solution.__name__
        

    # adding this feature on ExerciseClass as a mirror of ExerciseFunction
    # but this it is unclear if it's really useful as class exos will be likely
    # to always use the same layout..
    def set_call_layout(self):
        "set layout on all Args if/as specified in call_layout"
        if self.call_layout is not None:
            for scenario in self.scenarios:
                for step in scenario:
                    step[1].set_layout(self.call_layout)


    def correction(self, student_class):        # pylint: disable=r0914, r0915

        self.set_call_layout()

        overall = True

        # should be customizable
        columns = self.layout_args
        if not columns:
            columns = DEFAULT_LAYOUT_ARGS
        c1, c2, c3 = columns
        ref_class = self.solution

        table = Table(style=font_style(self.font_size))
        html = table.header()

        for i, scenario in enumerate(self.scenarios, 1):

            init_args = scenario.init_args

            # start of scenario
            legend = CellLegend(f"Scénario {i}")
            html += TableRow(
                cells=[TableCell(legend, colspan=4, tag='th',
                                 style='text-align:center')],
                style=font_style(self.header_font_size) + top_border_style).html()
            cells = [TableCell(CellLegend(x), tag='th')
                     for x in ('Appel', 'Attendu', 'Obtenu', '')]
            html += TableRow(cells=cells, style=top_border_style2 + bottom_border_style).html()

            # initialize both objects
            try:
                # clone args for both usages
                ref_args = init_args.clone(self.copy_mode)
                student_args = init_args.clone(self.copy_mode)
                # always render the classname - with a name
                init_args.render_function_name(self.name)
                init_args.render_prefix(f"{self.obj_name} = ")
                
                # initialize both objects
                REF = ref_args.init_obj(     # pytlint=disable: unused-variable
                    ref_class)  
                STU = student_args.init_obj( # pytlint=disable: unused-variable
                    student_class)
                cells = (TableCell(init_args, layout=self.layout, width=c1),
                         TableCell(CellLegend('-'),
                                   style=left_border_thick_style),
                         TableCell(CellLegend('-'),
                                   style=left_border_thin_style),
                         TableCell(CellLegend('-'),
                                   style=left_border_thick_style))
                html += TableRow(cells=cells, style=ok_style).html()
            except Exception as exc:
                import traceback
                traceback.print_exc()
                cell1 = TableCell(args_obj, layout=self.layout, width=c1+c2,
                                  colspan=2)
                error = f"Exception {exc}"
                cell2 = TableCell(CellLegend(error), width=c3,
                                  style=left_border_thick_style)
                cell3 = TableCell(CellLegend('KO'),
                                  style=left_border_thick_style)
                html += TableRow(cells=(cell1, cell2, cell3),
                                 style=ko_style).html()
                overall = False
                continue

            # other steps of that scenario
            for step in scenario.steps:
                displayed = step.replace(self.obj_name, ref_class.__name__)
                computed_ref = step.replace("REF", "ref_class")
                computed_stu = step.replace("STU", "student_class")

                # the function to use to run code, whether it's a statement
                # or an expression; in the former case of course, there is no need 
                # to cmpare results as they are None, but that's not important
                code_runner = exec if step.statement else eval
                ref_result = code_runner(computed_ref)
                try:
                    student_result = code_runner(computed_stu)
                    if step.statement:
                        style = ok_style
                        msg = 'OK'
                        ref_result = student_result = '-'
                    elif self.compare(ref_result, student_result):
                        style = ok_style
                        msg = 'OK'
                    else:
                        style = ko_style
                        msg = 'KO'
                        overall = False
                except Exception as exc:
                    style = ko_style
                    msg = 'KO'
                    overall = False
                    student_result = f"Exception {exc}"

                # xxx styling maybe a little too much...
                cells = (TableCell(displayed, layout='text', width=c1),
                         TableCell(ref_result, layout=self.layout, width=c2,
                                   style=left_border_thick_style
                                   +left_text_style),
                         TableCell(student_result, layout=self.layout, width=c3,
                                   style=left_border_thin_style
                                   +left_text_style),
                         TableCell(CellLegend(msg),
                                   style=left_border_thick_style))
                html += TableRow(cells=cells, style=style).html()

        log_correction(self.name, overall)

        html += "</table>"

        return HTML(html)


    def example(self):                                  # pylint: disable=r0914
        """
        display a table with example scenarios
        """
        self.set_call_layout()
        columns = self.layout_args if self.layout_args \
                  else DEFAULT_LAYOUT_ARGS
        ref_class = self.solution

        how_many_samples = self.nb_examples if self.nb_examples \
                           else len(self.scenarios)

        # can provide 3 args (convenient when it's the same as correction) or just 2
        columns = columns[:2]
        c1, c2 = columns
        table = Table(style=font_style(self.font_size))
        html = table.header()

        sample_scenarios = self.scenarios[:how_many_samples]
        for i, scenario in enumerate(sample_scenarios, 1):

            # first step is to create an instance
            # lets' call it SAMPLE
            init_args = scenario.init_args.clone(self.copy_mode)
            SAMPLE = init_args.init_obj(ref_class)       # pylint: disable=unused-variable

            init_args.render_function_name(self.name)
            init_args.render_prefix(f"{self.obj_name} = ")

            # start of scenario
            legend = CellLegend(f"Scénario {i}")
            html += TableRow(
                cells=[TableCell(legend, colspan=4, tag='th',
                                 style=center_text_style)],
                style=font_style(self.header_font_size) + top_border_style).html()
            cells = [TableCell(CellLegend(x), tag='th')
                     for x in ('Appel', 'Attendu')]
            html += TableRow(cells=cells, style=top_border_style2 + bottom_border_style).html()

            cells = (TableCell(init_args, layout=self.layout, width=c1),
                     TableCell(CellLegend('-'),
                               style=left_border_thick_style
                               + left_text_style))
            html += TableRow(cells=cells).html()

            for step in scenario.steps:
                computed = step.replace("SAMPLE", "ref_class")
                displayed = step.replace(self.obj_name, ref_class.__name__)
                code_runner = exec if step.statement else eval
                # print(f"statement={step.statement}, code={computed}")
                ref_result = code_runner(computed)
                if step.statement:
                    ref_result = "-"
                cells = (TableCell(displayed, layout='text', width=c1),
                         TableCell(ref_result, layout=self.layout, width=c2,
                                   style=left_border_thick_style
                                   +left_text_style))
                html += TableRow(cells=cells).html()

        html += table.footer()
        return HTML(html)
