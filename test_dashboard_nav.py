import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pjoin = os.path.join

def get_list_items(browser):
    return [{
        'link': a.get_attribute('href'),
        'label': a.find_element_by_class_name('item_name').text,
        'element': a,
    } for a in browser.find_elements_by_class_name('item_link')]


def wait_for_selector(browser, selector, timeout=10):
    wait = WebDriverWait(browser, timeout)
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

import time

def test_items(authenticated_browser, visited=None):
    tree_root_url = authenticated_browser.current_url
    if visited is None:
        visited = set()

    wait_for_selector(authenticated_browser, '.item_link')
    items = get_list_items(authenticated_browser)
    print(authenticated_browser.current_url, len(items))

    # steps_back = 0
    # while True:
    #     find items
    #     down a level
    #     steps_back += 1
    #     back
    #     if no folders:
    #         pass
    #
    # for i in range(steps_back):
    #     back

    for item in items:
        print(item)
        url = item['link']
        if url.startswith(tree_root_url):
            print("Going to", url)
            if url in visited:
                continue
            visited.add(url)
            #authenticated_browser.get(url)
            item['element'].click()
            wait_for_selector(authenticated_browser, '.item_link')
            assert authenticated_browser.current_url == url


            time.sleep(2)

            test_items(authenticated_browser, visited)
            authenticated_browser.back()
            wait_for_selector(authenticated_browser, '.item_link')

            time.sleep(1)

    print()
