"""
FORM ID: MATHTEXT_SUITE_V1
PURPOSE: Standalone parsing, indexing, and PDF compilation for math-rich documents.
DEPENDENCIES: reportlab (optional for direct PDF), standard library (json, re, html, http.server)
"""

import html
import json
import re
from typing import Any, Dict, List, Optional

# --- [1. PARSER ENGINE] ---


class MathToken:

    def __init__(self, kind: str, content: str, position: int):
        self.kind = kind  # 'text', 'inline_math', 'display_math'
        self.content = content
        self.position = position

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "content": self.content,
            "position": self.position,
        }


class MathTextParser:
    """Parses raw scientific texts into structured text and math node streams."""

    # Regex separates $$...$$, $...$, and regular sentences
    MATH_PATTERN = re.compile(
        r"(?P<display>\$\$(?:\\.|[^\$])+\$\$)|(?P<inline>\$(?:\\.|[^\$])+\$)",
        re.DOTALL,
    )

    @classmethod
    def parse_document(cls, text: str) -> List[MathToken]:
        tokens: List[MathToken] = []
        last_idx = 0

        for match in cls.MATH_PATTERN.finditer(text):
            start, end = match.span()
            if start > last_idx:
                raw_txt = text[last_idx:start]
                if raw_txt:
                    tokens.append(MathToken("text", raw_txt, last_idx))

            if match.group("display"):
                body = match.group("display")[2:-2].strip()
                tokens.append(MathToken("display_math", body, start))
            elif match.group("inline"):
                body = match.group("inline")[1:-1].strip()
                tokens.append(MathToken("inline_math", body, start))

            last_idx = end

        if last_idx < len(text):
            tokens.append(MathToken("text", text[last_idx:], last_idx))

        return tokens


# --- [2. SEARCHER & INDEXER] ---


class MathSearchIndex:
    """Inverted search engine identifying document IDs by math symbol, command, or token."""

    COMMAND_PATTERN = re.compile(r"\\[a-zA-Z]+")

    def __init__(self):
        self.docs: Dict[str, str] = {}
        self.symbol_index: Dict[str, set] = {}
        self.term_index: Dict[str, set] = {}

    def add_document(self, doc_id: str, content: str):
        self.docs[doc_id] = content
        tokens = MathTextParser.parse_document(content)

        for token in tokens:
            if "math" in token.kind:
                # Index math symbols/commands (\theta, \int, \frac, etc.)
                commands = self.COMMAND_PATTERN.findall(token.content)
                for cmd in commands:
                    self.symbol_index.setdefault(cmd.lower(), set()).add(doc_id)
            else:
                # Index words
                words = re.findall(r"\b\w{3,}\b", token.content.lower())
                for w in words:
                    self.term_index.setdefault(w, set()).add(doc_id)

    def search(self, query: str) -> List[Dict[str, Any]]:
        query = query.strip()
        matches = set()

        if query.startswith("\\"):
            matches = self.symbol_index.get(query.lower(), set())
        else:
            for term in query.lower().split():
                term_matches = self.term_index.get(term, set())
                matches = (
                    matches.intersection(term_matches)
                    if matches
                    else term_matches
                )

        return [
            {
                "doc_id": did,
                "preview": self.docs[did][:140] + "...",
                "tokens": [
                    t.to_dict()
                    for t in MathTextParser.parse_document(self.docs[did])
                ],
            }
            for did in matches
        ]


# --- [3. PDF BUILDER] ---


class MathPDFBuilder:
    """Exports math-annotated documents to printable PDF.

    Can compile directly via ReportLab Platypus or emit an HTML print-ready sheet.
    """

    @staticmethod
    def generate_html_print_bundle(
        doc_id: str, tokens: List[MathToken]
    ) -> str:
        """Returns standard HTML using KaTeX for instant client/headless print-to-PDF."""
        body_parts = []
        for t in tokens:
            if t.kind == "text":
                body_parts.append(
                    f"<span>{html.escape(t.content).replace(chr(10), '<br>')}</span>"
                )
            elif t.kind == "inline_math":
                body_parts.append(f"\\({t.content}\\)")
            elif t.kind == "display_math":
                body_parts.append(f"\\[{t.content}\\]")

        doc_html = "".join(body_parts)
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{doc_id}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
            onload="renderMathInElement(document.body);"></script>
    <style>
        @page {{ margin: 20mm; }}
        body {{ font-family: 'Times New Roman', serif; line-height: 1.6; font-size: 11pt; color: #111; }}
        .katex-display {{ margin: 1em 0; }}
    </style>
</head>
<body>
    <h1>{doc_id}</h1>
    <div>{doc_html}</div>
</body>
</html>"""

