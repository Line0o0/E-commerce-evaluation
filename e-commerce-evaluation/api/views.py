from django.conf import settings
from django.http import JsonResponse
from . import models
import hashlib
import time
import sys
sys.path.append('/home/admin/e-commerce-evaluation/predict')
sys.path.append('/home/admin/e-commerce-evaluation/crawler')

from Sentiment_lstm import lstm_predict, lstm_predict_score, lstm_file_predict
from Amazon import *
from formating import formating
from math import ceil
import os

par_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(par_dir)

#配置爬虫环境
def config_crawler():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 设置中文
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    #添加useragent
    ua = UserAgent()
    user_agent = ua.random
    string = 'user-agent="'+ua.random+'"'
    chrome_options.add_argument(string)

    #不显示图片，加快加载速度
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    #添加代理
    # r = requests.get('http://127.0.0.1:5010/get_all/').content
    # PROXY = random.choice(r)
    # PROXY=requests.get('http://127.0.0.1:5010/get/').content
    # chrome_options.add_argument('--proxy-server=http://'+PROXY)

    browser = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(browser, 15)
    return browser, wait

#将原码转为四位哈希码
def hash_code(s, salt='e-commerce-evaluation'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()[0:4]

#发送验证邮件或信息反馈邮件
def send_email(email,message,code):
    from django.core.mail import EmailMultiAlternatives
    if code == 1:
        subject = '验证码'
        text_content = '感谢注册易评，本网站提供电子产品评价分析功能'
        html_content = '''
                        <p>感谢注册易评，本网站提供电子产品评价分析功能</p>
			    		<p>您的验证码为{}</p>
                        '''.format(message)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        subject = '用户反馈'
        text_content = '用户反馈'
        html_content = '''
                        <p>问题描述：{} </p>
                        <p>联系邮箱：{} </p>
                        '''.format(message,email)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, ['845454427@qq.com'])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

#注册
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        email = request.POST.get('email', '')
        confirmcode = request.POST.get('confirmcode', '')

        if username == '' or email== '' or password1== '' or password2== '' or confirmcode== '':
            data={'code': 'fail', 'message': '请将信息填写完整'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})		
        if password1 != password2:
            data={'code': 'fail', 'message': '两次输入的密码不同'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        elif confirmcode != hash_code(email):
            data={'code': 'fail', 'message': '验证码错误'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            same_name_user = models.User.objects.filter(name=username)
            same_email_user = models.User.objects.filter(email=email)
            if same_name_user:
                data={'code': 'fail', 'message': '用户名已经存在'}
                return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
            if same_email_user:
                data={'code': 'fail', 'message': '该邮箱已被注册'}
                return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

            new_user = models.User()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.save()

            data={'code': 'success', 'message': '注册成功'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

#登陆
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')            
        useremail = request.POST.get('useremail', '')            
        if username == '' and useremail== '':
            data={'code': 'fail', 'message': '请将信息填写完整'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})		
        try:
            if username!='':
                user = models.User.objects.get(name=username)
            elif useremail!='':
                user = models.User.objects.get(email=useremail)
        except :
            data={'code': 'fail', 'message': '用户不存在'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        
        if user.password == hash_code(password):    
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            data={'code': 'success', 'message': '登陆成功'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            data={'code': 'fail', 'message': '密码不正确'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})		

#退出
def logout(request):
    if request.method == 'POST':
        if not request.session.get('is_login', None):
            data={'code': 'fail', 'message': '退出失败'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            request.session.flush()
            data={'code': 'success', 'message': '退出成功'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

#获取验证码
def verify(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email')
        confirmcode = hash_code(email)
        send_email(email,confirmcode,1)	
        data={'code': 'success','message': '发送成功'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

#重置密码
def reset(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        useremail = request.POST.get('email', '')
        newpassword = request.POST.get('password', '')
        newpassword2 = request.POST.get('password2', '')
        confirmcode = request.POST.get('confirmcode', '')
        if username == '' or useremail== '' or newpassword== '' or newpassword2== '' or confirmcode== '':
            data={'code': 'fail', 'message': '请将信息填写完整'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})		
        try:
            user = models.User.objects.get(name=username)
        except :
            data={'code': 'fail', 'message': '用户不存在'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

        if(newpassword!=newpassword2):
            data={'code': 'fail', 'message': '两次输入的密码不同'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        elif(user.email != useremail):
            data={'code': 'fail', 'message': '所填邮箱不是您的注册邮箱'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        elif confirmcode != hash_code(useremail):
            data={'code': 'fail', 'message': '验证码错误'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            user.password=hash_code(newpassword)
            user.save()
            data={'code': 'success', 'message':'重置成功'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        data={'code': 'fail', 'message':'请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

#情感分析：单条评论
def analyze_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        if comment != '':
            result = lstm_predict(comment)
            score = ceil(float(lstm_predict_score(comment))*100)
            data={'code': 'success', 'message': result, 'score': score}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            data={'code': 'fail', 'message': '请输入评论'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

#情感分析：商品链接
def analyze_url(request):
    if request.method == 'POST':
        url = request.POST.get('link', '')
        if url != '':
            #爬取数据
            mybrowser, mywait = config_crawler()
            set_url(url)
            stars=assess_link(mybrowser, mywait)
            mybrowser.quit()
            os.system('killall -e -p chromedriver')
            os.system('killall -e -p chrome')
            #清洗数据
            formating()
            #模型处理
            pos_num,neg_num = lstm_file_predict("../crawler/comment_wash.txt")

            data={'code': 'success', 'positive_number': pos_num, 'negative_number': neg_num,'stars': stars}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            data={'code': 'fail', 'message': '请输入商品链接'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
            
    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

#情感分析：品牌
def analyze_brand(request):
    if request.method == 'POST':
        brand = request.POST.get('brand', '')
        if brand != '':
            #爬取数据
            mybrowser, mywait = config_crawler()
            brand = request.POST.get('brand', '')
            set_brand(brand)
            assess_brand(mybrowser, mywait)
            mybrowser.quit()
            os.system('killall -e -p chromedriver')
            os.system('killall -e -p chrome')
            #清洗数据
            formating()
            #模型处理
            pos_num,neg_num = lstm_file_predict("../crawler/comment_wash.txt")

            data={'code': 'success', 'positive_number': pos_num, 'negative_number': neg_num}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            data={'code': 'fail', 'message': '请输入品牌名称'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})

#联系我们		
def contact(request):
    if request.method == 'POST':
        problem = request.POST.get('problem', '')
        conMail = request.POST.get('conMail', '')
        if(problem==''):
            data={'code': 'success','message': '请填写您的问题'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        elif(conMail==''):
            data={'code': 'success','message': '请填写您的联系方式'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
        else:
            send_email(conMail,problem,2)	
            data={'code': 'success','message': '发送成功'}
            return JsonResponse(data,json_dumps_params={'ensure_ascii':False})
    else:
        data={'code': 'fail', 'message': '请求无效'}
        return JsonResponse(data,json_dumps_params={'ensure_ascii':False})