# Header-Scanner

A command-line tool written in Python that audits the HTTP security headers of any website and grades each header based on configuration quality. Inspired by [securityheaders.com](https://securityheaders.com), built from scratch as a deep-dive learning project into web security and Python development.

## What it does

When a browser visits a website, the server sends back HTTP headers along with the page content. Some of these headers tell the browser to behave more defensively, preventing common attacks like clickjacking, cross-site scripting (XSS), protocol downgrade, and MIME-type sniffing.

The catch: even a perfectly secure backend is vulnerable if these headers are missing or misconfigured, because the vulnerability lives in the browser's behavior, not the server code.

This tool sends a request to any URL and:

- Reports whether each of the 6 main security headers is present
- Analyzes the **value** of each header and grades its configuration quality (A+ to F)
- Provides recommendations when headers are missing or weak
- Outputs a final score showing how the site performs overall

## Why this matters

This kind of analysis is part of the daily work of:

- **Penetration testers** auditing client websites
- **DevSecOps engineers** integrating automated security checks into CI/CD pipelines
- **Bug bounty hunters** scanning subdomains for low-hanging vulnerabilities

## Quick start

```bash
# Clone the repo
git clone https://github.com/GuiCoelhoRS/Header-Scanner.git
cd Header-Scanner

# Set up the virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the scanner against any URL
python scanner.py https://github.com
```

## Usage

The scanner accepts a URL as a command-line argument:

```bash
python scanner.py <url>
```

Show built-in help:

```bash
python scanner.py --help
```

### Examples

```bash
python scanner.py https://github.com
python scanner.py https://pypi.org
python scanner.py https://www.npmjs.com
```

## Example output

Running against GitHub:

```
=== Status Code ===
URL: https://github.com/
Status Code: 200
Total of received headers: 18
✅ Content-Security-Policy: default-src 'none'; base-uri 'self'; ...
   ↳ Grade: A — Strong script-src configuration
✅ Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
   ↳ Grade: A+ — Maximum protection (preload-eligible)
✅ X-Content-Type-Options: nosniff
   ↳ Grade: A — Correctly configured with 'nosniff'
✅ X-Frame-Options: deny
   ↳ Grade: A — It will never be loaded in an iframe
❌ Permissions-Policy: MISSING
✅ Referrer-Policy: origin-when-cross-origin, strict-origin-when-cross-origin
   ↳ Grade: C — Leaks path on same-origin requests
Report: This URL (https://github.com/) has 5 out of 6 security headers
```

## Project structure

```
Header-Scanner/
├── scanner.py          # main entry point — CLI parsing and orchestration
├── analyzers.py        # the 6 per-header analysis functions + dispatch dictionary
├── config.py           # constants (timeouts, header list, thresholds)
├── requirements.txt
├── README.md
└── .gitignore
```

The architecture follows the **separation of concerns** principle: configuration is isolated from logic, each analyzer is a pure function that can be tested independently, and the main loop dispatches to the right analyzer through a function dictionary — making the tool open for extension without modification.

## Headers analyzed

| Header | Purpose |
|---|---|
| `Content-Security-Policy` | Controls which sources of scripts, styles, and images can be loaded — primary defense against XSS |
| `Strict-Transport-Security` | Forces browsers to use HTTPS, preventing protocol downgrade attacks |
| `X-Content-Type-Options` | Prevents MIME-type sniffing attacks |
| `X-Frame-Options` | Prevents clickjacking by controlling iframe embedding |
| `Referrer-Policy` | Controls what referrer information is sent with outgoing requests |
| `Permissions-Policy` | Restricts access to browser APIs (camera, microphone, etc.) |

## Grading reference

Each header is graded based on the **quality** of its configured value, not just its presence. Letter grades follow the convention used by securityheaders.com and Mozilla Observatory.

### X-Content-Type-Options

| Value | Grade |
|---|---|
| `nosniff` | A |
| Anything else | F |

### X-Frame-Options

| Value | Grade |
|---|---|
| `DENY` | A |
| `SAMEORIGIN` | B |
| `ALLOW-FROM uri` | C (deprecated) |
| Multiple/duplicate values | F |
| Anything else | F |

### Referrer-Policy

| Value | Grade |
|---|---|
| `no-referrer` | A+ |
| `same-origin`, `strict-origin`, `strict-origin-when-cross-origin` | A |
| `no-referrer-when-downgrade`, `origin` | B |
| `origin-when-cross-origin` | C |
| `unsafe-url` | F |
| Anything else | F |

### Strict-Transport-Security

| Configuration | Grade |
|---|---|
| `max-age >= 1 year` + `includeSubDomains` + `preload` | A+ |
| `max-age >= 1 year` + `includeSubDomains` | A |
| `max-age >= 6 months` | A |
| `max-age >= 1 month` | B |
| `max-age < 1 month` | D |
| Missing `max-age` | F |

### Permissions-Policy

Grading is based on how many sensitive features are explicitly disabled (`feature=()`):

| Disabled count | Grade |
|---|---|
| 8 or more | A |
| 4 to 7 | B |
| 1 to 3 | C |
| 0 | D |

Sensitive features tracked: camera, microphone, geolocation, USB, serial, HID, bluetooth, payment, accelerometer, gyroscope, magnetometer, MIDI, display-capture.

### Content-Security-Policy

Grading focuses on the `script-src` directive (with `default-src` as fallback), since it's the most security-critical:

| Configuration | Grade |
|---|---|
| `'none'` (no scripts allowed) | A+ |
| Specific allowlist with no risky values | A |
| Contains `'unsafe-eval'` | B |
| Contains `'unsafe-inline'` | C |
| Contains both `'unsafe-inline'` and `'unsafe-eval'` | D |
| Contains `*` wildcard | D |
| No `script-src` or `default-src` defined | F |

## Architecture highlights

A few design choices worth noting:

- **Pure analyzer functions** — each `analyze_*` function takes a string and returns a `(grade, message)` tuple. No side effects. Easy to test in isolation.
- **Dispatch dictionary** — the main loop dispatches to the right analyzer via a `{header_name: function}` dictionary. Adding a new header requires no changes to the main loop, just registering the new function in the dictionary.
- **Defensive parsing** — handles real-world quirks like duplicated headers, missing components, invalid values, and case-insensitivity.
- **Layered error handling** — exceptions are caught from most specific (`Timeout`) to broadest (`RequestException`), with helpful messages at each layer.

## Roadmap

Completed:

- [x] HTTP request handling with proper error management
- [x] Detection of presence/absence for all 6 security headers
- [x] Quality analysis for all 6 security headers
- [x] Modular architecture (config / analyzers / scanner)
- [x] Function dispatch dictionary refactor
- [x] CLI support for URL input via argparse

Planned:

- [ ] `--timeout` and `--verbose` CLI options
- [ ] Support for batch scanning of multiple URLs
- [ ] JSON and HTML report output formats
- [ ] Unit tests with pytest
- [ ] Asynchronous requests for parallel scanning

## Tech stack

- **Python 3.12**
- **requests** — HTTP client library
- **argparse** — built-in CLI argument parsing

## License

MIT