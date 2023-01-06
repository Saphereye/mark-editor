import gi
import parser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Markdown editor")
        grid = Gtk.Grid()
        
        self.input_scroll = Gtk.ScrolledWindow()
        self.user_input = Gtk.TextView()
        self.text_buffer = self.user_input.get_buffer()
        self.text_buffer.set_text("Input")
        self.user_input.set_hexpand(True)
        self.user_input.set_vexpand(True)
        self.text_buffer.connect("changed", self.on_update)
        self.input_scroll.add(self.user_input)
        grid.attach(self.input_scroll, 0, 0, 1, 1)

        self.markdown_scroll = Gtk.ScrolledWindow()
        self.markdown_output = Gtk.Label()
        self.markdown_output.set_markup("<i>Output</i>")
        self.markdown_output.set_hexpand(True)
        self.markdown_output.set_vexpand(True)
        self.markdown_scroll.add(self.markdown_output)
        grid.attach(self.markdown_scroll, 1, 0, 1, 1)

        self.add(grid)
    
    def on_update(self, gparamstring):
        self.markdown_output.set_markup(
            parser.markdown_to_gtk(
                self.text_buffer.get_text(
                    self.text_buffer.get_start_iter(),
                    self.text_buffer.get_end_iter(),
                    True
                )
            )
        )

window = MainWindow()
window.set_default_size(800, 600)
window.set_border_width(10)
window.set_position(Gtk.WindowPosition.CENTER)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()