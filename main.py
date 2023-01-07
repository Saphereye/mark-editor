#!/usr/bin/env python3

import gi
import markdown_parser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Markdown editor")
        self.box = Gtk.HBox()
        self.pane1 = Gtk.HPaned()
        self.pane2 = Gtk.HPaned()
        self.initiate_key_press_sensing()
        self.load_css()
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
    
    def draw_body(self):     
        self.input_scroll = Gtk.ScrolledWindow()
        self.user_input = Gtk.TextView()
        self.text_buffer = self.user_input.get_buffer()
        self.text_buffer.set_text("Input")
        self.text_buffer.connect("changed", self.on_update)
        self.input_scroll.add(self.user_input)
        self.pane1.add(self.input_scroll)
        self.pane1.add(self.pane2)

        self.markdown_scroll = Gtk.ScrolledWindow()
        self.markdown_output = Gtk.Label()
        self.markdown_output.set_markup("<i>Output</i>")
        self.markdown_scroll.add(self.markdown_output)
        self.pane2.add(self.markdown_scroll)

        self.box.pack_start(self.pane1, True, True, 0)
        self.input_scroll.set_size_request(WINDOW_WIDTH//3, -1)
        self.add(self.box)
    
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
window.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
window.set_position(Gtk.WindowPosition.CENTER)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()