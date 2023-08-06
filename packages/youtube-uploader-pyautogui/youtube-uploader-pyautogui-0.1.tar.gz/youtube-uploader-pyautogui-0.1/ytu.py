from pyautogui import click, typewrite,  doubleClick, hotkey, press, displayMousePosition
import webbrowser as wb
import time

#displayMousePosition()
def youtube_upload(file_loc, title):

    wb.open("https://studio.youtube.com/")

    time.sleep(2)
    click(2395, 131)
    time.sleep(0.3)
    click(2340, 176)
    time.sleep(0.3)
    click(1280, 877)
    time.sleep(0.3)
    click(1142, 425)
    time.sleep(0.3)
    typewrite(file_loc,0.05)
    time.sleep(0.3)
    #doubleClick(503,586)
    time.sleep(0.3)
    click(1136, 394)
    time.sleep(5)
    hotkey('ctrl', 'a')
    press('delete')
    time.sleep(0.3)
    typewrite(title,0.05)
    time.sleep(0.3)
    click(865, 518)
    time.sleep(0.3)
    typewrite(title,0.05)
    time.sleep(0.3)
    click(1716, 1335)
    time.sleep(0.3)
    click(1716, 1335)
    time.sleep(0.3)
    click(1716, 1335)
    time.sleep(0.3)
    click(1716, 1335)

    print("Job Done!")

youtube_upload(input("[+] Enter Location Of File:\n"),input("[+] Enter Title/Description Of Video:\n"))