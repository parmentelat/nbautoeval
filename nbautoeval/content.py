import markdown2

from ipywidgets import HTML, HTMLMath, Layout

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


    def widget(self):
        """
        this generic code is only about caching
        each subclass should provide their _widget_(self) method
        """      
        if self._widget_instance is None:
            self._widget_instance = self._widget_()           # pylint: disable=no-member
        return self._widget_instance


    
class TextContent(Content):
    
    def __init__(self, text, 
                 is_code=False, needs_math=False, has_markdown=False,
                 **kwds):
        super().__init__(**kwds)
        self.text = text
        self.is_code = is_code
        self.needs_math = needs_math
        self.has_markdown = has_markdown
        
    # used in particular in quiz's sanity checks    
    def __str__(self):
        return self.text

    def set_is_code(self, is_code):
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
            text = markdown2.Markdown().convert(text)
        if self.is_code:
            text = f"<pre>{text}</pre>"
        if self.css_properties:
            text = f"<span {self.style_attribute()}'>{text}</span>"
        widget_class = HTML if not self.needs_math else HTMLMath
        result = widget_class(text, layout=self.layout_dict)
        for cls in self.classes:
            result.add_class(cls)
        return result
    
class MarkdownContent(TextContent):
    
    def __init__(self, text, needs_math=False, **kwds):
        super().__init__(text, needs_math=needs_math, has_markdown=True, **kwds)
            

class CssContent(Content):

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