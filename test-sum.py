# あるクラスの国語テストの点数をリストに代入 --- (*1)
points = [88, 76, 67, 43, 79, 80, 91]
math_points = [30, 60, 85, 62, 80, 55, 92]
# テストの合計を求める --- (*2)
sum_v = 0
for i in math_points:
    sum_v += i
    print(i,"点を足して合計は", sum_v)

# 平均を求める --- (*3)
ave_v = sum_v / len(points)
print("平均点は", ave_v, "点")

