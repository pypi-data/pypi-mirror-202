# simple_export

simple_export是一款导出工具包，目标是根据模板快速导出
[simple_export](https://github.com/mtl940610/simple_export/)

# python包上传到pypi过程

> 提示：文章写完后，目录可以自动生成，如何生成可参考右边的帮助文档

@[TOC](文章目录)

---

# 前言

有的时候会写一些python的工具包，上传到pypi会很方便下载使用，本篇文章将介绍打包上传过程

> [pypi官网](https://pypi.org/) [https://pypi.org/](https://pypi.org/)
> 
> [pypi打包上传文档](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
> 
> [testpypi官网 (pypi.org)](https://test.pypi.org/)
> 
> [simple-export · PyPI](https://pypi.org/project/simple-export/)
> 
> [GitHub - mtl940610/simple_export](https://github.com/mtl940610/simple_export)

# 一、pypi是什么？

Python 包索引 （PyPI） 是 Python 编程语言的软件存储库。

# 二、使用步骤

## 1.创建目录结构

> packaging_tutorial 根目录
> 
> LICENSE 参阅[https://choosealicense.com/](https://choosealicense.com/)选择许可证
> 
> pyproject.toml 配置文件
> 
> dist 打包后的目录
> 
> src/simple_export 项目文件，可替换成你自己的
> 
> tests 测试文件夹，可为空

```
└─packaging_tutorial
    │  LICENSE
    │  pyproject.toml
    │  README.md
    │
    ├─dist
    │      simple_export-0.1.9-py3-none-any.whl
    │      simple_export-0.1.9.tar.gz
    │
    ├─src
    │  └─simple_export
    │      │  example.py
    │      │  excel.py
    │      │  val1.xlsx
    │      │  __init__.py
    │      │
    │      ├─template
    │      │      excel1.xlsx
    │      │      excel2.xlsx
    │      │
    │      └─utils
    │          │  tool.py
    │          │  __init__.py
    │          │
    │          └─__pycache__
    │                  tool.cpython-38.pyc
    │                  __init__.cpython-38.pyc
    │
    └─tests
            example.py
            val1.xlsx
            __init__.py
```

## 2. 创建 pyproject.toml

| 名称  | 备注  |
| --- | --- |
| name | 包的分发名称。这可以是任何名称，只要它只包含字母、数字、.、_和-。它也不能已经在 PyPI 上使用。请务必使用您在本教程中的用户名更新此名称，因为这可确保您不会尝试上传与已存在名称相同的包。 |
| version | 包的版本号。有关版本的更多详细信息，请参阅版本说明符规范 。一些构建后端允许以其他方式指定它，例如从文件或 git 标签。 |
| authors | 用于识别包的作者；您为每位作者指定姓名和电子邮件。您也可以maintainers以相同的格式列出 |
| description | 简短单句摘要 |
| readme | readme文件的路径 |
| requires-python | 给出项目支持的 Python 版本。像pip这样的安装程序会回顾旧版本的包，直到找到一个具有匹配 Python 版本的包。 |
| classifiers | 为 index 和pip提供一些关于您的包的额外元数据。在这种情况下，该包仅与 Python 3 兼容，根据 MIT 许可获得许可，并且独立于操作系统。您应该始终至少包括您的包适用于哪些 Python 版本、您的包在哪个许可下可用以及您的包将在哪些操作系统上运行。有关分类器的完整列表，请参阅 https://pypi.org/classifiers/。 |
| urls | 允许您列出任意数量的额外链接以显示在 PyPI 上。通常这可能是源代码、文档、问题跟踪器等。 |

我的toml（示例）：

```c
[tool.poetry]
name = "simple-export"
version = "0.1.9"
description = "简单的模板导出工具"
authors = ["mtl <576694002@qq.com>"]
license = "Apache"
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.7"
openpyxl = "^3.0.10"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.urls]
"Homepage" = "https://github.com/mtl940610/simple_export"
"Bug Tracker" = "https://github.com/mtl940610/simple_export/issues"
```

## 3. 创建README.md

markdown格式随意编写，介绍项目

## 4. 创建许可证

LICENSE 参阅[https://choosealicense.com/](https://choosealicense.com/)选择许可证

## 5. 打包

![](file://C:\Users\e9\AppData\Roaming\marktext\images\2023-02-07-11-28-32-image.png?msec=1676359881325)

```
# 如果有虚拟环境需要进入虚拟环境 直接python 执行
python3 -m pip install --upgrade build
# pyproject.toml位于的同一目录运行此命令 此命令执行完后 dist目录下会生成两个文件 whl 、 tar.gz
python3 -m build
# 通过twine上传包
python3 -m pip install --upgrade twine
```

## 6. 注册pypi账号和testpypi账号

[pypi官网](https://pypi.org/) [https://pypi.org/

[testpypi官网 (pypi.org)](https://test.pypi.org/)

## 7. 上传到testpypi

一般可以先上传到testpypi，测试通过后在上传pypi，当然也可以直接上传到pypi

```
# testpypi 改为 pypi就是上传到pypi dist/* 是上传dist下所有文件
python3 -m twine upload --repository testpypi dist/*
```

## 8. 安装

```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps simple-export
```

---

# 总结

### 1.安装

如果换源了，有可能得等一段时间才能同步到其他源

可以先指定官方源

[test-pypi](https://test.pypi.org/simple/

pypi [[Simple index](https://pypi.org/simple)](https://pypi.org/simple)