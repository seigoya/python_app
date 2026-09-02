import random
import streamlit as st


st.set_page_config(
    page_title="ビンゴゲーム",
    page_icon="🎱",
    layout="centered"
)


def create_bingo_card():
    card = []

    columns = [
        list(range(1, 16)),
        list(range(16, 31)),
        list(range(31, 46)),
        list(range(46, 61)),
        list(range(61, 76)),
    ]

    for col_index in range(5):
        numbers = random.sample(columns[col_index], 5)
        card.append(numbers)

    card = [list(row) for row in zip(*card)]

    card[2][2] = "FREE"

    return card


def mark_number(card, number):
    for row in range(5):
        for col in range(5):
            if card[row][col] == number:
                card[row][col] = "X"
                return True

    return False


def check_bingo(card):
    size = 5

    def marked(cell):
        return cell == "X" or cell == "FREE"

    # 横
    for row in range(size):
        if all(marked(card[row][col]) for col in range(size)):
            return True

    # 縦
    for col in range(size):
        if all(marked(card[row][col]) for row in range(size)):
            return True

    # 左上 → 右下
    if all(marked(card[i][i]) for i in range(size)):
        return True

    # 右上 → 左下
    if all(marked(card[i][size - 1 - i]) for i in range(size)):
        return True

    return False


# -------------------------
# CSS
# -------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .bingo-header {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        padding: 8px;
        background-color: #222;
        color: white;
        border-radius: 10px;
        margin-bottom: 5px;
    }

    .bingo-cell {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        padding: 18px 4px;
        border: 2px solid #333;
        border-radius: 10px;
        margin: 3px;
        background-color: white;
    }

    .marked-cell {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        padding: 18px 4px;
        border: 2px solid #333;
        border-radius: 10px;
        margin: 3px;
        background-color: #ffdddd;
    }

    .free-cell {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        padding: 20px 4px;
        border: 2px solid #333;
        border-radius: 10px;
        margin: 3px;
        background-color: #fff1a8;
    }

    .draw-number {
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------
# 初期設定
# -------------------------

if "card" not in st.session_state:
    st.session_state.card = create_bingo_card()

if "numbers" not in st.session_state:
    st.session_state.numbers = list(range(1, 76))
    random.shuffle(st.session_state.numbers)

if "drawn_numbers" not in st.session_state:
    st.session_state.drawn_numbers = []

if "last_number" not in st.session_state:
    st.session_state.last_number = None


# -------------------------
# タイトル
# -------------------------

st.markdown(
    '<div class="main-title">🎱 ビンゴゲーム</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">ボタンを押して数字を引いてください</div>',
    unsafe_allow_html=True
)


# -------------------------
# ボタン
# -------------------------

col1, col2 = st.columns(2)

with col1:
    if st.button("🎲 数字を引く", use_container_width=True):

        if st.session_state.numbers:

            draw = st.session_state.numbers.pop()

            st.session_state.drawn_numbers.append(draw)
            st.session_state.last_number = draw

            mark_number(st.session_state.card, draw)

        else:
            st.warning("すべての数字を引きました。")


with col2:
    if st.button("🔄 新しいゲーム", use_container_width=True):

        st.session_state.card = create_bingo_card()

        st.session_state.numbers = list(range(1, 76))
        random.shuffle(st.session_state.numbers)

        st.session_state.drawn_numbers = []
        st.session_state.last_number = None

        st.rerun()


# -------------------------
# 出た数字
# -------------------------

if st.session_state.last_number is not None:

    st.markdown(
        f'<div class="draw-number">{st.session_state.last_number}</div>',
        unsafe_allow_html=True
    )

    if st.session_state.card:
        if st.session_state.last_number in st.session_state.drawn_numbers:
            st.caption("今回出た数字")


# -------------------------
# ビンゴカード
# -------------------------

headers = ["B", "I", "N", "G", "O"]

header_cols = st.columns(5)

for i in range(5):
    header_cols[i].markdown(
        f'<div class="bingo-header">{headers[i]}</div>',
        unsafe_allow_html=True
    )


for row in st.session_state.card:

    cols = st.columns(5)

    for i, cell in enumerate(row):

        if cell == "X":

            cols[i].markdown(
                '<div class="marked-cell">❌</div>',
                unsafe_allow_html=True
            )

        elif cell == "FREE":

            cols[i].markdown(
                '<div class="free-cell">⭐<br>FREE</div>',
                unsafe_allow_html=True
            )

        else:

            cols[i].markdown(
                f'<div class="bingo-cell">{cell}</div>',
                unsafe_allow_html=True
            )


# -------------------------
# ビンゴ判定
# -------------------------

if check_bingo(st.session_state.card):

    st.balloons()

    st.success("🎉 ビンゴ！おめでとうございます！")


# -------------------------
# 今まで出た数字
# -------------------------

st.markdown("---")

st.subheader("📋 今まで出た数字")

if st.session_state.drawn_numbers:

    st.write(
        "　".join(
            str(number)
            for number in st.session_state.drawn_numbers
        )
    )

else:
    st.write("まだ数字は出ていません。")


st.caption(
    f"残りの数字：{len(st.session_state.numbers)} 個"
)