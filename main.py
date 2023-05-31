import cv2 as cv
import numpy as np
import pyautogui as pg
import time
from PIL import ImageGrab
import threading
import clipboard

#print("/t", pg.displayMousePosition())

def generating():
    time.sleep(5)
    while True:
        capture("chat2")
        imgGen = cv.imread("generating.png", cv.IMREAD_UNCHANGED)
        imgChat = cv.imread("chat2.png", cv.IMREAD_UNCHANGED)


        imgGen_gray = cv.cvtColor(imgGen, cv.COLOR_BGR2GRAY)
        imgChat_gray = cv.cvtColor(imgChat, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(imgGen_gray,imgChat_gray, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc1 = cv.minMaxLoc(result)

        if(max_val >= 0.95):
            time.sleep(1)
            continue
        else:
            pg.moveTo(1500,770)
            pg.click()
            break


def errorMessage():
    while True:
        capture("chat1")
        time.sleep(5)
        imgError = cv.imread("error.png", cv.IMREAD_UNCHANGED)
        imgChat = cv.imread("chat1.png", cv.IMREAD_UNCHANGED)


        imgError_gray = cv.cvtColor(imgError, cv.COLOR_BGR2GRAY)
        imgChat_gray = cv.cvtColor(imgChat, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(imgError_gray,imgChat_gray, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc1 = cv.minMaxLoc(result)

        if(max_val >= 0.95):
            pg.hotkey('ctrl', 'r')
            time.sleep(2)
            main()

    #threshold = 0.7

    #locations = np.where(result >= threshold)
    #locations = list(zip(*locations[::-1]))
    #showAll(locations, imgError, imgChat)



def showAll(locations, image, screen):

    if locations:
        imgPaste_w = image.shape[1]
        imgPaste_h = image.shape[0]
        line_color = (0,255,0)
        line_type = cv.LINE_4

        for loc in locations:
            top_left = loc
            bottom_right = (top_left[0] + imgPaste_w, top_left[1] + imgPaste_h)
            cv.rectangle(screen, top_left, bottom_right, line_color, line_type)
        cv.imshow("jj", screen)
        cv.waitKey()

def getLowestPosition(locations):
        lowestY = -999
        lowestX = 0
        for loc in locations:
             if (loc[1] > lowestY):
                  lowestY = loc[1]
                  lowestX = loc[0]
        return lowestX, lowestY
             
def capture(archivo):
        
        screenshot = ImageGrab.grab()
        screenshot.save(f'{archivo}.png')


def scroll_up():
    # Realizar desplazamiento hacia arriba
    pg.scroll(100)

def getInfo():
    capture("chat3")
    imgChat = cv.imread("chat3.png", cv.IMREAD_UNCHANGED)
    imgIcon = cv.imread("gptIcon.png", cv.IMREAD_UNCHANGED)

    imgChat_gray = cv.cvtColor(imgChat, cv.COLOR_BGR2GRAY)
    imgIcon_gray = cv.cvtColor(imgIcon, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(imgChat_gray,imgIcon_gray, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc1 = cv.minMaxLoc(result)

    if(max_val >= 0.9):
        imgChat = cv.imread("chat3.png", cv.IMREAD_UNCHANGED)
        imgPaste = cv.imread("pasteIcon.png", cv.IMREAD_UNCHANGED)

        imgChat_gray = cv.cvtColor(imgChat, cv.COLOR_BGR2GRAY)
        imgPaste_gray = cv.cvtColor(imgPaste, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(imgChat_gray,imgPaste_gray, cv.TM_CCOEFF_NORMED)
        threshold = 0.7

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        x, y = getLowestPosition(locations)
        pg.moveTo(x,y)
        
        #showAll(locations, imgPaste, imgChat)
        pg.click()
        
    else:
        scroll_up()
        time.sleep(0.5)
        getInfo()

def main():
    capture("chat")
    detectError = threading.Thread(target=errorMessage)
    detectError.start()
    message = "haz un ensayo corto"
    imgChat = cv.imread("chat.png", cv.IMREAD_UNCHANGED)
    imgInput = cv.imread("input.png", cv.IMREAD_UNCHANGED)

    img_w = imgInput.shape[0]/3
    img_h = imgInput.shape[1]/20


    imgChat_gray = cv.cvtColor(imgChat, cv.COLOR_BGR2GRAY)
    imgInput_gray = cv.cvtColor(imgInput, cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(imgChat_gray,imgInput_gray, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if(max_val > 0.9):
        pg.moveTo(max_loc[0]+img_w, max_loc[1]+img_h)
        pg.click()
        pg.write(message)
        pg.press('enter')

        generating()
        time.sleep(4)
        getInfo()
        clipboardChat = clipboard.paste()
        print(clipboardChat)
        time.sleep(5)
        main()
    else:
        main()

time.sleep(4)
main()
#errorMessage()
