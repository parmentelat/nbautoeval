# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     cell_metadata_json: true
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: false
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: false
# ---

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %%
from nbautoeval import (
    TextContent, CodeContent, MathContent, MarkdownContent, 
    MarkdownMathContent)

# %% {"cell_style": "split"}
TextContent(r"""some basic content
<br> with html tags""").widget()

# %% {"cell_style": "split"}
MathContent(
"""with inline math $\forall x\in\mathbb{R}$""").widget()

# %%
MathContent(r"mutli-line is $$\phi: x \rightarrow e^x$$ supported as well").widget()

# %%
MathContent("but with `MathContent` **markdown is *not* supported**").widget()

# %% {"cell_style": "center"}
# of course this is doable with markdown as well
# but occasionally this can come in handy

CodeContent(r"""# CodeContent is designed for content
# that comes with a single big chunk of code
def fact(n):
    if n <= 1:
        return 1
    else:
        return n*fact(n-1)""").widget()

# %%
# TextContent(r"""*markdown* won't work as is""").widget()
MarkdownContent(r"""*markdown* **does work** work in `MarkdownContent`""").widget()

# %%
# now the tricky one
MarkdownContent(r"""it's expected that here **math won't show properly** $\forall$""").widget()

# %%
# that's the default, it has support for math and markdown
MarkdownMathContent(r"""markdown **and math** $\forall x \in\mathbb{C}$""").widget()

# %%
MarkdownMathContent(r"""markdown **and math** $$\forall x \in\mathbb{C}$$ on multiple lines""").widget()
