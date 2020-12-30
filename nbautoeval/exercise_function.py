# -*- coding: utf-8 -*-

# pylint: disable=c0111, w0703, r1705

############################################################
# the low level interface - used to be used directly in the first exercises

from ipywidgets import GridBox, Layout

from .content import TextContent, CssContent, ResultContent
from .callrenderer import Call, CallRenderer
from .renderer import Renderer
from .helpers import default_font_size, default_header_font_size
from .storage import log_correction, log2_correction
import pandas as pd


DEBUG = False
#DEBUG = True


default_column_headers_visible_function_name = (
    "appel",
    "attendu",
    "obtenu",
)
default_column_headers_no_function_name = (
    "arguments",
    "attendu",
    "obtenu",
)
# same order
column_span_classes = (
    "", "", "span-3-to-4",
)

###
CSS = """
.nbae-fun {
    width: max-content;
    border-top: .1em solid black;
    border-bottom: .1em solid black;
    padding: 0.1em 0em;
    row-gap: 0.5em;
    column-gap: .4em;
}
.nbae-fun .header {
    padding: .6em;
    background-color: #f1fcfc;
    border-bottom: .1em solid #666;
    font-weight: bold;
    border-top-left-radius: .4em;
    border-top-right-radius: .4em;
}
.nbae-fun .span-3-to-4 {
    grid-column: 3 / span 2;
}
div.nbae-fun pre {
    padding: 0px;
    line-height: 1.15;
    max-width: 100%;
    overflow: hidden;
}
div.nbae-fun .cell span {
    line-height: 1.15;
}
.nbae-fun .cell.ok, .nbae-fun .cell.ok code, .nbae-fun .result.ok {
    background-color: #d4f8e8;
}
.nbae-fun .cell.ok.even, .nbae-fun .cell.ok code.even, .nbae-fun .result.ok.even {
    background-color: #c4f8d8;
}
.nbae-fun .cell.ko, .nbae-fun .cell.ko code, .nbae-fun .result.ko {
    background-color: #ffc6c9;
}
.nbae-fun .cell.ko.even, .nbae-fun .cell.ko code.even, .nbae-fun .result.ko.even {
    background-color: #ffb6b9;
}
.nbae-fun .cell {
    padding: .2em .4em;
    border-radius: .4em;
    background-color: #f8f8f8;
    max-width: 100%;
}
.nbae-fun .cell.even {
    background-color: #f0f0f0;
}
.nbae-fun .ko.result {
    font-weight: bold;
    font-size: '130%';
}
.nbae-fun .result {
    padding: 4px;
}
.nbae-fun div.widget-html-content {
    display: flex;
}
"""

####################
class ExerciseFunction:                                           # pylint: disable=r0902
    """The class for an exercise where students are asked to write a
    function The teacher version of that function is provided as
    'solution' and is used against datasets to generate an online
    correction or example.

    A dataset is typically an instance of Args, it describes
    how the function is to be called (the arguments, both named and unnamed).

    **NOTE** that the Args model predates keyword-only and a fortiori
    positional-only parameters, so these might be a bit awkward to play with.

    The most useful method in this class is 'correction'; for each
    input in the dataset, we call both the teacher function and the
    student function, and compare the results using '==' to produce a
    table of green or red cells.

    The class provides a few other utility methods, notably 'example'
    that can be used in the students notebook to show the expected
    result for some or all of the inputs.

    One important aspects of this is copying. Realizing that both
    teacher and student functions can do side effects in the inputs,
    it means that these need to be copied before any call is made. By
    default the copy is a deep copy, but for some corner cases it can
    be required to use shallow copy instead; in this case just pass
    copy_mode='shallow' to the constructor here.

    In terms of rendering, an ExerciseFunction object requires 2 renderer objects

    * call_renderer is used to compute the contents of the leftmost column in the output
      of both correction() and example();
      this attribute should be a `CallRenderer` instance, that has a `render()` method
      that works on `Call` instances, and that returns a `Content` object.
    * result_renderer works similarly, it is used to render the results of the function
      calls in the internal columns of the output of correction(), and the rightmost
      column of the output of example();

    Typical uses of these 2 rendering attributes would be

    * ExerciseFunction(call_renderer=CallRenderer(show_function=False))
      allows to remove the function name, showing only arguments, to save space
    * ExerciseFunction(call_renderer=PPrintRenderer(width=30))
    * ExerciseFunction(result_renderer=PPrintRenderer(width=30)) allows to set
      a fixed limit limit for either calls or results.
    """
    def __init__(self, solution, datasets,              # pylint: disable=r0913
                 *,
                 copy_mode='deep',
                 nb_examples=1,
                 # how to render
                 call_renderer=None,
                 result_renderer=None,
                 #
                 column_headers=None,
                 font_size=default_font_size,
                 header_font_size=default_header_font_size,
                 # used for reports/logs, defaults computed from solution
                 name=None):
        # the 'official' solution
        self.solution = solution
        # the inputs - actually Args instances
        self.datasets = datasets
        # how to copy args
        self.copy_mode = copy_mode
        # how many examples
        self.nb_examples = nb_examples
        # renderers
        self.call_renderer = call_renderer or CallRenderer()
        self.result_renderer = result_renderer or Renderer()
        # header names: at this point, just remember any data passed
        # it's too erly to compute the actual value, as show_function
        # could be turned off later on - see e.g. ExerciseRegexp
        self._column_headers = column_headers
        #
        self.header_font_size = header_font_size
        self.font_size = font_size
        ###
        # in some weird cases this won't exist
        self.name = name or getattr(solution, '__name__', "no_name")


    @property
    def column_headers(self):
        return (self._column_headers if self._column_headers is not None
            else default_column_headers_visible_function_name if self.call_renderer.show_function
            else default_column_headers_no_function_name)


    def correction(self, student_function):             # pylint: disable=r0914
        """
        colums should be a 3-tuple for the 3 columns widths
        copy_mode can be either None, 'shallow', or 'deep' (default)
        or 'tee' for generators
        """
        datasets = self.datasets
        copy_mode = self.copy_mode

        #
        headers_props = {'font-size': self.header_font_size}
        body_props = {'font-size': self.font_size}
        contents = [TextContent(x, css_properties=headers_props)
                    .add_classes(['header', span_class])
                    for (x, span_class) in zip(self.column_headers, column_span_classes)]


        overall = True

        for index, dataset in enumerate(datasets):
            # will use original dataset for rendering to avoid any side-effects
            # during running

            # always clone all inputs
            if copy_mode != 'tee':
                student_dataset = dataset.clone(copy_mode)
                ref_dataset = dataset.clone(copy_mode)
            else:
                student_dataset, ref_dataset = dataset.copy_for_tee('tee')

            # run both codes
            ref_exc, stu_exc = False, False
            try:
                expected = ref_dataset.call(self.solution, debug=DEBUG)
            except Exception as exc:
                expected = exc
                ref_exc = True

            try:
                student_result = student_dataset.call(student_function, debug=DEBUG)
            except Exception as exc:
                student_result = exc
                stu_exc = True

            # compare results
            is_ok = self.validate(expected, student_result)
            if not is_ok:
                overall = False
            # render that run
            result_content = ResultContent(is_ok)
            classes = ['cell']
            if index % 2 == 0:
                classes.append("even")

            call = Call(self.solution, dataset)
            contents.append(self.call_renderer.render(call)
                            .add_classes(classes)
                            .add_css_properties(body_props))
            contents.append(self.result_renderer.render(expected)
                            .add_classes(classes).add_class('ok')
                            .add_css_properties(body_props)
                            .set_is_code(not ref_exc))
            contents.append(self.result_renderer.render(student_result)
                            .add_classes(classes)
                            .add_class(result_content.the_class())
                            .add_css_properties(body_props)
                            .set_is_code(not stu_exc))
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
                       layout=gridbox_layout).add_class("nbae-fun")
        return grid


    # public interface
    def example(self, how_many=None):

        if how_many is None:
            how_many = self.nb_examples
        if how_many == 0:
            how_many = len(self.datasets)


        headers_props = {'font-size': self.header_font_size}
        body_props = {'font-size': self.font_size}
        contents = [TextContent(x, css_properties=headers_props).add_class('header')
                    for x in self.column_headers[:2]]
        #

        for index, dataset in enumerate(self.datasets[:how_many]):
            # clone enve in example() mode to avoid altering datasets
            if self.copy_mode != 'tee':
                sample_dataset = dataset.clone(self.copy_mode)
            else:
                sample_dataset, dataset = dataset.copy_for_tee(self.copy_mode)

            # run
            try:
                expected = sample_dataset.call(self.solution)
            except Exception as exc:                     # pylint:disable=w0703
                expected = exc

            # render that row
            classes = ['cell', 'example']
            if index % 2 == 0:
                classes.append("even")


            call = Call(self.solution, dataset)
            contents.append(self.call_renderer.render(call)
                            .add_classes(classes)
                            .add_css_properties(body_props))
            contents.append(self.result_renderer.render(expected)
                            .add_classes(classes)
                            .add_css_properties(body_props))

        contents.append(CssContent(CSS))

        gridbox_layout  = Layout(grid_template_columns = 'max-content 1fr')
        grid = GridBox([content.widget() for content in contents],
                       layout=gridbox_layout).add_class("nbae-fun")
        return grid


    def validate(self, expected, result):               # pylint: disable=r0201
        """
        how to compare the results as obtained from
        * the solution function
        * and the student function

        the default here is to use ==
        """

        if DEBUG:
            print(f"ExerciseFunction.validate is comparing {expected} with {result}")
        if isinstance(expected, (pd.DataFrame, pd.Series)):
            return expected.equals(result)
        else:
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
                     **kwds):
            ExerciseFunction.__init__(
                self, solution, datasets,
                # xxx check this again
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
