
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="AI Chatbot Safety Tester", page_icon="🤖", layout="wide")

DATA = Path("data/test_questions.csv")
RESULTS = Path("results.csv")

questions = pd.read_csv(DATA)

st.title("🤖 AI Chatbot Safety Tester")
st.caption("Evaluate chatbot answers for correctness, clarity and safety.")

qid = st.sidebar.selectbox("Select Question", questions["id"].tolist())
row = questions[questions["id"] == qid].iloc[0]

st.subheader(f"Question {qid}")
st.info(row["question"])
st.write("**Category:**", row["category"])

response = st.text_area("Chatbot Response", height=180)
evaluation = st.selectbox("Evaluation", ["Correct","Incorrect","Unsafe","Unclear"])
notes = st.text_area("Notes")

if st.button("Save Evaluation"):
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
        rec = pd.concat([old, rec], ignore_index=True)
    rec.to_csv(RESULTS, index=False)
    st.success("Saved successfully!")

st.divider()
st.subheader("Dashboard")

if RESULTS.exists():
    df = pd.read_csv(RESULTS)
    total = len(df)
    correct = (df.evaluation=="Correct").sum()
    unsafe = (df.evaluation=="Unsafe").sum()
    error = total-correct
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Tests", total)
    c2.metric("Accuracy", f"{correct/total*100:.1f}%")
    c3.metric("Safety", f"{(total-unsafe)/total*100:.1f}%")
    c4.metric("Error Rate", f"{error/total*100:.1f}%")
    st.bar_chart(df.evaluation.value_counts())
else:
    st.info("No evaluations saved yet.")
