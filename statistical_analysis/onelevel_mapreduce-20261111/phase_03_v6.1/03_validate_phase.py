#!/usr/bin/env python3
"""Phase 3 v6.1 item-ledger and evidence-location structural checker.

This script checks reproducible structure and grounded file/line citations.
It cannot certify complete logical entailment or human source atomization.
"""
import json
from pathlib import Path
from collections import Counter

def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def main():
    root = Path(__file__).resolve().parent
    inputs = root.parent
    src = jsonl(root / "01_source_atoms_final.jsonl")
    neg = jsonl(root / "01_source_negative_controls_final.jsonl")
    matches = jsonl(root / "03_evidence_matches_final.jsonl")
    universe = jsonl(root / "03_canonical_universe_final.jsonl")
    bridges = jsonl(root / "03_semantic_coverage_bridges_final.jsonl")
    root_causes = jsonl(root / "03_fn_root_cause_audit_final.jsonl")
    tp_audit = jsonl(root / "03_tp_predicate_review_provisional.jsonl")
    atom_review = jsonl(root / "03_source_atomization_review_preliminary.jsonl")
    deltas = jsonl(root / "03_source_atomization_delta.jsonl")
    changes = jsonl(root / "07_change_delta.jsonl")
    status = json.loads((root / "03_phase_status_final.json").read_text(encoding="utf-8"))

    sids = [r["source_id"] for r in src]
    nids = [r["negative_control_id"] for r in neg]
    mids = [m["canonical_id"] for m in matches]
    assert len(sids)==len(set(sids))
    assert len(nids)==len(set(nids))
    assert set(sids).isdisjoint(nids)
    assert set(sids)==set(mids)
    assert len(matches)==len(src)
    assert len(universe)==len(src)+len(neg)
    assert len({u["canonical_id"] for u in universe})==len(universe)
    assert sum(m["scoring_cell"]=="TP" for m in matches)==len(tp_audit)
    assert sum(m["scoring_cell"]=="FN" for m in matches)+len(tp_audit)==len(src)
    assert {a["source_id"] for a in tp_audit}=={m["canonical_id"] for m in matches if m["scoring_cell"]=="TP"}
    assert len(bridges)==sum(m["entailment_grade"]=="E2" for m in matches)
    assert {b["source_id"] for b in bridges}=={m["canonical_id"] for m in matches if m["entailment_grade"]=="E2"}
    assert len(atom_review)==len(src)+len(deltas)
    assert set(d["old_source_ids"][0] for d in deltas).isdisjoint(sids)
    assert all(ch["kind"] in {"MATCHER_FALSE_NEGATIVE_CORRECTED","COMMON_SOURCE_ATOMIZATION_CORRECTION"} for ch in changes)
    assert all(all(e["physical_page"]>=1 and e["physical_page"]<=90 and e["quote_en"] for e in m["pdf_evidence"]) for m in matches)
    assert all(m["generated_evidence"] for m in matches)
    for m in matches:
        assert m["actual_label"]==1
        assert m["predicted_label"]==int(m["scoring_cell"]=="TP")
        assert m["source_statement_en"]
        for e in m["generated_evidence"]:
            path=inputs / e["file"]
            lines=path.read_text(encoding="utf-8").splitlines()
            assert 1<=e["line_start"]<=len(lines)
            assert e["quote_en"]==lines[e["line_start"]-1]
    final_fn={m["canonical_id"] for m in matches if m["scoring_cell"]=="FN"}
    final_tp={m["canonical_id"] for m in matches if m["scoring_cell"]=="TP"}
    assert all(a["best_generated_candidates"] for a in root_causes)
    assert len({a["source_id"] for a in root_causes})==len(root_causes)
    assert sum(a["final_scoring_cell"]=="FN" for a in root_causes)==len(final_fn)
    assert all(a["source_id"] in final_fn for a in root_causes if a["final_scoring_cell"]=="FN")
    assert all(a["source_id"] in final_tp for a in root_causes if a["final_scoring_cell"]=="TP")
    assert all(a["source_id"] not in sids for a in root_causes if a["final_scoring_cell"]=="REMOVED_OR_MERGED")
    assert sum(a["fn_review_disposition"]=="MATCHER_FALSE_NEGATIVE_CORRECTED" for a in root_causes)==sum(ch["kind"]=="MATCHER_FALSE_NEGATIVE_CORRECTED" for ch in changes)
    assert status["source_side_TP"]==len(final_tp)
    assert status["source_side_FN"]==len(final_fn)
    assert status["source_positive_decisions"]==len(matches)
    assert status["draft_canonical_units_R_plus_N"]==len(universe)
    assert status["frozen_negative_controls"]==len(neg)
    assert status["final_TP_evidence_records_preliminary"]==len(tp_audit)
    assert status["initial_FN_root_cause_audited"]==len(root_causes)
    assert all(u["actual_label"]==0 and u["predicted_label"] is None for u in universe if u["canonical_id"] in nids)
    assert (root / "03_semantic_coverage_and_limitations.md").exists()
    print(json.dumps({
        "structural_status":"PASS",
        "semantic_certification":"NOT_CERTIFIED",
        "source_R":len(src),"negative_N":len(neg),
        "TP":len(final_tp),"FN":len(final_fn),
        "root_cause_dispositions":dict(Counter(a["fn_review_disposition"] for a in root_causes)),
        "source_atomization_delta":len(deltas)
    },indent=2))

if __name__=="__main__": main()
