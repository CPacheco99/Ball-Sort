import pygame
from pathlib import Path
from Botones import Boton

class Menu:
    def __init__(self, screen, base_path):
        self.screen = screen
        self.base_path = base_path
        
        assets_dir = self.base_path / "assets"
        sound_dir = self.base_path / "Sonido"

        fondo_path = assets_dir / "Menu.png"
        if fondo_path.exists():
            self.fondo = pygame.image.load(str(fondo_path)).convert()
        else:
            self.fondo = None

        btn_jugar_path = assets_dir / "BotonJugar.png"
        btn_salir_path = assets_dir / "BotonSalirRojo.png"
        snd_click_path = sound_dir / "Click.mp3"
        snd_bg_path = sound_dir / "Sonidomenu.mp3"

        self.jugar = Boton(btn_jugar_path, snd_click_path, (550, 515), 0.1)
        self.salir = Boton(btn_salir_path, snd_click_path, (550, 615), 0.1)

        if snd_bg_path.exists():
            try:
                pygame.mixer.music.load(str(snd_bg_path))
                pygame.mixer.music.play(-1)
            except Exception:
                pass

    def run(self, clock):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"

        if self.jugar.es_presionado():
            return "PLAY"

        if self.salir.es_presionado():
            return "EXIT"

        self.screen.fill((0, 0, 0))
        if self.fondo:
            self.screen.blit(self.fondo, (0, 0))

        self.jugar.draw(self.screen)
        self.salir.draw(self.screen)

        pygame.display.flip()
        clock.tick(60)
        return "CONTINUE"
