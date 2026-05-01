# Header-Scanner

A command-line tool written in Python that audits the HTTP security headers of any website and grades each header based on configuration quality. Inspired by [securityheaders.com](https://securityheaders.com), but built from scratch as a deep-dive learning project into web security and Python development.

## What it does

When you visit a website, the server sends back HTTP headers along with the page content. Some of these headers tell your browser to behave more securely — preventing common attacks like clickjacking, cross-site scripting (XSS), protocol downgrade attacks, and MIME-type sniffing.

The catch: even a perfectly secure backend is vulnerable if these headers are missing or misconfigured, because the vulnerability lives in the browser's behavior, not the server code.

This tool sends a request to a URL and:

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

# Run the scanner
python scanner.py
```

The URL is currently set as a constant at the top of `scanner.py`. CLI argument support is on the roadmap.

## Example output

Running against PyPI:

```
=== Status Code ===
URL: https://pypi.org/
Status Code: 200
Total of received headers: 17
✅ Content-Security-Policy: default-src 'none'; script-src 'self' ...
   ↳ Grade: A — Strong script-src configuration
✅ Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   ↳ Grade: A+ — Maximum protection (preload-eligible)
✅ X-Content-Type-Options: nosniff
   ↳ Grade: A — Correctly configured with 'nosniff'
✅ X-Frame-Options: deny
   ↳ Grade: A — It will never be loaded in an iframe
✅ Permissions-Policy: accelerometer=(),autoplay=(),camera=(),...
   ↳ Grade: A — Strong defensive policy (10 sensitive features disabled)
✅ Referrer-Policy: origin-when-cross-origin
   ↳ Grade: C — Leaks path on same-origin requests
Report: This URL has 6 out of 6 Security Headers
```

## Project structure

```
Header-Scanner/
├── scanner.py          # main entry point — orchestrates the scan
├── analyzers.py        # the 6 per-header analysis functions
├── config.py           # constants (timeouts, header list, thresholds)
├── requirements.txt
├── README.md
└── .gitignore
```

The architecture follows the principle of **separation of concerns**: configuration is isolated from logic, and each analyzer is a pure function that can be tested independently.

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

## Roadmap

- [x] HTTP request handling with proper error management
- [x] Detection of presence/absence for all 6 security headers
- [x] Quality analysis for `X-Content-Type-Options`
- [x] Quality analysis for `X-Frame-Options`
- [x] Quality analysis for `Referrer-Policy`
- [x] Quality analysis for `Strict-Transport-Security`
- [x] Quality analysis for `Permissions-Policy`
- [x] Quality analysis for `Content-Security-Policy`
- [x] Modular architecture (config / analyzers / scanner)
- [ ] Refactor analyzer dispatch using a function dictionary
- [ ] Accept URL as a CLI argument (argparse)
- [ ] Support for batch scanning of multiple URLs
- [ ] JSON and HTML report output formats
- [ ] Unit tests with pytest
- [ ] Asynchronous requests for parallel scanning

## Tech stack

- **Python 3.12**
- **requests** — HTTP client library

## License

MIT
