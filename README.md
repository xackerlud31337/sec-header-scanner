# Header Scanner

A command-line tool that takes a list of URLs, requests each one, and checks the HTTP response headers for common security problems. It saves the findings to `report.json`.

## Usage

```
python project.py urls.txt
```

`urls.txt` contains one URL per line:

```
https://example.com
https://xackerlud.com
```

## Output

For every URL, `report.json` contains:

```json
{
    "url": "https://example.com",
    "status": 200,
    "headers": {"Server": "Apache/2.4.29", "Content-Type": "text/html"},
    "missing": ["Content-Security-Policy", "Strict-Transport-Security"],
    "leaks": ["Server: Apache/2.4.29"]
}
```

| Field | Meaning |
|---|---|
| `url` | The URL that was scanned |
| `status` | The HTTP status code (200 = OK, 301/302 = redirect, 404 = not found, 500 = server error) |
| `headers` | All response headers the server returned |
| `missing` | Security headers the site should send but doesn't |
| `leaks` | Headers that reveal information about the server's software |

## What it means if a header is in `missing`

These headers tell the browser how to protect the user. If one is missing, the browser falls back to less safe default behaviour.

| Header | What it does | Risk if missing |
|---|---|---|
| `Content-Security-Policy` | Tells the browser which sources scripts, styles and images may load from | Cross-site scripting (XSS) is much easier to exploit, because injected scripts are allowed to run |
| `Strict-Transport-Security` | Forces the browser to only use HTTPS for this site | An attacker on the same network can downgrade the user to plain HTTP and read or change the traffic |
| `X-Frame-Options` | Controls whether the page may be shown inside an `<iframe>` on another site | Clickjacking: an attacker hides the page in an invisible frame and tricks the user into clicking buttons on it |
| `X-Content-Type-Options` | With the value `nosniff`, stops the browser from guessing a file's type | The browser may treat an uploaded file (e.g. an "image") as a script and run it |

## What it means if a header is in `leaks`

These headers are not dangerous by themselves, but they tell an attacker what software the server runs. If a version number is included, an attacker can look up known vulnerabilities (CVEs) for exactly that version.

| Header | Example | What it reveals |
|---|---|---|
| `Server` | `Server: Apache/2.4.29 (Ubuntu)` | The web server software, version and sometimes the operating system |
| `X-Powered-By` | `X-Powered-By: PHP/7.2.24` | The backend language or framework and its version |

A value without a version number (e.g. `Server: nginx` or `Server: cloudflare`) is much less useful to an attacker than one with a version.

## What it does not flag

`X-XSS-Protection: 0` is **not** reported as a problem. That header controlled an old XSS filter that modern browsers have removed, and current security guidance recommends setting it to `0` or leaving it out. Real XSS protection comes from `Content-Security-Policy`.

## Limitations

Missing or leaking headers are signs of weak configuration, not proven vulnerabilities. They show where to look more closely. Most bug bounty programs do not accept missing headers alone as a valid report.

Only scan websites you own or have permission to test.

## Files

- `project.py`: the main program, with `main()`, `fetch()` and `check_headers()`
- `test_project.py`: pytest tests for `check_headers()` (run with `pytest`)
- `requirements.txt`: the libraries needed (`requests`)
