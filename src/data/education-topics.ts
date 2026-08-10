/**
 * 교육자료 카테고리와 주제 목록.
 *
 * 발간 여부는 여기 적지 않는다. `src/content/education/<topic>-<audience>.md` 가
 * 있으면 발간된 것으로 보고 인덱스가 자동으로 링크를 건다. 여기 있는 주제 중
 * 아직 파일이 없는 것은 「준비 중」으로 표시된다.
 *
 * slug 는 정본 저장소(emiclear_positionpaper)의 `topics/` 폴더명과 같아야 한다.
 * 새 주제가 착수되면 여기에 한 줄 추가하면 되고, 발간되면 저절로 링크가 살아난다.
 */

export interface Topic {
  /** 정본 폴더명 = 콘텐츠 파일 접두어 */
  slug: string;
  /** 카드에 노출되는 짧은 이름 */
  label: string;
  labelEn: string;
}

export interface Category {
  id: string;
  label: string;
  labelEn: string;
  description: string;
  descriptionEn: string;
  topics: Topic[];
}

export const categories: Category[] = [
  {
    id: "injury-care",
    label: "다쳤을 때",
    labelEn: "When a child is hurt",
    description: "다쳤을 때 집에서 하는 처치와 병원에 가야 할 때",
    descriptionEn: "What to do at home, and when to go to hospital",
    topics: [
      { slug: "burn", label: "화상", labelEn: "Burns" },
      { slug: "dental-trauma", label: "치아손상", labelEn: "Dental injury" },
      { slug: "head-injury", label: "두부외상", labelEn: "Head injury" },
      { slug: "facial-laceration", label: "얼굴 열상", labelEn: "Facial cuts" },
      { slug: "oral-soft-tissue", label: "입안 상처", labelEn: "Mouth injury" },
    ],
  },
  {
    id: "injury-prevention",
    label: "다치지 않게",
    labelEn: "Before it happens",
    description: "다치기 전에 갖추는 보호장구와 습관",
    descriptionEn: "Protective gear and habits that prevent injury",
    topics: [
      { slug: "helmet", label: "헬멧", labelEn: "Helmets" },
      { slug: "eye-protection", label: "눈 보호", labelEn: "Eye protection" },
      { slug: "orofacial-mouthguard", label: "마우스가드", labelEn: "Mouthguards" },
    ],
  },
];

/** 대상 표기. 카드 배지와 자료 페이지 eyebrow 에 함께 쓴다. */
export const audienceLabel = {
  public: "보호자용",
  clinicians: "의료인용",
} as const;

export const audienceLabelEn = {
  public: "For caregivers",
  clinicians: "For clinicians",
} as const;

/**
 * 영문판 파일은 `<topic>-<audience>-en.md` 로 둔다. 파일명에 점을 넣으면
 * 컬렉션 id 에 그대로 남아 URL 이 지저분해지므로 하이픈을 쓴다.
 * URL 은 접미사를 뗀 `/en/education/<topic>-<audience>/` 가 된다.
 */
export const EN_SUFFIX = "-en";
export const stripEn = (id: string) =>
  id.endsWith(EN_SUFFIX) ? id.slice(0, -EN_SUFFIX.length) : id;
