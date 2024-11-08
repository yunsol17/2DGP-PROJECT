from pico2d import *
import random

BK_WIDTH, BK_HEIGHT = 1080, 879
dir_x = 0  # x축 이동 방향 (왼쪽: -1, 오른쪽: 1)
dir_y = 0  # y축 이동 방향 (아래: -1, 위: 1)
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
        self.direction = 1  # 1이면 오른쪽, -1이면 왼쪽
        self.image = load_image('whale.png')
        self.frame_width = self.image.w // 2  # 가로 프레임 2개
        self.frame_height = self.image.h // 4  # 세로 프레임 4개
    def update(self):
        global dir_x, dir_y
        self.frame = (self.frame + 1) % 2
        self.x += dir_x * 20  # x축 방향 이동
        self.y += dir_y * 20  # y축 방향 이동
        # 화면 밖으로 나가지 않도록 위치 제한
        if self.x < 50:
            self.x = 50
        elif self.x > BK_WIDTH-50:
            self.x = BK_WIDTH-50
        if self.y < 230:
            self.y = 230
        elif self.y > BK_HEIGHT-100:
            self.y = BK_HEIGHT-100
        if dir_x != 0:
            self.direction = dir_x

    def draw(self):
        if self.direction ==-1:
            self.image.clip_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height, self.x, self.y,100,100)
        else:
            self.image.clip_composite_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height,0,'h', self.x, self.y,100,100)

# 이벤트 처리 함수
def handle_events():
    global swimming, dir_x, dir_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            swimming = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir_x += 1  # 오른쪽 이동
            elif event.key == SDLK_LEFT:
                dir_x -= 1  # 왼쪽 이동
            elif event.key == SDLK_UP:
                dir_y += 1  # 위쪽 이동
            elif event.key == SDLK_DOWN:
                dir_y -= 1  # 아래쪽 이동
            elif event.key == SDLK_ESCAPE:
                swimming = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x +=1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1

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
    delay(0.05)

# 종료 코드
close_canvas()
