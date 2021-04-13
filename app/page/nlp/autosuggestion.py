#import autocomplete
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fast_autocomplete import AutoComplete

with open("app/page/nlp/nlp.txt", "r") as f:
    text = f.readlines()
text = [i.strip() for i in text] + ["show " + i.strip() for i in text] + ["show me " + i.strip() for i in text]
words = {i: {} for i in text}
autocomplete = AutoComplete(words=words)


def autosuggestion(input_):
    try:
        word_suggestions = autocomplete.search(word=input_, max_cost=3, size=5)
        # print(word_suggestions_)
        # autocomplete.load()
        # word_suggestions = autocomplete.split_predict(input_, top_n=3)
        # word_suggestions = [i[0] for i in word_suggestions]
        data = {"word_suggestions": word_suggestions}
        return JSONResponse(jsonable_encoder(data), status_code=200)
    except Exception:
        return JSONResponse(jsonable_encoder({"word_suggestions": []}), status_code=200)
