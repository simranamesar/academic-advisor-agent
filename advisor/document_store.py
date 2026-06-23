"""Loads the PDFs once, splits them into overlapping chunks, and serves
keyword (BM25) retrieval. BM25 is used because it is fast, offline, and needs
no model downloads — ideal for a laptop.
"""
import re
from pypdf import PdfReader
from rank_bm25 import BM25Okapi
from .config import DOCUMENTS, CHUNK_SIZE, CHUNK_OVERLAP

STOPWORDS = set(
    "a an the is are was were be been being and or of to in on for with as it its this that "
    "what how when where which who do does did can could will would should i you he she they we "
    "at by from not no my our your their if then else than".split()
)

def tokenize(text):
    """Lowercase, keep word characters only (so 'thesis?' -> 'thesis'), drop stopwords."""
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS]


class Chunk:
    __slots__ = ("doc_key", "doc_label", "page", "text")
    def __init__(self, doc_key, doc_label, page, text):
        self.doc_key, self.doc_label, self.page, self.text = doc_key, doc_label, page, text


def _chunk_words(text, size, overlap):
    words = text.split()
    step = max(1, size - overlap)
    out = []
    for i in range(0, len(words), step):
        piece = " ".join(words[i:i + size]).strip()
        if piece:
            out.append(piece)
    return out


class DocumentStore:
    """Holds all chunks and a BM25 index per document plus a global index."""

    def __init__(self):
        self.chunks = []                 # list[Chunk]
        self._by_doc = {}                # doc_key -> list of chunk indices
        self._bm25_global = None
        self._bm25_by_doc = {}           # doc_key -> (BM25, [chunk indices])
        self._loaded = False

    # ---------- loading ----------
    def load(self):
        if self._loaded:
            return self
        for key, (path, label) in DOCUMENTS.items():
            if not path.exists():
                print(f"[warn] missing file for '{key}': {path}")
                continue
            reader = PdfReader(str(path))
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                for piece in _chunk_words(text, CHUNK_SIZE, CHUNK_OVERLAP):
                    self._by_doc.setdefault(key, []).append(len(self.chunks))
                    self.chunks.append(Chunk(key, label, page_num, piece))

        # build indexes
        self._bm25_global = BM25Okapi([tokenize(c.text) for c in self.chunks])
        for key, idxs in self._by_doc.items():
            self._bm25_by_doc[key] = (
                BM25Okapi([tokenize(self.chunks[i].text) for i in idxs]),
                idxs,
            )
        self._loaded = True
        return self

    # ---------- retrieval ----------
    def search(self, query, doc_key=None, k=3):
        """Return top-k Chunks. If doc_key is given, search only that document."""
        if not self._loaded:
            self.load()
        q = tokenize(query)
        if doc_key:
            bm25, idxs = self._bm25_by_doc[doc_key]
            scores = bm25.get_scores(q)
            order = sorted(range(len(idxs)), key=lambda j: scores[j], reverse=True)[:k]
            return [(self.chunks[idxs[j]], float(scores[j])) for j in order]
        # global
        scores = self._bm25_global.get_scores(q)
        order = sorted(range(len(self.chunks)), key=lambda j: scores[j], reverse=True)[:k]
        return [(self.chunks[j], float(scores[j])) for j in order]

    def full_text(self, doc_key):
        idxs = self._by_doc.get(doc_key, [])
        return " ".join(self.chunks[i].text for i in idxs)


# module-level singleton so the PDFs are parsed only once
_STORE = None
def get_store():
    global _STORE
    if _STORE is None:
        _STORE = DocumentStore().load()
    return _STORE
