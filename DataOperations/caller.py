import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Run and print your queries
from main_app.models import Student

'''
FC5204	John	Doe	15/05/1995	john.doe@university.com
FE0054	Jane	Smith	null	jane.smith@university.com
FH2014	Alice	Johnson	10/02/1998	alice.johnson@university.com
FH2015	Bob	Wilson	25/11/1996	bob.wilson@university.com
'''

def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-5-15',
        email='john.doe@university.com'
    )


    student_2 = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student_2.save()

    student_3 = Student()
    student_3.student_id = 'FH2014'
    student_3.first_name = 'Alice'
    student_3.last_name = 'Johnson'
    student_3.birth_date = '1998-02-10'
    student_3.email = 'alice.johnson@university.com'
    student_3.save()

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )

# add_students()
    # student_list = [
    #     Student(
    #         student_id='FC5204',
    #         first_name='John',
    #         last_name='Doe',
    #         birth_date='1995-5-15',
    #         email='john.doe@university.com'
    #     ),
    #     Student(
    #         student_id='FE0054',
    #         first_name='Jane',
    #         last_name='Smith',
    #         email='jane.smith@university.com'
    #     ),
    #     Student(
    #         student_id='FH2014',
    #         first_name='Alice',
    #         last_name='Johnson',
    #         birth_date='1998-02-10',
    #         email='alice.johnson@university.com'
    #     ),
    #     Student(
    #         student_id='FH2015',
    #         first_name='Bob',
    #         last_name='Wilson',
    #         birth_date='1996-11-25',
    #         email='bob.wilson@university.com'
    #     )
    # ]
    # Student.objects.bulk_create(student_list)
# #
def get_students_info():
    students = Student.objects.all()
    return '\n'.join(f"Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}" for s in students)

# print(get_students_info())
# get_students_info()


def update_students_emails():
    students = Student.objects.all()
    for s in students:
        s.email = s.email.replace(s.email.split('@')[1], 'uni-students.com')
        # s.save()
    Student.objects.bulk_update(students, ['email'])


def truncate_students():

    # student = Student.objects.filter(id=1)
    # student.delete()

    students = Student.objects.all()
    students.delete()













