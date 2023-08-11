import regex as re
import json
import requests
from os import getenv
from dotenv import load_dotenv


def summarize(data,model_number):
    text = data["content"]
    # to_tokanize = text[:1024]
    load_dotenv()
    HF_TOKEN = getenv("HF_TOKEN")
    if model_number == 1:
        API_URL = (
            "https://api-inference.huggingface.co/models/tuner007/pegasus_summarizer"
        )
    elif model_number == 2:
        API_URL = (
            "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        )
    elif model_number == 3:
        API_URL = (
            "https://api-inference.huggingface.co/models/pszemraj/led-base-book-summary"
        )
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "min_length": 100, "max_length": 300}
    response = requests.request("POST", API_URL, headers=headers, data=payload)
    summarized = json.loads(response.content.decode("utf-8"))

    tmp = " ".join([str(i) for i in summarized])
    tmp = tmp.replace("{", "")
    tmp = tmp.replace("''", "")
    tmp = tmp.replace(f"{chr(61623)}", "")
    tmp = tmp.replace("\x92", "")
    tmp = tmp.replace("\x0c", "")
    regex_pattern = "(?<='summary_text': '|\" )(.*)(?= .'|\"})"

    try:
        result = re.search(regex_pattern, tmp).group(0)
    except:
        result = tmp

    result = result.encode("ascii", "ignore")
    result = result.decode()
    data["summary"] = result
    return data
