"""Per-header security analysis functions."""

from config import (
    ONE_YEAR_IN_SECONDS,
    SIX_MONTHS_IN_SECONDS,
    ONE_MONTH_IN_SECONDS,
    SENSITIVE_FEATURES,
)



# ============= Function to analyze the Security Header X-Content-Type-Options =============
# This header helps us avoid MIME Type Sniffing
def analyze_x_content_type_options(value):
    normalized = value.strip().lower()
    if normalized == "nosniff":
        return "A", "Correctly configured with 'nosniff'"
    else :
        return "F", "Invalid value. Should be 'nosniff'"
    



# ============= Function to analyze the Security Header X-Frame-Options =============
#
def analyze_x_frame_options(value):
    # To catch duplicate headers it happened when I was testing so I added this case
    if "," in value:
        return "F", f"Multiple/duplicate values detected: {value}"
    
    normalized = value.strip().lower()

    if normalized == "deny":
        return "A","It will never be loaded in an iframe"
    elif normalized == "sameorigin":
        return "B","It has to be an iframe from the same origin"
    elif normalized.startswith("allow-from"):
        return "C","Deprecated, ignored by modern browsers"
    else :
        return "F","Invalid value. Should be DENY or SAMEORIGIN"
    




# ============= Function to analyse the Security Header Referrer-Policy =============
# This header controls the information that is send when we click on a link to other website
def analyze_referrer_policy(value):
    if "," in value:
        value = value.split(",")[0]

    normalized = value.strip().lower()

    if normalized == "no-referrer":
        return "A+","Never sends a referrer"
    elif normalized in ("same-origin","strict-origin","strict-origin-when-cross-origin"):
        return "A", "Strong privacy protection"
    elif normalized == "no-referrer-when-downgrade":
        return "B", "Default for older browsers"
    elif normalized == "origin":
        return "B", "Always sends the origin"
    elif normalized == "origin-when-cross-origin":
        return "C","Leaks path on same-origin requests"
    elif normalized == "unsafe-url":
        return "F","Privacy risk — leaks full URL even on HTTPS to HTTP"
    else :
        return "F", f"Invalid or unknown value: {value}"
    



# ============= Function to analyse the Security Header Strict_Transport_Security =============
# Normal Structure : Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# 
def analyze_strict_transport_security(value):
    has_includeSubDomains = False
    has_preload = False
    max_age = None
    
    parts = value.split(";")
    for part in parts:
        normalized = part.strip().lower()

        if normalized == "includesubdomains":
            has_includeSubDomains = True
        elif normalized == "preload":
            has_preload = True
        elif normalized.startswith("max-age="):
            try:
                num_str = normalized.split("=")[1].strip()
                max_age = int(num_str)
            except(ValueError,IndexError):
                pass

    if max_age is None:
        return "F","Missing or Invalid Max-Age"
    elif max_age >= ONE_YEAR_IN_SECONDS and has_includeSubDomains and has_preload:
        return "A+", "Maximum protection (preload-eligible)"
    elif max_age >= ONE_YEAR_IN_SECONDS and has_includeSubDomains:
        return "A", "Strong; subdomains protected"
    elif max_age >= SIX_MONTHS_IN_SECONDS :
        return "A", "Acceptable strong configuration"
    elif max_age >= ONE_MONTH_IN_SECONDS:
        return "B", "OK but max-age could be longer"
    return "D", "max-age too short to be effective"




# ============= Function to analyse the Security Header Permissions-Policy =============
# Structure of the Value : Permissions-Policy: camera=(), microphone=(), geolocation=(self)
# This header lets a site say "I don't need to access to X,Y browser APIs - disable them" so even if someone attacks the website calls to those APIs will fail

def analyze_permissions_policy(value):
    parts = value.split(",")
    count_disabled_features = 0

    for part in parts:
        part = part.strip()
        if "=" not in part: # Skip problematic parts of the header
            continue

        feature,allowlist = part.split("=",1)
        feature = feature.strip().lower()
        allowlist = allowlist.strip()

        if feature in SENSITIVE_FEATURES and allowlist == "()":
            count_disabled_features += 1
        
    if count_disabled_features >= 8:
        return "A", f"Strong defensive policy ({count_disabled_features} sensitive features disabled)"
    if count_disabled_features >= 4:
         return "B", f"Some defense-in-depth ({count_disabled_features} sensitive features disabled)"
    if count_disabled_features >= 1:
        return "C", f"Limited protection ({count_disabled_features} sensitive features disabled)"
    return "D", "Header present but very permissive — no sensitive features disabled"





# ============= Function to analyse the Security Header Content-Security-Policy =============
# CSP is a list of different components and it needs a more advanced parsing model
def analyze_content_security_policy(value):
    # Parsing ===
    # Example of script.src : script-src 'self' github.githubassets.com;
    directives = {}

    for directive_str in value.split(";"):
        directive_str = directive_str.strip()
        
        if not directive_str:
            continue

        parts = directive_str.split()
        if not parts:
            continue

        name = parts[0].lower()
        sources = parts[1:]

        directives[name] = sources

    if "script-src" in directives:
        script_sources = directives["script-src"]
    elif "default-src" in directives:
        script_sources = directives["default-src"]
    else:
        return "F", "No script-src or default-src defined"
    

    # Check for risky values
    has_none = "'none'" in script_sources
    has_wildcard = "*" in script_sources
    has_unsafe_inline = "'unsafe-inline'" in script_sources
    has_unsafe_eval = "'unsafe-eval'" in script_sources

    if has_none:
        return "A+", "Strict CSP — no scripts allowed"
    
    if has_wildcard:
        return "D", "script-src contains wildcard '*' — allows any script source"
    
    if has_unsafe_inline and has_unsafe_eval:
        return "D", "script-src contains both 'unsafe-inline' and 'unsafe-eval'"
    
    if has_unsafe_inline:
        return "C", "script-src contains 'unsafe-inline' — weakens XSS defense"
    
    if has_unsafe_eval:
        return "B", "script-src contains 'unsafe-eval'"
    
    return "A", "Strong script-src configuration"
