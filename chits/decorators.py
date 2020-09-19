from chits.models import * 
from accounts.models import * 
from django.shortcuts import redirect


def user_check(func,*args,**kwargs) :
    def wrapper(request,*args,**kwargs) :
       
        user = request.user 
        role = kwargs['role']
        if user is not None :
            if role !=user.role :
            
                if user.role =="DT" :
                    return redirect('chits:deligate_index')
                elif user.role=="MD" :
                    return redirect('chits:moderator_index')
                elif user.role =="JD" :
                    return redirect('chits:judge_index')
            else :
                return func(request,*args,**kwargs)
        else :
            return redirect('accounts:login')

    return wrapper

        
