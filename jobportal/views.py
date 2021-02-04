import datetime
from datetime import date

# This import is for updating the code base on deployment server
import git
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from jobportal.permission import *
# Importing models class
from .models import Candidate, Recruiter, Job, ApplyJob, BookmarkJob

User = get_user_model()


# Create your views here.
def home(request):
    # Restricting To admin to see the users home page
    if request.user.is_authenticated and request.user.role == "admin":
        return redirect('adminPanel')

    # Fetching all jobs for candidate
    job_data = Job.objects.get_queryset().order_by('-timestamp')

    # Fetching jobs posted by recruiter
    if request.user.is_authenticated and request.user.role == "recruiter":
        recu = Recruiter.objects.get(uname=request.user)
        job_data = Job.objects.filter(recruiter=recu).order_by('-timestamp')

    # Fetching details for site stats
    total_candidate = Candidate.objects.count()
    total_recruiter = Recruiter.objects.count()
    total_job_posted = Job.objects.count()

    paginator = Paginator(job_data, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        jobs = paginator.page(page)
    except(EmptyPage, InvalidPage):
        jobs = paginator.page(paginator.num_pages)

    context = {
        'job_data': jobs,
        'total_candidate': total_candidate,
        'total_recruiter': total_recruiter,
        'total_job_posted': total_job_posted,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', False)
        email = request.POST.get('email', False)
        sub = request.POST.get('subject', False)
        msg = request.POST.get('message', False)

        if name == '' or email == '' or sub == '' or msg == '':
            messages.info(request, "All fields are required !!!")
            return redirect('contact')
        else:
            subject = f'Message By - {name}'
            message = f'<strong>Subject :</strong> {sub} <br> <strong>Email : </strong> {email} <br> ' \
                      f'<strong>Message : </strong> {msg}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER, ]
            send_mail(subject, message, email_from, recipient_list, html_message=message, fail_silently=True)

            messages.success(request, "Message successfully send. We will contact you shortly.")
            return redirect('contact')

    return render(request, 'contact.html')


# This Python method is used to validate the dob
def isValidDob(dob):
    today = date.today()
    d = datetime.datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))

    if age < 18:
        return True
    else:
        return False


# Candidate Registration Method
def candidateRegister(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', False)
        lname = request.POST.get('lname', False)
        uname = request.POST.get('uname', False)
        em = request.POST.get('email', False)
        conNumber = request.POST.get('contactNumber', False)
        dob = request.POST.get('dob', False)
        passwd = request.POST.get('pass', False)
        cPasswd = request.POST.get('confirmPass', False)
        gen = request.POST.get('gender', False)
        imgFile = request.FILES.get('imageFile', False)

        if fname == '' or lname == '' or uname == '' or em == '' or conNumber == '' or passwd == '' or cPasswd == '' or gen == '' or imgFile == '' or dob == '':
            messages.info(request, "All fields are required !!!")
            return redirect('candidateRegister')
        else:
            if passwd != cPasswd:
                messages.warning(request, "Password must be same !!!")
                return redirect('candidateRegister')
            elif User.objects.filter(username=uname).exists():
                messages.warning(request, "Username Already In Use !!!")
                return redirect('candidateRegister')
            elif User.objects.filter(email=em).exists():
                messages.warning(request, "Email Already In Use !!!")
                return redirect('candidateRegister')
            elif isValidDob(dob):
                messages.warning(request, "You are under age !!!")
                return redirect('candidateRegister')
            else:
                user = User.objects.create(first_name=fname, last_name=lname, email=em, username=uname,
                                           role="candidate")
                # Saving Password in the encrypted format.
                user.set_password(passwd)
                candi = Candidate.objects.create(uname=user, candidate_number=conNumber, candidate_image=imgFile,
                                                 dob=dob, gender=gen)
                user.save()
                candi.save()

                messages.success(request, "Registration successfully done !!!")
                return redirect('candidateLogin')

    return render(request, 'candidate/candidate_register.html')


# Candidate Login Method
def candidateLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', False)
        passwd = request.POST.get('passwd', False)

        if uname == '' or passwd == '':
            messages.info(request, "All Fields are required !!!")
            return redirect('candidateLogin')
        elif not User.objects.filter(username=uname).exists():
            messages.error(request, "User doesn't exists !!!")
            return redirect('candidateLogin')
        else:
            user = auth.authenticate(username=uname, password=passwd)
            if user:
                try:
                    if user.role == "candidate":
                        auth.login(request, user)
                        return redirect('home')
                    else:
                        messages.warning(request, "Not a candidate, please try with another credentials !!!")
                        return redirect('candidateLogin')
                except:
                    messages.error(request, "Something went wrong !!!")
                    return redirect('candidateLogin')
            else:
                messages.error(request, "Invalid credentials, please try again !!!")
                return redirect('candidateLogin')

    return render(request, 'candidate/candidate_login.html')


# Logout Method To destroy the current session
def logout(request):
    auth.logout(request)
    return redirect('home')


# Recruiter Registration Method
def recruiterRegister(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', False)
        lname = request.POST.get('lname', False)
        comName = request.POST.get('comName', False)
        em = request.POST.get('email', False)
        uname = request.POST.get('uname', False)
        conNumber = request.POST.get('contactNumber', False)
        passwd = request.POST.get('pass', False)
        cPasswd = request.POST.get('confirmPass', False)
        gen = request.POST.get('gender', False)
        dob = request.POST.get('dob', False)
        imgFile = request.FILES.get('imageFile', False)

        if fname == '' or lname == '' or comName == '' or em == '' or uname == '' or conNumber == '' or passwd == '' or cPasswd == '' or gen == '' or imgFile == '' or dob == '':
            messages.info(request, "All fields are required, please try again !!!")
            return redirect('recruiterRegister')
        else:
            if passwd != cPasswd:
                messages.warning(request, "Password must be same !!!")
                return redirect('recruiterRegister')
            elif User.objects.filter(email=em).exists():
                messages.warning(request, "Email Already In Use !!!")
                return redirect('recruiterRegister')
            elif User.objects.filter(username=uname).exists():
                messages.warning(request, "Username Already In Use !!!")
                return redirect('candidateRegister')
            elif isValidDob(dob):
                messages.warning(request, "You are under age !!!")
                return redirect('recruiterRegister')
            else:
                user = User.objects.create(first_name=fname, last_name=lname, email=em, username=uname,
                                           role="recruiter")
                # Saving Password in the encrypted format
                user.set_password(passwd)
                recu = Recruiter.objects.create(uname=user, company_name=comName, recruiter_number=conNumber,
                                                gender=gen, dob=dob, recruiter_image=imgFile, status="pending")
                user.save()
                recu.save()
                messages.success(request, "Registration Successfully Done !!!")
                return redirect('recruiterLogin')

    return render(request, 'recruiter/recruiter_register.html')


# Recruiter Login Method
def recruiterLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', False)
        passwd = request.POST.get('passwd', False)

        if uname == '' or passwd == '':
            messages.info(request, "All fields are required !!!")
            return redirect('recruiterLogin')
        elif not User.objects.filter(username=uname).exists():
            messages.error(request, "User doesn't exists !!!")
            return redirect('recruiterLogin')
        else:
            user = auth.authenticate(username=uname, password=passwd)
            if user:
                try:
                    if user.role == "recruiter":
                        auth.login(request, user)
                        return redirect('home')
                    else:
                        messages.warning(request, "Not a recruiter, please try with another credentials !!!")
                        return redirect('recruiterLogin')
                except:
                    messages.error(request, "Something went wrong !!!")
                    return redirect('recruiterLogin')
            else:
                messages.error(request, "Invalid credentials, please try again !!!")
                return redirect('recruiterLogin')

    return render(request, 'recruiter/recruiter_login.html')


# Admin Login Method
def adminLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', False)
        passwd = request.POST.get('passwd', False)

        if uname == '' or passwd == '':
            messages.info(request, 'All fields are required, please try again !!!')
            return redirect('adminLogin')
        else:
            user = auth.authenticate(username=uname, password=passwd)
            if user:
                try:
                    if user.role == "admin":
                        auth.login(request, user)
                        return redirect('adminPanel')
                    else:
                        messages.warning(request, "You are not an Admin, please try with another credentials !!!")
                        return redirect('adminLogin')
                except:
                    messages.error(request, "Something went wrong !!!")
                    return redirect('adminLogin')
            else:
                messages.error(request, "User does not exists !!!")
                return redirect('adminLogin')

    return render(request, 'admin/admin_login.html')


# This view handle the search feature
def search(request):
    job_list = Job.objects.order_by('-timestamp')

    # search by keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(job_title__icontains=job_title_or_company_name) \
                       | job_list.filter(recruiter__company_name__icontains=job_title_or_company_name)

    # search by location
    if 'location' in request.GET:
        location = request.GET['location']

        if location:
            job_list = job_list.filter(job_location__icontains=location)

    # filter by job type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']

        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    if not job_list:
        no_job = True
    else:
        no_job = False

    context = {
        'job_list': job_list,
        'no_job': no_job
    }

    return render(request, 'common/search_result.html', context)


# Admin Home page render
@login_required(login_url='/admin-login')
@user_is_admin
def admin_home(request):
    total_candi = Candidate.objects.count()
    total_recu = Recruiter.objects.count()
    total_job = Job.objects.count()

    context = {
        'total_candi': total_candi,
        'total_recu': total_recu,
        'total_job': total_job,
    }

    return render(request, 'admin/admin_home.html', context)


# Changing The Password
@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        oldpass = request.POST.get('oldpass', False)
        newpass1 = request.POST.get('newpass1', False)
        newpass2 = request.POST.get('newpass2', False)

        if oldpass == '' or newpass1 == '' or newpass2 == '':
            messages.info(request, "All fields are required, please fill all the details !!!")
            return redirect('changePassword')
        else:
            if newpass1 != newpass2:
                messages.warning(request, "New and Confirm password must be same, please try again !!!")
                return redirect('changePassword')
            elif oldpass == newpass1 == newpass2:
                messages.warning(request, "New password must not be as Old password, please try again !!!")
                return redirect('candidateLogin')
            else:
                try:
                    if request.user.check_password(oldpass):
                        u = User.objects.get(username=request.user)
                        u.set_password(newpass1)
                        u.save()
                        messages.success(request, "Successfully password has been changed !!!")
                        return redirect('changePassword')
                    else:
                        messages.error(request, "Old Password is incorrect !!!")
                        return redirect('changePassword')
                except:
                    messages.warning(request, "Something went wrong !!!")
                    return redirect('changePassword')

    return render(request, 'common/change_password.html')


# Editing Profile details
@login_required(login_url='/')
@user_is_candidate
def edit_candidate_profile(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', False)
        lname = request.POST.get('lname', False)
        em = request.POST.get('email', False)
        uname = request.POST.get('username', False)
        mobile = request.POST.get('mobile', False)
        gen = request.POST.get('gender', False)
        img = request.FILES.get('image', False)

        if fname == '' or lname == '' or em == '' or uname == '' or mobile == '':
            messages.info(request, "All fields must be filled !!!")
            return redirect('editCandidateProfile')
        else:
            try:
                if User.objects.filter(email=em).exists() and request.user.email != em:
                    messages.warning(request, "Email already in use, please choice another email !!!")
                    return redirect('editCandidateProfile')
                elif Candidate.objects.filter(candidate_number=mobile).exists() and Candidate.objects.get(
                        uname=request.user).candidate_number == mobile:
                    messages.warning(request, "Mobile number already in use, please try again !!!")
                    return redirect('editCandidateProfile')
                else:
                    try:
                        u = User.objects.get(username=request.user)
                        u.first_name = fname
                        u.last_name = lname
                        u.email = em
                        c = Candidate.objects.get(uname=request.user)
                        c.candidate_number = mobile

                        if img:
                            c.candidate_image = img
                        if gen:
                            c.gender = gen

                        u.save()
                        c.save()
                        messages.success(request, "You profile has been updated !!!")
                        return redirect('editCandidateProfile')
                    except:
                        messages.warning(request, "Something went wrong !!!")
                        return redirect('editCandidateProfile')
            except:
                messages.warning(request, "Something went wrong !!!")
                return redirect('editCandidateProfile')

    candi = Candidate.objects.get(uname=request.user)
    return render(request, 'common/edit_profile.html', {'candi': candi})


@login_required(login_url='/')
@user_is_recruiter
def edit_recruiter_profile(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', False)
        lname = request.POST.get('lname', False)
        em = request.POST.get('email', False)
        uname = request.POST.get('username', False)
        company_name = request.POST.get('companyName', False)
        mobile = request.POST.get('mobile', False)
        gen = request.POST.get('gender', False)
        img = request.FILES.get('image', False)

        if fname == '' or lname == '' or em == '' or uname == '' or mobile == '' or company_name == '':
            messages.info(request, "All fields must be filled !!!")
            return redirect('editRecruiterProfile')
        else:
            try:
                if User.objects.filter(email=em).exists() and request.user.email != em:
                    messages.warning(request, "Email already in use, please choice another email !!!")
                    return redirect('editRecruiterProfile')
                elif Recruiter.objects.filter(recruiter_number=mobile).exists() and Recruiter.objects.get(
                        uname=request.user).recruiter_number == mobile:
                    messages.warning(request, "Mobile number already in use, please try again !!!")
                    return redirect('editRecruiterProfile')
                else:
                    try:
                        u = User.objects.get(username=request.user)
                        u.first_name = fname
                        u.last_name = lname
                        u.email = em
                        r = Recruiter.objects.get(uname=request.user)
                        r.recruiter_number = mobile

                        if img:
                            r.recruiter_image = img
                        if gen:
                            r.gender = gen

                        u.save()
                        r.save()
                        messages.success(request, "You profile has been updated !!!")
                        return redirect('editRecruiterProfile')
                    except:
                        messages.warning(request, "Something went wrong !!!")
                        return redirect('editRecruiterProfile')
            except:
                messages.warning(request, "Something went wrong !!!")
                return redirect('editRecruiterProfile')

    recu = Recruiter.objects.get(uname=request.user)
    return render(request, 'common/edit_profile.html', {'recu': recu})


@login_required(login_url='/recu-login')
@user_is_recruiter
def post_job(request):
    if request.method == 'POST':
        companyName = request.POST.get('companyName', False)
        jobTitle = request.POST.get('jobTitle', False)
        jobLocation = request.POST.get('jobLocation', False)
        jobType = request.POST.get('jobType', False)
        cate = request.POST.get('role', False)
        sal = request.POST.get('salary', False)
        exp = request.POST.get('experience', False)
        startDate = request.POST.get('startDate', False)
        lastDate = request.POST.get('lastDate', False)
        requiredSkill = request.POST.get('requiredSkills', False)
        web = request.POST.get('website', False)
        des = request.POST.get('description', False)
        companyLogo = request.FILES.get('image', False)

        if companyName == '' or jobTitle == '' or jobLocation == '' or jobType == '' or cate == '' or sal == '' or exp == '' or startDate == '' or lastDate == '' or requiredSkill == '' or web == '' or des == '' or companyLogo == '':
            messages.info(request, "All fields are required, please try again !!!")
            return redirect('postJob')
        else:
            start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
            last = datetime.datetime.strptime(lastDate, "%Y-%m-%d")
            if start == last:
                messages.error(request, "Start date and last date can't be same, try again !!!")
                return redirect('postJob')
            elif start > last:
                messages.error(request, "End date should be greater than start date !!!")
                return redirect('postJob')
            else:
                try:
                    recu = Recruiter.objects.get(uname=request.user)
                    post = Job.objects.create(recruiter=recu, job_title=jobTitle, job_location=jobLocation,
                                              job_type=jobType,
                                              category=cate, salary=sal, experience=exp, start_date=startDate,
                                              last_date=lastDate,
                                              skills=requiredSkill, website_link=web, description=des,
                                              company_logo_image=companyLogo)

                    post.save()
                    messages.success(request, "Job Successfully posted !!!")
                    return redirect('postJob')
                except:
                    messages.error(request, "Something went wrong, please try again !!!")
                    return redirect('postJob')

    recu = Recruiter.objects.get(uname=request.user)
    d = datetime.date.today()
    return render(request, 'recruiter/post_job.html', {'recu': recu, 'date': d.strftime("%Y-%m-%d")})


@login_required(login_url='/recu-login')
@user_is_recruiter
def editJob(request, id):
    try:
        edit_job = Job.objects.get(recruiter__uname=request.user, id=id)
    except:
        messages.error(request, "Something went wrong !!!")
        return redirect('postJob')

    if request.method == 'POST':
        companyName = request.POST.get('companyName', False)
        jobTitle = request.POST.get('jobTitle', False)
        jobLocation = request.POST.get('jobLocation', False)
        jobType = request.POST.get('jobType', False)
        cate = request.POST.get('role', False)
        sal = request.POST.get('salary', False)
        exp = request.POST.get('experience', False)
        startDate = request.POST.get('startDate', False)
        lastDate = request.POST.get('lastDate', False)
        requiredSkill = request.POST.get('requiredSkills', False)
        web = request.POST.get('website', False)
        des = request.POST.get('description', False)
        companyLogo = request.FILES.get('image', False)

        if companyName == '' or jobTitle == '' or jobLocation == '' or jobType == '' or cate == '' or sal == '' or exp == '' or startDate == '' or requiredSkill == '' or web == '' or des == '':
            messages.info(request, "All fields are required, please try again !!!")
            return redirect('postJob')
        else:
            if lastDate != '':
                edit_job.last_date = lastDate

            if companyLogo:
                edit_job.company_logo_image = companyLogo

            edit_job.job_title = jobTitle
            edit_job.job_location = jobLocation
            edit_job.job_type = jobType
            edit_job.category = cate
            edit_job.salary = sal
            edit_job.experience = exp
            edit_job.skills = requiredSkill
            edit_job.website_link = web
            edit_job.description = des

            edit_job.save()

            messages.success(request, "Job details has been updated !!!")
            return redirect('mypostedJobs')

    context = {
        'edit_job': edit_job
    }

    return render(request, 'recruiter/edit_job.html', context)


def jobDetails(request, id):
    try:
        job_details = Job.objects.get(pk=id)
    except:
        messages.error(request, "This job might be deleted by recruiter !!!")
        return redirect('listJobs')

    context = {
        'job_details': job_details,
    }

    return render(request, 'common/job_details.html', context)


def listJobs(request):
    all_jobs = Job.objects.all().order_by('-timestamp')

    paginator = Paginator(all_jobs, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        jobs = paginator.page(page)
    except(EmptyPage, InvalidPage):
        jobs = paginator.page(paginator.num_pages)

    context = {
        'all_jobs': jobs
    }

    return render(request, 'common/list_jobs.html', context)


@login_required(login_url='/candi-login')
@user_is_candidate
def applyJob(request, id):
    user = User.objects.get(id=request.user.id)
    candi = Candidate.objects.get(uname=user)
    job = Job.objects.get(id=id)
    last_date = job.last_date

    if request.method == 'POST':
        candi_resume = request.FILES.get('resume', False)
        if not candi_resume:
            messages.error(request, "Please upload your resume !!!")
            return redirect('applyJob', id)
        else:
            apply = ApplyJob.objects.create(job_applied=job, candidate=candi, resume=candi_resume)
            apply.save()

            subject = 'Easy Recruit Team'
            message = f'<h3>Hi {candi.uname.first_name}, your application has been submitted. <br></h3>' \
                      f'<strong>Company Name : </strong>{job.recruiter.company_name} <br>' \
                      f'<strong>Job ID : </strong>{job.id} <br>' \
                      f'<strong>Job Title : </strong>{job.job_title} <br>' \
                      f'<strong>Job Location : </strong>{job.job_location} <br><br>' \
                      f'You will be communicated by recruiter, if your resume will be shortlisted.'

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [candi.uname.email, ]
            send_mail(subject, message, email_from, recipient_list, html_message=message, fail_silently=True)

            messages.success(request, "Successfully applied !!!")
            return redirect('jobDetails', id)

    context = {
        'candi': candi,
        'job': job
    }

    return render(request, 'candidate/apply_job.html', context)


@login_required(login_url='/candi-login')
@user_is_candidate
def appliedJobsByCandidate(request):
    jobs = ApplyJob.objects.filter(candidate__uname=request.user)

    context = {
        'applied': jobs,
    }

    return render(request, 'candidate/applied_jobs_by_candidate.html', context)


@login_required(login_url='/candi-login')
@user_is_candidate
def withdrawJob(request, id):
    job = ApplyJob.objects.get(job_applied_id=id, candidate__uname=request.user)
    job.delete()
    return redirect('appliedJobsByCandidate')


@login_required(login_url='/recu-login')
@user_is_recruiter
def candidateApplied(request):
    candi_applied = ApplyJob.objects.filter(job_applied__recruiter__uname=request.user)

    context = {
        'candi_applied': candi_applied,
    }

    return render(request, 'recruiter/candidate_applied_job.html', context)


@login_required(login_url='/recu-login')
@user_is_recruiter
def mypostedJobs(request):
    my_jobs = Job.objects.filter(recruiter__uname=request.user).order_by('-timestamp')

    context = {
        'myjobs': my_jobs,
    }

    return render(request, 'recruiter/myposted_jobs.html', context)


@login_required(login_url='/recu-login')
@user_is_recruiter
def deleteJob(request, id):
    del_job = Job.objects.filter(id=id, recruiter__uname=request.user)
    del_job.delete()
    return redirect('mypostedJobs')


@login_required(login_url='/recu-login')
@user_is_recruiter
def resubmitProfileForReview(request):
    recu_detail = Recruiter.objects.get(uname=request.user)
    recu_detail.status = "pending"
    recu_detail.save()

    return redirect('postJob')


@login_required(login_url='/candi-login')
@user_is_candidate
def bookmarkJob(request, id):
    try:
        bookmark_job = BookmarkJob(user=request.user, job_id=id)
        bookmark_job.save()
        messages.success(request, "Job successfully saved !!!")
        return redirect('/job/' + str(id))
    except:
        messages.error(request, "Something went wrong !!!")
        return redirect('/job/' + str(id))


@login_required(login_url='/candi-login')
@user_is_candidate
def savedJobs(request):
    try:
        saved_jobs = BookmarkJob.objects.filter(user=request.user)
    except:
        messages.error(request, "Something went wrong !!!")
        return redirect('savedJobs')

    context = {
        'saved_jobs': saved_jobs
    }

    return render(request, 'candidate/saved_jobs.html', context)


@login_required(login_url='/candi-login')
@user_is_candidate
def deleteBookmark(request, id):
    try:
        del_saved_job = BookmarkJob.objects.get(user=request.user, job_id=id)
        del_saved_job.delete()
        messages.success(request, del_saved_job.job.job_title + " Job Deleted successfully !!!!")
        return redirect('savedJobs')
    except:
        messages.error(request, "Something went wrong !!!")
        return redirect('savedJobs')


@login_required(login_url='/admin-login')
@user_is_admin
def viewAllCandidates(request):
    candi = Candidate.objects.all()

    context = {
        'candi': candi
    }

    return render(request, 'admin/view_all_candidates.html', context)


@login_required(login_url='/admin-login')
@user_is_admin
def viewAllRecruiters(request):
    recu = Recruiter.objects.all()

    context = {
        'recu': recu
    }

    return render(request, 'admin/view_all_recruiter.html', context)


@login_required(login_url='/admin-login')
@user_is_admin
def deleteCandidate(request, id):
    try:
        user = User.objects.filter(id=id)
        user.delete()
        messages.success(request, "Successfully deleted !!!")
    except:
        messages.error(request, "Something went wrong !!!")
        return redirect('viewAllCandidate')

    return redirect('viewAllCandidate')


@login_required(login_url='/admin-login')
@user_is_admin
def deleteRecruiter(request, id):
    try:
        del_recu = User.objects.get(id=id)
        del_recu.delete()
        messages.success(request, "Successfully deleted")
        return redirect('viewAllRecruiter')
    except:
        messages.error(request, "Something went wrong !!!")
        return redirect('viewAllRecruiter')


@login_required(login_url='/admin-login')
@user_is_admin
def newRecruiterRequest(request):
    new_recu = Recruiter.objects.filter(status="pending")

    context = {
        'new_recu': new_recu
    }

    return render(request, 'admin/recruiter_request.html', context)


@login_required(login_url='/admin-login')
@user_is_admin
def assignStatus(request, id):
    recu_info = Recruiter.objects.get(uname_id=id)
    if request.method == 'POST':
        status = request.POST.get('status', False)
        recu_info.status = status
        recu_info.save()

        if status == "accepted":
            message = f'<h1>Hi <strong style="color:blue;">{recu_info.uname.first_name}</strong>, <strong style="color:green;">Good news :)</strong> your account has been <strong style="color: green;">approved</strong>. Now you can post your vacancies !!!</h1>'
        else:
            message = f'<h1>Hi <strong style="color:blue">{recu_info.uname.first_name}</strong>, Sorry to inform you that your account has been <strong style="color:red;">rejected</strong>.</h1>'

        subject = 'Easy Recruit Team'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [recu_info.uname.email, ]
        send_mail(subject, message, email_from, recipient_list, html_message=message, fail_silently=True)

        messages.success(request, "New status has been assigned To " + recu_info.uname.first_name)
        return redirect('newRecruiterRequest')

    context = {
        'recu_info': recu_info
    }
    return render(request, 'admin/assign_status.html', context)


@login_required(login_url='/admin-login')
@user_is_admin
def temporaryDisableAccount(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        status = request.POST.get('status', False)
        if status == "active":
            user.is_active = True
        else:
            user.is_active = False
        user.save()

        if user.role == "candidate":
            messages.success(request, "Account status has been changed")
            return redirect('viewAllCandidate')
        else:
            messages.success(request, "Account status has been changed")
            return redirect('viewAllRecruiter')

    context = {
        'userData': user
    }

    return render(request, 'admin/temporary_disable_account.html', context)


@login_required(login_url='/admin-login')
@user_is_admin
def sendWarningToRecruiter(request, id):
    job = Job.objects.get(id=id)

    subject = f'Warning Form Admin'
    msg = f'Hello <strong>{job.recruiter.uname.first_name}</strong>, ' \
          f'We have noticed that update is required for the below job details <br>' \
          f'<strong>Job Id : </strong> {id} <br>' \
          f'<strong>Job Title : </strong> {job.job_title} <br>' \
          f'<strong>Please Update above job else will be deleted by admin.</strong>'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [job.recruiter.uname.email, ]
    send_mail(subject, msg, email_from, recipient_list, html_message=msg, fail_silently=True)

    messages.success(request, "Warning email has been send to " + job.recruiter.uname.first_name + " !!!")
    return redirect('listJobs')


@login_required(login_url='/admin-login')
@user_is_admin
def deleteJobByAdmin(request, id):
    job = Job.objects.get(id=id)
    job.delete()

    subject = f'Job Deleted By Admin'
    msg = f'Hello <strong>{job.recruiter.uname.first_name}</strong>, ' \
          f'Sorry to inform you that we have deleted the below job <br>' \
          f'<strong>Job Id : </strong> {id} <br>' \
          f'<strong>Job Title : </strong> {job.job_title} <br>'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [job.recruiter.uname.email, ]
    send_mail(subject, msg, email_from, recipient_list, html_message=msg, fail_silently=True)

    messages.success(request, "Job successfully deleted")
    return redirect('listJobs')


"""

Update the changes on deployment serer

"""


@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("EasyRecruit/easyrecruit.pythonanywhere.com/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")
