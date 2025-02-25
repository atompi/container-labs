"""
title: Flux image generation filter
author: atompi
author_url: https://github.com/atompi
funding_url: https://github.com/atompi
version: 0.1
"""

import random
import re
from typing import Any, Awaitable, Callable, Optional

import aiohttp
from pydantic import BaseModel, Field


class AIOutput(BaseModel):
    success: bool
    prompt: str
    width: int
    height: int
    reason: Optional[str] = None
    seed: int = Field(default=-1)


class Filter:
    # 使用您提供的正则表达式，转换为 Python 格式
    JSON_REGEX = re.compile(r"\{(?:\\.|[^\\}])*}")

    class Valves(BaseModel):
        priority: int = Field(default=10, description="用于过滤操作的优先级别。")
        Siliconflow_Base_URL: str = Field(
            default="https://api.siliconflow.cn",
            description="Siliconflow API的基础URL。（例如：https://api.siliconflow.cn）",
        )
        Siliconflow_API_KEY: str = Field(
            default="",
            description="Siliconflow API的API密钥。",
        )
        max_retries: int = Field(
            default=3,
            description="HTTP请求的最大重试次数。",
        )
        num_inference_steps: int = Field(
            default=20,
            description="执行的推理步骤数。（1-100）",
        )
        model_name: str = Field(
            default="black-forest-labs/FLUX.1-schnell",
            description="用于生成图像的模型名称。",
        )

    def __init__(self):
        self.valves = self.Valves()

    @staticmethod
    def remove_markdown_images(content: str) -> str:
        # 根据需要调整，确保保留JSON格式
        return re.sub(r"!\[.*?\]\([^)]*\)", "", content)

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        await __event_emitter__(
            {
                "type": "status",
                "data": {
                    "description": "✨正在飞速生成提示词中，请耐心等待...",
                    "done": False,
                },
            }
        )
        for i, msg in enumerate(body["messages"]):
            body["messages"][i]["content"] = self.remove_markdown_images(msg["content"])
        return body

    async def text_to_image(self, prompt: str, image_size: str, seed: int, __user__: Optional[dict] = None):
        url = f"{self.valves.Siliconflow_Base_URL}/v1/images/generations"
        payload = {
            "model": self.valves.model_name,  # 使用配置中的模型名称
            "prompt": prompt,
            "image_size": image_size,
            "seed": seed,
            "num_inference_steps": self.valves.num_inference_steps,  # 保持推理步数
        }

        headers = {
            "authorization": f"Bearer {random.choice([key for key in self.valves.Siliconflow_API_KEY.split(',') if key])}",
            "accept": "application/json",
            "content-type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            for attempt in range(self.valves.max_retries):
                try:
                    async with session.post(url, json=payload, headers=headers) as response:
                        response.raise_for_status()
                        response_data = await response.json()
                        return response_data
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == self.valves.max_retries - 1:
                        return {"error": str(e)}

    async def generate_single_image(self, ai_output: AIOutput, __user__: Optional[dict] = None):
        image_size = f"{ai_output.width}x{ai_output.height}"
        if ai_output.seed == -1:
            ai_output.seed = random.randint(0, 9999999999)
        seed = ai_output.seed

        result = await self.text_to_image(ai_output.prompt, image_size, seed, __user__)

        if isinstance(result, dict) and "error" in result:
            error_message = result["error"]
            raise Exception(f"Siliconflow API Error: {error_message}")

        return result

    async def outlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        if "messages" in body and body["messages"] and __user__ and "id" in __user__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "🚀正在火速生成图片中，请耐心等待...",
                        "done": False,
                    },
                }
            )

            messages = body["messages"]
            if messages:
                ai_output_content = messages[-1].get("content", "")
                match = self.JSON_REGEX.search(ai_output_content)
                if not match:
                    raise ValueError("未在消息内容中找到有效的AI输出JSON。")

                ai_output_json_str = match.group()

                try:
                    ai_output = AIOutput.parse_raw(ai_output_json_str)
                except Exception as e:
                    raise ValueError(f"解析AI输出JSON时出错: {e}")

                if ai_output.success:
                    response_data = await self.generate_single_image(ai_output, __user__)
                    if response_data and "images" in response_data:
                        images = response_data.get("images", [])
                        if images:
                            image_url = images[0].get("url", "")

                            # 更新content_lines并重新写入
                            content_lines = [
                                "### 生成信息",
                                f"**提示词 (Prompt):** {ai_output.prompt}",
                                f"**尺寸 (Size):** {ai_output.width}x{ai_output.height}",
                                f"**种子 (Seed):** {ai_output.seed}",
                                f"**模型名称 (Model):** {self.valves.model_name}",
                                "\n### 生成的图片",
                                f"![预览图]({image_url})",
                                f"[🖼️图片下载链接]({image_url})",
                            ]
                            body["messages"][-1]["content"] = "\n\n".join(content_lines)

                            await __event_emitter__(
                                {
                                    "type": "status",
                                    "data": {
                                        "description": "🎉图片生成成功！",
                                        "done": True,
                                    },
                                }
                            )
                        else:
                            raise Exception("Siliconflow API Error: No images found in response.")
                else:
                    raise Exception(f"AI Output Error: {ai_output.reason}")
        return body
