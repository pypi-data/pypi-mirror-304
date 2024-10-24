from __future__ import annotations

from typing import Any, Union
from flaskomponent.css import stylesheet


class html_base:
    children: list[Union[dict, str, html_base, style]]
    kwargs: dict[str, Any]
    tagname: str
    self_closing: bool

    def __init__(self, *children: Union[dict, str, html_base, style]):
        self.kwargs = {}
        self.children = []
        for child in children:
            if isinstance(child, dict):
                self.kwargs.update(child)
            else:
                if isinstance(child, str):
                    while child.find('  ') != -1:
                        child = child.replace('  ', ' ')
                    while child.find('\n\n') != -1:
                        child = child.replace('\n\n', '\n')
                    while child.find('\n \n') != -1:
                        child = child.replace('\n \n', '\n')
                self.children.append(child)


    def render(self):
        return str(self)
    
    def __html__(self: html_base) -> str:
        return str(self)
    
    def __repr__(self: html_base) -> str:
        return str(self)

    def __str__(self) -> str:
        html_string = ''
        for item in self.children:
            if isinstance(item, dict):
                continue
            if isinstance(item, style):
                continue
            if isinstance(item, str):
                html_string += item
            else:
                html_string += str(item)

        props = ' '.join([f'{key}="{value}"' for key, value in self.kwargs.items()])
        props_section = " " + props if props else props
        if self.self_closing:
            result = f'<{self.tagname}{props_section}>'
        else:
            result = f'<{self.tagname}{props_section}>{html_string}</{self.tagname}>'

        return result

class html(html_base):
    tagname = 'html'
    self_closing = False

class script(html_base):
    tagname = 'script'
    self_closing = False

class head(html_base):
    tagname = 'head'
    self_closing = False

class body(html_base):
    tagname = 'body'
    self_closing = False

class img(html_base):
    tagname = 'img'
    self_closing = False

class meta(html_base):
    tagname = 'meta'
    self_closing = True

class style:
    tagname = 'style'
    self_closing = False

    def __init__(self, stylesheet: stylesheet):
        self.stylesheet = stylesheet

    def __html__(self):
        result = self.stylesheet.render()

        return f'<{self.tagname}>{result}</{self.tagname}>'

class title(html_base):
    tagname = 'title'
    self_closing = False

class div(html_base):
    tagname = 'div'
    self_closing = False


class select(html_base):
    tagname = 'select'
    self_closing = False


class option(html_base):
    tagname = 'option'
    self_closing = False

class h1(html_base):
    tagname = 'h1'
    self_closing = False

class h2(html_base):
    tagname = 'h2'
    self_closing = False

class h3(html_base):
    tagname = 'h3'
    self_closing = False

class h4(html_base):
    tagname = 'h4'
    self_closing = False

class p(html_base):
    tagname = 'p'
    self_closing = False

class a(html_base):
    tagname = 'a'
    self_closing = False

class button(html_base):
    tagname = 'button'
    self_closing = False

class form(html_base):
    tagname = 'form'
    self_closing = False

class input(html_base):
    tagname = 'input'
    self_closing = True

class label(html_base):
    tagname = 'label'
    self_closing = False

class ul(html_base):
    tagname = 'ul'
    self_closing = False

class li(html_base):
    tagname = 'li'
    self_closing = False

class span(html_base):
    tagname = 'span'
    self_closing = False

class nav(html_base):
    tagname = 'nav'
    self_closing = False

class header(html_base):
    tagname = 'header'
    self_closing = False

class footer(html_base):
    tagname = 'footer'
    self_closing = False


def render_html(*args):
    if len(args) == 1 and isinstance(args[0], html):
        return args[0].render()

    html_element = html(*args)
    return html_element.render()