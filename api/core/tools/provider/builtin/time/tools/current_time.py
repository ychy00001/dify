from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

from typing import Any, Dict, List, Union

from datetime import datetime, timezone
import logging
class CurrentTimeTool(BuiltinTool):
    def _invoke(self,
                user_id: str,
                tool_paramters: Dict[str, Any],
        ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        """
            invoke tools
        """
        logging.info("CurrentTime!!!")
        return self.create_text_message(f'{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")}')
    