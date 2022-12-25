import config
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def login():
    configs = config.load_config('config')
    url = configs['url']
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(url)
    time.sleep(5)
    now_url = driver.current_url
    if 'sso' in now_url:
        driver.find_element(By.XPATH, '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[1]/nz-input-group/input').send_keys(configs['username'])
        driver.find_element(By.XPATH, '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input').send_keys(configs['password'])
        driver.find_element(By.XPATH, '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[6]/div/button').click()
        time.sleep(5)
    else:
        driver.find_element(By.ID, 'yhm').send_keys(configs['username'])
        driver.find_element(By.ID, 'mm').send_keys(configs['password'])
        driver.find_element(By.ID, 'dl').click()
        time.sleep(5)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

if __name__ == '__main__':
    print(login())