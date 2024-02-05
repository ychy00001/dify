from core.tools.tool.builtin_tool import BuiltinTool
from core.tools.entities.tool_entities import ToolInvokeMessage
from base64 import b64decode
from httpx import post
from typing import Any, Dict, List, Union
import os
import logging


class CwText2ImageTool(BuiltinTool):
    def _invoke(self,
                user_id: str,
               tool_paramters: Dict[str, Any],
        ) -> Union[ToolInvokeMessage, List[ToolInvokeMessage]]:
        logging.info("cw request parameters: %s", tool_paramters)

        STYLE_LIST_MAP = {
                "muou_realistic": "muou_realistic",
                "muou_illustration": "muou_illustration",
                "动漫(Anime)": "动漫(Anime)",
                "连环漫画(Comic Book)": "连环漫画(Comic Book)",
                "剪纸艺术(Kirigami)": "剪纸艺术(Kirigami)",
                "黑白照片(Monochrome)": "黑白照片(Monochrome)"
            }
        STYLE_LIST = ["muou_realistic", "muou_illustration",
                         "动漫(Anime)", "连环漫画(Comic Book)", "剪纸艺术(Kirigami)", "黑白照片(Monochrome)"]
        SIZE_LIST = ["square", "vertical", "horizontal"]

        """
            invoke tools
        """
        keyword = tool_paramters['keyword']
        batch_size = 1
        map_img_style = "动漫(Anime)"
        size = "square"
        if "batch_size" in tool_paramters:
            batch_size = tool_paramters['batch_size'] if tool_paramters['batch_size'] > 1 else 1
        if "img_style" in tool_paramters:
            map_img_style = tool_paramters['img_style'] if tool_paramters['img_style'] in STYLE_LIST else STYLE_LIST[0]
            img_style = STYLE_LIST_MAP[map_img_style]
        if "size" in tool_paramters:
            size = tool_paramters['size'] if tool_paramters['size'] in SIZE_LIST else SIZE_LIST[0]
        img_with = 1024
        img_height = 1024

        if(size == "vertical"):
            img_with = 1024
            img_height = 1024
        elif (size == "horizontal"):
            img_with = 1792
            img_height = 1024

        ## 构建prompt
        content = "# Role:\n你是AI绘画工具Stable Diffusion的提示词高手。\n\n## Background:\n你擅长从用户输入的关键词或一句话内容中，丰富的生成一段图片描述，我会把你的创意直接使用AI绘画工具如stable diffusion进行AI绘画创作。\n\n## Goals:\n1. 根据Background、Skills、Subject、Input、Constrains、Workflows等描述。请自由发挥你的想象力，不仅限上述信息，可以根据你的理解，设计一个充满创意的画面感很强的图片描述\n\n## Constrains:\n1. 图片中不要有任何口号、标语、店名和文字\n2. 图片描述的内容中必须基于用户的Input，另外需要增加详细的设计元素，例如背景、颜色、主要物体、布局、场景等；\n3. 输出内容必须要包含Input中的内容\n4. 输出的图片描述内容要简短，不超过30个tokens\n5. 输出的描述可以是单词或短句，中间用逗号隔开\n6. 不要生成关于情感、味觉、声音听觉相关描述、不要有职业、色情等涉及隐私的描述\n7. 只需要生成与视觉相关的描述\n8. 必须用英文回答\n\n## Skills:\n你具备以下能力：\n1. 根据指定的行业主题Subject，生成的图片描述需要包含画面主体、画面场景、构图方式、画面背景等描述。\n2. 画面背景描述：设定周围的场景和辅助元素，比如天空的颜色、周围的物品、环境灯光、画面色调等视觉相关的描述，这一步是为了渲染画面氛围，凸显图片的主题。\n3. 构图方式描述：主要用来调节画面的镜头和视角，比如强调景深，物体位置、黄金分割构图、中全景、景深等\n4. 图片描述的画面要整体和谐，不能与给定的主题冲突\n\n## Workflows:\n* Input：输入相关的关键字或短语内容\n* Output：根据Input输入内容输出简短的图片描述，可以用关键字、短句来描述，不要超过30个tokens\n\n## Examples:\n* Subject:餐饮\n* Input: 早餐、杯子、牛奶和冰块，不要有人物描述\n* Output:A cozy breakfast scene,transparent plastic cup full of brown milk tea with ice cubes, placed on a wooden table with a bright yellow background,no humans.\n以上Examples仅做参考，不要重复输出相同内容\n\n## Subject:\n餐饮美食\n\n## Input:\n{0}\n## Output:\n".format(keyword)
        prompt_data = {
           "allowTruncation": False,
           "messages": [
               {
                   "role": "system",
                   "content": "string"
               },
               {
                   "role": "user",
                   "content": content
               }
           ],
           "parameters": {
               "do_sample": True,
               "max_new_tokens": 900,
               "repetition_penalty": 1.03,
               "stop": [
                   "</s>",
                   "User"
               ],
               "temperature": 0.7,
               "top_k": 30,
               "top_p": 0.95
           },
           "assistantPrefix": "",
           "userPrefix": ""
       }
        prompt_response = post(
                            'http://10.178.13.111:15501/chat',
                            json=prompt_data,
                            timeout=20
                )
        if prompt_response.status_code != 200:
            raise Exception(prompt_response.text)
        prompt_json = prompt_response.json()

        ## 生成图片
        f = open(os.path.split(os.path.realpath(__file__))[0]+"/template_img.txt")
        template_base_image = f.read()
        post_data = {
          "prompt": prompt_json["generated_text"],
          "negative_prompt": "",
          "override_settings": {
            "sd_model_checkpoint": "dreamshaperXL10_alpha2Xl10.safetensors [0f1b80cfe8]"
          },
          "seed": -1,
          "subseed": -1,
          "tiling": False,
          "sampler_index": "DPM++ 2M Karras",
          "batch_size": batch_size,
          "n_iter": 1,
          "steps": 20,
          "cfg_scale": 7,
          "width": img_with,
          "height": img_height,
          "save_images": False,
          "do_not_save_samples": True,
          "alwayson_scripts": {
            "style selector for sdxl 1.0": {
              "args": [
                True,
                False,
                False,
                False,
                img_style
              ]
            }
          }
        }
        img_response = post(
                    'http://10.178.13.79:7555/sdapi/v1/txt2img',
                    json=post_data,
                    timeout=50
        )
        if img_response.status_code != 200:
            raise Exception(img_response.text)

        result = []
        for image_b64 in img_response.json()["images"]:
            result.append(self.create_blob_message(blob=b64decode(image_b64),
                                                   meta={ 'mime_type': 'image/png' },
                                                   save_as=self.VARIABLE_KEY.IMAGE.value))
        return result