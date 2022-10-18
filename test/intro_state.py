#인트로 페이지
#한국공대 로고

from pico2d import *
import game_framework
import start_state

logo_image = None
logo_time = 0.01

def enter():
    global logo_image, logo_time
    logo_time = 0.01
    logo_image = load_image('resource\\background_image_sprites\\tuk_credit.png')
    pass

def exit():
    global logo_image
    del logo_image
    pass

def update():
    global logo_time
    if logo_time>1.0:
        logo_time = 0
        game_framework.change_state(start_state)
    delay(0.01)
    logo_time+=0.02

    pass

def draw():
    clear_canvas()
    logo_image.draw(1270//2,720//2)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    pass


#단독 실행 코드
def test_self():
    import sys
    this_module = sys.modules['__main__']

    pico2d.open_canvas(1270,720)
    game_framework.run(this_module)
    pico2d.close_canvas()

if __name__ == '__main__': #만약 단독 실행 상태이면
    test_self()