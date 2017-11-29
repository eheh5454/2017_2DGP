from pico2d import *
import game_framework
import Stage1


image = None
current_time = 0
space_to_start = None


class Space_to_start():
    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 3

    def __init__(self):
        self.total_frames = 0
        self.frame = 0
        self.total_frames = 0
        self.image = load_image('space_to_start.png')

    def update(self, frame_time):
        self.total_frames += self.ACTION_PER_TIME * self.FRAMES_PER_ACTION * frame_time
        self.frame = int(self.total_frames) % 3

    def draw(self):
        self.image.clip_draw(self.frame*500, 0, 500, 50, 400, 100)


def enter():
    global image, space_to_start
    open_canvas()
    image = load_image('title.png')
    space_to_start = Space_to_start()

def exit():
    global image, space_to_start
    del image
    del space_to_start
    close_canvas()


def update(frame_time):
    global current_time, space_to_start
    frame_time = get_time() - current_time
    space_to_start.update(frame_time)
    current_time += frame_time
    pass


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(400, 300)
    space_to_start.draw()
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.push_state(Stage1)


def pause(): pass


def resume(): pass

