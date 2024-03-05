import pickle
import time
from urllib.parse import unquote_plus
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging

logging.basicConfig(level=logging.INFO)

def login(driver,#: Union[Chrome, Edge, Firefox, Safari, Remote],
          username: str,
          password: str,
          save_session: str = False) -> tuple[str, str]:
  """Login to instagram with given credential, and return True if success,
  else False.

  Args:
      driver (:obj:`selenium.webdriver.remote.webdriver.WebDriver`): selenium
        driver for controlling the browser to perform certain actions.
      username (str): username for login.
      password (str): corresponding password for login.
      save_session (str, optional): If provided, the session will be saved
        to the given path. Defaults to False.

  Returns:
      fb_dtsg, session: if login successes; otherwise False.

  Examples:
      >>> from seleniumwire import webdriver
      >>> driver = webdriver.Chrome('path_to_chromedriver')
      >>> from threadscraper.login import login
      >>> login(driver, "your_username", "your_password", "path_to_save_session")
      >>> driver.quit()
  """
  try:
      
    driver.get('https://www.instagram.com/accounts/login/')

    # Wait until the page is rendered
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))

    reject_cookies_btn = driver.find_element(By.CSS_SELECTOR, "._a9--._ap36._a9_1")
    if reject_cookies_btn:
      reject_cookies_btn.click()
      time.sleep(1)

    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Locate and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait until the page url changes and is completely loaded
    while driver.current_url == 'https://www.instagram.com/accounts/login/':
        time.sleep(1)

    not_turn_on_notifications_btn = driver.find_element(By.CSS_SELECTOR, '._a9--._ap36._a9_1')
    if not_turn_on_notifications_btn:
      not_turn_on_notifications_btn.click()

    cookies = driver.get_cookies()
    for cookie in cookies:
      if cookie['name'] == 'sessionid':
        sessionid = cookie['value']
        sessionid = unquote_plus(sessionid)
        break
    
    # Listen to a request to https://www.instagram.com/api/graphql
    for request in driver.requests:
        if request.url == 'https://www.instagram.com/api/graphql':
          fb_dtsg = request.body.decode().split('fb_dtsg=')[1].split('&')[0]
          fb_dtsg = unquote_plus(fb_dtsg)
          break

    if save_session:
      with open(save_session, 'w') as file:
        file.write('DTSG=' + fb_dtsg + '\n')
        file.write('SESSION=' + sessionid + '\n')
      
    return fb_dtsg, sessionid
  except Exception as e:
    logging.error(f'Error while logging in: {e}')
    return False