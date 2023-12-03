from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

url = "https://rutube.ru/video/43c9436990f06b6e1ca56d7dd945b7b7/"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    driver.get(url=url)

    banner_close = driver.find_element(By.CSS_SELECTOR, ".freyja_char-base-button__icon-left__C5rMR.undefined").click()

    comments_section = driver.find_element(By.CSS_SELECTOR, ".wdp-comments-module__expandTitle")
    driver.execute_script("arguments[0].scrollIntoView();", comments_section)

    time.sleep(5)

    actions = ActionChains(driver)
    actions.move_to_element(comments_section).perform()

    driver.execute_script("arguments[0].click();", comments_section)

    time.sleep(5)

except Exception as e:
    print(e)

finally:
    try:
        driver.close()
        driver.quit()
    except Exception as e:
        print(e)
