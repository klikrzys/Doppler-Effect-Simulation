#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        pygame.display.set_caption("Doppler's Effect Simple Simulation")
        self.options = Options()
        self.window_surface = pygame.display.set_mode(self.options.resolution)

        self.background_surface = None
        self.background_img = pygame.image.load("background.png")

        # self.ui_manager = UIManager(self.options.resolution, 'data/themes/theme_2.json')  # , 'data/themes/theme_2.json'
        self.ui_manager = UIManager(self.options.resolution)
        self.ui_manager.preload_fonts([
            {'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
            {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
            {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
            {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
            {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
        ])

        # Transparent background behind control GUI.
        self.background_ui = pygame.Surface((500, 550), pygame.SRCALPHA)
        # notice the alpha value in the color
        self.background_ui.fill((255, 255, 255, 128))

        self.doppler_effect = DopplerEffect()

        self.recreate_ui()

        self.clock = pygame.time.Clock()

        self.button_response_timer = pygame.time.Clock()
        self.running = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(
            self.ui_manager.get_theme().get_colour('dark_bg'))

        self.start_button = UIButton(pygame.Rect((720, 325), (100, 40)),
                                     'START',
                                     self.ui_manager,
                                     object_id='#start_button')

        self.stop_button = UIButton(pygame.Rect((850, 325), (100, 40)),
                                    'STOP',
                                    self.ui_manager,
                                    object_id='#stop_button')

        self.restart_button = UIButton(pygame.Rect((785, 375), (100, 40)),
                                       'RESTART',
                                       self.ui_manager,
                                       object_id='#stop_button')

        self.frequency_label = UILabel(pygame.Rect(
            (720, 420), (240, 25)), "Frequency", self.ui_manager)

        self.frequency_slider = UIHorizontalSlider(pygame.Rect((700, 460), (210, 25)),
                                                   10,
                                                   (5, 20.0),
                                                   self.ui_manager,
                                                   object_id='#frequency_slider')
        self.frequency_label_value = UILabel(pygame.Rect(
            (922, 460), (70, 25)), "1.0 Hz", self.ui_manager)

        self.speed_label = UILabel(pygame.Rect(
            (720, 50), (240, 25)), "Speed:", self.ui_manager)
        self.entities_speed = UIDropDownMenu(['transmitter is faster', 'receiver is faster', 'equal speed'],  # options
                                             'equal speed',  # preselected option
                                             pygame.Rect(
            (720, 80), (240, 25)),
            self.ui_manager)

        self.emitter_label = UILabel(pygame.Rect(
            (720, 150), (240, 25)), "Transmitter", self.ui_manager)

        self.emitter_direction = UIDropDownMenu(['Left', 'Right'],  # options
                                                'Left',  # preselected option
                                                pygame.Rect(
                                                    (720, 180), (240, 25)),
                                                self.ui_manager)

        self.observer_label = UILabel(pygame.Rect(
            (720, 210), (240, 25)), "Receiver", self.ui_manager)

        self.observer_direction = UIDropDownMenu(['Left', 'Right'],  # options
                                                 'Right',  # preselected option
                                                 pygame.Rect(
                                                     (720, 240), (240, 25)),
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
                        self.doppler_effect.start()  # START ANIMATION :)
                    elif event.ui_element == self.stop_button:
                        self.doppler_effect.stop()  # STOP ANIMATION :(
                    elif event.ui_element == self.restart_button:  # RESET EVERYTING :O
                        self.doppler_effect.reset()
                        self.window_surface.blit(
                            self.background_surface, (0, 0))  # reset screen
                """ CHANGING FREQUENCY ON SLIDER """
                if self.frequency_slider.has_moved_recently:
                    # Set frequency value near the slider
                    frequency_val = float(
                        round(self.frequency_slider.get_current_value()))

                    self.frequency_label_value.set_text(
                        "{0:.1f}".format(frequency_val/10)+" Hz")
                    self.doppler_effect.setFrequency(frequency_val/10)
                    self.doppler_effect.reset()
                    self.window_surface.blit(
                        self.background_surface, (0, 0))  # reset screen
                if event.user_type == 'ui_drop_down_menu_changed':
                    emittDir = None
                    observDir = None
                    if event.ui_element == self.emitter_direction:
                        if self.emitter_direction.selected_option == "Left":
                            emittDir = -1
                        else:
                            emittDir = 1
                    elif event.ui_element == self.observer_direction:
                        if self.observer_direction.selected_option == "Left":
                            observDir = -1
                        else:
                            observDir = 1
                    elif event.ui_element == self.entities_speed:
                        emittSpeed = 1
                        observSpeed = 1
                        if self.entities_speed.selected_option == "transmitter is faster":
                            emittSpeed = 2
                        elif self.entities_speed.selected_option == "receiver is faster":
                            observSpeed = 2
                        # Set desired new entitie's speeds
                        self.doppler_effect.setSpeed(emittSpeed, observSpeed)

                    # Set desired new entitie's directions
                    self.doppler_effect.setDirection(emittDir, observDir)

                    self.doppler_effect.reset()  # reset 'the stage' :o
                    self.doppler_effect.stop()
                    self.window_surface.blit(self.background_surface, (0, 0))

    def run(self):
        self.window_surface = pygame.display.set_mode(self.options.resolution)
        self.recreate_ui()

        while self.running:
            time_delta = self.clock.tick(180)/1000.0

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)

            # Drawing main background
            self.window_surface.blit(self.background_img, (0, 0))
            #self.window_surface.blit(self.background_surface, (0, 0))

            # Update simulation
            self.doppler_effect.update(1)

            # Render current frame
            self.doppler_effect.render(self.window_surface)

            # draw graphical user interface
            self.window_surface.blit(
                self.background_ui, (650, 0))  # Background
            self.ui_manager.draw_ui(self.window_surface)  # Controls

            pygame.display.flip()

            self.clock.tick(60)


if __name__ == '__main__':
    app = OptionsUIApp()
    app.run()
