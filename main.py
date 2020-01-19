import pygame

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_horizontal_slider import UIHorizontalSlider
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui.elements.ui_label import UILabel
from doppler_effect import DopplerEffect 

class Options:
    def __init__(self):
        self.resolution = (1000, 650)


class OptionsUIApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Options UI")
        self.options = Options()
        self.window_surface = pygame.display.set_mode(self.options.resolution)

        self.background_surface = None

        #self.ui_manager = UIManager(self.options.resolution, 'data/themes/theme_2.json')  # , 'data/themes/theme_2.json'
        self.ui_manager = UIManager(self.options.resolution)
        self.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                       ])
        self.animation = True

        self.recreate_ui()

        self.clock = pygame.time.Clock()

        self.button_response_timer = pygame.time.Clock()
        self.running = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.ui_manager.get_theme().get_colour(None, None, 'dark_bg'))
        
        self.start_button = UIButton(pygame.Rect((720, 325), (100, 40)),
                                    'START',
                                    self.ui_manager,
                                    tool_tip_text="<font face=fira_code color=normal_text size=2>"
                                                  "<b><u>Uruchom animacje</u></b>"
                                                  "<br>"
                                                  "Po zmianie konfiguracji włącza na nowo"
                                                  "</font>",
                                    object_id='#start_button')
        
        self.stop_button = UIButton(pygame.Rect((850, 325), (100, 40)),
                                                'STOP',
                                                self.ui_manager,
                                                object_id='#stop_button')

        self.restart_button = UIButton(pygame.Rect((785, 375), (100, 40)),
                                                'RESTART',
                                                self.ui_manager,
                                                object_id='#stop_button')

        self.frequency_label = UILabel(pygame.Rect((720, 420), (240, 25)), "Czestotliwość", self.ui_manager)

        self.frequency_slider = UIHorizontalSlider(pygame.Rect((700, 460),(210, 25)),
                                                1.0,
                                                (1.0, 100.0),
                                                self.ui_manager,
                                                object_id='#frequency_slider')
        self.frequency_label_value = UILabel(pygame.Rect((922, 460), (70, 25)), "100.0 Hz", self.ui_manager)


        self.emitter_label = UILabel(pygame.Rect((720, 150), (240, 25)), "Źródło", self.ui_manager)

        self.emitter_direction = UIDropDownMenu(['Lewa','Prawa'], # options
                                                'Lewa', # preselected option
                                                pygame.Rect((720, 180), (240, 25)),
                                                self.ui_manager)


        self.emitter_label = UILabel(pygame.Rect((720, 210), (240, 25)), "Odbiorca", self.ui_manager)

        self.emitter_direction = UIDropDownMenu(['Lewa','Prawa'], # options
                                                'Lewa', # preselected option
                                                pygame.Rect((720, 240), (240, 25)),
                                                self.ui_manager)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)

            if event.type == pygame.USEREVENT:
                """ BUTTONS """
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == self.start_button:
                        self.animation = True # START ANIMATION :)
                    elif event.ui_element == self.stop_button:
                        self.animation = False # STOP ANIMATION :(
                """ CHANGING FREQUENCY ON SLIDER """
                if self.frequency_slider.has_moved_recently:
                    # Set frequency value near the slider
                    self.frequency_label_value.set_text(str(float(round(self.frequency_slider.get_current_value())))+" Hz")


    def run(self):
        self.window_surface = pygame.display.set_mode(self.options.resolution)
        self.recreate_ui()
        
        doppler_effect = DopplerEffect() 

        while self.running:
            time_delta = self.clock.tick(60)/1000.0

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)

            #Background
            self.window_surface.blit(self.background_surface, (0, 0))

            if self.animation:
                # Update objects
                doppler_effect.update(1)

            # Render current frame
            doppler_effect.render(self.window_surface)

            # draw graphics
            self.ui_manager.draw_ui(self.window_surface)


            pygame.display.update()


if __name__ == '__main__':
    app = OptionsUIApp()
    app.run()