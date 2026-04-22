import streamlit as st
import random
import string

st.set_page_config(
    page_title="8 Ball Pool Tracker",
    page_icon="🎱",
    layout="centered"
)

# ── Shared state ────────────────────────────────────────────────────────────
if "rooms" not in st.__dict__:
    st.__dict__["rooms"] = {}
rooms = st.__dict__["rooms"]

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a1a0f !important;
    color: #e8f5e9 !important;
}
[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(21,128,61,0.18) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(10,60,20,0.25) 0%, transparent 60%),
        repeating-linear-gradient(
            0deg, transparent, transparent 39px,
            rgba(255,255,255,0.018) 39px, rgba(255,255,255,0.018) 40px
        ),
        repeating-linear-gradient(
            90deg, transparent, transparent 39px,
            rgba(255,255,255,0.018) 39px, rgba(255,255,255,0.018) 40px
        );
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
section.main > div { padding-top: 2rem !important; }

/* ── Typography ── */
* { font-family: 'Rajdhani', sans-serif !important; }
h1, h2, h3 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 2px !important; }

/* ── Title ── */
.pool-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 3.2rem;
    letter-spacing: 4px;
    text-align: center;
    background: linear-gradient(135deg, #f5c842 0%, #fff7c0 50%, #c8971a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
    line-height: 1.1;
    text-shadow: none;
    filter: drop-shadow(0 0 18px rgba(245,200,66,0.35));
}
.pool-subtitle {
    text-align: center;
    color: #7cba7c;
    font-size: 1rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0;
    margin-bottom: 2rem;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(124,186,124,0.2) !important;
    margin: 1.5rem 0 !important;
}

/* ── Room ID badge ── */
.room-badge {
    display: inline-block;
    background: rgba(21,128,61,0.25);
    border: 1px solid rgba(124,186,124,0.4);
    border-radius: 8px;
    padding: 6px 18px;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.5rem;
    letter-spacing: 6px;
    color: #f5c842;
    margin-bottom: 4px;
}
.room-share-hint {
    font-size: 0.82rem;
    color: #5a8a5a;
    letter-spacing: 1px;
}

/* ── Cards / Containers ── */
[data-testid="stForm"] {
    background: rgba(15,40,20,0.7) !important;
    border: 1px solid rgba(124,186,124,0.2) !important;
    border-radius: 14px !important;
    padding: 1.2rem 1.4rem !important;
    backdrop-filter: blur(6px);
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(10,30,15,0.85) !important;
    border: 1px solid rgba(124,186,124,0.3) !important;
    border-radius: 8px !important;
    color: #e8f5e9 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #f5c842 !important;
    box-shadow: 0 0 0 2px rgba(245,200,66,0.15) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label { color: #7cba7c !important; font-weight: 600 !important; letter-spacing: 1px !important; }

/* ── Buttons ── */
[data-testid="stFormSubmitButton"] > button,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #15803d, #166534) !important;
    color: #fff !important;
    border: 1px solid rgba(124,186,124,0.4) !important;
    border-radius: 8px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 1rem !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFormSubmitButton"] > button:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(135deg, #f5c842, #c8971a) !important;
    color: #0a1a0f !important;
    border-color: #f5c842 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(245,200,66,0.3) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(10,30,15,0.6) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid rgba(124,186,124,0.2) !important;
    gap: 4px !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 1rem !important;
    color: #7cba7c !important;
    border-radius: 7px !important;
    padding: 6px 20px !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #15803d, #166534) !important;
    color: #fff !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(15,40,20,0.7) !important;
    border: 1px solid rgba(124,186,124,0.2) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    text-align: center !important;
}
[data-testid="stMetricLabel"] { color: #7cba7c !important; font-size: 0.8rem !important; letter-spacing: 2px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { font-family: 'Bebas Neue', sans-serif !important; font-size: 2rem !important; color: #f5c842 !important; letter-spacing: 2px !important; }

/* ── Player row card ── */
.player-row {
    background: rgba(15,40,20,0.65);
    border: 1px solid rgba(124,186,124,0.18);
    border-radius: 12px;
    padding: 10px 16px;
    margin-bottom: 8px;
    backdrop-filter: blur(4px);
    transition: border-color 0.2s;
}
.player-row:hover { border-color: rgba(124,186,124,0.4); }

.player-name-label {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.3rem;
    letter-spacing: 2px;
    color: #e8f5e9;
}
.leader-crown { color: #f5c842; margin-right: 4px; }

.score-positive { color: #4ade80 !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 1.8rem !important; text-align: center; }
.score-negative { color: #f87171 !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 1.8rem !important; text-align: center; }
.score-zero     { color: #7cba7c !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 1.8rem !important; text-align: center; }

/* ── Info / error ── */
[data-testid="stAlert"] {
    background: rgba(15,40,20,0.7) !important;
    border: 1px solid rgba(124,186,124,0.3) !important;
    border-radius: 10px !important;
    color: #7cba7c !important;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] { color: #5a8a5a !important; font-size: 0.85rem !important; letter-spacing: 1px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a1a0f; }
::-webkit-scrollbar-thumb { background: #15803d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ─────────────────────────────────────────────────────────────────
def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def score_class(score):
    if score > 0: return "score-positive"
    if score < 0: return "score-negative"
    return "score-zero"


# ── Landing Screen ───────────────────────────────────────────────────────────
if "room_id" not in st.session_state:

    st.markdown('<p class="pool-title">🎱 8 Ball Pool</p>', unsafe_allow_html=True)
    st.markdown('<p class="pool-subtitle">Score Tracker</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["➕  Create Room", "🔗  Join Room"])

    with tab1:
        with st.form("create_form", clear_on_submit=True):
            room_name = st.text_input("Room Name", placeholder="e.g. Friday Night Pool")
            if st.form_submit_button("🎱 Create Room") and room_name.strip():
                room_id = generate_room_id()
                rooms[room_id] = {"name": room_name.strip(), "players": {}}
                st.session_state.room_id = room_id
                st.rerun()

    with tab2:
        with st.form("join_form", clear_on_submit=True):
            code = st.text_input("Room ID", placeholder="e.g. AB12CD").strip().upper()
            if st.form_submit_button("🔗 Join Room"):
                if code in rooms:
                    st.session_state.room_id = code
                    st.rerun()
                else:
                    st.error("❌ Room not found — double-check the ID!")


# ── Room Screen ──────────────────────────────────────────────────────────────
else:
    room_id = st.session_state.room_id
    room    = rooms.get(room_id)

    if not room:
        st.error("Room expired or not found.")
        if st.button("← Go Back"):
            del st.session_state.room_id
            st.rerun()

    else:
        # ── Header ──
        st.markdown(f'<p class="pool-title">🎱 {room["name"]}</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:center;margin-bottom:1.5rem;">'
            f'<div class="room-badge">{room_id}</div><br>'
            f'<span class="room-share-hint">Share this Room ID with others to join</span>'
            f'</div>',
            unsafe_allow_html=True
        )

        col_exit, col_refresh = st.columns([1, 1])
        with col_exit:
            if st.button("🚪 Exit Room", use_container_width=True):
                del st.session_state.room_id
                st.rerun()
        with col_refresh:
            if st.button("🔃 Refresh Scores", use_container_width=True):
                st.rerun()

        st.divider()

        # ── Add Player ──
        with st.form("add_player_form", clear_on_submit=True):
            new_name = st.text_input("Player Name", placeholder="Enter player name...")
            if st.form_submit_button("➕ Add Player") and new_name.strip():
                name = new_name.strip()
                if name not in room["players"]:
                    room["players"][name] = 0
                else:
                    st.warning(f"'{name}' already exists!")
                st.rerun()

        players = room["players"]

        # ── Stats ──
        if players:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🎮 Players",    len(players))
            c2.metric("🏆 High Score", max(players.values()))
            c3.metric("📉 Low Score",  min(players.values()))
            c4.metric("∑ Total",       sum(players.values()))

            st.divider()

            # ── Player Rows ──
            sorted_players = sorted(players.items(), key=lambda x: x[1], reverse=True)

            for i, (name, score) in enumerate(sorted_players):
                is_leader = i == 0 and len(players) > 1
                with st.container():
                    st.markdown('<div class="player-row">', unsafe_allow_html=True)

                    col_name, col_amt, col_add, col_sub, col_score, col_del = st.columns([3, 2, 1, 1, 2, 1])

                    with col_name:
                        prefix = "👑 " if is_leader else "🎱 "
                        st.markdown(
                            f'<div class="player-name-label">{prefix}{name}</div>',
                            unsafe_allow_html=True
                        )

                    with col_amt:
                        amt = st.number_input(
                            "Points", min_value=0, value=0, step=1,
                            key=f"amt_{name}", label_visibility="collapsed"
                        )

                    with col_add:
                        if st.button("➕", key=f"add_{name}", use_container_width=True) and amt > 0:
                            room["players"][name] += amt
                            st.rerun()

                    with col_sub:
                        if st.button("➖", key=f"sub_{name}", use_container_width=True) and amt > 0:
                            room["players"][name] -= amt
                            st.rerun()

                    with col_score:
                        cls = score_class(score)
                        st.markdown(
                            f'<div class="{cls}">{score:+d}</div>' if score != 0
                            else f'<div class="{cls}">0</div>',
                            unsafe_allow_html=True
                        )

                    with col_del:
                        if st.button("🗑️", key=f"del_{name}", use_container_width=True):
                            del room["players"][name]
                            st.rerun()

                    st.markdown('</div>', unsafe_allow_html=True)

            st.divider()

            if st.button("🔄 Reset All Scores", use_container_width=True):
                for p in room["players"]:
                    room["players"][p] = 0
                st.rerun()

        else:
            st.info("🎱 No players yet — add some above to get started!")