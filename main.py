"""Terminal entry point for the Academic Advisor multi-agent system.

Usage:
    python main.py            # interactive Q&A loop
    python main.py --demo     # run a few sample questions and exit
"""
import sys
from advisor import Orchestrator


DEMO_QUESTIONS = [
    "How many ECTS is the internship and how many company hours are required?",
    "What grade do I need to pass a module and how many times can I repeat it?",
    "I'm interested in NLP and generative AI — which electives should I take?",
    "Can I do my internship abroad?",
    "When does the lecture period start in winter semester 25/26?",
    "Summarize the internship process.",
]


def run_demo(bot):
    for q in DEMO_QUESTIONS:
        print("=" * 80)
        print("Q:", q)
        print("-" * 80)
        print(bot.handle(q))
        print()


def repl(bot):
    print("Academic Advisor — ask about modules, regulations, internship, electives, calendar.")
    print("Type 'quit' or 'exit' to leave.\n")
    while True:
        try:
            q = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if q.lower() in {"quit", "exit", "q"}:
            break
        if not q:
            continue
        print(bot.handle(q), "\n")


def main():
    print("Loading documents (parsing PDFs once)...")
    bot = Orchestrator()
    bot.handle("warmup", show_route=False)  # triggers document load
    if "--demo" in sys.argv:
        run_demo(bot)
    else:
        repl(bot)


if __name__ == "__main__":
    main()
