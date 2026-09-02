import random
import streamlit as st


def create_bingo_card():
    """5x5のビンゴカードを作成する"""
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

    # 各列の数を横に並べる
    card = [list(row) for row in zip(*card)]

    # 真ん中をFREEにする
    card[2][2] = "FREE"

    return card


def mark_number(card, number):
    """カード内の数字をマークする"""
    for row in range(5):
        for col in range(5):
            if card[row][col] == number:
                card[row][col] = "X"
                return True

    return False


def check_bingo(card):
    """横・縦・斜めのビンゴ判定"""
    size = 5

    # FREEをXとして扱うための関数
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

    # 斜め
    if all(marked(card[i][i]) for i in range(size)):
        return True

    if all(marked(card[i][size - 1 - i]) for i in range(size)):
        return True

    return False


# -------------------------
# Web画面
# -------------------------

st.title("🎱 ビンゴゲーム")

st.write("1〜75の数字をランダムに引きます。")


# 最初だけカードを作る
if "card" not in st.session_state:
    st.session_state.card = create_bingo_card()

if "numbers" not in st.session_state:
    st.session_state.numbers = list(range(1, 76))
    random.shuffle(st.session_state.numbers)

if "drawn_numbers" not in st.session_state:
    st.session_state.drawn_numbers = []


# 新しいゲーム
if st.button("🔄 新しいゲーム"):
    st.session_state.card = create_bingo_card()

    st.session_state.numbers = list(range(1, 76))
    random.shuffle(st.session_state.numbers)

    st.session_state.drawn_numbers = []

    st.rerun()


# 数字を引く
if st.button("🎲 数字を引く"):

    if st.session_state.numbers:

        draw = st.session_state.numbers.pop()

        st.session_state.drawn_numbers.append(draw)

        st.subheader(f"出た数字：{draw}")

        if mark_number(st.session_state.card, draw):
            st.success("カードにあります！")

        else:
            st.info("カードにはありません。")

    else:
        st.warning("すべての数字を引きました。")


# -------------------------
# ビンゴカード表示
# -------------------------

st.subheader("あなたのビンゴカード")

headers = ["B", "I", "N", "G", "O"]

cols = st.columns(5)

for i in range(5):
    cols[i].markdown(f"### {headers[i]}")


for row in st.session_state.card:

    cols = st.columns(5)

    for i, cell in enumerate(row):

        if cell == "X":
            cols[i].markdown("## ❌")

        elif cell == "FREE":
            cols[i].markdown("## ⭐")

        else:
            cols[i].markdown(f"## {cell}")


# -------------------------
# ビンゴ判定
# -------------------------

if check_bingo(st.session_state.card):
    st.balloons()
    st.success("🎉 ビンゴ！")


# 今まで出た数字
st.subheader("今まで出た数字")

if st.session_state.drawn_numbers:
    st.write(st.session_state.drawn_numbers)

else:
    st.write("まだ数字は出ていません。") 