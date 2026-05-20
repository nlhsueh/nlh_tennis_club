import random
from datetime import date, timedelta
from members.models import Member

first_names = ['Alice', 'Bob', 'Charlie', 'David',
               'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan', 'Judy']
last_names = ['Smith', 'Johnson', 'Williams', 'Jones',
              'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']

for _ in range(10):
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    phone_num = random.randint(1000000000, 9999999999)

    # Generate a random date within the last 5 years
    random_days = random.randint(0, 365 * 5)
    join_date = date.today() - timedelta(days=random_days)

    Member.objects.create(
        firstname=fname,
        lastname=lname,
        phone=phone_num,
        joined_date=join_date
    )

print(Member.objects.all().values())

# exec(open('members/addMember.py').read())
