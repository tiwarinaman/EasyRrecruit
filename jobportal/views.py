import datetime
from datetime import date

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect

from jobportal.permission import *
# Importing models class
from .models import Candidate, Recruiter, PostJob, ApplyJob

User = get_user_model()


# Create your views here.
def home(request):
    job_data = PostJob.objects.get_queryset().order_by('-timestamp')

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
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def contact(request):
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

    return render(request, 'candidate_register.html')


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

    return render(request, 'candidate_login.html')


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

    return render(request, 'recruiter_register.html')


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

    return render(request, 'recruiter_login.html')


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

    return render(request, 'admin_login.html')


# Admin Home page render
@login_required(login_url='/admin-login')
@user_is_admin
def admin_home(request):
    return render(request, 'admin_home.html')


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

    return render(request, 'change_password.html')


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
    return render(request, 'edit_profile.html', {'candi': candi})


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
    return render(request, 'edit_profile.html', {'recu': recu})


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
                    post = PostJob.objects.create(recruiter=recu, job_title=jobTitle, job_location=jobLocation,
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
    return render(request, 'post_job.html', {'recu': recu, 'date': d.strftime("%Y-%m-%d")})


def jobDetails(request, id):
    try:
        job_details = PostJob.objects.get(pk=id)
    except:
        messages.error(request, "This job might be deleted by recruiter !!!")
        return redirect('listJobs')

    context = {
        'job_details': job_details,
    }

    return render(request, 'job_details.html', context)


def listJobs(request):
    all_jobs = PostJob.objects.all().order_by('-timestamp')

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

    return render(request, 'list_jobs.html', context)


@login_required(login_url='/candi-login')
@user_is_candidate
def applyJob(request, id):
    user = User.objects.get(id=request.user.id)
    candi = Candidate.objects.get(uname=user)
    job = PostJob.objects.get(id=id)

    if request.method == 'POST':
        candi_resume = request.FILES.get('resume', False)
        if not candi_resume:
            messages.error(request, "Please upload your resume !!!")
            return redirect('/apply/' + str(id))
        else:
            apply = ApplyJob.objects.create(job_applied=job, candidate=candi, resume=candi_resume)
            apply.save()

            messages.success(request, "Successfully applied !!!")
            return redirect('/job/' + str(id))

    context = {
        'candi': candi,
        'job': job
    }

    return render(request, 'apply_job.html', context)


@login_required(login_url='/candi-login')
@user_is_candidate
def appliedJobsByCandidate(request):
    jobs = ApplyJob.objects.filter(candidate__uname=request.user)

    context = {
        'applied': jobs,
    }

    return render(request, 'applied_jobs_by_candidate.html', context)


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

    return render(request, 'candidate_applied_job.html', context)


@login_required(login_url='/recu-login')
@user_is_recruiter
def mypostedJobs(request):
    my_jobs = PostJob.objects.filter(recruiter__uname=request.user)

    context = {
        'myjobs': my_jobs,
    }

    return render(request, 'myposted_jobs.html', context)


@login_required(login_url='/recu-login')
@user_is_recruiter
def deleteJob(request, id):
    del_job = PostJob.objects.filter(id=id, recruiter__uname=request.user)
    del_job.delete()
    return redirect('mypostedJobs')