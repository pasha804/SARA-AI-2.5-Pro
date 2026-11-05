import ctypes
import time
import uiautomation as auto

user32 = ctypes.windll.user32
h_desk = user32.OpenDesktopW('default', 0, False, 0x01FF)
user32.SetThreadDesktop(h_desk)

hwnd = 264486
user32.ShowWindow(hwnd, 9)
user32.SetForegroundWindow(hwnd)
time.sleep(0.3)

win = auto.ControlFromHandle(hwnd)
doc = win.DocumentControl()

# Click search box
search_box = doc.EditControl(Name='Search or start a new chat')
if search_box.Exists(2):
    search_box.Click()
    time.sleep(0.2)
    # Clear search box
    auto.SendKeys('{Ctrl}a{Back}')
    time.sleep(0.2)
    # Type BSCS 1-M and press enter
    auto.SendKeys('BSCS 1-M{Enter}')
    time.sleep(1.5)
    print("Navigated to BSCS 1-M!")
else:
    print("Search box not found")

