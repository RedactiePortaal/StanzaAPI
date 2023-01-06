import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import stanza
import os

app = FastAPI()

languages = os.getenv('STANZA_LANGUAGES', "nl").split()
packages = os.getenv('STANZA_PACKAGES', 'default').split()

if len(packages) != len(languages):
    packages = ['default' for _ in languages]

pipelines = {}

for lang, pack in zip(languages, packages):
    stanza.download(lang, package=pack, model_dir='./stanza_resources')
    pipelines[lang] = stanza.Pipeline(lang=lang, processors='tokenize,ner')


class AnalysisRequest(BaseModel):
    text: str


@app.post("/ner-per-sentence")
def analyze(req: AnalysisRequest):
    doc = pipelines['nl'](req.text)
    entities = []
    for sent in doc.sentences:
        sentEnts = []
        for ent in sent.ents:
            sentEnts.append({"name": ent.text, "type": ent.type})
        entities.append(sentEnts)
    return entities


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
