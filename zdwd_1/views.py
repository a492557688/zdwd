from django.shortcuts import render,render_to_response,HttpResponse,redirect
from zdwd_1 import models
# Create your views here.



def login(requests):
    if requests.method=='GET':
        return render_to_response('login.html')
    else :
        username=requests.POST.get("username")
        password=requests.POST.get("password")
        try:
            user=models.User.objects.get(username=username,password=password)
        except Exception as f :
            # return HttpResponse("登录失败 用户名或密码错误")
            return render(requests, "warning.html", context={"ts": "登录失败 用户名或密码错误"})
        user_obj = models.User.objects.get(username=username)
        if models.keguan_kaojuan.objects.filter(student_id=user_obj) or models.keguan_kaojuan.objects.filter(
                student_id=user_obj):
            # return HttpResponse("您已经完成答题 无需再答题")
            return render(requests, "warning.html", context={"ts": "您已经完成答题 无需再答题"})
        #取出所有客观题
        Keguan = models.Keguan.objects.all()
        Keguan_choise = models.Choise_keguan.objects.all()  #客观的选项

        import random
        zhuguan_querty = models.Zhuguan.objects.all()
        id_list=[obj["id"] for obj in zhuguan_querty.values("id")]
        random.shuffle(id_list)
        zhuguan_count=zhuguan_querty.count()
        tml=models.Conf.objects.first() #几道题
        tml=tml.conf1
        print(tml,zhuguan_count)
        tml=tml if zhuguan_count>tml else zhuguan_count  #展示的题目量

        zhuguan_querty=zhuguan_querty.filter(id__in=id_list)[:tml] #随机取 n个展示的题目量

        requests.session['name'] =username
        return render(requests,template_name='student.html',context={"Keguan":Keguan,"Keguan_choise":Keguan_choise,'zhuguan':zhuguan_querty})


def submit_form(requests):
    if requests.method == 'POST':
        if models.keguan_kaojuan.objects.filter(student_id__username=requests.session['name']) or models.keguan_kaojuan.objects.filter(
                student_id__username=requests.session['name']):
            return HttpResponse("您已经完成答题 无需再答题")


        for k in dict(requests.POST):
            typ,tm=k.split("_")
            answer=requests.POST.get(k) #用户填写的答案
            if typ=='kg':
                user_obj=models.User.objects.get(username=requests.session['name'])
                kg_obj=models.Keguan.objects.get(id=tm)  #获取这个题目对象
                val=kg_obj.val if kg_obj.bingo_answer==answer  else 0  # 如果答案正确设置这道题的分数 否则为0分
                models.keguan_kaojuan.objects.create(student_id=user_obj,tm_id_id=tm,answer=answer,val=val,max_val=kg_obj.val)
            else :#主管
                user_obj = models.User.objects.get(username=requests.session['name']) #取出这个用户
                #从数据库中取出这道题的关键字key
                zg_obj = models.Zhuguan.objects.get(id=tm)  # 获取这个题目的记录
                max_val=zg_obj.val #这道题最大分值
                answer_str=zg_obj.answer_key #答案关键字列表
                answer_list=[i for i in answer_str.split(" ") if i ]  #答案关键字列表
                count=0 #答对个数
                for key in answer_list: #循环这道题所有的关键字
                    if key in answer : #如果在 学生回答的答案里
                        count+=1  #回答个数+1
                bingo_rate=count/len(answer_list) #回答正确比例
                max_val=int(max_val)
                bingo_val=bingo_rate*max_val  #正确分值
                val=round(bingo_val,2)
                # val =int(round((count/len(answer_list))*max_val,0)) # (答对个数/答案个数)*这道题最大分值   比如 5道题答对1道   (1/5)*10分 =2分  比如 5道题答对1道   (1/7)*10分 =2分
                models.zhuguan_kaojuan.objects.create(student_id=user_obj,tm_id_id=tm,answer=answer,val=val,max_val=max_val)
        # return HttpResponse("恭喜您答题完成")
        return render(requests,"warning.html",context={"ts":"恭喜您答题完成"})

from django.db.models import Count,Sum
def order_1(requests):
    if  requests.method == 'GET':
        s_to_val={}  #德丰
        s_to_max_val={} #最高分
        zhuguan_val=models.zhuguan_kaojuan.objects.all()
        for zhuguan_obj in zhuguan_val:
            username=zhuguan_obj.student_id.username
            s_to_val.setdefault(username,0)
            s_to_val[username]+=zhuguan_obj.val  if zhuguan_obj.val else 0

            s_to_max_val.setdefault(username,0)
            s_to_max_val[username] +=zhuguan_obj.max_val
            print(zhuguan_obj.max_val)

        keguan_val = models.keguan_kaojuan.objects.all()
        for kg_obj in keguan_val:
            username = kg_obj.student_id.username
            s_to_val.setdefault(username, 0)
            s_to_val[username] += kg_obj.val  if kg_obj.val else 0
            s_to_max_val.setdefault(username, 0)
            s_to_max_val[username] += kg_obj.max_val
            print(kg_obj.max_val)

        reg=sorted(s_to_val.items(),key=lambda item:item[1],reverse=True)
        reg=tuple([(i[0],
                    i[1],
                    models.User.objects.get(username=i[0]).num,
                    s_to_max_val[i[0]],
                    f"{round((i[1]/s_to_max_val[i[0]])*100,2)} %",
                    )for i in reg])  #(name,分数,学号,总)

        return   render(requests,template_name='order.html',context={"s_to_val":reg})


def index(request):
    return render(request,template_name='index.html')