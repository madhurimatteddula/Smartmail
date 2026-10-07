import streamlit as st
import re
import pandas as pd
from textblob import TextBlob


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Email Priority Assistant",
    page_icon="📧",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 30px;
}

.section-title {
    font-size: 24px;
    font-weight: 650;
    margin-top: 22px;
    margin-bottom: 12px;
}

.info-card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    background-color: rgba(128, 128, 128, 0.05);
    min-height: 105px;
}

.card-title {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 8px;
}

.card-value {
    font-size: 22px;
    font-weight: 650;
}

.summary-box {
    padding: 16px;
    border-radius: 10px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    background-color: rgba(128, 128, 128, 0.04);
    line-height: 1.6;
}

.about-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    background-color: rgba(128, 128, 128, 0.04);
    line-height: 1.7;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📧 AI Email Priority Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Understand your emails faster with intelligent priority, '
    'category, sentiment, deadline and summary analysis.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# EMAIL ANALYSIS FUNCTION
# =========================================================

def analyze_email(email):

    email_lower = email.lower()

    # -----------------------------------------------------
    # PRIORITY DETECTION
    # -----------------------------------------------------

    high_priority_words = [
        "urgent",
        "immediately",
        "as soon as possible",
        "deadline",
        "critical",
        "emergency",
        "today",
        "action required",
        "important"
    ]

    medium_priority_words = [
        "meeting",
        "reminder",
        "please review",
        "follow up",
        "response required",
        "tomorrow"
    ]

    high_count = 0
    medium_count = 0

    for word in high_priority_words:
        if word in email_lower:
            high_count += 1

    for word in medium_priority_words:
        if word in email_lower:
            medium_count += 1

    if high_count >= 2:
        priority = "🔴 HIGH"

    elif high_count == 1 or medium_count >= 2:
        priority = "🟡 MEDIUM"

    else:
        priority = "🟢 LOW"

    # -----------------------------------------------------
    # CATEGORY DETECTION
    # -----------------------------------------------------

    categories = {

        "Work": [
            "project",
            "task",
            "client",
            "office",
            "work",
            "report",
            "manager"
        ],

        "Meeting": [
            "meeting",
            "conference",
            "call",
            "discussion",
            "schedule"
        ],

        "Finance": [
            "payment",
            "invoice",
            "salary",
            "transaction",
            "bank",
            "refund"
        ],

        "Job / Career": [
            "interview",
            "job",
            "application",
            "resume",
            "recruitment",
            "offer"
        ],

        "Personal": [
            "family",
            "birthday",
            "friend",
            "personal",
            "weekend"
        ]
    }

    category_scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            if keyword in email_lower:
                score += 1

        category_scores[category] = score

    category = max(
        category_scores,
        key=category_scores.get
    )

    if category_scores[category] == 0:
        category = "General"

    # -----------------------------------------------------
    # SENTIMENT ANALYSIS
    # -----------------------------------------------------

    sentiment_score = TextBlob(email).sentiment.polarity

    if sentiment_score > 0.2:
        sentiment = "😊 Positive"

    elif sentiment_score < -0.2:
        sentiment = "😟 Negative"

    else:
        sentiment = "😐 Neutral"

    # -----------------------------------------------------
    # ACTION DETECTION
    # -----------------------------------------------------

    action_words = [
        "please",
        "submit",
        "send",
        "complete",
        "review",
        "reply",
        "respond",
        "confirm",
        "attend",
        "provide",
        "finish"
    ]

    action_required = False

    for word in action_words:

        if word in email_lower:
            action_required = True
            break

    # -----------------------------------------------------
    # DEADLINE DETECTION
    # -----------------------------------------------------

    deadline_patterns = [
        r"by \w+ \d+",
        r"before \w+ \d+",
        r"by \w+",
        r"before \w+",
        r"today",
        r"tomorrow",
        r"this week",
        r"next week"
    ]

    deadline = "Not detected"

    for pattern in deadline_patterns:

        match = re.search(
            pattern,
            email_lower
        )

        if match:
            deadline = match.group()
            break

    # -----------------------------------------------------
    # EMAIL SUMMARY
    # -----------------------------------------------------

    sentences = re.split(
        r'(?<=[.!?])\s+',
        email.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if len(sentences) == 0:

        summary = "No summary available."

    elif len(sentences) == 1:

        summary = sentences[0]

    elif len(sentences) == 2:

        summary = " ".join(sentences)

    else:

        summary = " ".join(sentences[:2])

    # -----------------------------------------------------
    # RECOMMENDED ACTION
    # -----------------------------------------------------

    if priority == "🔴 HIGH":

        recommendation = (
            "Review this email immediately and complete "
            "the required action before the deadline."
        )

    elif priority == "🟡 MEDIUM":

        recommendation = (
            "Review this email soon and complete the "
            "requested action if necessary."
        )

    else:

        recommendation = (
            "This email can be reviewed during your "
            "normal email processing time."
        )

    return {
        "priority": priority,
        "category": category,
        "sentiment": sentiment,
        "action_required": action_required,
        "deadline": deadline,
        "summary": summary,
        "recommendation": recommendation
    }


# =========================================================
# EMAIL INPUT
# =========================================================

st.markdown(
    '<div class="section-title">📩 Enter Your Emails</div>',
    unsafe_allow_html=True
)

st.write(
    "Enter one or more emails below to analyze their "
    "priority, category, sentiment, deadline, required action "
    "and summary."
)


# =========================================================
# SESSION STATE
# =========================================================

if "email_count" not in st.session_state:
    st.session_state.email_count = 1


# =========================================================
# EMAIL BOXES
# =========================================================

emails = []

for i in range(st.session_state.email_count):

    st.markdown(
        f"**Email {i + 1}**"
    )

    email = st.text_area(
        f"Email content {i + 1}",
        height=150,
        key=f"email_{i}",
        placeholder="Paste your email content here...",
        label_visibility="collapsed"
    )

    emails.append(email)


# =========================================================
# ADD EMAIL
# =========================================================

col1, col2 = st.columns([1, 4])

with col1:

    if st.button("➕ Add Email"):

        if st.session_state.email_count < 20:

            st.session_state.email_count += 1
            st.rerun()

        else:

            st.warning(
                "You can analyze up to 20 emails at a time."
            )


# =========================================================
# ANALYZE EMAILS
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "🔍 Analyze Emails",
    type="primary",
    use_container_width=True
):

    valid_emails = []

    for email in emails:

        if email.strip():
            valid_emails.append(email.strip())

    if len(valid_emails) == 0:

        st.warning(
            "Please enter at least one email before analyzing."
        )

    else:

        results = []
        detailed_results = []

        # =================================================
        # PROCESS EMAILS
        # =================================================

        for index, email in enumerate(
            valid_emails,
            start=1
        ):

            result = analyze_email(email)

            results.append({

                "Email": f"Email {index}",
                "Priority": result["priority"],
                "Category": result["category"],
                "Sentiment": result["sentiment"],
                "Action Required":
                    "Yes"
                    if result["action_required"]
                    else "No",
                "Deadline": result["deadline"],
                "Summary": result["summary"]

            })

            detailed_results.append({

                "email_number": index,
                "content": email,
                "result": result

            })

        # =================================================
        # RESULT SECTION
        # =================================================

        st.divider()

        st.markdown(
            '<div class="section-title">📊 Email Analysis Results</div>',
            unsafe_allow_html=True
        )

        # =================================================
        # COUNTS
        # =================================================

        total_count = len(results)

        high_count = 0
        medium_count = 0
        low_count = 0
        action_count = 0

        for result in results:

            if "HIGH" in result["Priority"]:
                high_count += 1

            elif "MEDIUM" in result["Priority"]:
                medium_count += 1

            else:
                low_count += 1

            if result["Action Required"] == "Yes":
                action_count += 1

        # =================================================
        # SUMMARY CARDS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Emails",
                total_count
            )

        with col2:

            st.metric(
                "🔴 High Priority",
                high_count
            )

        with col3:

            st.metric(
                "🟡 Medium Priority",
                medium_count
            )

        with col4:

            st.metric(
                "📌 Action Required",
                action_count
            )

        # =================================================
        # EMAIL OVERVIEW
        # =================================================

        st.markdown(
            '<div class="section-title">📨 Email Overview</div>',
            unsafe_allow_html=True
        )

        results_df = pd.DataFrame(results)

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # SUMMARIZED EMAILS
        # =================================================

        st.markdown(
            '<div class="section-title">📝 Summarized Emails</div>',
            unsafe_allow_html=True
        )

        st.write(
            "Concise summaries of the analyzed emails are shown below."
        )

        for item in detailed_results:

            result = item["result"]

            st.markdown(
                f"### Email {item['email_number']} — "
                f"{result['priority']}"
            )

            st.markdown(
                f"""
                <div class="summary-box">
                    <b>Summary:</b><br>
                    {result["summary"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                f"**Category:** {result['category']}  |  "
                f"**Sentiment:** {result['sentiment']}  |  "
                f"**Deadline:** {result['deadline']}"
            )

            st.write(
                f"**Action Required:** "
                f"{'Yes' if result['action_required'] else 'No'}"
            )

            st.info(
                result["recommendation"]
            )

        # =================================================
        # ANALYTICS
        # =================================================

        st.markdown(
            '<div class="section-title">📈 Email Analytics</div>',
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # PRIORITY DISTRIBUTION
        # -------------------------------------------------

        priority_data = pd.DataFrame({

            "Priority": [
                "High",
                "Medium",
                "Low"
            ],

            "Emails": [
                high_count,
                medium_count,
                low_count
            ]
        })

        st.markdown("### Priority Distribution")

        st.bar_chart(
            priority_data.set_index("Priority")
        )

        # -------------------------------------------------
        # CATEGORY DISTRIBUTION
        # -------------------------------------------------

        category_counts = {}

        for result in results:

            category = result["Category"]

            if category in category_counts:
                category_counts[category] += 1

            else:
                category_counts[category] = 1

        category_data = pd.DataFrame({

            "Category": list(
                category_counts.keys()
            ),

            "Emails": list(
                category_counts.values()
            )
        })

        st.markdown("### Category Distribution")

        st.bar_chart(
            category_data.set_index("Category")
        )

        # -------------------------------------------------
        # SENTIMENT DISTRIBUTION
        # -------------------------------------------------

        sentiment_counts = {}

        for result in results:

            sentiment = result["Sentiment"]

            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1

            else:
                sentiment_counts[sentiment] = 1

        sentiment_data = pd.DataFrame({

            "Sentiment": list(
                sentiment_counts.keys()
            ),

            "Emails": list(
                sentiment_counts.values()
            )
        })

        st.markdown("### Sentiment Distribution")

        st.bar_chart(
            sentiment_data.set_index("Sentiment")
        )


# =========================================================
# ABOUT
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">ℹ️ About</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="about-box">

    <b>AI Email Priority Assistant</b> helps users quickly
    understand and organize their emails.

    The application analyzes email content to identify
    important messages, priority levels, categories,
    sentiment, deadlines, required actions and concise
    summaries.

    It provides the analysis in a clear format so users
    can quickly understand which emails need their attention.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

st.caption(
    "AI Email Priority Assistant"
)
