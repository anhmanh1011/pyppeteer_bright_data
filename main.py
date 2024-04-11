import asyncio
import time

import pyppeteer
from faker import Faker
from gologin import GoLogin

import imap

gl = GoLogin({
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjEyNzQ0ZWYyMTA2ZWU3MThkMmI1NjkiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjEyNzQ2OWFjYWMzZmY1MGFlYzZlMDcifQ.grLseXt_Plj6qgKkgxd95sDKi0huDixqnr1P-t9ONtA",
})


async def main():
    first_name, last_name, user_name = generate_name()
    profile_id = create_profile(user_name)
    # profile_id = '66182a2a805fd8aca0d801f1'
    print('profile_id' + profile_id)
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjEyNzQ0ZWYyMTA2ZWU3MThkMmI1NjkiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjEyNzQ2OWFjYWMzZmY1MGFlYzZlMDcifQ.grLseXt_Plj6qgKkgxd95sDKi0huDixqnr1P-t9ONtA",
        "profile_id": profile_id,
    })
    debugger_address = gl.start()
    browser = await pyppeteer.connect(browserURL="http://" + debugger_address, defaultViewport=None)
    try:

        page = await browser.newPage()
        await gl.normalizePageView(page)
        await page.goto("https://brightdata.com")
        await page.waitForSelector(selector='#btn_sign_up')
        await page.click(selector='#btn_sign_up')
        time.sleep(2)
        selector = '#brd_cookies_bar_accept'  # Replace with your actual selector

        # Check if the element exists
        element = await page.querySelector(selector)
        if element:
            # If the element exists, click on it
            await element.click()
        else:
            # If the element does not exist, skip or perform an alternative action
            print("Element not found, skipping the click action.")

        # Input first name
        await page.waitForSelector('[name="firstname"]')
        await page.type('[name="firstname"]', first_name)

        # Input last name
        await page.type('[name="lastname"]', last_name)

        # Input email
        await page.type('[name="email"]', 'corbinkohnerk@hotmail.com')

        # Select an option from a dropdown menu
        await page.select('[name="numemployees"]', '1-9 employees')

        # Click on a checkbox or another element
        await page.click('[name="LEGAL_CONSENT.subscription_type_9328122"]')

        # Click the submit button
        css_selector = "input[type='submit'].hs-button.primary.large"
        await page.click(css_selector)

        # Selector for the input field
        input_selector = '.cp_input'

        # Wait for the input element to be loaded
        await page.waitForSelector(input_selector)

        code = imap.read_mail('corbinkohnerk@hotmail.com', 'AxYVtx03', 'noreply@brightdata.com',
                              'Bright Data - Welcome')  # Replace with the text you want to type
        await page.type(input_selector, code)

        # CSS Selector for the submit button
        submit_button_selector = '.zbtn.code_submit'

        # Wait for the submit button to be loaded
        await page.waitForSelector(submit_button_selector)

        # Click on the submit button
        await page.click(submit_button_selector)
        time.sleep(5)
        await page.goto('https://brightdata.com/cp/billing_flow')
        # Selector for the button based on the data-testid attribute
        button_selector = '[data-testid="modal_footer_cancel_button"]'

        # Wait for the button to be loaded
        await page.waitForSelector(button_selector)

        # Click on the button
        await page.click(button_selector)

        time.sleep(10000)

    except Exception as e:
        e.with_traceback()
        print('error')
    finally:
        time.sleep(10000)
        await browser.close()
        gl.stop()


def generate_name():
    fake = Faker('en_US')
    first_name = fake.first_name()
    last_name = fake.last_name()
    user_name = fake.user_name()

    return first_name, last_name, user_name


def create_profile(profile_name: str):
    profile_id = gl.create({
        "name": profile_name,
        "os": 'mac',
        "navigator": {
            "language": 'en-US',
            "userAgent": 'random',
            "resolution": '1024x768',
            "platform": 'mac',
        },
        'proxy': {
            "mode": "http",
            "host": "resi-v4-targeted.whiteproxies.com",
            "port": 27007,
            "username": '',
            "password": '',
        },
        "webRTC": {
            "mode": "alerted",
            "enabled": True,
        },
        "storage": {
            "local": True,
            # Local Storage is special browser caches that websites may use for user tracking in a way similar to cookies.
            # Having them enabled is generally advised but may increase browser profile loading times.

            "extensions": True,
            # Extension storage is a special cotainer where a browser stores extensions and their parameter.
            # Enable it if you need to install extensions from a browser interface.

            "bookmarks": True,  # This option enables saving bookmarks in a browser interface.

            "history": True,  # Warning! Enabling this option may increase the amount of data required
            # to open/save a browser profile significantly.
            # In the interests of security, you may wish to disable this feature,
            # but it may make using GoLogin less convenient.

            "passwords": True,  # This option will save passwords stored in browsers.
            # It is used for pre-filling login forms on websites.
            # All passwords are securely encrypted alongside all your data.

            "session": True,  # This option will save browser session. It is used to save last open tabs.

            "indexedDb": False
            # IndexedDB is special browser caches that websites may use for user tracking in a way similar to cookies.
            # Having them enabled is generally advised but may increase browser profile loading times.
        }
    })
    return profile_id;


asyncio.get_event_loop().run_until_complete(main())
