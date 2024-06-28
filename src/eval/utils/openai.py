import openai
import yaml


def load_client(key_path="openai_key.yaml"):
    openai._reset_client()
    key = yaml.safe_load(open(key_path))
    for k, v in key.items():
        setattr(openai, k, v)
    return openai._load_client()


client = load_client()
