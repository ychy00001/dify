from typing import Any, Dict, List

from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController
from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.baidu.tools.baidu_search import BaiduSearchTool


class BaiduProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            BaiduSearchTool().fork_tool_runtime(
                meta={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_parameters={
                    "query": "test",
                    "result_type": "text"
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
