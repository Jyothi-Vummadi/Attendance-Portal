from doctest import script_from_examples
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm,date_form,stud
from django.contrib.auth import authenticate, login
from pyexpat.errors import messages
from colorama import Cursor
from django.db import connection
from django.shortcuts import render
import sys
import tkinter as tk
from tkinter import messagebox
import cv2
from django.views import View
import face_recognition
import pickle
import numpy as np
import time
import pickle
from datetime import datetime,date
from django.contrib import messages
from . models import User
from me22.forms import LoginForm,SignUpForm
from me22.models import att
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


def homepage(request):
    return render(request, 'home.html')

def sav(request):
    return render(request, 'sav.html')

def choice(request):
    return render(request, 'tav.html')

def embeddings(name, ref_id):
    sys.path.append('D:\BVRIT\SOFTWARES\PYTHON\Python\Lib')
    n = 5
    try:
        f = open("ref_name.pkl", "rb")

        ref_dictt = pickle.load(f)
        f.close()
    except:
        ref_dictt = {}
    ref_dictt[ref_id] = name
    f = open("ref_name.pkl", "wb")
    pickle.dump(ref_dictt, f)
    f.close()
    try:
        f = open("ref_embed.pkl", "rb")

        embed_dictt = pickle.load(f)
        f.close()
    except:
        embed_dictt = {}

    def msg(k):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Info", "Image "+str(k+1)+"/"+str(n) +
                            " has been captured\nClick OK to Continue\nPress Enter to Close")

    def close():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "Info", "Turning Off Camera...\nClick OK to end the Program")

    for i in range(n):
        key = cv2. waitKey(1)
        webcam = cv2.VideoCapture(0)
        while True:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            key = cv2.waitKey(1)
            if key == 32:
                face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                if face_locations != []:
                    face_encoding = face_recognition.face_encodings(frame)[0]
                    if ref_id in embed_dictt:
                        embed_dictt[ref_id] += [face_encoding]
                    else:
                        embed_dictt[ref_id] = [face_encoding]
                    webcam.release()
                    cv2.waitKey(1)
                    msg(i)
                    break
            elif key == 13:
                webcam.release()
                close()
                cv2.destroyAllWindows()
    webcam.release()
    close()
    cv2.destroyAllWindows()

    f = open("ref_embed.pkl", "wb")
    pickle.dump(embed_dictt, f)
    f.close()

def register_stu(request):
    msg = None
    User.is_fac = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['first_name']
            ref_id = form.cleaned_data['username']
            embeddings(name, ref_id)
            messages.success(request, 'You have Registered Successfully!!')
            form.save()
            return redirect('sav')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register_student.html', {'form': form, 'msg': msg})

def register_fac(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            ref_id = form.cleaned_data['username']
            form.save()
            c = User.objects.get(Q(username=ref_id))
            print(c)
            c.is_fac = True
            c.save()
            return redirect('choice')
        else:
            msg = 'Form is not valid'
            return render(request,'register_teacher.html', {'form': form,'msg':msg})
    else:
        form = SignUpForm()
        return render(request,'register_teacher.html', {'form': form})


def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            use = request.user
            if user is not None and user.is_fac:
                return redirect('choice')
            elif user is not None and user.is_fac is False:
                print(user)
                samples = att.objects.filter(id_s = user)
                print(samples)
                return render(request,'sav.html',{'samples': samples})
                # return redirect('sav')
            else:
                msg = 'Invalid Credentials'
                return render(request, 'login.html', {'form': form,'msg':msg})
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def faculty(request):
    return render(request,'faculty.html')

def student(request):
    return render(request,'student.html')

def recognition(request):
    at = False
    yea = date.today().year
    mon = date.today().month
    dat = date.today().day
    at = att.objects.filter(date__year=str(yea), date__month=str(mon),date__day=str(dat)).exists()
    if at is True:
        return render(request,'att_msg.html')
    else:
        def close():
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(
                "Info", "Turning Off Camera...\nClick OK to end the Program")
        f = open("D:\\MSE\\Attendance_2\\ref_name.pkl", "rb")
        ref_dictt = pickle.load(f)
        f.close()
        f = open("D:\\MSE\\Attendance_2\\ref_embed.pkl", "rb")
        embed_dictt = pickle.load(f)
        f.close()
        known_face_encodings = []
        known_face_names = []
        for ref_id, embed_list in embed_dictt.items():
            for embed in embed_list:
                known_face_encodings += [embed]
                known_face_names += [ref_id]
        video_capture = cv2.VideoCapture(0)
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        dates = []
        times = []
        names = []
        l = len(times)
        t_end = time.time() + 60*10
        while time.time() < t_end:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)
                    if len(times) < len(face_names):
                        names.append(name)
                        dates.append(str(datetime.today()).split()[0])
                        times.append(datetime.now().strftime("%H:%M:%S"))
            process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35),
                            (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    frame, ref_dictt[name], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == 13:
                close()
                break
        l = len(times)
        for i in range(l):
            print(int(names[i]))
            s_id = User.objects.filter(username=int(names[i])).first()
            temp = att(id_s=s_id, date=dates[i], time=times[i])
            temp.save()
        video_capture.release()
        cv2.destroyAllWindows()
        return render(request,'att_tak.html')

# @method_decorator(login_required, name='dispatch')
class display_date(View):
    def get(self, request):
        form = date_form()
        return render(request, 'tav_date.html', {'form': form})
    def post(self, request):
        form = date_form(request.POST)
        if form.is_valid():
            DD = form.cleaned_data['D']
            MM = form.cleaned_data['M']
            YY = form.cleaned_data['Y']
            samples = att.objects.filter(date__year=str(YY), date__month=str(MM),date__day=str(DD))
            if samples.exists():
                print(samples)
                form = date_form()
                return render(request, 'tav_date.html', {'form':form,'samples': samples})
            else:
                msg = 'No Data Found'
                return render(request, 'tav_date.html', {'form': form,'msg':msg})
        else:
            msg = 'Invalid Form'
            return render(request, 'tav_date.html', {'form': form,'msg':msg})


# @method_decorator(login_required, name='dispatch')
class display_name(View):
    def get(self, request):
        form = stud()
        return render(request, 'tav_name.html', {'form': form})
    def post(self, request):
        form = stud(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            print(name)
            cd = User.objects.filter(username=name).exists()
            if cd is False:
                msg = 'No User Found'
                return render(request, 'tav_n.html', {'form': form,'msg':msg})
            else:
                c = User.objects.get(Q(username=name))
                print('Sid is: '+str(c))
                print('Sid is: '+str(c))
                samples = att.objects.filter(id_s=c)
                if samples.exists():
                    print(samples)
                    form = stud()
                    return render(request, 'tav_n.html', {'form': form,'samples': samples})
                else:
                    msg = 'No Data Found'
                    return render(request, 'tav_n.html', {'form': form,'msg':msg})
        else:
            msg = 'Invalid Form'
            return render(request, 'tav_n.html', {'form': form,'msg':msg})
