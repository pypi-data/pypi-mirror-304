from enum import Enum


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


OPENAI_BASE_URL = "https://infer.e2enetworks.net/project/p-3862/genai/{model}/v1"
OPENAI_API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGSjg2R2NGM2pUYk5MT2NvNE52WmtVQ0lVbWZZQ3FvcXRPUWVNZmJoTmxFIn0.eyJleHAiOjE3NTkxNjI5MDYsImlhdCI6MTcyNzYyNjkwNiwianRpIjoiYzQ3Y2UwNmYtMmYyNy00MGZmLWJlMmItZDhhMjlkMTQ5MDZmIiwiaXNzIjoiaHR0cDovL2dhdGV3YXkuZTJlbmV0d29ya3MuY29tL2F1dGgvcmVhbG1zL2FwaW1hbiIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJkNDE5OWM0ZC1jOTA1LTQ1NDUtOTkxYy0wZDFiYWE5NGMwYzQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhcGltYW51aSIsInNlc3Npb25fc3RhdGUiOiI0ZTAyMzlhYS01OTE4LTQxNGItOWMwYS0yNGU0YzlhNzJkZDYiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImFwaXVzZXIiLCJkZWZhdWx0LXJvbGVzLWFwaW1hbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6IjRlMDIzOWFhLTU5MTgtNDE0Yi05YzBhLTI0ZTRjOWE3MmRkNiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkF0aGFydmEgUmF2aW5kcmEgIFBha2FkZSIsInByaW1hcnlfZW1haWwiOiJhdGhhcnZhLnBha2FkZUBlMmVuZXR3b3Jrcy5jb20iLCJpc19wcmltYXJ5X2NvbnRhY3QiOnRydWUsInByZWZlcnJlZF91c2VybmFtZSI6ImF0aGFydmEucGFrYWRlQGUyZW5ldHdvcmtzLmNvbSIsImdpdmVuX25hbWUiOiJBdGhhcnZhIFJhdmluZHJhICIsImZhbWlseV9uYW1lIjoiUGFrYWRlIiwiZW1haWwiOiJhdGhhcnZhLnBha2FkZUBlMmVuZXR3b3Jrcy5jb20ifQ.TPwgOFQZDU2YP7PZflKJmqTW38SzbUEyR66cGYWR42T__ZhrIUBtcyf68vmiIetf_b57_bHjuLo2O5jcs3Oinr-J1YfEvH_hG1QIV-bbrxq91ye6N-NANnf3KvWUWb1B-ecUroAshz1amOADYr2UuZGK7IPMJ29iyVOlydO6Q4s"
