import re
def clean_text(text:str)->str:
    text=re.sub(r"-\n", "",text)
    text=re.sub(r"\n{2,}", "\n",text)
    text=re.sub(r"[ \t]{2,}", " ",text)
    text=text.strip()
    return text
