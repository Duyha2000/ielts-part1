# https://docs.google.com/document/d/1n4n52y7RjgHDgp8qLMpNg1Fqi0CQp2zodFrFjWFNrOk/edit?tab=t.2k4lzdc5a0m9
"""
# BT1:
a = int(input())
if a > 0:
    print("positive")
elif a < 0:
    print("negative")
else:
    print("zero")
#BT2:
b = int(input())
if b < 13:
    print("Child")
elif b <= 19:
    print("Teenager")
elif b <= 64:
    print("adult")
else:
    print("senior")

# BT3:
c = int(input())
if c <= 50:
    print("1,700 d/kWh")
elif c <= 100:
    print("2,200 d/kWh")
else:
    print("2,800 d/kWh")
# BT4:
c = int(input())
if c % 3 == 0 and c % 5 == 0:
    print("divisible by both 3 and 5")
elif c % 3 == 0:
    print("divisible by three only")
elif c % 5 == 0:
    print("divisible by five only")
else:
    print("not divisible by 3 or 5")
#bT5:
d = int(input())
if 50 <= d <= 100:
    print("dau")
elif 50 > d >= 0:
    print("rot")
else:
    print("-1")
#bT6:
a = int(input())
b = int(input())
c = int(input())
if a + b > c and a + c > b and b + c > a and b > 0 and c > 0 and a > 0:
    print("valid triangle")
else:
    print("invalid triangle")
BT8:
a = input()
b = input()
if a == "admin" and b == "1234":
    print("login successful")
else:
    print("invalid credentials")
BT9:
d = float(input())
s = int(input())
if d >= 8.0 and s <= 3:
    print("eligible for cholarship")
else:
    print("not eligible for cholarship")
# BT10:
d = input()  # Nhập 1 ký tự: đúng 1 trong 5 trường ḥop (ký tự này)
if d == "a" or d == "e" or d == "i" or d == "o" or d == "u" or d == "A" or d == "E" or d == "I" or d == "O" or d == "U":
    print("nguyen am")
else:
    print("phụ âm")
# BT11:
a = input()
if a == "saturday" or a == "sunday":
    print("weekend")
else:
    print("weekday")

#BT12:
t = float(input())
v = float(input())
if t < 3 or v < 3:
    print("you failed due to low score")
else:
    print("passed")
    int float str bool

print("Allowed to take the entrance exam")
print("Not allowed to take the exam")

"""

has_diploma = input()
submitted_on_time = input()
has_exception_letter = input()
if has_diploma == "True" and (submitted_on_time == "True" or has_exception_letter == "True"):
    print("Allowed to take the entrance exam")
else:
    print("Not allowed to take the exam")
