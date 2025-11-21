from _app import Bottle, request, debug
from widgets import widgets

app = Bottle()
debug(False)
@app.route('/_reload', method='POST') #type:ignore
def reload_widget():
    data = request.json
    wid = data.get('id') #type:ignore
    widget = widgets.get(wid)
    if not widget:
        return "Widget not found", 404
    return widget.to_html()


@app.route('/_event', method='POST') #type:ignore
def handle_event():
    data = request.json
    wid = data.get('id') #type:ignore
    new_value = data.get('value', None) #type:ignore
    widget = widgets.get(wid)
    print("Making event...", wid)
    if not widget:
        return "Widget not found", 404

    if hasattr(widget, 'trigger'):
        print("Triggering...")
        if new_value is not None:
            result = widget.trigger(new_value)
        else:
            result = widget.trigger()
        print("Triggered!")
        # If the handler returns a widget, return its HTML
        if result and hasattr(result, 'to_html'):
            return result.to_html()
        # Otherwise, return the widget's HTML
        return widget.to_html()
    
    return "Widget has no trigger method", 400