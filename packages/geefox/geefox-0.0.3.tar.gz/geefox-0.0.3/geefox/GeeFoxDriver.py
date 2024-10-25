import concurrent.futures
import json
import http.client
import ssl
import socket
import time
from urllib.parse import urlparse

from tabulate import tabulate

from geefox import ProcessConstructor


class GeeFoxDriver:
    """
    GeeFox驱动器：
    初始化时需要传入ProcessConstructor
    """
    def __init__(self,process_examples :ProcessConstructor):
        self.process_examples = None
        if process_examples.request_params and process_examples.rules:
            self.process_examples = process_examples
            print(f"Instance {process_examples.title} loaded successful!")
        else:
            print(f"Instance {process_examples.title} not loaded! Because some parameters are missing")

    import concurrent.futures
    import json
    import http.client
    import ssl
    import socket
    import time
    from urllib.parse import urlparse
    from tabulate import tabulate  # 用于表格输出

    def scan(self, urls: list[str], use_multithreading=True, max_threads=10, output=True):
        '''
        使用实例针对指定的Url列表发起扫描，并可选择是否使用多线程处理，以及是否输出结果为表格

        :param urls: url 列表，例如 ["http://test.org"] 或 ["url1", "url2", "url3"]
        :param use_multithreading: 是否启用多线程处理，默认为 True
        :param max_threads: 线程数量，仅在使用多线程时有效，默认为 10
        :param output: 是否将结果以表格形式输出到控制台，默认为 True

        :return: 返回扫描结果，格式为 {url: {status: True/False, "error": false/true, "output": ""}}
        '''
        results = {}  # 用于保存扫描结果
        table_data = []  # 用于保存表格数据
        logo=r"""
   _____           ______        
  / ____|         |  ____|       
 | |  __  ___  ___| |__ _____  __
 | | |_ |/ _ \/ _ \  __/ _ \ \/ /
 | |__| |  __/  __/ | | (_) >  < 
  \_____|\___|\___|_|  \___/_/\_\    
            GeeFoxDriver Ver:0.0.3                                               
                https://geefox.org                                       
"""
        print(logo)
        def scan_url(url):
            result = {
                "status": True,
                "error": False,
                "response_time": None,
                "response_size": None,
                "output": None
            }
            try:
                parsed_url = urlparse(url)
                sslcontext = ssl._create_unverified_context()
                sslcontext.set_ciphers('DEFAULT:@SECLEVEL=0')
                if parsed_url.scheme == 'https':
                    conn = http.client.HTTPSConnection(parsed_url.netloc,
                                                       timeout=self.process_examples.request_params["timeout"],
                                                       context=sslcontext)
                elif parsed_url.scheme == 'http':
                    conn = http.client.HTTPConnection(parsed_url.netloc,
                                                      timeout=self.process_examples.request_params["timeout"])
                else:
                    result["status"] = False
                    result["error"] = True
                    result["output"] = f"Unsupported URL scheme: {parsed_url.scheme}"
                    return {url: result}

                start_time = time.time()
                conn.request(method=self.process_examples.request_params['method'],
                             url=self.process_examples.request_params['path'],
                             headers=self.process_examples.request_params['headers'],
                             body=self.process_examples.request_params['body'],
                             )
                response = conn.getresponse()
                response_time = int((time.time() - start_time) * 1000)
                response_status = response.status
                response_headers = response.getheaders()
                try:
                    response_body = response.read().decode('utf-8')
                except UnicodeDecodeError:
                    response_body = response.read()
                response_size = len(response_body)

            except http.client.HTTPException as e:
                result["status"] = False
                result["error"] = True
                result["output"] = str(e)
                return {url: result}

            except socket.timeout:
                result["status"] = False
                result["error"] = True
                result["output"] = "Request timed out."
                return {url: result}

            except Exception as e:
                result["status"] = False
                result["error"] = True
                result["output"] = str(e)
                return {url: result}

            finally:
                conn.close()

            result["response_time"] = f"{response_time}ms"
            result["response_size"] = f"{response_size}bytes"

            # 规则匹配
            for rule in self.process_examples.rules:
                if rule['pattern'] == 'code':
                    if response_status not in rule['matchers']:
                        result["status"] = False
                elif rule['pattern'] == 'keyword':
                    p = result["status"]
                    if rule['logic'] == 'all':
                        if rule['range'] == 'all':
                            p = all(
                                item in str(response_body) or item in str(response_headers) or item in str(response_status)
                                for item in rule['matchers'])
                        elif rule['range'] == 'body':
                            p = all(item in str(response_body) for item in rule['matchers'])
                        elif rule['range'] == 'header':
                            p = all(item in str(response_headers) for item in rule['matchers'])
                        elif rule['range'] == 'code':
                            p = all(item in str(response_status) for item in rule['matchers'])
                    elif rule['logic'] == 'any':
                        if rule['range'] == 'all':
                            p = any(
                                item in str(response_body) or item in str(response_headers) or item in str(response_status)
                                for item in rule['matchers'])
                        elif rule['range'] == 'body':
                            p = any(item in str(response_body) for item in rule['matchers'])
                        elif rule['range'] == 'header':
                            p = any(item in str(response_headers) for item in rule['matchers'])
                        elif rule['range'] == 'code':
                            p = any(item in str(response_status) for item in rule['matchers'])
                    result["status"] = p
                elif rule['pattern'] == 'custom':
                    for r in rule['matchers']:
                        result["status"] = eval(r)

            if self.process_examples.request_params['output'] == "code":
                result["output"] = str(response_status)
            elif self.process_examples.request_params['output'] == "headers":
                result["output"] = str(response_headers)
            elif self.process_examples.request_params['output'] == "body":
                result["output"] = str(response_body)
            elif self.process_examples.request_params['output'] == "request":
                result["output"] = (
                    f"{self.process_examples.request_params['method']} {self.process_examples.request_params['path']}\n"
                    f"Host:{parsed_url.netloc}\n"
                    f"{self.process_examples.request_params['headers']}")

            return {url: result}

        # 多线程执行
        if use_multithreading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = {executor.submit(scan_url, url): url for url in urls}
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    results.update(result)
        else:
            for url in urls:
                result = scan_url(url)
                results.update(result)

        # 将结果转换为表格数据
        if output:
            for url, result in results.items():
                max_size=10000
                output_text = result.get("output", "N/A")
                if output_text==None: output_text = ""
                if len(output_text) > max_size:
                    output_text = output_text[:max_size - 3] + "..."
                table_data.append([
                    url,
                    result["status"],
                    result.get("error", "N/A"),
                    result.get("response_time", "N/A"),
                    result.get("response_size", "N/A"),
                    output_text
                ])
            # 输出表格
            headers = ["URL", "Status","ERROR","Response Time", "Response Size", "Output"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

        # 返回结果以 JSON 形式
        return json.dumps(results, ensure_ascii=False)




