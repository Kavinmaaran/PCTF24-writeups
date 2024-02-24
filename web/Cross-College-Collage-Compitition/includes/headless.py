from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

with open('flag.txt', "r") as file:
    flag = file.read()


def visit_with_cookies(link_submitted,innerImageTag):

    options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument("-headless")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)
    try:
        browser.set_page_load_timeout(10)
        browser.get(link_submitted)
        browser.add_cookie({'name' : 'foo', 'value' : flag})
        browser.execute_script("""
        function post(path, params, method='post') {
        const form = document.createElement('form');
        form.method = method;
        form.action = path;
    
        for (const key in params) {
            if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];
    
            form.appendChild(hiddenField);
        }
        }
    
        document.body.appendChild(form);
        form.submit();
        }

        post(arguments[1], arguments[0]);
        """, {'content': innerImageTag.__str__()}, link_submitted)
        time.sleep(1)
        browser.quit()
    except Exception as e:
        print(e)
        browser.quit()
