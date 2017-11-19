from pico2d import *
import game_framework
import Stage1

image = None
space = None

def enter():
    global image, space
    image = load_image('game_over.png')
    space = load_image('Space.jpg')


def exit():
    global image, space
    del image
    del space


def update():
    pass


def draw():
    global image, space
    clear_canvas()
    space.draw(400, 300)
    image.draw(400, 300)
    update_canvas()


def handle_events():
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