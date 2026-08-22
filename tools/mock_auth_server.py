#!/usr/bin/env python3
"""Small, local-only mock authentication API for integration tests.

The server intentionally implements only the contract needed by local tests:
- GET /healthz -> liveness without authentication
- GET /api/me -> authenticated user response
- POST /api/events -> authenticated event acceptance

It binds to 127.0.0.1 by default and never logs Authorization headers.
"""

from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

DEFAULT_TOKEN = 'local-test-token'


class MockAuthHandler(BaseHTTPRequestHandler):
    server_version = 'MURMUROS-MockAuth/1.0'

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        expected = self.server.auth_token  # type: ignore[attr-defined]
        supplied = self.headers.get('Authorization', '')
        return supplied == f'Bearer {expected}'

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path == '/healthz':
            self._json(200, {'status': 'ok'})
            return
        if self.path == '/api/me':
            if not self._authorized():
                self._json(401, {'error': 'unauthorized'})
                return
            self._json(200, {'id': 'test-user', 'role': 'tester'})
            return
        self._json(404, {'error': 'not_found'})

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path != '/api/events':
            self._json(404, {'error': 'not_found'})
            return
        if not self._authorized():
            self._json(401, {'error': 'unauthorized'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self._json(400, {'error': 'invalid_json'})
            return
        if not isinstance(payload, dict) or not payload.get('event_type'):
            self._json(422, {'error': 'event_type_required'})
            return
        self._json(201, {'accepted': True, 'event_id': 'mock-event-001'})

    def log_message(self, format: str, *args: object) -> None:
        # Do not log request headers or bodies; keep local output deterministic.
        print(f'[mock-auth] {self.address_string()} - {format % args}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    token = os.environ.get('MOCK_AUTH_TOKEN', DEFAULT_TOKEN)
    server = ThreadingHTTPServer((args.host, args.port), MockAuthHandler)
    server.auth_token = token  # type: ignore[attr-defined]
    print(f'[mock-auth] listening on http://{args.host}:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
