"""The orchestrator: reads a query, decides which specialist agent should handle
it (rule-based intent routing), and delegates. This is the single entry point.
"""
from .agents import (ModuleHandbookAgent, RegulationsAgent, InternshipAgent,
                     ElectivesAgent, SummaryAgent, GeneralAgent)

# intent -> keywords that trigger it (checked in order)
ROUTES = [
    ("summary",     ["summarize", "summarise", "summary", "overview", "tldr", "brief"]),
    ("electives",   ["elective", "electives", "recommend", "specialization", "specialisation",
                     "which track", "choose a module", "interested in", "interest"]),
    ("internship",  ["internship", "intern", "placement", "werkstudent", "visa", "career service",
                     "company hours", "viva"]),
    ("regulations", ["regulation", "grading", "grade", "repeat", "fail", "deception", "plagiarism",
                     "attendance", "deadline", "thesis", "examination committee", "appeal", "ects rule",
                     "compensation", "leave of absence", "§"]),
    ("calendar",    ["calendar", "lecture period", "semester start", "holiday", "exam week",
                     "examination week", "orientation week", "non-lecture", "when does"]),
    ("module",      ["module", "handbook", "curriculum", "course", "ects", "semester", "exam form",
                     "credits", "syllabus", "prerequisite"]),
]


class Orchestrator:
    def __init__(self):
        self.agents = {
            "module":      ModuleHandbookAgent(),
            "regulations": RegulationsAgent(),
            "internship":  InternshipAgent(),
            "electives":   ElectivesAgent(),
            "summary":     SummaryAgent(),
            "general":     GeneralAgent(),
        }

    def route(self, query):
        q = query.lower()
        for intent, keywords in ROUTES:
            if any(kw in q for kw in keywords):
                # calendar questions are answered by the general (all-docs) search
                return "general" if intent == "calendar" else intent
        return "general"

    def handle(self, query, show_route=True):
        intent = self.route(query)
        agent = self.agents[intent]
        prefix = f"[routed to: {agent.name} agent]\n" if show_route else ""
        return prefix + agent.handle(query)
