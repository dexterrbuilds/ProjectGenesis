"""Read original v783 anatomy; emit a content-addressed research-only circuit.

No Genesis imports. Run explicitly with --cache pointing at downloaded originals.
All numeric root IDs are converted to strings before any JSON serialization.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pyarrow.feather as feather

HERE = Path(__file__).resolve().parent
EXPECTED = {
    "proofread_connections_783.feather": ("md5", "f48f972d262323a102aed49af1396b8a"),
    "proofread_root_ids_783.npy": ("md5", "e0e6c19732fd8c7a4e39a2d170105421"),
    "annotations-v3.1.0.tsv": ("sha256", "9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be"),
}


def digest(path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(2**20), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def extract(cache, output):
    for name, (alg, expected) in EXPECTED.items():
        if digest(cache / name, alg) != expected:
            raise ValueError(f"Source checksum mismatch: {name}")
    annotations = list(csv.DictReader((cache / "annotations-v3.1.0.tsv").open(), delimiter="\t"))
    ann = {int(r["root_id"]): r for r in annotations}
    proofread = set(map(int, np.load(cache / "proofread_root_ids_783.npy")))
    table = feather.read_table(cache / "proofread_connections_783.feather",
                               columns=["pre_pt_root_id", "post_pt_root_id", "syn_count", "neuropil"])
    pre = table["pre_pt_root_id"].to_numpy()
    post = table["post_pt_root_id"].to_numpy()
    contacts = table["syn_count"].to_numpy().astype(np.int64)

    def typed(name):
        return [i for i, r in ann.items() if r["cell_type"] == name]

    def upstream(targets, candidates):
        mask = np.isin(post, list(targets)) & np.isin(pre, list(candidates))
        return set(map(int, pre[mask]))

    targets = set(typed("MBON11") + typed("MBON18") + typed("MBON07"))
    kc = upstream(targets, [i for i,r in ann.items() if r["cell_class"] == "Kenyon_Cell"
                           and (r["cell_type"].startswith("KCab") or r["cell_type"].startswith("KCg"))])
    lh_candidates = {i for i,r in ann.items() if r["hemibrain_type"] in ("LHPD2a1", "LHPD2b1")}
    lh = set(map(int, post[np.isin(pre, typed("MBON18")) & np.isin(post,list(lh_candidates))]))
    pn = upstream(kc | lh, [i for i,r in ann.items() if r["cell_class"] == "ALPN"
                          and ("acetylcholine" in r["known_nt"] or r["top_nt"] == "acetylcholine")])
    groups = {"KC":kc, "PN":pn, "MB11":set(typed("MBON11")), "MB18":set(typed("MBON18")),
              "DAN":set(typed("PPL101")), "OA":set(typed("OA-VPM4")), "VALUE":set(typed("MBON07")),
              "CONTROL":set(typed("MBON14")), "APL":upstream(kc,typed("APL")), "LH":lh,
              "LHCENT":set(typed("LHCENT1"))}
    if any(not v for v in groups.values()):
        raise ValueError(f"Anatomical selection has an empty required group: {groups.keys()}")
    selected = set.union(*groups.values())
    if not selected <= proofread:
        raise ValueError("Selected root not in proofread inventory")
    role = {i: name for name, ids in groups.items() for i in ids}
    keep_pre, keep_post = np.isin(pre, list(selected)), np.isin(post, list(selected))
    retained = keep_pre & keep_post
    entering, leaving = ~keep_pre & keep_post, keep_pre & ~keep_post
    masks = {"retained": retained, "omitted_input": entering, "omitted_output": leaving}
    neuropil = table["neuropil"].to_pylist()

    def edges(mask):
        return sorted(({"source": str(int(pre[k])), "target": str(int(post[k])),
                        "neuropil": neuropil[k], "synapses": int(contacts[k])}
                       for k in np.flatnonzero(mask)), key=lambda e: (e["source"], e["target"], e["neuropil"] or ""))

    edge_rows = edges(retained)
    boundary_rows = edges(entering | leaving)
    per_node = {str(i): {"retained_input": 0, "retained_output": 0,
                         "omitted_input": 0, "omitted_output": 0} for i in selected}
    for e in edge_rows:
        per_node[e["target"]]["retained_input"] += e["synapses"]
        per_node[e["source"]]["retained_output"] += e["synapses"]
    boundary_classes = collections.Counter()
    for e in boundary_rows:
        incoming = int(e["target"]) in selected
        inside, outside = (e["target"], e["source"]) if incoming else (e["source"], e["target"])
        direction = "omitted_input" if incoming else "omitted_output"
        per_node[inside][direction] += e["synapses"]
        outside_ann = ann.get(int(outside), {})
        label = (direction, role[int(inside)], outside_ann.get("cell_class", "unannotated"),
                 outside_ann.get("cell_type", "unannotated"), outside_ann.get("top_nt", "unknown"))
        boundary_classes[label] += e["synapses"]

    nodes = []
    for i in sorted(selected):
        a = ann[i]
        nodes.append({"root_id": str(i), "role": role[i], **{k: a[k] for k in
                      ("cell_type", "cell_class", "cell_sub_class", "hemibrain_type", "side", "top_nt", "known_nt", "vfb_id", "fbbt_id", "matching_notes", "synonyms")}})
    circuit = {"schema": 1, "nodes": nodes, "edges": edge_rows,
               "groups": {k: sorted(map(str, v)) for k, v in groups.items()}}
    boundary = {
        "denominator": "All contacts in proofread_connections_783; excludes unproofread fragments, electrical and volume transmission.",
        "per_neuron": per_node,
        "by_external_class_type_transmitter": [dict(zip(
            ["direction", "inside_role", "outside_class", "outside_type", "predicted_nt", "synapses"], (*k, v)))
            for k, v in sorted(boundary_classes.items())],
        "totals": {name: {"neuropil_rows": int(mask.sum()), "synapses": int(contacts[mask].sum())}
                   for name, mask in masks.items()},
    }
    counts = {"neurons": len(nodes), "roles": {k: len(v) for k, v in groups.items()},
              "neuropil_edges": len(edge_rows), "directed_pairs": len({(e['source'], e['target']) for e in edge_rows}),
              "synapses": sum(e["synapses"] for e in edge_rows)}
    files = {"circuit.json": canonical(circuit), "boundary.json": canonical(boundary),
             "boundary-edges.json.gz": gzip.compress(canonical(boundary_rows), mtime=0)}
    manifest = {
        "schema": 1, "dataset": "adult female FAFB/FlyWire", "materialization": 783,
        "annotation_version": "v3.1.0", "counts": counts,
        "selection": "Bilateral MBON11/18/PPL101/OA-VPM4; MBON07 learned-state context; actual upstream gamma/alpha-beta KCs; actual cholinergic ALPN inputs to KCs and MBON18-linked PD2a1/b1 aliases; connected APL; MBON14 comparator; LHCENT1 feedback. No strength threshold or post-outcome expansion.",
        "crosswalk": {"PPL101":"MP1/PPL1-gamma1pedc", "MBON11":"MVP2/gamma1pedc-to-alpha-beta/MB112C",
                      "MBON18":"alpha2sc/MB080C", "OA-VPM4":"MB113C; not VPM3",
                      "LH":"hemibrain LHPD2a1/b1 aliases; uncertain exact functional-driver membership"},
        "crosswalk_sha256": digest(HERE/"LITERATURE.md"),
        "ambiguous_roots": sorted(map(str,lh)),
        "limitations": ["No peptide or receptor edges are inferred from chemical contacts.",
           "Resource modulation is a literature-direction body boundary, not starvation or simulated NPF release.",
           "Anatomical row neuropils do not establish exact receptor localization.",
           "PPL101 nitric oxide cotransmission omitted; LH aliases are one-to-many across annotation nomenclatures."],
        "sources": [{"file": name, "sha256": digest(cache/name), "source_checksum": f"{alg}:{checksum}",
                     "url": ("https://raw.githubusercontent.com/flyconnectome/flywire_annotations/v3.1.0/supplemental_files/Supplemental_file1_neuron_annotations.tsv" if name.endswith("tsv") else
                             f"https://zenodo.org/api/records/10676866/files/{name}/content")}
                    for name, (alg, checksum) in EXPECTED.items()],
        "license": {"zenodo_connectivity": "CC-BY-4.0", "flywire_site_guidelines": "CC-BY-NC-4.0",
                    "annotation_license": "not independently resolved", "use": "isolated research; resolve licensing before commercial redistribution"},
        "annotation_reconciliation": {"proofread_count": len(proofread), "annotation_count": len(ann),
                                      "missing_annotations": sorted(map(str, proofread - ann.keys())),
                                      "annotations_not_in_inventory": sorted(map(str, ann.keys() - proofread)),
                                      "selected_missing_annotations": []},
        "selected_roots": sorted(map(str, selected)),
        "artifacts": {name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)} for name, data in files.items()},
        "extractor_sha256": digest(__file__), "analysis_plan_sha256": digest(HERE / "PLAN.md"),
    }
    manifest_bytes = canonical(manifest)
    identity = hashlib.sha256(manifest_bytes).hexdigest()
    dest = output / identity
    dest.mkdir(parents=True, exist_ok=True)
    for name, data in {**files, "manifest.json": manifest_bytes}.items():
        path = dest / name
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError("Refusing to overwrite immutable artifact")
        else:
            with path.open("xb") as f:
                f.write(data)
    print(json.dumps({"manifest": str(dest/"manifest.json"), "id": identity, "counts": counts,
                      "boundary": boundary['totals'], "reconciliation": manifest['annotation_reconciliation']}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE/"artifacts")
    args = parser.parse_args()
    extract(args.cache, args.output)
