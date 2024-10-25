from enum import Enum
import os


class ValidatorModules(Enum):
    WORD_FILTER = "word_filter"
    PROFANITY_FILTER = "profanity_filter"
    PII_FILTER = "pii_filter"
    PHRASE_FILTER = "phrase_filter"
    HARMFUL_CONTENT = "harmful_content"


VALIDATOR_MODULE_NAMES = [i.value for i in ValidatorModules]


class ConfigKeys(Enum):
    TYPE = 'type'
    SERVED_MODEL = "served_model"
    MODEL = "model"
    BLOCKED_CATEGORIES = "blocked_categories"
    CATEGORY_LEVELS = "category_levels"
    EXTRA = "extra"
    ENTITIES = "entities"
    LIB_NAME = "lib_name"
    WORDLIST = "wordlist"
    PHRASESLIST = "pharseslist"
    WORDLIST_FILE = "wordlist_file"
    WHITELIST_WORDS = "whitelist_words"
    OVERWRITE_WORDLIST = "overwrite_wordlist"
    PROMPT_TEMPLATE = "prompt_template"
    THRESHOLD = "threshold"
    NAME = "name"
    DESCRIPTION = "description"
    BLOCK_MESSAGE = "block_message"


class ValidatorTypes(Enum):
    EMBEDDINGS = "embedding"
    GUARD = "guard"
    LLM = "llm"
    ALGO = "algo"
    PRESIDIO = "presidio"
    LIB = "lib"
    CLASSIFIER = "classifier"


class LibTypes(Enum):
    BETTER_PROFANITY = "better-profanity"
    ALT_PROFANITY_CHECK = "alt-profanity-check"
    FUZZYSEARCH = "fuzzysearch"


class GenAIModels(Enum):
    E5_MISTRAL_7B_INSTRUCT = "e5-mistral-7b-instruct"
    LLAMA_GUARD_3_8B = "llama_guard_3_8b"
    LLAMA3_2_3B_INSTRUCT = "llama3_2_3b_instruct"


E2E_TIR_TEAM_ID = os.environ.get("E2E_TIR_TEAM_ID")
E2E_TIR_PROJECT_ID = os.environ.get("E2E_TIR_PROJECT_ID")
E2E_TIR_API_KEY = os.environ.get("E2E_TIR_API_KEY")
E2E_TIR_ACCESS_TOKEN = os.environ.get("E2E_TIR_ACCESS_TOKEN")

OPENAI_BASE_URL = f"https://infer.e2enetworks.net/project/p-{E2E_TIR_PROJECT_ID}" + "/genai/{model}/v1"
OPENAI_API_KEY = E2E_TIR_ACCESS_TOKEN
