import os
from typing import Optional
import anthropic
import instructor
from openai import OpenAI

class LLM:
    """
    A simplified interface for 'deploying' LLMs in your code.

    ```python
    from yosemite.llms import LLM

    llm = LLM(provider="anthropic")
    completion = llm.invoke(
        query="What is the capital of France?"
    )
    ```

    ```bash
    The capital of France is Paris.
    ```

    ```python
    from pydantic import BaseModel

    class Completion(BaseModel):
        message: str

    instructor = LLM(provider="openai")
    completion = instructor.invoke(
        query="What is the capital of France?",
        pydantic_model=Completion
    )
    ```

    ```bash
    {
        "message": "The capital of France is Paris."
    }
    ```

    Args:
        provider (str): The LLM provider to use. Supported providers are "openai", "anthropic", and "nvidia".
        api_key (str, optional): The API key for the provider. Defaults to None.
        base_url (str, optional): The base URL for the provider. Defaults to None.

    Methods:
        invoke: Invokes the LLM with the given query.

    Raises:
        ValueError: If the provider is not supported or the API key is not available.
    """

    
    def __init__(self, provider: str, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key
        self.base_url = base_url

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
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def invoke(
        self,
        system: Optional[str] = None,
        query: Optional[str] = None,
        model: str = "gpt-3.5-turbo-1106",
        pydantic_model=None,
        max_tokens: int = 1024,
        temperature: float = 0.5,
        top_p: float = 1,
        stream: bool = False,
    ):
        """
        Generates a completion for the given query.

        Example:
        ```python
        completion = llm.invoke(
            query="What is the capital of France?"
        )
        ```

        Args:
            system (str, optional): The system prompt. Defaults to None.
            query (str, optional): The user query. Defaults to None.
            model (str, optional): The model to use. Defaults to "gpt-3.5-turbo-1106".
            pydantic_model (Any, optional): The Pydantic model to use for the response. Defaults to None.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
            temperature (float, optional): The sampling temperature. Defaults to 0.5.
            top_p (float, optional): The nucleus sampling parameter. Defaults to 1.
            stream (bool, optional): Whether to stream the response. Defaults to False.

        Returns:
            Any: The completion response.
        """
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

if __name__ == "__main__":
    instructor = LLM(provider="openai")
    completion = instructor.invoke(
        query="What is the capital of France?",
        stream=True
    )
    print(completion)