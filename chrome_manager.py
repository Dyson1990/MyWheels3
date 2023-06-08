# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: driver_manager.py
    @time: 2017/10/30 15:56
    
    @notice: 感谢https://www.cnblogs.com/z417/p/13785734.html z417的博文
--------------------------------
"""

import os
import random
import platform
import selenium.webdriver as webdriver
from selenium.webdriver.support.select import Select as webdriver_select
from selenium.webdriver.chrome.service import Service

from pathlib import Path



user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


user_agent = random.choice(user_agent_list)
headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': user_agent,
           # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive'
            }

def get_local_chrome_ver():
    if platform.system() == 'Windows':
        import winreg  # 和注册表交互
        import re  # 正则模块
        
        try:
            version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本号的正则表达式
            # 从注册表中获得版本号
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
            _v, _type = winreg.QueryValueEx(key, 'version')
            print('Current Chrome Version: {}'.format(_v)) # 这步打印会在命令行窗口显示
    
            return version_re.findall(_v)[0]  # 返回前3位版本号
    
        except WindowsError as e:
            print('check Chrome failed:{}'.format(e))
    else:
        raise Exception("目前只支持Windows系统")
        
def get_chrome_source():
    download_url = "https://chromedriver.chromium.org/downloads"
    import requests, parsel
    
    proxies = {'http': 'socks5://127.0.0.1:10808'
               , 'https': 'socks5://127.0.0.1:10808'}
    resp = requests.get(download_url, proxies=proxies)
    root = parsel.Selector(resp.text)
    e_as = root.xpath("//a[@class=\"XqQF9c\" and @target=\"_blank\"]")
    
    url_list = [e0.attrib["href"] for e0 in e_as if e0.attrib["href"].endswith("/")]
    func_ver = lambda s0: s0.split("?path=")[-1].split(".")[0]
    url_dict = {func_ver(url0): url0 for url0 in url_list[::-1]} # 取最靠上的版本

    return url_dict
    
def download_chromedriver(url_root, save_path=Path.home()):
    import requests
    
    if platform.system() == 'Windows':
        fn = "chromedriver_win32.zip"
        url = f"{url_root}fn"
    else:
        raise Exception("目前只支持Windows系统")
        
    proxies = {'http': 'socks5://127.0.0.1:10808'
               , 'https': 'socks5://127.0.0.1:10808'}
    print(url)
    resp = requests.get("https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip", proxies=proxies)
    with open(save_path/fn, "wb") as fw:
        fw.write(resp.content)


def chromedriver(engine_path, **kwargs):
    # 不让Chrome显示界面
    #display = pyvirtualdisplay.Display(visible=False)
    #display.start()

    options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument("--headless")
    for key in headers:
        s = '{}="{}"'.format(key, headers[key])
        options.add_argument(s)
    if 'proxy' in kwargs:
        options.add_argument('--proxy-server=http://%s' % kwargs['proxy'])
        
    # 尝试传参
    service = Service(engine_path)
    driver = webdriver.Chrome(service=service                                       
                              # , chrome_options=options)
                              , options=options)

    #display.stop()
    driver.set_window_size(1920, 1080)
    return driver

if __name__ == '__main__':

# =============================================================================
#     sysstr = platform.system()
#     if sysstr == 'Windows':
#         engine_path = os.path.join(os.getcwd()
#                                  , 'selenium_driver'
#                                  , 'chromedriver_win32.exe')
#     elif sysstr == 'Linux':
#         engine_path = os.path.join(os.getcwd()
#                                  , 'selenium_driver'
#                                  , 'chromedriver_linux64')
#     else:
#         raise Exception('unknown system')
# =============================================================================
    # engine_path = Path.home()/"chromedriver111_win.exe"
        
    # driver = chromedriver(engine_path)
    
    source_d = get_chrome_source()
    local_chrome_ver = get_local_chrome_ver()
    url_root = source_d[local_chrome_ver.split(".")[0]]
    download_chromedriver(url_root)
    
    # driver.get('http://lhnb.mofcom.gov.cn/publicity/info?id=1264473')
    # with codecs.open('test_driver.html', 'w', 'utf-8') as f:
    #     f.write(driver.page_source)

    
    
    
    """
    from selenium import webdriver # 引入配置对象DesiredCapabilities from selenium.webdriver.common.desired_capabilities import DesiredCapabilities dcap = dict(DesiredCapabilities.PHANTOMJS) #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器 dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS)) # 不载入图片，爬页面速度会快很多 dcap["phantomjs.page.settings.loadImages"] = False # 设置代理 service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5'] #打开带配置信息的phantomJS浏览器 driver = webdriver.PhantomJS(phantomjs_driver_path, desired_capabilities=dcap,service_args=service_args) # 隐式等待5秒，可以自己调节 driver.implicitly_wait(5) # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项 # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。 driver.set_page_load_timeout(10) # 设置10秒脚本超时时间 driver.set_script_timeout(10)
    """
