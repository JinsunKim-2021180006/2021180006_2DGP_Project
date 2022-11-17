import box
import game_framework
from pico2d import *
from random import randint

import item
import obj_maker
from collide import collide_check
import game_world

from ground import Ground
from box import BoxQuestion, Brick, Pipe, BluePipe

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

GRAVITY_MPS = -9.8
GRAVITY_PPS = (GRAVITY_MPS * PIXEL_PER_METER)

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP,\
    SHIFT_DOWN, SHIFT_UP,\
    SPACE, FALL_EVENT, LAND_I, LAND_W, LAND_R,\
    ENDING_EVENT = range(12)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP
}

# Boy States

class IdleState:

    def enter(boy, event):
        pass

    def exit(boy, event):
        if event == SPACE:
            boy.air_move = False

        if event == SHIFT_DOWN:
            boy.running = True

        if event == SHIFT_UP:
            boy.running = False

    def do(boy):
        # 땅이 없으면 떨어진다
        col = False

        for o in game_world.all_objects():
            if o.__class__ == Ground\
                    or o.__class__ == BoxQuestion\
                    or o.__class__ == Brick\
                    or o.__class__ == Pipe\
                    or o.__class__ == BluePipe:
                if collide_check(boy, o) == "bottom":
                    col = True
                    break

        if not col:
            boy.add_event(FALL_EVENT)


    def draw(boy):
        boy.image.clip_draw(0, boy.imageHeight * 6, 32, boy.imageHeight, boy.x - boy.scroll, boy.y)


class WalkState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.dir = 1
        elif event == LEFT_DOWN:
            boy.dir = -1
        elif event == RIGHT_UP:
            boy.dir = -1
        elif event == LEFT_UP:
            boy.dir = 1

        boy.velocity = RUN_SPEED_PPS

    def exit(boy, event):
        if event == SPACE:
            boy.air_move = True

        if event == FALL_EVENT:
            boy.air_move = True

        if event == SHIFT_DOWN:
            boy.running = True

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        # 떨어지는거
        col = False
        for o in game_world.all_objects():
            if o.__class__ == Ground \
                    or o.__class__ == BoxQuestion \
                    or o.__class__ == Brick \
                    or o.__class__ == Pipe \
                    or o.__class__ == BluePipe:
                if collide_check(boy, o) == "bottom":
                    col = True
                    break

        if not col:
            boy.add_event(FALL_EVENT)

        # 걷는거
        boy.x += boy.dir * boy.velocity * game_framework.frame_time

    def draw(boy):
        boy.image.clip_draw(32 * int(boy.frame), boy.imageHeight * 5, 32, boy.imageHeight, boy.x - boy.scroll, boy.y)


class RunState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.dir = 1
        elif event == LEFT_DOWN:
            boy.dir = -1
        elif event == RIGHT_UP:
            boy.dir = -1
        elif event == LEFT_UP:
            boy.dir = 1

        boy.velocity = RUN_SPEED_PPS * 3

    def exit(boy, event):
        if event == SPACE:
            boy.air_move = True

        if event == FALL_EVENT:
            boy.air_move = True

        if event == SHIFT_UP:
            boy.running = False

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        boy.x += boy.dir * boy.velocity * game_framework.frame_time

        col = False
        for o in game_world.all_objects():
            if o.__class__ == Ground\
                    or o.__class__ == BoxQuestion\
                    or o.__class__ == Brick\
                    or o.__class__ == Pipe\
                    or o.__class__ == BluePipe:
                if collide_check(boy, o) == 'bottom':
                    col = True
                    break

        if not col:
            boy.add_event(FALL_EVENT)

    def draw(boy):
        boy.image.clip_draw(32 * int(boy.frame), boy.imageHeight * 4, 32, boy.imageHeight, boy.x - boy.scroll, boy.y)


class JumpState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.dir = 1
            boy.air_move = True
        elif event == LEFT_DOWN:
            boy.dir = -1
            boy.air_move = True
        elif event == RIGHT_UP:
            boy.dir = 1
            boy.air_move = False
        elif event == LEFT_UP:
            boy.dir = -1
            boy.air_move = False

        boy.velocity = RUN_SPEED_PPS

        if boy.jump_y == 0:
            boy.timer = 0
            boy.jump_y = boy.y

    def exit(boy, event):
        if event == FALL_EVENT:
            boy.jump_y = 0
            boy.timer = 0

        if event == SHIFT_DOWN:
            boy.running = True

        if event == SHIFT_UP:
            boy.running = False

    def do(boy):
        boy.timer += game_framework.frame_time
        boy.y = ((1 / 2) * GRAVITY_PPS * boy.timer + boy.velocity * 4) * boy.timer + boy.jump_y  # S

        vj = boy.velocity * 4 + GRAVITY_PPS * boy.timer  # v
        if vj <= 0:
            boy.add_event(FALL_EVENT)

        col = False
        for o in game_world.all_objects():
            if o.__class__ == Ground \
                    or o.__class__ == Pipe \
                    or o.__class__ == BluePipe:
                if collide_check(boy, o) == 'top':
                    boy.y = o.y - o.imageHeight/2 - boy.imageHeight/2
                    col = True
                    break
            elif o.__class__ == BoxQuestion:
                if collide_check(boy, o) == 'top':
                    boy.y = o.y - o.imageHeight/2 - boy.imageHeight/2
                    col = True
                    if not o.used:
                        o.used = True
                        o.image = load_image('box_used.png')
                        drop_item = randint(0, 3)
                        if drop_item == 0:
                            obj_maker.make_obj(o.x, o.y + o.imageHeight, obj_maker.ObjType.o_item_t, 'mush')
                        # elif drop_item == 1:
                        #     obj_maker.make_obj(o.x, o.y + o.imageHeight, obj_maker.ObjType.o_item_t, 'flower')
                        else:
                            obj_maker.make_obj(o.x, o.y + o.imageHeight, obj_maker.ObjType.o_item_c, 'effect')
                    break
            elif o.__class__ == Brick:
                if collide_check(boy, o) == 'top':
                    boy.y = o.y - o.imageHeight / 2 - boy.imageHeight / 2
                    col = True

                    if boy.trans >= 1:
                        game_world.remove_object(o)
                    break

        if col:
            boy.add_event(FALL_EVENT)

        # 점프하면서 움직이는거
        if boy.air_move:
            if boy.running:
                boy.x += boy.dir * (boy.velocity * 2) * game_framework.frame_time
            else:
                boy.x += boy.dir * (boy.velocity) * game_framework.frame_time


    def draw(boy):
        boy.image.clip_draw(0, boy.imageHeight * 3, 32, boy.imageHeight, boy.x - boy.scroll, boy.y)


class FallingState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.dir = 1
            boy.air_move = True
        elif event == LEFT_DOWN:
            boy.dir = -1
            boy.air_move = True
        elif event == RIGHT_UP:
            boy.dir = 1
            boy.air_move = False
        elif event == LEFT_UP:
            boy.dir = -1
            boy.air_move = False

        boy.velocity = RUN_SPEED_PPS

    def exit(boy, event):
        if event == SHIFT_DOWN:
            boy.running = True

        if event == SHIFT_UP:
            boy.running = False

    def do(boy):
        col = False
        for o in game_world.all_objects():
            if o.__class__ == Ground\
                    or o.__class__ == BoxQuestion\
                    or o.__class__ == Brick\
                    or o.__class__ == Pipe\
                    or o.__class__ == BluePipe:
                if collide_check(boy, o) == 'bottom':
                    boy.y = o.y + o.imageHeight / 2 + boy.imageHeight / 2
                    col = True
                    break

        if col:
            # 초기화
            boy.timer = 0

            boy.y = o.y + o.imageHeight / 2 + boy.imageHeight / 2
            if boy.air_move:
                if boy.running:
                    boy.add_event(LAND_R)
                else:
                    boy.add_event(LAND_W)
            else:
                boy.add_event(LAND_I)
        else:
            boy.timer += game_framework.frame_time
            vf = GRAVITY_PPS * boy.timer  # 속력
            boy.y += vf * game_framework.frame_time  # 거리

        # 떨어지면서 움직이는거
        if boy.air_move:
            if boy.running:
                boy.x += boy.dir * (boy.velocity * 2) * game_framework.frame_time
            else:
                boy.x += boy.dir * (boy.velocity) * game_framework.frame_time

    def draw(boy):
        boy.image.clip_draw(0, boy.imageHeight * 2, 32, boy.imageHeight, boy.x - boy.scroll, boy.y)


class GameClearState:

    def enter(boy, event):
        pass

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + 3 * game_framework.frame_time) % 6

        boy.timer -= 1
        print(boy.timer)
        if boy.frame >= 5.3:
            boy.frame = 5.3

            if boy.timer <= 0:
                boy.gameclear = True
        else:
            boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time


    def draw(boy):
        boy.image.clip_draw(32 * int(boy.frame), 0, 32, boy.imageHeight, boy.x - boy.scroll, boy.y)


next_state_table = {
    IdleState: {RIGHT_UP: WalkState, LEFT_UP: WalkState, RIGHT_DOWN: WalkState, LEFT_DOWN: WalkState,
                SHIFT_DOWN: IdleState, SHIFT_UP: IdleState,
                SPACE: JumpState, FALL_EVENT: IdleState, LAND_I: IdleState, LAND_W: IdleState, LAND_R: IdleState,
                ENDING_EVENT: GameClearState},
    WalkState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                SHIFT_DOWN: RunState, SHIFT_UP: RunState,
                SPACE: JumpState, FALL_EVENT: FallingState, LAND_I: WalkState, LAND_W: WalkState, LAND_R: WalkState,
                ENDING_EVENT: GameClearState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                SHIFT_DOWN: WalkState, SHIFT_UP: WalkState,
                SPACE: JumpState, FALL_EVENT: FallingState, LAND_I: RunState, LAND_W: RunState, LAND_R: RunState,
                ENDING_EVENT: GameClearState},
    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState,
                SHIFT_DOWN: JumpState, SHIFT_UP: JumpState,
                SPACE: JumpState, FALL_EVENT: FallingState, LAND_I: JumpState, LAND_W: JumpState, LAND_R: JumpState,
                ENDING_EVENT: GameClearState},
    FallingState: {RIGHT_UP: FallingState, LEFT_UP: FallingState, RIGHT_DOWN: FallingState, LEFT_DOWN: FallingState,
                SHIFT_DOWN: FallingState, SHIFT_UP: FallingState,
                SPACE: FallingState, FALL_EVENT: IdleState, LAND_I: IdleState, LAND_W: WalkState, LAND_R: RunState,
                ENDING_EVENT: GameClearState},
    GameClearState: {RIGHT_UP: GameClearState, LEFT_UP: GameClearState, RIGHT_DOWN: GameClearState, LEFT_DOWN: GameClearState,
                SHIFT_DOWN: GameClearState, SHIFT_UP: GameClearState,
                SPACE: GameClearState, FALL_EVENT: GameClearState, LAND_I: GameClearState, LAND_W: GameClearState, LAND_R: GameClearState,
                ENDING_EVENT: GameClearState}
}


class Boy:
    def __init__(self):
        self.x, self.y = 32, 64
        self.scroll = 0
        self.imageWidth, self.imageHeight = 32, 32

        # 이미지
        self.trans = 0
        self.image = load_image('mario_base_l.png')
        self.image_l = load_image('mario_base_l.png')
        self.image_r = load_image('mario_base_r.png')
        self.image_sl = load_image('mario_super_l.png')
        self.image_sr = load_image('mario_super_r.png')

        self.font = load_font('ENCR10B.TTF', 16)

        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.gameclear = False
        # 달리기
        self.running = False

        # 점프
        self.timer = 0
        self.jump_y = 0
        self.air_move = False

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        self.JumpPPS = RUN_SPEED_PPS
        self.JumpDuring = 0.0
        self.JumpAccel = 0.0

        # 디버그
        self.show_font = False

    def get_bb(self):
        return self.x - self.imageWidth/2 - self.scroll, self.y - self.imageHeight/2,\
               self.x + self.imageWidth/2 - self.scroll, self.y + self.imageHeight/2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        # 충돌
        for o in game_world.all_objects():
            if o.__class__ == item.Transform:
                if collide_check(self, o):
                    if o.value == 'mush':
                        if self.trans < 1:
                            self.trans = 1  # 슈퍼마리오
                            self.imageHeight = 64
                    elif o.value == 'flower':
                        if self.trans < 2:
                            print('(임시) 파이어마리오')    # temp
                            # self.trans = 2  # 파이어마리오
                            # self.imageHeight = 64

                    game_world.remove_object(o)

            if o.__class__ == box.Flag:
                if not collide_check(self, o) == None:
                    if not self.cur_state == GameClearState:
                        self.timer = 1300
                        self.add_event(ENDING_EVENT)

        # 이미지 업데이트
        if self.dir == -1:
            if self.trans == 0:
                self.image = self.image_l
            elif self.trans == 1:
                self.image = self.image_sl
        else:
            if self.trans == 0:
                self.image = self.image_r
            elif self.trans == 1:
                self.image = self.image_sr


    def draw(self):
        self.cur_state.draw(self)

        # 디버그
        if self.show_font:
            # 현재 위치
            self.font.draw(self.x - 60 - self.scroll, self.y + 90, 'Pos: ' + str((int(self.x), int(self.y))), (0, 0, 255))
            # 스크롤 상태
            self.font.draw(self.x - 60 - self.scroll, self.y + 70, 'Scroll: ' + str(self.scroll), (255, 0, 255))
            # 현재 상태
            self.font.draw(self.x - 60 - self.scroll, self.y + 50, str(self.cur_state), (255, 255, 0))

        # 바운딩박스
        draw_rectangle(self.x - self.imageWidth/2 - self.scroll, self.y - self.imageHeight/2,\
               self.x + self.imageWidth/2 - self.scroll, self.y + self.imageHeight/2)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            if not self.show_font:
                self.show_font = True
            else:
                self.show_font = False