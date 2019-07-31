# 从“无招”到“有招”--浅析由JSON数据构建Panel Data

## 一骑红尘妃子笑，无人知是荔枝来

​	早在唐朝末期，杨贵妃酷爱吃荔枝。由于荔枝素有“一日而色变,二日而香变,三日而味变,四五日外,色香味尽去矣”的特点，极难保鲜，所以当时都是通过不断的在各地的驿站更换马匹，以最快的速度，从岭南速取荔枝回长安，以供杨贵妃享用。

​	而如今的互联网时代何尝不是如此，为了将数据以最快的速度呈现到用户的面前，全球各地的工程师都绞尽脑汁想对策。在时间的考验下，有两种格式被广泛使用--JSON以及HTML（XML的变种）格式。JSON格式以解析效率高、传输快、兼容性强著称，而HTML格式以展示效果好而闻名。

​	我们这里主要是讨论JSON数据。如果你写过爬虫项目，应该会注意到，互联网上很多用了Ajax技术的网站，传输数据都是用JSON格式来传的。更多的，很多API数据的格式，例如百度地图API，同样使用的JSON。

​	以下是静态爬虫中，“去哪儿网”获取航班数据的url（网址），大家可以直接复制到浏览器中访问，便能获取到数据。

[]: https://flight.qunar.com/fuzzysearch/inspire/search/singleCountry?callback=jQuery172037833562867516113_1560735493530&amp;depCode=BJS&amp;arr=%E5%85%8D%E7%AD%BE%2F%E8%90%BD%E5%9C%B0%E7%AD%BE&amp;arrType=2&amp;depDateRange=2019-06-19~2019-06-19%7C3&amp;filter=%7B%7D&amp;depRawDateRange=2019-06-19&amp;depRawDateRangeType=3&amp;_=1560735493631

​	为什么我们这里获取到的数据与我们直接在网页上看的数据不一样？那是因为我们访问这个网站的时候，这个JSON数据，还有很多其他的文件。

​	一般情况下，我们访问一个网站，网站服务器会先发送一个网页框架回来，然后我们的网页浏览器再根据网页框架中的链接再次申请数据。像图片、JSON数据这样的文件，都是这时候才被我们获取到的。若我们希望自己的爬虫能够高效运作，我们就需要学会直接申请JSON数据，自己解析JSON数据，而不是依靠浏览器来慢悠悠的完成。

​	在梳理JSON数据的过程中，虽然存在json_path这样的万能钥匙，但是我在工作学习中发现，很多客户光光是看着这扭来扭去的数据格式，就会心生厌恶。本着“客户即上帝”的原则，格式转换器的需求迫在眉睫。

​	

## 千里之行,始于足下

### JSON数据

>   ​	JSON(JavaScript Object Notation, JS 对象简谱) 是一种轻量级的数据交换格式。它基于 ECMAScript (欧洲计算机协会制定的js规范)的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据。简洁和清晰的层次结构使得 JSON 成为理想的数据交换语言。 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。
>
>   （这段介绍来自于百度百科）

### 结构化数据与非结构化数据

>   ​	结构化数据也称作行数据，是由二维表结构来逻辑表达和实现的数据，严格地遵循数据格式与长度规范，主要通过关系型数据库进行存储和管理。与结构化数据相对的是不适于由数据库二维表来表现的非结构化数据，包括所有格式的办公文档、XML、HTML、各类报表、图片和咅频、视频信息等。支持非结构化数据的数据库采用多值字段、子字段和变长字段机制进行数据项的创建和管理，广泛应用于全文检索和各种多媒体信息处理领域。
>
>   （这段介绍来自于百度百科，其实，XML、JSON格式这种应该算是半结构化数据）
>

### 结构化数据的特点

​	我们日常使用的数据，基本都是**结构化数据**，行是行，列是列。我觉得结构化数据方便的点在于，每一个数据都能非常清晰、非常方便的放在图表中。一些常用的数据分析或处理软件，例如Excel、SPSS、SAS等，都能将结构化数据与图表进行无缝连接。

### 面板数据

>   ​	面板数据(Panel Data)是将“截面数据”和“时间序列数据”综合起来的一种数据类型。具有“横截面”和“时间序列”两个维度，当这类数据按两个维度进行排列时，数据都排在一个平面上，与排在一条线上的一维数据有着明显的不同，整个表格像是一个面板，所以称为面板数据(Panel Data)。
>
>   （来源于
>
>   []: https://blog.csdn.net/secondlieutenant/article/details/79625694	"横截面数据、时间序列数据、面板数据"
>
>   ）
>

​	由此可见，面板数据简而言之，就是在截面数据的基础上加上时间维度，其实在数据处理的层面上与截面数据差不多，因为他们都是结构化数据。一个JSON数据中，如果有时间维度的话，则并不需要我们单独处理；若没有，则数据本身并不能做成面板数据。所以，**我们这里说的处理方法将不区分截面数据与面板数据**。（之后都称之为二维表）



## 明月几时有，把酒问青天

### JSON数据与面板数据

​	以下是一段包含时间维度的JSON格式数据（来源于企研数据工商企业微观数据库的统计表）：

```json
{
  "上海市": {
    "PROCODE": 310000,
    "DATA": [
      {
        "YEAR": 2009,
        "NEW": 93661,
        "EXIT": 45392,
        "STOCK": 657290,
        "APPLY_PATENT": 46032,
        "GRANT_PATENT": 33829,
        "GRANT_PATENT_FM": 14935,
        "GRANT_PATENT_SY": 9317,
        "GRANT_PATENT_WG": 9509,
        "APPLY_BRAND": 40747,
        "GRANT_BRAND": 27739
      },
      {
        "YEAR": 2010,
        "NEW": 109983,
        "EXIT": 33680,
  ......
    "云南省": {
    "PROCODE": 530000,
    "DATA": [
      {
        "YEAR": 2009,
        "NEW": 22072,
        "EXIT": 5346,
        "STOCK": 129401,
  ......
```

​	可以看到，其中包含相应年份的新增企业数（NEW），死亡企业数（EXIT），企业存量（Stock）等等。

​	我们的目标，是要做成类似于下面这样的二维表：

| PROVINCE | PROCODE | YEAR | NEW    | EXIT  | STOCK  |
| -------- | ------- | ---- | ------ | ----- | ------ |
| 上海市   | 310000  | 2009 | 93661  | 45392 | 657290 |
| 上海市   | 310000  | 2010 | 109983 | 33680 | 733593 |
| 上海市   | 310000  | 2011 | 118616 | 45866 | 806343 |
| 上海市   | 310000  | 2012 | 121399 | 46757 | 880985 |
| 上海市   | 310000  | 2013 | 138087 | 43831 | 975241 |
| ......   |         |      |        |       |        |
| 云南省   | 530000  | 2009 | 22072  | 5346  | 129401 |
| 云南省   | 530000  | 2010 | 22264  | 6556  | 145109 |
| ......   |         |      |        |       |        |

### JSON数据中一些术语的约定

​	之前的JSON数据中，我们抽象一下，可以得到这样的一个数据结构：

​		{某省名: {"PROCODE": 市码,"DATA": [{"YEAR": 年份， ....等等其他数据}]}}

​	仔细观察可以发现，这样的数据可以看做一个类似于“俄罗斯套娃”的盒子，每个盒子，我们约定为一个“阶”。

​	例如上面的“某省名”为第一阶，PROCODE和DATA为第二阶，YEAR为第四阶（[]方括号其实可以看作{}花括号中省略了索引）。最大为四阶，所以我们称这个JSON数据为四阶JSON数据。另外，我们将三阶以上（包括三阶）的JSON数据称为**高阶**JSON数据。

### 二阶JSON数据与CSV数据

​	二阶JSON可以很容易的用pandas来转化为CSV格式的数据（CSV可以看成是没有格式的XLSX格式数据，兼容性更好）。代码如下：

```python
In [1]: import pandas as pd

In [2]: json_data = {
             'col_a':{
                 'row1':123
                 , 'row2':321
                 }
             , 'col_b':{
                 'row1': 'abc'
                 , 'row2': 'abc'
                 }
             }

In [3]: df = pd.DataFrame(json_data)

In [4]: df.to_csv('./json_data.csv', encoding='utf_8_sig')
```

​	得到的二维表如下：

|      | col_a | col_b |
| ---- | ----- | ----- |
| row1 | 123   | abc   |
| row2 | 321   | abc   |

## 高阶JSON数据的窘境

​	高阶JSON由于维度过于复杂，很难直观的展示，我这里直接用代码来说明原因：

```python
In [1]: import pandas as pd

In [2]: json_data = {
             'col_a':{
                 'row1':{'detail2': 'qy'}
                 , 'row2': {'detail1': 'qy'}
                 }
             , 'col_b':{
                 'row1': 123
                 , 'row2': 'abc'
                 }
             }

In [3]: df = pd.DataFrame(json_data)

In [4]: df.to_csv('./json_data.csv', encoding='utf_8_sig')
```

​	我们只能得到这样一个表格：

|      | col_a             | col_b |
| ---- | ----------------- | ----- |
| row1 | {'detail2': 'qy'} | 123   |
| row2 | {'detail1': 'qy'} | abc   |

​	这样的情况下，我们仍然无法使用detail1和detail2中的数据（至少SPSS、STATA等软件没法用）。

​	显然，我们没法将这样的数据拿来画图，程序会将{'detail1': 'qy'} 与{'detail2': 'qy'}视为不同数据。更何况，在Python中“123”与“{'detail1': 'qy'}”甚至都不是同一类型的数据，根本没法做进一步的数据处理，非常令人沮丧。



## 山穷水尽疑无路，柳暗花明又一村

​	既然高阶JSON数据没法直接塞进一个二维表中，那么我们很自然的想到，将其分在多个二维表中保存，再根据需求来判断如何整合这些二维表。

```python
import pandas as pd
import numpy as np
import json

def multi_json2dataframes(json_obj, data_key='_id'):
    """
    万能JSON转DataFrame函数
    json_obj: json格式的对象，可以是字典、列表、json字符串
    data_key：拆开JSON数据后，用来连接不同子表的键
    """
    # 如果是以字符串的形式传入的JSON数据，则需要
    if isinstance(json_obj, (str, bytes)):
        json_obj = json.loads(json_obj) 
        
    # 将初始数据转化为dataframes
    ori_df = pd.DataFrame(json_obj, dtype=np.object)
    
    # 包含JSON格式的数据，不适合作为key使用
    type_func = lambda obj: isinstance(obj, (dict, list))
    if ori_df.loc[:, data_key].apply(type_func).any():
        raise(Exception('{}列包含JSON格式的数据，不适合作为key使用'.format(data_key)))
    
    # 因为之后需要将不同维度的
    ori_df = ori_df.set_index(data_key)
    df_pool = {'$': ori_df} # 构建待处理的DataFrame池
    res = {}
    while bool(df_pool):
        # str_title是其对应的DataFrame中数据的json_path
        str_title, df_tmp = df_pool.popitem()
        
        # 判断一列中是否有JSON格式的数据
        json_dtype = df_tmp.apply(lambda col:col.apply(type_func).any(), axis=0)
        
        # 分离出不是JSON格式的列，保存下来
        str_part = df_tmp.loc[:, json_dtype[json_dtype==False].index]
        if not str_part.empty:
            str_part.index.name = data_key
            res[str_title] = str_part.copy()
        
        # 分离出是JSON格式的列，放回df_pool中
        json_part = df_tmp.loc[:, json_dtype[json_dtype==True].index]
        
        if json_part.empty: # 避免将空的DataFrame放入df_pool
            continue
        
        # 这里的ser_key的构造还有待商榷
        for col in json_part.columns:
            ser = json_part.loc[:, col]
            ser_key = '{}/{}'.format(str_title, col)
            
            if ser_key in res.keys():
                ser_key = ser_key + '_dup'
            df_pool[ser_key] = pd.DataFrame(ser.to_dict()).T
            
    return res
```

我这段代码还有多个地方可以优化：

1.  对内存的利用不是很合理，json_obj读进来以后，没有把已经处理好的数据移出内存，也没有使用多进程来对多个df_tmp进行处理。遇到大文件可能会运行缓慢。
2.  使用的pandas库解析JSON而不是正则表达式，在性能上会有所欠缺。
3.  我这边只对df_tmp中的列进行了“是否为JSON格式”的判断。若df_tmp中有的列中，既有普通数据，又有JSON数据，结果里就会有点乱了。暂时没想好怎么存储一列中不同类型的数据，就先默认只要有JSON类型的数据，就把整列当成JSON格式的来做了。
4.  结果res中的key是我原本想用json_path，然而json_path的语法比较多，代码不够智能，而且可能存在错误。我以后想出来更有条理的之后再做更新。就目前而言，这个key不是很重要。

关于以上优化的实现，大家可以关注我的github：

[]: https://github.com/Dyson1990/MyWheels3/blob/master/json_manager.py



## 嘈嘈切切错杂弹，大珠小珠落玉盘

​	一顿敲击键盘后，是我们“见证奇迹的时刻”了。

​	我们现在再来看一个更加复杂但稍微规整一点的JSON格式数据（赋值为json_data）：

```json
{
	"col_a": {
		"index1": [{"detail1": ["qy11", "qy12"]}, {"detail2": "qy3"}, {"YEAR": 1996}],
		"index2": [{"detail1": ["qy21", "qy22"]}, {"detail2": "qy4"}, {"YEAR": 1987}]
	},
	"col_b": {
		"index1": 123,
		"index2": "abc"
	},
	"col_c": {
		"index1": "321",
		"index2": "123"
	},
	"key": {
		"index1": "row1",
		"index2": "row2"
	}
}
```

​	大家可以看见，我将时间维度加入了进去，但是却保存在了这个JSON文件中的一个小角落里。

​	调用之前的函数，并且将结果一个个打印出来：

```python
res_dict = multi_json2dataframes(json_data, 'key')
for data_title, df in res_dict.items():
    print('data_title: ', data_title)
    print(df)
    print('\n')
```

​	我们可以得到

名为“$”的表格：

| key  | col_b | col_c |
| ---- | ----- | ----- |
| row1 | 123   | 321   |
| row2 | abc   | 123   |

名为“$/col_a/2”的表格：

| key  | YEAR |
| ---- | ---- |
| row1 | 1996 |
| row2 | 1987 |

名为“$/col_a/1”的表格：

| key  | detail2 |
| ---- | ------- |
| row1 | qy3     |
| row2 | qy4     |

名为“$/col_a/0/detail1”的表格：

| key  | 0    | 1    |
| ---- | ---- | ---- |
| row1 | qy11 | qy12 |
| row2 | qy21 | qy22 |

​	到这里，我们就已经把所有的JSON数据都转化为一个个二维表了，而每个表之间都有key能关联上。

​	剩下的，只有把这些表格无脑合并了。由于以上的表格全都是DataFrame格式，用pd.merge即可轻松处理。若是要将表格“$/col_a/0/detail1”中的0列和1列合并为这样：

| key  | data |
| ---- | ---- |
| row1 | qy11 |
| row1 | qy12 |
| row2 | qy21 |
| row2 | qy22 |

可以在我的github中找dataframe_manager.py，其中有相应函数可以处理，或者有需要的话，我会在以后的文章中讲解，在此不再赘述。

​	至此，问题圆满解决。

