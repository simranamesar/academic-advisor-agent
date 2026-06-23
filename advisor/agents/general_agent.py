"""Fallback agent: searches across all documents (covers the calendar and
anything that doesn't match a specialist)."""
from .base import BaseAgent
from ..tools import search_all


class GeneralAgent(BaseAgent):
    name = "general"
    description = "anything that doesn't fit a specialist (searches all documents)"

    def handle(self, query):
        hits = search_all(query, k=4)
        return self._grounded_answer(query, hits, "Searching all documents:")
