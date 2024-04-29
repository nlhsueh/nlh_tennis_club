
from members.models import Member

albert = Member(firstname='Albert', lastname='Ma')
albert.save()

print(Member.objects.all().values())