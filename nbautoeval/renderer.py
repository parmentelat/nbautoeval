import pprint

from .content import TextContent

r"""
various ways to render a Python object

a (result) Renderer is expected to provide a render() method on all python objects

in turn render() is expected to return a "Content"
"""


class Renderer:
    """
    default renderer:
    * on classes that own a `_render_content_` method, use that;
      it should return a TextContent
    * otherwise use repr()
    """

    def __init__(self):
        pass

    def render(self, python_object):
        if hasattr(python_object, "_render_content_"):
            return python_object._render_content_()
        else:
            return (TextContent(repr(python_object))
                    .add_css_properties({'align-self': 'center'})
                    .set_is_code(not isinstance(python_object, Exception)))
                                       

    def __repr__(self):
        return f"<Renderer {type(self)}>"


class PPrintRenderer(Renderer):
    # the default for compact with pprint is False, but we favour True
    def __init__(self, *, width=80, indent=2, compact=True):
        self.width = width
        self.indent = indent
        self.compact = compact
    
    def render(self, python_object):
        return (TextContent(
                    pprint.pformat(python_object, compact=self.compact,
                                   indent=self.indent, width=self.width))
                    .add_css_properties({'align-self': 'center'})
                    .set_is_code(True))


class MultilineRenderer(Renderer):
    def render(self, python_object):
        if not isinstance(python_object, str):
            python_object = repr(python_object)
        return TextContent("\\n\n".join(python_object.split("\n")))
