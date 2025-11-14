from datetime import datetime
from .e2e_helpers import *


def unique_user(base_name="user"):
    suffix = uuid.uuid4().hex[:6]
    username = f"{base_name}{suffix}"
    email = f"{username}@gmail.com" 
    password = "Password123!"
    return username, email, password

def register_user(driver, username, email, password):
    driver.get(f"{BASE_URL}/auth/register")
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password2").send_keys(password)
    driver.find_element(By.NAME, "submit").click()
    
    try:
        wait.until(EC.url_contains('/auth/login'))
    except TimeoutException as exc:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        screenshot = f"registration_failed_{username}_{ts}.png"
        htmlfile = f"registration_failed_{username}_{ts}.html"

        try:
            driver.save_screenshot(screenshot)
            with open(htmlfile, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
        except Exception:
            pass

        raise AssertionError(f"Registration failed for user '{username}'. Did not redirect to login. Saved {screenshot} and {htmlfile}") from exc

def check_inbox(driver, expected_sender, expected_message):
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(f"{BASE_URL}/messages")
    wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{expected_sender}')]")))
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert expected_message in page_text, f"Message '{expected_message}' not found in inbox."

def test_full_user_message_flow(live_server, driver, setup_database):
    user1, user2 = setup_database
    
    test_password = "TestPassword123!"
    
    login_user(driver, user1.username, test_password)

    message_text = f"Hello from {user1.username}"
    send_message(driver, user2.username, message_text)

    logout_user(driver)

    login_user(driver, user2.username, test_password)

    check_inbox(driver, user1.username, message_text)