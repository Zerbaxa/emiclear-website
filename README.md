# EM-I-CLEAR Website

이 폴더는 응급의학혁신교육연구회(EM-I-CLEAR)의 공개 웹사이트 코드를 위한 별도 작업공간입니다.

## 관리 원칙

- 행정·세무·회원·주소 관련 원본 문서는 OneDrive `60_EMICLEAR`에서 관리합니다.
- 이 저장소에는 공개가 승인된 단체 소개, 교육자료, 활동소식과 웹사이트 코드만 둡니다.
- 회원명, 생년월일, 서명, 상세 주소, FTP 비밀번호와 각종 인증키는 저장하지 않습니다.
- 교육자료는 내부 검토를 마친 뒤 공개용 사본만 수동으로 반영합니다.

## 기술 구성

- Astro와 TypeScript
- Markdown/MDX 콘텐츠 컬렉션
- Pagefind 정적 검색
- GitHub 공개 저장소 `emiclear-website`
- GitHub Actions를 이용한 닷홈 FTP 자동 배포

## 로컬 실행

```bash
npm install
npm run dev
```

배포용 결과물은 `npm run build`로 생성하며 `dist` 폴더에 저장됩니다.

## 콘텐츠 관리

- 교육자료: `src/content/education`
- 활동소식: `src/content/news`
- `draft: true`인 문서는 공개 사이트에서 제외됩니다.
- 개인 작성자와 검토자 이름은 공개 문서에 기록하지 않습니다.

## 자동 배포

GitHub 저장소의 `main` 브랜치에 push하면 사이트를 빌드합니다. 저장소에 `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` Secrets가 등록된 경우에만 닷홈 `html` 폴더로 배포합니다.
