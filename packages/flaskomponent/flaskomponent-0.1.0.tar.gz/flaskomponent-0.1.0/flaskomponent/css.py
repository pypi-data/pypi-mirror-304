def css(item):
    return item.__css__()


class css_rule:
    def __init__(self, name, **rules):
        self.name = name
        self.rules = rules

    def __css__(self):
        css_rules = "; ".join([
            f"{key.replace('_', '-')}: {value}"
            for key, value in self.rules.items()
        ])
        return f"{self.name} {{{css_rules};}}"

class stylesheet:
    def __init__(self):
        self.rules = []

    def add_style(self, rule: css_rule):
        self.rules.append(rule)

        return self

    def render(self):
        style = " ".join([css(style) for style in self.rules])
        while style.find('  ') != -1:
            style = style.replace('  ', ' ')
        return style
