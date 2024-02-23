import pytesseract
import pyautogui
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from threading import Thread
import random
import keyboard
from random import choice, randint
import time
from time import sleep
import PySimpleGUI as sg
import win32com,win32com.client
shell=win32com.client.Dispatch('WScript.Shell')
import win32gui
import win32con
import requests
from PIL import Image
import cv2
import pyautogui
import numpy as np
import pytesseract
import io
from io import BytesIO
import pyperclip
import win32clipboard
from ctypes import windll
import pickle
import re
import sys
import os
from os import name, system
import ssl
import psutil
import shutil
from subprocess import CREATE_NO_WINDOW
from bs4 import BeautifulSoup


with open('SETTINGS.txt', 'r') as f:
    lines = f.readlines()
f.close()

_Q='"([^"]*)"'
username=''.join(re.findall(_Q,lines[+2]))
password=''.join(re.findall(_Q,lines[+3]))
quest= 'https://www.questionai.com/'
findme = ''

chromedriver_path = 'chromedriver.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

count = 0

rann = random.randint(0, 10)

event_called = False

sg.ChangeLookAndFeel('DarkBlack')
WIN_W = 100
WIN_H = 400

num_bars = 15
current_number = 0

findme = ["Start","All","Man","Select","Day","Month","Year","10","1988","Yes","Boy","Girl","Male","male","Accept","Complete","accept","complete","submit","Submit","2006","Continue","Own","House","Credit","$100,000","100,00","Verizon","Software","IT","Technology","next","Next","1","2","3","4","5","6","7","8","9","September","1988","2006","White","Master","Republican","continue","Start Survey","Month","Year","Take Another","Comenzar", "Aceptar", "Completar", "aceptar", "completar", "Enviar", "2006", "Continuar", "Propio", "Casa", "Crédito", "$100,000", "100,00", "Verizon", "Software", "TI", "Tecnología", "Siguiente", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Septiembre", "1988", "2006", "Blanco", "Maestro", "Republicano", "Continuar", "Iniciar Encuesta", "Mes", "Año", "Tomar Otro"]

def generate_spectrum_data(num_bars):
    global current_number
    current_number = (current_number % num_bars) + 1
    return [current_number]

def update_spectrum_bars(window, spectrum_data):
    window['far_0'].update(value="Initializing\n", text_color_for_value='lime')
    window['far_0'].update(f'{"█" * spectrum_data[0]:<1}', text_color_for_value='lime', append=True)

menu_layout = [
        ['File', ['Restart', 'Exit']],['Info',['CTRL+SHIFT+Z = Start', 'CTRL+SHIFT+C = Quit']],['More',['Stop Chrome']],
        ]

ColCent = [
        ]

layout = [
        [sg.MenubarCustom(menu_layout, text_color='white', pad=((1,1),(1,1)), bar_text_color='gold', background_color='black')],
        [sg.Multiline("", no_scrollbar=True, size=(12, 4), auto_size_text=True, visible=False, justification='left', font=('Courier New', 12), border_width=0 , key='_STLINE_', background_color='black')],
        [sg.Multiline('', visible=False, font=('Courier New', 12), expand_x=True, no_scrollbar=True, size=(12, 4), border_width=0, auto_size_text=True, key=f'far_{i}', background_color='black', text_color='lime') for i in range(1)],
        [sg.Push(), sg.Column(ColCent, element_justification='c')],
        [sg.Multiline('      START', visible=True,no_scrollbar=True,font=('Courier New', 14), size=(15, 1),background_color='black',border_width=0,justification='l',enable_events=True, text_color='lime', key='__Next__')],
        [sg.Button('',border_width=0, key='_G_'),sg.Button('',border_width=0, key='_E_')],
        ]

window = sg.Window('QBot', keep_on_top=True, size=(200,100),layout=layout, grab_anywhere=True, resizable=True, use_custom_titlebar=True, no_titlebar=True, return_keyboard_events=False, enable_close_attempted_event=True, finalize=True)
window['_STLINE_'].Widget.config(cursor='arrow')
window['__Next__'].Widget.config(cursor='arrow')


def terminate_chromedriver():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'chromedriver.exe':
            print(f"Terminating chromedriver.exe (PID {process.info['pid']})")
            psutil.Process(process.info['pid']).terminate()
        if process.info['name'] == 'chrome.exe':
            print(f"Terminating chromedriver.exe (PID {process.info['pid']})")
            psutil.Process(process.info['pid']).terminate()
def find_window_callback(hwnd, extra):
    text = extra
    window_text = win32gui.GetWindowText(hwnd)
    if text in window_text:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    return True 

def find_and_hide_window(text):
    win32gui.EnumWindows(find_window_callback, text)

class Threading(Thread):
    def __init__(self, main_instance):
        Thread.__init__(self)
        self.main_instance = main_instance

    def run(self):
        self.main_instance.Start()

class Main:
    global findme

    def StartStream(self, username, password):
        global findme
        window['far_0'].update(visible=False)
        window['_STLINE_'].update(visible=True)
        window['_STLINE_'].set_size((17, 4))
        service = Service(chromedriver_path)
        service.creationflags = CREATE_NO_WINDOW

        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False) 
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"+"AppleWebKit/537.36 (KHTML, like Gecko)"+"Chrome/87.0.4280.141 Safari/537.36")
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument("--start-fullscreen")
        #chrome_options.add_argument("--kiosk")

        driver = webdriver.Chrome(service=service, options=chrome_options)

        ssl._create_default_https_context = ssl._create_unverified_context

        def login():
            global event_called
            window['_STLINE_'].update(value='')
            window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
            window['_STLINE_'].update(value="  🗲Logging In  \n", text_color_for_value='yellow', append=True)
            window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)


            try:
                driver.get('https://earnhaus.com/sign-in')
            except WebDriverException as e:
                if "ERR_INTERNET_DISCONNECTED" in str(e):
                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='red')
                    window['_STLINE_'].update(value="  !NO INTERNET  \n", text_color_for_value='red', append=True)
                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='red', append=True)
                    driver.execute_script("""
                        var popup = window.open("", "Popup", "width=200,height=100");
                        popup.document.write("Internet Disconnected Error: Please check your internet connection.");
                        // You can customize the content and styling of the popup here
                    """)
                    
                    while True:
                        if driver.window_handles and len(driver.window_handles) == 1:
                            break
                        time.sleep(1)
                    terminate_chromedriver()
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='red')
                    window['_STLINE_'].update(value="  !NO INTERNET  \n", text_color_for_value='red', append=True)
                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='red', append=True)          
            sleep(5)
            try:
                if event_called == True:
                    try:
                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                        window['_STLINE_'].update(value="  🗲GMAIL  \n", text_color_for_value='yellow', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)                        
                        driver.get('https://accounts.google.com/')
                        login_username_present = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
                        login_username_present.send_keys(username)
                        sleep(1)
                        login_username_present.send_keys(Keys.ENTER)
                        sleep(5)
                        password_elem = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
                        sleep(1)
                        actions = ActionChains(driver)
                        actions.send_keys(Keys.ENTER).perform()
                        sleep(30)
                        
                        while True:
                            if driver.window_handles and len(driver.window_handles) == 1:
                                break
                        driver.get('https://earnhaus.com/sign-in')
                        sleep(7)
                        login_butt = driver.find_element(By.XPATH, '//*[@id="google-auth-init"]').click()
                        sleep(7)

                    except:
                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='red')
                        window['_STLINE_'].update(value="  !CAN'T LOGIN  \n", text_color_for_value='red', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='red', append=True)
                else:
                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                    window['_STLINE_'].update(value="  🗲EMAIL  \n", text_color_for_value='yellow', append=True)
                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True) 
                    driver.get('https://earnhaus.com/sign-in')
                    sleep(2)
                    print('EMAIL LOGIN')
                    login_butt = driver.find_element(By.XPATH, '//*[@id="sign-in-container"]/div[2]/div/a').click()
                    login_username_present = EC.visibility_of_element_located((By.NAME, 'email'))
                    WebDriverWait(driver, 60).until(login_username_present)

                    username_elem = driver.find_element(By.NAME, 'email').send_keys(username)
                    password_elem = driver.find_element(By.NAME, 'password').send_keys(password)
                    login_button_elem = driver.find_element(By.XPATH, '//*[@id="password-sign-in-button"]').click()
                sleep(random.uniform(4, 8))
                try: # Ai Signin
                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                    window['_STLINE_'].update(value="  🗲Ai  \n", text_color_for_value='yellow', append=True)
                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)   
                    driver.get('https://questionai.com')
                    sleep(8)
                    login = driver.find_element(By.XPATH, '//*[@id="continue-as"]/div[1]').click()
                    sleep(2)
                except:
                    pass
                window['_STLINE_'].update(value='Starting:\n')
                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime', append=True)
                window['_STLINE_'].update(value="  🗲Loading\n", text_color_for_value='lime', append=True)
                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
            except:
                if "earnhaus.com/members" not in driver.current_url:
                    driver.execute_script("""
                        var popup = window.open("", "Popup", "width=200,height=100");
                        popup.document.write("Check login credentials then restart");
                        // You can customize the content and styling of the popup here
                    """)
                    
                    while True:
                        if driver.window_handles and len(driver.window_handles) == 1:
                            break
                        time.sleep(1)
                    terminate_chromedriver()
                    os.execl(sys.executable, sys.executable, *sys.argv)
                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='red', append=True)
                window['_STLINE_'].update(value="  !Login Fail\n", text_color_for_value='red', append=True)
                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='red', append=True)
            answer()
            
        def answer():
            global findme
            window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
            window['_STLINE_'].update(value=f"   🗲Running\n", text_color_for_value='#6A9CA8', append=True)
            window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
            sleep(random.uniform(4, 8))

            def survey():
                driver.get('https://earnhaus.com/members')
                #driver.execute_script("document.body.style.zoom = '100%'")
                original_window = driver.current_window_handle
                original_tab = driver.current_window_handle
                #assert len(driver.window_handles) == 1

                sleep(random.uniform(8, 20))

                try:
                    survy = driver.find_element(By.XPATH, '//*[@id="offer-wall"]/div[1]/div/div[4]/div/div[2]/a').click()
                except:
                    try:
                        survy = driver.find_element(By.XPATH, '//*[@id="offer-wall"]/div[1]/div/div[2]/div[2]/div/h3/a').click()
                    except:
                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                        window['_STLINE_'].update(value=f"  No Survey!\n", text_color_for_value='red', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                        survey()

                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break
                sleep(random.uniform(4, 8))
                
                surv_tab = [tab for tab in driver.window_handles if tab != original_tab][0]
                
                driver.switch_to.window(surv_tab)
                WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
                sleep(random.uniform(4, 8))
                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                window['_STLINE_'].update(value=f"   🗲Start\n", text_color_for_value='#6A9CA8', append=True)
                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                url = driver.current_url
                def surveytab():
                        def find_and_click_image(image_path, threshold=0.8):
                            window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                            window['_STLINE_'].update(value=f"   🗲Looking\n", text_color_for_value='#6A9CA8', append=True)
                            window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                            sleep(1)
                            screenshot = pyautogui.screenshot()
                            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                            target_image = cv2.imread(image_path)

                            result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
                            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                            if max_val >= threshold:
                                w, h = target_image.shape[:-1]
                                center_x = max_loc[0] + w / 2
                                center_y = max_loc[1] + h / 2
                                offset_x = 0  # Adjust as needed
                                offset_y = -30  # Adjust as needed
                                pyautogui.click(center_x + offset_x, center_y + offset_y)
                                sleep(1)
                                pyautogui.click(center_x, center_y)
                                print(f'\nIMG {image_path}\n')
                                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                window['_STLINE_'].update(value=f"   🗲Found\n", text_color_for_value='#6A9CA8', append=True)
                                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                submit()
                                return True
                            else    :
                                return False
                        def send_to_clipboard(clip_type, data):
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardData(clip_type, data)
                            win32clipboard.CloseClipboard()

                        def take_screenshot_to_clipboard():
                            screen_width, screen_height = pyautogui.size()
                            region = (100, 80, screen_width - 100, screen_height - 100)
                            screenshot = pyautogui.screenshot(region=region)
                            output = BytesIO()
                            screenshot.convert("RGB").save(output, "BMP")
                            data = output.getvalue()[14:]
                            output.close()
                            send_to_clipboard(win32clipboard.CF_DIB, data)


                        def chra():
                            try:
                                elements = WebDriverWait(driver, 3).until(
                                    EC.presence_of_all_elements_located((By.XPATH, f"(//input[@type='radio'])[{rann}]"))
                                )

                                for element in elements:
                                    element.click()
                                print(f'\nRadios {elements}\n')
                            except:
                                pass
                            try:
                                elements = WebDriverWait(driver, 3).until(
                                    EC.presence_of_all_elements_located((By.XPATH, f"(//input[@type='checkbox'])[{rann}]"))
                                )

                                for element in elements:
                                    element.click()
                                print(f'\nRadios {elements}\n')
                            except:
                                pass                        
                        def submit():
                            try:
                                button = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn-continue') and contains(text(), 'Continue')]"))
                                )
                                button.click()
                                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                print(f'\nButton {button}\n')
                            except:
                                try:
                                    button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button")))
                                    button.click()
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                except:   
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  •No Button\n", text_color_for_value='red', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                    pass

                            try:
                                button = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn-continue') and contains(text(), 'Next')]"))
                                )
                                button.click()
                                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                print(f'\nButton {button}\n')
                            except:
                                try:
                                    button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button")))
                                    button.click()
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                except:   
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  •No Button\n", text_color_for_value='red', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                    pass
                            try:
                                button = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn-continue') and contains(text(), 'Month')]"))
                                )
                                button.click()
                                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                print(f'\nButton {button}\n')
                            except:
                                try:
                                    button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button")))
                                    button.click()
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                except:   
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  •No Button\n", text_color_for_value='red', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                    pass

                            try:
                                button = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn-continue') and contains(text(), 'Year')]"))
                                )
                                button.click()
                                window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                print(f'\nButton {button}\n')
                            except:
                                try:
                                    button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button")))
                                    button.click()
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  🗲Button\n", text_color_for_value='lime', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                except:   
                                    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                    window['_STLINE_'].update(value=f"  •No Button\n", text_color_for_value='red', append=True)
                                    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                    pass

                        #### START SURVEY SHIT ####
                        take_screenshot_to_clipboard()
                        filename = "screenshot.png"
                        screenshot = pyautogui.screenshot()
                        screenshot.save(filename)
                        ########################Vv GET AI ANSWER vV#######################################
                        if "earnhaus.com" in driver.current_url:
                            driver.get('https://earnhaus.com/members')
                            try:
                                survey = driver.find_element(By.XPATH, '//*[@id="offer-wall"]/div[1]/div/div[4]/div/div[2]/a').click()
                            except:
                                try:
                                    survey = driver.find_element(By.XPATH, '//*[@id="offer-wall"]/div[1]/div/div[2]/div[2]/div/h3/a').click()
                                except:
                                    pass
                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                        window['_STLINE_'].update(value=f"   🗲Thinking\n", text_color_for_value='#6A9CA8', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                        #driver.execute_script("document.body.style.zoom = '100%'")
                        sleep(1)
                        driver.execute_script(f"window.open('{quest}');")
                        quest_tab = [tab for tab in driver.window_handles if tab != surv_tab and tab != original_window][0]
                        driver.switch_to.window(quest_tab)
                        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(3))
                        sleep(9)
                        text = "Role Play: You are a white male american from philadelphia, 35 years of age, married to a 40 year old woman, you are republican, you have 4 kids,1 boy 7 years of age, 1 girl 5 years of age, 1 boy 13 years of age and 1 girl 15 years of age, you make over $100k a year as a software developer at microsoft, and answer the question from this image while only supplying the answer. if you do not see a question, assume the text is a label for an input and answer according to the displayed text. example if you see “Postal Code” you will return a postal code from Philadelphia, if you see a list of words, simply choose one. Answer all questions as the character you are role-playing. do not supply an explanation or context as to why you chose the answer. say ok when ready for the image:"
                        qss = driver.find_element(By.XPATH, '//*[@id="el-id-1024-1"]').click()
                        sleep(1)
                        qss = driver.find_element(By.XPATH, '//*[@id="el-id-1024-1"]').send_keys(text)
                        sleep(4)
                        try:
                            qsub = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/button').click()
                        except:
                            qsub = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/main/section/div/main/section[1]/div[3]/div[2]/div/img').click()
                        sleep(20)
                        driver.refresh()
                        sleep(9)
                        try:
                            qss = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/div').click()
                        except:
                            qss = driver.find_element(By.XPATH, '//*[@id="el-id-1024-1"]').click()
                        try:
                            qss = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/div').click()
                        except:
                            qss = driver.find_element(By.XPATH, '//*[@id="el-id-1024-1"]').click()

                        find_and_click_image("field.png")

                        sleep(3)
                        pyautogui.hotkey('ctrl', 'v')
                        pyautogui.hotkey('ctrl', 'v')
                        sleep(3)

                        qsel = driver.find_element(By.XPATH, '//*[@id="el-id-1024-3"]/div[3]/div').click()
                        sleep(15)
                        elements = driver.find_elements(By.CLASS_NAME, 'chat-answer')
                        last_element = elements[-1]
                        element = last_element
                        answr = element.text

                        answr = answr.split()
                        target_word = answr
                        print(f'\nTARGET:{target_word}\n')

                        if "questionai" in driver.current_url:
                            driver.close()
                        driver.switch_to.window(surv_tab)
                        sleep(5)
                        #driver.execute_script("document.body.style.zoom = '67%'")
                        ############################ END GET AI ANSWER ######################################
                        find_and_click_image("check.png")

                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                        window['_STLINE_'].update(value=f"   🗲Inputs\n", text_color_for_value='#6A9CA8', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                        
                        input_boxes = driver.find_elements(By.XPATH, "//input[@type='text']")
                    
                        # Assuming the first found input box is the one you want to interact with
                        if input_boxes:
                            input_box = input_boxes[0]
                            input_box.clear()
                            input_box.send_keys(target_word)
                        submit()
                        # FIND SVG SQUARES
                        svgs = driver.find_elements(By.TAG_NAME, 'svg')

                        try:
                            for svg in svgs:
                                # Get the value of the 'd' attribute in the <path> element inside <svg>
                                path = svg.find_element(By.TAG_NAME, 'path').get_attribute('d')
                                
                                # Check if the path represents a square with rounded corners
                                if 'M19' in path and 'H5' in path and 'V5' in path and 'c-1.1' in path:
                                    print("Found SVG with rounded corners or square shape!")
                                    path.click()
                                    print(svg.get_attribute('outerHTML'))
                        except:
                            pass
                        chra()
                        submit()
                        
                        try:
                            dropdown = Select(driver.find_element(By.CSS_SELECTOR,"select"))

                            options = dropdown.options

                            random_option = random.choice(options)
                            selected_option_text = random_option.text

                            dropdown.select_by_visible_text(selected_option_text)
                            print(f'Selected: {selected_option_text}')
                        except:
                            pass
                        sleep(1)
                        try:
                            dropdown_button = driver.find_element(By.CSS_SELECTOR, '.btn.dropdown-toggle')
                            dropdown_button.click()
                            dropdown_options = driver.find_element(By.CSS_SELECTOR, '.dropdown-menu .dropdown-item')
                            random_option = random.choice(dropdown_options)
                            random_option.click()
                            print("Selected a random option.")
                        except:
                            pass
                        sleep(1)
                        try:
                            dropdown_container = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, ".dropdown.bootstrap-select"))
                            )

                            options = dropdown_container.find_elements(By.CSS_SELECTOR, ".dropdown-menu .dropdown-item")

                            if options:
                                random.choice(options).click()
                                print(f'Selected: {options}')
                        except:
                            pass
                        sleep(1)
                        try:
                            radio_container = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='radio']"))
                            )

                            options = radio_container.find_elements(By.CSS_SELECTOR, "input[type='radio']")

                            if options:
                                random.choice(options).click()
                                print(f'Radio {options} selected')
                        except:
                            pass
                        sleep(1)
                        try:
                            checkbox_container = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']"))
                            )

                            checkboxes = checkbox_container.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

                            if checkboxes:
                                random.choice(checkboxes).click()
                                print(f'Checkbox {checkboxes} selected')
                        except:
                            pass
                        sleep(1)
                        try:
                            checkbox_container = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "svg[class*='checkbox']"))
                            )

                            checkboxes = checkbox_container.find_elements(By.CSS_SELECTOR, "svg[class*='checkbox']")

                            if checkboxes:
                                random.choice(checkboxes).click()
                                print(f'Checkbox {checkboxes} selected')
                        except:
                            pass
                        sleep(1)
                        try:
                            checkbox_container = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "svg[class*='radio']"))
                            )

                            checkboxes = checkbox_container.find_elements(By.CSS_SELECTOR, "svg[class*='radio']")

                            if checkboxes:
                                random.choice(checkboxes).click()
                                print(f'Radio {checkboxes} selected')
                        except:
                            pass
                        sleep(1)
                        try:
                            checkbox_container = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "svg[class*='input-box']"))
                            )

                            checkboxes = checkbox_container.find_elements(By.CSS_SELECTOR, "svg[class*='input-box']")

                            if checkboxes:
                                random.choice(checkboxes).click()
                                print(f'Input {checkboxes} selected')
                        except:
                            pass
                        sleep(1)
                        try:
                            checkbox_container = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "svg[class*='input']"))
                            )

                            checkboxes = checkbox_container.find_elements(By.CSS_SELECTOR, "svg[class*='input']")

                            if checkboxes:
                                random.choice(checkboxes).click()
                                print(f'Input {checkboxes} selected')
                        except:
                            pass
                        submit()

                        chra()
        

                        def werk():
                            sleep(1)
                            global findme
                            if "earnhaus.com" in driver.current_url:
                                driver.get('https://earnhaus.com/members')
                                try:
                                    survey = driver.find_element(By.XPATH, '//*[@id="offer-wall"]/div[1]/div/div[4]/div/div[2]/a').click()
                                except:
                                    try:
                                        survey = driver.find_element(By.XPATH, '//*[@id="offer-wall"]/div[1]/div/div[2]/div[2]/div/h3/a').click()
                                    except:
                                        pass
                            window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                            window['_STLINE_'].update(value=f"  🗲imgWerk\n", text_color_for_value='#6A9CA8', append=True)
                            window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                            filename = "screenshot.png"
                            screenshot = pyautogui.screenshot()
                            screenshot.save(filename)
                            sleep(1)
                            img = cv2.imread('screenshot.png')
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            _, blackAndWhite = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
                            cv2.imwrite('bw_screenshot.png', blackAndWhite)
                            data = pytesseract.image_to_data(Image.open('bw_screenshot.png'), output_type=pytesseract.Output.DICT)
                            for word in findme + target_word:
                                for i in range(len(data['text'])):
                                    if word in data['text'][i]:
                                        x = data['left'][i]
                                        y = data['top'][i]
                                        w = data['width'][i]
                                        h = data['height'][i]
                                        center_x = x + w / 2
                                        center_y = y + h / 2
                                        offset = 35
                                        click_x = center_x - offset
                                        print(f"Werk '{word}'")
                                        pyautogui.click(center_x, center_y)
                                        sleep(1)
                                        break
                        find_and_click_image("droparr.png")
                        find_and_click_image("droparr2.png")
                        try:
                            options = dropdown.find_elements(By.TAG_NAME, "option")
                            random_option = random.choice(options)
                            random_option.click()
                            find_and_click_image("select.png")
                        except:
                            pass
                        #######  DROP DOWN LIST ########
                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                        window['_STLINE_'].update(value=f" 🗲Dropdown Check\n", text_color_for_value='#6A9CA8', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                        for find_str in findme:
                            for target_str in target_word:
                                # Search by class
                                elements_by_class = driver.find_elements(By.XPATH, f"//*[contains(@class, '{find_str}')]")
                                for element in elements_by_class:
                                    try:
                                        if element.text and target_str in element.text and element not in clicked_elements:
                                            element.click()
                                            clicked_elements.add(element)
                                            sleep(1)
                                            options = element.find_elements(By.TAG_NAME, "option")
                                            random_option = random.choice(options)
                                            random_option.click()
                                            counter += 1  # Increment counter
                                            window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                                            window['_STLINE_'].update(value=f"   🗲Class: {counter}\n", text_color_for_value='#6A9CA8', append=True)
                                            window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                                            print('CLASS:' + element)
                                            break  # Exit the loop after successfully clicking one element
                                    except:
                                        break
                        ######  END DROP DOWN LIST #########
                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                        window['_STLINE_'].update(value=f"   🗲Inputs\n", text_color_for_value='#6A9CA8', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                        find_and_click_image("nput.png")
                        sleep(1)
                        try:
                            actions = ActionChains(driver)
                            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                            actions.send_keys(target_word)
                            actions.perform()
                            sleep(1)
                            screen_width, screen_height = pyautogui.size()
                            center_x = screen_width // 2
                            center_y = screen_height // 2
                            pyautogui.click(center_x, center_y)
                            pyautogui.click(center_x, center_y)
                            print('Ai Response Sent')
                        except:
                            pass
                        submit()
                        find_and_click_image("nput.png")
                        try:
                            actions = ActionChains(driver)
                            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                            actions.send_keys("19140")
                            actions.perform()
                            sleep(1)
                            screen_width, screen_height = pyautogui.size()
                            center_x = screen_width // 2
                            center_y = screen_height // 2
                            pyautogui.click(center_x, center_y)
                            pyautogui.click(center_x, center_y)
                            print('Zip Sent')
                        except:
                            pass
                        submit()
                        sleep(1)
                        werk()

                        submit()
                        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
                        window['_STLINE_'].update(value=f"   🗲Loop\n", text_color_for_value='#6A9CA8', append=True)
                        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)
                        time.sleep(1)
                        surveytab()
                surveytab()
            survey()            
        login()
    def Start(self):
        def hide_and_forget(element_list):
            for element in element_list:
                window[element].update(visible=False)
                window[element].Widget.master.pack_forget()
        elements_to_hide = [
            '__Next__','_E_','_G_'
        ]
        
        hide_and_forget(elements_to_hide)
        move_top_right(window)
        window['far_0'].update(visible=True)
        window['far_0'].set_size((17, 4))
        sleep(1)
        start_time = time.time()

        while True:
            current_time = time.time()
            if current_time - start_time > 4:
                elements_to_hide = [
                    'far_0'
                ]
                
                hide_and_forget(elements_to_hide)                
                break
            spectrum_data = generate_spectrum_data(num_bars)
            update_spectrum_bars(window, spectrum_data) 
        self.StartStream(username, password)

def chk(url='https://google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return True
    except requests.RequestException:
        window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='red')
        window['_STLINE_'].update(value="   NO INTERNET!\n", text_color_for_value='red', append=True)
        window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='red', append=True)
        return False
def move_top_right(window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = screen_width - win_width, 0
    window.move(x, y)

show_text = True
if __name__ == "__main__":
    chk()
    find_and_hide_window("chromedriver.exe")
    find_and_hide_window("py.exe")
    main = Main()
    window['_STLINE_'].set_size((17, 4))
    window['_STLINE_'].update(value="╔══════════════╗\n", text_color_for_value='lime')
    window['_STLINE_'].update(value="     •READY\n", text_color_for_value='#6A9CA8', append=True)
    window['_STLINE_'].update(value="╚══════════════╝", text_color_for_value='lime', append=True)

    def fxit():
        terminate_chromedriver()
        os._exit(0)
    def sst():
        threading_instance = Threading(main)
        threading_instance.start()
    keyboard.add_hotkey('ctrl+shift+c', fxit)
    keyboard.add_hotkey('ctrl+shift+z', sst)
    while True:
        
        if show_text:
            window['_G_'].update("-->GMAIL<--",button_color=('cyan', 'black'))
            window['_E_'].update("  -->EMAIL<--",button_color=('cyan', 'black'))
        else:
            window['_G_'].update("-->          <--",button_color=('cyan', 'black'))
            window['_E_'].update("  -->          <--",button_color=('cyan', 'black'))
            
            
        show_text = not show_text
        
        event, values = window.read(timeout=500)

        try:
            window.set_alpha(int(Opac)/100)
        except:
            window.set_alpha(100/100)
        if event == '_G_':
            event_called = True
            show_text = not show_text
            threading_instance = Threading(main)
            threading_instance.start()
        if event == '_E_':
            event_called = False
            show_text = not show_text
            threading_instance = Threading(main)
            threading_instance.start()
        if event in ('Stop Chrome'):
            terminate_chromedriver()
        if event in ('Restart', 'n:78'):
            terminate_chromedriver()
            os.execl(sys.executable, sys.executable, *sys.argv)
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(('Do you really want to exit?'), keep_on_top=True) == 'Yes':
            try:
                terminate_chromedriver()
                os._exit(0)
            except:
                break

        window.refresh()

