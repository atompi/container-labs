"""
title: Flux image generation filter v2
author: atompi
author_url: https://github.com/atompi
funding_url: https://github.com/atompi
version: 0.2
"""

import asyncio
import random
import re
from typing import Any, Awaitable, Callable, Optional

import aiohttp
from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        priority: int = Field(default=10, description="Priority level for the filter operations.")
        Siliconflow_Base_URL: str = Field(
            default="https://api.siliconflow.cn",
            description="Base URL for the Siliconflow API.(Such as https://api.siliconflow.cn)",
        )
        Siliconflow_API_KEY: str = Field(
            default="",
            description="API Key for the Siliconflow API.",
        )
        max_retries: int = Field(
            default=3,
            description="Maximum number of retries for the HTTP requests.",
        )
        image_num: int = Field(
            default=1,
            description="Manage Max Number of images to be generated.",
        )

    class UserValves(BaseModel):
        image_num: int = Field(
            default=1,
            description="Number of images to be generated.",
        )
        image_size: str = Field(
            default="1024x1024",
            description="Size of the image to be generated.(Such as 1024x1024, 512x1024, 768x512, 768x1024, 1024x576, 576x1024)",
        )
        num_inference_steps: int = Field(
            default=20,
            description="Number of inference steps to be performed.(1-100)",
        )

    def __init__(self):
        self.valves = self.Valves()

    @staticmethod
    def remove_markdown_images(content: str) -> str:
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

    async def text_to_image(self, prompt, __user__: Optional[dict] = None):
        url = f"{self.valves.Siliconflow_Base_URL}/v1/black-forest-labs/FLUX.1-schnell/text-to-image"
        payload = {
            "prompt": prompt,
            "image_size": __user__["valves"].image_size,
            "num_inference_steps": __user__["valves"].num_inference_steps,
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
                except Exception:
                    if attempt == self.valves.max_retries - 1:
                        return await response.text()

    async def generate_multiple_images(self, prompt, __user__: Optional[dict] = None):
        image_num = min(__user__["valves"].image_num, self.valves.image_num)
        tasks = [self.text_to_image(prompt, __user__) for _ in range(image_num)]
        results = await asyncio.gather(*tasks)
        return results

    async def outlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]],
        __user__: Optional[dict] = None,
        __model__: Optional[dict] = None,
    ) -> dict:
        # This function is the main entry point for the API, which is used to process the request
        # and return the response. You can modify the code below to customize the behavior of the API.
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
                prompt = messages[-1].get("content", "")
                response_datas = await self.generate_multiple_images(prompt, __user__)
                if response_datas:
                    for response_data in response_datas:
                        if response_data and "images" in response_data:
                            images = response_data.get("images", [])
                            for image in images:
                                # markdown_output = f"![预览图]({images[0].get('url', '')})\n[🖼️图片下载链接]({images[0].get('url', '')})"
                                markdown_output = f"![预览图]({image.get('url', '')})"
                                try:
                                    body["messages"][-1]["content"] += f"\n\n{markdown_output}"
                                except Exception as e:
                                    print(e)
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": "🥳图片生成成功！请查看下方预览图并通过下载按钮下载吧！",
                                "done": True,
                            },
                        }
                    )
                else:
                    raise Exception("Siliconflow API Error: response_datas is None")
        return body
