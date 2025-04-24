from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from pharmacy.forms import PatientForm, PatientSelfRegistrationForm, PrescriptionForm, PrescriptionUploadForm
from pharmacy.models import CustomUser, Patients
from django.contrib.auth.decorators import login_required
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def custom_error_view(request, exception=None, status_code=400):
    error_messages = {
        400: ('Bad Request', 'The server cannot process the request due to a client error.'),
        403: ('Forbidden', 'You don\'t have permission to access this resource.'),
        404: ('Not Found', 'The page you\'re looking for doesn\'t exist or has been moved.'),
        500: ('Server Error', 'Something went wrong on our end. We\'re working to fix it.'),
        503: ('Service Unavailable', 'The server is temporarily unable to handle the request.')
    }
    
    error_code = status_code
    error_message, error_description = error_messages.get(status_code, ('Error', 'An unexpected error occurred.'))
    
    return render(request, 'error.html', {
        'error_code': error_code,
        'error_message': error_message,
        'error_description': error_description
    }, status=status_code)


def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            # Create a new patient
            patient = form.save(commit=False)
            patient.save()
            messages.success(request, 'Patient registered successfully!')
            return redirect('admin_dashboard')  # Redirect to a success page
    else:
        form = PatientForm()
    return render(request, 'register_patient.html', {'form': form},status=200)

def patient_register(request):
    
    if request.method == 'POST':
        form = PatientSelfRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    user_type=5  # Indicates "Patient" user type
                )
                
                # Create patient profile
                Patients.objects.create(
                    admin=user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_number=form.cleaned_data['phone_number'],
                    gender=form.cleaned_data['gender']
                )
                
                # Log the user in
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to our pharmacy system')
                return redirect('pharmacy:patient_home')
            
            except IntegrityError as e:
                if 'username' in str(e):
                    messages.error(request, 'Username already exists. Please choose a different username.')
                elif 'email' in str(e):
                    messages.error(request, 'Email already registered. Please use a different email.')
                else:
                    messages.error(request, f'Registration failed due to system error: {str(e)}')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')

        # Render the form with error messages
        return render(request, 'patient_templates/patient_register.html', {'form': form})
    else:
        # Render the blank form for GET requests
        form = PatientSelfRegistrationForm()
        return render(request, 'patient_templates/patient_register.html', {'form': form})


@login_required
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            if hasattr(request.user, 'patients'):
                prescription.patient_id = request.user.patients.id  # Ensure user is linked to a patient
                prescription.save()
                messages.success(request, 'Your prescription/concern has been submitted successfully!')
                return redirect('patient_dashboard')
            else:
                messages.error(request, 'Prescription upload failed. Please contact support.')
    else:
        form = PrescriptionUploadForm()

    return render(request, 'patient_templates/upload_prescription.html', {'form': form},status=200)
