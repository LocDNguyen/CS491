#MAIN CODE FROM Danny Barthaud AT https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
#MAIN CODE FROM Danny Barthaud AT https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
#MAIN CODE FROM Danny Barthaud AT https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html

from pygame.sprite import Sprite
import pygame.freetype


class UIPlain(Sprite):
    def __init__(self, center_position, text, font_size, text_rgb):

        self.mouse_over = False

        default_image = create_surface_with_text(text=text, font_size=font_size, text_rgb=text_rgb)
        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=text_rgb)

        self.images = [default_image, highlighted_image]
        self.rects = [default_image.get_rect(center=center_position), highlighted_image.get_rect(center=center_position)]

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, text_rgb, action=None):
        self.mouse_over = False

        default_image = create_surface_with_text(text=text, font_size=font_size, text_rgb=text_rgb)
        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=text_rgb)

        self.images = [default_image, highlighted_image]
        self.rects = [default_image.get_rect(center=center_position), highlighted_image.get_rect(center=center_position)]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def create_surface_with_text(text, font_size, text_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb)
    return surface.convert_alpha()

def draw_text(x, y, text, font_size, text_rgb, screen):
    font = pygame.font.SysFont('freesansbold.ttf', font_size)
    img = font.render(text, True, text_rgb)
    text_rect = img.get_rect(center=(x / 2, y))
    screen.blit(img, text_rect)