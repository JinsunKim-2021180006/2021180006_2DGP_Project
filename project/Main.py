import pico2d
import game_framework

import intro_state
import start_state
import play_state
import arena_state

state = [
    intro_state,
    start_state,
    play_state,
    arena_state
    ]

 
pico2d.open_canvas(1270,720)
game_framework.run(state[0])
pico2d.close_canvas()

