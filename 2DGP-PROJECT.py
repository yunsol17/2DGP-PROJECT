from pico2d import *
import random

BK_WIDTH, BK_HEIGHT = 1080, 879

open_canvas(BK_WIDTH, BK_HEIGHT)

# 배경 클래스
class BackGround:
    def __init__(self):
        self.image = load_image('BackGround.JPG')
    def update(self):
        pass
    def draw(self):
        self.image.draw(BK_WIDTH // 2, BK_HEIGHT // 2)

# 고래 클래스
class Whale:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 400
        self.frame = 0
        self.image = load_image('whale.png')
        self.frame_width = self.image.w // 2  # 가로 프레임 2개
        self.frame_height = self.image.h // 4  # 세로 프레임 4개
    def update(self):
        self.frame = (self.frame + 1) % 2
        self.x -= 5
    def draw(self):
        self.image.clip_draw(self.frame % 2  * self.frame_width, 3 * self.frame_height,
                             self.frame_width, self.frame_height, self.x, self.y)

# 이벤트 처리 함수
def handle_events():
    global swimming
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            swimming = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            swimming = False

# 게임 초기화
def reset_world():
    global swimming
    global background
    global whale
    swimming = True
    background = BackGround()
    whale = Whale()

# 월드 업데이트
def update_world():
    whale.update()

# 월드 렌더링
def render_world():
    clear_canvas()
    background.draw()
    whale.draw()  # 고래 그리기 추가
    update_canvas()

# 초기화 코드
reset_world()

# 메인 게임 루프
swimming = True
while swimming:
    handle_events()
    update_world()
    render_world()
    delay(0.5)

# 종료 코드
close_canvas()
