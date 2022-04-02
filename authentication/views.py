from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth import logout as logout_
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rent.models import UserAdditionalInfo
from .forms import PasswordChangeForm
from rent.views import permissions


#redirectng the user to login page after logout
def logout(request):
    logout_(request)
    return redirect('login')

def forgot_password(request):
    try:
        value = request.session['username']
    except:
        return render(request, 'authentication/forgot-password.html', {'errors': [f"No User found"]})
    try:
        user = User.objects.get(username = value)
    except:
        user=None

    if request.method == "POST" and user:
        if UserAdditionalInfo.objects.filter(user=user):
            security_question = UserAdditionalInfo.objects.get(user=user)
            security_answer = request.POST['security_answer']
            if security_answer == security_question.security_answer:
                request.session['security_answer'] = security_answer
                return redirect('change-password')
            else:
                return render(request, 'authentication/forgot-password2.html', {"security_question":security_question.security_question,'errors':["Incorrect Answer"],"title":"Forgot Password"})
        else:
            messages.error(request, "The user doesn't have a security question.")

            return redirect('login')
            
        

    if user:
        if UserAdditionalInfo.objects.filter(user = user):
            security_question = UserAdditionalInfo.objects.get(user=user)

            return render(request, 'authentication/forgot-password2.html', {"security_question":security_question.security_question,"title":"Forgot Password"})
        
        messages.error(request, "The user doesn't have a security quesion.")

        return redirect('login')

    del(request.session['username'])
    request.session['errors']=[f"No User found with the username {value}"]
    return redirect('forgot')

def forgot(request):
    context={"title":"Forgot Password"}
    if 'errors' in request.session.keys():
        context['errors']=request.session['errors']

        del(request.session['errors'])

    if request.POST:
        username= request.POST.get("username")
        request.session['username']=username
        
        return redirect('forgot-password')

    return render(request, 'authentication/forgot-password.html',context)



class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    template_name = 'authentication/forgot-password3.html'
    title = _('Password change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        security_answer = self.request.session['security_answer']

        user = User.objects.get(username=self.request.session['username'])

        security_question = UserAdditionalInfo.objects.get(user=user)

        if security_answer != security_question.security_answer:
            self.request.session['error'] = ["No username specified"]
            return reverse_lazy("login")

        kwargs['user'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Forgot Password"
        return context
    

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



def page_not_found_view(request, exception):
    context={
        **permissions(request)
    }
    return render(request, '404.html', context)


def error_view(request):
    context={
        **permissions(request)
    }
    return render(request, "500.html", context)

def permission_denied_view(request, exception):
    context={
        **permissions(request)
    }
    return render(request, "403.html", context)

def bad_request_view(request, exception):
    context={
        **permissions(request)
    }
    return render(request, "400.html")