from pico2d import *
import random
import time

BK_WIDTH, BK_HEIGHT = 1080, 879
dir_x = 0  # x축 이동 방향 (왼쪽: -1, 오른쪽: 1)
dir_y = 0  # y축 이동 방향 (아래: -1, 위: 1)
open_canvas(BK_WIDTH, BK_HEIGHT)

fish1_list = []
last_spawn_time = time.time()

# 배경 클래스
class BackGround:
    def __init__(self):
        self.image = load_image('BackGround.JPG')
    def update(self):
        pass
    def draw(self):
        self.image.draw(BK_WIDTH // 2, BK_HEIGHT // 2)
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
        self.image.clip_draw(self.frame * self.frame_width, 0,self.frame_width, self.frame_height,self.x, self.y, 150, 70)
class Hp:
    def __init__(self):
        self.x, self.y = 60, 845
        self.frame = 0
        self.image = load_image('hp.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h
    def draw(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,self.frame_width, self.frame_height,self.x, self.y, 70, 50)

class Num:
    def __init__(self):
        self.x, self.y = 130, 83
        self.frame = 0
        self.image = load_image('num.png')
        self.frame_width = self.image.w // 9
        self.frame_height = self.image.h

    def update(self):
        pass
        #self.frame = (self.frame + 1) % 9

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
        self.direction = 1  # 1이면 오른쪽, -1이면 왼쪽
        self.image = load_image('whale.png')
        self.frame_width = self.image.w // 2  # 가로 프레임 2개
        self.frame_height = self.image.h // 4  # 세로 프레임 4개
        self.is_colliding = False  # 충돌 상태를 나타내는 변수
        self.collision_time = 0  # 충돌 발생 시간을 기록

    def update(self):
        global dir_x, dir_y
        current_time = time.time()

        # 충돌 상태에서 1초 경과 시 초기화
        if self.is_colliding and current_time - self.collision_time >= 0.1:
            self.is_colliding = False  # 충돌 상태 해제
            self.frame = 0  # 첫 번째 줄 애니메이션 초기화

        if not self.is_colliding:  # 충돌 상태가 아닐 때만 기본 프레임 애니메이션
            self.frame = (self.frame + 1) % 2
        self.x += dir_x * 20  # x축 방향 이동
        self.y += dir_y * 20  # y축 방향 이동

        # 화면 밖으로 나가지 않도록 위치 제한
        if self.x < 50:
            self.x = 50
        elif self.x > BK_WIDTH - 50:
            self.x = BK_WIDTH - 50
        if self.y < 230:
            self.y = 230
        elif self.y > BK_HEIGHT - 100:
            self.y = BK_HEIGHT - 100
        if dir_x != 0:
            self.direction = dir_x

    def draw(self):
        if self.is_colliding:  # 충돌 상태일 때는 두 번째 줄의 첫 번째 프레임 사용
            if self.direction == -1:
                self.image.clip_draw(0, 2 * self.frame_height, self.frame_width, self.frame_height,
                                     self.x, self.y, 100, 100)
            else:
                self.image.clip_composite_draw(0, 2 * self.frame_height, self.frame_width, self.frame_height,
                                               0, 'h', self.x, self.y, 100, 100)
        else:  # 일반 상태
            if self.direction == -1:
                self.image.clip_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height,
                                     self.x, self.y, 100, 100)
            else:
                self.image.clip_composite_draw(self.frame * self.frame_width, 3 * self.frame_height, self.frame_width, self.frame_height,
                                               0, 'h', self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.direction == -1:  # 왼쪽 방향
            return self.x - 50, self.y - 20, self.x + 40, self.y + 20
        else:  # 오른쪽 방향
            return self.x - 40, self.y - 20, self.x + 50, self.y + 20
class Squid:
    def __init__(self):
        self.x, self.y = -20, random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('squid.png')
        self.frame_width = self.image.w // 5  # 스프라이트 가로 분할
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 5  # 프레임 수는 스프라이트 가로 프레임 수에 맞추세요
        self.x += 5

    def draw(self):
        if self.direction == -1:
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 150, 150)  # 크기 조정
            draw_rectangle(*self.get_bb())
        else:
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,self.frame_width, self.frame_height,0, 'h', self.x, self.y, 150, 150)
            draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 5, self.y - 45, self.x + 40, self.y + 60
class Fish1:
    def __init__(self):
        self.x, self.y = -20, random.randint(230, BK_HEIGHT - 100)
        self.bx,self.by=350,80
        self.frame = 0
        self.direction = -1
        self.image = load_image('fish1.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h

    def update(self):
        self.x += 5

    def draw(self):
        if self.direction == -1:
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 20, 20)  # 크기 조정
            draw_rectangle(*self.get_bb())
        else:
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 20, 20)
            draw_rectangle(*self.get_bb())

    def drawB(self):
        self.image.clip_draw(self.frame * self.frame_width, 0,
                             self.frame_width, self.frame_height,
                             self.bx, self.by, 20, 20)
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
class Fish2:
    def __init__(self):
        self.x, self.y = -20, random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('fish2.png')
        self.frame_width = self.image.w
        self.frame_height = self.image.h

    def update(self):
        self.x += 5

    def draw(self):
        if self.direction == -1:
            draw_rectangle(*self.get_bb())
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 50, 50)  # 크기 조정
        else:
            draw_rectangle(*self.get_bb())
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 50, 50)
    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
class Fish3:
    def __init__(self):
        self.x, self.y = -20, random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('fish3.png')
        self.frame_width = self.image.w // 5  # 스프라이트 가로 분할
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 5  # 프레임 수는 스프라이트 가로 프레임 수에 맞추세요
        self.x += 5

    def draw(self):
        if self.direction == -1:
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
class Crab:
    def __init__(self):
        self.x, self.y = -20, random.randint(230, BK_HEIGHT - 100)
        self.frame = 0
        self.direction = -1
        self.image = load_image('crab.png')
        self.frame_width = self.image.w // 3  # 스프라이트 가로 분할
        self.frame_height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 3  # 프레임 수는 스프라이트 가로 프레임 수에 맞추세요
        self.x += 5

    def draw(self):
        if self.direction == -1:
            draw_rectangle(*self.get_bb())
            self.image.clip_draw(self.frame * self.frame_width, 0,
                                 self.frame_width, self.frame_height,
                                 self.x, self.y, 40, 40)  # 크기 조정
        else:
            draw_rectangle(*self.get_bb())
            self.image.clip_composite_draw(self.frame * self.frame_width, 0,
                                           self.frame_width, self.frame_height,
                                           0, 'h', self.x, self.y, 40, 40)
    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

def spawn_fish1():
    global fish1_list
    count = random.randint(1, 3)  # 2개 또는 3개 생성
    for _ in range(count):
        fish1_list.append(Fish1())
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
    global level
    global num
    global whale
    global squid
    global fish1
    global fish2
    global fish3
    global crab
    global hp
    swimming = True
    background = BackGround()
    num = Num()
    hp=Hp()
    level = Level()
    whale = Whale()
    squid = Squid()
    fish1=Fish1()
    fish2=Fish2()
    fish3=Fish3()
    crab = Crab()
# 월드 업데이트
def update_world():
    global last_spawn_time
    current_time = time.time()

    if current_time - last_spawn_time >= 5.0:
        spawn_fish1()
        last_spawn_time = current_time
    num.update()
    level.update()
    whale.update()
    crab.update()
    fish1.update()
    fish2.update()
    fish3.update()
    squid.update()
    for fish in fish1_list[:]:
        fish.update()
        if check_collision(whale, fish):  # Whale과 Fish1 충돌 체크
            whale.is_colliding = True
            whale.collision_time = time.time()
            fish1_list.remove(fish)  # 충돌한 Fish1 제거
        elif fish.x < -50 or fish.x > BK_WIDTH + 50:  # 화면 밖으로 나간 경우 제거
            fish1_list.remove(fish)

# 월드 렌더링
def render_world():
    clear_canvas()
    background.draw()
    hp.draw()
    num.draw()
    level.draw()
    fish1.drawB()
    for fish in fish1_list:
        fish.draw()
    fish2.draw()
    fish3.draw()
    squid.draw()
    crab.draw()
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
    delay(0.07)

# 종료 코드
close_canvas()
