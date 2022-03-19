from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth import logout as logout_
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from rent.models import UserAdditionalInfo
from .forms import PasswordChangeForm

#redirectng the user to login page after logout
def logout(request):
    logout_(request)
    return redirect('login')

def forgot_password(request):
    try:
        value = request.session['username']
    except:
        return render(request, 'rent/forgot-password.html', {'errors': [f"No User found"]})
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
                return render(request, 'rent/forgot-password2.html', {"security_question":security_question.security_question,'errors':["Incorrect Answer"]})
        else:
            messages.error(request, "The user doesn't have a security question.")

            return redirect('login')
            
        

    if user:
        if UserAdditionalInfo.objects.filter(user = user):
            security_question = UserAdditionalInfo.objects.get(user=user)

            return render(request, 'rent/forgot-password2.html', {"security_question":security_question.security_question})
        
        messages.error(request, "The user doesn't have a security quesion.")

        return redirect('login')

    del(request.session['username'])
    request.session['errors']=[f"No User found with the username {value}"]
    return redirect('forgot')

def forgot(request):
    context={}
    if 'errors' in request.session.keys():
        context['errors']=request.session['errors']

        del(request.session['errors'])

    if request.POST:
        username= request.POST.get("username")
        request.session['username']=username
        
        return redirect('forgot-password')

    return render(request, 'rent/forgot-password.html',context)



class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    template_name = 'rent/forgot-password3.html'
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

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
