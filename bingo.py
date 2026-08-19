import random


def create_bingo_card():
    """5x5 のビンゴカードを作成する"""
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

    # 真ん中のセルは FREE
    card[2][2] = "FREE"
    return card


def print_card(card):
    print("\nB  I  N  G  O")
    for row in card:
        print(" | ".join(f"{cell:>2}" for cell in row))
    print()


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

    # 横
    for row in range(size):
        if all(card[row][col] == "X" for col in range(size)):
            return True

    # 縦
    for col in range(size):
        if all(card[row][col] == "X" for row in range(size)):
            return True

    # 斜め
    if all(card[i][i] == "X" for i in range(size)):
        return True
    if all(card[i][size - 1 - i] == "X" for i in range(size)):
        return True

    return False


def main():
    print("=== ビンゴゲーム ===")
    print("1〜75の数字が出ます。カードと一致した数字をマークします。")
    card = create_bingo_card()
    print_card(card)

    numbers = list(range(1, 76))
    random.shuffle(numbers)

    for draw in numbers:
        print(f"出た数字: {draw}")
        if mark_number(card, draw):
            print("カードにあります！")
        else:
            print("カードにはありません。")

        print_card(card)

        if check_bingo(card):
            print("🎉 ビンゴ！")
            break

    print("ゲーム終了")


if __name__ == "__main__":
    main()
