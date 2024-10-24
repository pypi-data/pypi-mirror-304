import subprocess
from .defaults import default
from enum import Enum
from pydantic import BaseModel, conint, Extra, root_validator, HttpUrl
from typing import Optional
import os

# Custom exceptions to be raised when using custom_openai_compatible provider.
class MissingModelError(ValueError):
    def __init__(self):
        self.message = "The model cannot be None for the 'custom_openai_compatible' provider."
        super().__init__(self.message)

class MissingHostError(ValueError):
    def __init__(self):
        self.message = "The 'host' field is required and must be a valid URL when using the 'custom_openai_compatible' provider."
        super().__init__(self.message)

def get_diff() -> str:
    """Retrieve the staged changes in the git repository."""
    diff = subprocess.run(['git', 'diff', '--staged', '-M'], capture_output=True, text=True)
    return diff.stdout

def get_context_size(diff : str, system : str) -> int:
    """Based on the git diff and system prompt estimate ollama context window needed"""
    input_len = len(system) + len(diff)
    num_ctx = int(min(max(input_len*2.64, 1024), 128000))
    return num_ctx


class EmojiSteps(Enum):
    """If emoji should be performed in the same step as the message or in a separe one"""
    single = 'single'
    step2 = '2-step'
    false = False


class LModelOptions(BaseModel):
    """The options for the LLM"""
    num_ctx: Optional[int] = None
    temperature: Optional[float] = None
    max_tokens: Optional[conint(ge=1)] = None  # Ensure max_tokens is a positive integer if provided

    class Config:
        extra = Extra.allow # Allows for extra arguments

class Provider(str, Enum):
    """The supported LLM Providers"""
    ollama = 'ollama'
    openai = 'openai'
    google = 'google'
    groq = 'groq'
    oai_custom = 'custom_openai_compatible'


class LModel(BaseModel):
    """The model object containin the provider, model name, system prompt, option and host"""
    provider: Provider = Provider.ollama
    model: Optional[str] = None # Most providers have default, required for custom_openai_compatible
    system_prompt: Optional[str] = None
    options: Optional[LModelOptions] = None
    host: Optional[HttpUrl] = None  # required for custom_openai_compatible

    @root_validator(pre=True)
    def set_model_default(cls, values):
        # If 'model' is not provided, set it based on 'provider'
        provider = values.get('provider')
        if 'model' not in values or values['model'] is None:
            if provider == Provider.ollama:
                values['model'] = 'gemma2'
            if provider == Provider.groq:
                values['model'] = 'llama-3.1-70b-versatile'
            elif provider == Provider.google:
                values['model'] = 'gemini-1.5-pro'
            elif provider == Provider.openai:
                values['model'] = 'gpt-3.5-turbo'
        return values

        @root_validator(pre=True)
        def validate_provider_requirements(cls, values):
            provider = values.get('provider')

            # Enforce that 'model' is not None when using custom_openai_compatible
            if provider == Provider.oai_custom:
                if not values.get('model'):
                    raise MissingModelError()

            return values

        @root_validator(pre=True)
        def check_host_for_oai_custom(cls, host, values):
            provider = values.get('provider')
            if provider == Provider.oai_custom and not host:
                raise MissingHostError()

            return host

class Context(BaseModel):
    """Context object for tha commit request"""
    project_name: Optional[str] = None
    project_language: Optional[str] = None
    project_description: Optional[str] = None
    commit_guidelines: Optional[str] = None

class EmojiConfig(BaseModel):
    emoji_steps: EmojiSteps = EmojiSteps.single
    emoji_convention: str = "simple"
    emoji_model: Optional[LModel] = None

class CommitCraftRequest(BaseModel):
    diff: str
    models: LModel = LModel() # Will support multiple models in 1.1.0 but for now only one
    emoji: EmojiConfig = EmojiConfig()
    context: Optional[Context] = None

def commit_craft(request: CommitCraftRequest) -> str:
    """CommitCraft generates a system message and requests a commit message based on staged changes """
    context_info = request.context
    system_prompt = request.models.system_prompt
    if not system_prompt and context_info:
        if (context_info.project_name and context_info.project_language and context_info.project_description):
            system_prompt = f'''
# Proposure

You are a commit message helper for {context_info.project_name} a project written in {context_info.project_language} described as :

{context_info.project_description}

Your only task is to recive a git diff and return a simple commit message folowing these guidelines:

{context_info.commit_guidelines if context_info.commit_guidelines else  default.get("commit_guidelines")}
            '''.strip()
        else:
            system_prompt = f'''
# Proposure

You are a commit message helper.

Your only task is to recive a git diff and return a simple commit message folowing these guidelines:

{context_info.commit_guidelines if context_info.commit_guidelines else  default.get("commit_guidelines")}
            '''.strip()
    elif not system_prompt and not context_info:
        system_prompt = f'''
# Proposure

You are a commit message helper.

Your only task is to recive a git diff and return a simple commit message folowing these guidelines:

{default.get("commit_guidelines")}
        '''.strip()

    emoji = request.emoji
    if emoji.emoji_steps == EmojiSteps.single:
        if emoji.emoji_convention in ('simple', 'full'):
            system_prompt+=f"\n\n{default.get('emoji_guidelines', {}).get(emoji.emoji_convention)}"
        elif emoji.emoji_convention:
            system_prompt+=f"\n\n{emoji.emoji_convention}"

    model = request.models
    model_options = model.options.dict() if model.options else {}
    match model.provider:
        case "ollama":
            import ollama
            Ollama = ollama.Client(str(model.host) if model.host else os.getenv("OLLAMA_HOST"))
            if 'num_ctx' in model_options.keys():
                if model_options['num_ctx']:
                    return Ollama.generate(
                        model=model.model,
                        system=system_prompt,
                        prompt=request.diff,
                        options=model_options
                    )['response']
                else:
                    model_options['num_ctx'] = get_context_size(request.diff, system_prompt)
                    return Ollama.generate(
                        model=model.model,
                        system=system_prompt,
                        prompt=request.diff,
                        options=model_options
                    )['response']
            else:
                model_options['num_ctx'] = get_context_size(request.diff, system_prompt)
                return Ollama.generate(
                    model=model.model,
                    system=system_prompt,
                    prompt=request.diff,
                    options=model_options
                )['response']

        case "groq":
            from groq import Groq
            client = Groq(api_key=os.getenv('GROQ_API_KEY'))
            groq_configs = ('top_p','temperature', 'max_tokens')
            groq_options = {config : model_options.get(config) if model_options.get(config) else None for config in (set(tuple(model_options.keys())) & set(groq_configs))}
            return client.chat.completions.create(
                messages=[
                    {
                        "role" : "system",
                        "content" : system_prompt
                    },
                    {
                        "role" : "user",
                        "content" : request.diff
                    }
                ],
                model=model.model,
                stream=False,
                **groq_options
            ).choices[0].message.content

        case 'google':
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            model=genai.GenerativeModel(
              model_name=model.model,
              system_instruction=system_prompt)
            return model.generate_content(request.diff).text

        case 'openai':
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            openai_configs = ('top_p','temperature', 'max_tokens')
            openai_options = {config : model_options.get(config) if model_options.get(config) else None for config in (set(tuple(model_options.keys())) & set(openai_configs))}
            return client.chat.completions.create(
                messages=[
                    {
                        "role" : "system",
                        "content" : system_prompt
                    },
                    {
                        "role" : "user",
                        "content" : request.diff
                    }
                ],
                model=model.model,
                stream=False,
                **openai_options
            ).choices[0].message.content

        case 'custom_openai_compatible':
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('CUSTOM_API_KEY', default='nokey'), base_url=str(model.host))
            openai_configs = ('top_p','temperature', 'max_tokens')
            openai_options = {config : model_options.get(config) if model_options.get(config) else None for config in (set(tuple(model_options.keys())) & set(openai_configs))}
            return client.chat.completions.create(
                messages=[
                    {
                        "role" : "system",
                        "content" : system_prompt
                    },
                    {
                        "role" : "user",
                        "content" : request.diff
                    }
                ],
                model=model.model,
                stream=False,
                **openai_options
            ).choices[0].message.content

        case _:
            raise NotImplementedError("provider not found")
