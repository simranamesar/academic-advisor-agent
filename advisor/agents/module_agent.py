"""Answers questions about modules, ECTS, exam forms, semesters."""
from .base import BaseAgent
from ..tools import search_module_handbook


class ModuleHandbookAgent(BaseAgent):
    name = "module_handbook"
    description = "modules, courses, ECTS, exam forms, curriculum structure"

    def handle(self, query):
        hits = search_module_handbook(query, k=3)
        return self._grounded_answer(query, hits, "From the module handbook:")
