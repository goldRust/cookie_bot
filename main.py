import sys
import PIL.ImageGrab as IG
from PIL import Image
import os
import csv

import multiprocessing

import mouse, time
from pynput.keyboard import Listener, KeyCode

cookie_pix = [(217,190,94),(140,148,87),(140,148,87),(115,74,43),(92,57,34),(68,41,25),(115,74,43),(115,74,43),(115,74,43),(115,74,43)]
contract = [(190,191,143),(210,208,187),(190,191,143)]
tall_bunny = [(178,165,147),(167,111,85),(164,141,114),(161,121,106)]
stripe_bunny = [(216,209,197),(156,168,147),(145,153,137),(117,136,107),(145,136,92)]
white_bunny = [(226,218,209), (234,211,164),(184,162,124),(217,169,121),(188,171,147)]
brown_bunny = [(100,89,70),(100,89,70),(90,101,90),(121,99,67),(90,101,90),(109,98,84)]
fortune_text = (173,223,47)

start_x = 0
stop_x = 1940
start_y = 80
stop_y = 1060
def main():
    processes = []
    p = multiprocessing.Process(target=run_clicks)
    p.start()
    #processes.append(p)
    q = multiprocessing.Process(target=check_cookie)
    q.start()
    #processes.append(q)
    p.join()
    q.join()
    while True:
        time.sleep(300)
        if not p.is_alive():
            p.start()
            p.join()
        if not q.is_alive():
            q.start()
            q.join()





def run_clicks():
    active = True
    while active:
        mouse.move(200, 500)
        start_mouse = mouse.get_position()
        for i in range(1000):
            time.sleep(.001)
            mouse.click()
            end_mouse = mouse.get_position()
        if end_mouse != start_mouse:
            active = False

def check_cookie():

    #cookie = Cookie_Box(x,y)
    #box = (cookie.start_x,cookie.start_y,cookie.end_x, cookie.end_y)
    spells_cast = 0
    cookies_clicked = 0
    fortunes = 0

    active = True
    while active:
        box = (start_x,start_y,stop_x,stop_y)
        im = IG.grab(box, include_layered_windows=False, all_screens=True)
        im.save(os.getcwd() + "\\cookie.png", 'PNG')
        cookie_im = Image.open("cookie.png", 'r')
        pix_list = list(cookie_im.getdata())
        n = 1940
        two_dim_pix = [pix_list[i * n:(i+1)*n] for i in range((len(pix_list)+ n - 1)//n)]

        y_index = 1

        for row in two_dim_pix:
            '''
            x_index = contains(row, tall_bunny)
            if x_index == -1:
                x_index = contains(row, stripe_bunny)
                if x_index == -1:
                    x_index = contains(row, white_bunny)
                    if x_index == -1:
                        x_index = contains(row, brown_bunny)
            '''
            x_index = contains(row, contract)

            if x_index != -1:
                print("Cookie found!")
                cookies_clicked += 1

                get_cookie(x_index,y_index)
            y_index += 1
                #mouse.move(start_mouse[0], start_mouse[1])
            start_mouse = mouse.get_position()

        if two_dim_pix[330][1238] != (17,15,24):
            spells_cast += 1
            print("Forcing the hand of fate!")
            mouse.move(904,272+start_y)
            mouse.click()
            mouse.move(200,500)
            start_mouse = mouse.get_position()

        if fortune_text in two_dim_pix[97]:
            mouse.move(1067, 97+start_y)
            mouse.click()
            fortunes += 1
            mouse.move(start_mouse[0],start_mouse[1])

        print(f"{cookies_clicked} cookies clicked.\n{spells_cast} spells cast.\n{fortunes} fortunes gained.")

        end_mouse = mouse.get_position()
        if end_mouse != start_mouse:
            print("Exiting.")
            active = False

def contains(big_list, small_list):
    for i in range(len(big_list)):
        if big_list[i:i+len(small_list)] == small_list:
            return i
    return -1


def get_cookie(x,y):
    print(x, y)
    mouse.move(x, y + start_y)
    print(mouse.get_position())
    mouse.click()
    mouse.move(200, 500)


'''
    for i in range(80):
        mouse.move(-2000, 1150 - i*5)
        time.sleep(.001)
        mouse.click()
        mouse.move(-3600, 800)
        time.sleep(.001)
        mouse.click()
'''
class Cookie_Box:
    def __init__(self,x,y):
        self.start_x = x
        self.end_x = x + 95
        self.start_y = y
        self.end_y = y + 95
        self.center_x = self.end_x - 47
        self.center_y = self.end_y - 47


if __name__ == '__main__':
    main()