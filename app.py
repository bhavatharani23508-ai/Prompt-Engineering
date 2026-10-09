
import streamlit as st
from prompt_templates import TECHNIQUES, get_prompt
from llm import generate_response

st.set_page_config(
    page_title="Prompt Comparison Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- THEME STATE ----------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "comparison_results" not in st.session_state:
    st.session_state.comparison_results = []

dark = st.session_state.dark_mode

# ---------------- THEME STYLING ----------------
if dark:
    bg = "#101426"
    surface = "#1b2138"
    text = "#f3f5ff"
    muted = "#b7c0dc"
    border = "#343d5d"
    input_bg = "#252d47"
else:
    bg = "#f5f6ff"
    surface = "#ffffff"
    text = "#20264a"
    muted = "#68718d"
    border = "#e2e5f4"
    input_bg = "#ffffff"

st.markdown(f"""
<style>
.stApp {{
    background: {bg};
    color: {text};
}}
[data-testid="stHeader"] {{
    background: transparent;
}}
.block-container {{
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #252a72 0%, #5540a8 55%, #8b45b6 100%);
}}
section[data-testid="stSidebar"] * {{
    color: white !important;
}}
.hero {{
    background: linear-gradient(120deg, #3149c9, #7852d6, #b44db4);
    padding: 30px;
    border-radius: 22px;
    color: white;
    margin: 10px 0 24px 0;
    box-shadow: 0 8px 28px rgba(81, 67, 180, 0.20);
}}
.hero h1 {{
    color: white;
    font-size: 36px;
    margin-bottom: 8px;
}}
.hero p {{
    color: #f1efff;
    font-size: 16px;
}}
div[data-testid="stMetric"] {{
    background: {surface};
    border: 1px solid {border};
    border-radius: 16px;
    padding: 18px;
}}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: {text};
}}
.technique-card {{
    background: {surface};
    border: 1px solid {border};
    border-radius: 17px;
    padding: 20px;
    min-height: 150px;
    margin-bottom: 14px;
    color: {text};
    box-shadow: 0 4px 15px rgba(50, 60, 120, 0.06);
}}
.technique-card h3 {{
    color: {text};
    font-size: 19px;
}}
.technique-card p {{
    color: {muted};
    font-size: 14px;
}}
.section-caption {{
    color: {muted};
    font-size: 14px;
}}
div[data-testid="stExpander"] {{
    background: {surface};
    border: 1px solid {border};
    border-radius: 14px;
}}
.stTextArea textarea, .stTextInput input {{
    background: {input_bg};
    color: {text};
}}
h1, h2, h3, p, label {{
    color: {text};
}}
</style>
""", unsafe_allow_html=True)

# ---------------- TOP BAR ----------------
top_left, top_right = st.columns([5, 1])

with top_left:
    st.markdown(
        f"<h3 style='margin:0;color:{text}'>🧪 Prompt Lab</h3>",
        unsafe_allow_html=True
    )

with top_right:
    button_label = "☀️ Light Mode" if dark else "🌙 Dark Mode"
    if st.button(button_label, use_container_width=True):
        st.session_state.dark_mode = not dark
        st.rerun()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 🧪 Prompt Lab")
    st.caption("Your interactive prompt engineering studio")
    st.divider()

    page = st.radio(
        "Navigate",
        ["Dashboard", "Prompt Workspace", "About"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### ✨ Experiment")
    st.caption("Compare prompts. Evaluate results. Learn what works.")
    st.caption("Python · Streamlit · Groq")

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Prompt Comparison Lab ✨</h1>
        <p>One task. Six prompting techniques. Discover how the prompt
        changes the response.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("🧠 Prompt Techniques", len(TECHNIQUES))
    c2.metric("⭐ Evaluation Criteria", "3")
    c3.metric("⚡ AI Provider", "Groq")

    st.markdown("## 🎨 Explore the Techniques")
    st.markdown(
        '<p class="section-caption">Choose a technique in the workspace '
        'to start experimenting.</p>',
        unsafe_allow_html=True
    )

    descriptions = {
        "Zero-shot": (
            "⚡", "#3478f6",
            "Give the model a task without examples."
        ),
        "One-shot": (
            "💡", "#8957e5",
            "Provide one example to guide the response."
        ),
        "Few-shot": (
            "🎯", "#14a98b",
            "Use multiple examples to guide the output."
        ),
        "CoT": (
            "🪜", "#ed8a27",
            "Request a concise explanation of key steps."
        ),
        "Manual CoT": (
            "📝", "#e65383",
            "Give the model a clear sequence of steps."
        ),
        "ToT": (
            "🌳", "#08a5b5",
            "Compare different possible approaches."
        )
    }

    columns = st.columns(3)

    for index, technique in enumerate(TECHNIQUES):
        emoji, accent, description = descriptions.get(
            technique,
            ("✨", "#7852d6", "Explore this technique.")
        )

        with columns[index % 3]:
            st.markdown(
                f"""
                <div class="technique-card"
                     style="border-top:4px solid {accent};">
                    <h3>{emoji} {technique}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div style="
            padding:18px;
            border-radius:14px;
            background:linear-gradient(100deg,#e8efff,#f6e9ff);
            color:#30346c;
            margin-top:8px;">
            🚀 <b>Ready to experiment?</b>
            Open Prompt Workspace in the sidebar and run your first comparison.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- PROMPT WORKSPACE ----------------
elif page == "Prompt Workspace":

    st.markdown("## 🚀 Prompt Workspace")
    st.write(
        "Enter one task and compare responses from different "
        "prompting techniques."
    )

    task = st.text_area(
        "📝 Your task",
        placeholder=(
            "Example: Write an SQL query to find the top 5 products "
            "by sales."
        ),
        height=130
    )

    selected = st.multiselect(
        "Choose prompting techniques",
        options=TECHNIQUES,
        default=TECHNIQUES
    )

    if st.button(
        "✨ Run Comparison",
        type="primary",
        use_container_width=True
    ):
        if not task.strip():
            st.warning("Please enter a task first.")
        elif not selected:
            st.warning("Select at least one prompting technique.")
        else:
            results = []
            progress = st.progress(0)
            status = st.empty()

            for index, technique in enumerate(selected):
                status.write(f"Generating response: **{technique}**")

                try:
                    prompt = get_prompt(technique, task)
                    response = generate_response(prompt)

                    results.append({
                        "technique": technique,
                        "prompt": prompt,
                        "response": response,
                        "clarity": 3,
                        "relevance": 3,
                        "format": 3,
                        "error": False
                    })

                except Exception as error:
                    results.append({
                        "technique": technique,
                        "prompt": "",
                        "response": str(error),
                        "clarity": 3,
                        "relevance": 3,
                        "format": 3,
                        "error": True
                    })

                progress.progress((index + 1) / len(selected))

            st.session_state.comparison_results = results
            status.success("Comparison finished!")
            progress.empty()

    results = st.session_state.comparison_results

    if results:
        st.divider()
        st.markdown("## 📊 Compare Responses")
        st.caption("Rate each successful response from 1 to 5.")

        for index, result in enumerate(results):
            with st.expander(
                f"{'⚠️' if result['error'] else '✨'} "
                f"{result['technique']}",
                expanded=True
            ):
                if result["error"]:
                    st.error("Response generation failed.")
                    st.code(result["response"])
                    continue

                st.markdown("**🤖 AI Response**")
                st.write(result["response"])

                with st.expander("🔎 View prompt sent to the model"):
                    st.code(result["prompt"])

                a, b, c = st.columns(3)

                result["clarity"] = a.slider(
                    "Clarity", 1, 5, result["clarity"],
                    key=f"clarity_{index}"
                )
                result["relevance"] = b.slider(
                    "Relevance", 1, 5, result["relevance"],
                    key=f"relevance_{index}"
                )
                result["format"] = c.slider(
                    "Output Format", 1, 5, result["format"],
                    key=f"format_{index}"
                )

        successful = [
            item for item in results if not item["error"]
        ]

        if successful:
            st.divider()

            if st.button(
                "🏆 Calculate Evaluation Results",
                use_container_width=True
            ):
                scores = []

                for item in successful:
                    average = (
                        item["clarity"]
                        + item["relevance"]
                        + item["format"]
                    ) / 3
                    scores.append((item["technique"], average))

                st.markdown("## 🏆 Evaluation Summary")

                for technique, score in scores:
                    st.write(f"**{technique}** — {score:.2f}/5")
                    st.progress(score / 5)

                best_name, best_score = max(
                    scores, key=lambda x: x[1]
                )
                st.success(
                    f"Highest-rated technique: {best_name} "
                    f"({best_score:.2f}/5)"
                )

            report = "# Prompt Comparison Lab Report\n\n"

            for item in results:
                report += f"## {item['technique']}\n\n"

                if item["error"]:
                    report += f"**Error:** {item['response']}\n\n"
                    continue

                average = (
                    item["clarity"]
                    + item["relevance"]
                    + item["format"]
                ) / 3

                report += f"**Prompt:**\n\n{item['prompt']}\n\n"
                report += f"**Response:**\n\n{item['response']}\n\n"
                report += (
                    f"**Clarity:** {item['clarity']}/5  \n"
                    f"**Relevance:** {item['relevance']}/5  \n"
                    f"**Format:** {item['format']}/5  \n"
                    f"**Average:** {average:.2f}/5\n\n---\n\n"
                )

            st.download_button(
                "⬇️ Download Experiment Report",
                data=report,
                file_name="prompt_comparison_report.md",
                mime="text/markdown",
                use_container_width=True
            )

# ---------------- ABOUT ----------------
else:

    st.markdown("## 📚 About Prompt Comparison Lab")

    st.write(
        "This application explores how different prompting techniques "
        "influence large language model responses."
    )

    st.markdown("### 🧠 Techniques Covered")
    st.markdown("""
    - **Zero-shot:** No examples are provided.
    - **One-shot:** One example is provided.
    - **Few-shot:** Multiple examples are provided.
    - **CoT:** Requests concise key steps.
    - **Manual CoT:** Provides an explicit sequence of steps.
    - **ToT:** Compares multiple possible approaches.
    """)

    st.markdown("### ⭐ Evaluation Criteria")
    st.markdown("""
    - Clarity
    - Relevance
    - Output format
    """)

    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    - Python
    - Streamlit
    - Groq API
    - Large Language Models
    - Prompt Templates
    """)

    st.info(
        "CoT asks for a concise explanation of key steps, "
        "not private internal reasoning."
    )