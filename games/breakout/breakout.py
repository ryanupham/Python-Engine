import pyglet
from pyglet.window import key

import engine.game
import engine.spatial
from engine.entity import EntityModel, Entity
from engine.events import EventManager, InputType
from engine.time import LocalTimeline


def ball_brick_collision_handler(self, other):
    self.position.y_vel *= -1
    other.destroy()


def ball_paddle_collision_handler(self, other):
    self.position.y_vel *= -1
    self.position.y = other.height


def ball_step_handler(self):
    if self.y <= 0:
        global lives
        lives -= 1

        if lives < 0:
            pass
        else:
            self.position.x = (width - self.width) / 2
            self.position.y = (height - self.height) / 2

            self.position.x_vel = 2
            self.position.y_vel = 5
    elif self.y + self.height > height:
        self.position.y_vel *= -1

    if self.x <= 0 or self.x + self.width >= width:
        self.position.x_vel *= -1


def paddle_a_down_handler(self):
    self.position.x_vel = -7


def paddle_d_down_handler(self):
    self.position.x_vel = 7


def paddle_a_up_handler(self):
    if self.position.x_vel == -7:
        self.position.x_vel = 0


def paddle_d_up_handler(self):
    if self.position.x_vel == 7:
        self.position.x_vel = 0


def paddle_p_down_handler(self):
    if game_timeline.paused:
        game_timeline.resume()
    else:
        game_timeline.pause()


def paddle_step_handler(self):
    if self.position.x < 0:
        self.position.x = 0
        self.position.x_vel = 0
    elif self.position.x + self.width > width:
        self.position.x = width - self.width
        self.position.x_vel = 0


game = engine.game.Game
pyglet.resource.path = ["../breakout/resources"]

bg_color = (255/255, 248/255, 231/255)
width=1280
height=768
game_timeline = LocalTimeline()

lives = 3

ball_sprite = pyglet.sprite.Sprite(pyglet.resource.image("ball.png"))
brick_sprite = pyglet.sprite.Sprite(pyglet.resource.image("brick.png"))
paddle_sprite = pyglet.sprite.Sprite(pyglet.resource.image("paddle.png"))

ball_model = EntityModel("ball", sprite=ball_sprite, timeline=game_timeline)
brick_model = EntityModel("brick", sprite=brick_sprite, timeline=game_timeline)
paddle_model = EntityModel("paddle", sprite=paddle_sprite, timeline=game_timeline)

ball_model.add_collision_script(ball_brick_collision_handler, brick_model.name)
ball_model.add_collision_script(ball_paddle_collision_handler, paddle_model.name)
ball_model.add_step_script(ball_step_handler)
paddle_model.add_input_script(paddle_a_down_handler, InputType.KEY_DOWN, key.A)
paddle_model.add_input_script(paddle_d_down_handler, InputType.KEY_DOWN, key.D)
paddle_model.add_input_script(paddle_a_up_handler, InputType.KEY_UP, key.A)
paddle_model.add_input_script(paddle_d_up_handler, InputType.KEY_UP, key.D)
paddle_model.add_input_script(paddle_p_down_handler, InputType.KEY_DOWN, key.P)
paddle_model.add_step_script(paddle_step_handler)

game.initialize(width, height, bg_color)

game.add_entity(Entity(model=ball_model), engine.spatial.Position(100, 100, 2, 5))
game.add_entity(Entity(model=paddle_model), engine.spatial.Position((width - paddle_sprite.width) / 2, 0))

for x in range(10):
    for y in range(5):
        game.add_entity(Entity(model=brick_model), engine.spatial.Position(x * brick_sprite.width,
                                                                           height - ((y + 1) * brick_sprite.height)))

game.start()

