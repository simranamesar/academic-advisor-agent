"""Summarises a whole document (e.g. 'summarise the internship process')."""
from .base import BaseAgent
from ..tools import summarize_document
from ..config import DOCUMENTS

# map keywords in the request to a document key
_KEYS = {
    "module_handbook":    ["handbook", "curriculum", "module", "course"],
    "study_regulations":  ["regulation", "exam", "grading", "thesis rule"],
    "internship_process": ["internship process", "internship steps", "internship procedure"],
    "internship_faqs":    ["faq", "frequently asked"],
    "academic_calendar":  ["calendar", "semester dates", "lecture period", "holiday"],
}


class SummaryAgent(BaseAgent):
    name = "summary"
    description = "summarise one of the documents"

    def _pick_doc(self, query):
        q = query.lower()
        for key, words in _KEYS.items():
            if any(w in q for w in words):
                return key
        return "module_handbook"  # sensible default

    def handle(self, query):
        key = self._pick_doc(query)
        label = DOCUMENTS[key][1]
        summary = summarize_document(key, query=query, n=5)
        return f"Summary of {label}:\n\n{summary}"
