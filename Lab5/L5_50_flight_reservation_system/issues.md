# Lab 5: Identified Issues

Line numbers refer to the original flight_reservation_system.py.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (B605) | Security (High) | 63 | os.system runs a shell command built from the filename, so a crafted filename could run arbitrary commands | Replaced os.system with a plain print |
| Weak MD5 hash (B324) | Security (High) | 52 | MD5 is broken and unsafe for hashing passenger passport IDs | Replaced with hashlib.sha256 |
| Use of eval (B307, W0123) | Security (Medium) | 47 | eval executes any string passed in as code | Replaced the expression string with a numeric surcharge_rate parameter |
| Bare except with pass (E722, W0702, B110) | Bug (Medium) | 31-32 | Catches every error and hides it silently | Catch only KeyError and print a message |
| Mutable default argument (W0102) | Bug (Medium) | 15 | baggage_tags=[] is shared across all calls | Default to None and create a new list inside the function |
| Hardcoded secret (B105) | Security (Low) | 75, 84 | API token is stored in the code and printed to the console | Read it from the AIRLINE_API_SECRET environment variable and never print it |
| Insecure random PIN (B311) | Security (Low) | 56 | random is predictable and unsuitable for PINs | Used secrets.randbelow |
| File opened without with or encoding (R1732, W1514) | Bug (Low) | 60-62 | File may stay open on error, and the encoding depends on the platform | Used with open(..., encoding="utf-8") |
| Global statement (W0603) and constant naming (C0103) | Style | 12, 16 | global total_revenue modifies module state | Stored revenue in a STATS dictionary |
| Redefined outer name (W0621) and unused loop variable (W0612) | Style | 66, 68 | Parameter flights shadows the global, and f is never used | Renamed the parameter to flight_data and used sum over .values() |
| Unused import and variables (F401, F841, W0611, W0612) | Style | 4, 36, 46 | math and airport_fee are unused, and base_fare was only used inside eval | Removed the unused names, so base_fare is now used directly |
| Comparison to None (E711, C0121) and simplifiable if (R1703, R1705) | Style | 37-42 | == None and an if/else that just returns a boolean | Used is None and return not flight["is_full"] |
| Function naming (C0103) | Style | 15-66 | camelCase function names break PEP 8 | Renamed all functions to snake_case |
| Missing docstrings (C0114, C0116) | Style | 1, all functions | No module or function documentation | Added docstrings |
| Long lines and old formatting (E501, C0301, C0209) | Style | 7-9, 23 | Lines over 79 characters and % string formatting | Wrapped lines and used f-strings |
| Missing final newline (W292, C0304) | Style | 87 | File does not end with a newline | Added a final newline and an if \_\_name\_\_ == "\_\_main\_\_" guard |
| Cancelling a flight with no bookings (not flagged by tools) | Logic bug | 27-30, 77 | Cancelling BA202 reopened a full flight that had no bookings, so the output wrongly showed 3 available flights | Added a booked counter and only allow a cancellation when bookings exist |
| Revenue not refunded (not flagged by tools) | Logic bug | 27-30 | Cancelling did not reduce total revenue | Subtract the fare on cancellation and print the total revenue |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.00/10 | 10.00/10 |
| Flake8 | 10 issues | 0 issues |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
