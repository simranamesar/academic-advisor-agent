"""Answers questions about examination regulations: grading, repeats, thesis, deadlines."""
from .base import BaseAgent
from ..tools import search_study_regulations


class RegulationsAgent(BaseAgent):
    name = "regulations"
    description = "exam rules, grading scale, repeats, thesis, deadlines, attendance"

    def handle(self, query):
        hits = search_study_regulations(query, k=3)
        return self._grounded_answer(query, hits, "According to the examination regulations:")
