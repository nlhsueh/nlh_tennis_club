from members.models import Member
import datetime

# 定義 10 位會員的資料清單
members_data = [
    {"firstname": "Albert", "lastname": "Ma", "phone": 912345678, "joined_date": datetime.date(2024, 1, 5)},
    {"firstname": "Alice", "lastname": "Wang", "phone": 923456789, "joined_date": datetime.date(2024, 1, 12)},
    {"firstname": "Bob", "lastname": "Chen", "phone": 934567890, "joined_date": datetime.date(2024, 2, 15)},
    {"firstname": "Carol", "lastname": "Lee", "phone": 945678901, "joined_date": datetime.date(2024, 3, 20)},
    {"firstname": "David", "lastname": "Lin", "phone": 956789012, "joined_date": datetime.date(2024, 4, 10)},
    {"firstname": "Emma", "lastname": "Wu", "phone": 967890123, "joined_date": datetime.date(2024, 5, 18)},
    {"firstname": "Frank", "lastname": "Huang", "phone": 978901234, "joined_date": datetime.date(2024, 6, 22)},
    {"firstname": "Grace", "lastname": "Chang", "phone": 989012345, "joined_date": datetime.date(2024, 7, 30)},
    {"firstname": "Henry", "lastname": "Tsai", "phone": 990123456, "joined_date": datetime.date(2024, 8, 14)},
    {"firstname": "Ivy", "lastname": "Kao", "phone": 901234567, "joined_date": datetime.date(2024, 9, 25)},
]

# 批次建立與儲存會員
print("--- 正在匯入會員資料 ---")
for data in members_data:
    # 檢查是否已存在相同姓名的會員，避免重複匯入
    if not Member.objects.filter(firstname=data["firstname"], lastname=data["lastname"]).exists():
        member = Member(
            firstname=data["firstname"],
            lastname=data["lastname"],
            phone=data["phone"],
            joined_date=data["joined_date"]
        )
        member.save()
        print(f"成功新增會員: {member.firstname} {member.lastname}")
    else:
        print(f"會員已存在，跳過新增: {data['firstname']} {data['lastname']}")

print("\n--- 目前所有會員資料 ---")
for m in Member.objects.all().values():
    print(m)