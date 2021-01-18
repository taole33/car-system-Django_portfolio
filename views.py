from django.template.response import TemplateResponse
from django.views import generic
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q



from carmanage.forms import CarForm , ClashForm , ScrapForm ,SearchForm
from carmanage.models import Car,Clash,Scrap

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



########車両表示から車両登録まで####################
@login_required
def show_all(request):
        cardatabase = Car.objects.all
        show_mode="all"
        return TemplateResponse(request,'carmanage/manage.html',{'cardatabase':cardatabase,'show_mode':show_mode})

@login_required
def show_exist(request):

    cardatabase = Car.objects.filter(scrap__scrap=None) #True→Falseにしたケースが漏れている（後日修正）
    show_mode="exist"
    return TemplateResponse(request,'carmanage/manage.html',{'cardatabase':cardatabase,'show_mode':show_mode})

@login_required
def top(request):
    text = 'お知らせ内容を表示'
    return TemplateResponse(request,'carmanage/top.html',{'text':text})


@login_required
class RegisterView(generic.FormView):
    template_name = 'carmanage/regist.html'
    form_class = CarForm


@login_required
def register(request):

    form = CarForm() #インスタンス化
    #GETのときの処理
    if request.method =='GET':
        return TemplateResponse(request, 'carmanage/regist.html',{'form': form}) 

    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['form_data'] = request.POST #セッションで入力内容を持っておく
            return redirect('carmanage:regist_success')#POSTではredirect推奨
        else:
            form = CarForm()

@login_required
def register_success(request):
    form = request.session.get('form_data')
    return TemplateResponse(request, 'carmanage/regist_success.html',
                            {'form': form})

###############事故車関係########################
@login_required
def clash_regist(request):
    form = ClashForm() #インスタンス化

    if request.method == 'POST':
        form = ClashForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['form_data'] = request.POST #セッションで入力内容を持っておく
            #return redirect('carmanage:regist_success')#POSTではredirect推奨
        else:
            form = ClashForm()
    
    #GETのときの処理
    return TemplateResponse(request, 'carmanage/clash_regist.html',
                            {'form': form}) 

@login_required
def clash_list(request):
    clashdatabase = Clash.objects.all

    return TemplateResponse(request,'carmanage/clash_list.html',{'clashdatabase':clashdatabase})


###############廃車関係########################
@login_required
def scrap_regist(request):
    form = ScrapForm() #インスタンス化

    if request.method == 'POST':
        form = ScrapForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['form_data'] = request.POST #セッションで入力内容を持っておく
            #return redirect('carmanage:regist_success')#POSTではredirect推奨
        else:
            form = ScrapForm()
    
    #GETのときの処理
    return TemplateResponse(request, 'carmanage/scrap_regist.html',
                            {'form': form})                             
                            
@login_required
def scrap_list(request):
    scrapdb = Scrap.objects.all

    return TemplateResponse(request,'carmanage/scrap_list.html',{'scrapdb':scrapdb})


########車両詳細関係###########
@login_required
def car_detail(request, car_id):
    try:
        car = Car.objects.filter(id=car_id)
    except Car.DoesNotExist:
        raise Http404

    try:
        clash = Clash.objects.filter(car__id=car_id)
    except Clash.DoesNotExist:
        raise Http404

    try:
        scrap = Scrap.objects.filter(car__id=car_id)
    except Scrap.DoesNotExist:
        raise Http404

    return TemplateResponse(request, 'carmanage/car_detail.html',{'car': car,'clash':clash,'scrap':scrap})



########車両編集機能関係###########
@login_required
def car_edit(request,car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('carmanage:car_detail',
                                                args=(car_id,)))
    else:
        form = CarForm(instance=car)

    return TemplateResponse(request, 'carmanage/car_edit.html',
                            {'form': form, 'car': car})





#####################車両検索関係###########################

@login_required
def car_search(request):
    form = SearchForm() #インスタンス化

    if request.method == 'POST':
        form = SearchForm(request.POST)
        
        searchregion = form.data["region"]
        searchbunruinum = form.data["bunruinum"]
        searchhiragana = form.data["hiragana"]
        searchnumber = form.data["number"]
        searchprice = form.data["price"]
        searchdistance = form.data["distance"]

        if form.is_valid():
            request.session['form_data'] = request.POST #セッションで入力内容を持っておく
            if searchregion:
                cardatabase = Car.objects.filter(region__icontains=searchregion)    
            if searchbunruinum:
                cardatabase = Car.objects.filter(bunruinum__icontains=searchbunruinum)
            if searchhiragana:
                cardatabase = Car.objects.filter(hiragana__icontains=searchhiragana)
            if searchnumber:
                cardatabase = Car.objects.filter(number__icontains=searchnumber)
            if searchdistance:
                cardatabase = Car.objects.filter(distance__icontains=searchdistance)
            if searchprice:
                cardatabase = Car.objects.filter(price=searchprice)
            show_mode = "search"
            return TemplateResponse(request,'carmanage/manage.html',{'cardatabase':cardatabase,'show_mode':show_mode})


    
    #GETのときの処理
    return TemplateResponse(request, 'carmanage/car_search.html',
                            {'form': form})  

# 同じサーバーで動かすためのcaradmin用の設定
