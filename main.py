from widgets import BWidget, BButton, BTimeWidget, BValueWidget, BCheckbox, BSlider, BDropdown, BLabel, BContainer
from pages import Page
from app import app  # your Bottle app with /_reload and /_event

# --- Create widgets ---
w_text = BWidget("Hello! I am static text")
w_time = BTimeWidget()
w_button = BButton("Click Me!")
w_input = BValueWidget("Type here...")
w_checkbox = BCheckbox(False)
w_slider = BSlider(50, min_val=0, max_val=100, step=5)
w_dropdown = BDropdown(options=["Option 1", "Option 2", "Option 3"], selected="Option 2")
w_label = BLabel("I am a label")

# Nested container example
container = BContainer(children=[w_label, w_button])

def on_button_clicked():
    with open('logs.log', 'a') as f:
        f.write("Clicked\n")
    w_text.update("Button clicked!")
w_button.set_handler(on_button_clicked)

# --- Handlers ---
def on_input_change(val):
    w_text.update(f"You typed: {val}")

w_input.set_onchange(on_input_change)

def on_checkbox_change(checked):
    w_label.update(f"Checkbox is {'checked' if checked else 'unchecked'}")

w_checkbox.set_onchange(on_checkbox_change)

def on_slider_change(val):
    w_label.update(f"Slider value: {val}")

w_slider.set_onchange(on_slider_change)

def on_dropdown_change(selection):
    w_label.update(f"Dropdown selected: {selection}")

w_dropdown.set_onchange(on_dropdown_change)

# --- Create page ---
showcase_page = Page(widgets=[w_text, w_time, w_input, w_checkbox, w_slider, w_dropdown, container])
showcase_page.register()
app.run(host='127.0.0.1', port=8080)
