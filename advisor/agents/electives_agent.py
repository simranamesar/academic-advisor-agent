"""Recommends elective / track modules based on the student's interests."""
from .base import BaseAgent
from ..tools import recommend_electives


class ElectivesAgent(BaseAgent):
    name = "electives"
    description = "recommend elective or track modules based on interests"

    def handle(self, query):
        recs = recommend_electives(query, k=5)
        if not recs:
            return "I couldn't find matching electives for that interest."
        lines = ["Based on your interests, these handbook modules look relevant:"]
        for i, r in enumerate(recs, 1):
            snippet = r["text"][:160].rsplit(" ", 1)[0]
            lines.append(f"  {i}. {snippet}…  ({r['source']}, p.{r['page']})")
        lines.append("\nCheck the handbook for the full module description and prerequisites.")
        return "\n".join(lines)
