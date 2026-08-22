# Lokal mock-auth for MURMUROS

`tools/mock_auth_server.py` er en dependency-fri, lokal HTTP-server for å teste autentiseringsflyt uten ekstern API. Den binder til `127.0.0.1` som standard, bruker et eksplisitt testtoken og logger aldri `Authorization`-header eller request-body.

## Endepunkter

| Metode | Path | Auth | Forventet respons |
|---|---|---|---|
| GET | `/healthz` | Nei | `200 {"status":"ok"}` |
| GET | `/api/me` | Bearer-token | `200` for gyldig token, `401` ellers |
| POST | `/api/events` | Bearer-token | `201` for gyldig `event_type`, `422` ellers |

## Kjør lokalt

```bash
export MOCK_AUTH_TOKEN='local-test-token'
python tools/mock_auth_server.py --host 127.0.0.1 --port 8080
```

Serveren kan testes fra en annen terminal:

```bash
curl -fsS http://127.0.0.1:8080/healthz
curl -i http://127.0.0.1:8080/api/me
curl -fsS -H 'Authorization: Bearer local-test-token' \
  http://127.0.0.1:8080/api/me
curl -fsS -X POST \
  -H 'Authorization: Bearer local-test-token' \
  -H 'Content-Type: application/json' \
  -d '{"event_type":"PATTERN_DETECTED"}' \
  http://127.0.0.1:8080/api/events
```

## Kjør testene

```bash
python -m pytest -q tests/test_mock_auth_server.py
```

Testene starter og stopper serveren automatisk, verifiserer health-endepunktet, avviser manglende og feil token, aksepterer gyldig token og tester payload-validering.

## Bruk med Act

For Act er den enkleste og sikreste varianten å starte mock-serveren i samme workflow-jobb/container som klienttesten:

```yaml
- name: Start local mock auth
  shell: bash
  env:
    MOCK_AUTH_TOKEN: local-test-token
  run: |
    set -euo pipefail
    python tools/mock_auth_server.py --host 127.0.0.1 --port 8080 >/tmp/mock-auth.log 2>&1 &
    echo $! >/tmp/mock-auth.pid
    for _ in $(seq 1 50); do
      curl -fsS http://127.0.0.1:8080/healthz >/dev/null && break
      sleep 0.1
    done
    curl -fsS http://127.0.0.1:8080/healthz >/dev/null

- name: Run authenticated integration test
  shell: bash
  env:
    AUTH_BASE_URL: http://127.0.0.1:8080
    API_KEY: local-test-token
  run: python -m pytest -q tests/integration

- name: Stop local mock auth
  if: always()
  shell: bash
  run: |
    if [ -f /tmp/mock-auth.pid ]; then
      kill "$(cat /tmp/mock-auth.pid)" 2>/dev/null || true
    fi
```

Hvis testen kjøres i en separat container, bruk et felles Docker-nettverk eller service-container med et fast tjenestenavn. Ikke bind mock-serveren til `0.0.0.0` med mindre nettverkseksponering er tilsiktet og brannmuren er kontrollert.

## Sikkerhetsregler

Bruk kun dummy-data og deterministiske testresponser. Ikke legg ekte tokens i `act.secrets`, logger, fixtures eller commit-historikk. Hold mock-serveren lokal, ikke implementer ekte passordlagring, og ikke la testen sende persondata eller produksjonsdata til den.
