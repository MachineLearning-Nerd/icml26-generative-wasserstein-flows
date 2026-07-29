# Evaluator-blind red-team review

The reviewer received only a fresh copy of the candidate artifact and began
at `README.md`, `logbook.json`, and `pages/index.md`. No repository knowledge,
OpenResearch logs, or storage paths were supplied.

## Pass 1 — FAIL

The first pass opened the canonical entrypoints, all six claim pages, the
visibility matrix, the historical overview, the cumulative runner, the pinned
environment, all six contracts, source audits, methods, raw results, checker
outputs, negative-control outputs, limitations, and verifier sources.

Seven conclusions were treated as unverifiable because the canonical pages
did not literally label required concepts:

- Claims 1, 2, and 6 did not say “negative control.”
- Claim 2 did not say “Exact claim.”
- Claims 3, 4, and 5 did not say “assumption.”

The complete file-open record is downloadable as
[red_team_pass1.json](red_team_pass1.json).

## Pass 2 — PASS

After only evaluator-facing wording fixes, the review was repeated from a
different fresh copy. It opened 68 reachable files, found every required
claim contract, exact status, source audit, method, inline result, raw data
link, verifier, checker, failing control, limitation, Git SHA, seed statement,
CPU allocation, runtime, fixed command, and pinned environment.

It also verified the judged-file subset hashes, text-only upload allowlist,
displayed key numbers, UTF-8 text, and absence of obvious secret values.
No conclusion remained unverifiable. The exact file-open record and empty
failure list are downloadable as [red_team_pass2.json](red_team_pass2.json).

## Pass 3 — PASS

The passing records and review page were then packaged into the candidate and
the traversal was repeated from a third fresh copy. It opened the added review
page and both prior records as reachable evidence; all scientific,
preservation, text-only, and secret-scan gates remained complete. Download the
[third file-open record](red_team_pass3.json).

## Pass 4 — PASS

After adding the final release forecast, confidence table, command ledger, and
publication action, a fourth fresh-copy traversal opened the new report and
again found no unverifiable conclusion. Download the
[fourth file-open record](red_team_pass4.json).
