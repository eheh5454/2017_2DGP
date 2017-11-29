from pico2d import *
import game_framework
import Stage1


image = None
space = None
font = None


def enter():
    global image, space, font
    image = load_image('game_over.png')
    space = load_image('Space.jpg')
    font = load_font('ENCR10B.TTF', 50)


def exit():
    global image, space, font
    del image
    del space
    del font


def update(frame_time):
    pass


def draw(frame_time):
    global image, space, Score
    clear_canvas()
    space.draw(400, 300)
    image.draw(400, 300)
    font.draw(200, 400, 'Your Score:%d' % Stage1.Score, (220, 220, 0))
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()


def pause():
    pass


def resume():
    pass