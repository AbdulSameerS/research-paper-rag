import re

SECTION_KEYWORDS = {
    "abstract": "Abstract",
    "introduction": "Introduction",
    "background": "Background",
    "related work": "Related Work",
    "method": "Methods",
    "methods": "Methods",
    "methodology": "Methods",
    "approach": "Methods",
    "experiment": "Experiments",
    "experiments": "Experiments",
    "evaluation": "Evaluation",
    "result": "Results",
    "results": "Results",
    "discussion": "Discussion",
    "conclusion": "Conclusion",
    "references": "References",
}


def normalize_line(line: str) -> str:
    line = line.strip().lower()
    line = re.sub(r"\s+", " ", line)
    return line


def detect_section_from_text(text: str) -> str:
    lines = text.splitlines()

    for line in lines:
        cleaned = normalize_line(line)
        cleaned = re.sub(r"^\d+(\.\d+)*\s+", "", cleaned)

        for keyword, section_name in SECTION_KEYWORDS.items():
            if cleaned == keyword:
                return section_name

    return "Unknown"