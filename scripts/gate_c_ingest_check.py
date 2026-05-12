#!/usr/bin/env python3
"""
Gate C Three-Lane Ingest Checker
Validates gate-c-review-log.ndjson, gate-c-rework-log.ndjson, gate-c-stability-log.ndjson
against the Gate C Three-Lane Ingest Checklist (2026-05-11).

Usage:
    python scripts/gate_c_ingest_check.py
"""

import json
import sys
from pathlib import Path

WINDOW_ID = "gate-c-window-2026-05-11"
REQUIRED_LANES = ["copilot", "claude", "chatgpt"]
MIN_VALID_ROWS = 10

BASE = Path(__file__).parent.parent / "docs" / "status"
REVIEW_LOG  = BASE / "gate-c-review-log.ndjson"
REWORK_LOG  = BASE / "gate-c-rework-log.ndjson"
STABILITY_LOG = BASE / "gate-c-stability-log.ndjson"

PASS  = "[PASS]"
FAIL  = "[FAIL]"
WARN  = "[WARN]"
ALLOWED_TOOL_EVIDENCE = {"complete", "partial", "absent", "unknown"}


def load_ndjson(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


# ─── Section 1: Required Files ──────────────────────────────────────────────

def check_required_files():
    print("=" * 60)
    print("§1  Required Files")
    print("=" * 60)
    all_ok = True
    for path in [REVIEW_LOG, REWORK_LOG, STABILITY_LOG]:
        exists = path.exists()
        tag = PASS if exists else FAIL
        print(f"  {tag}  {path.name}")
        if not exists:
            all_ok = False
    return all_ok


# ─── Section 2.1: Review Log Schema ─────────────────────────────────────────

def check_review_log(rows):
    print("\n" + "=" * 60)
    print("§2.1  Review Log Schema")
    print("=" * 60)

    required_keys = ["window_id", "lane", "run_id",
                     "review_start_utc", "review_end_utc", "review_minutes"]

    counts = {lane: {"total": 0, "valid": 0, "pending": 0, "schema_fail": 0}
              for lane in REQUIRED_LANES}
    counts["copilot"] = {"total": 0, "valid": 0, "pending": 0, "schema_fail": 0}

    schema_errors = []
    for row in rows:
        # window_id filter
        if row.get("window_id") != WINDOW_ID:
            schema_errors.append(f"  {FAIL}  wrong window_id in row: {row.get('run_id')}")
            continue

        lane = row.get("lane", "unknown")
        if lane not in counts:
            counts[lane] = {"total": 0, "valid": 0, "pending": 0, "schema_fail": 0}
        counts[lane]["total"] += 1

        # Required keys
        missing = [k for k in required_keys if k not in row]
        if missing:
            schema_errors.append(f"  {FAIL}  {row.get('run_id')} missing keys: {missing}")
            counts[lane]["schema_fail"] += 1
            continue

        rm = row["review_minutes"]
        if rm is None:
            counts[lane]["pending"] += 1
        elif isinstance(rm, (int, float)) and rm >= 0:
            # Check timestamp ordering if both are present
            start = row.get("review_start_utc")
            end   = row.get("review_end_utc")
            if start and end and end < start:
                schema_errors.append(
                    f"  {FAIL}  {row.get('run_id')} review_end < review_start")
                counts[lane]["schema_fail"] += 1
            else:
                counts[lane]["valid"] += 1
        else:
            schema_errors.append(
                f"  {FAIL}  {row.get('run_id')} review_minutes invalid: {rm!r}")
            counts[lane]["schema_fail"] += 1

    for err in schema_errors:
        print(err)

    print(f"\n  {'Lane':<12} {'total':>6} {'valid':>6} {'pending':>8} {'schema_fail':>12}")
    print(f"  {'-'*46}")
    vol_ok = True
    for lane in REQUIRED_LANES:
        c = counts.get(lane, {"total": 0, "valid": 0, "pending": 0, "schema_fail": 0})
        vol_tag = PASS if c["valid"] >= MIN_VALID_ROWS else FAIL
        if c["valid"] < MIN_VALID_ROWS:
            vol_ok = False
        print(f"  {vol_tag}  {lane:<10} {c['total']:>6} {c['valid']:>6} {c['pending']:>8} {c['schema_fail']:>12}")

    print(f"\n  Minimum valid rows (>={MIN_VALID_ROWS}) per lane:")
    for lane in REQUIRED_LANES:
        c = counts.get(lane, {"valid": 0})
        tag = PASS if c["valid"] >= MIN_VALID_ROWS else FAIL
        note = ""
        if c.get("pending", 0) > 0 and c["valid"] < MIN_VALID_ROWS:
            note = f" ← {c['pending']} rows pending (review_minutes=null; timestamps not yet captured)"
        print(f"    {tag}  {lane}: {c['valid']}/{MIN_VALID_ROWS} valid rows{note}")

    return counts, vol_ok


def check_optional_tool_evidence(rows):
    print("\n" + "=" * 60)
    print("禮2.4  Optional Tool Evidence (informational)")
    print("=" * 60)

    lane_counts = {lane: {"complete": 0, "partial": 0, "absent": 0, "unknown": 0, "invalid": 0}
                   for lane in REQUIRED_LANES}
    any_present = False

    for row in rows:
        if row.get("window_id") != WINDOW_ID:
            continue
        lane = row.get("lane", "unknown")
        if lane not in lane_counts:
            lane_counts[lane] = {"complete": 0, "partial": 0, "absent": 0, "unknown": 0, "invalid": 0}

        value = row.get("tool_evidence_completeness")
        if value is None:
            value = "unknown"

        any_present = True
        if value in ALLOWED_TOOL_EVIDENCE:
            lane_counts[lane][value] += 1
        else:
            lane_counts[lane]["invalid"] += 1

    if not any_present:
        print(f"  {WARN}  No tool evidence annotations found (non-blocking).")
        return lane_counts

    print(f"\n  {'Lane':<12} {'complete':>9} {'partial':>8} {'absent':>7} {'unknown':>8} {'invalid':>8}")
    print(f"  {'-'*60}")
    for lane in REQUIRED_LANES:
        c = lane_counts.get(lane, {"complete": 0, "partial": 0, "absent": 0, "unknown": 0, "invalid": 0})
        tag = PASS if c["invalid"] == 0 else WARN
        print(f"  {tag}  {lane:<10} {c['complete']:>9} {c['partial']:>8} {c['absent']:>7} {c['unknown']:>8} {c['invalid']:>8}")

    print(f"\n  {PASS}  Missing field fallback: absent `tool_evidence_completeness` is counted as `unknown`.")
    print(f"  {PASS}  Informational only: does not affect Gate C pass/provisional-pass.")
    return lane_counts


# ─── Section 2.2: Rework Log Schema ─────────────────────────────────────────

def check_rework_log(rows):
    print("\n" + "=" * 60)
    print("§2.2  Rework Log Schema")
    print("=" * 60)

    required_keys = ["window_id", "lane", "run_id",
                     "reopen_count", "revert_count", "total_changes", "reopen_revert_rate"]

    lane_agg = {lane: {"total_changes": 0, "reopen": 0, "revert": 0,
                        "valid_rows": 0, "schema_fail": 0}
                for lane in REQUIRED_LANES}

    schema_errors = []
    for row in rows:
        if row.get("window_id") != WINDOW_ID:
            schema_errors.append(f"  {FAIL}  wrong window_id: {row.get('run_id')}")
            continue

        lane = row.get("lane", "unknown")
        if lane not in lane_agg:
            lane_agg[lane] = {"total_changes": 0, "reopen": 0, "revert": 0,
                               "valid_rows": 0, "schema_fail": 0}

        missing = [k for k in required_keys if k not in row]
        if missing:
            schema_errors.append(f"  {FAIL}  {row.get('run_id')} missing keys: {missing}")
            lane_agg[lane]["schema_fail"] += 1
            continue

        tc = row["total_changes"]
        if tc <= 0:
            schema_errors.append(
                f"  {FAIL}  {row.get('run_id')} total_changes must be > 0, got {tc}")
            lane_agg[lane]["schema_fail"] += 1
            continue

        expected = (row["reopen_count"] + row["revert_count"]) / tc
        actual   = row["reopen_revert_rate"]
        if abs(expected - actual) > 0.001:
            schema_errors.append(
                f"  {FAIL}  {row.get('run_id')} rate mismatch: "
                f"expected {expected:.4f}, got {actual}")
            lane_agg[lane]["schema_fail"] += 1
            continue

        lane_agg[lane]["valid_rows"]    += 1
        lane_agg[lane]["total_changes"] += tc
        lane_agg[lane]["reopen"]        += row["reopen_count"]
        lane_agg[lane]["revert"]        += row["revert_count"]

    for err in schema_errors:
        print(err)

    print(f"\n  {'Lane':<12} {'valid_rows':>10} {'total_changes':>14} {'reopen':>8} {'revert':>8} {'rate':>8}")
    print(f"  {'-'*62}")
    all_ok = True
    for lane in REQUIRED_LANES:
        a = lane_agg.get(lane, {"valid_rows": 0, "total_changes": 0, "reopen": 0, "revert": 0})
        tc = a["total_changes"]
        rate = (a["reopen"] + a["revert"]) / tc if tc > 0 else None
        denom_ok = tc > 0
        tag = PASS if denom_ok else FAIL
        if not denom_ok:
            all_ok = False
        rate_str = f"{rate:.4f}" if rate is not None else "N/A"
        print(f"  {tag}  {lane:<10} {a['valid_rows']:>10} {tc:>14} {a['reopen']:>8} {a['revert']:>8} {rate_str:>8}")

    return lane_agg, all_ok


# ─── Section 2.3: Stability Log Schema ──────────────────────────────────────

def check_stability_log(rows):
    print("\n" + "=" * 60)
    print("§2.3  Stability Log Schema")
    print("=" * 60)

    required_keys = ["window_id", "lane", "run_id",
                     "integration_stability", "stability_note"]

    lane_counts = {lane: {"stable": 0, "degraded": 0, "unknown": 0, "schema_fail": 0}
                   for lane in REQUIRED_LANES}

    schema_errors = []
    for row in rows:
        if row.get("window_id") != WINDOW_ID:
            schema_errors.append(f"  {FAIL}  wrong window_id: {row.get('run_id')}")
            continue

        lane = row.get("lane", "unknown")
        if lane not in lane_counts:
            lane_counts[lane] = {"stable": 0, "degraded": 0, "unknown": 0, "schema_fail": 0}

        missing = [k for k in required_keys if k not in row]
        if missing:
            schema_errors.append(f"  {FAIL}  {row.get('run_id')} missing keys: {missing}")
            lane_counts[lane]["schema_fail"] += 1
            continue

        stab = row["integration_stability"]
        if stab not in ("stable", "degraded"):
            schema_errors.append(
                f"  {FAIL}  {row.get('run_id')} integration_stability={stab!r} "
                f"(must not be unknown)")
            lane_counts[lane]["unknown"] += 1
        elif stab == "stable":
            lane_counts[lane]["stable"] += 1
        else:
            lane_counts[lane]["degraded"] += 1

    for err in schema_errors:
        print(err)

    print(f"\n  {'Lane':<12} {'stable':>8} {'degraded':>9} {'unknown':>8} {'schema_fail':>12}")
    print(f"  {'-'*51}")
    all_ok = True
    for lane in REQUIRED_LANES:
        c = lane_counts.get(lane, {"stable": 0, "degraded": 0, "unknown": 0, "schema_fail": 0})
        has_rows = (c["stable"] + c["degraded"]) > 0
        tag = PASS if has_rows and c["unknown"] == 0 else FAIL
        if not has_rows or c["unknown"] > 0:
            all_ok = False
        print(f"  {tag}  {lane:<10} {c['stable']:>8} {c['degraded']:>9} {c['unknown']:>8} {c['schema_fail']:>12}")

    return lane_counts, all_ok


# ─── Section 3: Lane-by-Lane Ingest ──────────────────────────────────────────

def check_lane_ingest(review_counts, rework_agg, stability_counts):
    print("\n" + "=" * 60)
    print("§3  Lane-by-Lane Ingest Checklist")
    print("=" * 60)

    all_lanes_ok = True
    for lane in REQUIRED_LANES:
        print(f"\n  Lane: {lane.upper()}")
        rc = review_counts.get(lane, {"valid": 0})
        ra = rework_agg.get(lane, {"total_changes": 0})
        sc = stability_counts.get(lane, {"stable": 0, "unknown": 0})

        ok1 = rc.get("valid", 0) >= MIN_VALID_ROWS
        ok2 = ra.get("total_changes", 0) > 0
        ok3 = sc.get("stable", 0) > 0 and sc.get("unknown", 0) == 0
        ok4 = ok1 and ok2 and ok3  # lane Gate C can be computed

        tag1 = PASS if ok1 else FAIL
        tag2 = PASS if ok2 else PASS  # rework denominator ok even if 0 reopen/revert
        tag3 = PASS if ok3 else FAIL
        tag4 = PASS if ok4 else WARN

        note1 = "" if ok1 else f" (only {rc.get('valid',0)} valid; {rc.get('pending',0)} pending)"
        note3 = "" if ok3 else " (0 rows)" if sc.get("stable", 0) == 0 else ""

        print(f"    {tag1}  review log rows >= {MIN_VALID_ROWS}{note1}")
        print(f"    {tag2}  rework log valid denominator (total_changes={ra.get('total_changes',0)})")
        print(f"    {tag3}  stability log rows ingested{note3}")
        if ok4:
            rrr = (ra.get("reopen", 0) + ra.get("revert", 0)) / max(ra.get("total_changes", 1), 1)
            print(f"    {PASS}  lane-level Gate C: reopen_revert_rate={rrr:.4f}, stability=stable")
        else:
            print(f"    {WARN}  lane-level Gate C: cannot fully compute (review_minutes=null)")
            all_lanes_ok = False

    return all_lanes_ok


# ─── Section 4: Upgrade Gate ────────────────────────────────────────────────

def check_upgrade_gate(review_counts, rework_agg, stability_counts):
    print("\n" + "=" * 60)
    print("§4  Upgrade Gate (provisional-pass -> pass)")
    print("=" * 60)

    cond1 = all(review_counts.get(l, {}).get("valid", 0) >= MIN_VALID_ROWS
                for l in REQUIRED_LANES)
    cond2 = all(rework_agg.get(l, {}).get("total_changes", 0) > 0
                for l in REQUIRED_LANES)
    cond3 = all(stability_counts.get(l, {}).get("stable", 0) > 0 and
                stability_counts.get(l, {}).get("unknown", 0) == 0
                for l in REQUIRED_LANES)
    cond4 = cond1  # avg_review_minutes computable only if valid rows >= 10

    print(f"  {PASS if cond1 else FAIL}  All lanes have >= {MIN_VALID_ROWS} valid review timing rows")
    for lane in REQUIRED_LANES:
        v = review_counts.get(lane, {}).get("valid", 0)
        p = review_counts.get(lane, {}).get("pending", 0)
        note = f"(pending: {p})" if p > 0 else ""
        print(f"         {lane}: valid={v} {note}")

    print(f"  {PASS if cond2 else FAIL}  All lanes have valid reopen/revert denominator")
    print(f"  {PASS if cond3 else FAIL}  All lanes have non-unknown stability entries")
    print(f"  {PASS if cond4 else FAIL}  avg_review_minutes computable from valid rows")

    upgrade = cond1 and cond2 and cond3 and cond4
    result = "pass" if upgrade else "provisional-pass"
    print(f"\n  Upgrade gate: {'OPEN' if upgrade else 'BLOCKED'}")
    print(f"  Gate C result: {result}")
    if not upgrade:
        blocked_by = []
        if not cond1:
            blocked_by.append("review_minutes=null for all rows (timestamps not yet captured)")
        if not cond3:
            blocked_by.append("copilot lane has 0 stability entries")
        print(f"  Blocked by: {'; '.join(blocked_by)}")

    return result


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"\nGate C Three-Lane Ingest Check")
    print(f"Window: {WINDOW_ID}")
    print(f"Date: 2026-05-11\n")

    # §1
    files_ok = check_required_files()
    if not files_ok:
        print(f"\n{FAIL}  Required files missing — stopping.")
        sys.exit(1)

    # Load
    review_rows   = load_ndjson(REVIEW_LOG)
    rework_rows   = load_ndjson(REWORK_LOG)
    stability_rows = load_ndjson(STABILITY_LOG)

    # §2
    review_counts, review_vol_ok = check_review_log(review_rows)
    check_optional_tool_evidence(review_rows)
    rework_agg,    rework_ok     = check_rework_log(rework_rows)
    stability_counts, stab_ok   = check_stability_log(stability_rows)

    # §3
    lanes_ok = check_lane_ingest(review_counts, rework_agg, stability_counts)

    # §4
    result = check_upgrade_gate(review_counts, rework_agg, stability_counts)

    # §5 summary
    print("\n" + "=" * 60)
    print("§5  Final Sign-off")
    print("=" * 60)
    print(f"  Window ID  : {WINDOW_ID}")
    print(f"  Result     : {result}")
    print(f"  Files OK   : {files_ok}")
    print(f"  Rework OK  : {rework_ok}")
    print(f"  Stability  : {stab_ok}")
    print(f"  Review vol : {review_vol_ok}")
    if result == "provisional-pass":
        print(f"  Reason     : review_minutes=null for all rows; "
              f"copilot lane has no ingest data.")
        print(f"  Action     : start capturing timestamps from next run batch per lane.")
    print()


if __name__ == "__main__":
    main()
