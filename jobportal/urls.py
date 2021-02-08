from django.conf import settings
from django.conf.urls.static import static
# This Import is for resetting the password.
from django.contrib.auth import views as auth_view
from django.urls import path

from . import views

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
                  path('search-result', views.search, name="search"),
                  path('change-password', views.change_password, name="changePassword"),
                  path('edit-candidate-profile', views.edit_candidate_profile, name="editCandidateProfile"),
                  path('edit-recruiter-profile', views.edit_recruiter_profile, name="editRecruiterProfile"),
                  path('post-job', views.post_job, name="postJob"),
                  path('edit-job/<int:job_id>', views.editJob, name="editJob"),
                  path('job/<int:job_id>', views.jobDetails, name="jobDetails"),
                  path('job-list', views.listJobs, name="listJobs"),
                  path('apply/<int:job_id>', views.applyJob, name="applyJob"),
                  path('applied-jobs', views.appliedJobsByCandidate, name="appliedJobsByCandidate"),
                  path('withdraw-job/<int:job_id>', views.withdrawJob, name="withdrawJob"),
                  path('candidate-applied', views.candidateApplied, name="candidateApplied"),
                  path('change-job-status/<int:candidate_id>', views.changeCandidateJobStatus,
                       name="changeCandidateJobStatus"),
                  path('myposted-jobs', views.mypostedJobs, name="mypostedJobs"),
                  path('delete-job/<int:job_id>', views.deleteJob, name="deleteJob"),
                  path('bookmark-job/<int:bookmark_job_id>', views.bookmarkJob, name="bookmarkJob"),
                  path('saved-job', views.savedJobs, name="savedJobs"),
                  path('delete-bookmark/<int:bookmark_job_id>', views.deleteBookmark, name="deleteBookmark"),
                  path('all-candidates', views.viewAllCandidates, name="viewAllCandidate"),
                  path('all-recruiters', views.viewAllRecruiters, name="viewAllRecruiter"),
                  path('delete-candidate/<int:candidate_id>', views.deleteCandidate, name="deleteCandidate"),
                  path('delete-recruiter/<int:recruiter_id>', views.deleteRecruiter, name="deleteRecruiter"),
                  path('new-request', views.newRecruiterRequest, name="newRecruiterRequest"),
                  path('assign-status/<int:recruiter_id>', views.assignStatus, name="assignStatus"),
                  path('temporary-disable/<int:user_id>', views.temporaryDisableAccount, name="temporaryDisable"),
                  path('send-warning/<int:job_id>', views.sendWarningToRecruiter, name="sendWarningToRecruiter"),
                  path('delete-job-by-admin/<int:job_id>', views.deleteJobByAdmin, name="deleteJobByAdmin"),
                  path('add-recruiter', views.addNewRecruiter, name="addNewRecruiter"),
                  path('resubmit-profile', views.resubmitProfileForReview, name="resubmitProfile"),

                  # URL is to update the code on deployment server
                  path("update_server/", views.update, name="update"),

                  # This Urls is for resetting the password (By Using Django Default Views)
                  path('reset_password',
                       auth_view.PasswordResetView.as_view(template_name="common/password_reset.html"),
                       name="reset_password"),
                  path('reset_password_send',
                       auth_view.PasswordResetDoneView.as_view(template_name="common/password_reset_send.html"),
                       name="password_reset_done"),
                  path('reset/<uidb64>/<token>/',
                       auth_view.PasswordResetConfirmView.as_view(template_name="common/password_reset_form.html"),
                       name="password_reset_confirm"),
                  path('reset_password_complete',
                       auth_view.PasswordResetCompleteView.as_view(template_name="common/password_reset_done.html"),
                       name="password_reset_complete"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
