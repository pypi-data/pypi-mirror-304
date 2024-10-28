import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pytesseract
from PIL import Image
import io
import datetime
import threading

def login_and_save_cookies(playwright: Playwright, username: str, password: str, cookie_path: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/svscenter/myCollect")
    page.get_by_placeholder("用户名").click()
    page.get_by_placeholder("用户名").fill(username)
    page.get_by_placeholder("密码").click()
    page.get_by_placeholder("密码").fill(password)
    page.locator("#index_login_btn").click()
    time.sleep(2)

    # 保存cookie到本地文件
    context.storage_state(path=cookie_path)

    context.close()
    browser.close()

def login_task(username: str, password: str, cookie_path: str):
    with sync_playwright() as playwright:
        login_and_save_cookies(playwright, username, password, cookie_path)

def perform_task(playwright: Playwright, cookie_path: str, num: int) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state=cookie_path)
    page = context.new_page()
    page.goto("https://scenter.sdu.edu.cn/tp_fp/view?m=fp#act=fp/svscenter/myCollect")

    for i in range(1, 300):
        page.reload()
        time.sleep(0.5)
        element = page.locator('//div[@uname="svs"]')
        text = element.inner_text().replace('\n', '').replace(' ', '')
        if '未到开放时间' in text:
            print('未到开放时间')
            continue
        else:
            print('到开放时间')
            break

    # 选择场馆
    page.get_by_text("体育学院").click()

    page.frame_locator("#formIframe").get_by_role("button", name="请选择").first.click()
    page.frame_locator("#formIframe").locator('//ul[@class="dropdown-menu inner selectpicker"]/li[last()]').first.click()
    
    page.frame_locator("#formIframe").get_by_role("button", name="请选择").first.click()
    page.frame_locator("#formIframe").locator("a").filter(has_text="18:00-20:00").click()

    page.frame_locator("#formIframe").get_by_role("button", name="请选择").first.click()
    page.frame_locator("#formIframe").locator("a").filter(has_text="综合体育馆羽毛球").click()

    page.frame_locator("#formIframe").get_by_role("button", name="请选择").click()
    page.frame_locator("#formIframe").locator("a").filter(has_text=re.compile(f"^{num}$")).click()
    page.get_by_role("button", name="申请").click()

    yzm_btn = page.locator('//a[@id="a_changeApplyCode"]')
    screenshot_data = yzm_btn.screenshot()
    yzm_pic = Image.open(io.BytesIO(screenshot_data))
    data = pytesseract.image_to_string(yzm_pic, lang="eng")
    page.locator('//body/div[1]/div[2]/div[13]/div/div[8]/div/div/div/div/div[2]/div[1]/input').fill(data)

    page.get_by_role("button", name="确定").click()
    time.sleep(500)

def task(cookie_path: str, num: int):
    with sync_playwright() as playwright:
        perform_task(playwright, cookie_path, num)

def schedule_task(cookie_path: str, num: int, scheduled_time: datetime.time):
    t = threading.Thread(target=task, args=(cookie_path, num))
    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= scheduled_time:
            print("running...")
            t.start()
            t.join()
            break
        else:
            time.sleep(2)
            print("sleeping...")

# Example usage:
# login_task('username', 'password', 'cookies.json')
# schedule_task('cookies.json', 10, datetime.time(12, 29, 55))