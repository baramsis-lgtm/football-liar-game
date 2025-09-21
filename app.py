import random
from flask import Flask, render_template, request, redirect, url_for, session

# Flask 앱 초기화 및 세션에 필요한 비밀 키 설정
app = Flask(__name__)
# 보안을 위해 실제 서비스에서는 더 복잡한 문자열을 사용하세요.
app.secret_key = 'your_super_secret_key_here'

# ----------------------------
# LiarGame_football.py에서 가져올 데이터
# ----------------------------
# 35개 클럽
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

clubs_by_tier = {
    "S": clubs_S, "A": clubs_A, "B": clubs_B
}
# 현역 선수 (100명) - S/A/B로 분류
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

# 레전드 선수 200명 (티어 + 주 활동 시기 포함)
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

# 합치기 및 중복 제거, era 필터링을 위해 하나의 리스트로 변환
raw_legends = legends_S + legends_A + legends_B

# 중복 제거 및 정리
final_legends = []
seen = set()
for name, tier, era in raw_legends:
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
        legends_by_era["2000s"].append(name)

# ----------------------------
# 유틸리티: 선택된 카테고리 기준으로 제시어 풀 반환
# ----------------------------
def build_word_pool(category, difficulty, legend_era=None):
    tiers = []
    if difficulty == "축알못":
        tiers = ["S"]
    elif difficulty == "축잘알":
        tiers = ["S", "A"]
    # HTML 난이도 '축신'을 '고인물'과 동일하게 처리
    elif difficulty == "축신":
        tiers = ["S", "A", "B"]
    else: # 다른 값(고인물)이 들어올 경우를 대비
        tiers = ["S", "A", "B"]

    pool = []
    if category == "클럽":
        for t in tiers:
            pool += clubs_by_tier.get(t, [])
    elif category == "현역선수":
        for t in tiers:
            pool += players_by_tier.get(t, [])
    elif category == "레전드":
        for name, tier, era in final_legends:
            if tier in tiers and (not legend_era or legend_era == era):
                pool.append(name)
    
    pool_unique = []
    seen_local = set()
    for p in pool:
        p_strip = p.split('(')[0].strip()
        if p_strip and p_strip not in seen_local:
            pool_unique.append(p)
            seen_local.add(p_strip)
    return pool_unique


# ----------------------------
# Flask 라우트 (웹 페이지의 주소와 기능 연결)
# ----------------------------

@app.route('/', methods=['GET', 'POST'])
def home():
    error_message = None
    # GET 요청 시: 세션 데이터가 남아있을 경우 제거
    if request.method == 'GET' and 'game_state' in session:
        session.pop('game_state', None)
    
    if request.method == 'POST':
        try:
            # POST 요청 시: 새로운 게임 시작이므로 세션 데이터 완전 초기화
            session.pop('game_state', None)
            
            category = request.form.get('category')
            difficulty = request.form.get('difficulty')
            legend_era = request.form.get('legend_era')
            
            # num_players가 올바른 숫자인지 확인합니다.
            num_players_str = request.form.get('num_players')
            if not num_players_str or not num_players_str.isdigit():
                error_message = "오류: 인원수를 올바르게 입력해주세요."
                return render_template('index.html', error_message=error_message)
            
            num_players = int(num_players_str)
            if num_players < 2 or num_players > 6:
                error_message = "오류: 인원수는 2명에서 6명 사이여야 합니다."
                return render_template('index.html', error_message=error_message)

            word_pool = build_word_pool(category, difficulty, legend_era)
            if not word_pool:
                error_message = "오류: 해당 조건에 맞는 제시어가 없습니다."
                return render_template('index.html', error_message=error_message)

            selected_word = random.choice(word_pool)
            liar_index = random.randrange(num_players)
            participant_order = list(range(num_players))
            random.shuffle(participant_order)

            session['game_state'] = {
                'selected_word': selected_word,
                'liar_index': liar_index,
                'num_players': num_players,
                'participant_order': participant_order,
                'current_index': 0
            }
            
            return redirect(url_for('show_word'))

        except (ValueError, KeyError) as e:
            # 예기치 않은 오류 발생 시 사용자에게 메시지 표시
            error_message = f"게임 설정 중 오류가 발생했습니다: {e}"
            return render_template('index.html', error_message=error_message)

    return render_template('index.html', error_message=error_message)

@app.route('/show_word')
def show_word():
    game_state = session.get('game_state')
    if not game_state:
        # 세션에 게임 상태가 없으면 홈으로 리다이렉트
        return redirect(url_for('home'))

    current_index = game_state['current_index']
    num_players = game_state['num_players']

    if current_index >= num_players:
        return render_template('game_start.html')
    
    player_id = game_state['participant_order'][current_index]
    is_liar = (player_id == game_state['liar_index'])

    displayed_text = "라이어" if is_liar else game_state['selected_word']

    return render_template('show_word.html', 
                            displayed_text=displayed_text,
                            current_player=current_index + 1,
                            total_players=num_players)

@app.route('/next_player', methods=['POST'])
def next_player():
    game_state = session.get('game_state')
    if game_state:
        game_state['current_index'] += 1
        session['game_state'] = game_state

    return redirect(url_for('show_word'))

# ----------------------------
# 서버 실행
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)