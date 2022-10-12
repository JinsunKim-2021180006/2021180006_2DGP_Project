import pico2d

import game_framework
import loby_state
import arena_state
import character_move

state = [
    loby_state,
    arena_state,
    character_move
    ]


pico2d.open_canvas(1270,720)
game_framework.run(state[0])
pico2d.close_canvas()