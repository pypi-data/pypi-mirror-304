# 샘플 이미지
다음은 해당 패키지를 통해 티스토리 블로그를 이사하여 운영 중인 사이트의 샘플 이미지입니다.

샘플 사이트 : <https://dstory.seolpyo.com/>

티스토리 블로그 : <https://white-seolpyo.tistory.com/>

![이미지 1](https://github.com/white-seolpyo/seolpyo-dstory/blob/main/img1.png?raw=true)

![이미지 2](https://github.com/white-seolpyo/seolpyo-dstory/blob/main/img2.png?raw=true)


# 프로젝트 문의 / 제안
프로젝트와 관련한 내용은 [설표의장고 게시판](https://django.seolpyo.com/board/)에 이야기해주시면 감사합니다.

# 프로젝트 설명
패키지명은 Django + Tistory를 합친 DSTORY(디스토리)로 명명했습니다.

## 프로젝트의 목적
백업파일을 이용하여 티스토리 블로그에 작성한 글들을 Django로 이전하여 운영할 수 있도록 합니다.

## 프로젝트 특징
- 티스토리와 동일한 url 구조(숫자 주소 + 문자 주소 + rss + 사이트맵)를 사용합니다.
- 태그, 카테고리, 공지사항, 서식, 페이지 정보를 가져올 수 있으며, 티스토리 블로그 로그인 정보를 이용해 임의로 설정한 문자 주소, 보호 글의 비밀번호 등의 정보도 가져올 수 있습니다.
- 애드센스 코드 적용과 ads.txt 페이지를 손쉽게 할 수 있습니다.
- Google Analytics 태그 추가를 쉽게 할 수 있습니다.
- Google Tag Manager 태그 추가도 쉽게 할 수 있습니다.


# 사용방법
다음과 같이 ">>"으로 표현되는 명령어는 cmd.exe에 입력하는 명령어입니다.
cmd.exe는 윈도우키 + R => cmd 를 실행하면 사용할 수 있습니다.
```
>> cmd.exe에 입력하는 명령어입니다.
```
## 패키지 설치
디스토리 패키지를 설치합니다.

tqdm, requests, bs4(BeautifulSoup), selenium, django, django-summenote 패키지가 함께 설치됩니다.

컴퓨터에 파이썬이 설치되지 않았다면 다음 글을 확인해주세요.

[파이썬 설치방법](https://django.seolpyo.com/entry/17/)
```
>> pip install seolpyo-dstory
```

## 장고 프로젝트 생성방법
C:/ 경로로 이동한 다음(리눅스인 경우 ~/), mysite라는 폴더를 생성하고, 폴더 안에 장고 프로젝트를 생성합니다.
```
>> cd C:/
>> mkdir mysite
>> cd mysite
>> django-admin startproject config .
```


## 기초 설정하기
1. mysite > config 에 settings 폴더를 만든 다음, settings.py를 settings 폴더로 이동시킵니다.
1. mysite > config > settigns 폴더에 ```__init__.py``` 를 만들고, 다음과 같이 작성합니다.

seolpyo_dsotry.settings 파일은 장고의 기초설정을 빠르게 하기 위해 작성된 파일입니다.
```
# config/settings/__init__.py
from .settings import *
from seolpyo_dstory.settings import *

BASE_DIR = BASE_DIR.parent
for i in apps:
  if i not in INSTALLED_APPS: INSTALLED_APPS.append(i)

TEMPLATES[0]['OPTIONS']['context_processors'].append(processor)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 애드센스 코드
DSTORY_CONTEXT['adsense'] = '' # ca-pub-123456789 => '123456789'
# 구글 애널리틱스 코드
DSTORY_CONTEXT['ga'] = '' # G-A1B2C3D4 => 'A1B2C3D4'
# 구글 태그매니저 코드
DSTORY_CONTEXT['gtm'] = '' # GTM-X1Y2Z3 => 'X1Y2Z3'
# 네이버 웹마스터도구 소유권 인증
DSTORY_NAVER = '' # naverA1B2C3D4E5F6G7H8I9.html => 'A1B2C3D4E5F6G7H8I9'
```

※ 별도의 이용자 모델이 있는 경우, AUTH_USER_MODEL 선언해주어야 합니다. 위 설정을 사용하면 'seolpyo_dstory.User'를 사용하게 됩니다.


## urls.py 변경하기

mysite > config > urls.py를 열어 내용을 다음과 같이 변경합니다.
```
# config/urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('seolpyo_dstory.urls')),
]

if not settings.DEBUG:
    handler400 = 'seolpyo_dstory.views.handler'
    handler403 = 'seolpyo_dstory.views.handler'
    handler404 = 'seolpyo_dstory.views.handler'
    handler500 = 'seolpyo_dstory.views.handler'

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('media/', document_root=(settings.BASE_DIR / 'media/'))
```

## 마이그레이션
관리자를 추가하기 위해 마이그레이션을 생성하고, 적용합니다.
```
>> python manage.py makemigrations
>> python manage.py migrate
```

### 관리자 추가하기
티스토리 백업파일을 이용한 복구에는 관리자 계정이 필요합니다.

createsuperuser 명령을 통해 관리자를 추가합니다.

user 생성시 비밀번호를 입력하더라도 마스킹 문자(*)가 노출되지 않을 수 있습니다.
```
>> python manage.py createsuperuser
```

## 티스토리 백업파일을 이용해 글 복구하기
이 패키지는 티스토리 블로그 이사를 위한 2가지 방법을 제공합니다.

하나는 백업파일만을 이용한 단순 복구, 다른 하나는 백업파일과 티스토리 블로그에 접속해 공개설정, 비밀번호, 문자 주소 등의 정보를 가져와 적용하는 것입니다.

티스토리 백업파일은 글의 공개 여부나 보호글의 비밀번호, 임의로 설정한 문자 주소 정보를 제공하지 않습니다.

다운로드한 티스토리 백업파일을 mysite 폴더에 이동시킨 다음, tistory.zip이라는 이름으로 변경합니다.

### 백업파일을 통한 단순복구
장고 shell을 실행하고, 다음 명령어를 입력합니다.
임의로 설정한 문자 주소, 비밀 글 설정 등은 복구되지 않습니다. 백업파일에 해당 정보가 없기 때문입니다.
```
>> python manage.py shell
>> from seolpyo_dstory.utils import restore as r
>> r()
```

### 백업파일과 티스토리 블로그를 통한 복구
장고 shell을 실행하고, 다음 명령어를 입력합니다.

복구 과정에서 티스토리에 로그인하기 위한 로그인 아이디와 로그인 비밀번호를 요구합니다.

user 생성시와 마찬가지로 비밀번호 입력시 마스킹 문자(*)가 표시되지 않을 수 있습니다.

2단계 인증을 사용 중인 경우 로그인에 실패하기 때문에 2단계 인증을 사용하지 않는 계정이어야 합니다.
```
>> python manage.py shell
>> from seolpyo_dstory.utils import restore2 as r
>> r()
```


## 확인하기
장고 프로젝트를 실행하고, 복구된 글을 확인해봅니다.

로컬 서버에서 실행하는 경우 기본 주소는 <http://127.0.0.1:8000>입니다.
```
>> python manage.py runserver
```


# 그 외 설정들
여러 설정들을 만들고 적용할 수 있도록 했습니다.

디스토리 설정들과 장고 사이트 호스팅 관련 정보는 [설표의장고](https://django.seolpyo.com/)에서 확인하실 수 있습니다.


# 디스토리 웹사이트 배포하기(운영 방법)
디스토리 패키지를 통해 서버에서 웹사이트를 운영하는 방법은 다음 링크에서 확인하실 수 있습니다.

[디스토리 배포 방법 확인하러 가기](https://django.seolpyo.com/entry/52/)
