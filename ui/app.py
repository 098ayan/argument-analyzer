import streamlit as st

from analyzer.parser import split_sentences
from analyzer.classifier import (
    detect_conclusion_with_confidence,
    extract_premises,
    split_compound,
)
from analyzer.fallacies import detect_all_fallacies
from analyzer.objections import detect_counter_arguments

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Argument Analyzer",
    page_icon="📘",
    layout="centered"
)

# -------------------------------------------------
# Minimal aesthetic CSS
# -------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", sans-serif;
}
textarea {
    font-size: 16px !important;
    line-height: 1.7 !important;
}
section[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("Argument Analyzer")
st.caption("Clear analysis of conclusions, premises, objections, and structure.")

st.markdown("---")

# -------------------------------------------------
# UI TOGGLES
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    show_argument_graph = st.checkbox("Show argument graph", value=False)

with col2:
    use_ml = st.checkbox(
        "Use ML assistance (silent)",
        value=False,
        help="ML assists internally only. No explanations shown."
    )

st.markdown("---")

# -------------------------------------------------
# Input
# -------------------------------------------------
argument = st.text_area(
    "Paste an argument below",
    height=240,
    placeholder=(
        "Example:\n"
        "Evolution is false because it contradicts religion.\n"
        "However, evolution has strong scientific evidence."
    )
)

analyze = st.button("Analyze Argument", use_container_width=True)

# -------------------------------------------------
# Session state init
# -------------------------------------------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# -------------------------------------------------
# Run analysis
# -------------------------------------------------
if analyze:
    if argument.strip() == "":
        st.warning("Please enter some text.")
    else:
        sentences = split_sentences(argument)

        # ML toggle is PASSED HERE
        conclusion, confidence, _ = detect_conclusion_with_confidence(
            sentences,
            use_ml=use_ml
        )

        premises = extract_premises(sentences, conclusion) if conclusion else []
        fallacies = detect_all_fallacies(sentences, conclusion)

        objections = detect_counter_arguments(
            sentences,
            conclusion=conclusion,
            premises=premises
        )

        st.session_state.analysis_done = True
        st.session_state.sentences = sentences
        st.session_state.conclusion = conclusion
        st.session_state.confidence = confidence
        st.session_state.premises = premises
        st.session_state.fallacies = fallacies
        st.session_state.objections = objections

# -------------------------------------------------
# Clause-level helper
# -------------------------------------------------
def render_clause(sentence: str, conclusion: str | None):
    head, tail = split_compound(sentence)

    if conclusion and head == conclusion:
        st.markdown(f"🟦 **{head}**")
        if tail:
            st.markdown(f"🟩 because {tail}")
        return

    if tail:
        st.markdown(f"🟩 {head}")
        st.markdown(f"⬜ because {tail}")
        return

    st.markdown(f"⬜ {sentence}")

# -------------------------------------------------
# Display results
# -------------------------------------------------
if st.session_state.analysis_done:
    st.markdown("---")
    st.subheader("Analysis")

    sentences = st.session_state.sentences
    conclusion = st.session_state.conclusion
    confidence = st.session_state.confidence
    premises = st.session_state.premises
    objections = st.session_state.objections

    # Conclusion
    st.markdown("### Conclusion")
    if conclusion:
        st.success(conclusion)
        st.progress(confidence)
    else:
        st.info("No clear conclusion detected.")

    # Premises
    st.markdown("### Premises")
    if premises:
        for p in premises:
            st.write("•", p)
    else:
        st.info("No explicit premises detected.")

    # Counter-Arguments
    st.markdown("### Counter-Arguments")
    if objections:
        for o in objections:
            icon = "🔴" if o["type"] == "rebuttal" else "🟠"
            st.info(f"{icon} {o['sentence']}")
    else:
        st.success("No counter-arguments detected.")

    # Clause Breakdown
    st.markdown("### Clause Breakdown")
    for s in sentences:
        render_clause(s, conclusion)

    # Argument Graph
    if show_argument_graph:
        st.markdown("### Argument Graph")

        try:
            from analyzer.graph import build_argument_graph
            import networkx as nx
            import matplotlib.pyplot as plt

            graph = build_argument_graph(conclusion, premises, objections)
            G = nx.DiGraph()

            for n in graph["nodes"]:
                G.add_node(
                    n["id"],
                    label=n["label"],
                    color=n["color"],
                    type=n["type"]
                )

            for e in graph["edges"]:
                G.add_edge(e["from"], e["to"], style=e["style"])

            pos = {"C": (0, 0)}

            for i, n in enumerate([n for n, d in G.nodes(data=True) if d["type"] == "premise"]):
                pos[n] = (i - 0.5, -1)

            for i, n in enumerate([n for n, d in G.nodes(data=True) if d["type"] == "rebuttal"]):
                pos[n] = (i - 0.5, 1)

            for i, n in enumerate([n for n, d in G.nodes(data=True) if d["type"] == "undercutter"]):
                pos[n] = (i - 0.5, -2)

            plt.figure(figsize=(9, 6))
            nx.draw(
                G,
                pos,
                with_labels=True,
                node_color=[G.nodes[n]["color"] for n in G.nodes],
                node_size=2200,
                font_size=9,
            )
            st.pyplot(plt)

        except Exception as e:
            st.warning("Argument graph could not be rendered.")
            st.caption(str(e))
