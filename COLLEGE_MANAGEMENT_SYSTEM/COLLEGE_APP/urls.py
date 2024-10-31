from django.urls import path
from COLLEGE_APP import views

urlpatterns = [
    path('', views.school),
    path('login', views.login),
    path('logout',views.logout),
    path('home', views.home),
# Admin urls--------------------------------------------------------------------------------------------
    path('home', views.home),
    path('admin_manage_staffs', views.admin_manage_staffs),
    path('add_staff', views.add_staff),
    path('admin_add_staff', views.admin_add_staff),
    path('edit_staff/<id>', views.edit_staff),
    path('delete_staff/<id>', views.delete_staff),
    path('admin_edit_staff', views.admin_edit_staff_post),
    path('staff_search_filter', views.staff_search_filter),

    path('admin_manage_courses', views.admin_manage_courses),
    path('course_search',views.course_search),
    path('add_course',views.add_course),
    path('admin_add_course',views.admin_add_course),
    path('edit_course/<id>', views.edit_course),
    path('delete_course/<id>', views.delete_course),
    path('admin_edit_course', views.admin_edit_course_post),

    path('view_complaints', views.view_complaints),
    path('search_complaint', views.search_complaint),
    path('reply_complaint/<id>', views.reply_complaint),
    path('admin_reply_complaint_post', views.admin_reply_complaint_post),

    path('add_notification', views.add_notification),
    path('admin_add_notification', views.admin_add_notification),
# Staff urls-------------------------------------------------------------------------------------------
    path('staff_home', views.staff_home),
    path('staff_view_notification', views.staff_view_notification),
    path('notification_search',views.notification_search),

    path('staff_view_students', views.staff_view_students),
    path('staff_search_student', views.staff_search_student),

    path('staff_view_profile', views.staff_view_profile),

    path('staff_manage_subjects', views.staff_manage_subjects),
    path('add_subject',views.add_subject),
    path('staff_add_subject', views.staff_add_subject),
    path('edit_subject/<id>', views.edit_subject),
    path('staff_edit_subject', views.staff_edit_subject),
    path('delete_subject/<id>', views.delete_subject),
    path('subject_search', views.subject_search),

    path('sub_notes',views.sub_notes),
    path('staff_view_notes',views.staff_view_notes),
    path('staff_add_notes', views.staff_add_notes),

# Students urls-------------------------------------------------------------------------------------------
    path('create_account', views.create_account),
    path('student_create_account', views.student_create_account,name='student_create_account'),

    path('student_view_notification', views.student_view_notification),
    path('student_notification_search', views.student_notification_search),

    path('student_view_profile', views.student_view_profile),

    path('view_notes', views.view_notes),
    path('search_notes',views.search_notes),

    path('complaints_page', views.complaints_page),
    path('student_complaint_search', views.student_complaint_search),
    path('add_new_complaint', views.add_new_complaint),
    path('send_complaint', views.send_complaint),
    
]