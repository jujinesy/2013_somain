from member.models import *

TYPE_TYPE_CHOICES = (
    ('1', '멘티'),
    ('2', '멘토'),
    ('3', '관리자'),
    ('4', '시스템 관리자'),
)
def create_initialdata():
    create_initialdata_type

def create_initialdata_type():
    for i in len(TYPE_TYPE_CHOICES):
        number, title = TYPE_TYPE_CHOICES[i]
        new_type_instance = Type(priority=i, title=title)
        new_type_instance.save()
