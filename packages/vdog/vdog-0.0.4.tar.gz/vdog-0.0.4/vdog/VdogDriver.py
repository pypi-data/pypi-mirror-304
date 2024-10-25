import http.client
import json
import ssl
import socket
from urllib.parse import urlparse
from vdog import ProcessConstructor


class VdogDriver:
    def __init__(self,process_examples :ProcessConstructor):
        self.process_examples = None
        if process_examples.request_params and process_examples.rules:
            self.process_examples = process_examples
            print(f"Instance {process_examples.title} loaded successful!")
        else:
            print(f"Instance {process_examples.title} not loaded! Because some parameters are missing")


    def scan(self, urls: list[str]):
        '''
        使用实例针对指定的Url列表发起扫描

        :param urls: url 列表，例如 ["http://test.org"] 或 ["url1", "url2", "url3"]

        :return: 返回扫描结果，格式为 {url: {status: True/False, "error": false/true, "output": ""}}
        '''
        results = {}  # 用于保存扫描结果

        for url in urls:
            result = {
                "status": True,
                "error": False,
                "output": None
            }

            try:
                parsed_url = urlparse(url)
                sslcontext = ssl._create_unverified_context()
                sslcontext.set_ciphers('DEFAULT:@SECLEVEL=0')
                if parsed_url.scheme == 'https':
                    conn = http.client.HTTPSConnection(parsed_url.netloc,
                                                       timeout=self.process_examples.request_params["timeout"],context=sslcontext)
                elif parsed_url.scheme == 'http':
                    conn = http.client.HTTPConnection(parsed_url.netloc,
                                                      timeout=self.process_examples.request_params["timeout"])
                else:
                    result["status"] = False
                    result["error"] = True
                    result["output"] = f"Unsupported URL scheme: {parsed_url.scheme}"
                    results[url] = result
                    print(result)
                    continue
                conn.request(method=self.process_examples.request_params['method'],
                             url=self.process_examples.request_params['path'],
                             headers=self.process_examples.request_params['headers'],
                             body=self.process_examples.request_params['body'],
                             )
                response = conn.getresponse()
                response_state = response.status
                response_headers = response.getheaders()
                response_body = response.read().decode()

            except http.client.HTTPException as e:
                result["status"] = False
                result["error"] = True
                result["output"] = str(e)
                results[url] = result
                print(result)
                continue
            except socket.timeout:
                result["status"] = False
                result["error"] = True
                result["output"] = "Request timed out."
                results[url] = result
                print(result)
                continue
            except Exception as e:
                result["status"] = False
                result["error"] = True
                result["output"] = str(e)
                results[url] = result
                print(result)
                continue
            finally:
                conn.close()

            # 规则匹配
            for rule in self.process_examples.rules:
                if rule['pattern'] == 'code':
                    if response_state not in rule['matchers']:
                        result["status"] = False
                elif rule['pattern'] == 'keyword':
                    p = result["status"]
                    if rule['logic'] == 'all':
                        if rule['range'] == 'all':
                            p = all(
                                item in response_body or item in str(response_headers) or item in str(response_state)
                                for item in rule['matchers'])
                        elif rule['range'] == 'body':
                            p = all(item in response_body for item in rule['matchers'])
                        elif rule['range'] == 'header':
                            p = all(item in str(response_headers) for item in rule['matchers'])
                        elif rule['range'] == 'code':
                            p = all(item in str(response_state) for item in rule['matchers'])
                    elif rule['logic'] == 'any':
                        if rule['range'] == 'all':
                            p = any(
                                item in response_body or item in str(response_headers) or item in str(response_state)
                                for item in rule['matchers'])
                        elif rule['range'] == 'body':
                            p = any(item in response_body for item in rule['matchers'])
                        elif rule['range'] == 'header':
                            p = any(item in str(response_headers) for item in rule['matchers'])
                        elif rule['range'] == 'code':
                            p = any(item in str(response_state) for item in rule['matchers'])
                    result["status"] = p
                elif rule['pattern'] == 'custom':
                    print("该方法暂不可用")

            if self.process_examples.request_params['output'] == "code":
                result["output"] = str(response_state)
            elif self.process_examples.request_params['output'] == "headers":
                result["output"] = str(response_headers)
            elif self.process_examples.request_params['output'] == "body":
                result["output"] = str(response_body)
            elif self.process_examples.request_params['output'] == "request":
                result["output"] = (f"{self.process_examples.request_params['method']} {self.process_examples.request_params['path']}\n"
                                    f"Host:{parsed_url.netloc}\n"
                                    f"{self.process_examples.request_params['headers']}")
            # 保存结果
            results[url] = result
            print(result)

        # 返回结果以 JSON 形式
        return json.dumps(results, ensure_ascii=False)



