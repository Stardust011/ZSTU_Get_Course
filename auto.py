import config
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# 配置区
course_id = ''

quit_course_id = ''
# 2022-12-26 12:0:0
ddl = 1672027200

configs = config.load_config('config')
url = configs['url']
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='log.txt', level=logging.WARNING, format=LOG_FORMAT)

ttl = 0

def login():
    try:
        logging.debug('开始登录')
        driver.get(url)
        time.sleep(3)
        now_url = driver.current_url
        if 'sso' in now_url:
            driver.find_element(By.XPATH, '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[1]/nz-input-group/input').send_keys(configs['username'])
            driver.find_element(By.XPATH, '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input').send_keys(configs['password'])
            driver.find_element(By.XPATH, '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div/app-login-auth-panel/div/div[1]/app-login-normal/div/form/div[6]/div/button').click()
        else:
            driver.find_element(By.ID, 'yhm').send_keys(configs['username'])
            driver.find_element(By.ID, 'mm').send_keys(configs['password'])
            driver.find_element(By.ID, 'dl').click()
        return 0
    except:
        logging.error('登录失败')
        now_url = driver.current_url
        if 'index_initMenu.html' in now_url:
            return 0
        return 1

def quit_course():
    try:
        logging.debug('退选课程')
        # 退出课程
        driver.find_element(By.XPATH, '//*[@id="choosedBox"]/div/div[1]/span').click()
        time.sleep(3)
        #mCSB_1_container > div > div.right_div
        quit_div_id = 'right_' + quit_course_id
        # //*[@id="right_EBD3998804821C84E0530100007F9418"]/div/table/tbody/tr/td[9]/p/button
        q_div = driver.find_element(By.XPATH, '//*[@id="mCSB_1_container"]/div/div[2]').find_element(By.ID, quit_div_id)
        q_table = q_div.find_element(By.TAG_NAME, 'li').find_element(By.TAG_NAME, 'table')
        q_button = q_table.find_element(By.XPATH, './tbody/tr/td[9]/p/button')
        logging.debug('课程退出按钮: ' + q_button.text + 'find!')

        driver.execute_script("arguments[0].click();", q_button)
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="btn_confirm"]'))
        driver.find_element(By.XPATH, '//*[@id="btn_confirm"]').click()
        logging.info('课程退出成功')
        # 关闭侧边栏
        driver.find_element(By.XPATH, '//*[@id="choosedBox"]/div/div[1]/span').click()
        return 0
    except:
        logging.error('退选课程失败')
        return 1

def search_course(flag):
    try:
        logging.debug('查询课程')
        # 点击搜索
        driver.find_element(By.XPATH, '//*[@id="searchBox"]/div/div[1]/div/div/div/div/span/button[1]').click()
        time.sleep(2)
        #contentBox > div.tjxk_list > div.panel.panel-info > div.panel-body.table-responsive > table
        course_table = driver.find_element(By.XPATH, '//*[@id="contentBox"]/div[2]/div[1]/div[2]/table')
        course_table_body = course_table.find_element(By.TAG_NAME, 'tbody')
        course_table_body_rows = course_table_body.find_elements(By.TAG_NAME, 'tr')
        for course_table_body_row in course_table_body_rows:
            course_table_body_row_columns = course_table_body_row.find_elements(By.TAG_NAME, 'td')
            if course_table_body_row_columns[21].text == '已满':
                continue
            else:
                if flag == 1:
                    print('开始退出课程')
                    quit_course()
                print(course_table_body_row_columns[21].text)
                add_button = course_table_body_row_columns[24].find_element(By.TAG_NAME, 'button')
                driver.execute_script("arguments[0].click();", add_button)
                print('课程添加成功')
                return 0
        return 5
    except:
        logging.error('查询课程失败')
        return 1

def main():
    # 登录
    global ttl
    while ttl <= 3:
        if login() == 0:
            break
        else:
            ttl += 1
        print('登录失败: ' + str(ttl) + '次')
    if ttl > 3:
        logging.error('登录失败-超过最大重试次数')
        exit()
    ttl = 0
    # 搜索课程
    try:
        logging.debug('进入课程组')
        driver.get(configs['choose_course_url'])
        WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH,'//*[@id="nav_tab"]/li[1]/a'))
        # 填入课程ID
        driver.find_element(By.XPATH, '//*[@id="searchBox"]/div/div[1]/div/div/div/div/input').send_keys(course_id)
        # 选择课程组
        driver.find_element(By.XPATH, '//*[@id="nav_tab"]/li[7]/a').click()
    except:
        logging.error('进入课程组失败')
        exit()

if __name__ == '__main__':
    logging.info('程序开始')
    driver = webdriver.Chrome(executable_path='./chromedriver')
    main()
    while int(time.time()) <= ddl:
        re = search_course(1)
        if re == 0:
            logging.warning('选课成功')
            break
        else:
            ttl += 1
            if ttl % 10 == 0:
                logging.info('尝试选课: ' + str(ttl) + '次')
            if re == 1:
                logging.warning('选课失败: 重新登录')
                main()
    time.sleep(5)
    driver.quit()
