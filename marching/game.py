import pygame


class Game:
    window_width: int = 100
    window_height: int = 100
    target_framerate: int = 60

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.last_dt = 0

    def on_event(self, event: pygame.event.Event): ...
    def on_draw(self, out: pygame.Surface): ...
    def on_update(self, dt: float): ...

    def start(self):
        running = True

        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.on_event(event=event)

            dt = clock.tick(self.target_framerate) / 1000

            self.on_update(dt=dt)
            self.on_draw(out=self.screen)
            pygame.display.flip()

            self.last_dt = dt
