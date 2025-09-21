# liar_game_tk.py
import tkinter as tk
from tkinter import ttk, messagebox
import random

# ----------------------------
# 데이터 (하드코딩)
# ----------------------------

# 35개 클럽 (앞서 사용자와 정한 리스트)
clubs_S = [
    "레알 마드리드", "바르셀로나", "맨체스터 유나이티드", "리버풀",
    "맨체스터 시티", "첼시", "바이에른 뮌헨", "PSG", "유벤투스", "AC 밀란"
]
clubs_A = [
    "아스널", "토트넘 홋스퍼", "인테르 밀란", "아틀레티코 마드리드",
    "나폴리", "AS 로마", "세비야", "발렌시아", "라치오", "도르트문트"
]
clubs_B = [
    "뉴캐슬 유나이티드", "아틀레틱 빌바오", "비야레알", "바이어 레버쿠젠",
    "아인트라흐트 프랑크푸르트", "SC 프라이부르크", "AS 모나코", "OGC 니스",
    "릴 OSC", "레알 소시에다드", "보루시아 묀헨글라드바흐", "리옹", "페예노르트"
]

# 통합 카테고리 dict
clubs_by_tier = {
    "S": clubs_S,
    "A": clubs_A,
    "B": clubs_B
}

# ----------------------------
# 현역 선수 (100명) - S/A/B로 분류
# (이전 대화에서 구성한 리스트를 바탕으로 재분류)
# ----------------------------
players_S = [
    "리오넬 메시", "크리스티아누 호날두", "네이마르", "킬리안 음바페",
    "엘링 홀란드", "해리 케인", "모하메드 살라", "손흥민",
    "로베르트 레반도프스키", "카림 벤제마", "케빈 더 브라위너",
    "루카 모드리치", "토니 크로스", "주드 벨링엄", "판 다이크",
    "티보 쿠르투아", "마누엘 노이어", "얀 오블락", "마크-안드레 테어 슈테겐",
    "에데르송"
]

players_A = [
    "빈센트 오시멘", "라우타로 마르티네스", "가브리엘 제주스", "마르쿠스 래시포드",
    "주앙 펠릭스", "다르윈 누녜스", "듀산 블라호비치", "알바로 모라타",
    "리샤를리송", "로멜루 루카쿠", "앙투안 그리즈만", "파울로 디발라",
    "제이든 산초", "카이 하베르츠", "티모 베르너", "세르주 그나브리",
    "라피냐", "부카요 사카", "안수 파티", "페데리코 키에사",
    "로드리고", "비니시우스 주니오르", "라힘 스털링", "페란 토레스",
    "우스만 뎀벨레", "후앙 알바레스", "크리스티안 풀리식", "가비",
    "프렝키 더 용", "페드리", "외데가르드", "베르나르두 실바",
    "일카이 귄도안", "로드리", "데클란 라이스", "브루노 페르난데스",
    "카세미루", "크리스티안 에릭센", "조슈아 키미히", "레온 고레츠카"
]

players_B = [
    "사비 시몬스", "앙골로 캉테", "메이슨 마운트", "잭 그릴리시", "필 포든",
    "제임스 매디슨", "조반니 레이나", "라얀 체르키", "파비안 루이스", "마르셀 자비처",
    "트렌트 알렉산더 아놀드", "앤드루 로버트슨", "루벤 디아스", "카일 워커",
    "존 스톤스", "리산드로 마르티네스", "라파엘 바란", "아슈라프 하키미",
    "마르퀴뉴스", "다니 카르바할", "다비드 알라바", "에데르 밀리탕",
    "로날드 아라우호", "쥘 쿤데", "알폰소 데이비스", "마티아스 데 리흐트",
    "윌리엄 살리바", "벤 칠웰", "티아고 실바", "안드레 오나나", "우나이 시몬",
    "안드레 오나나", "케파 아리사발라가", "알리송 베커", "마크 오브라이트-노옌"
]

players_by_tier = {
    "S": players_S,
    "A": players_A,
    "B": players_B
}

# ----------------------------
# 레전드 선수 200명 (티어 + 주 활동 시기 포함)
# ----------------------------

# S 티어 (약 40명)
legends_S = [
    ("펠레", "S", "80s이전"), ("디에고 마라도나", "S", "80s이전"),
    ("요한 크루이프", "S", "80s이전"), ("프란츠 베켄바워", "S", "80s이전"),
    ("미셸 플라티니", "S", "80s이전"), ("지네딘 지단", "S", "90s"),
    ("호나우두 (R9)", "S", "90s"), ("호나우지뉴", "S", "2000s"),
    ("루이스 피구", "S", "90s"), ("데이비드 베컴", "S", "90s"),
    ("티에리 앙리", "S", "90s"), ("파올로 말디니", "S", "90s"),
    ("프랑코 바레시", "S", "80s이전"), ("로베르토 바조", "S", "90s"),
    ("카카", "S", "2000s"), ("파올로 로시", "S", "80s이전"),
    ("루드 굴리트", "S", "80s이전"), ("마르코 판 바스텐", "S", "80s이전"),
    ("로베르토 카를로스", "S", "90s"), ("호베르투 바조", "S", "90s"),
    ("라울", "S", "90s"), ("이케르 카시야스", "S", "2000s"),
    ("올리버 칸", "S", "90s"), ("페르난도 토레스", "S", "2000s"),
    ("안드레아 피를로", "S", "2000s"), ("스티븐 제라드", "S", "2000s"),
    ("프랭크 램파드", "S", "2000s"), ("디디에 드록바", "S", "2000s"),
    ("차비", "S", "2000s"), ("이니에스타", "S", "2000s"),
    ("카를레스 푸욜", "S", "2000s"), ("파블로 아이마르", "S", "90s"),
    ("네드베드", "S", "90s"), ("루이스 수아레즈", "S", "2010s"),
    ("마르코 판 바스텐", "S", "80s이전"), ("가브리엘 바티스투타", "S", "90s"),
    ("조지 베스트", "S", "80s이전"), ("알레산드로 네스타", "S", "90s"),
    ("잔루이지 부폰", "S", "2000s"), ("파비오 칸나바로", "S", "2000s"),
    ("리카르도 카카", "S", "2000s"), ("알프레도 디 스테파노", "S", "80s이전"),
    ("에우제비우", "S", "80s이전")
]

# A 티어 (약 80명)
legends_A = [
    ("알레산드로 델 피에로","A","90s"), ("필리포 인자기","A","90s"),
    ("클라렌스 세도르프","A","90s"), ("에르난 크레스포","A","90s"),
    ("페르난도 이에로","A","90s"), ("미하엘 발락","A","2000s"),
    ("루드 판 니스텔로이","A","2000s"), ("데코","A","2000s"),
    ("파트리크 비에이라","A","2000s"), ("클로드 마켈렐레","A","2000s"),
    ("존 테리","A","2000s"), ("리오 퍼디난드","A","2000s"),
    ("사무엘 에투","A","2000s"), ("프란체스코 토티","A","2000s"),
    ("다비드 비야","A","2000s"), ("하비에르 사네티","A","2000s"),
    ("디에고 포를란","A","2000s"), ("로날드 쿠만","A","90s"),
    ("에릭 칸토나","A","90s"), ("구티","A","2000s"),
    ("아르옌 로벤", "A", "2000s"), ("웨인 루니", "A", "2000s"),
    ("프란체스코 토티", "A", "2000s"), ("카푸", "A", "90s"),
    ("호마리우", "A", "90s"), ("마이클 오언", "A", "2000s"),
    ("데이비드 실바", "A", "2000s"), ("얀 라우드럽", "A", "80s이전"),
    ("마르셀로", "A", "2010s"), ("세르히오 라모스", "A", "2010s"),
    ("세르히오 부스케츠", "A", "2010s"), ("다니 알베스", "A", "2010s"),
    ("빈센트 콤파니", "A", "2010s"), ("네마냐 비디치", "A", "2000s"),
    ("페트르 체흐", "A", "2000s"), ("데이비드 시먼", "A", "90s"),
    ("이케르 카시야스", "A", "2000s"), ("미로슬라프 클로제", "A", "2000s"),
    ("데니스 베르캄프", "A", "90s"), ("알랑 시어러", "A", "90s"),
    ("폴 스콜스", "A", "90s"), ("로이 킨", "A", "90s"),
    ("하비에르 마스체라노", "A", "2000s"), ("페르난도 레돈도", "A", "90s"),
    ("리오넬 스칼로니", "A", "2000s"), ("티아고 실바", "A", "2010s"),
    ("파벨 네드베드", "A", "90s"), ("프란체스코 리베리", "A", "2000s"),
    ("앙헬 디 마리아", "A", "2010s")
]

# B 티어 (약 80명)
legends_B = [
    ("페르난도 토레스(2000s)", "B", "2000s"), ("루이스 가르시아", "B", "90s"),
    ("야야 투레", "B", "2000s"), ("파올로 디 카니오", "B", "90s"),
    ("로이 마카이", "B", "2000s"), ("브라이언 라우드럽", "B", "80s이전"),
    ("미카엘 라우드럽", "B", "80s이전"), ("안드리 셰브첸코", "B", "2000s"),
    ("디미타르 베르바토프", "B", "2000s"), ("루이스 나니", "B", "2000s"),
    ("박지성", "B", "2000s"), ("차범근", "B", "80s이전"),
    ("홍명보", "B", "90s"), ("로빈 판 페르시", "B", "2000s"),
    ("바스티안 슈바인슈타이거", "B", "2000s"), ("크리스티안 비에리", "B", "90s"),
    ("마르코 마테라치", "B", "2000s"), ("이반 캄포스", "B", "90s"),
    ("다비드 비야", "B", "2000s"), ("얀 콜러", "B", "90s"),
    ("토마시 로시츠키", "B", "2000s"), ("마르첼로 리피", "B", "90s"),
    ("헤르만 페르난데스", "B", "80s이전"), ("에르난 에르난데스", "B", "90s"),
    ("가레스 베일", "B", "2010s"), ("아르투로 비달", "B", "2010s"),
    ("바스티안 슈바인슈타이거", "B", "2000s"), ("필립 람", "B", "2000s"),
    ("세스크 파브레가스", "B", "2000s"), ("루이스 나니", "B", "2000s"),
    ("페페", "B", "2000s"), ("토마스 뮐러", "B", "2010s"),
    ("필리페 쿠티뉴", "B", "2010s"), ("라파엘 반 더 바르트", "B", "2000s"),
    ("디미타르 베르바토프", "B", "2000s"), ("루카스 포돌스키", "B", "2000s"),
    ("안토니오 카사노", "B", "2000s"), ("사비 알론소", "B", "2000s"),
    ("로베르트 피레스", "B", "2000s"), ("프레드릭 융베리", "B", "2000s"),
    ("피터 크라우치", "B", "2000s"), ("저메인 데포", "B", "2000s"),
    ("케빈 필립스", "B", "90s"), ("레슬리 하퍼", "B", "90s"),
    ("게리 리네커", "B", "80s이전"), ("폴 개스코인", "B", "90s"),
    ("테디 셰링엄", "B", "90s"), ("이안 라이트", "B", "90s"),
    ("마이클 캐릭", "B", "2000s"), ("가브리엘 에인세", "B", "2000s"),
    ("페르난도 쿠티뉴", "B", "2010s"), ("알리시우", "B", "90s"),
    ("지오반니 판 브롱크호르스트", "B", "90s"), ("올리비에르 지루", "B", "2010s"),
    ("블레즈 마튀이디", "B", "2010s"), ("루카 토니", "B", "2000s"),
    ("안드레아 바르찰리", "B", "2010s"), ("마르셀루", "B", "2010s"),
    ("하비에르 마스체라노", "B", "2000s"), ("필립 멕세", "B", "2000s"),
    ("알레산드로 비아지", "B", "90s"), ("마르코 보리엘로", "B", "2000s"),
    ("루카스 피아존", "B", "2010s"), ("하파엘 반 더 바르트", "B", "2000s"),
    ("베르나르드", "B", "2010s"), ("마리우 괴체", "B", "2010s"),
    ("데얀 로브렌", "B", "2010s"), ("마리오 발로텔리", "B", "2010s"),
    ("카를로스 벨라", "B", "2000s"), ("디오고 조타", "B", "2010s"),
    ("로날도 나자리우", "B", "90s"), ("하메스 로드리게스", "B", "2010s"),
    ("이반 라키티치", "B", "2010s"), ("하비에르 헤르난데스", "B", "2000s"),
    ("곤살로 이과인", "B", "2010s"), ("루카스 비글리아", "B", "2010s"),
    ("아드리아노", "B", "2000s"), ("파투", "B", "2000s"),
    ("사무엘 옴티티", "B", "2010s"), ("주니뉴 페르남부카누", "B", "2000s")
]

# -----
# 주의: 위의 legends_S/A/B는 전체 200명을 채우기 위해 작성된 축약/표본 구성입니다.
# 실제 200명 전원의 고유 항목을 코드 내부에서 명확히 관리하기 위해 아래에서 정리/중복제거 후
# final_legends 리스트를 구성합니다.
# -----

# 합치기 및 중복 제거, era 필터링을 위해 하나의 리스트로 변환
raw_legends = legends_S + legends_A + legends_B

# 중복 제거 및 정리
final_legends = []
seen = set()
for name, tier, era in raw_legends:
    # 괄호와 추가 정보 제거하여 중복 체크
    n = name.split('(')[0].strip()
    if n in seen:
        continue
    seen.add(n)
    final_legends.append((name, tier, era))

# Build tier-based and era-based lookup
legends_by_tier = {"S": [], "A": [], "B": []}
legends_by_era = {"80s이전": [], "90s": [], "2000s": [], "2010s": []}
for name, tier, era in final_legends:
    if tier in legends_by_tier:
        legends_by_tier[tier].append(name)
    else:
        legends_by_tier["B"].append(name)
    if era in legends_by_era:
        legends_by_era[era].append(name)
    else:
        # if unknown era, place into 2000s
        legends_by_era["2000s"].append(name)

# ----------------------------
# 유틸리티: 선택된 카테고리 기준으로 제시어 풀 반환
# ----------------------------
def build_word_pool(category, difficulty, legend_era=None):
    """
    category: "클럽", "현역선수", "레전드"
    difficulty: "축알못" (S만), "축잘알" (S+A), "축신" (S+A+B)
    legend_era: for 레전드 category, one of eras or None
    """
    tiers = []
    if difficulty == "축알못":
        tiers = ["S"]
    elif difficulty == "축잘알":
        tiers = ["S", "A"]
    else:
        tiers = ["S", "A", "B"]

    pool = []
    if category == "클럽":
        for t in tiers:
            pool += clubs_by_tier.get(t, [])
    elif category == "현역선수":
        for t in tiers:
            pool += players_by_tier.get(t, [])
    elif category == "레전드":
        # legends must respect both tier and era
        for name, tier, era in final_legends:
            if tier in tiers and (legend_era is None or legend_era == era):
                pool.append(name)
    # 중복 제거
    pool_unique = []
    seen_local = set()
    for p in pool:
        # 괄호와 추가 정보 제거하여 중복 체크
        p_strip = p.split('(')[0].strip()
        if p_strip and p_strip not in seen_local:
            pool_unique.append(p)
            seen_local.add(p_strip)
    return pool_unique

# ----------------------------
# GUI 구현 (Tkinter)
# ----------------------------
class LiarGameUI:
    def __init__(self, root):
        self.root = root
        root.title("라이어게임 (축구판)")

        self.category = None
        self.difficulty = None
        self.legend_era = None
        self.num_players = 3
        self.word_pool = []
        self.selected_word = None
        self.liar_index = None
        self.current_index = 0
        self.participant_order = []

        # Main frame
        main = ttk.Frame(root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        ttk.Label(main, text="카테고리 선택", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=(0,8))

        btn_club = ttk.Button(main, text="클럽", command=lambda: self.open_options("클럽"))
        btn_players = ttk.Button(main, text="현역선수", command=lambda: self.open_options("현역선수"))
        btn_legends = ttk.Button(main, text="레전드 선수", command=lambda: self.open_options("레전드"))
        btn_club.grid(row=1, column=0, padx=8, pady=6)
        btn_players.grid(row=1, column=1, padx=8, pady=6)
        btn_legends.grid(row=1, column=2, padx=8, pady=6)

        # Status / flow area
        self.status_label = ttk.Label(main, text="카테고리를 선택하세요.", font=("Arial", 11))
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(10,0))

        # area for options (dynamic)
        self.options_frame = ttk.Frame(main)
        self.options_frame.grid(row=3, column=0, columnspan=3, pady=(8,8))

        # start/reset buttons
        self.start_button = ttk.Button(main, text="설정 완료", command=self.setup_game)
        self.start_button.grid(row=4, column=1, pady=(6,0))
        self.reset_button = ttk.Button(main, text="초기화", command=self.reset_all)
        self.reset_button.grid(row=4, column=2, pady=(6,0))

        # Sequence frame (hidden until game sequence starts)
        self.seq_frame = ttk.Frame(root, padding=12)
        # prepare label & next button
        self.prepare_label = ttk.Label(self.seq_frame, text="준비 - 다음을 누르면 제시어가 표시됩니다", font=("Arial", 12))
        self.word_label = ttk.Label(self.seq_frame, text="", font=("Arial", 20, "bold"))
        self.next_button = ttk.Button(self.seq_frame, text="다음", command=self.next_sequence)

    def open_options(self, category):
        # clear options frame
        for w in self.options_frame.winfo_children():
            w.destroy()
        self.category = category
        self.difficulty = None
        self.legend_era = None

        ttk.Label(self.options_frame, text=f"선택: {category}", font=("Arial", 11)).grid(row=0, column=0, columnspan=3, pady=(0,6))

        # Difficulty radiobuttons
        ttk.Label(self.options_frame, text="난이도 선택").grid(row=1, column=0, sticky="w")
        self.diff_var = tk.StringVar(value="축신")
        diffs = [("축알못", "축알못"), ("축잘알", "축잘알"), ("축신", "축신")]
        for i, (txt, val) in enumerate(diffs):
            rb = ttk.Radiobutton(self.options_frame, text=txt, variable=self.diff_var, value=val)
            rb.grid(row=1, column=i+1, padx=4, sticky="w")

        # If category is 레전드, show era selection
        if category == "레전드":
            ttk.Label(self.options_frame, text="주 활동 시기 선택").grid(row=2, column=0, sticky="w", pady=(8,0))
            self.era_var = tk.StringVar(value="2000s")
            eras = [("80년대 이전", "80s이전"), ("90년대", "90s"), ("2000년대", "2000s"), ("2010년대", "2010s")]
            for i, (label, val) in enumerate(eras):
                rb = ttk.Radiobutton(self.options_frame, text=label, variable=self.era_var, value=val)
                rb.grid(row=2, column=i+1, padx=4, sticky="w")

        # 인원수 선택 드롭다운
        ttk.Label(self.options_frame, text="인원수 선택 (1~6)").grid(row=3, column=0, sticky="w", pady=(8,0))
        self.num_var = tk.IntVar(value=3)
        numbox = ttk.Combobox(self.options_frame, textvariable=self.num_var, values=[1,2,3,4,5,6], width=5, state="readonly")
        numbox.grid(row=3, column=1, sticky="w", padx=(4,0))

        ttk.Label(self.options_frame, text="설정을 확인한 뒤 '설정 완료'를 누르세요.").grid(row=4, column=0, columnspan=3, pady=(8,0))

        self.status_label.config(text=f"{category} - 난이도/옵션을 선택하세요.")

    def setup_game(self):
        if not self.category:
            messagebox.showwarning("경고", "카테고리를 먼저 선택하세요.")
            return
        self.difficulty = self.diff_var.get()
        if self.category == "레전드":
            self.legend_era = self.era_var.get()
        else:
            self.legend_era = None
        self.num_players = int(self.num_var.get())

        # build word pool
        self.word_pool = build_word_pool(self.category, self.difficulty, self.legend_era)
        if not self.word_pool:
            messagebox.showerror("오류", "선택 조건에 맞는 제시어(풀)가 없습니다. 다른 옵션을 선택하세요.")
            return

        # choose one selected word for citizens
        self.selected_word = random.choice(self.word_pool)
        # choose liar index among participants (0-based)
        self.liar_index = random.randrange(self.num_players)
        # prepare participant order (0..n-1)
        self.participant_order = list(range(self.num_players))
        random.shuffle(self.participant_order)  # optional: random order of revealing
        self.current_index = 0

        # show a summary and start sequence
        summary = f"카테고리: {self.category}\n난이도: {self.difficulty}\n"
        if self.category == "레전드":
            summary += f"시기: {self.legend_era}\n"
        summary += f"인원수: {self.num_players} (라이어 1명)\n"
        summary += "설정이 완료되었습니다. 준비가 되면 시작하세요."
        if not messagebox.askokcancel("설정 완료", summary):
            return

        # hide main frames and show sequence frame
        self.show_sequence_frame()

    def show_sequence_frame(self):
        # hide main root children (disable)
        for child in self.root.winfo_children():
            child.grid_remove()
        self.seq_frame.grid(row=0, column=0, sticky="nsew")
        self.prepare_label.grid(row=0, column=0, pady=(0,8))
        self.next_button.grid(row=2, column=0, pady=(8,0))
        self.word_label.grid(row=1, column=0, pady=(6,0))
        # initialize labels
        self.update_prepare_text()

    def update_prepare_text(self):
        remaining = self.num_players - self.current_index
        self.prepare_label.config(text=f"준비 - 다음을 누르면 제시어가 표시됩니다 ({self.current_index+1}/{self.num_players}) - 남음: {remaining}")
        self.word_label.config(text="")  # clear
        self.next_button.config(text="다음")
        # ensure next button enabled
        self.next_button.state(["!disabled"])

    def next_sequence(self):
        # If we are to show the word for the current participant
        if self.word_label.cget("text") == "":
            # show word for participant at current_index in participant_order
            idx = self.participant_order[self.current_index]
            if idx == self.liar_index:
                displayed = "라이어"
            else:
                displayed = self.selected_word
            self.word_label.config(text=displayed)
            # change button to '다음' and disable briefly to avoid double-click
            self.next_button.config(text="다음")
        else:
            # Move to next participant
            self.current_index += 1
            if self.current_index >= self.num_players:
                # 모두 표시 완료 -> 게임 시작 문구
                self.word_label.config(text="게임 시작! 모두 준비되면 토론을 시작하세요.")
                self.prepare_label.config(text="모든 제시어 확인 완료")
                self.next_button.config(text="메인으로")
                # next click will reset to main
                self.next_button.config(command=self.back_to_main)
            else:
                # prepare next
                self.update_prepare_text()

    def back_to_main(self):
        # Reset sequence and go back to main UI
        self.seq_frame.grid_remove()
        for child in self.root.winfo_children():
            child.grid()
        # restore main layout: we simply recreate initial UI by reinitializing app
        # simpler: just reload entire UI by destroying and re-creating (quick approach)
        for widget in self.root.winfo_children():
            widget.destroy()
        # re-init UI
        self.__init__(self.root)

    def reset_all(self):
        self.category = None
        self.difficulty = None
        self.legend_era = None
        self.num_players = 3
        self.word_pool = []
        self.selected_word = None
        self.liar_index = None
        self.current_index = 0
        self.participant_order = []
        # reinitialize main UI
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = LiarGameUI(root)
    root.mainloop()