# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 17:35:21 2023

@author: Weave
"""
from pathlib import Path
py_dir = Path(__file__).parent

import math
import collections
import pytesseract

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.patches import Rectangle
from PIL import Image, ImageSequence

def rgb_to_hex(rgb_tup: tuple):
    """
    原文链接：https://blog.csdn.net/sinat_37967865/article/details/93203689

    Parameters
    ----------
    rgb : TYPE
        DESCRIPTION.

    Returns
    -------
    color : TYPE
        DESCRIPTION.

    """
    color = '#'
    for i in rgb_tup:
        num = int(i)
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color

def hex_to_rgb(hex_str: str):
    """
    原文链接：https://blog.csdn.net/sinat_37967865/article/details/93203689

    Parameters
    ----------
    hex : TYPE
        DESCRIPTION.

    Returns
    -------
    rgb : TYPE
        DESCRIPTION.

    """
    r = int(hex_str[1:3],16)
    g = int(hex_str[3:5],16)
    b = int(hex_str[5:7], 16)
    rgb = str(r)+','+str(g)+','+str(b)
    return rgb

def plot_colortable(colors, ncols=4, sort_colors=False):
    """
    展示颜色所用的
    
    plot_colortable(mcolors.CSS4_COLORS)
    plt.show()
    

    Parameters
    ----------
    colors : TYPE
        colors目前只接收这种形式的传参，mcolors.CSS4_COLORS:
        {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', 'aqua': '#00FFFF'
         ......
         , 'whitesmoke': '#F5F5F5', 'yellow': '#FFFF00', 'yellowgreen': '#9ACD32'
         }

    ncols : TYPE, optional
        DESCRIPTION. The default is 4.
    sort_colors : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        names = sorted(
            colors, key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))
    else:
        names = list(colors)

    n = len(names)
    nrows = math.ceil(n / ncols)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')
        
        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=colors[name], edgecolor='0.7') # 
        )

    return fig

def rgb_list(img):
    """
    将图片对象转换为rgb矩阵
    
    例如3*3全白图片：
    [(255,255,255), (255,255,255), (255,255,255)
    , (255,255,255), (255,255,255), (255,255,255)
    , (255,255,255), (255,255,255), (255,255,255)]

    """
    img_array = img.load()
    width = img.size[0]
    height = img.size[1]
    
    output = []
    for x0 in range(1, width - 1):
        for y0 in range(1, height - 1):
            output.append(img_array[x0, y0])
    return output

def gray_level(rgb_tup):
    """
    计算一个rgb数组的灰度值
    """
    return rgb_tup[0] * 0.299 + rgb_tup[1] * 0.587 + rgb_tup[2] * 0.114

def uniform_color(img, color_set, target_color=(255,255,255)):
    """
    统一颜色：
    即将图片中，所有像素读出来，若颜色存在于color_set中，则替换为target_color，默认白色。
    """
    img_array = img.load()
    width = img.size[0]
    height = img.size[1]

    # 遍历图片的每一个像素点
    for x0 in range(1, width - 1):
        for y0 in range(1, height - 1):
            if img_array[x0, y0] in color_set:
                img_array[x0, y0] = target_color
    return img

def rm_frame(img, depth=2, bg_color = (255,255,255)):
    """
    去除图片边框
    """
    img_array = img.load()
    width = img.size[0]
    height = img.size[1]
    
    # 遍历“边框”的每一个像素点
    for dep0 in range(depth):
        for x0 in range(0, width - 1):
            img_array[x0, 0+dep0] = bg_color
            img_array[x0+1, height-1-dep0] = bg_color
    
        for y0 in range(0, height-1):
            img_array[0+dep0, y0+1] = bg_color
            img_array[width-1-dep0, y0] = bg_color
            
    return img

def make_box_by_x(img, bg_color=(255,255,255), idx=0, **correction):
    """
    制作box列表，用来生成tesseract的box文件
    """
    img_array = img.load()
    width = img.size[0]
    height = img.size[1]
    
    # 取出所有满足条件的x0坐标：在x=x0时，y轴方向上所有的点的颜色都是bg_color
    x_blank = []
    for x0 in range(0, width-1):
        b0 = all([img_array[x0, y0]==bg_color for y0 in range(0, height-1)])
        if b0:
            x_blank.append(x0)
            
    """
    取出图片中，所有字符边界的x轴区间。即[[3,7], [10,16]]表示：
   x1 x2 x3 x4
    | |   | |
    |Y|   |C|
    | |   | |
   x1=3, x2=7, x3=10, x4=16
    """
    x_box = []
    for i0 in range(len(x_blank)-1):
        if x_blank[i0+1] - x_blank[i0] > 1:
            x_box.append([x_blank[i0], x_blank[i0+1]])
    
    # x_box中，确定下了一个字符的左右边界，下面单独确定每个字符的上下边界
    box_list = []
    for box0 in x_box:
        l0 = [y0 for x0 in range(box0[0], box0[1]+1)
                 for y0 in range(0, height-1)
                 if img_array[x0, y0]!=bg_color
             ]
        box_list.append([box0[0]+correction.get("x", 0) # +1
                         , min(l0)+correction.get("y", 0) # +2
                         , box0[1]+correction.get("w", 0) # 
                         , max(l0)-min(l0)+correction.get("h", 0) # +3
                         , idx]
                       )
    return box_list

# =============================================================================
# def make_box(img, bg_color=(255,255,255), idx=0, **correction):
#     img_array = img.load()
#     width = img.size[0]
#     height = img.size[1]
#     
#     x_blank = []
#     for x0 in range(0, width-1):
#         b0 = all([img_array[x0, y0]==bg_color for y0 in range(0, height-1)])
#         if b0:
#             x_blank.append(x0)
#             
#     y_blank = []
#     for y0 in range(0, height-1):
#         b0 = all([img_array[x0, y0]==bg_color for x0 in range(0, width-1)])
#         if b0:
#             y_blank.append(y0)
#     
#     x_box = []
#     for i0 in range(len(x_blank)-1):
#         if x_blank[i0+1] - x_blank[i0] > 1:
#             x_box.append([x_blank[i0], x_blank[i0+1]])
#             
#     y_box = []
#     for i0 in range(len(y_blank)-1):
#         if y_blank[i0+1] - y_blank[i0] > 1:
#             y_box.append([y_blank[i0], y_blank[i0+1]])
#     
#     box_list = []
#     for box1 in x_box:
#         for box2 in y_box:
#             box_list.append([box1[0]+correction.get("x", 0) # +1
#                              , box2[0]+correction.get("y", 0) # +2
#                              , box1[1]+correction.get("w", 0) # 
#                              , box2[1]-box2[0]+correction.get("h", 0) # +3
#                              , idx]
#                            )
#     return box_list
# =============================================================================


if __name__ == "__main__":
    plot_colortable(mcolors.CSS4_COLORS)
    plt.show()

