import AppKit
from PyObjCTools import AppHelper
import time

class AppDelegate(AppKit.NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # Use a time delay to ensure the window is available
        time.sleep(0.1)
        
        # Get the main window of the application
        window = AppKit.NSApp().mainWindow()
        if window:
            # Set the window behavior to always stay on top
            window.setCollectionBehavior(AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces |
                                         AppKit.NSWindowCollectionBehaviorStationary |
                                         AppKit.NSWindowCollectionBehaviorIgnoresCycle)
            
            # Create a button
            button = AppKit.NSButton.alloc().initWithFrame_(AppKit.NSMakeRect(20, 20, 100, 30))
            button.setTitle_("New Activity")
            button.setBezelStyle_(4)
            button.setTarget_(self)
            button.setAction_("buttonClicked:")
            
            # Add the button to the window
            window.contentView().addSubview_(button)
        
    def buttonClicked_(self, sender):
        # This method will be called when the button is clicked
        print("New Activity button clicked!")

if __name__ == "__main__":
    app = AppKit.NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
