# -*- coding: utf-8 -*-

# pylint: disable=c0111, w0703, r1705

############################################################
# the low level interface - used to be used directly in the first exercises

from IPython.display import HTML

from .log import log_correction
from .rendering import (
    Table, TableRow, TableCell, CellLegend,
    font_style, default_font_size, default_header_font_size,
    ok_style, ko_style,
    center_text_style, left_text_style,
    bottom_border_style, left_border_thick_style, left_border_thin_style,
)

DEBUG = False
#DEBUG = True

########## defaults for columns widths - for FUN
# this historically was called 'columns' as it was used to specify
# the width of the 3 columns (in correction mode)
# or of the 2 columns (in example mode)
# however when adding new layouts like 'text', the argument passed to the layout
# function ceased to be a column width, so we call this layout_args instead
# but in most cases this does represent column widths
DEFAULT_LAYOUT_ARGS = (24, 28, 28)

####################
class ExerciseFunction:                                 # pylint: disable=r0902
    """The class for an exercise where students are asked to write a
    function The teacher version of that function is provided as
    'solution' and is used against datasets to generate an online
    correction or example.
    A dataset is an instance of Args (or ArgsKeywords)

    The most useful method in this class is 'correction'; for each
    input in the dataset, we call both the teacher function and the
    student function, and compare the results using '==' to produce a
    table of green or red cells.

    The class provides a few other utility methods, like 'example'
    that can be used in the students notebook to show the expected
    result for some or all of the inputs.

    One important aspects of this is copying. Realizing that both
    teacher and student functions can do side effects in the inputs,
    it means that these need to be copied before any call is made. By
    default the copy is a deep copy, but for some corner cases it can
    be required to use shallow copy instead; in this case just pass
    copy_mode='shallow' to the constructor here.

    Some more cosmetic settings are supported as well, for defining
    the column widths in both the correction and example outputs. Also
    nb_examples allows you to specify how many inputs should be
    considered for generating the example table (starting of course at
    the top of the list).
    Finally render_name, if set to True, will cause the function name
    to appear in the first column together with arguments
    """
    def __init__(self, solution, datasets,              # pylint: disable=r0913
                 copy_mode='deep',
                 layout='pprint',
                 call_layout=None,
                 render_name=True,
                 nb_examples=1,
                 layout_args=None,
                 column_headers=None,
                 font_size=default_font_size,
                 header_font_size=default_header_font_size):
        # the 'official' solution
        self.solution = solution
        # the inputs - actually Args instances
        self.datasets = datasets
        # how to copy args
        self.copy_mode = copy_mode
        # applicable to all cells whose Args instance has not specified a layout
        self.layout = layout
        # supersedes the layout in the first column
        self.call_layout = call_layout
        # states if the function name should appear in the call cells
        self.render_name = render_name
        # how many examples
        self.nb_examples = nb_examples
        # column details - 3-tuples
        # sizes - defaults should be fine in most cases
        self.layout_args = layout_args
        # header names - for some odd cases
        self.column_headers = column_headers
        # sizes for the table
        self.font_size = font_size
        self.header_font_size = header_font_size
        ###
        # in some weird cases this won't exist
        self.name = getattr(solution, '__name__', "no_name")

    def set_call_layout(self):
        "set layout on all Args if/as specified in call_layout"
        if self.call_layout is not None:
            for dataset in self.datasets:
                dataset.set_layout(self.call_layout)

    def correction(self, student_function):             # pylint: disable=r0914
        """
        colums should be a 3-tuple for the 3 columns widths
        copy_mode can be either None, 'shallow', or 'deep' (default)
        """
        self.set_call_layout()
        datasets = self.datasets
        copy_mode = self.copy_mode
        columns = self.layout_args if self.layout_args \
                  else DEFAULT_LAYOUT_ARGS

        col1, col2, col3 = columns
        #print("Using columns={}".format(columns))

        table = Table(style=font_style(self.font_size))
        html = table.header()

        if self.column_headers:
            tit1, tit2, tit3 = self.column_headers
        else:
            tit1, tit2, tit3 = (
                "Arguments" if not self.render_name else "Appel",
                "Attendu",
                "Obtenu")
        html += TableRow(
            cells=[TableCell(CellLegend(x), tag='th', style=center_text_style)
                   for x in (tit1, tit2, tit3, '')],
            style=font_style(self.header_font_size)).html()

        overall = True
        for dataset in datasets:
            # will use original dataset for rendering to avoid any side-effects
            # during running
            if self.render_name:
                dataset.render_function_name(self.name)
            # always clone all inputs
            student_dataset = dataset.clone(copy_mode)
            ref_dataset = dataset.clone(copy_mode)

            # run both codes
            try:
                expected = ref_dataset.call(self.solution, debug=DEBUG)
            except Exception as exc:
                expected = exc

            try:
                student_result = student_dataset.call(student_function, debug=DEBUG)
            except Exception as exc:
                student_result = exc

            # compare results
            is_ok = self.validate(expected, student_result)
            if not is_ok:
                overall = False
            # render that run
            message = 'OK' if is_ok else 'KO'
            style = ok_style if is_ok else ko_style
            html += TableRow(
                style=style + bottom_border_style,
                cells=[TableCell(dataset, layout=self.layout, width=col1),
                       TableCell(expected, layout=self.layout, width=col2,
                                 style=left_text_style
                                 +left_border_thick_style),
                       TableCell(student_result, layout=self.layout, width=col3,
                                 style=left_text_style
                                 +left_border_thin_style),
                       TableCell(CellLegend(message),
                                 style=left_border_thick_style)]
            ).html()

        log_correction(self.name, overall)
        html += table.footer()
        return HTML(html)

    # public interface
    def example(self, how_many=None):

        self.set_call_layout()

        if how_many is None:
            how_many = self.nb_examples
        columns = self.layout_args if self.layout_args \
                  else DEFAULT_LAYOUT_ARGS

        if how_many is None:
            how_many = self.nb_examples
        if how_many == 0:
            how_many = len(self.datasets)

        # can provide 3 args (convenient when it's the same as correction) or just 2
        columns = columns[:2]
        col1, col2 = columns
        #print("Using columns={}".format(columns))

        table = Table(style=font_style(self.font_size))
        html = table.header()

        title1 = "Arguments" if not self.render_name else "Appel"
        # souci avec l'accent de 'Résultat Attendu'
        html += TableRow(style=font_style(self.header_font_size),
                         cells=[TableCell(CellLegend(x),
                                          tag='th',
                                          style=center_text_style)
                                for x in (title1, 'Resultat Attendu')]).html()
        for dataset in self.datasets[:how_many]:
            sample_dataset = dataset.clone(self.copy_mode)
            if self.render_name:
                dataset.render_function_name(self.name)
            try:
                expected = sample_dataset.call(self.solution)
            except Exception as exc:                     # pylint:disable=w0703
                expected = exc
            html += TableRow(
                cells=[TableCell(dataset,
                                 layout=self.layout, width=col1),
                       TableCell(expected, layout=self.layout, width=col2,
                                 style=left_text_style+left_border_thick_style)
                       ]).html()

        html += table.footer()
        return HTML(html)


    def validate(self, expected, result):               # pylint: disable=r0201
        """
        how to compare the results as obtained from
        * the solution function
        * and the student function

        the default here is to use ==
        """
        return expected == result

# see this question on SO
# https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur

try:
    import numpy as np
    import warnings

    class ExerciseFunctionNumpy(ExerciseFunction):
        """
        This is suitable for functions that are expected to return a numpy (nd)array
        """

        def __init__(self, solution, datasets,
                     *args,
                     layout='text',
                     call_layout='pprint',
                     **kwds):
            ExerciseFunction.__init__(
                self, solution, datasets,
                layout=layout,
                call_layout=call_layout,
                *args, **kwds)

        # redefine validation function on numpy arrays
        def validate(self, expected, result):
            try:
                return np.all(
                    np.isclose(
                        expected, result))
            except Exception:
                # print("OOPS", type(e), e)
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter(action='ignore', category=FutureWarning)
                        # we need to return a genuine bool here
                        result = expected == result
                        if isinstance(result, np.ndarray):
                            return np.all(result)
                        else:
                            return result
                except Exception as exc:
                    print("OOPS2", type(exc), exc)
                    return False

except Exception:
    #print("ExerciseFunctionNumpy not defined ; numpy not installed ? ")
    pass
