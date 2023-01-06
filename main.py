import gi
import parser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

# This would typically be its own file
MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
        <item>
            <attribute name="label">About</attribute>
            <attribute name="action">app.about</attribute>
        </item>
        <item>
            <attribute name="label">Quit</attribute>
            <attribute name="action">app.quit</attribute>
        </item>
    </section>
  </menu>
</int
"""


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Markdown editor")
        self.grid = Gtk.Grid()

        self.draw_menu()
        self.draw_body()
    
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
    
    def draw_menu(self):
        bar = Gtk.Toolbar()

        refresh_btn = Gtk.ToolButton(Gtk.STOCK_REFRESH)
        refresh_btn.connect("clicked", self.on_refresh_clicked)

        save_btn = Gtk.ToolButton(Gtk.STOCK_SAVE)
        save_btn.connect("clicked", self.on_refresh_clicked)

        zoom_in_btn = Gtk.ToolButton(Gtk.STOCK_ZOOM_IN)
        zoom_in_btn.connect("clicked", self.on_refresh_clicked)

        zoom_out_btn = Gtk.ToolButton(Gtk.STOCK_ZOOM_OUT)
        zoom_out_btn.connect("clicked", self.on_refresh_clicked)

        bar.insert(refresh_btn, 0)
        bar.insert(save_btn, 1)
        bar.insert(zoom_in_btn, 2)
        bar.insert(zoom_out_btn, 3)

        self.grid.attach(bar, 0, 0, 1, 1)
    
    def on_refresh_clicked(self, button):
        self.text_buffer.set_text("")
    
    def draw_body(self):        
        self.input_scroll = Gtk.ScrolledWindow()
        self.user_input = Gtk.TextView()
        self.text_buffer = self.user_input.get_buffer()
        self.text_buffer.set_text("Input")
        self.user_input.set_hexpand(True)
        self.user_input.set_vexpand(True)
        self.text_buffer.connect("changed", self.on_update)
        self.input_scroll.add(self.user_input)
        self.grid.attach(self.input_scroll, 0, 1, 1, 1)

        self.markdown_scroll = Gtk.ScrolledWindow()
        self.markdown_output = Gtk.Label()
        self.markdown_output.set_markup("<i>Output</i>")
        self.markdown_output.set_hexpand(True)
        self.markdown_output.set_vexpand(True)
        self.markdown_scroll.add(self.markdown_output)
        self.grid.attach(self.markdown_scroll, 1, 1, 1, 1)

        self.add(self.grid)
    
    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

window = MainWindow()
window.set_default_size(800, 600)
window.set_border_width(10)
window.set_position(Gtk.WindowPosition.CENTER)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()