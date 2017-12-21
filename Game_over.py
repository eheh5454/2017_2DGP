from pico2d import *
import game_framework
import Stage


image = None
space = None
score_font = None
restart_font = None

def enter():
    global image, space, score_font, restart_font
    image = load_image('game_over.png')
    space = load_image('Space.jpg')
    score_font = load_font('ENCR10B.TTF', 50)
    restart_font = load_font('YGD360.TTF', 70)


def exit():
    global image, space, score_font, restart_font
    del image
    del space
    del score_font
    del restart_font


def update(frame_time):
    pass


def draw(frame_time):
    global image, space, Score, restart_font
    clear_canvas()
    space.draw(400, 300)
    image.draw(400, 300)
    score_font.draw(200, 400, 'Your Score:%d' % Stage.Score, (220, 220, 0))
    restart_font.draw(50, 100, 'SPACE TO RESTART', (250, 250, 0))
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.pop_state()



def pause():
    pass


def resume():
    pass