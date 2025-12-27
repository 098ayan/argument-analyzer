from typing import List, Dict, Optional

DEFAULT_COLORS = {
    "conclusion": "#4A90E2",   # blue
    "premise": "#7ED321",      # green
    "rebuttal": "#D0021B",     # red
    "undercutter": "#F5A623",  # orange
}

def build_argument_graph(
    conclusion: Optional[str],
    premises: List[str],
    objections: List[Dict],
) -> Dict:
    """
    Build a clause-level argument graph with:
    - premises supporting conclusion
    - rebuttals attacking conclusion
    - undercutters attacking premises (fallback to conclusion if none)
    """

    nodes = []
    edges = []

    #  Conclusion 
    if conclusion:
        nodes.append({
            "id": "C",
            "label": conclusion,
            "type": "conclusion",
            "color": DEFAULT_COLORS["conclusion"],
        })

    # Premises
    for i, p in enumerate(premises):
        pid = f"P{i}"
        nodes.append({
            "id": pid,
            "label": p,
            "type": "premise",
            "color": DEFAULT_COLORS["premise"],
        })

        if conclusion:
            edges.append({
                "from": pid,
                "to": "C",
                "type": "support",
                "style": "solid",
            })

    # Objections
    for i, o in enumerate(objections):
        oid = f"O{i}"
        o_type = o.get("type", "rebuttal")

        nodes.append({
            "id": oid,
            "label": o.get("sentence", ""),
            "type": o_type,
            "color": DEFAULT_COLORS.get(o_type, "#999999"),
        })

        if not conclusion:
            continue

        # Undercutter fallback if no premises exist
        if o_type == "undercutter" and not premises:
            target = "C"
            edge_type = "rebuttal"
        else:
            target = "C" if o_type == "rebuttal" else "P0"
            edge_type = o_type

        edges.append({
            "from": oid,
            "to": target,
            "type": edge_type,
            "style": "dashed",
        })

    return {
        "nodes": nodes,
        "edges": edges,
    }
