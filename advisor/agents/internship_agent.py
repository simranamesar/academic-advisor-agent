"""Answers internship questions using both the process doc and the FAQ."""
from .base import BaseAgent
from ..tools import search_internship


class InternshipAgent(BaseAgent):
    name = "internship"
    description = "internship semester, ECTS, approval steps, visa, Werkstudent, thesis overlap"

    def handle(self, query):
        hits = search_internship(query, k=4)
        return self._grounded_answer(query, hits, "Regarding the internship:")
