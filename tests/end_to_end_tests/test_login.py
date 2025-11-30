import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .e2e_helpers import *
from app.models import User
from app import db


def test_login(live_server, driver, setup_database_following):
    user1, user2 = setup_database_following
    test_password = "TestPassword123!"

    driver.get(f"{BASE_URL}/auth/login")

    wait = WebDriverWait(driver, TIMEOUT)
    
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(user1.username)
    driver.find_element(By.NAME, "password").send_keys(test_password)
    driver.find_element(By.NAME, "submit").click()

    wait = WebDriverWait(driver, TIMEOUT)
    
    logout_link = wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
    )

    assert logout_link.is_displayed(), "No Logout link"
