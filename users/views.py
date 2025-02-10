from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.conf import settings
from .models import User
import requests
from django.core.files.storage import FileSystemStorage
import json
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from .models import User, TravelPlan, TravelSchedule
from accompany.models import Accompany_Zzim, TravelParticipants, TravelGroup, AccompanyRequest
from flash.models import FlashZzim, Flash
from .serializers import SignupSerializer, UserSerializer, LoginSerializer
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, TravelPlanForm
from django.core.files.base import ContentFile
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accommodation.models import AccommodationReview
from django.http import JsonResponse
from django.template.loader import render_to_string
from market.models import Market,MarketZzim
from django.utils import timezone
from .models import PhoneVerification
import qrcode
import random, string, io, base64, re, imaplib, email
from email.header import decode_header

@csrf_exempt
def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})

def social_login(request):
    return render(request, 'users/social_login.html')

def kakao_login(request):
    client_id = settings.KAKAO_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):
    code = request.GET.get("code")
    client_id = settings.KAKAO_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"  

    token_request = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    token_json = token_request.json()
    
    if "error" in token_json:
        return redirect('users:login')

    access_token = token_json.get("access_token")
    
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    
    kakao_account = profile_json.get("kakao_account", {})
    email = kakao_account.get("email")
    properties = profile_json.get("properties", {})

    kakao_id = profile_json.get("id")
    username = kakao_account.get("profile", {}).get("nickname", f"kakao_{kakao_id}")
    profile_image = properties.get("profile_image")
    birth = kakao_account.get("birthday")
    birth_year = kakao_account.get("birthyear")

    gender = kakao_account.get("gender")
    gender_map = {"male": "M", "female": "F"}
    user_gender = gender_map.get(gender, "U")
    phone_number = kakao_account.get("phone_number")


    full_birth = None

    if birth and birth_year:
        full_birth = f"{birth_year}-{birth[:2]}-{birth[2:]}"

    if not email:
        email = f"kakao_{kakao_id}@example.com"  # 카카오 ID를 활용한 임시 이메일 생성
        properties = profile_json.get("properties", {})
        nickname = properties.get("nickname")
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            social_id=f"kakao_{profile_json.get('id')}",
            username=username,
            nickname=username,
            birth=full_birth,
            user_gender=user_gender,
            user_phone=phone_number
        )
        if profile_image:
            response = requests.get(profile_image)
            if response.status_code == 200:
                image_name = f"profile_images/{user.email.replace('@', '_')}.jpg"
                user.profile_image.save(image_name, ContentFile(response.content))
        user.save()
    login(request, user)
    return redirect('main:home')  

def naver_login(request):
    client_id = settings.NAVER_CLIENT_ID
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback/"
    state = "RANDOM_STATE"
    
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
    )

def naver_login_callback(request):
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback/"  
    code = request.GET.get("code")
    state = request.GET.get("state")
    
    token_request = requests.post(
        "https://nid.naver.com/oauth2.0/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
            "state": state,
        },
    )
    token_json = token_request.json()
    
    if "error" in token_json:
        return redirect("/")
        
    access_token = token_json.get("access_token")
    profile_request = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    
    if profile_json.get("resultcode") != "00":
        return redirect("/")
        
    response = profile_json.get("response")
    email = response.get("email")
    name = response.get("name")
    profile_image_url = response.get("profile_image")
    birth = response.get("birthday")
    birth_year = response.get("birthyear")
    phone_number = response.get("mobile")
    gender_map = {"M": "M", "F": "F"}
    user_gender = gender_map.get(response.get("gender"), "U")

    full_birth = None
    if birth and birth_year:
        full_birth = f"{birth_year}-{birth[:2]}-{birth[3:]}"
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            social_id=f"naver_{response.get('id')}",
            username=name,
            nickname=name,
             birth=full_birth,
            user_gender=user_gender,
            user_phone=phone_number
        )
        if profile_image_url:
            response = requests.get(profile_image_url)  # 이미지 다운로드
            if response.status_code == 200:
                image_name = f"profile_images/{user.email.replace('@', '_')}.jpg"
                user.profile_image.save(image_name, ContentFile(response.content))
        
        user.save()
    
    login(request, user)
    return redirect('main:home')

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        if request.content_type == 'application/json':
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                request.session.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    "token": str(refresh.access_token),
                    "user": {
                        "user_id": user.id,
                        "nickname": user.nickname,
                        "profile_image": user.profile_image.url if user.profile_image else None,
                    }
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            
            if user:
                login(request, user)
                request.session.save()
                return redirect('main:home')
            return render(request, 'login/login.html', {'error': '로그인 실패'})

    def get(self, request):
        return render(request, 'login/login.html')


def signup_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email', "").strip()
            password = request.POST.get('password', "").strip()
            name = request.POST.get('name', "").strip()
            nickname = request.POST.get('nickname', "").strip()
            birth_year = request.POST.get('birth-year', "").strip()
            birth_month = request.POST.get('birth-month', "").strip()
            birth_day = request.POST.get('birth-day', "").strip()
            phone = request.POST.get('phone', "").strip()
            gender = request.POST.get('gender', "").strip()
            profile_image = request.FILES.get('profile-picture')

            print(f"📢 회원가입 요청: email={email}, name={name}, nickname={nickname}")

            if User.objects.filter(email=email).exists():
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': '이미 존재하는 이메일입니다.'})
                else:
                    return render(request, 'register/register.html', {'error': '이미 존재하는 이메일입니다.'})
            
            # 전화번호 중복 체크
            # 전화번호 중복 체크
            if not phone:
                # 전화번호 값이 없으면
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': '전화번호를 입력하세요.'})
                else:
                    return render(request, 'register/register.html', {'error': '전화번호를 입력하세요.'})
            elif User.objects.filter(user_phone=phone).exists():
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': '이미 존재하는 전화번호입니다.'})
                else:
                    return render(request, 'register/register.html', {'error': '이미 존재하는 전화번호입니다.'})


            #  성별 값 변환 (default: 'U' Unknown)
            gender_map = {"male": "M", "female": "F"}
            user_gender = gender_map.get(gender, "U")

            # 닉네임 기본값 설정
            if not nickname:
                nickname = name or "사용자"

            # 생년월일 설정
            if birth_year and birth_month and birth_day:
                birth = f"{birth_year}-{birth_month}-{birth_day}"
            else:
                birth = None  # 기본값 설정 가능

            # 나이 계산 (예외 방지)
            try:
                from datetime import datetime
                current_year = datetime.now().year
                user_age = current_year - int(birth_year) if birth_year.isdigit() else None
            except Exception as e:
                print(f"⚠️ 나이 계산 오류: {e}")
                user_age = None

            # 사용자 생성
            user = User.objects.create_user(
                email=email,
                password=password,
                username=name or nickname,
                nickname=nickname,
                birth=birth,
                user_age=user_age,
                user_gender=user_gender,
                user_phone=phone
            )

            # 프로필 이미지 저장
            if profile_image:
                user.profile_image = profile_image
            else:
                user.profile_image = 'profile_images/default-profile.png'  # 기본 프로필 지정

            user.save()
            print(f"✅ 회원가입 성공: {user.email}")

            # 회원가입 후 자동 로그인
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': f"{request.build_absolute_uri('/')}"} )
            else:
                return redirect('main:home')

        except Exception as e:
            print(f"❌ 회원가입 중 오류 발생: {e}") 
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            else:
                context = {
                    'error': str(e),
                    'email': email,
                    'name': name,
                    'nickname': nickname,
                    'birth-year': birth_year,
                    'birth-month': birth_month,
                    'birth-day': birth_day,
                    'phone': phone,
                    'gender': gender,
                }
                return render(request, 'register/register.html', context)
    return render(request, 'register/register.html')



def user_logout(request):
    logout(request)
    return redirect('main:home')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # 세션에 로그인 처리 (Django의 세션 인증)
            login(request, user)

            # JWT 토큰 발급 (API용)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return redirect('main:home')
        else:
            return render(request, 'login/login.html', {'error': '로그인 실패'})
    return render(request, 'login/login.html')


# 마이페이지 설정
@login_required
def my_page(request):
    return render(request, 'mypage/myPage.html', {'user':request.user})

# 랜덤 문자열 생성 함수
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_decoded_header(header_value):
    decoded_parts = decode_header(header_value)
    header_text = ""
    for part, encoding in decoded_parts:
        # 인코딩이 None이거나 'unknown-8bit'인 경우 대체 인코딩 사용
        if encoding is None or (isinstance(encoding, str) and encoding.lower() == 'unknown-8bit'):
            encoding = 'utf-8'
        if isinstance(part, bytes):
            try:
                header_text += part.decode(encoding, errors="replace")
            except Exception as e:
                # 만약 여전히 에러가 난다면, 기본 utf-8로 디코딩
                header_text += part.decode('utf-8', errors="replace")
        else:
            header_text += part
    return header_text

def phone_verification(request):
    # 새로 인증 요청 시마다 새로운 랜덤 문자열을 생성
    random_str = generate_random_string(10)
    
    # DB에 인증 요청 기록 저장
    PhoneVerification.objects.create(
        user=request.user if request.user.is_authenticated else None,
        random_string=random_str
    )
    
    # 세션에도 저장 (추후 인증 검증 시 사용)
    request.session['phone_verification_code'] = random_str
    
    # SMS 전송 링크 생성  
    # (참고: 통신사별 SMS 전송용 이메일 주소가 달라질 수 있음)
    sms_link = f"sms:piro.urabi@gmail.com?body={random_str}"
    
    # QR 코드 생성 
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(sms_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    context = {
        'random_str': random_str,
        'sms_link': sms_link,
        'qr_code_base64': qr_code_base64,
    }
    return render(request, 'register/phone_verification.html', context)


def search_email_for_code(mail, random_str):
    # 먼저 INBOX에서 검색
    result, data = mail.search(None, f'(BODY "{random_str}")')
    if data[0]:
        return data[0].split()
    # 만약 INBOX에 없으면, 스팸 폴더도 검색
    mail.select('[Gmail]/Spam')  # Gmail의 스팸 폴더 이름은 보통 "[Gmail]/Spam"입니다.
    result, data = mail.search(None, f'(BODY "{random_str}")')
    if data[0]:
        return data[0].split()
    return None

def verify_phone_status(request):
    random_str = request.session.get('phone_verification_code')
    if not random_str:
        return JsonResponse({'result': 'unauthorized'})
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(settings.IMAP_USER, settings.IMAP_PASSWORD)
        mail.select('inbox')
        result, data = mail.search(None, f'(BODY "{random_str}")')
        if not data[0]:
            return JsonResponse({'result': 'wait'})
        
        email_ids = data[0].split()
        result, msg_data = mail.fetch(email_ids[-1], '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # 디코딩된 From 헤더 사용
        raw_from_header = msg.get('From', '')
        from_header = get_decoded_header(raw_from_header)
        print("DECODED FROM HEADER:", from_header)
        
        # 전화번호 추출: 정규식을 사용하여 0으로 시작하는 10~11자리 숫자 추출
        match = re.search(r'(0\d{9,10})', from_header)
        if match:
            phone_number = match.group(1)
            verification_obj = PhoneVerification.objects.filter(random_string=random_str).latest('created_at')
            verification_obj.verified = True
            verification_obj.phone_number = phone_number
            verification_obj.save()
            if request.user.is_authenticated:
                request.user.user_phone = phone_number
                request.user.save()
            return JsonResponse({'result': 'verified', 'phone_number': phone_number})
        return JsonResponse({'result': 'wait'})
    except Exception as e:
        print("Verification error:", e)
        return JsonResponse({'result': 'error'})


# 정보 수정
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        birth_year = request.POST.get("birth_year")
        birth_month = request.POST.get("birth_month")
        birth_day = request.POST.get("birth_day")

        if 'profile_image' in request.FILES:
            print("✅ 파일 업로드 감지됨!")
        else:
            print("⚠️ 파일 업로드가 안 됨")


        if birth_year and birth_month and birth_day:
            request.user.birth = f"{birth_year}-{birth_month}-{birth_day}"  # YYYY-MM-DD 형식으로 변환하여 저장

        if form.is_valid():
            form.save()
            request.user.save() 
            return redirect('users:my_page')
        else:
            print(form.errors)  # 디버깅용 출력

    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'mypage/editProfile.html', {'form': form, 'user': request.user})

# 채팅 : 토큰 발급
@login_required
def get_token_for_logged_in_user(request):
    refresh = RefreshToken.for_user(request.user)
    return JsonResponse({
        "access": str(refresh.access_token)
    })

    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def some_protected_route(request):
    return Response({'message': 'This is a protected route!'}, status=status.HTTP_200_OK)

@login_required
def my_trip(request, pk): # 여행 계획 작성, 여행일정 id
    this_schedule = get_object_or_404(TravelSchedule, schedule_id=pk)
    if request.method == 'POST':
        form = TravelPlanForm(request.POST)

        if form.is_valid():
            travel_plan = form.save(commit=False)
            travel_plan.created_by = request.user
            this_schedule = TravelSchedule.objects.get(schedule_id=pk)
            travel_plan.schedule = this_schedule
            travel_plan.markers = request.POST.get('markers', '')  # 기본값 ''
            travel_plan.polyline = request.POST.get('polyline', '')

            travel_plan.save()  

            return render(request, 'mypage/plan_detail.html', {
                'travel_plan': travel_plan,
            })
    else:
        form = TravelPlanForm()

    return render(request, 'mypage/myTrip.html', {
        'form': form,
        'this_schedule': this_schedule,
    })

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, id=pk)
    current_user = request.user  # 현재 로그인한 사용자
    
    # 여행 계획 및 동행 관련 쿼리 작성 
    user_plans = TravelPlan.objects.filter(created_by=user)
    user_accompany = TravelGroup.objects.filter(created_by=user)
    accompany_count = user_accompany.count()
    
    # 숙소 리뷰 쿼리 수정 - is_parent=False인 리뷰만 가져오기
    accommodation_reviews = AccommodationReview.objects.filter(
        user=user,
        is_parent=False
    ).order_by('-created_at')
    
    review_count = accommodation_reviews.count()
    
    # 처음 5개만 보이도록 슬라이싱 initial_reviews = accommodation_reviews[:5]
    
    #나눔마켓
    mkt_self_items = Market.objects.filter(user=user)
    mkt_self_count = mkt_self_items.count()

    # 사용자가 등록한 번개 모임 가져오기
    flash_meetings = Flash.objects.filter(created_by=user).order_by("-date_time")
    flash_count = flash_meetings.count()

    # 동행 태그 처리
    for accompany in user_accompany:
        accompany.tags = accompany.tags.split(',') if accompany.tags else []
    
    return render(request, 'mypage/userDetail.html', {
        'user': user,
        'current_user': current_user,
        'plans': user_plans,
        'accompanies': user_accompany,
        'accompany_count': accompany_count,
        "flash_meetings": flash_meetings,
        "flash_count": flash_count,
        'accommodation_reviews': accommodation_reviews,  # 숙소 리뷰 데이터 추가 
        'review_count': review_count,  # 리뷰 개수 추가
        'has_more': review_count > 5,  # 더보기 버튼 표시 여부
        'mkt_self_items' :mkt_self_items, #마켓 작성자 게시글
        'mkt_self_count' :mkt_self_count
    })
    
    
# # def load_more_reviews(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     offset = int(request.GET.get('offset', 5))
#     limit = 5  # 한 번에 추가로 보여줄 리뷰 수
    
#     # is_parent=False인 리뷰만 가져오기
#     accommodation_reviews = AccommodationReview.objects.filter(
#         user=user,
#         is_parent=False
#     ).order_by('-created_at')[offset:offset+limit]
    
#     # 더 보여줄 리뷰가 있는지 확인
#     total_reviews = AccommodationReview.objects.filter(
#         user=user,
#         is_parent=False
#     ).count()
    
#     has_more = total_reviews > (offset + limit)
    
#     context = {
#         'accommodation_reviews': accommodation_reviews
#     }
    
#     html = render_to_string('mypage/_review_cards.html', context)
    
#     return JsonResponse({
#         'html': html,
#         'has_more': has_more
#     })

@login_required
def plan_detail(request, pk):
    travel_plan = TravelPlan.objects.get(plan_id=pk)
    return render(request, 'mypage/plan_detail.html', {
        'travel_plan': travel_plan,
    })

def delete_trip(request, pk):
    travel_plan = TravelPlan.objects.get(plan_id=pk)
    travel_plan.delete()
    return redirect('users:schedule_detail', pk=travel_plan.schedule.schedule_id)

def update_trip(request, pk):
    travel_plan = TravelPlan.objects.get(plan_id=pk)
    if request.method == 'POST':
        form = TravelPlanForm(request.POST, instance=travel_plan)
        if form.is_valid():
            travel_plan = form.save(commit=False)
            travel_plan.created_by = request.user
            travel_plan.markers = request.POST.get('markers', '')  # 기본값 ''
            travel_plan.polyline = request.POST.get('polyline', '')
            travel_plan.save()
            return redirect('users:plan_detail', pk=travel_plan.plan_id)
    else:
        form = TravelPlanForm(instance=travel_plan)
    return render(request, 'mypage/myTrip.html', {
        'form': form,
    })

def user_list(request):
    user = get_object_or_404(User, id=request.user.id)
    user_plans = TravelSchedule.objects.filter(user=user)
    user_plan_count = user_plans.count()
    user_accompanies = TravelParticipants.objects.filter(user=user)
    user_accompany_count = user_accompanies.count()
    for accompany in user_accompanies:
        travel_group = TravelGroup.objects.get(travel_id=accompany.travel_id)
        accompany.tags = travel_group.tags.split(',') if travel_group.tags else []
    user_request = AccompanyRequest.objects.filter(user=user)
    user_request_count = user_request.count()

    return render(request, 'mypage/planlist.html', {
        'plans': user_plans,
        'plan_count': user_plan_count,
        'accompanies': user_accompanies,
        'accompany_count': user_accompany_count+user_request_count,
        'ac_requests': user_request,
    })

def zzim_list(request):
    user = get_object_or_404(User, id=request.user.id)

    ac_zzims = Accompany_Zzim.objects.filter(user=user)
    ac_zzim_items = [zzim.item for zzim in ac_zzims]
    ac_zzim_count = ac_zzims.count()

    # 사용자가 찜한 번개 목록 가져오기
    flash_zzims = FlashZzim.objects.filter(user=user).select_related("flash")
    flash_zzim_items = [zzim.flash for zzim in flash_zzims]
    flash_zzim_count = flash_zzims.count()
    
    mkt_zzims = MarketZzim.objects.filter(user=user)
    mkt_zzims_items = [zzim.market for zzim in mkt_zzims]
    mkt_zzim_count = mkt_zzims.count()

    return render(request, 'mypage/zzim_list.html', {
        'ac_zzims': ac_zzim_items,
        'ac_zzim_count': ac_zzim_count,
        'flash_zzims': flash_zzim_items,
        'flash_zzim_count': flash_zzim_count,
        'mkt_zzims':mkt_zzims_items,
        'mkt_zzim_count' : mkt_zzim_count,
    })

def schedule_create(request):
    if request.method == 'POST':
        schedule_name = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        new_schedule = TravelSchedule.objects.create(name=schedule_name, user=request.user, start_date=start_date, end_date=end_date)
        return redirect('users:schedule_detail', pk=new_schedule.schedule_id)

def schedule_detail(request, pk):
    schedule = TravelSchedule.objects.get(schedule_id=pk)
    plans = TravelPlan.objects.filter(schedule=schedule)
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        schedule.photo = photo
        schedule.save()
    return render(request, 'mypage/schedule_detail.html', {
        'schedule': schedule,
        'plans': plans,
    })

def delete_schedule(request):
    schedule_id = request.GET.get('schedule_id')
    schedule = get_object_or_404(TravelSchedule, pk=schedule_id)
    schedule.delete()
    return redirect('users:user_list')