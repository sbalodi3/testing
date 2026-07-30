Implement offline tests for Module 2 of my container hardening agent.

Create or update:

- tests/test_ez_scan_ingest.py
- tests/test_artifacts.py, if it already exists
- the workflow/CLI test files that already cover run_ez_scan and `harden scan`
- tests/fixtures/ez_scan/ez-scan.csv

Follow the current pytest style. Use tmp_path and FakeEzScanBackend or
httpx.MockTransport where appropriate. No test may contact a real endpoint,
Nexus, or GitHub.

Build ingestion tests through the real safe boundary:

1. Create a run using ArtifactStore.
2. Create a small results ZIP containing ez-scan.csv.
3. Process it through process_ez_scan_bundle(...).
4. Pass the returned EzScanBundleManifest to ingest_ez_scan_findings(...).

Do not bypass the bundle manifest by passing an arbitrary CSV path.

Required tests:

1. Valid nine-column CSV produces normalized findings.
2. Header-only CSV produces zero findings and a valid summary.
3. Missing required column raises EzScanIngestError.
4. Duplicate normalized header raises EzScanIngestError.
5. Extra column is accepted and produces a warning.
6. UTF-8 BOM is accepted.
7. Invalid nonempty score reports the correct CSV row.
8. Score outside 0 through 10 is rejected.
9. Unknown severity becomes UNKNOWN and produces a warning.
10. Empty and N/A fixed versions become None.
11. python:setuptools becomes package `setuptools`, ecosystem `pypi`, and
    ecosystem_source `package_prefix`.
12. Unprefixed packages remain ecosystem `unknown`.
13. Identical findings from ACS and NeuVector merge scanner sources and
    evidence.
14. Rows with different fixed versions remain separate.
15. Finding IDs and output ordering remain identical across repeated runs.
16. Source path, hash, scanner, and physical row are preserved in evidence.
17. Bundle member hash mismatch is rejected.
18. record_ingestion_result writes:
    - normalized-findings.json
    - ingestion-summary.json
    - manifest entries for both
    - phase findings_normalized
19. Re-recording identical results is idempotent.
20. Different content cannot overwrite immutable ingestion artifacts.
21. End-to-end fake workflow ingests only after PASSED.
22. Failed, cancelled, and timed-out jobs do not create normalized findings.
23. CLI prints counts without printing an access token.

Important test rule:
When testing malformed Pydantic input, call model_validate(...) on malformed
data. Do not use model_copy(...) as a substitute for validation.

Use sanitized fixture values. The ACS and NeuVector JSON samples are
intentionally truncated, so do not parse or depend on them.

Run or provide commands for:

python3 -m pytest
python3 -m ruff check .

If failures are caused by Module 2 integration, fix them within the Module 2
files. Do not broaden scope into Git, SBOM, remediation, or model integration.

At the end, report:
- files created
- files modified
- test results
- Ruff results
- any unverified assumptions
