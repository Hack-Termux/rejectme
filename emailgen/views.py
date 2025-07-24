from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import requests
from decouple import config

# 🔹 Email Rejection Generator View
def email_form(request):
    email = None
    error = None

    if request.method == "POST":
        position = request.POST.get("position")
        company = request.POST.get("company")

        prompt = f"""
        Write a short, polite, and personalized follow-up email after being rejected 
        for the position of {position} at {company}. 
        Show continued interest and express professionalism.
        """

        headers = {
            "Authorization": f"Bearer {config('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()
            email = data["choices"][0]["message"]["content"]
        except Exception as e:
            error = "There was an error generating your email. Please try again later."

    return render(request, "form.html", {"email": email, "error": error})

# 🔹 Job Application Form View
def job_application(request):
    letter = None

    if request.method == 'POST':
        name = request.POST['name']
        position = request.POST['position']
        about = request.POST.get('about', '')
        cv_file = request.FILES.get('cv')

        # Upload CV
        cv_url = None
        if cv_file:
            fs = FileSystemStorage()
            filename = fs.save(cv_file.name, cv_file)
            cv_url = fs.url(filename)

        # AI Prompt
        prompt = f"""
        Write a formal job application letter from someone named {name} who is applying 
        for the position of {position}. Here is some background info they provided: "{about}". 
        Make the letter polite, enthusiastic, and professional.
        """

        headers = {
            "Authorization": f"Bearer {config('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()
            letter = data["choices"][0]["message"]["content"]
        except:
            letter = "⚠️ Could not generate application letter. Please try again."

        return render(request, 'job_success.html', {
            'name': name,
            'position': position,
            'about': about,
            'cv_url': cv_url,
            'letter': letter
        })

    return render(request, 'job_form.html')
