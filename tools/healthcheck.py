#!/usr/bin/env python3
"""Check that the published archive is up and correct. Exits 1 if any check fails.

  python3 healthcheck.py https://archive.example.org/ [--catalogue catalogue/posts.json] [--samples 5]

Environment:
  HKA_PAYMENT_PATTERNS  payment details that must never reappear, one regular expression per line. Kept in a
                        secret (not in the code) so the numbers are not republished; without it that check is skipped.
  HKA_PREVIEW_PASSWORD  during a password-protected preview, lets the checks log in as "preview".

Checks: home page and sample posts load with the archive notice, folder-style addresses work, missing
pages return the archive's 404 page, pages are served as UTF-8, no payment details have reappeared,
the HTTPS certificate is not close to expiry, and (for a custom domain) the domain registration is not
close to expiry. Writes a Markdown summary to $GITHUB_STEP_SUMMARY when run in GitHub Actions.
"""
import argparse, base64, datetime, json, os, random, re, socket, ssl, sys, urllib.error, urllib.parse as up, urllib.request

UA = "hka8964-archive-healthcheck/1.0"
HEADERS = {"User-Agent": UA}
if os.environ.get("HKA_PREVIEW_PASSWORD"):
    HEADERS["Authorization"] = "Basic " + base64.b64encode(
        ("preview:" + os.environ["HKA_PREVIEW_PASSWORD"]).encode()).decode()
NOTICE = 'id="hka-archive-notice"'
NOT_FOUND_MARK = "Page not found"
PAYMENT_LINES = [l.strip() for l in os.environ.get("HKA_PAYMENT_PATTERNS", "").splitlines() if l.strip()]
PAYMENT = re.compile("|".join(PAYMENT_LINES)) if PAYMENT_LINES else None

results = []


def record(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (f" - {detail}" if detail else ""), flush=True)


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.headers, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode("utf-8", "replace")


def check_page(label, url):
    try:
        status, headers, body = fetch(url)
    except Exception as e:
        record(label, False, f"{url}: {e}")
        return
    problems = []
    if status != 200:
        problems.append(f"HTTP {status}")
    if NOTICE not in body:
        problems.append("archive notice missing")
    if "charset=utf-8" not in (headers.get("Content-Type") or "").lower():
        problems.append(f"Content-Type is {headers.get('Content-Type')!r}")
    if PAYMENT and PAYMENT.search(body):
        problems.append("payment details present")
    record(label, not problems, f"{url}: " + ", ".join(problems) if problems else url)


def days_left_cert(host):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, 443), timeout=20) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            not_after = tls.getpeercert()["notAfter"]
    expires = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=datetime.timezone.utc)
    return (expires - datetime.datetime.now(datetime.timezone.utc)).days


def days_left_domain(host):
    domain = ".".join(host.split(".")[-2:])  # fine for .org/.com/.news; not for two-part endings like .org.uk
    req = urllib.request.Request(f"https://rdap.org/domain/{domain}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    for event in data.get("events", []):
        if event.get("eventAction") == "expiration":
            expires = datetime.datetime.fromisoformat(event["eventDate"].replace("Z", "+00:00"))
            return domain, (expires - datetime.datetime.now(datetime.timezone.utc)).days
    return domain, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site_url")
    ap.add_argument("--catalogue", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "catalogue", "posts.json"),
                    help="local posts.json; if missing, the catalogue published on the site is used")
    ap.add_argument("--samples", type=int, default=5)
    ap.add_argument("--min-cert-days", type=int, default=21)
    ap.add_argument("--min-domain-days", type=int, default=60)
    ap.add_argument("--no-domain-check", action="store_true", help="skip the domain registration check (e.g. for a host's own address)")
    a = ap.parse_args()
    base = a.site_url.rstrip("/") + "/"
    host = up.urlsplit(base).hostname

    if not PAYMENT:
        print("SKIP payment details check - HKA_PAYMENT_PATTERNS is not set", flush=True)
    check_page("home page", base)
    paths = []
    try:
        if os.path.exists(a.catalogue):
            rows = json.load(open(a.catalogue, encoding="utf-8"))
        else:
            rows = json.loads(fetch(base + "catalogue/posts.json")[2])
        rows = [r for r in rows if r["type"] == "post"]
        paths = [r["archive_path"] for r in random.sample(rows, min(a.samples, len(rows)))]
    except Exception as e:
        record("catalogue of posts", False, str(e))
    for p in paths:
        check_page(f"post {p}", base + up.quote(p))
    if paths:  # the same post without the trailing slash must still be served
        check_page("folder address without slash", base + up.quote(paths[0].rstrip("/")))

    for name in ("robots.txt", "llms.txt", "catalogue/posts.json"):
        try:
            status, _, _ = fetch(base + name)
            record(f"{name} reachable", status == 200, f"HTTP {status}")
        except Exception as e:
            record(f"{name} reachable", False, str(e))

    status, _, body = fetch(base + "this-page-does-not-exist-" + str(random.randint(1000, 9999)))
    record("missing page returns 404 page", status == 404 and NOT_FOUND_MARK in body, f"HTTP {status}")

    try:
        days = days_left_cert(host)
        record("HTTPS certificate", days >= a.min_cert_days, f"{days} days left")
    except Exception as e:
        record("HTTPS certificate", False, str(e))

    if not a.no_domain_check:
        try:
            domain, days = days_left_domain(host)
            record("domain registration", days is not None and days >= a.min_domain_days,
                   f"{domain}: {days} days left" if days is not None else f"{domain}: no expiry date in RDAP")
        except Exception as e:
            record("domain registration", False, str(e))

    failed = [r for r in results if not r[1]]
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"## Health check: {base}\n\n| Check | Result | Detail |\n|---|---|---|\n")
            for name, ok, detail in results:
                f.write(f"| {name} | {'✅' if ok else '❌'} | {detail} |\n")
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
