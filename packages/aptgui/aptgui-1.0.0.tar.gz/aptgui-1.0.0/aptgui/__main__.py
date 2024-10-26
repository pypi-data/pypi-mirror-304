from . import App, Col, Frame, Label, Row, TextBox, Window

greeting: Label

App(
    Window(
        Col(
            Frame(
                Row(
                    Label(text="Name:"),
                    TextBox(
                        on_change=lambda textbox: setattr(
                            greeting, "text", f"Hello, {textbox.value}!"
                        ),
                        width=32,
                    ),
                ),
                Row(greeting := Label(text="Hello, Stranger!"), ...),
                Col(),
                Col(weight=1),
            ),
            weight=1,
        ),
        title="Hello App",
    ),
).run()
