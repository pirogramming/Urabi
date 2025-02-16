# ✈️ Urabi
> 사용자가 원하는대로 함께하는 동행서비스! Urabi  <br>
>  Team 민설아 유승인 최민석 김재원 이시은

| 민설아 (팀장)                                  | 유승인                               | 최민석                                 | 김재원                                           | 이시은                                  |
| ---------------------------------------- | ------------------------------------ | -------------------------------------- | ------------------------------------------------ | -------------------------------------- |
| FE, BE                                       |  FE, BE                                    |  FE, BE                                     |  FE, BE                                              |  FE, BE                                 |
|  [@axoesnxm](https://github.com/axoesnxm) | [@seung-in-Yoo](https://github.com/seung-in-Yoo) | [@03minseok](https://github.com/03minseok) | [@dhrkawk](https://github.com/dhrkawk) | [@iseun15](https://github.com/iseun15) |

#### Urabi 노션 페이지 바로가기: [Urabi_notion](https://www.notion.so/18673a6fb5e480f6987fe294ed5c6baf)
#### Urabi 피그마 페이지 바로가기: [Urabi_figma](https://www.figma.com/files/team/1465277384609902795/all-projects?fuid=1387363449201856791)
<br>


# 🐾 UrabiTeam Name | 팀원: [팀원 이름 작성]

## 🚀 Urabi: 유럽 여행 동행 & 커뮤니티 플랫폼

'함께 떠나는 유럽 여행, Urabi에서 동행을 찾아보세요!'

🔗 배포 링크: [배포 링크 추가]
🎬 프로모션 영상: [영상 링크 추가]

## 📂 Content

- [🔎 기술 스택](#-기술-스택)
- [🔎 서비스 기획 배경](#-서비스-기획-배경)
- [🔎 서비스 매커니즘](#-서비스-매커니즘)
- [🔎 주요 기능](#-주요-기능)
- [🔎 상세 기능](#-상세-기능)
- [🔎 와이어프레임](#-와이어프레임)
- [🔎 데이터베이스 구조](#-데이터베이스-구조)
- [🔎 API 명세](#-api-명세)
- [🔎 개발 과정](#-개발-과정)
- [🔎 팀 소개](#-팀-소개)

## 🛠️ 기술 스택

### 프론트엔드 (FrontEnd)

- React
- HTML5
- CSS3
- JavaScript
- 스타일링: Tailwind CSS
- 상태 관리: Redux
- 라우팅: React Router
- HTTP 클라이언트: Axios

### 백엔드 (BackEnd)

- Django
- Django REST Framework
- Redis (캐싱 및 세션 관리)

### 데이터베이스 관리 (Database Management)

- PostgreSQL (AWS RDS)

### 서버 및 배포 (Server & Deployment)

- AWS EC2
- Nginx
- Gunicorn

### 협업 툴 (Collaboration Tools)

- Notion
- Slack
- Git
- GitHub
- Figma

## 🌍 서비스 기획 배경

여행은 함께할 때 더 즐겁습니다. 하지만 막상 유럽 여행을 계획할 때 동행을 찾기가 쉽지 않죠. Urabi는 지도 기반의 여행 동행 모집을 중심으로, 다양한 여행자들이 모여 정보를 공유하고, 함께할 수 있도록 돕는 커뮤니티 플랫폼입니다.

특히 유럽에서는 **즉흥적인 여행 계획(번개 여행)**이 흔하기 때문에, 이를 반영한 "여행번개" 기능을 제공하여 자유로운 만남과 경험을 가능하게 합니다. 또한, 숙소 후기를 공유하고, 여행 중 필요 없는 물품을 나눌 수 있는 커뮤니티 마켓 기능도 포함하여 여행자 간의 편의를 극대화했습니다.

Urabi를 통해 함께 여행할 동행을 찾고, 실시간으로 소통하며, 더 안전하고 즐거운 여행을 떠나보세요!

## 🔗 서비스 매커니즘 & 사용 가이드

### 1️⃣ 여행 동행 찾기

- 지도 기반으로 여행 동행을 찾고 모집할 수 있습니다.
- 모집글 작성 시 여행 일정, 지역, 선호 스타일 등을 설정할 수 있습니다.
- 관심 있는 모집글에 댓글을 남기거나 실시간 채팅을 통해 동행을 결정할 수 있습니다.

### 2️⃣ 여행 번개 (즉흥 여행 모임)

- 갑자기 생긴 일정에도 유럽에서 동행을 찾을 수 있도록 실시간 번개 기능을 제공합니다.
- 위치 기반으로 가까운 지역에서 여행 번개가 열리면 알림을 받을 수 있습니다.

### 3️⃣ 숙소 후기 공유

- 여행 중 머문 숙소의 리뷰를 남기고, 다른 사용자의 리뷰를 참고하여 숙소를 선택할 수 있습니다.

### 4️⃣ 나눔 마켓

- 여행 중 더 이상 필요 없는 물품을 나누거나 판매할 수 있습니다.
- 다른 여행자들과 여행 가이드북, 교통 패스 등의 물품을 거래할 수 있습니다.

## ✨ 주요 기능

### 🗺 지도 기반 동행 모집

- 여행 일정과 지역을 설정하여 동행을 찾을 수 있습니다.
- 실시간 채팅을 통해 동행과 소통할 수 있습니다.

### ⚡ 즉흥 여행 번개 (여행번개 기능)

- 급하게 동행이 필요한 경우, 근처의 여행자들과 빠르게 연결될 수 있습니다.

### 🏠 숙소 후기 공유

- 여행자들이 머물렀던 숙소에 대한 리뷰를 남길 수 있습니다.
- 필터링 기능을 통해 가격대, 위치, 청결도 등을 비교할 수 있습니다.

### 🎁 나눔 마켓

- 여행 중 불필요해진 물품을 다른 여행자에게 나눠줄 수 있습니다.
- 안전한 거래 시스템을 지원하여 신뢰할 수 있는 환경을 제공합니다.

## 📌 상세 기능

### 💡 카테고리별 기능

#### 🏝 여행 동행

- 사용자의 현재 위치를 기반으로 근처에서 동행을 찾을 수 있음
- 필터를 적용하여 비슷한 여행 스타일을 가진 동행을 검색 가능
- 동행 모집 글 작성 및 수정 기능
- 댓글 및 실시간 채팅 기능 제공

#### 🔥 여행 번개

- 즉흥적인 여행을 위한 번개 모집 기능
- 사용자의 GPS를 활용하여 가까운 여행자들에게 알림 발송
- 참여 가능 여부를 실시간으로 확인할 수 있음

#### 🏡 숙소 후기

- 여행자들이 머문 숙소의 정보를 공유
- 청결도, 가격, 위치 등의 정보를 포함한 리뷰 작성 가능
- 검색 및 필터링 기능을 통해 원하는 숙소 정보 검색 가능

#### 🎁 나눔 마켓

- 여행 중 필요 없어진 물품을 여행자들끼리 거래 가능
- 사용자가 올린 물품에 대해 실시간 문의 및 채팅 가능

## 📊 데이터베이스 구조
# Accommodation Reviews Database Schema

## AccommodationReview Table

| Column Name      | Data Type        | Constraints                                |
|-----------------|----------------|--------------------------------------------|
| review_id       | AutoField       | Primary Key                               |
| user_id         | ForeignKey(User) | On Delete: CASCADE                        |
| city           | CharField(50)   | Not Null                                  |
| accommodation_name | CharField(100) | Not Null                                  |
| category        | CharField(50)   | Not Null                                  |
| rating         | Decimal(2,1)    | Range: 1.0 ~ 5.0                          |
| content        | TextField       | Nullable                                  |
| created_at     | DateTimeField   | Auto Now Add                              |
| updated_at     | DateTimeField   | Auto Now                                  |
| photo          | ImageField      | Upload To: `accommodation_reviews/`, Nullable |
| is_parent      | BooleanField    | Default: True                             |
| latitude       | FloatField      | Nullable                                  |
| longitude      | FloatField      | Nullable                                  |
| location_view  | ImageField      | Upload To: `accommodation_views/`, Nullable |
| favorites      | ManyToManyField(User) | Related Name: `favorite_reviews`, Nullable |
| likes          | ManyToManyField(User) | Related Name: `liked_reviews`, Nullable |

---

## ReviewComment Table

| Column Name      | Data Type        | Constraints                      |
|-----------------|----------------|----------------------------------|
| comment_id     | BigAutoField    | Primary Key                     |
| review_id      | ForeignKey(AccommodationReview) | On Delete: CASCADE |
| user_id        | ForeignKey(User) | On Delete: CASCADE              |
| content        | TextField       | Not Null                        |
| created_at     | DateTimeField   | Auto Now Add                    |

# Travel Group Database Schema

## TravelGroup Table

| Column Name    | Data Type       | Constraints                                  |
|---------------|----------------|----------------------------------------------|
| travel_id     | BigAutoField    | Primary Key                                 |
| title         | CharField(100)  | Not Null                                    |
| city          | CharField(50)   | Not Null                                    |
| explanation   | TextField       | Not Null                                    |
| start_date    | DateField       | Not Null                                    |
| end_date      | DateField       | Not Null                                    |
| created_by    | ForeignKey(User) | On Delete: CASCADE, Related Name: `created_travels` |
| created_at    | DateTimeField   | Auto Now Add                                |
| updated_at    | DateTimeField   | Auto Now                                    |
| now_member    | IntegerField    | Default: 1                                  |
| max_member    | IntegerField    | Not Null                                    |
| tags          | TextField       | Nullable                                   |
| photo         | ImageField      | Upload To: `static/travel_photos/`, Nullable |
| gender        | CharField(10)   | Choices: '전체', '남성만', '여성만', Default: '상관없음' |
| min_age       | IntegerField    | Nullable                                   |
| max_age       | IntegerField    | Nullable                                   |
| markers       | JSONField       | Nullable                                   |
| polyline      | JSONField       | Nullable                                   |
| this_plan_id  | IntegerField    | Nullable                                   |
| call_schedule | BooleanField    | Default: False                             |

---

## TravelParticipants Table

| Column Name | Data Type        | Constraints                                  |
|-------------|----------------|----------------------------------------------|
| id          | BigAutoField    | Primary Key                                 |
| travel_id   | ForeignKey(TravelGroup) | On Delete: CASCADE, Related Name: `travel_participants` |
| user_id     | ForeignKey(User) | On Delete: CASCADE, Related Name: `user_participations` |

---

## Accompany_Zzim Table

| Column Name | Data Type        | Constraints                                  |
|-------------|----------------|----------------------------------------------|
| user_id     | ForeignKey(User) | On Delete: CASCADE, Related Name: `zzims`   |
| item_id     | ForeignKey(TravelGroup) | On Delete: CASCADE, Related Name: `zzim_items` |

**Unique Constraint:** (`user_id`, `item_id`)

---

## AccompanyRequest Table

| Column Name | Data Type        | Constraints                                  |
|-------------|----------------|----------------------------------------------|
| travel_id   | ForeignKey(TravelGroup) | On Delete: CASCADE, Related Name: `travel_requests` |
| user_id     | ForeignKey(User) | On Delete: CASCADE, Related Name: `user_requests` |

---

# Chat System Database Schema

## ChatRoom Table

| Column Name        | Data Type        | Constraints                                      |
|--------------------|----------------|--------------------------------------------------|
| id                | AutoField       | Primary Key                                     |
| user1_id          | ForeignKey(User) | On Delete: CASCADE, Related Name: `user1_chatrooms` |
| user2_id          | ForeignKey(User) | On Delete: CASCADE, Related Name: `user2_chatrooms` |
| created_at        | DateTimeField   | Auto Now Add                                    |
| last_message_time | DateTimeField   | Nullable                                       |
| deleted_at_user1  | DateTimeField   | Nullable                                       |
| deleted_at_user2  | DateTimeField   | Nullable                                       |

**Unique Constraint:** (`user1_id`, `user2_id`)  
**Ordering:** `-last_message_time`, `-created_at`

---

## Message Table

| Column Name | Data Type        | Constraints                                  |
|-------------|----------------|----------------------------------------------|
| id          | AutoField       | Primary Key                                 |
| room_id     | ForeignKey(ChatRoom) | On Delete: CASCADE, Related Name: `messages` |
| sender_id   | ForeignKey(User) | On Delete: CASCADE                         |
| content     | TextField       | Not Null                                    |
| timestamp   | DateTimeField   | Auto Now Add                                |
| read_by     | ManyToManyField(User) | Related Name: `read_messages`, Nullable    |
| deleted_by  | ManyToManyField(User) | Related Name: `deleted_messages`, Nullable |

---

이 스키마는 `Markdown`으로 정리된 데이터베이스 모델을 나타냅니다.  
데이터베이스 테이블과 컬럼의 관계를 한눈에 보기 쉽도록 정리하였으며, GitHub, Notion 등에 활용하기 좋습니다. 😊

# 📊 데이터베이스 구조

## Flash 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| meeting_id    | BigAutoField (PK)          | 모임 ID                          |
| title         | CharField (max_length=100) | 모임 제목                        |
| city          | CharField (max_length=50)  | 도시                             |
| latitude      | DecimalField (max_digits=10, decimal_places=6) | 위도 |
| longitude     | DecimalField (max_digits=10, decimal_places=6) | 경도 |
| date_time     | DateTimeField              | 모임 날짜 및 시간                |
| max_people    | IntegerField               | 최대 인원                        |
| explanation   | TextField                  | 모임 설명                        |
| tags          | TextField (blank=True)     | 태그 (쉼표로 구분된 문자열)      |
| created_by    | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 생성자 |
| created_at    | DateTimeField (auto_now_add=True) | 생성 일시 |
| updated_at    | DateTimeField (auto_now=True) | 수정 일시 |
| now_member    | IntegerField (default=0)   | 현재 인원                        |

## FlashParticipants 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| flash         | ForeignKey (Flash, on_delete=CASCADE, related_name="flash_participants") | 모임 |
| user          | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 사용자 |
| joined_at     | DateTimeField (auto_now_add=True) | 참가 시간 |

**Meta Class**
- unique_together = ("flash", "user")  # 중복 참가 방지

## FlashRequest 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| flash         | ForeignKey (Flash, on_delete=CASCADE, related_name="flash_requests") | 모임 |
| user          | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 사용자 |
| requested_at  | DateTimeField (auto_now_add=True) | 참가 요청 시간 |

**Meta Class**
- unique_together = ("flash", "user")  # 중복 요청 방지

## FlashZzim 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| user          | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 사용자 |
| flash         | ForeignKey (Flash, on_delete=CASCADE) | 모임 |
| created_at    | DateTimeField (auto_now_add=True) | 찜한 시간 |

**Meta Class**
- unique_together = ("user", "flash")  # 중복 찜 방지

## Market 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| item_id       | BigAutoField (PK)          | 물품 ID                          |
| user          | ForeignKey (User, verbose_name=("작성자"), on_delete=CASCADE) | 작성자 |
| trade_type    | CharField (max_length=10, choices=TRADE_TYPE_CHOICES) | 거래 유형 |
| city          | CharField (max_length=50)  | 도시                             |
| title         | CharField (max_length=100) | 제목                             |
| category      | CharField (max_length=10, choices=CATEGORY_CHOICES) | 카테고리 |
| explanation   | TextField                  | 설명                             |
| price         | DecimalField (max_digits=10, decimal_places=2) | 가격 |
| currency_unit | CharField (choices=CURRENCY_UNIT, max_length=10) | 통화 단위 |
| status        | CharField (max_length=20, default='거래 가능', choices=TRADE_STATUS_CHOICES) | 거래 상태 |
| created_at    | DateField (auto_now_add=True) | 생성 일시 |
| updated_at    | DateField (auto_now=True)  | 수정 일시 |
| photo         | ImageField ('마켓_이미지', blank=True, upload_to='market/%Y%m%d') | 사진 |

## MarketZzim 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| user          | ForeignKey (User, on_delete=CASCADE) | 사용자 |
| market        | ForeignKey (Market, on_delete=CASCADE) | 마켓 |

**Meta Class**
- unique_together = ("user", "market")  # 중복 찜 방지
```` ▋

# 📊 데이터베이스 구조

## User 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| id            | AutoField (PK)             | 사용자 ID                        |
| email         | EmailField (unique=True)   | 이메일                           |
| username      | CharField (max_length=150, blank=True, null=True) | 사용자명                         |
| user_age      | IntegerField (null=True, blank=True) | 나이                             |
| user_gender   | CharField (max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True, default=None) | 성별 |
| user_phone    | CharField (max_length=20, null=True, blank=True, default=None) | 전화번호                         |
| nickname      | CharField (max_length=10, null=True) | 닉네임                           |
| birth         | DateField (null=True, blank=True) | 생년월일                         |
| social_id     | CharField (max_length=100, null=True, blank=True) | 소셜 ID                          |
| profile_image | ImageField (upload_to='profile_images', null=True, blank=True, default='profile_images/default-profile.png') | 프로필 이미지 |
| trust_score   | IntegerField (default=36.5) | 신뢰 점수                        |
| created_at    | DateTimeField (auto_now_add=True) | 생성 일시                        |
| is_active     | BooleanField (default=True) | 활성 상태                        |
| is_staff      | BooleanField (default=False) | 스태프 여부                      |

## TravelSchedule 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| schedule_id   | BigAutoField (PK)          | 일정 ID                          |
| name          | CharField (max_length=100) | 일정 이름                        |
| user          | ForeignKey (User, on_delete=CASCADE, related_name='travel_schedules') | 사용자 |
| start_date    | DateField                  | 시작 날짜                        |
| end_date      | DateField                  | 종료 날짜                        |
| photo         | ImageField (upload_to='schedule_images', null=True, blank=True) | 사진 |
| is_public     | BooleanField (default=False) | 공개 여부                       |
| created_at    | DateTimeField (auto_now_add=True) | 생성 일시                        |
| updated_at    | DateTimeField (auto_now=True) | 수정 일시                        |

## TravelPlan 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| plan_id       | BigAutoField (PK)          | 계획 ID                          |
| schedule      | ForeignKey (TravelSchedule, on_delete=CASCADE, related_name='plans') | 일정 |
| explanation   | TextField                  | 설명                             |
| start_date    | DateField                  | 시작 날짜                        |
| end_date      | DateField                  | 종료 날짜                        |
| markers       | JSONField (null=True, blank=True) | 마커                              |
| polyline      | JSONField (null=True, blank=True) | 폴리라인                          |
| created_by    | ForeignKey (User, on_delete=CASCADE, related_name='travel_plans') | 생성자 |
| created_at    | DateTimeField (auto_now_add=True) | 생성 일시                        |
| updated_at    | DateTimeField (auto_now=True) | 수정 일시                        |

## PhoneVerification 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| id            | AutoField (PK)             | 인증 ID                          |
| user          | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True, blank=True) | 사용자 |
| random_string | CharField (max_length=255, unique=True) | 랜덤 문자열                      |
| created_at    | DateTimeField (auto_now_add=True) | 생성 일시                        |
| verified      | BooleanField (default=False) | 인증 여부                        |
| phone_number  | CharField (max_length=20, blank=True, null=True) | 전화번호                         |

## Flash 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| meeting_id    | BigAutoField (PK)          | 모임 ID                          |
| title         | CharField (max_length=100) | 모임 제목                        |
| city          | CharField (max_length=50)  | 도시                             |
| latitude      | DecimalField (max_digits=10, decimal_places=6) | 위도 |
| longitude     | DecimalField (max_digits=10, decimal_places=6) | 경도 |
| date_time     | DateTimeField              | 모임 날짜 및 시간                |
| max_people    | IntegerField               | 최대 인원                        |
| explanation   | TextField                  | 모임 설명                        |
| tags          | TextField (blank=True)     | 태그 (쉼표로 구분된 문자열)      |
| created_by    | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 생성자 |
| created_at    | DateTimeField (auto_now_add=True) | 생성 일시                        |
| updated_at    | DateTimeField (auto_now=True) | 수정 일시                        |
| now_member    | IntegerField (default=0)   | 현재 인원                        |

## FlashParticipants 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| flash         | ForeignKey (Flash, on_delete=CASCADE, related_name="flash_participants") | 모임 |
| user          | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 사용자 |
| joined_at     | DateTimeField (auto_now_add=True) | 참가 시간 |

**Meta Class**
- unique_together = ("flash", "user")  # 중복 참가 방지

## FlashRequest 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| flash         | ForeignKey (Flash, on_delete=CASCADE, related_name="flash_requests") | 모임 |
| user          | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 사용자 |
| requested_at  | DateTimeField (auto_now_add=True) | 참가 요청 시간 |

**Meta Class**
- unique_together = ("flash", "user")  # 중복 요청 방지

## FlashZzim 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| user          | ForeignKey (settings.AUTH_USER_MODEL, on_delete=CASCADE) | 사용자 |
| flash         | ForeignKey (Flash, on_delete=CASCADE) | 모임 |
| created_at    | DateTimeField (auto_now_add=True) | 찜한 시간 |

**Meta Class**
- unique_together = ("user", "flash")  # 중복 찜 방지

## Market 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| item_id       | BigAutoField (PK)          | 물품 ID                          |
| user          | ForeignKey (User, verbose_name=("작성자"), on_delete=CASCADE) | 작성자 |
| trade_type    | CharField (max_length=10, choices=TRADE_TYPE_CHOICES) | 거래 유형 |
| city          | CharField (max_length=50)  | 도시                             |
| title         | CharField (max_length=100) | 제목                             |
| category      | CharField (max_length=10, choices=CATEGORY_CHOICES) | 카테고리 |
| explanation   | TextField                  | 설명                             |
| price         | DecimalField (max_digits=10, decimal_places=2) | 가격 |
| currency_unit | CharField (choices=CURRENCY_UNIT, max_length=10) | 통화 단위 |
| status        | CharField (max_length=20, default='거래 가능', choices=TRADE_STATUS_CHOICES) | 거래 상태 |
| created_at    | DateField (auto_now_add=True) | 생성 일시                        |
| updated_at    | DateField (auto_now=True)  | 수정 일시                        |
| photo         | ImageField ('마켓_이미지', blank=True, upload_to='market/%Y%m%d') | 사진 |

## MarketZzim 테이블
| 필드명        | 데이터 타입                | 설명                             |
|---------------|----------------------------|----------------------------------|
| user          | ForeignKey (User, on_delete=CASCADE) | 사용자 |
| market        | ForeignKey (Market, on_delete=CASCADE) | 마켓 |

**Meta Class**
- unique_together = ("user", "market")  # 중복 찜 방지
```` ▋


## 📡 API 명세

- 회원가입 및 로그인 API
- 여행 동행 모집 및 검색 API
- 여행 번개 모집 및 참여 API
- 숙소 후기 작성 및 조회 API
- 나눔 마켓 거래 API
- 실시간 채팅 API

## 📅 개발 과정

- 1주차: 기획 및 와이어프레임 제작
- 2주차: 데이터베이스 설계 및 API 개발
- 3주차: 프론트엔드 개발 및 백엔드 연동
- 4주차: 테스트 및 배포

## 👥 팀 소개

- [팀원 1] - PM & 기획
- [팀원 2] - 프론트엔드 개발
- [팀원 3] - 백엔드 개발
- [팀원 4] - UI/UX 디자인

Urabi와 함께 즐거운 유럽 여행을 계획해보세요! 🚀
