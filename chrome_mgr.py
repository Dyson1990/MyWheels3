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
import platform
import selenium.webdriver as webdriver
from selenium.webdriver.support.select import Select as webdriver_select
from selenium.webdriver.chrome.service import Service
from anti_useragent import UserAgent
from pathlib import Path
from loguru import logger

ua = UserAgent()
headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': ua.random,
           # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive'
            }

def get_local_chrome_ver():
    """
    Windows下可能需要修改注册表路径

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    _v : TYPE
        DESCRIPTION.

    """
    try:
        if platform.system() == 'Windows':
            import winreg  # 和注册表交互
            # import re  # 正则模块
            reg_path =  r'Software\Google\Chrome\BLBeacon'
            reg_key = "version"
            
            # 打开注册表，并获取版本号信息
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
            _v, _ = winreg.QueryValueEx(registry_key, reg_key)
            winreg.CloseKey(registry_key)
            logger.info(f'current chrome version: {_v}') # 这步打印会在命令行窗口显示

        elif platform.system() == 'Linux':
            # Linux的代码未测试
            import subprocess

            # 使用 subprocess 模块执行命令，获取输出结果
            output = subprocess.check_output(['google-chrome', '--version'], stderr=subprocess.STDOUT)
            
            # 将 bytes 对象转换为字符串，并提取版本号信息
            version_str = output.decode('utf-8').strip()
            _v = version_str.split(' ')[2]

            logger.info(f'current chrome version: {_v}') 
        else:
            raise Exception("目前只支持Windows、Linux系统")

        return _v
        
    except WindowsError as e:
        logger.error(f'check Chrome failed:{e}')
        
def get_chrome_source():
    """
    获取chromedriver官网上所有版本的具体版本号

    Returns
    -------
    url_dict : TYPE
        DESCRIPTION.

    """
    download_url = "https://chromedriver.chromium.org/downloads"
    import requests, parsel
    
    proxies = {'http': 'socks5://127.0.0.1:10808'
               , 'https': 'socks5://127.0.0.1:10808'}
    resp = requests.get(download_url, proxies=proxies)
    root = parsel.Selector(resp.text)
    e_as = root.xpath("//a[@class=\"XqQF9c\" and @target=\"_blank\"]")
    
    url_list = [e0.attrib["href"] for e0 in e_as if e0.attrib["href"].endswith("/")]
    func_ver = lambda s0: s0.split("?path=")[-1][:-1]
    url_dict = {func_ver(url0).split(".")[0]: func_ver(url0) for url0 in url_list[::-1]} # 取最靠上的版本

    return url_dict
    
def download_chromedriver(ver, save_dir=Path.home()):
    logger.info(f"target chromedriver version: {ver}")
    import requests, zipfile
    from tqdm import tqdm
    
    if platform.system() == 'Windows':
        fn = "chromedriver_win32.zip"
    elif platform.system() == 'Linux':
        fn = "chromedriver_linux64.zip"
    else:
        raise Exception("目前只支持Windows、Linux系统")
    
    url = f"https://chromedriver.storage.googleapis.com/{ver}/{fn}"
    proxies = {'http': 'socks5://127.0.0.1:10808'
               , 'https': 'socks5://127.0.0.1:10808'}
    
    # 注释、细节见requests_manager.py
    resp = requests.get(url, proxies=proxies, stream=True)
    total_size = int(resp.headers.get('Content-Length', 0))
    total_size_mb = round(total_size / (1024 * 1024), 2)
    progress_bar = tqdm(total=total_size_mb, unit='MB', desc=url.split('/')[-1], ncols=80)
    
    # 解压下载好的zip文件
    zip_path = save_dir/fn
    logger.info(f"ready to download:{url}")
    with open(zip_path, 'wb') as fw, progress_bar:
        for data in resp.iter_content(chunk_size=1024):
            fw.write(data)
            progress_bar.update(len(data) / (1024 * 1024))
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extract('chromedriver.exe', save_dir)
    
    os.remove(zip_path)
    exe_path = save_dir/'chromedriver.exe'
    fn_new = f'chromedriver_{platform.system()}_{ver.split(".")[0]}.exe'
    exe_path = exe_path.rename(save_dir/fn_new)
    return exe_path
    

def chromedriver(engine_path, **kwargs):
    global headers
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
    print(local_chrome_ver)
    target_ver = source_d[local_chrome_ver.split(".")[0]]
    exe_path = download_chromedriver(target_ver)
    print(exe_path)
    os.remove(exe_path)
    
    # https://chromedriver.storage.googleapis.com/index.html?path=112.0.5615.49/chromedriver_win32.zip
    # https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip
    
    # driver.get('http://lhnb.mofcom.gov.cn/publicity/info?id=1264473')
    # with codecs.open('test_driver.html', 'w', 'utf-8') as f:
    #     f.write(driver.page_source)

    
    """
    from selenium import webdriver # 引入配置对象DesiredCapabilities from selenium.webdriver.common.desired_capabilities import DesiredCapabilities dcap = dict(DesiredCapabilities.PHANTOMJS) #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器 dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS)) # 不载入图片，爬页面速度会快很多 dcap["phantomjs.page.settings.loadImages"] = False # 设置代理 service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5'] #打开带配置信息的phantomJS浏览器 driver = webdriver.PhantomJS(phantomjs_driver_path, desired_capabilities=dcap,service_args=service_args) # 隐式等待5秒，可以自己调节 driver.implicitly_wait(5) # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项 # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。 driver.set_page_load_timeout(10) # 设置10秒脚本超时时间 driver.set_script_timeout(10)
    """
