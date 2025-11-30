import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .e2e_helpers import *
from app.models import User
from app import db


def test_registration(live_server, driver):
    wait = WebDriverWait(driver, TIMEOUT)
    
    username = "user3"
    email = "user3@example.com"
    password = "user3password"

    driver.get(BASE_URL)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click to Register!"))).click()

    wait.until(EC.url_contains('/auth/register'))

    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password2").send_keys(password)
    driver.find_element(By.NAME, "submit").click()

    wait.until(EC.url_contains('/auth/login'))

    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "submit").click()

    wait.until(EC.url_contains(f'{BASE_URL}'))

    assert driver.current_url == f"{BASE_URL}/index"

        