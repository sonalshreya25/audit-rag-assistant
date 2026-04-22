import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from rag_pipeline import RAGPipeline

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Audit RAG Assistant",
    page_icon="🏦",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        background-color: #f8fafc;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e9eef5;
        padding: 12px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        text-align: center;
    }

    .main-title {
        background: linear-gradient(90deg, #dbeafe, #fce7f3);
        padding: 18px 24px;
        border-radius: 18px;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
    }

    .section-card {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 16px;
        border: 1px solid #e9eef5;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }

    .small-note {
        color: #64748b;
        font-size: 0.92rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("""
<div class="main-title">
    <h1 style="margin-bottom:0.2rem;">🏦 Audit RAG Assistant Dashboard</h1>
    <p class="small-note" style="margin-top:0;">
        Retrieve policies and audit findings, identify missing controls, and visualize audit risk.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------- LOAD DATA --------------------
def load_docs():
    with open("data/policies.txt", "r", encoding="utf-8") as f:
        policies = [x.strip() for x in f if x.strip()]
    with open("data/audit_reports.txt", "r", encoding="utf-8") as f:
        reports = [x.strip() for x in f if x.strip()]
    return policies + reports

docs = load_docs()
rag = RAGPipeline(docs)

# -------------------- SIDEBAR --------------------
st.sidebar.header("⚙️ Settings")
mode = st.sidebar.selectbox("Mode", ["Control Gap Analysis", "Q&A"])
top_k = st.sidebar.slider("Top Results", min_value=2, max_value=8, value=4)

st.sidebar.markdown("---")


# -------------------- INPUT --------------------
query = st.text_area(
    "Enter Process Description or Question",
    placeholder="Example: New vendors are onboarded by procurement. Approvals are collected through email..."
)

# -------------------- ANALYZE --------------------
if st.button("Analyze"):

    if not query.strip():
        st.warning("Please enter a process description or question.")
        st.stop()

    results = rag.retrieve(query, top_k=top_k)

    # -------------------- INSIGHT LOGIC --------------------
    text = query.lower()
    missing_controls = []

    if "dual approval" not in text and "two independent" not in text and "maker-checker" not in text:
        missing_controls.append("Dual Approval")

    if "review" not in text:
        missing_controls.append("Access Review")

    if "document" not in text and "documentation" not in text and "retained" not in text and "stored" not in text:
        missing_controls.append("Audit Evidence")

    if "segregation of duties" not in text and "sod" not in text and "separate roles" not in text:
        missing_controls.append("Segregation of Duties")

    total_controls = 4
    missing_count = len(missing_controls)
    present_count = total_controls - missing_count
    evidence_coverage = int((present_count / total_controls) * 100)
    risk_score = int((missing_count / total_controls) * 100)

    if risk_score > 70:
        risk_label = "High"
    elif risk_score > 40:
        risk_label = "Medium"
    else:
        risk_label = "Low"

    # -------------------- TOP SECTION --------------------
    left_col, right_col = st.columns([1.25, 1])

    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🔍 Retrieved Evidence")
        for text_chunk, score in results:
            st.info(f"{text_chunk}\n\n**Relevance Score:** {round(score, 2)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🧠 Audit Insights")

        if not missing_controls:
            st.success("All key controls appear to be present based on the provided description.")
        else:
            for c in missing_controls:
                st.warning(f"Missing: {c}")

        st.markdown("#### Suggested Auditor Focus")
        if missing_count >= 3:
            st.error("This process appears weakly controlled and should be prioritized for detailed review.")
        elif missing_count == 2:
            st.warning("This process has moderate control gaps and should be reviewed for compliance evidence.")
        else:
            st.success("This process appears relatively well controlled, with limited review points.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📊 Audit Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Controls Missing", missing_count)
    m2.metric("Controls Present", present_count)
    m3.metric("Risk Level", risk_label)
    m4.metric("Evidence Coverage", f"{evidence_coverage}%")

    # -------------------- CHART DATA --------------------
    controls = ["Dual Approval", "Access Review", "Audit Evidence", "Segregation of Duties"]
    status = [0 if c in missing_controls else 1 for c in controls]

    control_df = pd.DataFrame({
        "Control": controls,
        "Status": status
    })
    control_df["Status Label"] = control_df["Status"].map({1: "Present", 0: "Missing"})

    present = sum(status)
    missing = len(status) - present

    pie_df = pd.DataFrame({
        "Category": ["Present", "Missing"],
        "Count": [present, missing]
    })

    # -------------------- PASTEL COLORS --------------------
    PASTEL_GREEN = "#B8E0D2"
    PASTEL_RED = "#F6C1C1"
    PASTEL_BLUE = "#C7DDF2"
    PASTEL_YELLOW = "#F9E2AE"
    PASTEL_LAVENDER = "#D8C6F2"

    # -------------------- DASHBOARD VISUALS --------------------
    st.markdown("## 📈 Audit Analytics Dashboard")

    row1_col1, row1_col2 = st.columns(2)

    # ---------- BAR CHART ----------
    with row1_col1:
        fig_bar = px.bar(
            control_df,
            x="Control",
            y="Status",
            color="Status Label",
            color_discrete_map={
                "Present": PASTEL_GREEN,
                "Missing": PASTEL_RED
            },
            title="Control Coverage Overview",
            text="Status"
        )
        fig_bar.update_traces(textposition="outside")
        fig_bar.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=50, b=10),
            yaxis=dict(range=[0, 1.15], title="Status"),
            xaxis_title="Control",
            plot_bgcolor="white",
            paper_bgcolor="white",
            legend_title="",
            title_x=0.02
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ---------- PIE CHART ----------
    with row1_col2:
        fig_pie = px.pie(
            pie_df,
            values="Count",
            names="Category",
            color="Category",
            color_discrete_map={
                "Present": PASTEL_GREEN,
                "Missing": PASTEL_RED
            },
            title="Control Distribution",
            hole=0.45
        )
        fig_pie.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="white",
            title_x=0.02,
            legend_title=""
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    # ---------- RISK GAUGE ----------
    with row2_col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": PASTEL_LAVENDER},
                "steps": [
                    {"range": [0, 40], "color": PASTEL_GREEN},
                    {"range": [40, 70], "color": PASTEL_YELLOW},
                    {"range": [70, 100], "color": PASTEL_RED}
                ]
            }
        ))
        fig_gauge.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="white"
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # ---------- SUMMARY PANEL ----------
    with row2_col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📌 Executive Summary")

        st.markdown(f"""
        **Process Type:** {mode}  
        **Missing Controls:** {missing_count}  
        **Present Controls:** {present_count}  
        **Risk Rating:** {risk_label}  
        **Evidence Coverage:** {evidence_coverage}%  
        """)

        st.markdown("#### Auditor Recommendation")
        if risk_score > 70:
            st.error("Prioritize this workflow for immediate review and control remediation.")
        elif risk_score > 40:
            st.warning("Review this workflow for control strengthening and documentation completeness.")
        else:
            st.success("This workflow appears relatively controlled, though periodic monitoring is still recommended.")

        st.markdown("#### Suggested Next Steps")
        steps = []
        if "Dual Approval" in missing_controls:
            steps.append("- Implement maker-checker or dual approval for critical actions.")
        if "Access Review" in missing_controls:
            steps.append("- Introduce periodic access reviews for sensitive roles.")
        if "Audit Evidence" in missing_controls:
            steps.append("- Retain formal documentation and approval evidence.")
        if "Segregation of Duties" in missing_controls:
            steps.append("- Review role design to reduce SoD conflicts.")

        if steps:
            st.markdown("\n".join(steps))
        else:
            st.markdown("- Maintain periodic testing and evidence retention for current controls.")

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Enter a process description or audit-related question, then click **Analyze**.")
    st.markdown("### Good demo prompt")
    st.code(
        "New vendors are onboarded by the procurement team. Approvals are collected through email and stored informally. "
        "Users can request access to update vendor bank details, and access is granted by IT without periodic review. "
        "No centralized documentation is maintained."
    )