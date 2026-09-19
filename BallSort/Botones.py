import pygame
from pathlib import Path

class Boton:
    def __init__(self, image_path, sound_path=None, position=(0, 0), scale=1.0):
        image_path = Path(image_path)
        if sound_path:
            sound_path = Path(sound_path)

        self.image = pygame.image.load(str(image_path)).convert_alpha()
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        self.image = pygame.transform.smoothscale(self.image, (new_width, new_height))
        
        self.sound = None
        if sound_path and sound_path.exists():
            try:
                self.sound = pygame.mixer.Sound(str(sound_path))
            except Exception:
                self.sound = None

        self.rect = self.image.get_rect(topleft=position)
        self.pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def es_presionado(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed and not self.pressed:
                self.pressed = True
                if self.sound:
                    self.sound.play()
                return True
            if not mouse_pressed:
                self.pressed = False
            return False
        return False