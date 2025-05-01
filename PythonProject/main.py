# if - else
# Nhap vao 1 so va kiem tra so do > 0 -> Nếu > 0 -> in ra: "Số này lớn hơn 0", ngược lại in ra số này < 0
# B1: Nhập 1 số nguyên (khoởi tạo 1 biến và dùng hàm input để nhập)
# s = int(input())  # Biến s được nhập từ bàn phím
"""
if s > 0:
    print("so nay lon  hon 0")
else:
    print("so nay be hon 0")
    
Bài 2: So sánh lương của hai người:
Nhập lương của hai người từ bàn phím. So sánh và in ra:
"person1" nếu người đầu tiên có lương cao hơn.
"person2" nếu người thứ hai có lương cao hơn.
Yêu cầu: Sử dụng if/else.
Nếu có > 2 điều kiện -> những điều kiệnở giữa elif ( else if)
So sánh 2 giá trị bằng nhau trong if else ( phải dùng ==)
person1 = int(input())
person2 = int(input())
if person1 > person2:
    print("nguoi dau tien dau tien co luong cao hon")
elif person1 == person2:
    print("2 nguoi co luong bang nhau")
else:
    print("nguoi thu hai cao hon")
s = int(input())
if s > 0:
    print("so nay lon  hon 0")
elif s == 0:
    print("so nay bang 0")
elif ...
else:
    print("so nay be hon 0")

VD: 3 6 9 12 18 24 30 42: đều là những số chia hết cho 3
3 : 3 = 1 dư 0 (/ /%)
18 : 3 = 6 dư 0
42 : 3 = 14 dư 0
=> Số chia hết cho 3: là số ghi chia cho 3 dư 0
=> Trong if else: 90% là mình sẽ dùng % ( chia lấy phần dư)
So sánh 2 giá trị bằng nhau trong if else ( phải dùng ==)
Nhập vào 1 số, kiểm tra số đó có chia hết cho 3 hay không -> Nếu có in ra chia hết cho 3, còn không thì in ra không chia hết
a = int(input())
if a % 3 == 0:
    print("so nay chia het cho 3")
else:
    print("khong chia het cho 3")
Bài 3:
Kiểm tra số chẵn hay lẻ:
Viết chương trình kiểm tra xem một số nguyên n nhập từ bàn phím là số chẵn hay số lẻ.
Nếu là số chẵn, in ra: "Even number". Ví dụ: số chia hết cho 2: 18 6 4
18 : 2 = 9 dư 0
Nếu là số lẻ, in ra: "Odd number".
n = int(input())
if n % 2 == 0:
    print("even number")
else:
    print("odd number")

Bài 4:
Phân loại điểm số:
Nhập vào một điểm số nguyên (trong khoảng từ 0 đến 100), phân loại theo:
≤ 50: "Weak" (Yếu)
51 → 60: "Average" (Trung bình)
61 → 75: "Good" (Khá)
76 → 90: "Very Good" (Giỏi)
90: "Excellent" (Xuất sắc)
Gợi ý: dùng if elif else
b = int(input())
if b <= 50:
    print("weak")
elif b <= 60:
    print("Average")
elif b <= 75:
    print("good")
elif b <= 90:
    print("very good")
else:
    print("excellent")

BT: Kiểm tra năm nhuận:
Nhập vào một số nguyên là năm từ bàn phím. Xác định xem năm đó có phải năm nhuận hay không.
Nếu đúng, in: "Year <năm> is a leap year!"
Nếu sai, in: "Year <năm> is not a leap year!"
-> Quy tắc:
Là năm nhuận nếu chia hết cho 4
s = int(input())
if s % 4 == 0:
    print("Year", s, "is a leap year!")
else:
    print("Year", s, "is not a leap year!")
BT: Bài 5:
In ra tên thứ trong tuần:
-> Nhập vào một số nguyên từ 0 đến 6 và in ra tên ngày tương ứng:
0: "Sunday" (Chủ Nhật)
1: "Monday" (Thứ Hai)
2: "Tuesday" (Thứ Ba)
3: "Wednesday" (Thứ Tư)
4: "Thursday" (Thứ Năm)
5: "Friday" (Thứ Sáu)
6: "Saturday" (Thứ Bảy)
 Yêu cầu: Sử dụng if/else if/else
 d = int(input())
if d == 0:
    print("sunday")
elif d == 1:
    print("monday")
elif d == 2:
    print("tuesday")
elif d == 3:
    print("wednesday")
elif d == 4:
    print("thursday")
elif d == 5:
    print("friday")
else:
    print("saturday")

Bài 6:
Thực hiện phép toán cơ bản:
 Nhập vào hai số nguyên a, b và một ký tự c từ bàn phím biểu thị phép toán (+, -, *, /). Tính và in kết quả.
 Ví dụ:
-> Nếu a = 7, b = 9, c = '+' thì in: 16.
 Yêu cầu: Dùng if/elif/else
 a = int(input())
b = int(input())
c = input()  # Nhâp từ bàn phím
if c == "+":
    print(a + b)
elif c == "-":
    print(a - b)
elif c == "*":
    print(a * b)
else:
    print(a / b)

Bài 7:
Tính phí gửi xe theo thời gian:
 Quy tắc tính phí:
+ Dưới 3 giờ: Miễn phí
+ 3h–3h29p: 4$
+ 3h30p–3h59p: 7$
+ 4h–4h29p: 11$
+ 4h30p–4h59p: 16$
+ 5h–5h29p: 22$
+ 5h30p–5h59p: 30$
+ 6h đúng: 40$
Input:

hours: số giờ đỗ.
minutes: số phút đỗ.
=> Yêu cầu: Tính và lưu phí đỗ xe vào biến parkingFee.
"""
a = int(input())  # Giờ: 2
b = int(input())  # phút: 45
# Đổi hết ra phút: 2 * 60 + 45
tongSoPhut = a * 60 + b  # 165
if tongSoPhut < 180:
    print("free")
elif tongSoPhut <= 209:
    print("4$")
elif tongSoPhut <= 239:
    print("7$")
elif tongSoPhut <= 269:
    print("11$")
elif tongSoPhut <= 299:
    print("16$")
elif tongSoPhut <= 329:
    print("22$")
elif tongSoPhut <= 369:
    print("30$")
else:
    print("40$")
