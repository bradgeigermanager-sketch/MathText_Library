"""
FORM ID: MATHTEXT_SERVER_V2
PURPOSE: Lightweight REST controller, auto-populating indexer, and document registry.
"""

import json
import os
import sys
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from corpus_seed import CORPUS
from mathtext_core import MathPDFBuilder, MathSearchIndex, MathTextParser

HOST = "127.0.0.1"
PORT = 8080
STATIC_DIR = Path(__file__).resolve().parent

INDEXER = MathSearchIndex()


def preload_corpus():
    """Ingests pre-packaged mathematical corpora into the inverted search index."""
    for doc_id, meta in CORPUS.items():
        INDEXER.add_document(doc_id, meta["content"])
    print(
        f"[*] Corpus loaded: {len(CORPUS)} documents indexed."
    )
    print(
        f"[*] Symbol index populated with {len(INDEXER.symbol_index)} unique LaTeX command keys."
    )


class MathTextRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def _send_json(
        self, data: dict, status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        return json.loads(self.rfile.read(content_length).decode("utf-8"))

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/":
            self.path = "/index.html"
            return super().do_GET()

        # Document Registry
        if path == "/api/documents":
            doc_list = [
                {
                    "id": k,
                    "title": v["title"],
                    "category": v["category"],
                }
                for k, v in CORPUS.items()
            ]
            self._send_json({"documents": doc_list})
            return

        # Fetch document content
        if path == "/api/load":
            query_params = parse_qs(parsed_url.query)
            doc_id = query_params.get("id", [""])[0]
            if doc_id in CORPUS:
                self._send_json(
                    {
                        "id": doc_id,
                        "title": CORPUS[doc_id]["title"],
                        "content": CORPUS[doc_id]["content"],
                    }
                )
            else:
                self._send_json(
                    {"error": "Document not found"},
                    HTTPStatus.NOT_FOUND,
                )
            return

        # Inverted index search
        if path == "/api/search":
            query_params = parse_qs(parsed_url.query)
            q = query_params.get("q", [""])[0].strip()
            if not q:
                self._send_json(
                    {"query": "", "count": 0, "results": []}
                )
                return

            results = INDEXER.search(q)
            self._send_json(
                {"query": q, "count": len(results), "results": results}
            )
            return

        super().do_GET()

    def do_POST(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        try:
            body = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json(
                {"error": "Malformed JSON payload"},
                HTTPStatus.BAD_REQUEST,
            )
            return

        if path == "/api/parse":
            content = body.get("content", "")
            tokens = MathTextParser.parse_document(content)
            self._send_json(
                {
                    "token_count": len(tokens),
                    "tokens": [t.to_dict() for t in tokens],
                }
            )
            return

        if path == "/api/index":
            doc_id = body.get("doc_id", "untitled")
            content = body.get("content", "")
            title = body.get("title", doc_id)
            category = body.get("category", "Custom")

            # Update corpus cache and indexer
            CORPUS[doc_id] = {
                "title": title,
                "category": category,
                "content": content,
            }
            INDEXER.add_document(doc_id, content)

            self._send_json(
                {
                    "status": "indexed",
                    "doc_id": doc_id,
                    "indexed_symbols": len(INDEXER.symbol_index),
                }
            )
            return

        if path == "/api/export":
            doc_id = body.get("doc_id", "MathText_Export")
            content = body.get("content", "")
            tokens = MathTextParser.parse_document(content)
            html_bundle = MathPDFBuilder.generate_html_print_bundle(
                doc_id, tokens
            )
            payload = html_bundle.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        self._send_json(
            {"error": "Endpoint not found"}, HTTPStatus.NOT_FOUND
        )


def run():
    preload_corpus()
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MathTextRequestHandler)
    print(f"[*] Serving MathText Studio at http://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    run()
    
