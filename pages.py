from bottle import Bottle
from app import app

class Page:
    """
    Base class for pages.
    Each page should define a `to_html()` method that returns full HTML content.
    """

    def __init__(self, widgets=None, route='/'):
        # widgets is a list of widget instances to render
        self.widgets = widgets or []
        self.route = route
        self.app = app

    def to_html(self):
        """
        Render all widgets and include JS polling/event logic.
        """
        widget_html = '\n'.join(w.to_html() for w in self.widgets)

        return f'''
<html>
<head><title>Bottle FUI Example</title></head>
<body>
{widget_html}

<script>
// Poll reloadable widgets
function reloadWidget(id) {{
    fetch('/_reload', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{id:id}})
    }}).then(r=>r.text()).then(html=>{{
        const el = document.getElementById(id);
        if(el && el.outerHTML === html) el.outerHTML = html;
    }}).catch(err=>console.error(id, ':', err));
}}

setInterval(()=>{{
    document.querySelectorAll('[reload]').forEach(el=>{{ reloadWidget(el.id); }});
}}, 100);

// Button events
function setupButtonEvents() {{
    // Select all elements that have a 'click' attribute
    document.querySelectorAll('[click]').forEach(el => {{
        el.onclick = () => {{
            console.log(el.id, "triggering...");
            fetch('/_event', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{id: el.id}})
            }})
            .then(r => r.text())
            .then(html => {{
                el.outerHTML = html;       // replace with updated HTML
                setupButtonEvents();       // rebind after replacement
            }})
            .catch(err => console.error(err));
            console.log(el.id, "triggered!");
        }}
    }});
}}

// Initial bind
setupButtonEvents();

// Input / checkbox / range / select events
function setupInputEvents() {{
    document.querySelectorAll('[data-event="change"]').forEach(el=>{{
        const eventType = el.tagName === "SELECT" ? "change" : "input";
        el.addEventListener(eventType, () => {{
            let value;
            if(el.type === "checkbox") value = el.checked;
            else if(el.type === "range") value = el.value;
            else value = el.value;

            fetch('/_event', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{id: el.id, value: value}})
            }}).catch(err=>console.error(err));
        }});
    }});
}}
setupInputEvents();
</script>

</body>
</html>
'''

    def register(self, **kwargs):
        """
        Register this page to a route on a Bottle app.
        """
        page = self  # closure

        @self.app.route(self.route, **kwargs) #type:ignore
        def render(**_kwargs):
            return page.to_html()
