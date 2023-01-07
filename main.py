import gi
import markdown_parser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Markdown editor")
        self.grid = Gtk.Grid()
        self.initiate_key_press_sensing()
        self.load_css()
        #self.draw_menu()
        self.draw_body()
    
    def on_update(self, gparamstring):
        self.markdown_output.set_markup(
            markdown_parser.markdown_to_gtk(
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
    
    # UI Logic
    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager
    
    def load_css(self):
        with open('main.css', 'r') as file:
            css = bytes(file.read(), 'utf8')
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    # Key Event Logic
    def initiate_key_press_sensing(self):
        self.connect("key-press-event",self.key_press_event)
        self.connect("key-release-event",self.key_release_event)
        self.key_buffer = {}
    
    def key_press_event(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        self.key_buffer[keyname] = True
        self.perform_shortcut_action()
    
    def key_release_event(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        self.key_buffer[keyname] = False
    
    # Shortcut Logic

    def perform_shortcut_action(self):
        """
        Reads the dict key-buffer 
        and checks which shortcut was pressed
        by taking Ctrl, Shift as higher precedence
        """
        if self.key_buffer['Control_L']:
            if self.key_buffer['s']:
                self.save()
            elif self.key_buffer['x']:
                self.cut()
            elif self.key_buffer['v']:
                self.paste()
    
    def save(self):
        # TODO Open a save window to take user input
        print("save")
    
    def cut(self):
        # TODO Delete contents and keep in clipboard
        print("cut")
    
    def paste(self):
        # TODO Print contents from clipboard
        # TODO Add logic for adding image when pasted
        print("paste")

window = MainWindow()
window.set_default_size(800, 600)
window.set_position(Gtk.WindowPosition.CENTER)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()