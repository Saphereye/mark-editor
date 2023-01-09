import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio

class SaveWindow(Gtk.Window):
    def __init__(self) -> None:
        super().__init__()
        self.draw_header_bar()
    
    # Header Bar logic
    def draw_header_bar(self):
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Mark Editor"
        self.set_titlebar(header_bar)
    
    # Input for file name

    # Button for confirmation

if __name__ == "__main__":
    window = SaveWindow()
    window.set_default_size(400, 300)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()