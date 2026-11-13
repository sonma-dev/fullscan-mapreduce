#!/usr/bin/env python3
import json,collections,pathlib
p=pathlib.Path(__file__).resolve().parent
def load(s):return [json.loads(l) for l in open(p/s,encoding="utf8") if l.strip()]
J=load("04_atomic_judgments_final.jsonl");R=load("01_source_atoms_final.jsonl");N=load("01_source_negative_controls_final.jsonl");GO=load("02_generated_atoms_final.jsonl");GC=load("02_generated_classes_final.jsonl")
c=collections.Counter(x["scoring_cell"] for x in J);TP,TN,FP,FN=(c[x] for x in ("TP","TN","FP","FN"))
assert TP+FN==len(R) and TN+FP==len(N) and sum(c.values())==len(J)
assert len(GO)>=len(GC) and sum(len(x["generated_occurrence_ids"]) for x in GC)==len(GO)
res={"TP":TP,"TN":TN,"FP":FP,"FN":FN,"precision":TP/(TP+FP) if TP+FP else None,"recall":TP/(TP+FN) if TP+FN else None,"f1":2*TP/(2*TP+FP+FN) if 2*TP+FP+FN else None,"duplicate":(len(GO)-len(GC))/len(GO) if GO else None}
print(json.dumps(res,indent=2))
