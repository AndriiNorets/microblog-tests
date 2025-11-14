# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Импортируем всё необходимое из нашего файла с хелперами
# from .e2e_helpers import *

# @pytest.fixture(scope='function')
# def setup_database(app):
#     with app.app_context():
#         test_password = "TestPassword123!"
#         user1 = User(username='testuser1', email='user1@gmail.com')
#         user1.set_password(test_password)
#         user2 = User(username='testuser2', email='user2@gmail.com')
#         user2.set_password(test_password)
        
#         db.session.add_all([user1, user2])
#         db.session.commit()
        
#         # --- ИЗМЕНЕНИЕ: Используем "свежие" объекты из БД ---
#         u1_fresh = db.session.get(User, user1.id)
#         u2_fresh = db.session.get(User, user2.id)

#         u1_fresh.follow(u2_fresh)
        
#         post1 = Post(body="this post is about the python programming language", author=u1_fresh)
#         post2 = Post(body="a second post, this one is about java", author=u2_fresh)
#         post3 = Post(body="another developer post, also about python", author=u2_fresh)

#         db.session.add_all([post1, post2, post3])
#         db.session.commit()
        
#         # Возвращаем "свежие" объекты, чтобы избежать проблем в тестах
#         yield u1_fresh, u2_fresh

# def test_user_can_search_for_posts(live_server, driver, setup_database):
#     """
#     E2E Тест: Пользователь логинится, использует форму поиска
#     и видит релевантные результаты.
#     """
#     user1, _ = setup_database
#     test_password = "TestPassword123!"

#     # 1. Логинимся
#     login_user(driver, user1.username, test_password)

#     # 2. Находим форму поиска и отправляем запрос
#     wait = WebDriverWait(driver, TIMEOUT)
#     search_field = wait.until(EC.presence_of_element_located((By.ID, "q")))
#     search_term = "python"
#     search_field.send_keys(search_term)
#     search_field.submit()

#     # 3. Проверяем, что мы на странице результатов, ища видимый заголовок H1
#     try:
#         wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//h1[contains(text(), 'Search Results')]")
#         ))
#     except Exception as exc:
#         # Если мы даже не нашли заголовок, сохраняем скриншот и падаем
#         driver.save_screenshot("search_page_error.png")
#         raise AssertionError("Could not find 'Search Results' header on the page.") from exc
        
#     # --- ОТЛАДОЧНЫЙ ШАГ: Делаем скриншот страницы результатов ---
#     # Это позволит нам увидеть, почему посты не отображаются.
#     driver.save_screenshot("search_results_page.png")

#     # 4. Получаем весь текст со страницы
#     page_text = driver.find_element(By.TAG_NAME, 'body').text
    
#     # 5. Проверяем, что посты про "python" отображаются
#     assert "this post is about the python programming language" in page_text, \
#         "Post about python was not found on the search results page."
    
#     # 6. Убеждаемся, что пост про "java" НЕ отображается
#     assert "this one is about java" not in page_text, \
#         "Post about java was incorrectly found on the search results page."

