import time
from selenium import webdriver  # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Correct import for ChromeDriverManager
from os import getcwd

options = Options()
options.add_argument('--use-fake-ui-for-media-stream')
options.add_argument('--headless')

def listen():
    # Create a Service instance with ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://aquamarine-llama-e17401.netlify.app/')
        txt_box = driver.find_element(By.ID, "textbox")
        last_txt = txt_box.get_attribute('value')

        while True:
            current_txt = txt_box.get_attribute('value')
            if current_txt != last_txt:
                print(current_txt)
                # Only write to file if there is a change
                with open(f'{getcwd()}\\input_cmd.txt', 'w') as file:
                    file.write(current_txt)
                last_txt = current_txt
            time.sleep(0.1)  # Adjust sleep duration if needed

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


import subprocess

def weather(area):
    subprocess.run(f'curl wttr.in/{area}')

