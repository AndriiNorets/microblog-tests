# tests/end_to_end_tests/e2e_helpers.py

import pytest
import threading
from werkzeug.serving import make_server
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.models import User, Post
from app import db

BASE_URL = "http://127.0.0.1:5001"  
TIMEOUT = 5

@pytest.fixture(scope='function')
def live_server(app):
    server = make_server("127.0.0.1", 5001, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server
    server.shutdown()

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()

@pytest.fixture(scope='function')
def setup_database(app):
    with app.app_context():
        test_password = "TestPassword123!"

        user1 = User(username='testuser1', email='user1@gmail.com')
        user1.set_password(test_password)
        
        user2 = User(username='testuser2', email='user2@gmail.com')
        user2.set_password(test_password)

        db.session.add_all([user1, user2])
        db.session.commit()
        
        user1.follow(user2)
        
        post = Post(body="This is a post by user2.", author=user2)
        post1 = Post(body="this post is about the python programming language", author=user1)
        post2 = Post(body="a second post, this one is about java", author=user2)
        post3 = Post(body="another developer post, also about python", author=user2)
        
        db.session.add(post)
        db.session.commit()
        yield user1, user2

@pytest.fixture(scope='function')
def setup_database_following(app):
    with app.app_context():
        test_password = "TestPassword123!"

        user1 = User(username='testuser1', email='user1@gmail.com')
        user1.set_password(test_password)

        user2 = User(username='testuser2', email='user2@gmail.com')
        user2.set_password(test_password)

        db.session.add_all([user1, user2])
        db.session.commit()
        
        yield user1, user2

def login_user(driver, username, password):
    driver.get(f"{BASE_URL}/auth/login")
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "submit").click()
    open_navbar_if_collapsed(driver)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))

def logout_user(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    open_navbar_if_collapsed(driver)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))).click()
    wait.until(EC.presence_of_element_located((By.NAME, "username")))

def send_message(driver, to_user, message):
    wait = WebDriverWait(driver, TIMEOUT)
    open_navbar_if_collapsed(driver)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Explore"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, to_user))).click()
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Send private message"))).click()
    wait.until(EC.presence_of_element_located((By.NAME, "message"))).send_keys(message)
    driver.find_element(By.NAME, "submit").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-info")))

def open_navbar_if_collapsed(driver):
    try:
        wait = WebDriverWait(driver, 2)
        
        toggler = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "navbar-toggler"))
        )
        
        toggler.click()
        
        wait.until(
            EC.visibility_of_element_located((By.ID, "navbarSupportedContent"))
        )
    except Exception:
        pass
