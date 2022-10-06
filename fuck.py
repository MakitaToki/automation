from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        for browser_type in [p.chromium]:
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto("http://122.4.213.20:8006/")
            page.type('#txtUserName', 'xxxx')


            page.type('#_easyui_textbox_input1', 'xjkljkfd')
            locator = page.locator('.sliderImgPuzzle')
            # canvasContainer = page.locator('.canvasContainer')
            time.sleep(1)
            locator.hover()
            canvas = page.locator('.canvasContainer canvas:first-child')
            dict = canvas.evaluate("canvas => canvas.getBoundingClientRect()")
            left = dict.get('left')
            top = dict.get('top')
            width = dict.get('width')
            height = dict.get('height')
            # print(dict)
            # canvasContainer.evaluate("cc => {new MutationObserver((mutation, observer) => {if(mutation.type === 'attributes'){alert(`${observer}`)}}).observe(cc, {attributes: true})}")
            time.sleep(1)
            locator.hover()


            locator.dispatch_event('mouseover',{

                page.screenshot(path='D:/code/playwright教程/image/example6.png'),
                # print(canvasContainer.bounding_box())
                # canvasContainer.screenshot(path='D:/code/playwright教程/image/example2.png')
            }, timeout=40000)
            # canvas = page.locator('')
            # page.hover('.sliderImgPuzzle')

            browser.close()

main()