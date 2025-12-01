import streamlit as st

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="AI Chat UI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# CUSTOM CSS
# --------------------------
# st.markdown("""
#     <style>
#         /* App background */
#         .stApp {
#             background-color: #121212;
#             color: white;
#         }

#         /* Sidebar */
#         section[data-testid="stSidebar"] {
#             background-color: #0d0d0d;
#         }
#         section[data-testid="stSidebar"] * {
#             color: white !important;
#             font-weight: 600 !important;   /* <-- Bold text */
#         }

#         /* Top navigation buttons */
#         .top-nav button {
#             background: #1f1f1f !important;
#             color: white !important;
#             border-radius: 8px;
#             margin-right: 10px;
#             padding: 0.5rem 1rem;
#             border: 1px solid #333 !important;
#         }
            
#         .top-nav button:hover {
#             background: #7a3cff !important;
#         }

#         /* Cards */
#         .card {
#             background:#1e1e1e;
#             padding:15px;
#             border-radius:10px;
#             margin-bottom:20px;
#             border:1px solid #333;
#         }
#         .card p {
#             color:white;
#             font-size:1rem;
#             font-weight:600;
#         }
#     </style>
# """, unsafe_allow_html=True)

st.markdown("""
<style>

    /* TOP NAV BUTTONS (UPDATED) */

    /* Default button style */
    .top-nav button {
        background: #ffffff !important;          /* White background */
        color: #000000 !important;               /* Black icon/text */
        border-radius: 12px;
        margin-right: 20px;
        padding: 0.6rem 2rem;
        border: 1px solid #333 !important;
        transition: all 0.25s ease-in-out;
    }

    /* Hover effect: turn black + white text */
    .top-nav button:hover {
        background: #000000 !important;          /* Black */
        color: #ffffff !important;               /* White icon/text */
        border-color: #000000 !important;
        cursor: pointer;
    }

</style>
""", unsafe_allow_html=True)




# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.title("📅 Previous 30 Days")

sidebar_items = [
    "Speak Any Language",
    "Explore Philosophy",
    "Code Problem Solver",
    "Virtual Travel Buddy",
    "Healthy Living Tips",
    "Art & Music Picks",
]

for item in sidebar_items:
    st.sidebar.write(f"- {item}")

st.sidebar.markdown("---")
st.sidebar.write("⬆️ Upgrade")
st.sidebar.write("👤 Your Name")

# --------------------------
# MAIN NAV BAR
# --------------------------
st.markdown('<div class="top-nav">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("🏠 Home")
with col2:
    st.button("📄 Documentation")
with col3:
    st.button("⬇️ Download")
st.markdown('</div>', unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center; margin-top:20px;'>AI Chat</h1>", unsafe_allow_html=True)
st.write("")
st.write("")

# --------------------------
# Section builder
# --------------------------
def render_section(title, items):
    st.subheader(title)
    cols = st.columns(3)
    for i, text in enumerate(items):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="card">
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# --------------------------
# Sections
# --------------------------
render_section("🕒 Recent", [
    "Speak Any Language: Translate phrases instantly.",
    "Explore Philosophy: Discuss profound questions.",
    "Code Problem Solver: Fix issues and errors.",
])

render_section("📌 Frequent", [
    "Imagination Unleashed: Create a unique story.",
    "Learn Something New: Explain complex topics.",
    "Cooking Made Easy: Get recipes instantly.",
])

render_section("⭐ Recommended", [
    "Virtual Travel Buddy: Tour the world virtually.",
    "Healthy Living Tips: Fitness & wellness advice.",
    "Art & Music Picks: Discover creative gems.",
])

# --------------------------
# CHAT BOX WITH SEND BUTTON
# --------------------------
st.markdown("### 💬 Chat")

col_input, col_button = st.columns([5, 1])

with col_input:
    user_message = st.text_input("Type a message:", key="chat_input", label_visibility="collapsed")

with col_button:
    send = st.button("Send")

# Display message (not connected to LLM yet)
if send and user_message.strip() != "":
    st.write(f"**You:** {user_message}")
    st.write("*Bot would respond here (LLM not connected yet).*")
