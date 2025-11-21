import uuid
import time

widgets = {}  # store all widgets by id

class BWidget:
    def __init__(self, content='', prop=None, tag='div', reload=False):
        self.tag = tag or 'div'
        self.id = self.tag + str(uuid.uuid4())
        self.content = content
        self.prop = prop or []
        widgets[self.id] = self
        self.reload = reload

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop + (['reload'] if self.reload else []))
        return f'<{self.tag} id="{self.id}" {prop_str}>{self.content}</{self.tag}>'

    def update(self, new_content):
        self.content = new_content
        return self.content


class BButton(BWidget):
    def __init__(self, content='', prop=None, handler=None):
        super().__init__(content, prop, tag='button')
        self.handler = handler or (lambda: print(self.id, "clicked!"))

    def set_handler(self, handler):
        self.handler = handler

    def trigger(self, *args, **kwargs):
        result = self.handler(*args, **kwargs)
        return result if hasattr(result, 'to_html') else self

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop)
        return f'<button id="{self.id}" {prop_str} click reload>{self.content}</button>'


class BTimeWidget(BWidget):
    def to_html(self):
        self.content = f'Time: {time.strftime("%H:%M:%S")}'
        prop_str = ' '.join(self.prop + ['reload'])
        return f'<div id="{self.id}" {prop_str}>{self.content}</div>'


class BValueWidget(BWidget):
    def __init__(self, value='', prop=None, onchange=None):
        super().__init__(str(value), prop, tag='input-text')
        self.onchange = onchange or (lambda val: None)

    def set_onchange(self, handler):
        self.onchange = handler

    def trigger(self, new_value=None):
        if new_value is not None:
            self.content = str(new_value)
        return self.onchange(self.content)

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop)
        return f'<input type="text" id="{self.id}" value="{self.content}" {prop_str} data-event="change"/>'

class BCheckbox(BWidget):
    def __init__(self, checked=False, prop=None, onchange=None):
        super().__init__('', prop, tag='checkbox')
        self.checked = checked
        self.onchange = onchange or (lambda val: None)

    def set_onchange(self, handler):
        self.onchange = handler

    def trigger(self, new_value=None):
        if new_value is not None:
            self.checked = bool(new_value)
        return self.onchange(self.checked)

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop)
        checked_attr = 'checked' if self.checked else ''
        return f'<input type="checkbox" id="{self.id}" {prop_str} {checked_attr} data-event="change"/>'


class BSlider(BWidget):
    def __init__(self, value=0, min_val=0, max_val=100, step=1, prop=None, onchange=None):
        super().__init__(str(value), prop, tag='slider')
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.onchange = onchange or (lambda val: None)

    def set_onchange(self, handler):
        self.onchange = handler

    def trigger(self, new_value=None):
        if new_value is not None:
            self.value = int(new_value)
            self.content = str(self.value)
        return self.onchange(self.value)

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop)
        return f'<input type="range" id="{self.id}" value="{self.value}" min="{self.min_val}" max="{self.max_val}" step="{self.step}" {prop_str} data-event="change"/>'


class BDropdown(BWidget):
    def __init__(self, options=None, selected=None, prop=None, onchange=None):
        super().__init__('', prop, tag='dropdown')
        self.options = options or []
        self.selected = selected
        self.onchange = onchange or (lambda val: None)

    def set_onchange(self, handler):
        self.onchange = handler

    def trigger(self, new_value=None):
        if new_value is not None:
            self.selected = new_value
        return self.onchange(self.selected)

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop)
        options_html = ''.join(f'<option value="{opt}" {"selected" if opt==self.selected else ""}>{opt}</option>' for opt in self.options)
        return f'<select id="{self.id}" {prop_str} data-event="change">{options_html}</select>'


class BLabel(BWidget):
    def __init__(self, text='', prop=None, tag='label'):
        super().__init__(text, prop)

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop)
        return f'<span id="{self.id}" {prop_str}>{self.content}</span>'


class BContainer(BWidget):
    def __init__(self, children=None, prop=None):
        super().__init__('', prop)
        self.children = children or []

    def to_html(self):
        prop_str = ' '.join(str(p) for p in self.prop + ['reload'])
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<div id="{self.id}" {prop_str}>{children_html}</div>'
