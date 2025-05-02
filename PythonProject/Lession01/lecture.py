# Scratch (<10t), Python, C++, Java
# Python , C++ (khó hơn)
# print("Xin chào")
#  Toán - tin
# Biến:
# 1 chữ nhật, có chiều dài - chiều rộng -> tính diện tích chữ nhật
# x = chieudai = 3
# y = chieurong = 4

# dientich = chieudai * chieurong ( 3 * 4)
# Chu vi tam giac:
# a, b, c => a + b + c

# Kiểu dữ liệu
"""
a = 3  # int - integer: số nguyên: -17, 18
b = 6.3  # float: số thập phân
c = "Hello"  # String (str)
d = True  # bool (boolean: True/False)
# Kiểm tra kiểu dữ liệu 1 biến: dùng type(): kiểu
# print(type(a)  # kiểm tra kiểu dữ liệu biến
print(type(c))
# Ghi chú (chú thích)
"""
"""
x = a 
b = c
c = d
=> Chú thích nhiều dòng (""" """)
Ghi chú: 1. Note lại được
         2. Sửa lỗi
"""
x = 4
# print(x)

# 1 số loại toán tử trong Python: + - * /
length = 3
width = 2
# print(length * width)
# Khởi tạo 1 biến bán kính và tính diện tích hình tròn(r * r * PI), chu vi (2 * PI * bankinh)
r = 5
pi = 3.14
# print(2 * pi * r)  # Chu vi
# print(r * r * pi)
# Diện tích
# print(5 / 2)  # 2.5
# //: chia lấy phần nguyên, %: chia lấy phần dư:

# Ví dụ: 11 : 4 = 2 dư 3,
# 34 : 5 = 6 dư 4:
# print(34 // 5)  # 6
# print(34 % 5)  # 4
"""
"""
"""
Bài 2: Phép toán đơn giản
Viết chương trình khai báo hai số a và b, sau đó in ra:
Tổng, hiệu, tích, thương (/),  nguyên (//), dư (%).
a = 65
b = 6
print(a + b)  # 71
print(a - b)  # 59
print(a / b)  # 10.888
print(a * b)  # 390
print(a % b)  # 5
print(a // b)  # 10

🔸 Bài 3: Đổi nhiệt độ
Viết chương trình nhận giá trị nhiệt độ bằng độ C (celsius) và đổi sang độ F theo công thức:
fahrenheit = celsius * 9/5 + 32 
ctrl C -> ctrl V
👉 Yêu cầu: Dùng kiểu float.
c = 54
f = c * 9 / 5 + 32
print(f)

🔸 Bài 4: Tính diện tích hình chữ nhật và chu vi hình chữ nhật
Khai báo hai biến width và height rồi tính diện tích hình chữ nhật:
area = width * height
w = 2
h = 3
a = w * h
p = 2 * (w + h)
print(a)
print(p)
a = 6
b = 2
c = 9
d = (a + b + c) / 3
print(d)

✅ Bài 6: Tính tuổi
Mô tả: Cho 1 năm sinh, tính tuổi (giả sử năm hiện tại là 2025).
Input:
2000
Output:
-> Tuổi của bạn là: 25
a = 25
b = 2025
c = b - a
print("Tuổi của bạn là", c)
Giá trị in để sau , ; biến in trong " "
🔸 Bài 1: Khai báo và in biến
Viết chương trình khai báo các biến "name, age, height" và in ra thông tin theo định dạng:
Họ tên: <name>, Tuổi: <age>, Chiều cao: <height> cm
👉 Gợi ý: Dùng kiểu str, int, float.
n = "huy"
a = 13
h = 160
print("Họ tên", n, "Tuổi ", a, " Chiều cao ", h)

🔸 Bài 2: Khai báo và in biến
Viết chương trình khai báo các biến "address, sdt, class" 
a = "243/ phường 2"
sdt = "0384258679"
c = "9/4"
print("Dia chi", a, "so dien thoai", sdt, "lop hoc", c) print
input()

Nhap 2 biến tên, địa chỉ => in ra thông tin
=> Khởi tạo 2 biến và nhập bằng input()
name = input()
print(name)
address = input()  # str
print(address)

Nhập chiều dài, chiều rộng -> in ra diện tích HCN
chieudai = int(input())
chieurong = int(input())
print(chieudai * chieurong)

✅ Bài 6: Tính tuổi
Mô tả: Nhập năm sinh, tính tuổi (giả sử năm hiện tại là 2025).
Input:
2000
Output:
Tuổi của bạn là: 25
namsinh = int(input())  # 2000
hientai = 2025  # Ko input ( vì biết chính xác giá trị)
age = hientai - namsinh
print("tuoi cua ban la", age)

Nhập bán kính hình tròn
-> in ra:
Diện tích hình tròn là: ...
Chu vi hình tròn là:
r = int(input())
pi = 3.14
dtht = r * r * pi
cvht = 2 * r * pi
print("Diện tích hình tròn là:", dtht)
print("Chu vi hình tròn là:", cvht)

If - else:
Nếu hôm nay trời mưa, tôi sẽ ở nhà
Nếu em học giỏi, mẹ sẽ mua iphone cho em, nếu không thì mẹ sẽ cắt mạng 
Nếu em thi cuối kỳ > 5 điểm, em sẽ qua môn , nếu không thi ở lại lớp
diem = int(input())
if diem > 5:
    print("Qua mon")
else:
    print("Ở lại lớp")

Nhập vào 1 số, kiểm tra số này > 0 hay không
-> Nếu có, in ra số > 0
Nếu không, in ra số này < 0
so = int(input())
if so > 0:
    print(">0")
else:
    print("<0")

Các phép toán so sánh: > < >= <= ==: bằng !=: khác
a = 3 
b = 4
a = 3
b = 3
print(a == b)  # True
"""
# Nhập 2 số a và b và kiểm tra số nào lớn hơn, nếu a > b thì in ra "số a lớn hơn" và ngược lại
a = int(input())
b = int(input())
if a > b:
    print("so a lon hon")
else:
    print("so a be hon")
