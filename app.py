import streamlit as st

from src.parser import parse_transcript
from src.retrieval import EvidenceRetriever
from src.llm import LLMClient
from src.validation import validate_evidence
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Hasamex Expert Interview Analyzer",
    page_icon="🔎",
    layout="wide"
)


# ============================================================
# INTERVIEW GUIDE
# ============================================================

INTERVIEW_GUIDE = {
    1: "How would you describe current adoption of robotic surgery in your market?",
    2: "What are the main barriers to adoption?",
    3: "How important are hospital budgets and ROI in purchasing decisions?",
    4: "How important are surgeon training and clinical outcomes?",
    5: "What adoption trend do you expect over the next 3–5 years?",
    6: "What is the typical hospital decision-making timeline for purchasing a new robotic system?"
}


# ============================================================
# BALANCED CROSS-MARKET RETRIEVAL
# ============================================================

def balanced_search(
    retriever,
    query,
    per_country=3
):
    """
    Retrieve relevant evidence while ensuring
    representation from every market.

    This function is implemented directly in app.py
    so it does not depend on search_diverse().
    """

    # --------------------------------------------------------
    # Create embedding for user query
    # --------------------------------------------------------

    query_embedding = retriever.model.encode(
        [query],
        convert_to_numpy=True
    )

    # --------------------------------------------------------
    # Calculate similarity against all evidence
    # --------------------------------------------------------

    similarities = cosine_similarity(
        query_embedding,
        retriever.embeddings
    )[0]

    # --------------------------------------------------------
    # Find available markets
    # --------------------------------------------------------

    countries = sorted(
        set(
            segment["country"]
            for segment in retriever.segments
        )
    )

    results = []

    # --------------------------------------------------------
    # Get top evidence from every country
    # --------------------------------------------------------

    for country in countries:

        country_indices = [
            i
            for i, segment
            in enumerate(retriever.segments)
            if segment["country"] == country
        ]

        ranked_indices = sorted(
            country_indices,
            key=lambda i: similarities[i],
            reverse=True
        )

        for index in ranked_indices[
            :per_country
        ]:

            item = retriever.segments[
                index
            ].copy()

            item["score"] = float(
                similarities[index]
            )

            results.append(item)

    # --------------------------------------------------------
    # Sort final evidence by relevance
    # --------------------------------------------------------

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results


# ============================================================
# LOAD TRANSCRIPTS
# ============================================================

@st.cache_data
def load_transcripts():

    files = [
        (
            "data/Transcript_1_France.txt",
            "France"
        ),
        (
            "data/Transcript_2_Germany.txt",
            "Germany"
        ),
        (
            "data/Transcript_3_UK.txt",
            "United Kingdom"
        )
    ]

    all_segments = []

    for file_path, country in files:

        segments = parse_transcript(
            file_path,
            country
        )

        all_segments.extend(
            segments
        )

    return all_segments


# ============================================================
# LOAD LLM
# ============================================================

@st.cache_resource
def load_llm():

    return LLMClient()


# ============================================================
# INITIALIZE
# ============================================================

segments = load_transcripts()

# IMPORTANT:
# Retriever is intentionally NOT cached.
# This ensures the current EvidenceRetriever class
# is used every time Streamlit runs the application.

retriever = EvidenceRetriever(
    segments
)

llm = load_llm()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🔎 Hasamex Expert Interview Analyzer"
)

st.caption(
    "AI-powered analysis of expert interviews "
    "on the European robotic surgery market"
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "Research Dataset"
)

st.sidebar.metric(
    "Expert Responses",
    len(segments)
)

st.sidebar.metric(
    "Markets",
    3
)

st.sidebar.metric(
    "Interview Questions",
    6
)

st.sidebar.divider()

st.sidebar.caption(
    "Evidence is retrieved directly from the "
    "source transcripts. Quotes and timestamps "
    "are not generated by the LLM."
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📋 Interview Guide",
        "🔍 Cross-Call Analysis",
        "💬 Ask AI"
    ]
)


# ============================================================
# TAB 1 — INTERVIEW GUIDE
# ============================================================

with tab1:

    st.header(
        "Interview Guide Analysis"
    )

    question_number = st.selectbox(
        "Select an interview question",
        options=list(
            INTERVIEW_GUIDE.keys()
        ),
        format_func=lambda x:
            f"Q{x} — {INTERVIEW_GUIDE[x]}"
    )

    question = INTERVIEW_GUIDE[
        question_number
    ]

    if st.button(
        "Analyze Question",
        type="primary"
    ):

        with st.spinner(
            "Retrieving evidence and analyzing interviews..."
        ):

            # Question-specific retrieval
            evidence = retriever.search(
                query=question,
                top_k=3,
                question_number=question_number
            )

            # Validate source evidence
            validated = validate_evidence(
                evidence
            )

            # Generate synthesis
            result = llm.answer(
                question,
                validated
            )

        # ----------------------------------------------------
        # AI SYNTHESIS
        # ----------------------------------------------------

        st.subheader(
            "AI Synthesis"
        )

        st.write(
            result["answer"]
        )

        # ----------------------------------------------------
        # COMMON THEMES
        # ----------------------------------------------------

        if result["common_themes"]:

            st.subheader(
                "Common Themes"
            )

            for theme in result[
                "common_themes"
            ]:

                st.markdown(
                    f"• {theme}"
                )

        # ----------------------------------------------------
        # MARKET DIFFERENCES
        # ----------------------------------------------------

        if result["market_differences"]:

            st.subheader(
                "Market Differences"
            )

            for difference in result[
                "market_differences"
            ]:

                st.markdown(
                    f"**{difference['market']}** — "
                    f"{difference['difference']}"
                )

        # ----------------------------------------------------
        # SUPPORTING EVIDENCE
        # ----------------------------------------------------

        st.subheader(
            "Supporting Evidence"
        )

        for item in validated:

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.markdown(
                        f"**{item['country']}**"
                    )

                    st.caption(
                        f"{item['expert']} · "
                        f"{item['role']}"
                    )

                with col2:

                    st.metric(
                        "Timestamp",
                        item["timestamp"]
                    )

                st.markdown(
                    f"> {item['text']}"
                )

                if item["valid"]:

                    st.caption(
                        "✓ Source evidence verified"
                    )

                else:

                    st.error(
                        item["error"]
                    )


# ============================================================
# TAB 2 — CROSS-CALL ANALYSIS
# ============================================================

with tab2:

    st.header(
        "Cross-Call Analysis"
    )

    st.write(
        "Compare themes and differences across "
        "France, Germany and the United Kingdom."
    )

    cross_question = st.text_input(
        "What would you like to compare?",
        value=(
            "What are the main similarities and "
            "differences across the three markets?"
        )
    )

    if st.button(
        "Analyze Across Calls",
        type="primary"
    ):

        with st.spinner(
            "Analyzing all expert interviews..."
        ):

            # ------------------------------------------------
            # BALANCED RETRIEVAL
            #
            # France      -> Top 3
            # Germany     -> Top 3
            # United Kingdom -> Top 3
            #
            # Total       -> 9 evidence records
            # ------------------------------------------------

            evidence = balanced_search(
                retriever,
                cross_question,
                per_country=3
            )

            # Validate evidence
            validated = validate_evidence(
                evidence
            )

            # Generate synthesis
            result = llm.answer(
                cross_question,
                validated
            )

        # ----------------------------------------------------
        # CROSS-CALL SYNTHESIS
        # ----------------------------------------------------

        st.subheader(
            "Cross-Call Synthesis"
        )

        st.write(
            result["answer"]
        )

        # ----------------------------------------------------
        # COMMON THEMES
        # ----------------------------------------------------

        if result["common_themes"]:

            st.subheader(
                "Common Themes"
            )

            for theme in result[
                "common_themes"
            ]:

                st.markdown(
                    f"• {theme}"
                )

        # ----------------------------------------------------
        # MARKET DIFFERENCES
        # ----------------------------------------------------

        if result["market_differences"]:

            st.subheader(
                "Market Differences"
            )

            for difference in result[
                "market_differences"
            ]:

                st.markdown(
                    f"**{difference['market']}** — "
                    f"{difference['difference']}"
                )

        # ----------------------------------------------------
        # SUPPORTING EVIDENCE
        # ----------------------------------------------------

        st.subheader(
            "Supporting Evidence"
        )

        for item in validated:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{item['country']}** · "
                    f"{item['expert']} · "
                    f"{item['timestamp']}"
                )

                st.markdown(
                    f"> {item['text']}"
                )

                if item["valid"]:

                    st.caption(
                        "✓ Source evidence verified"
                    )

                else:

                    st.error(
                        item["error"]
                    )


# ============================================================
# TAB 3 — ASK AI
# ============================================================

with tab3:

    st.header(
        "Ask AI"
    )

    st.write(
        "Ask a free-form question across all "
        "three expert interviews."
    )

    user_question = st.text_area(
        "Your question",
        placeholder=(
            "Example: How do France and Germany "
            "differ in their purchasing priorities?"
        )
    )

    if st.button(
        "Ask",
        type="primary"
    ):

        if not user_question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching expert evidence..."
            ):

                # ------------------------------------------------
                # Balanced retrieval for free-form questions
                # ------------------------------------------------

                evidence = balanced_search(
                    retriever,
                    user_question,
                    per_country=2
                )

                # Validate source evidence
                validated = validate_evidence(
                    evidence
                )

                # Generate answer
                result = llm.answer(
                    user_question,
                    validated
                )

            # ------------------------------------------------
            # ANSWER
            # ------------------------------------------------

            st.subheader(
                "Answer"
            )

            st.write(
                result["answer"]
            )

            # ------------------------------------------------
            # COMMON THEMES
            # ------------------------------------------------

            if result["common_themes"]:

                st.subheader(
                    "Common Themes"
                )

                for theme in result[
                    "common_themes"
                ]:

                    st.markdown(
                        f"• {theme}"
                    )

            # ------------------------------------------------
            # MARKET DIFFERENCES
            # ------------------------------------------------

            if result["market_differences"]:

                st.subheader(
                    "Market Differences"
                )

                for difference in result[
                    "market_differences"
                ]:

                    st.markdown(
                        f"**{difference['market']}** — "
                        f"{difference['difference']}"
                    )

            # ------------------------------------------------
            # RETRIEVED EVIDENCE
            # ------------------------------------------------

            st.subheader(
                "Retrieved Evidence"
            )

            for item in validated:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"**{item['country']}** · "
                        f"{item['expert']}"
                    )

                    st.caption(
                        f"{item['role']} · "
                        f"{item['timestamp']}"
                    )

                    st.markdown(
                        f"> {item['text']}"
                    )

                    if item["valid"]:

                        st.caption(
                            "✓ Source evidence verified"
                        )

                    else:

                        st.error(
                            item["error"]
                        )