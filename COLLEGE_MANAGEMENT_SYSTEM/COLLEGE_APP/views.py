from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, HttpResponse, get_object_or_404,redirect
from .models import *
from datetime import date, datetime
from django.db.models import Q

#Main Functions
# Function to render the login page
def school(request):
    auth.logout(request)
    return render(request, "loginindex.html")


def wmo(request):
    return render(request, "loginindex.html")

def staff_home(request):
    return render(request, 'staff/staff_index.html')

# Function to go to the home page
def home(request):
    return render(request, 'admin/admin_index.html')

def logout(request):
    auth.logout(request)
    return render(request, 'loginindex.html')


# Function to Login for admin,staff,student
def login(request):
    user_name = request.POST["user_name"]
    password = request.POST["password"]
    login_object = login_table.objects.filter(user_name=user_name, password=password)
    if login_object.exists():
        # login_objects = login_object.first()
        login_object_1 = login_table.objects.filter(user_name=user_name, password=password).first()
        request.session['lid'] = login_object_1.id
        if login_object_1.type == "admin":
            ob = auth.authenticate(username='admin', password='admin')
            if ob is not None:
                auth.login(request, ob)
                request.session['lid'] = login_object[0].id
                return render(request, 'admin/admin_index.html')
            else:
                return HttpResponse('''<script>alert("Admin authentication failed"); window.location = "/";</script>''')
        elif login_object_1.type == "staff":
            ob = staff_profile.objects.filter(STAFF_LOGIN=login_object_1.id)
            ob1 = auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)
                request.session['lid'] = login_object[0].id
                if len(ob) > 0:
                    return render(request, 'staff/staff_index.html')
                else:
                    return HttpResponse('''<script>alert("INVALID"); window.location = "/";</script>''')
            else:
                return HttpResponse('''<script>alert("INVALID"); window.location = "/";</script>''')
        elif login_object_1.type == "student":
            ob = student_profile.objects.filter(STUDENT_LOGIN=login_object_1.id)
            ob2 = auth.authenticate(username='admin', password='admin')
            if ob2 is not None:
                auth.login(request, ob2)
                request.session['lid'] = login_object[0].id
                return render(request, 'student/index2.html')
            else:
                return HttpResponse('''<script>alert("INVALID USERS"); window.location = "/";</script>''')
        else:
            return HttpResponse('''<script>alert("INVALID"); window.location = "/";</script>''')
    else:
        return HttpResponse('''<script>alert("INVALID"); window.location = "/";</script>''')
#----------------------------------------------------------------------------------------------------------------------------------------------#
# Admin functions
# Function to see the staffs in the home page

@login_required(login_url='/')
def admin_manage_staffs(request):
    staff_details = staff_profile.objects.all()
    return render(request, 'admin/manage_staff.html', {'staff_details': staff_details})

# Function to render the page add staff
@login_required(login_url='/')
def add_staff(request):
    return render(request, 'admin/add_staffs.html')

# Function to create a new staff
@login_required(login_url='/')
def admin_add_staff(request):
    staff_name = request.POST["name"]
    staff_email = request.POST["email"]
    staff_phone = request.POST["phone"]
    staff_dob = request.POST["dob"]
    staff_code = request.POST["code"]
    user_name = request.POST["user_name"]
    password = request.POST["password"]

    staff_login_details = login_table()

    staff_login_details.user_name = user_name
    staff_login_details.password = password
    staff_login_details.type = "staff"
    staff_login_details.save()

    staff_details_objects = staff_profile()

    staff_details_objects.STAFF_LOGIN_id = staff_login_details.id

    staff_details_objects.staff_name = staff_name
    staff_details_objects.staff_email = staff_email
    staff_details_objects.staff_phone = staff_phone
    staff_details_objects.staff_dob = staff_dob
    staff_details_objects.staff_code = staff_code

    staff_details_objects.save()
    return HttpResponse('''<script>alert("Items Saved");window.location="/admin_manage_staffs"</script>''')

#Function to add a search filter for searching the staffs
@login_required(login_url='/')
def staff_search_filter(request):
    search = request.POST["search"]
    staff_details = staff_profile.objects.filter(staff_name__startswith=search)
    return render(request, 'admin/manage_staff.html',{'staff_details':staff_details})

# Function to edit the staff details
@login_required(login_url='/')
def edit_staff(request,id):
    details = staff_profile.objects.get(id=id)
    return render(request,'admin/edit_staff.html',{'details':details})

# Function to post the edited staff details
@login_required(login_url='/')
def admin_edit_staff_post(request):
    staff_name = request.POST["name"]
    staff_email = request.POST["email"]
    staff_phone = request.POST["phone"]
    staff_dob = request.POST["dob"]
    staff_code = request.POST["code"]
    id = request.POST["id"]

    edit_details = staff_profile.objects.get(id=id)

    edit_details.staff_name = staff_name
    edit_details.staff_email = staff_email
    edit_details.staff_phone = staff_phone
    edit_details.staff_dob = staff_dob
    edit_details.staff_code = staff_code

    edit_details.save()
    return HttpResponse('''<script>alert("Edited Successfully");window.location="/admin_manage_staffs"</script>''')

#Function to manage courses
@login_required(login_url='/')
def admin_manage_courses(request):
    course_details = courses.objects.all()
    return render(request, 'admin/manage_courses.html', {'course_details':course_details})

#Function to search for the course
@login_required(login_url='/')
def course_search(request):
    search = request.POST["search"]
    course_details = courses.objects.filter(
        Q(course_name__startswith=search) | Q(course_type__startswith=search))
    return render(request, 'admin/manage_courses.html', {'course_details':course_details})

#Function to render to the add course page
@login_required(login_url='/')
def add_course(request):
    return render(request, 'admin/add_course.html')

#Function to add course
@login_required(login_url='/')
def admin_add_course(request):
    course_name = request.POST["course_name"]
    course_duration = request.POST["course_duration"]
    course_type = request.POST["course_type"]

    course_details = courses()

    course_details.course_name = course_name
    course_details.course_duration = course_duration
    course_details.course_type = course_type

    course_details.save()
    return HttpResponse('''<script>alert("Course Added Successfully");window.location="/admin_manage_courses"</script>''')

# Function to edit the course details
@login_required(login_url='/')
def edit_course(request,id):
    details = courses.objects.get(id=id)
    return render(request,'admin/edit_course.html',{'details':details})

# Function to post the edited course details
@login_required(login_url='/')
def admin_edit_course_post(request):
    course_name = request.POST["course_name"]
    id = request.POST["id"] # Get this id from the table, for the get method, hide this id in the html and save the id
    course_duration = request.POST["course_duration"]
    course_type = request.POST["course_type"]

    edit_details = courses.objects.get(id=id)

    edit_details.course_name = course_name
    edit_details.course_duration = course_duration
    edit_details.course_type = course_type

    edit_details.save()
    return HttpResponse('''<script>alert("Edited Successfully");window.location="/admin_manage_courses"</script>''')

#Function to view the complaints
@login_required(login_url='/')
def view_complaints(request):
    student_complaints = complaints.objects.all()
    return render(request, 'admin/view_complaints.html', {'student_complaints': student_complaints})

#Function to search for a complaint
@login_required(login_url='/')
def search_complaint(request):
    from_date = request.POST["from_date"]
    to = request.POST["to"]
    student_complaints = complaints.objects.filter(date__range=(from_date, to))
    return render(request, 'admin/view_complaints.html', {'student_complaints': student_complaints})

#Function to reply for a complaint
@login_required(login_url='/')
def reply_complaint(request,id):
    details = complaints.objects.get(id=id)
    return render(request, 'admin/reply_complaint.html', {'details': details})

#Function to post the reply for the complaint
@login_required(login_url='/')
def admin_reply_complaint_post(request):
    student_complaint = request.POST["student_complaint"]
    complaint_reply = request.POST["complaint_reply"]
    id = request.POST["id"]
    complaint_date = date.today()

    complaint_details = complaints.objects.get(id=id)

    complaint_details.complaint = student_complaint
    complaint_details.reply = complaint_reply
    complaint_details.date = complaint_date
    complaint_details.replied_status = True

    complaint_details.save()
    return HttpResponse('''<script>alert("Replied Successfully");window.location="/view_complaints"</script>''')

#Function to add_notifications
@login_required(login_url='/')
def add_notification(request):
    return render(request, 'admin/Add_Notification.html')

@login_required(login_url='/')
def admin_add_notification(request):
    notification_note = request.POST["notification_note"]
    notification_date = date.today()
    notification_type = request.POST["notification_type"]

    notification_details = notification()

    notification_details.notification = notification_note
    notification_details.notification_date = notification_date
    notification_details.type = notification_type

    notification_details.save()
    return HttpResponse('''<script>alert("Notification Added Successfully");window.location="/home"</script>''')

#Function to delete the staff details
@login_required(login_url='/')
def delete_staff(request,id):
    staff_object_delete = staff_profile.objects.get(id=id)
    staff_object_delete.delete()
    return HttpResponse('''<script>alert("Deleted successfully");window.location="/admin_manage_staffs"</script>''')

#Function to delete the course
@login_required(login_url='/')
def delete_course(request,id):
    course_object_delete = courses.objects.get(id=id)
    course_object_delete.delete()
    return HttpResponse('''<script>alert("Deleted successfully");window.location="/admin_manage_courses"</script>''')

#------------------------------------------------------------------------------------------------------------------------------#
# Staff Functions
#Function to view the notifications
@login_required(login_url='/')
def staff_view_notification(request):
    notification_details = notification.objects.filter(type='STAFF')
    return render(request, 'staff/view_notification.html',{'notification_details':notification_details})

#Function to search for a notification
@login_required(login_url='/')
def notification_search(request):
    from_date = request.POST["from_date"]
    to = request.POST["to"]
    notification_details = notification.objects.filter(notification_date__range=(from_date, to))
    return render(request, 'staff/view_notification.html',{'notification_details':notification_details})

#Function to view the students
@login_required(login_url='/')
def staff_view_students(request):
    student_details = student_profile.objects.all()
    return render(request, 'staff/view_students.html',{'student_details':student_details})

#Function to search for student details
@login_required(login_url='/')
def staff_search_student(request):
    search = request.POST["search"]
    student_details = student_profile.objects.filter(Q(student_name__startswith=search)| Q(student_current_sem__startswith=search))
    return render(request, 'staff/view_students.html',{'student_details':student_details})

#Function to view the staff profile
@login_required(login_url='/')
def staff_view_profile(request):
    staff_id = request.session.get('lid')
    if staff_id:
        staff_profile_details = get_object_or_404(staff_profile, STAFF_LOGIN_id= staff_id)
        return render(request, 'staff/view_profile.html', {'staff_profile_details': staff_profile_details})
    else:
        return HttpResponse("No Data Found")

#Function to manage the subjects
@login_required(login_url='/')
def staff_manage_subjects(request):
    courses_list = courses.objects.all()
    return render(request, 'staff/manage_subjects.html', {'courses_list': courses_list})

#Function to search for a subject
@login_required(login_url='/')
def subject_search(request):
    course_id = request.POST.get('course_id')
    if course_id:
        subjects_details = subject.objects.filter(COURSE_ID=course_id)
    else:
        subjects_details = subject.objects.all()  # or handle no selection case as needed
    courses_list = courses.objects.all()
    return render(request, 'staff/manage_subjects.html', {'subjects_details': subjects_details, 'courses_list': courses_list})

#Function to render the page to edit a subject
@login_required(login_url='/')
def edit_subject(request,id):
    subject_details = subject.objects.get(id=id)
    return render(request, 'staff/staff_edit_subject.html', {'subject_details' : subject_details})

#Function to post the edited data
@login_required(login_url='/')
def staff_edit_subject(request):
    subject_name = request.POST['subject_name']
    id = request.POST['id']

    edit_subject = subject.objects.get(id=id)
    edit_subject.subject_name = subject_name

    edit_subject.save()
    return HttpResponse('''<script>alert("Edited Successfully");window.location="/staff_manage_subjects"</script>''')

#Function to delete the subject
@login_required(login_url='/')
def delete_subject(request,id):
    subject_details_delete = subject.objects.get(id=id)
    subject_details_delete.delete()
    return HttpResponse('''<script>alert("Deleted successfully");window.location="/staff_manage_subjects"</script>''')

#Function to render to the page add a subject
@login_required(login_url='/')
def add_subject(request):
    courses_list = courses.objects.all()
    return render(request, 'staff/add_subject.html', {'courses_list':courses_list})

#Function to add subject
@login_required(login_url='/')
def staff_add_subject(request):
    course_id = request.POST['course_id']
    subject_name = request.POST['subject_name']

    course = courses.objects.get(id=course_id)

    subject_object = subject(subject_name=subject_name, COURSE_ID=course)

    subject_object.save()
    return HttpResponse('''<script>alert("Added successfully");window.location="/staff_manage_subjects"</script>''')

@login_required(login_url='/')
def staff_view_notes(request):
    notes_details = notes.objects.all()
    return render(request, 'staff/view_notes.html', {'notes_details':notes_details})

# Function for file uploading
@login_required(login_url='/')
def sub_notes(request):
    subject_list = subject.objects.all()
    return render(request, 'staff/staff_add_notes.html', {'subject_list':subject_list})

#Function to add notes
@login_required(login_url='/')
def staff_add_notes(request):
    subject_id = request.POST['subject_id']
    note_file = request.FILES['note_media_file']


    fs=FileSystemStorage()

    date=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{date}_{note_file.name}"

    fs.save(filename,note_file)
    path=fs.url(filename)

    # fsave=fs.save(note_file.name,note_file)

    subject_instance = subject.objects.get(id=subject_id)
    staff_login_id = request.session['lid']
    staff_profile_instance = staff_profile.objects.get(STAFF_LOGIN__id=staff_login_id)

    notes_object = notes(
        subject_note=path,
        SUBJECT_ID=subject_instance,
        STAFF_ID=staff_profile_instance
    )
    notes_object.save()
    return HttpResponse('''<script>alert("Note added successfully");window.location="/sub_notes"</script>''')

# ------------------------------------------------------------------------------------------------------------------------
# Students Functions

#Function to render for account creation
# @login_required(login_url='/')
def create_account(request):
    course_list = courses.objects.all()
    return render(request, 'student/create_account.html', {'course_list': course_list})

#Function to create account
# @login_required(login_url='/')
def student_create_account(request):
    if request.method == 'POST':
        student_name = request.POST['name']
        student_email = request.POST['email']
        student_phone = request.POST['phone']
        student_current_sem = request.POST['semester']
        student_dob = request.POST['dob']
        student_admission_number = request.POST['code']
        student_user_name = request.POST['user_name']
        student_password = request.POST['password']
        course_id = request.POST['course_id']

        if login_table.objects.filter(user_name=student_user_name).exists():
            return HttpResponse('''<script>alert("Username already exists");window.location=" "</script>''')

        login_table_objects = login_table(
            user_name=student_user_name,
            password=student_password,
            type="student"
        )
        login_table_objects.save()

        course_objects = courses.objects.get(id=course_id)

        student_details_objects = student_profile(
            student_name=student_name,
            student_email=student_email,
            student_phone=student_phone,
            student_current_sem=student_current_sem,
            student_dob=student_dob,
            student_admission_number=student_admission_number,
            STUDENT_COURSE=course_objects,
            STUDENT_LOGIN=login_table_objects
        )

        student_details_objects.save()
        return HttpResponse('''<script>alert("Account Created");window.location=" "</script>''')
    else:
        return render(request, 'loginindex.html')

#Function to render for the notification page
@login_required(login_url='/')
def student_view_notification(request):
    notification_details = notification.objects.filter(type='STUDENT')
    return render(request, 'student/view_notification.html', {'notification_details':notification_details})

#Function to view the notifications
@login_required(login_url='/')
def student_notification_search(request):
    from_date = request.POST["from_date"]
    to = request.POST["to"]
    notification_details = notification.objects.filter(notification_date__range=(from_date, to),type='STUDENT')
    return render(request, 'student/view_notification.html',{'notification_details':notification_details})

#Function for view student's profile
@login_required(login_url='/')
def student_view_profile(request):
    student_id = request.session['lid']
    if student_id:
        # student_profile_details = get_object_or_404(student_profile, STUDENT_LOGIN=student_id)

        ob=student_profile.objects.get(STUDENT_LOGIN=student_id)
        return render(request, 'student/index.html', {'student_profile_details':ob})
    else:
        return HttpResponse("NO DATA FOUND")

# Function to view the notes in Dropdown list
@login_required(login_url='/')
def view_notes(request):
    student_id = request.session.get('lid')
    if student_id:
        student_profile_details = get_object_or_404(student_profile, STUDENT_LOGIN=student_id)
        student_course = student_profile_details.STUDENT_COURSE
        subject_list = subject.objects.filter(COURSE_ID=student_course)

        return render(request, 'student/view_notes.html',{
            'student_profile_details':student_profile_details,
            'subject_list':subject_list,
        })
    else:
        return HttpResponse("NO DATA FOUND")


#Function to search for notes. Who adds the note, For which subject
@login_required(login_url='/')
def search_notes(request):
    subject_id = request.POST['subject_id']
    if subject_id:
        subjects_details = subject.objects.filter(COURSE_ID=subject_id)
        notes_details = notes.objects.filter(SUBJECT_ID=subject_id).select_related('STAFF_ID')
        return render(request, 'student/view_notes.html',{
            'subjects_details':subjects_details,
            'notes_details':notes_details
        })
    else:
        return render(request, 'student/view_notes.html')

#Function for view the complaints
@login_required(login_url='/')
def complaints_page(request):
    student_id = request.session.get('lid')
    if student_id:
        student_profile_instance = get_object_or_404(student_profile, STUDENT_LOGIN=student_id)
        complaint_details = complaints.objects.filter(STUDENT_ID=student_profile_instance)
        return render(request, 'student/manage_complaints.html', {'complaint_details': complaint_details})
    else:
        return HttpResponse("No COMPLAINTS FOUND")

#Function for complaint search
@login_required(login_url='/')
def student_complaint_search(request):
    student_id = request.session.get('lid')
    if student_id:
        student_profile_instance = get_object_or_404(student_profile, STUDENT_LOGIN=student_id)
        from_date = request.POST["from_date"]
        to_date = request.POST["to"]
        complaint_details = complaints.objects.filter(
            STUDENT_ID=student_profile_instance,
            date__range=(from_date, to_date)
        )
        return render(request, 'student/manage_complaints.html', {'complaint_details': complaint_details})
    else:
        return HttpResponse("No COMPLAINTS FOUND")

#Function to render the page for add new complaint
@login_required(login_url='/')
def add_new_complaint(request):
    return render(request, 'student/add_complaint.html')

#Function to send a new complaint
@login_required(login_url='/')
def send_complaint(request):
    student_login_id = request.session['lid']
    complaint_data = request.POST['student_complaint']
    reply = "REPLY PENDING"
    complaint_date = date.today()

    student_profile_instance = student_profile.objects.get(STUDENT_LOGIN__id=student_login_id)

    complaint_object = complaints(
        complaint=complaint_data,
        reply=reply,
        date=complaint_date,
        replied_status=False,
        STUDENT_ID=student_profile_instance
    )
    complaint_object.save()
    return HttpResponse('''<script>alert("Complaint Send");window.location="complaints_page"</script>''')
