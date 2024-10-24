# coding=utf-8
'''
流程构造器模块

该模块用于构造和管理 HTTP 请求及其匹配规则。提供了请求构造器和规则构造器方法，方便用户设置请求参数、定义匹配逻辑以及获取最终构造的请求和规则的输出。

主要功能包括：
1. **请求构造器**：用于设置请求的主机地址、方法、路径、头部、体、查询参数和 cookies。
2. **规则构造器**：用于定义匹配规则，包括匹配模式、范围、逻辑和匹配器列表。
3. **输出流程构造器**：返回当前流程构造器的所有请求参数和规则，便于调试和查看，也可以被他人导入请求构造器。
4. **导入流程构造器**：通过他人分享的流程构造器构建一个流程构造器

使用示例：
```
constructor = ProcessConstructor()
constructor.request_constructor('http://example.com', 'GET')
constructor.rule_constructor('code', [200, 201])
'''
import json


class ProcessConstructor:
    '''
    流程构造器模块

    该模块用于构造和管理 HTTP 请求及其匹配规则。提供了请求构造器和规则构造器方法，方便用户设置请求参数、定义匹配逻辑以及获取最终构造的请求和规则的输出。

    主要功能包括：
    1. **请求构造器**：用于设置请求的主机地址、方法、路径、头部、体、查询参数和 cookies。
    2. **规则构造器**：用于定义匹配规则，包括匹配模式、范围、逻辑和匹配器列表。
    3. **输出流程构造器**：返回当前流程构造器的所有请求参数和规则，便于调试和查看，也可以被他人导入请求构造器。
    4. **导入流程构造器**：通过他人分享的流程构造器构建一个流程构造器

    使用示例：
    ```
    constructor = ProcessConstructor()
    constructor.request_constructor('http://example.com', 'GET')
    constructor.rule_constructor('code', [200, 201])
    '''
    def __init__(self,title :str="vdog Process Constructor"):
        self.title = title
        self.version = "0.0.1"
        self.request_params = {}
        self.rules = []
    def request_constructor(self,method: str,path: str="/",timeout: int=10,headers: dict={},body=None,params: dict=None,cookies: dict=None,output: str=None):
        '''请求构造器：用于构造一个请求器

        :param method: 请求方法（必要，如 'GET', 'POST' 等）。
        :param path: 请求路径（可选，未指定默认为/）。
        :param timeout：超时时间（可选，未指定默认未10秒）
        :param headers: 请求头（可选，字典格式）。
        :param body: 请求体（可选，任意内容）。
        :param params: URL 查询参数（可选，字典格式）。
        :param cookies: 请求的 cookies（可选，字典格式）。
        :param output: 指定输出的内容（可选，字符串格式。输出内容，未指定默认为None。可选参数：code/header/body/request,如果扫描过程中出错则为错误原因）

        :return: 返回当前的 ProcessConstructor 实例，方便链式调用。
        '''
        self.request_params = {
            "method": method,
            "path": path,
            "timeout": timeout,
            "headers": headers,
            "body": body,
            "params": params,
            "cookies": cookies,
            "output": output
        }
        return self

    def rule_constructor(self, pattern: str, matchers: list, range: str="all", logic: str="all"):
        '''规则构造器：用于构造匹配规则

        :param pattern: 匹配模式：code/keyword/custom
        :param range: 匹配范围：code/body/header/all
        :param logic: 匹配逻辑:all/any,all代表匹配matchers列表的所有参数为真才为真，any代表匹配器matchers列表任意参数为真即为真
        :param matchers: 匹配器列表，定义如何对目标进行匹配的逻辑或算法。

        custom：自定义语法，语法可参考文档[https://docs.python.org/3/library/re.html#re.finditer]

        :return: 返回当前的 ProcessConstructor 实例，方便链式调用。
        '''
        rule = {
            "pattern": pattern,
            "range": range,
            "logic": logic,
            "matchers": matchers
        }
        self.rules.append(rule)
        return self

    def output(self):
        '''输出当前构造器的结构，可分享给他人供其使用'''
        data={
            "request": self.request_params,
            "rules": self.rules
        }
        return json.dumps({
            "title": self.title,
            "woodpecker_version": self.version,
            "process_constructor": data
        })

    def import_module(self, json_data: str):
        '''根据构造器 JSON 导入构造一个 ProcessConstructor

        :param json_data: JSON 字符串，包含构造器的参数。

        :return: 返回当前的 ProcessConstructor 实例，方便链式调用。
        '''
        data = json.loads(json_data)
        self.title = data.get("title", self.title)
        self.version = data.get("woodpecker_version", self.version)
        process_data = data.get("process_constructor", {})

        self.request_params = process_data.get("request", {})
        self.rules = process_data.get("rules", [])
        return self