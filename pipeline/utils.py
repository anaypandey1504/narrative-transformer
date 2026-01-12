import json
import time
import functools
from typing import Callable, Any


def parse_llm_json(response_content: str) -> dict:
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        pass
    
    text = response_content
    start = text.find('{')
    end = text.rfind('}') + 1
    
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    raise ValueError(f"Failed to parse JSON from response: {text[:200]}...")


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"  ⚠ Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        print(f"  ✗ All {max_retries + 1} attempts failed.")
            
            raise last_exception
        
        return wrapper
    return decorator


def make_llm_call(client, model: str, messages: list, temperature: float, 
                  response_format: dict = None, max_tokens: int = None) -> str:
    @retry_with_backoff(max_retries=3, initial_delay=1.0)
    def _call():
        kwargs = {
            'model': model,
            'messages': messages,
            'temperature': temperature
        }
        if response_format:
            kwargs['response_format'] = response_format
        if max_tokens:
            kwargs['max_tokens'] = max_tokens
            
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    
    return _call()
