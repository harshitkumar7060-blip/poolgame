import streamlit as st
import random
import string
import os
import json

st.set_page_config(
    page_title="8 Ball Pool",
    page_icon="🎱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Shared state ─────────────────────────────────────────────────────────────DATA_FILE = "rooms_data.json"
def load_rooms():
   if os.path.exists(DATA_FILE):
       try:
           with open(DATA_FILE, "r") as f:
               return json.load(f)
       except Exception:
           return {}
   return {}
def save_rooms(rooms_data):
   with open(DATA_FILE, "w") as f:
       json.dump(rooms_data, f)
rooms = load_rooms()

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #071a0c !important;
    color: #e8f5e9 !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse at 15% 15%, rgba(21,128,61,0.18) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 85%, rgba(10,60,20,0.25) 0%, transparent 55%);
}
[data-testid="stHeader"], [data-testid="stToolbar"],
#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }

section.main > div.block-container {
    padding: 0.5rem 0.6rem 1rem !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}

/* ── Title ── */
.pool-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2rem;
    letter-spacing: 4px;
    text-align: center;
    background: linear-gradient(135deg, #f5c842 0%, #fff7c0 50%, #c8971a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 10px rgba(245,200,66,0.3));
    line-height: 1;
    margin-bottom: 2px;
}
.pool-sub {
    text-align: center;
    color: #5a9a5a;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.room-badge {
    display: block;
    text-align: center;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.6rem;
    letter-spacing: 8px;
    color: #f5c842;
    background: rgba(21,128,61,0.2);
    border: 1px solid rgba(245,200,66,0.25);
    border-radius: 8px;
    padding: 3px 0;
    margin-bottom: 3px;
}
.room-hint {
    text-align: center;
    font-size: 0.68rem;
    color: #4a7a4a;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

/* ── Stat strip ── */
.stat-strip {
    display: flex;
    gap: 5px;
    margin-bottom: 6px;
}
.stat-box {
    flex: 1;
    background: rgba(15,40,20,0.7);
    border: 1px solid rgba(124,186,124,0.15);
    border-radius: 7px;
    padding: 4px 2px;
    text-align: center;
}
.stat-label { font-size: 0.58rem; color: #5a8a5a; letter-spacing: 1px; text-transform: uppercase; }
.stat-val   { font-family: 'Bebas Neue', sans-serif !important; font-size: 1.1rem; color: #f5c842; }

/* ── Player name ── */
.p-name {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.05rem;
    letter-spacing: 1px;
    color: #e8f5e9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-top: 5px;
}
.p-score-pos { font-family: 'Bebas Neue', sans-serif !important; font-size: 1.15rem; color: #4ade80; text-align: center; padding-top: 4px; }
.p-score-neg { font-family: 'Bebas Neue', sans-serif !important; font-size: 1.15rem; color: #f87171; text-align: center; padding-top: 4px; }
.p-score-zer { font-family: 'Bebas Neue', sans-serif !important; font-size: 1.15rem; color: #7cba7c; text-align: center; padding-top: 4px; }

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(10,30,15,0.9) !important;
    border: 1px solid rgba(124,186,124,0.25) !important;
    border-radius: 7px !important;
    color: #e8f5e9 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    padding: 4px 6px !important;
    height: 34px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #f5c842 !important;
    box-shadow: 0 0 0 2px rgba(245,200,66,0.1) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label { display: none !important; }

[data-testid="stNumberInput"] [data-testid="stNumberInputStepDown"],
[data-testid="stNumberInput"] [data-testid="stNumberInputStepUp"] {
    display: none !important;
}

/* ── Buttons ── */
[data-testid="stFormSubmitButton"] > button,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #15803d, #166534) !important;
    color: #fff !important;
    border: 1px solid rgba(124,186,124,0.3) !important;
    border-radius: 7px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 1.5px !important;
    font-size: 0.88rem !important;
    padding: 4px 4px !important;
    height: 34px !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
[data-testid="stFormSubmitButton"] > button:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(135deg, #f5c842, #c8971a) !important;
    color: #071a0c !important;
    border-color: #f5c842 !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(10,30,15,0.7) !important;
    border-radius: 9px !important;
    padding: 3px !important;
    border: 1px solid rgba(124,186,124,0.18) !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 0.9rem !important;
    color: #7cba7c !important;
    border-radius: 6px !important;
    padding: 3px 12px !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #15803d, #166534) !important;
    color: #fff !important;
}

/* ── Form ── */
[data-testid="stForm"] {
    background: rgba(15,40,20,0.55) !important;
    border: 1px solid rgba(124,186,124,0.15) !important;
    border-radius: 10px !important;
    padding: 6px 8px !important;
}

hr { border: none !important; border-top: 1px solid rgba(124,186,124,0.12) !important; margin: 5px 0 !important; }

[data-testid="stAlert"] {
    background: rgba(15,40,20,0.7) !important;
    border: 1px solid rgba(124,186,124,0.2) !important;
    border-radius: 7px !important;
    color: #7cba7c !important;
    font-size: 0.82rem !important;
}

/* tighten columns */
[data-testid="stHorizontalBlock"] { gap: 3px !important; align-items: center !important; }
[data-testid="stColumn"] { padding: 0 !important; min-width: 0 !important; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #071a0c; }
::-webkit-scrollbar-thumb { background: #15803d; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────
def gen_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def score_html(s):
    if s > 0: return f'<div class="p-score-pos">+{s}</div>'
    if s < 0: return f'<div class="p-score-neg">{s}</div>'
    return f'<div class="p-score-zer">0</div>'


# ══════════════════════════════════════════════════════════════════════════════
# LANDING
# ══════════════════════════════════════════════════════════════════════════════
if "room_id" not in st.session_state:
    st.markdown('<p class="pool-title">🎱 8 Ball Pool</p>', unsafe_allow_html=True)
    st.markdown('<p class="pool-sub">Score Tracker</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["➕  Create Room", "🔗  Join Room"])

    with tab1:
        with st.form("create_form", clear_on_submit=True):
            room_name = st.text_input("n", placeholder="Room name e.g. Friday Night")
            if st.form_submit_button("🎱 Create Room") and room_name.strip():
                rid = gen_id()
                rooms[rid] = {"name": room_name.strip(), "players": {}}
                save_rooms(rooms)
                st.session_state.room_id = rid
                st.rerun()

    with tab2:
        with st.form("join_form", clear_on_submit=True):
            code = st.text_input("n", placeholder="Enter Room ID e.g. AB12CD").strip().upper()
            if st.form_submit_button("🔗 Join Room"):
                if code in rooms:
                    st.session_state.room_id = code
                    st.rerun()
                else:
                    st.error("Room not found!")


# ══════════════════════════════════════════════════════════════════════════════
# ROOM
# ══════════════════════════════════════════════════════════════════════════════
else:
    room_id = st.session_state.room_id
    room    = rooms.get(room_id)

    if not room:
        st.error("Room expired.")
        if st.button("← Back"):
            del st.session_state.room_id
            st.rerun()
        st.stop()

    players = room["players"]

    # ── Header ──
    st.markdown(f'<p class="pool-title">🎱 {room["name"]}</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="room-badge">{room_id}</div>'
        f'<p class="room-hint">Share this ID · others can join anytime</p>',
        unsafe_allow_html=True
    )

    # ── Stat strip ──
    if players:
        best  = max(players.values())
        worst = min(players.values())
        total = sum(players.values())
        st.markdown(
            f'''<div class="stat-strip">
                <div class="stat-box"><div class="stat-label">Players</div><div class="stat-val">{len(players)}</div></div>
                <div class="stat-box"><div class="stat-label">Best</div><div class="stat-val" style="color:#4ade80">{best:+d}</div></div>
                <div class="stat-box"><div class="stat-label">Worst</div><div class="stat-val" style="color:#f87171">{worst:+d}</div></div>
                <div class="stat-box"><div class="stat-label">Total</div><div class="stat-val">{total}</div></div>
            </div>''',
            unsafe_allow_html=True
        )

    # ── Add player (single line form) ──
    with st.form("add_player_form", clear_on_submit=True):
        c1, c2 = st.columns([4, 1])
        with c1:
            new_name = st.text_input("n", placeholder="Add player name...")
        with c2:
            submitted = st.form_submit_button("➕")
        if submitted and new_name.strip():
            name = new_name.strip()
            if name not in players:
                players[name] = 0
                save_rooms(rooms)
            st.rerun()

    # ── Player rows — one line each ──
    if not players:
        st.info("🎱 Add players above to get started!")
    else:
        for i, (name, score) in enumerate(players.items()):
            # columns: name | amt input | + | - | score | del
            c_name, c_amt, c_add, c_sub, c_score, c_del = st.columns([2.8, 1.8, 0.8, 0.8, 1.2, 0.8])

            with c_name:
                st.markdown(f'<div class="p-name">{name}</div>', unsafe_allow_html=True)

            with c_amt:
                amt = st.number_input(
                    "a", min_value=0, value=0, step=1,
                    key=f"amt_{name}", label_visibility="collapsed"
                )

            with c_add:
                if st.button("➕", key=f"add_{name}", use_container_width=True):
                    if amt > 0:
                        players[name] += amt
                        save_rooms(rooms)
                        st.rerun()

            with c_sub:
                if st.button("➖", key=f"sub_{name}", use_container_width=True):
                    if amt > 0:
                        players[name] -= amt
                        save_rooms(rooms)
                        st.rerun()

            with c_score:
                st.markdown(score_html(score), unsafe_allow_html=True)

            with c_del:
                if st.button("🗑", key=f"del_{name}", use_container_width=True):
                    del players[name]
                    save_rooms(rooms)
                    st.rerun()

    st.divider()

    # ── Footer ──
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 Reset", use_container_width=True):
            for p in players:
                players[p] = 0
            st.rerun()
    with c2:
        if st.button("🔃 Refresh", use_container_width=True):
            st.rerun()
    with c3:
        if st.button("🚪 Exit", use_container_width=True):
            del st.session_state.room_id
            st.rerun()
