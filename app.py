import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Chatbot Safety Tester",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# File Paths
# -----------------------------
BASE_DIR = Path(__file__).parent
DATA = BASE_DIR / "data" / "test_questions.csv"
RESULTS = BASE_DIR / "results.csv"

# -----------------------------
# Load Questions
# -----------------------------
questions = pd.read_csv(DATA)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 AI Chatbot Safety Tester")
st.caption(
    "Evaluate chatbot answers for correctness, clarity, reliability and safety."
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("🧪 Test Configuration")

qid = st.sidebar.selectbox(
    "Select Question",
    questions["id"].tolist()
)

row = questions[questions["id"] == qid].iloc[0]

# -----------------------------
# Question
# -----------------------------
st.subheader(f"Question {qid}")

st.info(row["question"])

st.write(
    f"**Category:** `{row['category']}`"
)

# -----------------------------
# Chatbot Response
# -----------------------------
st.subheader("💬 Chatbot Response")

response = st.text_area(
    "Paste the chatbot's answer here:",
    height=180,
    placeholder="Enter the chatbot response..."
)

# -----------------------------
# Evaluation
# -----------------------------
evaluation = st.selectbox(
    "Evaluate the response",
    [
        "Correct",
        "Incorrect",
        "Unsafe",
        "Unclear"
    ]
)

notes = st.text_area(
    "Evaluation Notes",
    placeholder="Explain why you selected this evaluation..."
)

# -----------------------------
# Save
# -----------------------------
if st.button("💾 Save Evaluation", use_container_width=True):

    if not response.strip():
        st.warning("Please enter a chatbot response first.")

    else:

        rec = pd.DataFrame([{
            "id": qid,
            "category": row["category"],
            "question": row["question"],
            "chatbot_response": response,
            "evaluation": evaluation,
            "notes": notes
        }])

        if RESULTS.exists():
            old = pd.read_csv(RESULTS)
            rec = pd.concat(
                [old, rec],
                ignore_index=True
            )

        rec.to_csv(
            RESULTS,
            index=False
        )

        st.success("✅ Evaluation saved successfully!")

# -----------------------------
# Dashboard
# -----------------------------
st.divider()

st.header("📊 Evaluation Dashboard")

if RESULTS.exists():

    df = pd.read_csv(RESULTS)

    total = len(df)

    correct = (
        df["evaluation"] == "Correct"
    ).sum()

    incorrect = (
        df["evaluation"] == "Incorrect"
    ).sum()

    unsafe = (
        df["evaluation"] == "Unsafe"
    ).sum()

    unclear = (
        df["evaluation"] == "Unclear"
    ).sum()

    accuracy = (
        correct / total * 100
        if total > 0 else 0
    )

    safety = (
        (total - unsafe) / total * 100
        if total > 0 else 0
    )

    error_rate = (
        (incorrect + unsafe + unclear)
        / total * 100
        if total > 0 else 0
    )

    # Metrics
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🧪 Total Tests",
        total
    )

    c2.metric(
        "✅ Accuracy",
        f"{accuracy:.1f}%"
    )

    c3.metric(
        "🛡️ Safety",
        f"{safety:.1f}%"
    )

    c4.metric(
        "❌ Error Rate",
        f"{error_rate:.1f}%"
    )

    # Results
    st.subheader("Evaluation Results")

    result_counts = pd.Series({
        "Correct": correct,
        "Incorrect": incorrect,
        "Unsafe": unsafe,
        "Unclear": unclear
    })

    st.bar_chart(result_counts)

    # Table
    st.subheader("📋 Evaluation History")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Download
    csv = df.to_csv(index=False)

    st.download_button(
        "⬇️ Download Results CSV",
        csv,
        "chatbot_evaluation_results.csv",
        "text/csv"
    )

else:

    st.info(
        "No evaluations saved yet. "
        "Test a chatbot response above to begin."
    )
