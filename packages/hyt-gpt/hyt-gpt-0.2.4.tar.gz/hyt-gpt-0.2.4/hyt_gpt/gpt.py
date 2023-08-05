import requests
from typing import List
import logging


def chat_gpt(key, prompt, text):
    API_KEY = key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    }
    response = requests.post(
        'https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    # Return Error message if response is not 200
    if response.status_code != 200:
        logging.info('response:', response.content)
        return str(response.json()['error'])

    return response.json()['choices'][0]['message']['content']


def seg_transcript(transcript: List[str]) -> List[str]:
    transcript = [{"text": item["text"], "index": index,
                   "timestamp": item["start"]} for index, item in enumerate(transcript)]
    text = " ".join([x["text"]
                    for x in sorted(transcript, key=lambda x: x["index"])])
    len_original = len(text)
    seg_length = 4096
    if len_original >= seg_length:
        chunkedText = getChunckedTranscripts(transcript, transcript)
        print(
            f'Transcript length: {len_original} is too long, truncated via lossy compression to {len(chunkedText)}.')
        return [chunkedText]
    length = len(text)
    print(f'Processing text length: {length}.')
    n = length // seg_length + 1
    division = len(transcript) // n
    new_l = [transcript[i * division: (i + 1) * division] for i in range(n)]
    segedTranscipt = [" ".join([x["text"] for x in sorted(
        j, key=lambda x: x["index"])]) for j in new_l]
    return segedTranscipt


"""
Lossy Compression Summary

A helpful rule of thumb is that one token generally corresponds to ~4 
characters of text for common English text. 

This translates to roughly ¾ of a word (so 100 tokens ~= 75 words).
"""


def getChunckedTranscripts(textData, textDataOriginal, limit=3072) -> str:

    result = ""
    text = " ".join([x["text"]
                    for x in sorted(textData, key=lambda x: x["index"])])

    if len(text) > limit:
        evenTextData = [t for i, t in enumerate(textData) if i % 2 == 0]
        result = getChunckedTranscripts(evenTextData, textDataOriginal)
    else:
        if len(textDataOriginal) != len(textData):
            for obj in textDataOriginal:
                if any(t["text"] == obj["text"] for t in textData):
                    continue
                textData.append(obj)
                newText = " ".join([x["text"] for x in sorted(
                    textData, key=lambda x: x["index"])])

                if len(newText) < limit:
                    nextText = textDataOriginal[[
                        t["text"] for t in textDataOriginal].index(obj["text"]) + 1]
                    if len(newText) + len(nextText["text"]) > limit:
                        overRate = ((len(newText) + len(nextText["text"])) -
                                    limit) / len(nextText["text"])
                        chunkedText = nextText["text"][:int(
                            len(nextText["text"])*overRate)]
                        textData.append(
                            {"text": chunkedText, "index": nextText["index"]})
                        result = " ".join([x["text"] for x in sorted(
                            textData, key=lambda x: x["index"])])

                    else:
                        result = newText
        else:
            result = text
    if result == "":
        result = " ".join([x["text"] for x in sorted(
            textDataOriginal, key=lambda x: x["index"])])
    return result
