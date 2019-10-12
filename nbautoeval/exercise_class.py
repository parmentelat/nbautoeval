# -*- coding: utf-8 -*-

# pylint: disable=c0111, c0103, r1705, w0703

from IPython.display import HTML

from .log import log_correction

from .rendering import (
    Table, TableRow, TableCell, CellLegend,
    font_style, default_font_size, default_header_font_size,
    ok_style, ko_style,
    center_text_style, left_text_style,
    top_border_style, top_border_style2, 
    bottom_border_style, bottom_border_style2, bottom_border_style3,
    left_border_thick_style, left_border_thin_style,
    table_border_style,
)


########## defaults for columns widths - for FUN
# this historically was called 'columns' as it was used to specify
# the width of the 3 columns (in correction mode)
# or of the 2 columns (in example mode)
# however when adding new layouts like 'text', the argument passed to the layout
# function ceased to be a column width, so we call this layout_args instead
# but in most cases this does represent column widths
DEFAULT_LAYOUT_ARGS = (50, 25, 25)

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
          ClassExpression("repr(INSTANCE)"),
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
            return exp if isinstance(exp, ClassExpression) else ClassExpression(exp)
        self.steps = [step(exp) for exp in expressions]


##########
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


    def correction(self, stu_class):        # pylint: disable=r0914, r0915

        self.set_call_layout()

        overall = True

        # should be customizable
        columns = self.layout_args
        if not columns:
            columns = DEFAULT_LAYOUT_ARGS
        c1, c2, c3 = columns
        ref_class = self.solution

        table = Table(style=font_style(self.font_size) + table_border_style)
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
                stu_args = init_args.clone(self.copy_mode)
                # always render the classname - with a name
                init_args.render_function_name(self.name)
                init_args.render_prefix(f"{self.obj_name} = ")
                init_args.render_postfix(f"; {self.obj_name}")
                
                # initialize both objects
                REF = ref_args.init_obj(     # pylint: disable=unused-variable
                    ref_class)  
                STU = stu_args.init_obj(     # pylint: disable=unused-variable
                    stu_class)
                ref_repr = repr(REF)
                stu_repr = repr(STU)
                ok = self.validate(REF, STU, ref_class, stu_class)
                style = ok_style if ok else ko_style
                overall = overall and ok
                msg = 'OK' if ok else 'KO'
                cells = (TableCell(init_args, layout=self.layout, width=c1),
                         TableCell(CellLegend(ref_repr),
                                   style=left_border_thick_style+left_text_style),
                         TableCell(CellLegend(stu_repr),
                                   style=left_border_thin_style+left_text_style),
                         TableCell(CellLegend(msg),
                                   style=left_border_thick_style))
                html += TableRow(cells=cells, style=style + bottom_border_style2).html()
            except Exception as exc:
                import traceback
                traceback.print_exc()
                cell1 = TableCell(init_args, layout=self.layout, width=c1+c2,
                                  colspan=2)
                error = f"Exception {exc}"
                cell2 = TableCell(CellLegend(error), width=c3,
                                  style=left_border_thick_style)
                cell3 = TableCell(CellLegend('KO'),
                                  style=left_border_thick_style)
                html += TableRow(cells=(cell1, cell2, cell3),
                                 style=ko_style + bottom_border_style2).html()
                overall = False
                continue

            # other steps of that scenario
            for step in scenario.steps:
                code_ref = step.replace("REF", "ref_class")
                code_stu = step.replace("STU", "stu_class")
                disp = step.replace(self.obj_name, ref_class.__name__)
                layout = self.layout
                if step.statement:
                    disp += f"; {self.obj_name}"
                    layout = 'text'

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
                    ok = self.validate(ref_result, stu_result, ref_class, stu_class)
                    style = ok_style if ok else ko_style
                    msg = 'OK' if ok else 'KO'
                    overall = overall and ok
                except Exception as exc:
                    style = ko_style
                    msg = 'KO'
                    overall = False
                    stu_result = f"Exception {exc}"
                    if step.statement:
                        ref_result = repr(REF)

                cells = (TableCell(disp, layout='text', width=c1),
                         TableCell(ref_result, layout=layout, width=c2,
                                   style=left_border_thick_style
                                   +left_text_style),
                         TableCell(stu_result, layout=layout, width=c3,
                                   style=left_border_thin_style
                                   +left_text_style),
                         TableCell(CellLegend(msg),
                                   style=left_border_thick_style))
                html += TableRow(cells=cells, style=style + bottom_border_style3).html()

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
        table = Table(style=font_style(self.font_size) + table_border_style)
        html = table.header()

        sample_scenarios = self.scenarios[:how_many_samples]
        for i, scenario in enumerate(sample_scenarios, 1):

            # start of scenario
            legend = CellLegend(f"Scénario {i}")
            html += TableRow(
                cells=[TableCell(legend, colspan=4, tag='th',
                                 style=center_text_style)],
                style=font_style(self.header_font_size) + top_border_style).html()
            cells = [TableCell(CellLegend(x), tag='th')
                     for x in ('Appel', 'Attendu')]
            html += TableRow(cells=cells, 
                             style=top_border_style2 + bottom_border_style).html()

            # object construction
            init_args = scenario.init_args.clone(self.copy_mode)
            SAMPLE = init_args.init_obj(ref_class)      # pylint: disable=unused-variable

            init_args.render_function_name(self.name)
            init_args.render_prefix(f"{self.obj_name} = ")

            cells = (TableCell(init_args, layout=self.layout, width=c1),
                     TableCell(CellLegend(repr(SAMPLE)),
                               style=left_border_thick_style
                               + left_text_style))
            html += TableRow(cells=cells, style=bottom_border_style2).html()

            for step in scenario.steps:
                code = step.replace("SAMPLE", "ref_class")
                disp = step.replace(self.obj_name, ref_class.__name__)
                code_runner = exec if step.statement else eval
                ref_result = code_runner(code)
                ### display
                if step.statement:
                    disp += f"; {self.obj_name}"
                    layout = 'text'
                    ref_result = repr(SAMPLE)
                else:
                    layout = self.layout
                cells = (TableCell(disp, layout='text', width=c1),
                         TableCell(ref_result, layout=layout, width=c2,
                                   style=left_border_thick_style
                                   +left_text_style))
                html += TableRow(cells=cells, style=bottom_border_style3).html()

        html += table.footer()
        return HTML(html)
    

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

