import json
import nodriver as uc
import logging
from time import sleep

async def login(username: str,
          password: str,
          save_session: str = False) -> tuple[str, str]:
  """Login to instagram with given credential and return the tokens dtsg and sessionid,
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
    tab = await driver.get('https://www.instagram.com/accounts/login/')
    await tab

    # Reject unnecessary cookies
    reject_cookies = await tab.select('button[class="_a9-- _ap36 _a9_1"]')
    if reject_cookies is not None:
      await reject_cookies.click()

    await tab

    # Fill the username and password input fields
    username_input = await tab.select('input[name="username"]')
    await username_input.send_keys(username)
    password_input = await tab.select('input[name="password"]')
    await password_input.send_keys(password)

  # Locate and click the login button
    sleep(1)
    login_button = await tab.select("button[type='submit']")
    await login_button.click()
    
    await tab
    
    i = 0
    dtsg = None
    while i < 3 and dtsg == None:
      i += 1
      sleep(5)
      await tab.wait_for(selector='#__eqmc', timeout=60)

      data = await tab.query_selector('#__eqmc')
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