"""Central configuration: where the documents live and how they are labelled.

To use your own files, drop them in ./data and update the paths below.
"""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# key -> (file path, human-readable label)
DOCUMENTS = {
    "module_handbook":    (DATA_DIR / "module_handbook.pdf",    "Module Handbook (ADSAI Curriculum)"),
    "study_regulations":  (DATA_DIR / "study_regulations.pdf",  "General Examination Regulations"),
    "internship_process": (DATA_DIR / "internship_process.pdf", "Internship Process"),
    "internship_faqs":    (DATA_DIR / "internship_faqs.pdf",    "Internship FAQs"),
    "academic_calendar":  (DATA_DIR / "academic_calendar.pdf",  "Academic Calendar"),
}

# Retrieval settings
CHUNK_SIZE = 120     # words per chunk
CHUNK_OVERLAP = 30   # words shared between consecutive chunks
