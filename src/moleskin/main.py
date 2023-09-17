from typing import Tuple
import pygame
from moleskin.components.frame import Frame

TestState = Tuple
TestSelectedState = None
TestForm = Tuple


class TestFrame(Frame[TestState, TestSelectedState, TestForm]):
    def draw(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # write your pygame event and graphics code here

        pygame.display.flip()
        return True

    def state(self):
        return ()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    # TODO create a menu component type for the Fram
    TestFrame(None).loop(screen)
    pygame.quit()


if __name__ == '__main__':
    main()
