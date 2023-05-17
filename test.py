#!/usr/bin/env pythonw

from Cocoa import NSObject, NSApplication, NSApp, NSWindow, NSButton, NSSound, NSFontManager, NSTextField, \
    NSTextFieldSquareBezel, NSFont
from PyObjCTools import AppHelper

class AlwaysOnTopApp(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        print("Hello, World!")

    def newActivity_(self, sender):
        print("New Activity button clicked!")

        # Create text field for text entry
        text_field = NSTextField.alloc().initWithFrame_(((10.0, 100.0), (100.0, 22.0)))
        text_field.setBezelStyle_(NSTextFieldSquareBezel)
        text_field.setPlaceholderString_("Enter text")
        text_field.setFont_(NSFont.fontWithName_size_("Garamond", 14))
        text_field.setEditable_(True)
        text_field.setSelectable_(True)
        text_field.setBordered_(True)
        text_field.setBezeled_(True)

        # Create text field for number entry
        number_field = NSTextField.alloc().initWithFrame_(((120.0, 100.0), (60.0, 22.0)))
        number_field.setBezelStyle_(NSTextFieldSquareBezel)
        number_field.setPlaceholderString_("Enter number")
        number_field.setFont_(NSFont.fontWithName_size_("Garamond", 14))
        number_field.setEditable_(True)
        number_field.setSelectable_(True)
        number_field.setBordered_(True)
        number_field.setBezeled_(True)

        self.win.contentView().addSubview_(text_field)
        self.win.contentView().addSubview_(number_field)

        text_field.becomeFirstResponder()

    def quitApp_(self, sender):
        NSApp().terminate_(sender)


def main():
    app = NSApplication.sharedApplication()
    delegate = AlwaysOnTopApp.alloc().init()
    NSApp().setDelegate_(delegate)

    win = NSWindow.alloc()
    frame = ((200.0, 300.0), (250.0, 160.0))
    win.initWithContentRect_styleMask_backing_defer_(frame, 15, 2, 0)
    win.setTitle_("AlwaysOnTopApp")
    win.setLevel_(3)  # floating window

    delegate.win = win  # Set win as an attribute of the delegate
    
    new_activity = NSButton.alloc().initWithFrame_(((10.0, 10.0), (230.0, 25.0)))
    win.contentView().addSubview_(new_activity)
    new_activity.setBezelStyle_(4)
    new_activity.setTitle_("New Activity")
    new_activity.setTarget_(app.delegate())
    new_activity.setAction_("newActivity:")

    quit_app = NSButton.alloc().initWithFrame_(((10.0, 30.0), (230.0, 25.0)))
    win.contentView().addSubview_(quit_app)
    quit_app.setBezelStyle_(4)
    quit_app.setTitle_("Quit App")
    quit_app.setTarget_(app.delegate())
    quit_app.setAction_("quitApp:")

    # Set Cormorant font for buttons
    font_manager = NSFontManager.sharedFontManager()
    Cormorant_font = font_manager.fontWithFamily_traits_weight_size_("Cormorant", 0, 5, 18.0)
    new_activity.setFont_(Cormorant_font)
    quit_app.setFont_(Cormorant_font)

    beep = NSSound.alloc()
    beep.initWithContentsOfFile_byReference_("/System/Library/Sounds/Tink.Aiff", 1)
    new_activity.setSound_(beep)

    win.display()
    win.orderFrontRegardless()

    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()
