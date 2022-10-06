import os
import re
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, Request, Response, Position


def create_image_directory():
    image_directory = os.path.split(os.path.realpath(sys.argv[0]))[0] + '/images'
    # print(image_directory)
    if not os.path.exists(image_directory):
        Path(image_directory).mkdir(parents=True, exist_ok=True)
    return image_directory


def on_request(request: Request):
    print(request)


def on_response(response: Response):
    print(response)
    print(f'响应状态码: {response.headers}')
    print(f'第二组内容: {response.ok} {response.url}')


def main():
    with sync_playwright() as p:
        for i in range(1, 52):
            for browser_type in [p.chromium]:
                browser = browser_type.launch(headless=True)
                page = browser.new_page()
                # page.on("request", on_request)
                # page.on("response", on_response)
                # page.on("requestfailed", on_request)
                # # page.on("responsefailed", on_response)
                # page.on("requestfinished", on_request)
                # page.on("response", on_response)
                # page.on("response", on_response)

                page.goto("http://122.4.213.20:8006/", wait_until="domcontentloaded")

                # canvas = page.locator('.canvas_container canvas:first-child')
                # dict = canvas.evaluate("canvas => canvas.getBoundingClientRect()")
                # left = dict.get('left')
                # top = dict.get('top')
                # width = dict.get('width')
                # height = dict.get('height')
                # print(dict)
                page.type('#txtUserName', 'xxxx', delay=100)

                page.type('#_easyui_textbox_input1', 'xjkljkfd', delay=100)

                slider = page.locator('.sliderImgPuzzle')
                # drag_button.bounding_box()
                # canvas = page.locator('.canvas_container canvas:first-child')
                # print(canvas.bounding_box())
                # cao = drag_button.evaluate()

                # fuck = drag_button.evaluate("div => { let bounding_box = {}; new MutationObserver((mutationList, observer) => { for (const mutation of mutationList){if(mutation.type === 'attributes') { const box = document.getElementsByClassName('canvas_container')[0].getBoundingClientRect(); Object.defineProperty(bounding_box, 'left', {value:box.left}); Object.defineProperty(bounding_box, 'top', {value: box.top});Object.defineProperty(bounding_box, 'width',{value:box.width});Object.defineProperty(bounding_box, 'height', {value: box.height}); } }}).observe(document.getElementsByClassName('canvas_container')[0],{attributes: true});var mouseevent = new MouseEvent('mouseover', {'view': window, 'bubbles': false, 'cancelable': true});document.getElementsByClassName('sliderImgPuzzle')[0].dispatchEvent(mouseevent); return bounding_box;}")
                image_directory = create_image_directory()
                # fuck = page.evaluate("div => { console.log(div);}", drag_button)
                # print(fuck)

                slider.click(button='middle', delay=5000)
                canvas_container = page.locator(
                    '//div[@class="canvasContainer" and contains(@style,"display: block" )]')

                # if Path(f'{image_directory}/captcha.png').is_file():
                #     os.remove(f'{image_directory}/captcha.png')
                bbox = canvas_container.bounding_box()
                page.screenshot(path=f'{image_directory}/captcha-{i}.png',
                                clip={'x': bbox['x'], 'y': bbox['y'], 'width': bbox.get('width'),
                                      'height': bbox.get('height')})

                out_bytes = subprocess.check_output(
                    ["python", os.path.dirname(__file__) + "./yolov5/detect.py", "--weights",
                     os.path.dirname(__file__) + "./yolov5/runs/train/exp/weights/best.onnx",
                     "--source", f'{image_directory}/captcha-{i}.png'])
                out_text = out_bytes.decode('utf-8')
                offset = re.search("^[0-9]*", out_text).group(0)
                print(offset)
                print(type(offset))
                slider_box = slider.bounding_box()
                # slider.hover()
                #
                page.mouse.move(slider_box.get('x') + slider_box.get('width') / 2,
                                slider_box.get('y') + slider_box.get('height') / 2)

                page.mouse.down()
                # print(float(offset))
                # print(slider_box.get('x'))
                page.mouse.move(slider_box.get('x') + float(offset), slider_box.get('y'),
                                steps=30)
                page.mouse.up()
                page.screenshot(path=f'{image_directory}/checkifmove-{i}.png')
                browser.close()
                # pos = Position(x=slider_box.get('x') + float(offset),y=slider_box.get('y'))
                # page.drag_and_drop('.sliderImgPuzzle', '.sliderImgPuzzle', target_position=pos,force=True)
                # try:
                #     page.wait_for_selector("//div[text()='请按住滑块向右滑动填充拼图！']", timeout=30000)
                #     print("没有完成拼图")
                # except:
                #     print("没有出现填充拼图要求")
                #
                # page.wait_for_timeout(2000)
                # msg_check = page.locator(
                #     '//div[@id="msg"]')
                # if msg_check.text_content() is None:
                #     print("没有等到元素出现")
                # if "验证成功" in msg_check.text_content():
                #     print("确实成功了")
                # btn_login = page.locator("#btnLogin")
                # btn_login.click()
                # print("点击登录了")
                # try:
                #     page.wait_for_selector("//div[@class=panel-title and text()='友情提示']", timeout=10000)
                # except:
                #     print("没有出现友情提示框")
                # print("爬虫结束了")
                # time.sleep(2)
                # page.drag_and_drop(target_position={ x: offset + slider.bounding_box().get('x'), y:slider.bounding_box().get('y')})
                # page.mouse.up()
                # ele = page.locator("h2")

                # print(type(expect(ele.text_content())))
                # expect(ele.text_content()).to_contain_text('long pressed')


main()
