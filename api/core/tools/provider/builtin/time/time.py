from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController
from core.tools.errors import ToolProviderCredentialValidationError

from core.tools.provider.builtin.time.tools.current_time import CurrentTimeTool

from typing import Any, Dict
import logging

class TimeProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            logging.info("CurrentTimeProvider!!!")
            CurrentTimeTool().fork_tool_runtime(
                meta={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_paramters={},
            )
        except Exception as e:
            logging.info(e)
            raise ToolProviderCredentialValidationError(str(e))