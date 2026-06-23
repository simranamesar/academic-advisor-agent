# Academic Advisor — Multi-Agent System (terminal)

A small **orchestrator + specialist agents** system that answers student questions
from five SRH documents. No frontend — it runs in the terminal. Retrieval is
**BM25** (keyword search), so it works fully offline with no model downloads.

## What it does
An **orchestrator** reads your question, decides the intent, and routes it to one
specialist agent. Each agent calls a **tool** that retrieves grounded evidence from
the PDFs and answers with its sources cited.

```
you> How many ECTS is the internship?
[routed to: internship agent]
Regarding the internship:
The internship carries 30 ECTS ... 750–900 hours ...
Sources: Internship FAQs (p.2)
```

## Folder structure
```
academic_advisor/
├── main.py                  # terminal entry point (REPL + --demo)
├── requirements.txt
├── data/                    # the 5 source PDFs (swap in your own)
│   ├── module_handbook.pdf
│   ├── study_regulations.pdf
│   ├── internship_process.pdf
│   ├── internship_faqs.pdf
│   └── academic_calendar.pdf
└── advisor/
    ├── config.py            # document registry + chunking settings
    ├── document_store.py    # load PDFs, chunk, BM25 index, retrieval
    ├── tools.py             # search_module_handbook(), search_study_regulations(),
    │                        #   recommend_electives(), summarize_document(), ...
    ├── llm.py               # offline extractive summariser + optional LLM hook
    ├── orchestrator.py      # routes a query to the right agent
    └── agents/              # one file per agent
        ├── base.py
        ├── module_agent.py        -> search_module_handbook()
        ├── regulations_agent.py   -> search_study_regulations()
        ├── internship_agent.py    -> search_internship()
        ├── electives_agent.py     -> recommend_electives()
        ├── summary_agent.py       -> summarize_document()
        └── general_agent.py       -> search_all() (fallback, covers the calendar)
```

## Install & run
```bash
pip install -r requirements.txt
python main.py            # interactive
python main.py --demo     # run sample questions and exit
```

## The four core tools (in advisor/tools.py)
- `search_module_handbook(query)` — modules, ECTS, exam forms, curriculum.
- `search_study_regulations(query)` — grading, repeats, thesis, deadlines.
- `recommend_electives(interests)` — ranks handbook elective/track modules by your interests.
- `summarize_document(doc_key)` — extractive summary of any document.
(Plus `search_internship()` and `search_all()` so the internship docs and calendar are covered.)

## How routing works
`advisor/orchestrator.py` holds a keyword→intent table checked in order
(summary → electives → internship → regulations → calendar → module → general).
Calendar is checked before module so "lecture period / when does …" isn't swallowed
by the generic word "semester". Anything unmatched falls back to the general agent,
which searches all documents.

## Swapping BM25 for semantic search (optional)
BM25 matches keywords. To also catch synonyms, embed chunks with
`sentence-transformers` and rank by cosine similarity inside
`DocumentStore.search`. Keep BM25 as a fallback for exact terms (hybrid search).

## Turning on a real LLM (optional)
Answers are extractive by default. In `advisor/llm.py` set `USE_LLM = True` and
implement `_call_llm` (a flan-t5 snippet is included in the comments, or call an API).
Every agent then phrases its answer with the model while staying grounded in the
retrieved context.

## Adding documents
Drop a PDF in `data/`, add an entry to `DOCUMENTS` in `advisor/config.py`, and
(optionally) add keywords/a new agent. Everything else picks it up automatically.
