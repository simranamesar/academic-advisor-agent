"""Base class shared by every specialist agent."""
from ..llm import answer as llm_answer


class BaseAgent:
    name = "base"
    description = "base agent"

    def _grounded_answer(self, query, hits, intro):
        """Build a readable answer from retrieved hits + cite sources."""
        if not hits:
            return f"{intro}\nI couldn't find anything relevant in the documents for that."
        context = "\n".join(h["text"] for h in hits)
        body = llm_answer(intro, context, query=query)
        sources = sorted({f"{h['source']} (p.{h['page']})" for h in hits})
        return f"{intro}\n\n{body}\n\nSources: " + "; ".join(sources)

    def handle(self, query):
        raise NotImplementedError
