import json
import nodriver as uc
import logging
from time import sleep

async def login(username: str,
          password: str,
          save_session: str = False) -> tuple[str, str]:
  """Login to threads with given credential and return the tokens dtsg and sessionid,
  else False.

  Args:
      username (str): username for login.
      password (str): corresponding password for login.
      save_session (str, optional): If provided, the session will be saved
        to the given path. Defaults to False.

  Returns:
      fb_dtsg, session: if login successes; otherwise False.

  Examples:
      >>> dtsg, session = uc.loop().run_until_complete(login('your_username', 'your_password'))
      ('fb_dtsg', 'session')
      - or -
      >>> import asyncio
      >>> asyncio.run(login('your_username', 'your_password'))
      - For jupyer notebooks: - (asyncio may still cause problems in jupyter notebooks)
      >>> import asyncio
      >>> dtsg, session = await asyncio.create_task(login('your_username', 'your_password'))
  """
  try:
    driver = await uc.start()
    tab = await driver.get('https://www.threads.net/accounts/login/')
    sleep(2)
    
    logging.info("Going to threads.net...")
    await tab

    try:
      logging.info("Rejecting cookies")
      reject_cookies = await tab.wait_for('[role="dialog"] > div >div > div > div > div > div > .x1i10hfl[role="button"]')
      reject_cookies = await tab.query_selector_all('[role="dialog"] > div >div > div > div > div > div > .x1i10hfl[role="button"]')
      print(len(reject_cookies))
      await reject_cookies[1].click()
    except:
      logging.error("Couldn't find 'Reject Cookies' button")
    
    try:
      sleep(1)
      logging.info("Rejecting cookies again")
      reject_cookies = await tab.wait_for('[role="dialog"] > div >div > div > div > div > div > .x1i10hfl[role="button"]')
      reject_cookies = await tab.query_selector_all('[role="dialog"] > div >div > div > div > div > div > .x1i10hfl[role="button"]')
      print(len(reject_cookies))
      await reject_cookies[1].click()
    except:
      logging.error("Couldn't find 'Reject Cookies' button")
    

    try:
      logging.info("Looking for 'Login with Instagram' button")
      btn = await tab.wait_for('a[aria-selected="false"]',timeout=20)
      await btn.click()
    except:
      logging.error("Couldn't find login button")
    
    username_input = await tab.wait_for('input[autocomplete="username"]')
    await username_input.send_keys(username)
    sleep(1)
    password_input = await tab.select('input[autocomplete="current-password"]')
    await password_input.send_keys(password)

  # Locate and click the login button
    sleep(1)
    login_button = await tab.select('div[role="button"]')
    await login_button.click()
    
    dtsg = None   
    i = 0
    while i < 3 and dtsg == None:
      i += 1
      sleep(5)
      try:
        data = await tab.wait_for('#__eqmc', timeout=60)
      except:
        logging.error("Couldn't find the dtsg token")

      if data.text != None:
        data = json.loads(data.text)
        dtsg = data["f"]

    requests_style_cookies = await driver.cookies.get_all(requests_cookie_format=True)
    
    sessionid = None
    for cookie in requests_style_cookies:
      if cookie.name == 'sessionid':
        sessionid = cookie.value
      

    if save_session:
      with open(save_session, 'w') as file:
        file.write('DTSG=' + dtsg + '\n')
        file.write('SESSION=' + sessionid + '\n')
    driver.stop()
    return dtsg, sessionid
  except Exception as e:
    logging.error(f'Error while logging in: {e}')
    return False