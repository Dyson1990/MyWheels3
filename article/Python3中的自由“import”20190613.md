# Python3中的自由“import”

​	很久没更新了，一直比较忙。最近做了一个数据清洗框架，遇到了不少没见过的问题，一一解决之后，积累了不少经验，往后有空可以慢慢的分享出来。

## 对自由的渴望

​	我觉得做框架最麻烦的，就是各种情况都要考虑到，能兼容不同业务。

​	我这边遇到的一个问题，就是导入py文件。网上有不少花里胡哨的import方法，可以参考（我只在Python2下试过这些方法）

[import]: https://www.jb51.net/article/141643.htm	"Python实现调用另一个路径下py文件中的函数方法总结_python_脚本之家"

​	但是，我觉得，没有一个是满足我的要求的。我希望能从电脑中任意一个位置导入一个函数或者一个类。出于强迫症，我不想把这些函数的路径放入sys.path里，感觉不够pythonic。而且文件多起来的话，感觉比较难以维护，涉及多个文件的import的更改。

​	以下是我的解决方案：

```python
import pkgutil

def get_obj(dir_path, mod_name, obj_name=None):
    """
    dir_path: str
    mod_name: str
    """
    importer = pkgutil.get_importer(dir_path) # 返回一个FileFinder对象
    loader = importer.find_module(mod_name) # 返回一个SourceFileLoader对象
    mod = loader.load_module() # 返回需要的模块
    if obj_name:
        obj = getattr(mod, obj_name)
        return obj
    else:
        return mod
```

​	Python3中管理“import”的库是importlib，但是我怎么样都无法避免通过修改sys.path来使用importlib（可能还是积累不够吧）。接着，我找到了pkgutil包（属于Python3标准库），从源码看，它也是基于importlib。上面代码中的两个几个对象，也都是在importlib中定义的。

​	接下来我想对pkgutil.get_importer函数做个浅析。

## 初识pkgutil.get_importer

​	首先我们来看看get_importer的源码

```python
def get_importer(path_item):
    """Retrieve a finder for the given path item

    The returned finder is cached in sys.path_importer_cache
    if it was newly created by a path hook.

    The cache (or part of it) can be cleared manually if a
    rescan of sys.path_hooks is necessary.
    """
    try:
        importer = sys.path_importer_cache[path_item]
    except KeyError:
        for path_hook in sys.path_hooks:
            try:
                importer = path_hook(path_item)
                sys.path_importer_cache.setdefault(path_item, importer)
                break
            except ImportError:
                pass
        else:
            importer = None
    return importer
```

​	这里涉及两个关键要素，path_importer_cache与path_hooks

​	这个两个函数，是一对好邻居，可以从官方文档中看出来。

> -  `sys.path_hooks`
>
>   A list of callables that take a path argument to try to create a [finder](https://docs.python.org/3.5/glossary.html#term-finder) for the path. If a finder can be created, it is to be returned by the callable, else raise [`ImportError`](https://docs.python.org/3.5/library/exceptions.html#ImportError). Originally specified in [**PEP 302**](https://www.python.org/dev/peps/pep-0302). 
>
> -  `sys.path_importer_cache`
>
>   A dictionary acting as a cache for [finder](https://docs.python.org/3.5/glossary.html#term-finder) objects. The keys are paths that have been passed to [`sys.path_hooks`](https://docs.python.org/3.5/library/sys.html#sys.path_hooks) and the values are the finders that are found. If a path is a valid file system path but no finder is found on [`sys.path_hooks`](https://docs.python.org/3.5/library/sys.html#sys.path_hooks) then `None` is stored. Originally specified in [**PEP 302**](https://www.python.org/dev/peps/pep-0302).  Changed in version 3.3: `None` is stored instead of [`imp.NullImporter`](https://docs.python.org/3.5/library/imp.html#imp.NullImporter) when no finder is found.  

​	其中提及的finder以及相关的loader都是跟importlib中的FileFinder、SourceLoader对象有关，不是我这篇文章的主要内容，暂且不深入了解。

​	结合代码以及官方文档，大家可以看到，归根结底，还是要看我们所想要的py文件的路径的对象，能否用path_importer_cache获取。不能的话，get_importer函数就会在path_hooks中“搜索”（不知道我理解的对不对）。若还是找不到，则返回None。

​	这么看来，其实get_importer也不是一个很稳定的函数。它需要不断的尝试，以返回符合要求的importer（实际上是importlib中的FileFinder）。因此，我在多进程中并不想使用这个函数。然而由于Python3中pickle的机制原因，并未如愿以偿。这是因为在Python3中无法序列化某个函数，强行序列化之后，得到的结果只有一个函数名称，进而在反序列化的时候报错。我目前还没有深入研究过Python3中的finder和loader，以后有精力再试试深入学习一下源代码，说不定finder是可以序列化的呢？

## Python3中的pickle

之前我们有提及强行序列化Python函数，会导致反序列化的时候会报错，我们可以做如下试验：

```python
In [1]: import sql_reader
In [2]: import pickle
In [3]: import codecs
In [4]: with codecs.open('./test', 'wb') as f:
   ...:     pickle.dump(sql_reader.sql_reader.connect, f) # 这里sql_reader是我自己Python代码包
```

得到的test文件中的内容是：

```
cbuiltins
getattr
q csql_reader
sql_reader
qX   connectqǱRq.
```

关闭目前的Python解释器，换个目录重新打开Python解释器后，我们可以发现：

```Python
In [1]: import codecs
In [2]: import pickle
In [3]: with codecs.open('./qy_opt/test', 'rb') as f:
   ...:     func = pickle.load(f)
   ...:
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
<ipython-input-5-7300734cdec3> in <module>
      1 with codecs.open('./qy_opt/test', 'rb') as f:
----> 2     func = pickle.load(f)
      3

ModuleNotFoundError: No module named 'sql_reader'
```

已经没有办法反序列化这个connect函数了。

## 浅尝自由

​	回到我的代码中，我这个代码其实很简单。三个参数：

1. dir_path是py文件夹的路径
2. mod_name是py文件名，不包括扩展名
3. obj_name是可选参数，不填则函数返回module对象，否则obj_name是类名就返回类的对象，是函数名就返回函数对象（函数和类同名？请规范一下你的编码习惯）

我的这个get_obj函数使用效果如下：

```python
In [1]: obj = get_obj('./', 'html_table_reader') 

In [2]: type(obj)                                                                         
Out[2]: module

In [3]: ', '.join(dir(obj))
Out[3]: '__builtins__, __cached__, __doc__, __file__, __loader__, __name__, __package__, __spec__, bs4, data_standardize, np, pd, standardize, sys, table_tr_td, title_standardize'

In [4]: obj = get_obj('./', 'html_table_reader', 'table_tr_td')                          

In [5]: type(obj)
Out[5]: function

In [6]: ', '.join(dir(obj))     
Out[6]: '__annotations__, __call__, __class__, __closure__, __code__, __defaults__, __delattr__, __dict__, __dir__, __doc__, __eq__, __format__, __ge__, __get__, __getattribute__, __globals__, __gt__, __hash__, __init__, __init_subclass__, __kwdefaults__, __le__, __lt__, __module__, __name__, __ne__, __new__, __qualname__, __reduce__, __reduce_ex__, __repr__, __setattr__, __sizeof__, __str__, __subclasshook__'

```

​	这里的obj，已经可以当成正式的module对象或function对象来用了。所引用的py文件根本不需要放在项目文件夹下即可调用，

​	虽然适用范围不是很广，但是对于一些像我这样，偶尔喜欢自己造点轮子的人来说，或者是要编写框架，暂时不知道要用到哪些自定义函数的人来说，应该是有一定的利用价值的。