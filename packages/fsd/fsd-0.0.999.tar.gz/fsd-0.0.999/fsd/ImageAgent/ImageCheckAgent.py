import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class ImageCheckAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_image_check_plan(self, user_prompt):
        """
        Get a plan for image generation based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image generation plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an extremely precise image request analyzer. Your task is to scrutinize the user's request with utmost diligence to detect ANY indication, no matter how subtle or implicit, of a need to generate, create, or produce even a SINGLE NEW image in png, jpg, jpeg, PNG, JPG, JPEG, or .ico format. Your focus is EXCLUSIVELY on NEW image generation demands.\n\n"
                    "IMPORTANT RULES:\n"
                    "1. Completely disregard all mentions of modifying existing images, moving images, or any other image-related tasks that don't involve creating new images.\n"
                    "2. Return '1' if there is even the slightest hint that at least one new image of these types might need to be generated. This includes implied needs, vague references, or any contextual clues that suggest new image creation.\n"
                    "3. Return '0' ONLY if you are 100% certain, without any shadow of doubt, that absolutely no new images of these types are required or implied.\n"
                    "4. Be extremely cautious about returning '0'. If there's any uncertainty at all, always err on the side of returning '1'.\n\n"
                    "Respond in this exact JSON format:\n"
                    "{\n"
                    '    "result": ""\n'
                    "}\n\n"
                    "Examples:\n"
                    "1. If there's any indication of new image creation:\n"
                    "   Response: {'result': '1'}\n"
                    "2. If there's absolutely no indication of new image creation:\n"
                    "   Response: {'result': '0'}"
                )
            },
            {
                "role": "user",
                "content": f"Conduct an exhaustive analysis of the following request. Look for ANY indication, no matter how subtle or indirect, of a need to create NEW PNG, png, JPG, jpg, JPEG, jpeg, or .ico images. Even a single new image requirement should be flagged. Disregard all other image types or operations. Request: {user_prompt}"
            }
        ]

        try:
            logger.debug("\n #### The `ImageCheckAgent` is initiating a request to the AI Gateway")
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `ImageCheckAgent` has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### The `ImageCheckAgent` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `ImageCheckAgent` has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.error(f" #### The `ImageCheckAgent` encountered an error during the process: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_image_check_plans(self, user_prompt):
        """
        Get image generation plans based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Image generation plan or error reason.
        """
        logger.debug("\n #### The `ImageCheckAgent` is beginning to retrieve image check plans")
        plan = await self.get_image_check_plan(user_prompt)
        logger.debug("\n #### The `ImageCheckAgent` has successfully retrieved image check plans")
        return plan
