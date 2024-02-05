from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController
from core.tools.errors import ToolProviderCredentialValidationError

from core.tools.provider.builtin.cw.tools.cw_text2img import CwText2ImageTool

from typing import Any, Dict, List

class CwProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            CwText2ImageTool().fork_tool_runtime(
                meta={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_parameters={
                    "keyword": "cat",
                    "batch_size": 1,
                    "img_style": "muou_realistic",
                    "size": "square"
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))