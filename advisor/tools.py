"""The tools the agents call. Each returns retrieved evidence (text + source)
so answers stay grounded in the documents.
"""
from .document_store import get_store
from .llm import extractive_summary


def _format(hits):
    """Turn (Chunk, score) hits into a list of dicts with source info."""
    return [
        {"text": c.text, "source": c.doc_label, "page": c.page, "score": round(s, 3)}
        for c, s in hits if s > 0
    ]


def search_module_handbook(query, k=3):
    """Search the module handbook / curriculum for modules, ECTS, exam forms, etc."""
    return _format(get_store().search(query, doc_key="module_handbook", k=k))


def search_study_regulations(query, k=3):
    """Search the General Examination Regulations (grading, repeats, thesis, deadlines...)."""
    return _format(get_store().search(query, doc_key="study_regulations", k=k))


def search_internship(query, k=3):
    """Search the internship process + FAQ documents together (ECTS, approval, visa, etc.)."""
    store = get_store()
    hits = store.search(query, doc_key="internship_process", k=k) \
         + store.search(query, doc_key="internship_faqs", k=k)
    hits.sort(key=lambda x: x[1], reverse=True)
    return _format(hits[:k])


def search_all(query, k=4):
    """Search across every document (used for the calendar and general questions)."""
    return _format(get_store().search(query, k=k))


def recommend_electives(interests, k=5):
    """Recommend elective / track modules from the handbook matching the student's
    interests. `interests` is free text, e.g. 'NLP and generative AI'."""
    query = f"elective track specialization module {interests}"
    hits = get_store().search(query, doc_key="module_handbook", k=k * 4)
    # prefer chunks that look like real module rows (mention ECTS)
    hits = sorted(hits, key=lambda h: (("ects" in h[0].text.lower()), h[1]), reverse=True)
    picked, seen = [], set()
    for c, s in hits:
        if s <= 0:
            continue
        snippet = c.text.strip()
        key = snippet[:60]
        if key in seen:
            continue
        seen.add(key)
        picked.append({"text": snippet, "source": c.doc_label, "page": c.page, "score": round(s, 3)})
        if len(picked) >= k:
            break
    return picked


def summarize_document(doc_key, query=None, n=5):
    """Return an extractive summary of one document (optionally focused by query)."""
    store = get_store()
    text = store.full_text(doc_key)
    if not text:
        return f"(no document found for key '{doc_key}')"
    return extractive_summary(text, query=query, n=n)
