"""Optional language-model layer.

By default the advisor runs fully offline using a small extractive summariser
(no downloads, no GPU). To get nicer phrasing, set USE_LLM = True and fill in
`_call_llm` with a real model or API.
"""
import re
from .document_store import tokenize

USE_LLM = False   # flip to True after wiring up _call_llm below


def _call_llm(prompt: str) -> str:
    """Plug a real model in here, e.g.:

        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        tok = AutoTokenizer.from_pretrained("google/flan-t5-base")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        ids = tok(prompt, return_tensors="pt", truncation=True, max_length=512)
        out = model.generate(**ids, max_new_tokens=160)
        return tok.decode(out[0], skip_special_tokens=True)

    or an API call. Return a plain string.
    """
    raise NotImplementedError


def _split_sentences(text):
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+|•|\u2022", text)
    return [p.strip() for p in parts if len(p.strip()) > 25]


def extractive_summary(text, query=None, n=4):
    """Pick the n most relevant sentences. If a query is given, rank by overlap
    with the query; otherwise rank by overall keyword frequency (centrality)."""
    sents = _split_sentences(text)
    if not sents:
        return text[:400]
    if query:
        qw = set(tokenize(query))
        scored = sorted(sents, key=lambda s: sum(w in qw for w in tokenize(s)), reverse=True)
    else:
        from collections import Counter
        freq = Counter(w for s in sents for w in tokenize(s))
        scored = sorted(sents, key=lambda s: sum(freq[w] for w in tokenize(s)) / (len(tokenize(s)) + 1),
                        reverse=True)
    top = scored[:n]
    # keep original order for readability
    top_in_order = [s for s in sents if s in top]
    return " ".join(top_in_order)


def answer(prompt: str, context: str, query: str = None) -> str:
    """Used by agents to phrase a final answer from retrieved context."""
    if USE_LLM:
        full = f"{prompt}\n\nContext:\n{context}\n\nAnswer concisely:"
        return _call_llm(full)
    return extractive_summary(context, query=query, n=4)
