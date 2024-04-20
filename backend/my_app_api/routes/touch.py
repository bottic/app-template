import logging


from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from urllib.parse import unquote

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/example", tags=["Example"])

CLICKS: dict[int, int] = {}


class WhoAmI(BaseModel):
    id: int


class TouchGet(WhoAmI):
    count: int

class Text(BaseModel):
    text: str


@router.get("/whoami", response_model=WhoAmI)
def whoami(auth=Depends(UnionAuth(allow_none=False))):
    return {"id": auth["id"]}


@router.get("/touch", response_model=TouchGet)
def touch(auth=Depends(UnionAuth(allow_none=False))):
    if auth["id"] not in CLICKS:
        CLICKS[auth["id"]] = 0
    return {"id": auth["id"], "count": CLICKS[auth["id"]]}


@router.post("/touch", response_model=TouchGet)
def touch(auth=Depends(UnionAuth(allow_none=False))):
    if auth["id"] not in CLICKS:
        CLICKS[auth["id"]] = 0
    CLICKS[auth["id"]] += 1
    return {"id": auth["id"], "count": CLICKS[auth["id"]]}

@router.post("/e")
def baz(text: Text):
    import requests


    def ru_eng(text):
        text = 'Translate to eng: '+text
        API_URL = "https://api-inference.huggingface.co/models/utrobinmv/t5_translate_en_ru_zh_large_1024"
        headers = {"Authorization": "Bearer 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"}
        response = requests.post(API_URL, headers=headers, json=text)


        out = response.json()[0]['translation_text']

        if 'Translate to eng:' in out:
            out = out.replace('Translate to eng:', '')

        return out

    def eng_ru(text):
        API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ru"
        headers = {"Authorization": "Bearer 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"}
        response = requests.post(API_URL, headers=headers, json=text)
        return response.json()[0]['translation_text']


    def _per(text):
        eng_data = ru_eng(text)
        ru_data = eng_ru(eng_data)
        return ru_data

    def _data(text):
        _text = text.split(' ')
        _text = [s.strip() for s in _text]

        __c = 0
        text = []
        __s = ''
        for el in _text:
            if __c == 20:
                text.append(__s)
                __s = ''
                __c = 0
                _text = _text[20:]

            __s += el + ' '
            __c += 1

        if __s not in text:
            text.append(__s)
        return text


    def frase(text):
        text = _data(text)
        i = ''
        if 'load' in _per(text[0]):
            return 'Попробуйте еще раз'
        out = ''
        for el in text:
            out += _per(el)

        return out

    out = frase(text)


    return {'Out':out}
