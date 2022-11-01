import pico2d
import game_framework

import arena_state

state_chk = 0

state = [
    arena_state
    ]


pico2d.open_canvas(1270,720)
game_framework.run(state[0])
pico2d.close_canvas()