import pprint

from .args import ArgsTupleDict
from .helpers import commas
from .content import TextContent

class Call:

    def __init__(self, function, args: ArgsTupleDict):
        self.function = function
        self.args = args


#
class CallRenderer:

    def __init__(self, *,
                 is_code=True, show_function=True, prefix="", postfix="",
                 max_width=0, css_properties=None):

        self.is_code = is_code
        self.show_function = show_function
        self.prefix = prefix
        self.postfix = postfix
        self.max_width = max_width
        self.css_properties = css_properties if css_properties is not None else {}


    def __repr__(self):
        result =  f"<CallRenderer"
        if self.show_function: result += f" show_function={self.show_function}"
        if self.max_width: result += f" m_w={self.max_width}"
        if self.prefix: result += f" pre={self.prefix}"
        if self.postfix: result += f" post={self.postfix}"
        result += ">"
        return result


    def visible_function_name(self, call):
        if not self.show_function:
            return None
        function_name = self.show_function
        if function_name is True:
            function_name = call.function.__name__
        return function_name


    def render(self, call: Call):
        text = ', '.join(call.args.tokens())
        # show_function can be either a function name to display
        # or just True in which case we compute the name
        # of the call's function attribute
        function_name = self.visible_function_name(call)
        if function_name:
            text = f"{function_name}({text})"
        text = f"{self.prefix}{text}{self.postfix}"
        result = (TextContent(text)
                  .add_css_properties(self.css_properties)
                  .add_css_properties({'align-self': 'center'}))
        if self.max_width:
            result.add_layout({'max-width': f"{self.max_width}em"})
        result.set_is_code(self.is_code)
        return result




class PPrintCallRenderer(CallRenderer):
    def __init__(self, width=80, indent=2, compact=True, *args, **kwds):
        self.width = width
        self.indent = indent
        self.compact = compact
        super().__init__(*args, **kwds)


    def render(self, call: Call):
        # try to render with no width limit, if it fits it's OK
        raw_content = super().render(call)
        simple_case = raw_content.text
        if len(simple_case) <= self.width:
            return raw_content
        # else
        indent = self.indent
        width = self.width
        sep = indent*' '
        html = ""
        html += self.prefix
        function_name = self.visible_function_name(call)
        if function_name:
            html += function_name + "(\n"
        def indent_pformat(pformat_result):
            return sep + pformat_result.replace("\n", "\n"+sep)
        args_tokens = [
            pprint.pformat(arg, width=width-indent, indent=indent)
            for arg in call.args.args]
        keyword_tokens = [
            f"{k}={pprint.pformat(v, width=width-indent, indent=indent)}"
            for (k, v) in call.args.keywords.items()]
        tokens = [indent_pformat(x) for x in args_tokens + keyword_tokens]
        html += (",\n").join(tokens)
        if function_name:
            html += ")\n"
        html += self.postfix
        return (TextContent(html, css_properties=self.css_properties)
                .set_is_code(self.is_code))


class IsliceRenderer(PPrintCallRenderer):

    @staticmethod
    def pretty_slice(generator_args):
        if not generator_args.islice:
            return "all results"
        if len(generator_args.islice) == 1:
            end, = generator_args.islice
            return f"iters →{end}"
        if len(generator_args.islice) == 2:
            beg, end = generator_args.islice
            if beg is not None:
                return f"iters {beg}→{end}"
            else:
                return f"iters →{end}"
        if len(generator_args.islice) == 3:
            beg, end, step = generator_args.islice
            if beg is not None:
                return f"iters {beg}→{end}/{step}"
            else:
                return f"iters →{end}/{step}"
        return f"ERROR: unknown islice {generator_args.islice}"

    # by design this should be called on Call objects
    # whose Args instance is a GeneratorArgs
    def render(self, generator_call):
        generator_args = generator_call.args
        default_content = super().render(generator_call)
        if generator_args.islice is None:
            return default_content
        # xxx not super clean...
        default_content.text += f"\n<b>{self.pretty_slice(generator_args)}</b>"
        return default_content

