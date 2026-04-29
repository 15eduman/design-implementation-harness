# 디자인 구현 하네스

LLM 에이전트가 원본 디자인의 품질을 잃지 않고 UI를 구현, 컴포넌트화,
QA 리뷰할 수 있도록 돕는 범용 하네스입니다.

Figma-to-app, Figma-to-Figma, 디자인 시스템 마이그레이션처럼 시각 구현도가
중요한 작업을 위해 만들었습니다. 여백, 이미지 슬롯, 아이콘 인스턴스,
마스크, 그라디언트, row rhythm, 컴포넌트 재사용, 스크린샷 QA 같은 요소를
명시적으로 다룹니다.

영문 문서는 [README.md](README.md)를 참고하세요.

## 왜 필요한가

LLM은 UI의 큰 구조는 꽤 잘 재현합니다. 하지만 고품질 프로덕트 디자인은
작고 구체적인 결정들에 많이 의존합니다.

- 정확한 gutter와 카드 폭
- 아이콘 slot과 실제 아이콘 visual size의 차이
- 이미지 crop safe area
- progress mask와 gradient
- 고정 row height
- CTA baseline alignment
- 컴포넌트 밀도
- 원본 asset 재사용

에이전트가 텍스트 프롬프트나 범용 스타일 가이드만 보고 시작하면 이런
디테일이 흔한 기본값으로 평평해지기 쉽습니다. 결과는 구조적으로는 맞지만
시각적으로 약해집니다.

이 하네스는 에이전트에게 더 엄격한 흐름을 강제합니다.

```txt
source design
  -> module inventory
  -> source-backed components
  -> candidate composition
  -> screenshot diff
  -> structured visual QA
  -> targeted repair
```

목표는 취향을 자동화하는 것이 아닙니다. 좋은 원본 디자인의 품질을
구현 과정에서 덜 잃게 만드는 것입니다.

## 누가 쓰면 좋은가

### 디자이너와 디자인 시스템 담당자

고품질 Figma 원본이 구현이나 화면 확장 과정에서 계속 약해질 때 유용합니다.
시각적 우려를 재사용 가능한 컴포넌트 규칙과 QA 기준으로 바꿉니다.

### 프론트엔드 개발자

디자인 리뷰에서 “거의 맞는데 뭔가 다르다”는 피드백이 반복될 때 좋습니다.
gutter, 카드 radius, 이미지 crop, CTA alignment 같은 측정 가능한 문제를
주관적 감상과 분리할 수 있습니다.

### AI 에이전트 빌더

UI 작업을 역할별 에이전트로 나누고 싶을 때 사용합니다.

```txt
Componentizer -> Composer -> Visual QA -> Repair
```

한 에이전트에게 디자인, 구현, 판단, 수정을 모두 맡기는 것보다 안정적입니다.

### 제품팀과 QA

디자인 구현도를 릴리즈 품질의 일부로 관리하고 싶을 때 쓸 수 있습니다.
PR, QA 리뷰, 디자인 sign-off에서 논의하기 쉬운 구조화된 QA 리포트를 만들 수
있습니다.

### 에이전시와 외주 제작팀

클라이언트가 Figma를 제공하고 faithful implementation을 기대할 때 유용합니다.
“디자인처럼 더 맞춰주세요”보다 더 명확한 리뷰 언어를 제공합니다.

## 잘 맞는 경우

이 하네스는 다음 상황에 잘 맞습니다.

- 이미 완성도 높은 원본 디자인이 있다.
- 시각 구현도가 중요하다.
- UI가 모듈 또는 컴포넌트 기반이다.
- 여러 사람 또는 여러 에이전트가 같은 시각 시스템을 재현해야 한다.
- 원본과 후보 화면의 스크린샷을 캡처할 수 있다.

커머스, 금융, SaaS, 헬스케어, 내부 도구, 교육, 네이티브 앱, 소비자 제품,
디자인 시스템 마이그레이션 등 다양한 제품군에 적용할 수 있습니다. 핵심
구조는 특정 브랜드나 서비스에 묶여 있지 않습니다.

## 덜 맞는 경우

다음 상황에서는 효과가 낮습니다.

- 디자인이 아직 러프한 와이어프레임이다.
- 목표가 넓은 시각 탐색이다.
- 구현 속도가 fidelity보다 중요하다.
- 모든 화면이 의도적으로 완전히 다르다.
- 안정적인 원본 스크린샷이나 컴포넌트 시스템이 없다.

## 핵심 원칙

원본 디자인이 있다면 에이전트는 새로 그리는 것부터 시작하면 안 됩니다.
먼저 원본 시스템을 식별하고 재사용해야 합니다.

우선순위:

1. 원본 Figma 컴포넌트 또는 노드
2. 원본 스크린샷
3. 모듈 스펙
4. QA 체크리스트
5. 범용 디자인 가이드
6. 에이전트의 자체 판단

## 디렉터리 구조

```txt
.
  README.md
  README.ko.md
  CLAUDE.md
  LICENSE
  requirements.txt
  design-harness.config.json
  agents.yaml
  docs/
    design-strategy.example.md
    module-spec.example.md
  prompts/
    agent-system.md
    source-reader.md
    componentizer.md
    composer.md
    visual-qa.md
    repair.md
  checklists/
    accessibility.md
    visual-fidelity.md
  schemas/
    component-inventory.schema.json
    qa-report.schema.json
    module-inventory.schema.json
  scripts/
    create_qa_report.py
    validate_qa_report.py
    build_agent_packet.py
    score_visual_diff.py
    create-qa-report.mjs
  guides/
    figma-screenshot-diff.md
  reports/
    sample-qa-report.md
```

## 빠른 시작

1. `design-harness.config.json`을 수정합니다.

원본 디자인 정보를 넣습니다.

```json
{
  "source": {
    "figmaFileKey": "YOUR_FIGMA_FILE_KEY",
    "sourceNodeId": "SOURCE_NODE_ID",
    "sourceFrameName": "Source screen name",
    "sourceFrameSize": {
      "width": 390,
      "height": 844
    }
  }
}
```

2. 모듈 인벤토리를 추가합니다.

```json
{
  "name": "ProductCard",
  "sourceNodeId": "123:456",
  "targetComponentName": "Commerce/ProductCard",
  "critical": true
}
```

3. QA 리포트 초안을 생성합니다.

```bash
python3 scripts/create_qa_report.py
```

4. 리포트 구조를 검증합니다.

```bash
python3 scripts/validate_qa_report.py \
  --allow-draft \
  --strict-categories \
  reports/qa-report.draft.json
```

5. 에이전트 프롬프트 패킷을 생성합니다.

```bash
python3 scripts/build_agent_packet.py visual_qa
```

6. 원본과 후보 이미지가 있으면 screenshot diff를 실행합니다.

```bash
python3 scripts/score_visual_diff.py \
  captures/source/screen.source.png \
  captures/candidate/screen.candidate.png \
  --out captures/diff/screen.diff.json
```

`score_visual_diff.py`는 Pillow가 필요합니다.

```bash
python3 -m pip install -r requirements.txt
```

7. smoke test를 실행합니다.

```bash
python3 -m unittest discover -s tests
```

## 에이전트 역할

역할은 `agents.yaml`에 정의되어 있습니다.

### Source Reader

Figma 원본 metadata, screenshot, 모듈 후보를 읽습니다. 원본 geometry를
metadata 없이 추론하거나 새로 그리면 안 됩니다.

프롬프트: `prompts/source-reader.md`

### Componentizer

원본 모듈을 재사용 가능한 컴포넌트로 변환합니다. 원본 geometry, mask,
gradient, image slot, icon instance를 보존합니다.

프롬프트: `prompts/componentizer.md`

### Composer

source-backed component instance로 후보 화면을 조립합니다. content, order,
image override, 허용된 property만 바꿉니다.

프롬프트: `prompts/composer.md`

### Visual QA

원본과 후보 screenshot을 구조화된 rubric으로 리뷰합니다.
`schemas/qa-report.schema.json`에 맞는 리포트를 생성합니다.

프롬프트: `prompts/visual-qa.md`

### Repair

실패한 QA 항목만 수정합니다. 여러 픽셀을 손으로 조정하기보다 약한 재구성물을
source-backed component로 교체하는 것을 우선합니다.

프롬프트: `prompts/repair.md`

## 접근성

시각 구현도만으로는 충분하지 않습니다. 후보 화면이 탐색 가능하고, 읽을 수
있고, 조작 가능한지 확인하려면 `checklists/visual-fidelity.md`와 함께
`checklists/accessibility.md`를 사용하세요.

## 잡아낼 수 있는 문제

- 원본 gutter가 범용 모바일 gutter로 바뀌는 문제
- 카드 radius가 기본값으로 흐르는 문제
- 이미지 slot이 content에 따라 늘어나는 문제
- 제품 이미지의 safe crop이 깨지는 문제
- AI/helper row가 일반 subtitle처럼 변하는 문제
- 아이콘이 근사 placeholder로 바뀌는 문제
- progress mask와 gradient가 평평한 도형으로 대체되는 문제
- 컴포넌트가 재사용되지 않고 다시 그려지는 문제
- 전체 구조는 맞지만 로컬 density가 무너지는 문제

## Screenshot Diff

`score_visual_diff.py`는 두 이미지를 비교하고 대략적인 시각 지표를 반환합니다.

- `similarityScore`
- `rms`
- `changedAreaRatio`
- compared dimensions

이 점수는 최종 판정이 아니라 triage signal입니다. Visual QA Agent가 모듈 스펙,
체크리스트, diff 결과를 함께 보고 판단해야 합니다.

캡처와 diff 흐름은 다음 문서를 참고하세요.

- `guides/figma-screenshot-diff.md`

## QA 리포트

리포트는 `schemas/qa-report.schema.json`을 따라야 합니다.

각 이슈는 다음 항목을 포함해야 합니다.

- category
- severity
- observed difference
- expected source behavior
- likely cause
- repair instruction

예시 category:

- `frameRhythm`
- `cardGeometry`
- `internalAlignment`
- `imageSlotFidelity`
- `typographyHierarchy`
- `aiLineGrammar`
- `dataResilience`
- `sourceComponentReuse`

config가 있는 경우 strict category 검증을 사용하세요.

```bash
python3 scripts/validate_qa_report.py \
  --allow-draft \
  --strict-categories \
  reports/qa-report.draft.json
```

완성된 리포트에는 threshold 검증을 사용할 수 있습니다.

```bash
python3 scripts/validate_qa_report.py \
  --strict-categories \
  --enforce-thresholds \
  reports/qa-report.json
```

## Codex Skill

초안 skill은 다음 위치에 있습니다.

```txt
skill/design-implementation-harness/SKILL.md
```

Codex 또는 다른 agent runtime이 디자인 구현 작업에서 이 workflow를 자동으로
불러오게 만들 때 시작점으로 사용할 수 있습니다.

## 다른 제품으로 일반화하기

`design-harness.config.json`의 서비스별 값을 교체하세요.

- `figmaFileKey`
- `sourceNodeId`
- `sourceFrameName`
- `moduleInventory`
- `captureCases`
- 연결된 spec/checklist

하네스 core는 중립적으로 유지하고, 제품별 정보는 config, module inventory,
source screenshot, 선택적 디자인 문서에 둡니다.

## 실전 규칙

후보 화면이 약해 보이면 먼저 이렇게 물어보세요.

```txt
에이전트가 재사용해야 할 원본 컴포넌트를 다시 그린 것은 아닌가?
```

그렇다면 픽셀 튜닝 전에 source-backed component로 교체하세요.

## 한계

- 실제 디자인 시스템을 대체하지 않습니다.
- 원본 예시 없이 좋은 새 시각 방향을 보장하지 않습니다.
- 이미지 diff는 폰트, anti-aliasing, scale, dynamic content에 과민할 수 있습니다.
- screenshot score는 구조화된 Visual QA와 함께 사용해야 합니다.
