# Header-Scanner

A command-line tool written in Python that looks at the HTTP security headers of any website and grades each one based on configuration quality.

Built as a learning project with the help of Claude (To Guide not to do full coding but with helpful tips and documentation so I could read the stuff I needed to use) to explore real-world web security, HTTP, and Python development.

## What it does

When you visit a website, the server sends back HTTP headers along with the page content. Some of these headers tell your browser to behave more securely — preventing common attacks like clickjacking, cross-site scripting (XSS), and protocol downgrade attacks.

The catch: even a perfectly secure backend is vulnerable if these headers are missing or misconfigured, because the vulnerability lives in the browser's behavior, not the server code.

This tool sends a request to a URL and:

- Reports whether each of the 6 main security headers is present
- Analyzes the value of each header and grades its configuration quality
- Provides recommendations when headers are missing or weak
- Outputs a final score showing how the site performs overall

## Why this matters

This kind of analysis is part of the daily work of:

- **Penetration testers** auditing client websites
- **DevSecOps engineers** integrating automated security checks into CI/CD pipelines
- **Bug bounty hunters** scanning large numbers of subdomains for low-hanging vulnerabilities

A reference implementation that does this professionally is [securityheaders.com](https://securityheaders.com).

## Headers analyzed

The tool currently audits these six security headers:

| Header | Purpose |
|---|---|
| `Content-Security-Policy` | Controls which sources of scripts, styles, and images can be loaded |
| `Strict-Transport-Security` | Forces browsers to use HTTPS, preventing downgrade attacks |
| `X-Content-Type-Options` | Prevents MIME-type sniffing attacks |
| `X-Frame-Options` | Prevents clickjacking by controlling iframe embedding |
| `Referrer-Policy` | Controls what referrer information is sent with outgoing requests |
| `Permissions-Policy` | Restricts access to browser APIs (camera, microphone, etc.) |

## Grading reference

Each header is graded based on the quality of its configured value, not just its presence.

### X-Content-Type-Options

| Value | Grade | Note |
|---|---|---|
| `nosniff` | A | Correctly configured |
| Anything else | F | Invalid value |

### X-Frame-Options

| Value | Grade | Note |
|---|---|---|
| `DENY` | A | Strictest setting — cannot be framed |
| `SAMEORIGIN` | B | Acceptable — same-origin only |
| `ALLOW-FROM uri` | C | Deprecated, ignored by modern browsers |
| Multiple/duplicate values | F | Inconsistent server configuration |
| Anything else | F | Invalid value |

### Referrer-Policy

| Value | Grade | Note |
|---|---|---|
| `no-referrer` | A+ | Never sends referrer information |
| `same-origin` | A | Sends referrer only to same origin |
| `strict-origin` | A | Sends only origin, only on HTTPS to HTTPS |
| `strict-origin-when-cross-origin` | A | Modern recommended default |
| `no-referrer-when-downgrade` | B | Old browser default |
| `origin` | B | Always sends only the origin |
| `origin-when-cross-origin` | C | Leaks path on same-origin requests |
| `unsafe-url` | F | Leaks full URL — privacy risk |
| Anything else | F | Invalid or unknown value |

### Strict-Transport-Security (planned)

| Configuration | Grade | Note |
|---|---|---|
| `max-age >= 1 year` + `includeSubDomains` + `preload` | A+ | Maximum protection |
| `max-age >= 6 months` | A | Strong |
| `max-age >= 1 month` | B | Acceptable |
| `max-age < 1 month` | D | Too short to be effective |
| Missing `max-age` | F | Invalid |

### Content-Security-Policy (planned)

Graded based on directive completeness and avoidance of risky values like `unsafe-inline` and `unsafe-eval`.

### Permissions-Policy (planned)

Graded based on which browser APIs are explicitly disabled when not needed.

## How to use

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

## Roadmap

- [x] HTTP request handling with proper error management
- [x] Detection of presence/absence for all 6 security headers
- [x] Quality analysis for `X-Content-Type-Options`
- [x] Quality analysis for `X-Frame-Options`
- [ ] Quality analysis for `Referrer-Policy`
- [ ] Quality analysis for `Strict-Transport-Security`
- [ ] Quality analysis for `Permissions-Policy`
- [ ] Quality analysis for `Content-Security-Policy`
- ...

## Tech stack

- **Python 3.12**
- **requests** — HTTP client library

## License

MIT