from django.db import models

class login_table(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=30)

class staff_profile(models.Model):
    staff_name = models.CharField(max_length=30)
    staff_email = models.CharField(max_length=30)
    staff_phone = models.BigIntegerField()
    staff_dob = models.DateField()
    staff_code = models.CharField(max_length=10)
    STAFF_LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)

class courses(models.Model):
    course_name = models.CharField(max_length=60)
    course_duration = models.IntegerField()
    course_type = models.CharField(max_length=20) # Aided / Self_Financing

class subject(models.Model):
    subject_name = models.CharField(max_length=30)
    COURSE_ID = models.ForeignKey(courses, on_delete=models.CASCADE)

class student_profile(models.Model):
    student_name = models.CharField(max_length=30)
    student_email = models.CharField(max_length=30)
    student_phone = models.BigIntegerField()
    student_current_sem = models.CharField(max_length=30)
    student_dob = models.DateField()
    student_admission_number = models.CharField(max_length=10)
    STUDENT_COURSE = models.ForeignKey(courses, on_delete=models.CASCADE)
    STUDENT_LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)

class notification(models.Model):
    notification = models.CharField(max_length=400)
    notification_date = models.DateField()
    type = models.CharField(max_length=20)  # For student and Staff

class notes(models.Model):
    subject_note = models.FileField()
    STAFF_ID = models.ForeignKey(staff_profile, on_delete=models.CASCADE)
    SUBJECT_ID = models.ForeignKey(subject, on_delete=models.CASCADE)

class complaints(models.Model):
    complaint = models.CharField(max_length=500)
    reply = models.CharField(max_length=500)
    date = models.DateField()
    replied_status = models.BooleanField(default=False)
    STUDENT_ID = models.ForeignKey(student_profile, on_delete=models.CASCADE)


