from webdriver_manager.chrome import ChromeDriverManager   #-------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from datetime import datetime
import json
from dateutil.relativedelta import *
import os
import sys
import csv
import requests
import random
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from PIL import Image
from io import BytesIO
import config
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

username = config.username
password = config.password
chrome_version = config.chrome_version   #'114.0.5735.90'    #------------------------

max_dimension = config.max_dimension   #400  # for resize image, Replace with the desired maximum dimension (width or height)
chrome_headless = config.chrome_headless    #True

nation = config.nation       #['Thai','Korea','Laos','Asia']
location = config.location     #['on the beach','in car','in town','in garden']
style = config.style    #['unofficial photo','from moblie camera','Take a normal photo','Take a friendly photo',' ']
wearing = config.wearing_styles     #['T-shirt','shirt','dress']
photo = config.photo_perspectives_person   #['take a picture of the side face',' ']

def PostApi(image_url,cls):
    output_image_path = 'resized.png'
    resize_and_save(image_url,output_image_path)
    r = post_img(output_image_path,cls)
    return r

def add_row_to_csv(file_path, row_data):
    try:
        if not os.path.isfile(file_path):
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['link', 'class', 'time'])
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row_data)
        # print("Row added successfully!")
    except Exception as e:
        print(f"Error adding row: {e}")
        
def post_img(file_name,cls):
    url = "https://back.banrairobot.win/upload/image"
    payload = {'folder': {cls}}
    files=[
      ('file',('LogoRTA.png',open(file_name,'rb'),'image/png'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.text

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        return img
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def resize_and_save_image(image, output_path, max_dimension):
    try:
        width, height = image.size

        if width > height:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        else:
            new_width = int(width * (max_dimension / height))
            new_height = max_dimension

        resized_img = image.resize((new_width, new_height))

        resized_img.save(output_path)
        print("Image resized and saved successfully!")
        return True
    except Exception as e:
        print(f"Error resizing and saving image: {e}")
        return False
        
def resize_and_save(image_url,output_image_path):
    # max_dimension = 400  # Replace with the desired maximum dimension (width or height)
    image = download_image(image_url)

    if image:
        return resize_and_save_image(image, output_image_path, max_dimension)
    else:
        return False

def window_scroll_down(x,scroll_time):
    source1 = driver.find_element(By.XPATH,x)
    action = ActionChains(driver)
    for i in range(scroll_time):
        try:
            action.drag_and_drop_by_offset(source1, 0, 300).perform()
            time.sleep(1)
        except:
            pass
        
def line_noti(token,msg):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url, headers=headers, data = {'message':msg})
    return r.text

def scrolling_down(t):
    for i in range(t):
        driver.execute_script("window.scrollBy(0,2000)","")
        time.sleep(0.5)
        
def get_text(x):
    return driver.find_element(By.XPATH,x).text

def get_herf(x):
    attb = ['href','onclick','src','data-responsive']
    for a in attb:
        v = driver.find_element(By.XPATH,x).get_attribute(a)
        if v:
            break 
    return v

def click(x):
    driver.find_element(By.XPATH,x).click()
    
def sent_key(x,val):
    driver.find_element(By.XPATH, x).send_keys(val)
    
def clear(x):
    driver.find_element(By.XPATH, x).clear()

def ENTER(x):
    driver.find_element(By.XPATH, x).send_keys(Keys.ENTER)
    
def wait(x,t):
    WebDriverWait(driver, t).until(EC.presence_of_element_located((By.XPATH, x)))
    
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True

def update_csv(path,data):
    df = pd.read_csv(path)
    
    for k in data.keys():
        data[k] = [data[k]]
    new_data_df = pd.DataFrame(data)
    df = df.append(new_data_df, ignore_index=True)
    df.to_csv(path, index=False)
    
def sent_command(command):
#     sent_key('/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div',command[0])
    x = '/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div'
    e = '/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/form/div/div[1]/div/div[3]/div/div/div'
    sent_key(x,command[0])
    time.sleep(1)
    ENTER(e)
    time.sleep(3)
    if len(command) > 1:
        sent_key('/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/main/form/div/div[2]/div/div[2]/div/div/div/span[2]/span[2]',command[1])
        time.sleep(1)
    try:
        ENTER('/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div/main/form/div/div[2]/div/div[2]/div/div/div')
    except:
        pass

def findlast_UV():
    def findlast_xpath():
        last_xpath = None
        attemp = 0
        for i in range(2,10000):
                        # '/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[91 ]/div/div[2]/div[2]/div[1]/div/button[1]'
                        # '/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[91 ]/div/div[2]/div[2]/div[1]/div/button[4]'
            u_xpath = [f'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[{i}]/div/div[3]/div[2]/div[1]/div/button[4]',
                       f'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[{i}]/div/div[2]/div[2]/div[1]/div/button[4]']
            v_xpath = [f'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[{i}]/div/div[3]/div[2]/div[2]/div/button[4]',
                       f'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[{i}]/div/div[2]/div[2]/div[2]/div/button[4]']
            if check_exists_by_xpath(v_xpath[0]):
                last_xpath = (u_xpath[0],v_xpath[0],i)
            elif check_exists_by_xpath(v_xpath[1]):
                last_xpath = (u_xpath[1],v_xpath[1],i)
            else:
                attemp += 1
                if attemp > 100:
                    return last_xpath
        return last_xpath

    u,v,n = findlast_xpath()
    U = []
    V = []
    for i in range(1,5):
        U.append(u.replace('button[4]',f'button[{i}]'))
        V.append(v.replace('button[4]',f'button[{i}]'))
    return U,V,n

def find_last_U():
    last_u = 0
    attemp = 0
    for u in range(10000):

        sta = None
        try:
            sta = check_exists_by_xpath(f'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[{u}]/div/div[3]/div[1]/div/div/div/div/div/a')
        except:
            try:
                sta = check_exists_by_xpath(f'/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div[2]/div/ol/li[{u}]/div/div[3]/div[1]/div/div/div/div/div/a')
            except Exception as e:
                print(e)
                pass

    #     u = 10
        # sta = check_exists_by_xpath(f'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[{u}]/div/div[3]/div[2]/div[3]/div/button[4]')
                                     
        if sta:
            last_u = u
        else:
            attemp += 1
        if attemp > 50:
            break
    #     print(u,sta)
    return last_u

try:

    L = {}
    CLS = ['fImage','mImage']
    TYPE = ['woman','man']
    for k in CLS:
        L[k] = []
        
    while True:
        ##start---------------

        chrome_options = Options()
        if chrome_headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options,service=ChromeService(ChromeDriverManager(chrome_version).install()))

        driver.set_window_size(1000, 6000)
        # driver.maximize_window()
        print('driver.get_window_size()',driver.get_window_size())

        driver.get('https://discord.com/channels/@me/1120122639726432326/1120175931760320562')
        time.sleep(10)

        # #login
        x_username = '/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/input'
        x_password = '/html/body/div[2]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/div[2]/div/input'
        sent_key(x_username,username)
        sent_key(x_password,password)
        time.sleep(1)
        ENTER(x_password)
        time.sleep(10)

        #open misjourney chat
        click('/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/nav/div[1]/button')
        time.sleep(1)
        sent_key('/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/div/div/div/input','Midjourney Bot')
        time.sleep(1)
        click('/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/div/div/div/div[1]/div/div[2]/div')
        time.sleep(10)

        #set fast or relax
        # sent_command(['/fast'])
        sent_command([config.mode])
        time.sleep(10)

        #crawling loop...
        # for x in range(3):
        x = 0
        # L = {}
        # CLS = ['fImage','mImage']
        # TYPE = ['woman','man']
        # for k in CLS:
        #     L[k] = []

        while True:
            
            sent_command([f'loop {x}'])  
            time.sleep(1)

            cls = CLS[x%len(CLS)]
            Type = TYPE[x%len(CLS)]
            text = f'{random.choice(nation)} {Type} wearing in {random.choice(wearing)} style at {random.choice(location)} by {random.choice(style)} {random.choice(photo)}'

            print('\nloop:',x,'='*40)
            print('text',text)

            sent_command(['/imagine',text])
            time.sleep(3)
            
            #find last n
            U,V,n = findlast_UV()
            last_n = n
            print('last n=',n)
            
            #wait for genenrated
            print('wait for genenrated...')
            start_attemp = time.time()
            while n == last_n and time.time()-start_attemp < config.waiting_time:
                U,V,n = findlast_UV()
                time.sleep(3)
                
            #update last n
            U,V,n = findlast_UV()
            last_n = n
            print('last n=',n)
            last_U = find_last_U()
            print('last_U=',last_U)
            
            
            #click U
            i = 0
            start_attemp = time.time()
            while i < 4 and time.time()-start_attemp < config.waiting_time:
                try:
                    click(U[i])
                    print('click U',i+1)
                    i += 1
                except:
                    pass
                time.sleep(2)
                
            #check click U complte or not
            start_attemp = time.time()
            last_U = find_last_U()
            while last_U < last_n+4 and time.time()-start_attemp < config.waiting_time:
                last_U = find_last_U()
                print('last_U',last_U)
            print('upscale complete! last_U',last_U)
            time.sleep(5)
                
            #get href
            current_l = []
            for i in range(last_n+1,last_n+10):
                l = None
                try:
                    l = get_herf(f'/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[{i}]/div/div[3]/div[1]/div/div/div/div/div/a')
                except:
                    try:
                        l = get_herf(f'/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div[2]/div/ol/li[{i}]/div/div[3]/div[1]/div/div/div/div/div/a')
                    except Exception as e:
                        # print(e)
                        pass
                if l:
                    L[cls].append(l)
                    current_l.append(l)
                    print(cls,i,l)
            if not current_l:
                print('restart!!'*100)

                #logout
                click('/html/body/div[2]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/section/div[2]/div[1]/div[2]')
                time.sleep(2)
                click('/html/body/div[2]/div[2]/div[1]/div[3]/div/div/div/div/div/div[3]/div[5]/div/div[3]/div/div[2]/div[2]')
                time.sleep(5)
                click('/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/div[3]/button')
                time.sleep(2)
                click('/html/body/div[2]/div[2]/div[1]/div[3]/div[3]/div/div/div[1]')
                time.sleep(2)

                driver.close()
                break

            print('get href complete!')
            print('L',L)
            print("len(L['fImage'])",len(L['fImage']),"len(L['mImage'])",len(L['mImage']))
            print('-'*20)

            #sent api and save csv
            min_L = min([len(L[k]) for k in L.keys()])
            if min_L > 0:
                print('min_L',min_L,'-='*100)
                for ii in range(min_L):
                    for cls in L.keys():
            #             cls = 'fImage'
                        image_url = L[cls].pop()
                        r = PostApi(image_url,cls)
                        add_row_to_csv('misjourey_data.csv', [image_url,cls,time.time()])
                        print(r,cls,image_url)

            x += 1

except Exception as e:
    print('Error',e)
    driver.close()
    time.sleep(10)
