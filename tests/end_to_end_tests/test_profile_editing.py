from selenium.webdriver.common.by import By
from .e2e_helpers import *

def test_user_can_edit_profile(live_server, driver, setup_database):
    user1, _ = setup_database
    test_password = "TestPassword123!"

    login_user(driver, user1.username, test_password)
    
    open_navbar_if_collapsed(driver)
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Profile"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit your profile"))).click()
    
    new_username = f"{user1.username}_edited"
    new_bio = "This bio was updated by an automated Selenium test."
    
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.clear()
    username_field.send_keys(new_username)
    
    about_me_field = driver.find_element(By.NAME, "about_me")
    about_me_field.clear()
    about_me_field.send_keys(new_bio)
    
    driver.find_element(By.NAME, "submit").click()

    success_message = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert"))
    )
    assert "Your changes have been saved." in success_message.text
    
    open_navbar_if_collapsed(driver)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Profile"))).click()
    
    page_text = driver.find_element(By.TAG_NAME, 'body').text
    assert new_username in page_text
    assert new_bio in page_text