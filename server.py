"""
FORM ID: MATHTEXT_SERVER_V1
PURPOSE: Lightweight REST controller and static asset server for MathText suite.
DEPENDENCIES: Python standard library (http.server, json, urllib, pathlib)
"""

import json
import os
import sys
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Import the core engine
try:
    from mathtext_core import MathPDFBuilder, MathSearchIndex, MathTextParser
except ImportError:
    print(
        "ERROR: Ensure 'mathtext_core.py' is located in the same directory.",
        file=sys.stderr,
    )
    sys.exit(1)

HOST = "127.0.0.1"
PORT = 8080
STATIC_DIR = Path(__file__).resolve().parent

# Global in-memory indexer instance
INDEXER = MathSearchIndex()


class MathTextRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler exposing REST endpoints and serving the workspace."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    # -------------------------------------------------------------
    # Helper Utilities
    # -------------------------------------------------------------

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
        raw_data = self.rfile.read(content_length)
        return json.loads(raw_data.decode("utf-8"))

    # -------------------------------------------------------------
    # GET Handlers: Static Files & Search API
    # -------------------------------------------------------------

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Root redirect to index.html
        if path == "/":
            self.path = "/index.html"
            return super().do_GET()

        # API: Search inverted index
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

        # Fallback to serving static assets (HTML, CSS, JS)
        super().do_GET()

    # -------------------------------------------------------------
    # POST Handlers: Parsing, Document Indexing, and PDF Export
    # -------------------------------------------------------------

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

        # API: Parse document into AST tokens
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

        # API: Index document into inverted search engine
        if path == "/api/index":
            doc_id = body.get("doc_id", "untitled_doc")
            content = body.get("content", "")
            INDEXER.add_document(doc_id, content)
            self._send_json(
                {
                    "status": "indexed",
                    "doc_id": doc_id,
                    "indexed_symbols": len(INDEXER.symbol_index),
                    "indexed_terms": len(INDEXER.term_index),
                }
            )
            return

        # API: Generate export-ready KaTeX HTML/print bundle
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


def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MathTextRequestHandler)
    print(f"[*] MathText Studio initialized.")
    print(f"[*] Serving on http://{HOST}:{PORT}")
    print(f"[*] Endpoints active: /api/parse, /api/index, /api/search, /api/export")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()

