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

    # блок с комментариями
    comments = driver.find_element(By.CSS_SELECTOR, ".wdp-comments-module__expandTitle")
    # прокрутка страницы вниз
    driver.execute_script("arguments[0].scrollIntoView();", comments)

    # создаем перемещение указателя мыши к элементу comments
    actions = ActionChains(driver)
    actions.move_to_element(comments).perform()

    # нажатие на кнопку для открытия всех комментариев
    driver.execute_script("arguments[0].click();", comments)

    # количество прокруток
    scroll_count = 5
    container = 0

    # множество для уникальных комментариев
    unique_comments = set()

    # прокрутка и сбор комментариев
    for i in range(scroll_count):
        time.sleep(2)  # подождать, чтобы комментарии успели загрузиться
        com
        ent_elements = driver.find_elements(By.CLASS_NAME, "wdp-comment-item-module__descriptionContainer")
        for coment_element in coment_elements:
            container += 1
            coment_text = coment_element.text

            # проверяем, был ли комментарий ранее
            if coment_text not in unique_comments:
                unique_comments.add(coment_text)
                with open("rutube_comments.txt", "a", encoding="utf-8") as file:
                    file.write(str(container) + ") " + coment_text + "\n")

        # прокрутка вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

except Exception as e:
    print(e)

finally:
    try:
        driver.close()
        driver.quit()
    except Exception as e:
        print(e)
