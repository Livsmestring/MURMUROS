import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / 'tools' / 'mock_auth_server.py'
TOKEN = 'test-suite-token'


@pytest.fixture
def mock_server():
    env = {**os.environ, 'MOCK_AUTH_TOKEN': TOKEN}
    process = subprocess.Popen(
        [sys.executable, str(SERVER), '--port', '18080'],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    base_url = 'http://127.0.0.1:18080'
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            request_json(base_url + '/healthz')
            break
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.05)
    else:
        stdout, stderr = process.communicate(timeout=1)
        raise RuntimeError(f'mock server failed to start: {stdout} {stderr}')

    yield base_url
    process.terminate()
    process.wait(timeout=5)


def request_json(url, *, method='GET', payload=None, token=None):
    body = None if payload is None else json.dumps(payload).encode()
    headers = {'Content-Type': 'application/json'} if body else {}
    if token is not None:
        headers['Authorization'] = f'Bearer {token}'
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def test_health_endpoint_is_public(mock_server):
    status, payload = request_json(mock_server + '/healthz')
    assert (status, payload) == (200, {'status': 'ok'})


def test_protected_endpoint_rejects_missing_or_invalid_token(mock_server):
    assert request_json(mock_server + '/api/me')[0] == 401
    assert request_json(mock_server + '/api/me', token='wrong-token')[0] == 401


def test_protected_endpoint_accepts_test_token(mock_server):
    status, payload = request_json(mock_server + '/api/me', token=TOKEN)
    assert status == 200
    assert payload == {'id': 'test-user', 'role': 'tester'}


def test_event_endpoint_validates_payload_and_accepts_valid_event(mock_server):
    invalid_status, invalid_payload = request_json(
        mock_server + '/api/events', method='POST', payload={}, token=TOKEN
    )
    valid_status, valid_payload = request_json(
        mock_server + '/api/events',
        method='POST',
        payload={'event_type': 'PATTERN_DETECTED'},
        token=TOKEN,
    )
    assert (invalid_status, invalid_payload) == (422, {'error': 'event_type_required'})
    assert (valid_status, valid_payload) == (
        201,
        {'accepted': True, 'event_id': 'mock-event-001'},
    )
