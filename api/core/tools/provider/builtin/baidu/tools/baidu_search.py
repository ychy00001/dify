from core.tools.tool.builtin_tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.provider.builtin.baidu.tools.baidu_engine import bing_search

from typing import Any, Dict, List, Union

import os
import sys
import json
import logging
import subprocess


class HiddenPrints:
    """Context manager to hide prints."""

    def __enter__(self) -> None:
        """Open file to pipe stdout to."""
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, *_: Any) -> None:
        """Close file that stdout was piped to."""
        sys.stdout.close()
        sys.stdout = self._original_stdout


class BaiduAPI:
    """
    BaiduAPI tool provider.
    """
    search_engine: Any  #: :meta private:
    search_result: int = 3

    def __init__(self) -> None:
        """Initialize BaiduAPI tool provider."""
        self.search_engine = None
        self.search_result = 3

    def run(self, query: str, **kwargs: Any) -> str:
        """Run query through SerpAPI and parse result."""
        typ = kwargs.get("result_type", "text")
        return self._process_response(self.results(query), typ=typ)

    def execute_command_and_get_json(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                json_result = result.stdout.strip()
                try:
                    data = json.loads(json_result)
                    return data
                except json.JSONDecodeError as e:
                    logging.info(f"Error decoding JSON: {e}")
                    return None
            else:
                logging.info(f"Error executing command: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def results(self, query: str) -> dict:
        """Run query through SerpAPI and return the raw result."""
        # 命令行发起请求执行python文件
        # python /app/api/core/tools/provider/builtin/baidu/tools/baidu_engine.py
        res = self.execute_command_and_get_json("python /app/api/core/tools/provider/builtin/baidu/tools/baidu_engine.py {} {}".format(query,3))
#         res = bing_search(query, num_results=3)
        logging.info("Search result: %s", json.dumps(res,ensure_ascii=False))
        return res

    @staticmethod
    def _process_response(res: list, typ: str) -> str:
        # res 结构 [{"title": title, "description": description, "url": url},...]
        """Process response from SerpAPI."""
        toret = ""
        if typ == "text":
            for item in res:
                logging.info("title: {}\n description: {}\n url: {} \n".format(item["title"], item["description"], item["url"]))
                toret += "[{}]\n   {}\n".format(item["title"], item["description"])
        elif typ == "link":
            for item in res:
                logging.info("title: {}\ndescription: {}\n url: {} \n".format(item["title"], item["description"], item["url"]))
                toret += f"[{item['title']}]({item['url']})\n"
        logging.info("Search Toret: %s", toret)
        return toret

class BaiduSearchTool(BuiltinTool):
    def _invoke(self, 
                user_id: str,
               tool_paramters: Dict[str, Any], 
        ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            invoke tools
        """
        query = tool_paramters['query']
        result_type = tool_paramters['result_type']

        result = BaiduAPI().run(query, result_type=result_type)
        if result_type == 'text':
            return self.create_text_message(text=result)
        return self.create_link_message(link=result)


