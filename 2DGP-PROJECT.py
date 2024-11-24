from pico2d import *
import random
import time

# 화면 크기
BK_WIDTH, BK_HEIGHT = 1080, 879

# 이동 방향 초기화
dir_x, dir_y = 0, 0  # x축, y축 이동 방향 (왼쪽: -1, 오른쪽: 1)

# 캔버스 생성
open_canvas(BK_WIDTH, BK_HEIGHT)

# 객체 리스트 초기화
fish1_list = []
crab_list = []

# 초기 시간
last_spawn_time = time.time()
fish1_cnt = 0  # Fish1을 먹은 개수

# 디버깅 모드 설정
DEBUG_MODE = True

# 디버그용 충돌 박스 그리기 함수
def draw_rectangle_debug(*args):
    if DEBUG_MODE:
        draw_rectangle(*args)

# 배경 클래스
class BackGround:
    def __init__(self):
        self.image = load_image('BackGround.JPG')

    def update(self):
        pass

    def draw(self):
        self.image.draw(BK_WIDTH // 2, BK_HEIGHT // 2)

# 레벨 표시 클래스
class Level:
    def __init__(self):
        self.x, self.y = 130, 150
        self.frame = 0
        self.image = load_image('level.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,
                             self.frame_width, self.frame_height,
                             self.x, self.y, 150, 70)

# HP 표시 클래스
class Hp:
    def __init__(self):
        self.x, self.y = 60, 845
        self.frame = 0
        self.image = load_image('hp.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h

    def draw(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,
                             self.frame_width, self.frame_height,
                             self.x, self.y, 70, 50)

# 숫자 표시 클래스
class Num:
    def __init__(self):
        self.x, self.y = 130, 83
        self.frame = 0
        self.image = load_image('num.png')
        self.frame_width = self.image.w // 9
        self.frame_height = self.image.h

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,
                             self.frame_width, self.frame_height,
                             self.x, self.y, 50, 50)

# 충돌 체크 함수
def check_collision(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

# 고래 클래스
class Whale:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 400
        self.frame = 0
        self.direction = 1
        self.image = load_image('whale.png')
        self.frame_width = self.image.w // 2
        self.frame_height = self.image.h // 4
        self.is_colliding = False
        self.collision_time = 0

    def update(self):
        global dir_x, dir_y
        current_time = time.time()

        if self.is_colliding and current_time - self.collision_time >= 0.1:
            self.is_colliding = False
            self.frame = 0

        if not self.is_colliding:
            self.frame = (self.frame + 1) % 2
        self.x += dir_x * 20
        self.y += dir_y * 20

        self.x = max(50, min(self.x, BK_WIDTH - 50))
        self.y = max(230, min(self.y, BK_HEIGHT - 100))

        if dir_x != 0:
            self.direction = dir_x

    def draw(self):
        if self.is_colliding:
            if self.direction == -1:
                self.image.clip_draw(0, 2 * self.frame_height, self.frame_width, self.frame_height,
                                     self.x, self.y, 100, 100)
            else:
                self.image.clip_composite_draw(0, 2 * self.frame_height, self.frame_width, self.frame_height,
                                               0, 'h', self.x, self.y, 100, 100)
        else:
            if self.direction == -1:
                self.image.clip_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height,
                                     self.x, self.y, 100, 100)
            else:
                self.image.clip_composite_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height,
                                               0, 'h', self.x, self.y, 100, 100)
        draw_rectangle_debug(*self.get_bb())

    def get_bb(self):
        if self.direction == -1:
            return self.x - 50, self.y - 20, self.x + 40, self.y + 20
        else:
            return self.x - 40, self.y - 20, self.x + 50, self.y + 20

# Fish1 클래스
class Fish1:
    def __init__(self):
        self.x, self.y = -20, random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('fish1.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h

    def update(self):
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,
                             self.frame_width, self.frame_height,
                             self.x, self.y, 20, 20)
        draw_rectangle_debug(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

# Crab 클래스
class Crab:
    def __init__(self):
        self.x, self.y = -20, random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('crab.png')
        self.frame_width = self.image.w // 3
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 3
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,
                             self.frame_width, self.frame_height,
                             self.x, self.y, 40, 40)
        draw_rectangle_debug(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

# Fish1 스폰 함수
def spawn_fish1():
    global fish1_list
    count = random.randint(1, 3)
    for _ in range(count):
        fish1_list.append(Fish1())

# Crab 스폰 함수
def spawn_crab():
    global crab_list
    count = random.randint(1, 3)
    for _ in range(count):
        crab_list.append(Crab())

# 이벤트 처리 함수
def handle_events():
    global swimming, dir_x, dir_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            swimming = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
            elif event.key == SDLK_ESCAPE:
                swimming = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1

# 초기화 함수
def reset_world():
    global swimming, background, level, num, whale, hp
    swimming = True
    background = BackGround()
    num = Num()
    hp = Hp()
    level = Level()
    whale = Whale()

# 월드 업데이트 함수
def update_world():
    global last_spawn_time, fish1_cnt
    current_time = time.time()

    if current_time - last_spawn_time >= 5.0:
        spawn_fish1()
        if fish1_cnt >= 10:  # Fish1을 10개 먹었을 때부터 Crab 생성
            spawn_crab()
        last_spawn_time = current_time

    whale.update()
    for fish in fish1_list[:]:
        fish.update()
        if check_collision(whale, fish):
            whale.is_colliding = True
            fish1_cnt += 1
            whale.collision_time = time.time()
            fish1_list.remove(fish)
        elif fish.x < -50 or fish.x > BK_WIDTH + 50:
            fish1_list.remove(fish)

    for crab in crab_list[:]:
        crab.update()
        if check_collision(whale, crab):
            whale.is_colliding = True
            whale.collision_time = time.time()
            crab_list.remove(crab)
        elif crab.x < -50 or crab.x > BK_WIDTH + 50:
            crab_list.remove(crab)

# 월드 렌더링 함수
def render_world():
    clear_canvas()
    background.draw()
    hp.draw()
    num.draw()
    level.draw()
    for fish in fish1_list:
        fish.draw()
    for crab in crab_list:
        crab.draw()
    whale.draw()
    update_canvas()

# 초기화 및 게임 루프
reset_world()

swimming = True
while swimming:
    handle_events()
    update_world()
    render_world()
    delay(0.07)

close_canvas()
