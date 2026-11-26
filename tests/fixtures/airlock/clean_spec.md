# Clean Spec Negative Fixture

> **Airlock Notice:** Process aid only — not legal advice.

- **Contact placeholder:** `qa@example.com`
- **Status byte mask:** `0x0f`

## 1. API Shape

```http
GET /api/timer/status HTTP/1.1
```

```json
{
  "state": "paused",
  "remaining_ms": 42000
}
```

| Test ID | Obligation | Input | Expected Outcome |
| --- | --- | --- | --- |
| `test_01` | `obl_timer_01` | `GET /api/timer/status` | HTTP `200` |
