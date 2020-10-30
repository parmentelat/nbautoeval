# an earlier version was relying on markdown2
#from myst_parser.main import to_html, default_parser

from markdown_it import MarkdownIt

from ipywidgets import HTML, HTMLMath, Layout, Image

class Content:

    """
    this class is what a renderer returns
    it models what will ultimately go into a visible Area, that is to say
    . css properties
    . classes
    . a layout (in the ipywidgets sense), here we model this as a dictionary

    the most useful verions of this is TextContent, that has
    . a textual contents
    . whether it is code
    . whether it contains math


    this is materialized by its widget() method that should return an ipywidget
    """

    def __init__(self, *, css_properties=None, classes=None, layout_dict=None):
        self.css_properties = css_properties or {}
        self.classes = classes or []
        self.layout_dict = layout_dict or {}
        self._widget_instance = None

    def __repr__(self):
        return (f"<{type(self).__name__} with {len(self.css_properties)} css props "
                f"{len(self.classes)} classes> "
                f"and {len(self.layout_dict)} items in its ipywidgets layout")

    def style(self):
        return "".join(f"{k}:{v};" for (k, v) in self.css_properties.items())
    def style_attribute(self):
        return f'style="{self.style()}"' if self.css_properties else ''



    def add_css_properties(self, css_properties: dict):
        self.css_properties.update(css_properties)
        return self

    def add_class(self, cls):
        self.classes.append(cls)
        return self

    def add_classes(self, classes):
        self.classes.extend(classes)
        return self

    def add_layout(self, layout_dict):
        self.layout_dict.update(layout_dict)
        return self

    # default needed in some corner cases; must return self
    def set_is_code(self, *_):
        return self

    def widget(self):
        """
        this generic code is only about caching
        each subclass should provide their _widget_(self) method
        """
        if self._widget_instance is None:
            self._widget_instance = self._widget_()           # pylint: disable=no-member
        return self._widget_instance



class TextContent(Content):
    '''
    the generic mechanics to turn a text into a widget
    several settings are available, which by default
    are all turned off

    is_code: will cause the whole content to be taken as code
    needs_math: will create a HTMLMath widget instead of plain HTML
    has_markdown: text first goes through a markdown stage
    '''
    def __init__(self, text,
                 is_code=False, needs_math=False, has_markdown=False,
                 **kwds):
        super().__init__(**kwds)
        # make yaml more robust, especially with answers like 'no'
        # that, when not quoted in yaml, produce False that is a bool
        if not isinstance(text, str):
            print(f"WARNING: building a TextContent from non-str {text}")
            text = str(text)
        self.text = text
        self.is_code = is_code
        self.needs_math = needs_math
        self.has_markdown = has_markdown

    # used in particular in quiz's sanity checks
    def __str__(self):
        return self.text

    def set_is_code(self, is_code):
        """
        the set_ methods allow to alter the object with chained statements
        my_content.set_is_code().set_needs_math()
        """
        self.is_code = is_code
        return self

    def set_needs_math(self, needs_math):
        self.needs_math = needs_math
        return self

    def set_has_markdown(self, has_markdown):
        self.has_markdown = has_markdown
        return self

    def _widget_(self):

        text = self.text
        if self.has_markdown:
            parser = MarkdownIt("commonmark")
            text = parser.render(text)
        if self.is_code:
            text = f"<pre>{text}</pre>"
        if self.css_properties:
            text = f"<span {self.style_attribute()}'>{text}</span>"
        widget_class = HTML if not self.needs_math else HTMLMath
        result = widget_class(text, layout=self.layout_dict)
        for cls in self.classes:
            result.add_class(cls)
        return result

# get predefined settings just by the class name
class CodeContent(TextContent):

    def __init__(self, text, **kwds):
        super().__init__(text, **kwds)
        self.is_code = True

class MathContent(TextContent):

    def __init__(self, text, **kwds):
        super().__init__(text, **kwds)
        self.needs_math = True

class MarkdownContent(TextContent):
    def __init__(self, text, **kwds):
        super().__init__(text, **kwds)
        self.has_markdown = True

class MarkdownMathContent(TextContent):
    """
    most useful - most common
    """
    def __init__(self, text, **kwds):
        super().__init__(text, **kwds)
        self.has_markdown = True
        self.needs_math = True


class CssContent(Content):
    """
    dedicated to inject CSS into HTML through
    a <style> tag that has display='none'
    """

    def __init__(self, plain_css, **kwds):
        self.plain_css = plain_css
        super().__init__(**kwds)

    def __repr__(self):
        return f"<CssContent {self.plain_css}>"

    def _widget_(self):
        html = f"<style>{self.plain_css}</style>"
        return HTML(html, layout={'display': 'none'})


class ResultContent(Content):

    def __init__(self, boolean, **kwds):
        self.boolean = boolean
        super().__init__(**kwds)
        self.css_properties['align-self'] = 'center'


    def _widget_(self):
        symbol = "fa-check" if self.boolean else "fa-close"

        html = f'<span {self.style_attribute()} class="fa {symbol}"></span>'
        result = HTML(html)
        result.add_class('result')
        result.add_class(self.the_class())
        for cls in self.classes:
            result.add_class(cls)
        return result


    def the_class(self):
        return 'ok' if self.boolean else 'ko'

class ImshowContent(Content):
    """
    a numpy (2d) ndarray, with a (css) width
    """

    def __init__(self, ndarray, css_width, cmap, **kwds):
        self.ndarray = ndarray
        self.css_width = css_width
        self.cmap = cmap
        super().__init__(**kwds)

    def _widget_(self):
        # using a BytesIO to perform imsave in memory
        from matplotlib.pyplot import imsave
        import base64
        import io
        import tempfile
        with io.BytesIO() as temp:
            kwds = {}
            if self.cmap is not None:
                kwds['cmap'] = self.cmap
            imsave(temp, self.ndarray, **kwds)
            temp.seek(0)
            image_bytes = temp.read()
        # must be a str
        b64repr = base64.b64encode(image_bytes).decode(encoding="ascii")
        html = (f"<img"
                f" width='{self.css_width}' "
                f" style='image-rendering: pixelated'"
                f" src='data:image/png; base64, {b64repr}'/>")
        result = HTML(html)
        for cls in self.classes:
            result.add_class(cls)
        return result
