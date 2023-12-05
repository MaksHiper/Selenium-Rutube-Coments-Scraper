from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

url = "https://rutube.ru/"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)



def get_video_links():
    try:
        driver.get(url=url)

        try:
            banner_close = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".freyja_char-base-button__icon-left__C5rMR.undefined"))
            )
            banner_close.click()
        except Exception as e:
            print(f"Ошибка при закрытии баннера: {e}")

        search_open = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wdp-header-right-module__search"))
        )
        search_open.click()

        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "freyja_char-header-search__input__ln9vI"))
        )
        search.send_keys("ТЕМА ДЛЯ ПОИСКА")
        search.send_keys(Keys.ENTER)
        time.sleep(4)

        # Получаем ссылки на видео
        video_elements = driver.find_elements(By.CLASS_NAME, "pen-card-horizontal-inline__title")
        video_links = [element.get_attribute("href") for element in video_elements]

        return video_links

    except Exception as e:
        print(f"Ошибка при получении ссылок на видео: {e}")
        return []

def open_video(url):
    try:
        driver.get(url)
        open_vid_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pen-card-horizontal-inline__title"))
        )
        open_vid_button.click()

    except Exception as e:
        print(f"Ошибка при открытии видео: {e}")

def com_parse():
    try:
        comments = driver.find_element(By.CSS_SELECTOR, ".wdp-comments-module__expandTitle")
        driver.execute_script("arguments[0].scrollIntoView();", comments)
        actions = ActionChains(driver)
        actions.move_to_element(comments).perform()
        driver.execute_script("arguments[0].click();", comments)
        scroll_count = 5
        container = 0
        unique_comments = set()

        for i in range(scroll_count):
            time.sleep(2)
            comment_elements = driver.find_elements(By.CLASS_NAME, "wdp-comment-item-module__descriptionContainer")
            for comment_element in comment_elements:
                container += 1
                comment_text = comment_element.text

                if comment_text not in unique_comments:
                    unique_comments.add(comment_text)
                    with open("rutube_comments.txt", "a", encoding="utf-8") as file:
                        file.write(str(container) + ") " + comment_text + "\n")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    except Exception as e:
        print(e)

def main():
    try:
        video_links = get_video_links()

        for video_link in video_links:
            open_video(video_link)
            com_parse()
            driver.back()
            time.sleep(5)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        try:
            time.sleep(5)
            driver.close()
            driver.quit()
        except Exception as e:
            print(f"Ошибка при закрытии драйвера: {e}")

if __name__ == "__main__":
    main()
