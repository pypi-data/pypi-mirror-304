from portkey_ai import Portkey
from typing import Dict, List, Optional
import random
import asyncio
import time

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class BaseModel:
    def __init__(self, api_key: str, virtual_key: str, config_id: str):
        self.portkey = Portkey(api_key=api_key, virtual_key=virtual_key, config=config_id)

    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        raise NotImplementedError

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        raise NotImplementedError

class AzureModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        logger.debug("Using AzureModel for prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 4096
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Using AzureModel for stream_prompt")
        common_params = {
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.2,
            "top_p": 0.1,
            "stream": True
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

class BedrockModel(BaseModel):

    async def coding_prompt(self, messages: List[Dict[str, str]], model: str) -> Dict:
        logger.debug("Using BedrockModel for coding_prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 4096,
            "model": model
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)


    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        logger.debug("Using BedrockModel for prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 4096,
            "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Using BedrockModel for stream_prompt")
        common_params = {
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.2,
            "top_p": 0.1,
            "stream": True,
            "model": "anthropic.claude-3-5-sonnet-20240620-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)
    
    def generate_image(self, prompt: str):
        return self.portkey.images.generate(
            prompt=prompt,
            model="stability.stable-diffusion-xl-v1"
        )

class BedrockOpusModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        logger.debug("Using BedrockOpusModel for prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 4096,
            "model": "anthropic.claude-3-opus-20240229-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Using BedrockOpusModel for stream_prompt")
        common_params = {
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.2,
            "top_p": 0.1,
            "stream": True,
            "model": "anthropic.claude-3-opus-20240229-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

class GeminiModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        logger.debug("Using GeminiModel for prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 4096,
            "model": "gemini-1.5-pro"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Using GeminiModel for stream_prompt")
        common_params = {
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.2,
            "top_p": 0.1,
            "stream": True,
            "model": "gemini-1.5-pro"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

class GeminiFlashModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        logger.debug("Using GeminiFlashModel for prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 4096,
            "model": "gemini-1.5-flash"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Using GeminiFlashModel for stream_prompt")
        common_params = {
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.2,
            "top_p": 0.1,
            "stream": True,
            "model": "gemini-1.5-flash"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

class DalleModel(BaseModel):
    def generate_image(self, prompt: str, size: str = "1024x1024"):
        logger.debug("Using DALL-E 3 for image generation")
        return self.portkey.images.generate(prompt=prompt, size=size)

class LlamaModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        logger.debug("Using LlamaModel for prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 2048,
            "model": "meta.llama3-1-70b-instruct-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Using LlamaModel for stream_prompt")
        common_params = {
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.2,
            "top_p": 0.1,
            "stream": True,
            "model": "meta.llama3-1-70b-instruct-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

class CodingLlamaModel(BaseModel):
    async def prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> Dict:
        logger.debug("Using CodingLlamaModel for prompt")
        common_params = {
            "messages": messages,
            "temperature": 0.2,
            "top_p": 0.1,
            "max_tokens": 2048,
            "model": "meta.llama3-1-405b-instruct-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

    async def stream_prompt(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float):
        logger.debug("Using CodingLlamaModel for stream_prompt")
        common_params = {
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.2,
            "top_p": 0.1,
            "stream": True,
            "model": "meta.llama3-1-405b-instruct-v1:0"
        }
        return await asyncio.to_thread(self.portkey.chat.completions.create, **common_params)

class AIGateway:
    _instance = None

    API_KEY = "Tf7rBh3ok+wNy+hzHum7dmizdBFh"
    CONFIG_ID = "pc-zinley-74e593"
    
    VIRTUAL_KEYS: Dict[str, str] = {
        "azure1": "azure-4667e4",
        "azure2": "azure-7e4746",
        "bedrock": "bedrock-bfa916",
        "gemini": "gemini-b5d385",
        "dalle3_1": "dalle3-34c86a",
        "dalle3_2": "dalle3-ea9815"
    }

    ARCH_STEAM_WEIGHTS = {
        "azure1": 0.35,
        "azure2": 0.35,
        "bedrock": 0.3,
    }

    MODEL_WEIGHTS = {
        "azure1": 0.45,
        "azure2": 0.45,
        "bedrock": 0.1,
    }

    STREAM_MODEL_WEIGHTS = {
        "azure1": 0.45,
        "azure2": 0.45,
        "bedrock": 0.1,
    }

    STREAM_EXPLAINER_MODEL_WEIGHTS = {
        "azure1": 0.5,
        "azure2": 0.5
    }

    STREAM_Architect_MODEL_WEIGHTS = {
        "bedrock": 1,
    }

    Architect_MODEL_WEIGHTS = {
        "bedrock": 1,
    }

    CODING_MODEL_WEIGHTS = {
        "bedrock": 1
    }

    IMAGE_MODEL_WEIGHTS = {
        "sdxl": 0.3,
        "dalle3_model1": 0.2,
        "dalle3_model2": 0.5,
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIGateway, cls).__new__(cls)
            cls._instance.azure1_model = AzureModel(cls.API_KEY, cls.VIRTUAL_KEYS["azure1"], cls.CONFIG_ID)
            cls._instance.azure2_model = AzureModel(cls.API_KEY, cls.VIRTUAL_KEYS["azure2"], cls.CONFIG_ID)
            cls._instance.bedrock_model = BedrockModel(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock"], cls.CONFIG_ID)
            cls._instance.bedrock_opus_model = BedrockOpusModel(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock"], cls.CONFIG_ID)
            cls._instance.gemini_model = GeminiModel(cls.API_KEY, cls.VIRTUAL_KEYS["gemini"], cls.CONFIG_ID)
            cls._instance.gemini_flash_model = GeminiFlashModel(cls.API_KEY, cls.VIRTUAL_KEYS["gemini"], cls.CONFIG_ID)
            cls._instance.dalle3_model1 = DalleModel(cls.API_KEY, cls.VIRTUAL_KEYS["dalle3_1"], cls.CONFIG_ID)
            cls._instance.dalle3_model2 = DalleModel(cls.API_KEY, cls.VIRTUAL_KEYS["dalle3_2"], cls.CONFIG_ID)
            cls._instance.llama_model = LlamaModel(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock"], cls.CONFIG_ID)
            cls._instance.coding_llama_model = CodingLlamaModel(cls.API_KEY, cls.VIRTUAL_KEYS["bedrock"], cls.CONFIG_ID)
            logger.debug("AIGateway initialized with all models")
        return cls._instance

    def _select_model(self, weights, exclude=None):
        available_models = {k: v for k, v in weights.items() if k != exclude}
        if not available_models:
            raise ValueError("No available models to choose from")
        selected_model = random.choices(list(available_models.keys()), 
                              weights=list(available_models.values()), 
                              k=1)[0]
        logger.debug(f"Selected model: {selected_model}")
        return selected_model

    async def prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting prompt method")
        tried_models = set()
        while len(tried_models) < len(self.MODEL_WEIGHTS):
            model_type = self._select_model(self.MODEL_WEIGHTS, exclude=tried_models)
            error_429_count = 0
            while error_429_count < 2:
                try:
                    logger.debug(f"Attempting to use {model_type} model")
                    model = getattr(self, f"{model_type}_model")
                    completion = await model.prompt(messages, max_tokens, temperature, top_p)
                    logger.debug(f"Successfully received response from {model_type} model")
                    return completion
                except Exception as e:
                    if "429" in str(e):
                        error_429_count += 1
                        logger.error(f"Error 429 encountered for {model_type} model. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                    else:
                        logger.error(f"Error in prompting {model_type} model: {str(e)}")
                        break
            tried_models.add(model_type)
        
        logger.debug("All models failed to respond")
        raise Exception("All models failed to respond")
    
    async def arch_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting arch_prompt method")
        model_type = "bedrock"
        model = getattr(self, f"{model_type}_model")
        error_429_count = 0
        for attempt in range(3):
            try:
                logger.debug(f"Attempt {attempt + 1}: Using {model_type} model for architecture")
                completion = await model.prompt(messages, max_tokens, temperature, top_p)
                logger.debug(f"Successfully received response from {model_type} model for architecture")
                return completion
            except Exception as e:
                if "429" in str(e):
                    error_429_count += 1
                    if error_429_count < 2:
                        logger.debug(f"Error 429 encountered. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                        continue
                logger.debug(f"Error in prompting {model_type} model for architecture: {str(e)}")
                if attempt < 2:
                    logger.error(f"Retrying in 1-3 seconds...")
                    await asyncio.sleep(random.uniform(1, 3))
                else:
                    logger.error("All attempts failed for arch_prompt")
                    raise Exception("All attempts failed for arch_prompt")
    
    async def coding_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0) -> Dict:
        logger.debug("Starting coding_prompt method")
        models = [
            "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0"
        ]
        for i, model in enumerate(models):
            attempts = 1 if i == 0 else 2  # v2 gets 1 attempt, v1 gets 2 attempts
            error_429_count = 0
            for attempt in range(attempts):
                try:
                    logger.debug(f"Attempt {attempt + 1} for coding with {model}")
                    completion = await self.bedrock_model.coding_prompt(messages, model)
                    logger.debug(f"Successfully received response for coding from {model}")
                    return completion
                except Exception as e:
                    if "429" in str(e):
                        error_429_count += 1
                        if error_429_count < 2:
                            logger.debug(f"Error 429 encountered. Retrying in 5 seconds...")
                            await asyncio.sleep(5)
                            continue
                    logger.debug(f"Error in prompting for coding with {model}: {str(e)}")
                    if attempt < attempts - 1:
                        logger.info(f"Retrying in 2-3 seconds...")
                        await asyncio.sleep(random.uniform(2, 3))
                    else:
                        if i < len(models) - 1:
                            logger.error(f"{model} failed, falling back to {models[i+1]}")
                        else:
                            logger.error("All versions failed")
        
        logger.debug("All models and attempts failed for coding prompt")
        raise Exception("All models and attempts failed for coding prompt")

    async def stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        logger.debug("Starting stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.STREAM_MODEL_WEIGHTS):
            model_type = self._select_model(self.STREAM_MODEL_WEIGHTS, exclude=tried_models)
            error_429_count = 0
            while error_429_count < 2:
                try:
                    logger.debug(f"Attempting to use {model_type} model for streaming")
                    model = getattr(self, f"{model_type}_model")
                    chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                    logger.debug(f"Successfully received streaming response from {model_type} model")
                    final_response = ""
                    for chunk in chat_completion_stream:
                        if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            print(content, end='', flush=True)
                            final_response += content
                    print()
                    return final_response
                except Exception as e:
                    if "429" in str(e):
                        error_429_count += 1
                        logger.error(f"Error 429 encountered for {model_type} model. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                    else:
                        logger.error(f"Error in streaming from {model_type} model: {str(e)}")
                        break
            tried_models.add(model_type)
        
        logger.debug("All models failed to respond for stream prompt")
        raise Exception("All models failed to respond")
    
    async def explainer_stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        logger.debug("Starting explainer_stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.STREAM_EXPLAINER_MODEL_WEIGHTS):
            model_type = self._select_model(self.STREAM_EXPLAINER_MODEL_WEIGHTS, exclude=tried_models)
            error_429_count = 0
            while error_429_count < 2:
                try:
                    logger.debug(f"Attempting to use {model_type} model for streaming")
                    model = getattr(self, f"{model_type}_model")
                    chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                    logger.debug(f"Successfully received streaming response from {model_type} model")
                    final_response = ""
                    for chunk in chat_completion_stream:
                        if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            print(content, end='', flush=True)
                            final_response += content
                    print()
                    return final_response
                except Exception as e:
                    if "429" in str(e):
                        error_429_count += 1
                        logger.error(f"Error 429 encountered for {model_type} model. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                    else:
                        logger.error(f"Error in streaming from {model_type} model: {str(e)}")
                        break
            tried_models.add(model_type)
        
        logger.debug("All models failed to respond for explainer stream prompt")
        raise Exception("All models failed to respond")
    
    async def arch_stream_prompt(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 4096, 
                     temperature: float = 0.2, 
                     top_p: float = 0):
        logger.debug("Starting arch_stream_prompt method")
        tried_models = set()
        while len(tried_models) < len(self.ARCH_STEAM_WEIGHTS):
            model_type = self._select_model(self.ARCH_STEAM_WEIGHTS, exclude=tried_models)
            error_429_count = 0
            while error_429_count < 2:
                try:
                    logger.debug(f"Attempting to use {model_type} model for streaming")
                    model = getattr(self, f"{model_type}_model")
                    chat_completion_stream = await model.stream_prompt(messages, max_tokens, temperature, top_p)
                    logger.debug(f"Successfully received streaming response from {model_type} model")
                    final_response = ""
                    for chunk in chat_completion_stream:
                        if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            print(content, end='', flush=True)
                            final_response += content
                    print()
                    return final_response
                except Exception as e:
                    if "429" in str(e):
                        error_429_count += 1
                        logger.error(f"Error 429 encountered for {model_type} model. Retrying in 5 seconds...")
                        await asyncio.sleep(5)
                    else:
                        logger.error(f"Error in streaming from {model_type} model: {str(e)}")
                        break
            tried_models.add(model_type)
        
        logger.debug("All models failed to respond for arch stream prompt")
        raise Exception("All models failed to respond")

    def generate_image(self, prompt: str, size: str = "1024x1024"):
        logger.debug("Starting image generation")
        tried_models = set()
        while len(tried_models) < len(self.IMAGE_MODEL_WEIGHTS):
            model_type = self._select_model(self.IMAGE_MODEL_WEIGHTS, exclude=tried_models)
            error_429_count = 0
            while error_429_count < 2:
                logger.debug(f"Attempting to use {model_type} model for image generation")
                try:
                    if model_type.startswith("dalle3"):
                        image = getattr(self, f"{model_type}").generate_image(prompt, size)
                    else:
                        image = self.bedrock_model.generate_image(prompt)
                    logger.debug(f"Successfully generated image with {model_type} model")
                    return image
                except Exception as e:
                    if "429" in str(e):
                        error_429_count += 1
                        logger.debug(f"Error 429 encountered for {model_type} model. Retrying in 5 seconds...")
                        time.sleep(5)
                    else:
                        logger.error(f"Error in generating image, retrying...")
                        break
            tried_models.add(model_type)
        
        raise Exception("All image generation models failed!")