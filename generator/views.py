from django.shortcuts import render
from PIL import Image
import pytesseract
from generator.models import *
from generator.refine_text import *
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import monitor
from .PK_From_DB import *
from .make_blank import Create_Blank
from .make_image import make_image
from googletrans import Translator
from .forms import PhotoForm
import EVM.settings
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def home(request):
    _email = request.session.get('user')
    problem_num = problem.objects.filter(ID=_email).count()
    context = {'email': _email, 'PN': problem_num}
    return render(request, 'generator/Dashboard.html', context)

#사진 업로드 하는 창 부름
def Upload_Photo(request):
    _email = request.session.get('user')
    problem_num = problem.objects.filter(ID=_email).count()

    context = {'email': _email, 'PN': problem_num}

    return render(request, 'generator/Upload_Photo.html', context)

#업로드 된 문제에 관한 정보들을 갖고, problem DB에 저장. 그리고 scan_from_DB로 OCR 인식.
def create(request):
    if(request.method == 'POST'):
        _problem_id = GET_PK("problem")
        _problem_type = request.POST['problem_type']
        _blank_num = int(request.POST['blank_num'])
        _answer = int(request.POST['answer'])
        _info = request.POST['info']
        _keyword_duplicate = request.POST['keyword_duplicate']
        if _keyword_duplicate == 'True':
            _keyword_duplicate = True
        else:
            _keyword_duplicate = False
        _email = request.session.get('user')
        _user = monitor.objects.get(email=_email)

        for img in request.FILES.getlist('imgs'):
            _imgs = img

        _problem = problem(problem_id = _problem_id,ID=_user,type=_problem_type, image=_imgs,
                           blank_num=_blank_num, answer=_answer, info=_info, keyword_duplicate=_keyword_duplicate).save()
        context = scan_img_from_DB(_problem_id)
        context['email']=_email
        context['id']=_problem_id

        request.session['problem_id'] = _problem_id

        return render(request, 'generator/OCR.html', context)
    else:
        return render(request, 'generator/Upload_Photo.html')

#업로드된 문제를 필요에 따라 이미지 자르기.
def beforeImageCrop(request):
    _email = request.session.get('user')
    problem_num = problem.objects.filter(ID=_email).count()
    _problem_id = request.session.get('problem_id')
    _problem = problem.objects.get(problem_id=_problem_id)
    _example = problem.objects.get(problem_id="000000000001")

    problems = problem.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('beforeImageCrop')
    else:
        form = PhotoForm()

    context = {'email': _email, 'PN': problem_num, 'form': form, 'problem': _problem, 'example': _example}

    return render(request, 'generator/ImageCrop.html', context)

#크롭된 이미지에 관한 내용 problem DB에 저장. 그리고 scan_from_DB로 OCR 인식.
def createCropImage(request):
    if(request.method == 'POST'):
        _problem_id = request.session.get('problem_id')
        _email = request.session.get('user')
        _user = monitor.objects.get(email=_email)

        _problem = problem.objects.get(problem_id=_problem_id)

        for img in request.FILES.getlist('imgs'):
            _imgs = img

        _problem.image=_imgs
        _problem.save()

        context = scan_img_from_DB(_problem_id)
        context['email']=_email
        context['id']=_problem_id

        request.session['problem_id'] = _problem_id

        return render(request, 'generator/OCR.html', context)
    else:
        return render(request, 'generator/Upload_Photo.html')

def show_problem(request):
    _email = request.session.get('user')
    context = {}
    context['email'] = _email

    _text = request.POST.get('text', '')
    _problem_id = request.session.get('problem_id','')

    _update_prob = problem.objects.get(problem_id=_problem_id)

    _info = _update_prob.info

    # 빈칸 생성.
    _problem_text = Create_Blank(_text, _update_prob.blank_num, _update_prob.keyword_duplicate)

    _img = make_image(_problem_text, _info)

    _img_name = "\\results\\"+_problem_id+"_blank.png"
    _img_path = EVM.settings.MEDIA_ROOT + _img_name

    _img.save(_img_path)

    _update_prob.problem_image = _img_path
    _update_prob.text = _text
    _update_prob.blank_text = _problem_text

    translator = Translator()
    translated_text = translator.translate(_text, dest='ko', src='en').text
    _update_prob.translation_text = translated_text
    _update_prob.save()

    context['problem'] = _update_prob

    return render(request, 'generator/Show_BlankText.html', context)


#DB에서 해당 problem_id 찾은 후, 해당 problem에서 지문 추출 후, 정제까지 완료. 정제된 지문 앱으로 전달.
def scan_img_from_DB(id):
    temp_problem = problem.objects.get(problem_id=id)
    img = Image.open(temp_problem.image)
    one_text = pytesseract.image_to_string(img, lang='kor+eng')

    refined_text = ""

    #유형에 따른 지문 정제
    if(temp_problem.type=="order"):
        refined_text = type_order(one_text, temp_problem.answer)
    elif(temp_problem.type=="blank"):
        refined_text = type_blank(one_text, temp_problem.answer)
    elif (temp_problem.type == "insert"):
        refined_text = type_insert(one_text, temp_problem.answer)
    elif (temp_problem.type == "subject"):
        refined_text = type_subject(one_text)

    temp_problem.text = refined_text
    temp_problem.save()

    context = {'problem':temp_problem}
    return context

# 사용자가 생성한 problem들 보여주기.
def show_UserProblem(request):
    _email = request.session.get('user')
    context = {}
    context['email'] = _email

    candidates = problem.objects.filter(ID=_email)
    context['candidates'] = candidates

    return render(request, 'generator/Show_UserProblemList.html', context)


# 사용자가 생성한 problem 1개 보여주기.
def show_OneProblem(request, word):
    _email = request.session.get('user')
    context = {}
    context['email'] = _email

    candidates = problem.objects.get(problem_id=word)
    context['candidates'] = candidates

    return render(request, 'generator/OneProblem.html', context)

# 사용자가 바꾸려는 problem 1개 보여주기.
def show_OneBlankNum(request, word):
    _email = request.session.get('user')
    context = {}
    context['email'] = _email

    candidates = problem.objects.get(problem_id=word)
    context['candidates'] = candidates

    return render(request, 'generator/OneBlankNum.html', context)

# 사용자가 생성한 problem과 빈칸 개수들 보여주기.
def show_UserBlankNum(request):
    _email = request.session.get('user')
    context = {}
    context['email'] = _email

    candidates = problem.objects.filter(ID=_email)
    context['candidates'] = candidates

    return render(request, 'generator/ChangeBlankNum.html', context)

def change_BlankNum(request,word):
    _email = request.session.get('user')
    context = {}
    context['email'] = _email

    _update_prob = problem.objects.get(problem_id=word)
    _problem_id = _update_prob.problem_id

    _blankNum = request.POST.get('blank_num','')
    _update_prob.blank_num = int(_blankNum)

    _keyword_duplicate = request.POST.get('keyword_duplicate', '')
    if _keyword_duplicate == 'True':
        _keyword_duplicate = True
    else:
        _keyword_duplicate = False
    _update_prob.keyword_duplicate = _keyword_duplicate

    _text = _update_prob.text
    _info = _update_prob.info

    # 빈칸 생성.
    _problem_text = Create_Blank(_text, _blankNum, _keyword_duplicate)

    _img = make_image(_problem_text, _info)

    _img_name = "\\results\\"+_problem_id+"_blank.png"
    _img_path = EVM.settings.MEDIA_ROOT + _img_name

    _img.save(_img_path)

    _update_prob.problem_image = _img_path
    _update_prob.text = _text
    _update_prob.blank_text = _problem_text

    _update_prob.save()

    context['candidates'] = _update_prob

    return render(request, 'generator/OneProblem.html', context)

# 개발자 정보
def show_DeveloperInfo(request):
    _email = request.session.get('user')
    context = {}
    context['email'] = _email

    return render(request, 'generator/DeveloperInfo.html', context)



