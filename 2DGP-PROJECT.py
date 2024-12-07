from PyInstaller.log import level
from pico2d import *
import random
import time
from pico2d import load_font
# 화면 크기
BK_WIDTH, BK_HEIGHT = 1080, 879
# 이동 방향 초기화
dir_x, dir_y = 0, 0  # x축, y축 이동 방향 (왼쪽: -1, 오른쪽: 1)
# 캔버스 생성
open_canvas(BK_WIDTH, BK_HEIGHT)
# 객체 리스트 초기화
fish1_list = []
crab_list = []
fish2_list = []
fish3_list = []
squid_list = []
shark_list =[]
# 초기 시간
last_spawn_time = time.time()
fish1_cnt = 0  # Fish1을 먹은 개수
crab_cnt = 0
fish2_cnt =0
fish3_cnt =0
squid_cnt =0
level1_cnt=1
level2_cnt=1
level3_cnt=1
level4_cnt=1
current_level=1
# 디버깅 모드 설정
DEBUG_MODE = True
# 디버그용 충돌 박스 그리기 함수
def draw_rectangle_debug(*args):
    if DEBUG_MODE:
        draw_rectangle(*args)
# 배경 클래스
class BackGround:
    def __init__(self):
        self.image = load_image('BackGround.PNG')

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
class HpBar:
    def __init__(self):
        self.x, self.y = 230, 845
        self.hp = 100
        self.max_width = 250
        self.image = load_image('hpbar.png')

    def decrease_hp(self, amount):
        self.hp = max(0, self.hp - amount)

    def draw(self):
        current_width = int(self.max_width * (self.hp / 100))
        self.image.clip_draw(0, 0, current_width, self.image.h,
                             self.x - (self.max_width - current_width) // 2, self.y,
                             current_width, 40)
# 숫자 표시 클래스
class Num:
    def __init__(self):
        self.x, self.y = 130, 83
        self.frame = 0
        self.image = load_image('num.png')
        self.frame_width = self.image.w // 9
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 9

    def draw(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,
                             self.frame_width, self.frame_height,
                             self.x, self.y, 50, 50)
class Count:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 20)
        self.x, self.y = 100, 50
        self.fish1_image = load_image('fish1.png')
        self.crab_image = load_image('crab.png')
        self.fish2_image = load_image('fish2.png')
        self.fish3_image = load_image('fish3.png')
        self.squid_image = load_image('squid.png')

        self.crab_frame = 0
        self.crab_frame_width = self.crab_image.w // 3
        self.crab_frame_height = self.crab_image.h

        self.fish3_frame = 0
        self.fish3_frame_width = self.fish3_image.w // 5
        self.fish3_frame_height = self.fish3_image.h

        self.squid_frame = 0
        self.squid_frame_width = self.squid_image.w // 5
        self.squid_frame_height = self.squid_image.h

    def update(self):
        self.crab_frame = (self.crab_frame + 1) % 3
        self.fish3_frame = (self.fish3_frame + 1) % 5
        self.squid_frame = (self.squid_frame + 1) % 5

    def draw(self, fish1_cnt, crab_cnt, fish2_cnt, fish3_cnt, squid_cnt,current_level):
        self.font.draw(self.x+180, self.y + 70, f'Fish1: {fish1_cnt}', (255, 255, 255))
        self.font.draw(self.x+330, self.y + 70, f'Crab: {crab_cnt}', (255, 255, 255))
        self.font.draw(self.x+480, self.y + 70, f'Fish2: {fish2_cnt}', (255, 255, 255))
        self.font.draw(self.x+630, self.y + 70, f'Fish3: {fish3_cnt}', (255, 255, 255))
        self.font.draw(self.x+780, self.y + 70, f'Squid: {squid_cnt}', (255, 255, 255))

        self.fish1_image.draw(self.x + 220, self.y + 20, 40, 40)
        if current_level>=2:
            self.crab_image.clip_draw(self.crab_frame * self.crab_frame_width, 0,
                                      self.crab_frame_width, self.crab_frame_height,
                                      self.x + 370, self.y + 20, 50, 50)
        if current_level >= 3:
            self.fish2_image.draw(self.x + 520, self.y + 20, 50, 50)
        if current_level >= 4:
            self.fish3_image.clip_draw(self.fish3_frame * self.fish3_frame_width, 0,
                                       self.fish3_frame_width, self.fish3_frame_height,
                                       self.x + 670, self.y + 20, 70, 70)
        if current_level >= 5:
            self.squid_image.clip_draw(self.squid_frame * self.squid_frame_width, 0,
                                       self.squid_frame_width, self.squid_frame_height,
                                       self.x + 820, self.y + 20, 70, 70)
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
        self.scale = 1.0
        self.invincible = False
        self.invincible_start_time = 0

    def update(self):
        global dir_x, dir_y
        current_time = time.time()

        if self.invincible and current_time - self.invincible_start_time > 2.0:
            self.invincible = False

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
        draw_width = self.frame_width * self.scale
        draw_height = self.frame_height * self.scale

        if self.is_colliding:
            if self.direction == -1:
                self.image.clip_draw(0, 2 * self.frame_height, self.frame_width, self.frame_height,
                                     self.x, self.y, draw_width, draw_height)
            else:
                self.image.clip_composite_draw(0, 2 * self.frame_height, self.frame_width, self.frame_height,
                                               0, 'h', self.x, self.y, draw_width, draw_height)
        else:
            if self.direction == -1:
                self.image.clip_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height,
                                     self.x, self.y, draw_width, draw_height)
            else:
                self.image.clip_composite_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height,
                                               0, 'h', self.x, self.y, draw_width, draw_height)
        draw_rectangle_debug(*self.get_bb())


    def get_bb(self):
        width_offset = 40 * self.scale
        width_offset2 = 50 * self.scale
        height_offset = 15 * self.scale

        if self.direction == -1:
            return self.x - width_offset2, self.y - height_offset, self.x + width_offset, self.y + height_offset
        else:
            return self.x - width_offset, self.y - height_offset, self.x + width_offset2, self.y + height_offset

    def size_up(self, scale_increment):
        self.scale += scale_increment
class Shark:
    def __init__(self):
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.x = -20
        else:
            self.x = BK_WIDTH + 20
        self.y = random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.image = load_image('shark.png')
        self.frame_width = self.image.w // 2
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 2  # 프레임 수는 스프라이트 가로 프레임 수에 맞추세요
        self.x += 10 * self.direction

    def draw(self):
        if self.direction == 1:
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 200, 150)
        else:
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 200, 150)
        draw_rectangle_debug(*self.get_bb())

    def get_bb(self):

        if self.direction == -1:
            return self.x - 90, self.y - 50, self.x + 90, self.y + 30
        else:
            return self.x - 90, self.y - 50, self.x + 90, self.y + 30
# Fish1 클래스
class Fish1:
    def __init__(self):
        self.direction = random.choice([-1, 1])
        if self.direction == -1:
            self.x = -20
        else:
            self.x = BK_WIDTH + 20
        self.y = random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('fish1.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h

    def update(self):
        self.x += 5* self.direction

    def draw(self):
        if self.direction == -1:
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 20, 20)
        else:
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 20, 20)
        draw_rectangle_debug(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
# Crab 클래스
class Crab:
    def __init__(self):
        self.direction = random.choice([-1, 1])
        if self.direction == -1:
            self.x = -20
        else:
            self.x = BK_WIDTH + 20
        self.y = random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.image = load_image('crab.png')
        self.frame_width = self.image.w // 3
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 3
        self.x += 5 * self.direction

    def draw(self):
        if self.direction == -1:
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 40, 40)
        else:
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 40, 40)
        draw_rectangle_debug(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15
class Fish2:
    def __init__(self):
        self.direction = random.choice([-1, 1])
        if self.direction == -1:
            self.x = -20
        else:
            self.x = BK_WIDTH + 20
        self.y = random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = 1
        self.image = load_image('fish2.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h
    def update(self):
        self.x += 5 * self.direction
    def draw(self):
        if self.direction == 1:
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 50, 50)
        else:
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
class Fish3:
    def __init__(self):
        self.direction = random.choice([-1, 1])
        if self.direction == -1:
            self.x = -20
        else:
            self.x = BK_WIDTH + 20
        self.y = random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('fish3.png')
        self.frame_width = self.image.w // 5  # 스프라이트 가로 분할
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 5  # 프레임 수는 스프라이트 가로 프레임 수에 맞추세요
        self.x += 5 * self.direction

    def draw(self):
        if self.direction == 1:
            draw_rectangle(*self.get_bb())
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 90, 90)  # 크기 조정
        else:
            draw_rectangle(*self.get_bb())
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 80, 80)
    def get_bb(self):
        return self.x - 30, self.y - 20, self.x + 40, self.y + 10
class Squid:
    def __init__(self):
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.x = -20
        else:
            self.x = BK_WIDTH + 20
        self.y = random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('squid.png')
        self.frame_width = self.image.w // 5  # 스프라이트 가로 분할
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 5  # 프레임 수는 스프라이트 가로 프레임 수에 맞추세요
        self.x += 5 * self.direction

    def draw(self):
        if self.direction == -1:
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 150, 150)
            draw_rectangle(*self.get_bb())
        else:
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,self.frame_width, self.frame_height,0, 'h', self.x, self.y, 150, 150)
            draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 5, self.y - 45, self.x + 40, self.y + 60
count = Count()
# Fish1 스폰 함수
def spawn_fish1():
    global fish1_list
    count = random.randint(1, 3)
    for _ in range(count):
        fish = Fish1()
        fish.direction = random.choice([-1, 1])
        fish1_list.append(fish)
# Crab 스폰 함수
def spawn_crab():
    global crab_list
    count = random.randint(1, 3)
    for _ in range(count):
        crab = Crab()
        crab.direction = random.choice([-1, 1])
        crab_list.append(crab)
# Fish2를 생성하는 함수
def spawn_fish2():
    global fish2_list
    count = random.randint(1, 3)
    fish2 = Fish2()
    fish2.direction = random.choice([-1, 1])
    for _ in range(count):
        fish2_list.append(fish2)
# Fish3를 생성하는 함수
def spawn_fish3():
    global fish3_list
    count = random.randint(1, 3)
    fish3 = Fish3()
    fish3.direction = random.choice([-1, 1])
    for _ in range(count):
        fish3_list.append(fish3)
def spawn_squid():
    global squid_list
    count = random.randint(1, 3)
    squid = Squid()
    squid.direction = random.choice([-1, 1])
    for _ in range(count):
        squid_list.append(squid)
def spawn_shark():
    global shark_list
    count = random.randint(1, 2)
    for _ in range(count):
        shark = Shark()
        shark_list.append(shark)
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
    global swimming, background, level, num, whale, hp,hpbar
    swimming = True
    background = BackGround()
    num = Num()
    hp = Hp()
    level = Level()
    whale = Whale()
    hpbar = HpBar()
# 월드 업데이트 함수
def update_world():
    global last_spawn_time, fish1_cnt,crab_cnt,fish2_cnt,fish3_cnt,squid_cnt,swimming,current_level

    current_time = time.time()
    for crab in crab_list[:]:
        if check_collision(whale, crab):
            if not whale.invincible:
                if current_level<2:
                    hpbar.decrease_hp(10)
                    whale.invincible = True
                    whale.invincible_start_time = current_time
            else:
                crab.update()
    for fish2 in fish2_list[:]:
        if check_collision(whale, fish2):
            if not whale.invincible:
                if current_level<3:
                    hpbar.decrease_hp(10)
                    whale.invincible = True
                    whale.invincible_start_time = current_time
            else:
                fish2.update()
    for fish3 in fish3_list[:]:
        if check_collision(whale, fish3):
            if not whale.invincible:
                if current_level<4:
                    hpbar.decrease_hp(10)
                    whale.invincible = True
                    whale.invincible_start_time = current_time
            else:
                fish3.update()
    for squid in squid_list[:]:
        if check_collision(whale, squid):
            if not whale.invincible:
                if current_level<5:  # 상위 단계 조건 확인
                    hpbar.decrease_hp(10)
                    whale.invincible = True
                    whale.invincible_start_time = current_time
            else:
                squid.update()
    for shark in shark_list[:]:
        if check_collision(whale, shark):
            if not whale.invincible:
                hpbar.decrease_hp(20)
                whale.invincible = True
                whale.invincible_start_time = current_time
            else:
                shark.update()
    if current_time - last_spawn_time >= 3.0:
        spawn_fish1()
        spawn_crab()

        if current_level>=2:
            spawn_fish2()
        if current_level>=3:
            spawn_fish3()
        if current_level>=4:
            spawn_squid()
        if current_level >= 5:
            spawn_shark()
        last_spawn_time = current_time
    whale.update()
    for fish in fish1_list[:]:
        fish.update()
        if check_collision(whale, fish):
            whale.is_colliding = True
            fish1_cnt += 1
            if(fish1_cnt == level1_cnt):
                current_level=2
                num.update()
                whale.size_up(0.25)
            whale.collision_time = time.time()
            fish1_list.remove(fish)
        elif fish.x < -50 or fish.x > BK_WIDTH + 50:
            fish1_list.remove(fish)
    for crab in crab_list[:]:
        crab.update()
        if check_collision(whale, crab):
            if current_level >= 2:
                whale.is_colliding = True

                if (crab_cnt == level2_cnt):
                    num.update()
                    whale.size_up(0.25)
                    current_level = 3
                crab_cnt += 1
                whale.collision_time = time.time()
                crab_list.remove(crab)
            elif crab.x < -50 or crab.x > BK_WIDTH + 50:
                crab_list.remove(crab)
    for fish2 in fish2_list[:]:
        fish2.update()
        if check_collision(whale, fish2):
            if current_level >= 3:
                whale.is_colliding = True
                if (fish2_cnt == level3_cnt):
                    num.update()
                    whale.size_up(0.25)
                    current_level = 4
                fish2_cnt += 1
                whale.collision_time = time.time()
                fish2_list.remove(fish2)
        elif fish2.x < -50 or fish2.x > BK_WIDTH + 50:
            fish2_list.remove(fish2)
    for fish3 in fish3_list[:]:
        fish3.update()
        if check_collision(whale, fish3):
            if current_level >= 4:
                whale.is_colliding = True
                if (fish3_cnt == level4_cnt):
                    num.update()
                    whale.size_up(0.25)
                    current_level = 5
                fish3_cnt += 1
                whale.collision_time = time.time()
                fish3_list.remove(fish3)
        elif fish3.x < -50 or fish3.x > BK_WIDTH + 50:
            fish3_list.remove(fish3)
    for squid in squid_list[:]:
        squid.update()
        if check_collision(whale, squid):
            if current_level >= 5:
                whale.is_colliding = True
                squid_cnt += 1
                if (squid_cnt == 1):
                    num.update()
                    whale.size_up(0.25)
                    current_level = 5
                whale.collision_time = time.time()
                squid_list.remove(squid)
        elif squid.x < -50 or squid.x > BK_WIDTH + 50:
            squid_list.remove(squid)
    for shark in shark_list[:]:
        shark.update()
        if shark.x < -100 or shark.x > BK_WIDTH + 100:
            shark_list.remove(shark)

# 월드 렌더링 함수
def render_world():
    clear_canvas()
    background.draw()
    hp.draw()
    hpbar.draw()
    num.draw()
    level.draw()
    for fish in fish1_list:
        fish.draw()
    for crab in crab_list:
        crab.draw()
    for fish2 in fish2_list:
        fish2.draw()
    for fish3 in fish3_list:
        fish3.draw()
    for squid in squid_list:
        squid.draw()
    for shark in shark_list:
        shark.draw()
    whale.draw()
    count.draw(fish1_cnt, crab_cnt, fish2_cnt, fish3_cnt, squid_cnt,current_level)
    if not swimming:
        font = load_font('ENCR10B.TTF', 50)
        font.draw(BK_WIDTH // 2 - 150, BK_HEIGHT // 2, 'GAME OVER', (255, 0, 0))

    update_canvas()
# 초기화 및 게임 루프
reset_world()
swimming = True
while swimming:
    handle_events()
    update_world()
    count.update()
    render_world()
    delay(0.07)
close_canvas()
