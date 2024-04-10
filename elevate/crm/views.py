from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, CreateClassForm, StudentForm, TransactionForm, ImageUploadForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import auth

from .models import ClassModel, StudentModel, TransactionModel, UploadedImage

from django.contrib.auth import authenticate, login, logout

from PIL import Image

import pytesseract

import spacy

import re

from spacy.matcher import Matcher
# - Authentication models and functions

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def homepage(request):

    return render(request, 'crm/index.html')


def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("my-login")

    context = {'registerform':form}

    return render(request, 'crm/register.html', context=context)

def create_class(request):
    if request.method == 'POST':
        form = CreateClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_class_data')  # Redirect to a success page or wherever you want
    else:
        form = CreateClassForm()
    
    return render(request, 'crm/create_class.html', {'form': form})

def display_class_data(request):
    class_data = ClassModel.objects.all()
    return render(request, 'crm/fetch_class.html', {'class_data': class_data})

def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_student_data')
            # Redirect or do something else after successful form submission
    else:
        form = StudentForm()
    
    return render(request, 'crm/create_student.html', {'form': form})

def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_transaction_data')
            # Redirect or do something else after successful form submission
    else:
        form = TransactionForm()
    
    return render(request, 'crm/create_transaction.html', {'form': form})

def display_transaction_data(request):
    transaction_data = TransactionModel.objects.all()
    return render(request, 'crm/fetch_transaction.html', {'transaction_data': transaction_data})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            instance = form.save()

            # Get the path of the uploaded image
            image_path = instance.image.path

            # Open the uploaded image using PIL
            uploaded_image = Image.open(image_path)

            # Use pytesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(uploaded_image)

            # Extract values after "Student Number:" and "Ksh:" using string manipulation
            student_number = None
            amount_paid = None

            # Load the English language model in spaCy
            nlp = spacy.load('en_core_web_sm')

            # Process the text using spaCy
            doc = nlp(extracted_text)

            # Define a spaCy matcher to identify specific patterns for student number and amount
            matcher = Matcher(nlp.vocab)
            pattern_student_number = [{"LOWER": "student"}, {"LOWER": "number"}, {"IS_PUNCT": True, "OP": "?"}, {"SHAPE": "ddd"}]
            # pattern_amount_paid = [{"LOWER": "ksh"}, {"IS_PUNCT": True, "OP": "?"}, {"SHAPE": "dddd"}]

            pattern_amount_paid = [{"LOWER": "ksh"}, {"IS_PUNCT": True, "OP": "?"}, {"TEXT": ":", "OP": "?"}, {"IS_SPACE": True, "OP": "?"}, {"SHAPE": "dddd"}]


            matcher.add("STUDENT_NUMBER", [pattern_student_number])
            matcher.add("AMOUNT_PAID", [pattern_amount_paid])

            # print ("Matcher details : " ,
            #        matcher)

            # Find matches in the processed text
            matches = matcher(doc)

            # Extract Student Number and Amount Paid from matches
            for match_id, start, end in matches:
                if nlp.vocab.strings[match_id] == "STUDENT_NUMBER":
                    student_number = doc[start:end].text.strip().split(":")[-1].strip().zfill(3)
                elif nlp.vocab.strings[match_id] == "AMOUNT_PAID":
                    amount_paid = doc[start:end].text.strip().split(":")[-1].strip()
             
            student_number_pattern = re.compile(r'Student Number:\s*(\d+)')
            ksh_pattern = re.compile(r'Ksh:\s*(\d+)')
            # reg_pattern = re.compile(r'Receipt #:\s*(\d+)')

            extracted_text = extracted_text.replace('‘', "").replace('’', "'")

            # Search for matches
            student_number_match = student_number_pattern.search(extracted_text)
            ksh_match = ksh_pattern.search(extracted_text)

            receipt_no = None

            receipt_no_index = extracted_text.find("Receipt No:")
            if receipt_no_index != -1:
                receipt_no = extracted_text[receipt_no_index + len("Receipt No:"):].split()[0]

            print("receipt no =>", receipt_no)

            # reg_match = reg_pattern.search(extracted_text)


            print("Extracted text" , extracted_text)            

            # Extract values
            student_number = student_number_match.group(1) if student_number_match else None
            ksh_value = ksh_match.group(1) if ksh_match else None
            # reg_value = reg_match.group(1) if reg_match else None

            # print("Receipt no: " ,reg_value)
            print("Amount:" , ksh_value)
             # Convert amount_paid to decimal for storage in the model
            
            # try:
            amount_paid_decimal = float(ksh_value)
            # amount_paid_decimal = (ksh_value)

            # except 
            

            # Find the StudentModel instance based on the extracted student_number
            student_instance = None
            if student_number:
                try:
                    student_instance = StudentModel.objects.get(id=int(student_number))
                except StudentModel.DoesNotExist:
                    # Handle the case where the student with that number doesn't exist
                    student_instance = student_number
                    print("Error in converting :")
                    pass
                
            try:
                existing_transaction = TransactionModel.objects.get(receipt_no=receipt_no)
                pass
            except TransactionModel.DoesNotExist:
                transaction = TransactionModel.objects.create(
                amount=amount_paid_decimal,
                student_number=student_instance,
                receipt_no = receipt_no
                # receipt_no = reg_value
                    # Assuming student_number is a ForeignKey field
            )

            return redirect('display_transaction_data')
       
    else:
        form = ImageUploadForm()
    return render(request, 'crm/upload_image.html', {'form': form})
    
def display_student_data(request):
    student_data = StudentModel.objects.all()
    return render(request, 'crm/fetch_student.html', {'student_data': student_data})

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'loginform':form}

    return render(request, 'crm/my-login.html', context=context)


def user_logout(request):

    auth.logout(request)

    return redirect("")

def dashboard(request):

    return render(request, 'crm/dashboard.html')

