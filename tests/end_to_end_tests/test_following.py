import pytest
from selenium.webdriver.common.by import By
from .e2e_helpers import *
from app.models import User
from app import db


def test_following(live_server, driver, setup_database_following):
    user1, user2 = setup_database_following
    test_password = "TestPassword123!"

    login_user(driver, user1.username, test_password)

    driver.get(f"{BASE_URL}/user/{user2.username}")
    
    wait = WebDriverWait(driver, TIMEOUT)
    
    # Wait and click follow button
    follow_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//form[@action='/follow/{user2.username}']//input[@type='submit']"))
    )
    follow_button.click()

    # Wait and click unfollow button
    unfollow_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//form[@action='/unfollow/{user2.username}']//input[@type='submit']"))
    )
    assert unfollow_button.get_attribute('value') == 'Unfollow'

    unfollow_button.click()

    # Verify follow button is back
    follow_button_again = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//form[@action='/follow/{user2.username}']//input[@type='submit']"))
    )
    
    assert follow_button_again.get_attribute('value') == 'Follow'