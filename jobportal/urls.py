from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

# This Import is for resetting the password.
from django.contrib.auth import views as auth_view


urlpatterns = [
   path('', views.home, name='home'),
   path('about', views.about, name='about'),
   path('contact', views.contact, name='contact'),
   path('candi-reg', views.candidateRegister, name='candidateRegister'),
   path('candi-login', views.candidateLogin, name='candidateLogin'),
   path('recu-reg', views.recruiterRegister, name='recruiterRegister'),
   path('recu-login', views.recruiterLogin, name='recruiterLogin'),
   path('admin-login', views.adminLogin, name='adminLogin'),
   path('admin-panel', views.admin_home, name='adminPanel'),
   path('logout', views.logout, name="logout"),
   path('change-password', views.change_password, name="changePassword"),
   path('edit-candidate-profile', views.edit_candidate_profile, name="editCandidateProfile"),
   path('edit-recruiter-profile', views.edit_recruiter_profile, name="editRecruiterProfile"),
   path('post-job', views.post_job, name="postJob"),
   path('job/<int:id>', views.jobDetails, name="jobDetails"),
   path('job-list', views.listJobs, name="listJobs"),

   # This Urls is for resetting the password (By Using Django Default Views)
   path('reset_password', auth_view.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
   path('reset_password_send', auth_view.PasswordResetDoneView.as_view(template_name="password_reset_send.html"), name="password_reset_done"),
   path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
   path('reset_password_complete', auth_view.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
