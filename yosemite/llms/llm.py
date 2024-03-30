import os
import asyncio
from typing import Optional
import anthropic
import instructor
from openai import OpenAI
import requests
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from huggingface_hub import InferenceClient
import xai_sdk

class LLM:
    def __init__(self, provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
            """
            Initializes the LLM class with the specified provider, API key, base URL, and model.

            Args:
                provider (str): The provider for the language model. Supported providers are "openai", "anthropic", "nvidia",
                                "ai21", "mistral", "huggingface", and "transformers".
                api_key (str, optional): The API key for the provider. Defaults to None.
                base_url (str, optional): The base URL for the provider. Only applicable for the "nvidia" provider. Defaults to None.
                model (str, optional): The name or path of the model. Only applicable for the "transformers" provider. Defaults to None.

            Raises:
                ValueError: If the API key is not available for the specified provider.

            Examples:
                Initialize LLM class with OpenAI provider and API key:
                >>> llm = LLM(provider="openai", api_key="YOUR_OPENAI_API_KEY")

                Initialize LLM class with NVIDIA provider, API key, and base URL:
                >>> llm = LLM(provider="nvidia", api_key="YOUR_NVIDIA_API_KEY", base_url="https://integrate.api.nvidia.com/v1")

                Initialize LLM class with Transformers provider and model name or path:
                >>> llm = LLM(provider="transformers", model="gpt2")
            """
            self.provider = provider.lower()
            self.api_key = api_key
            self.base_url = base_url
            self.model_name_or_path = model

            if self.provider == "openai":
                if self.api_key is None:
                    self.api_key = os.getenv("OPENAI_API_KEY")
                if self.api_key is None:
                    raise ValueError("OpenAI API key is not available")
                self.llm = instructor.patch(OpenAI(api_key=self.api_key))
            elif self.provider == "anthropic":
                if self.api_key is None:
                    self.api_key = os.getenv("ANTHROPIC_API_KEY")
                if self.api_key is None:
                    raise ValueError("Anthropic API key is not available")
                self.client = anthropic.Anthropic(api_key=self.api_key)
            elif self.provider == "nvidia":
                if self.api_key is None:
                    self.api_key = os.getenv("NVIDIA_API_KEY")
                if self.api_key is None:
                    raise ValueError("NVIDIA API key is not available")
                if self.base_url is None:
                    self.base_url = "https://integrate.api.nvidia.com/v1"
                self.llm = OpenAI(base_url=self.base_url, api_key=self.api_key)
            elif self.provider == "ai21":
                if self.api_key is None:
                    self.api_key = os.getenv("AI21_API_KEY")
                if self.api_key is None:
                    raise ValueError("AI21 API key is not available")
                self.url = "https://api.ai21.com/studio/v1/j2-mid/complete"
            elif self.provider == "mistral":
                if self.api_key is None:
                    self.api_key = os.getenv("MISTRAL_API_KEY")
                if self.api_key is None:
                    raise ValueError("Mistral API key is not available")
                self.client = MistralClient(api_key=self.api_key)
            elif self.provider == "huggingface":
                self.client = InferenceClient()
            elif self.provider == "grok":
                self.client = xai_sdk.Client()
                self.chat = self.client.chat
            elif self.provider == "transformers":
                if self.model_name_or_path is None:
                    raise ValueError("Model name or path is required for transformers provider")
                from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, padding_side="left", truncation_side="left")
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path)
                self.pipeline = TextGenerationPipeline(model=self.model, tokenizer=self.tokenizer)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
    async def invoke_grok(self, query: str, stream: bool = False):
        conversation = self.chat.create_conversation()
        
        if stream:
            token_stream, _ = conversation.add_response(query)
            response = ""
            async for token in token_stream:
                response += token
            return response
        else:
            response = await conversation.add_response_no_stream(query)
            return response.message

    def invoke(
        self,
        system: Optional[str] = None,
        query: Optional[str] = None,
        model: str = "gpt-3.5-turbo-1106",
        pydantic_model=None,
        max_tokens: int = 1024,
        temperature: float = 0.75,
        top_p: float = 1,
        stream: bool = False,
        max_length: int = 100,
        num_return_sequences: int = 1,
        top_k: int = 50,
        do_sample: bool = True,
    ):
        if query is None:
            raise ValueError("Query is required for instruct()")
        
        if system is None:
            system = "You are a helpful assistant."

        if self.provider == "openai":
            if model == "3":
                model = "gpt-3.5-turbo-1106"
            elif model == "4":
                model = "gpt-4-turbo-preview"

            completion = self.llm.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": query},
                ],
                response_model=pydantic_model,
            )
            
            if pydantic_model is None:
                return completion.choices[0].message.content
            else:
                return completion.completion
            
        elif self.provider == "anthropic":
            if system is None:
                system_prompt = "You are a helpful assistant."
            else:
                system_prompt = system

            if model is None:
                model = "claude-3-opus-20240229"

            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": query
                            }
                        ]
                    }
                ]
            )
            return message.content
        elif self.provider == "nvidia":
            completion = self.llm.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": query}],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=stream
            )

            if stream:
                response = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        response += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="")
                return response
            else:
                return completion.choices[0].message.content
        elif self.provider == "ai21":
            payload = {
                "numResults": 1,
                "maxTokens": max_tokens,
                "minTokens": 0,
                "temperature": temperature,
                "topP": top_p,
                "topKReturn": 0,
                "frequencyPenalty": {
                    "scale": 0,
                    "applyToWhitespaces": True,
                    "applyToPunctuations": True,
                    "applyToNumbers": True,
                    "applyToStopwords": True,
                    "applyToEmojis": True
                },
                "presencePenalty": {
                    "scale": 0,
                    "applyToWhitespaces": True,
                    "applyToPunctuations": True,
                    "applyToNumbers": True,
                    "applyToStopwords": True,
                    "applyToEmojis": True
                },
                "countPenalty": {
                    "scale": 0,
                    "applyToWhitespaces": True,
                    "applyToPunctuations": True,
                    "applyToNumbers": True,
                    "applyToStopwords": True,
                    "applyToEmojis": True
                }
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            response = requests.post(self.url, json=payload, headers=headers)
            return response.json()["completions"][0]["data"]["text"]
        elif self.provider == "mistral":
            messages = [
                ChatMessage(role="user", content=query)
            ]
            if stream:
                stream_response = self.client.chat_stream(model=model, messages=messages)
                response = ""
                for chunk in stream_response:
                    response += chunk.choices[0].delta.content
                return response
            else:
                chat_response = self.client.chat(model=model, messages=messages)
                return chat_response.choices[0].message.content
        elif self.provider == "huggingface":
            if stream:
                response = ""
                for token in self.client.text_generation(query, max_new_tokens=max_tokens, temperature=temperature, top_p=top_p, stream=True):
                    response += token
                return response
            else:
                return self.client.text_generation(query, max_new_tokens=max_tokens, temperature=temperature, top_p=top_p)
        elif self.provider == "grok":
            return asyncio.run(self.invoke_grok(query, stream))
        elif self.provider == "transformers":
            if system is None:
                system = "You are a helpful assistant."
            
            prompt = f"{system}\n\nUser: {query}\nAssistant:"
            
            from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
            
            config = AutoConfig.from_pretrained(self.model_name_or_path)
            tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
            model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path, config=config)
            
        generation_kwargs = {
            "max_length": max_length,
            "num_return_sequences": num_return_sequences,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "do_sample": do_sample,
            "repetition_penalty": 1.2,
            "no_repeat_ngram_size": 2,
            "pad_token_id": tokenizer.eos_token_id,
            "early_stopping": True,
            "num_beams": 3,
        }
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
        generated_outputs = model.generate(**inputs, **generation_kwargs)
        generated_text = tokenizer.decode(generated_outputs[0], skip_special_tokens=True)
        generated_text = generated_text.split("Assistant:", 1)[1].strip()
        return generated_text

if __name__ == "__main__":
    instructor = LLM(provider="openai")
    completion = instructor.invoke(
        query="What is the capital of France?",
        stream=True
    )
    print(completion)
    
    local_llm = LLM(provider="transformers", model="openai-community/gpt2")
    query = "What is the capital of France?"
    completion = local_llm.invoke(query=query, stream=True)
    print(completion)