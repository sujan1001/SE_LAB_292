import math
import random
import pygame


class GameEngine:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.arm_position = 0.0
        self.target_limit = 100.0
        self.last_key = None

        self.stamina = 100.0
        self.max_stamina = 100.0

        self.winner = None
        self.game_state = "PLAYING"
        self.ai_strength = 0.35

        # Task 2: AI normal -> surge -> cooldown cycle
        self.ai_cycle_frame = 0
        self.ai_cycle_length = 600       # 10 seconds at 60 FPS
        self.ai_surge_duration = 120     # 2 seconds
        self.ai_cooldown_duration = 180  # 3 seconds
        self.ai_surge_active = False
        self.ai_cooldown_active = False

        # Task 4: counter-surge bonus
        self.counter_surge_active = False

        self.font_big = pygame.font.SysFont(None, 44)
        self.font_med = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if self.stamina <= 10:
                return

            if event.key == pygame.K_LEFT:
                if self.last_key != pygame.K_LEFT:
                    push_strength = 4.2

                    # Task 4: double push strength during counter-surge
                    if self.counter_surge_active:
                        push_strength *= 2

                    self.arm_position -= push_strength
                    self.stamina = max(0.0, self.stamina - 2.0)
                    self.last_key = pygame.K_LEFT

            elif event.key == pygame.K_RIGHT:
                if self.last_key != pygame.K_RIGHT:

                    # Task 4:
                    # Pressing Right during the AI cooldown activates
                    # the counter-surge comeback bonus.
                    if self.ai_cooldown_active:
                        self.counter_surge_active = True

                    push_strength = 4.2

                    if self.counter_surge_active:
                        push_strength *= 2

                    self.arm_position -= push_strength
                    self.stamina = max(0.0, self.stamina - 2.0)
                    self.last_key = pygame.K_RIGHT

    def update(self):
        if self.game_state != "PLAYING":
            return

        # ---------------------------------------------------------
        # Task 2: AI surge / cooldown cycle
        # ---------------------------------------------------------

        self.ai_cycle_frame = (
            self.ai_cycle_frame + 1
        ) % self.ai_cycle_length

        surge_start = (
            self.ai_cycle_length -
            self.ai_surge_duration
        )

        cooldown_start = (
            surge_start -
            self.ai_cooldown_duration
        )

        if self.ai_cycle_frame >= surge_start:
            self.ai_surge_active = True
            self.ai_cooldown_active = False
            self.counter_surge_active = False

            current_ai_strength = self.ai_strength * 2.5

        elif self.ai_cycle_frame >= cooldown_start:
            self.ai_surge_active = False
            self.ai_cooldown_active = True

            current_ai_strength = self.ai_strength * 0.35

        else:
            self.ai_surge_active = False
            self.ai_cooldown_active = False
            self.counter_surge_active = False

            current_ai_strength = self.ai_strength

        ai_variance = random.uniform(0.3, 1.0)

        self.arm_position += (
            current_ai_strength * ai_variance
        )

        # ---------------------------------------------------------
        # Task 4: increased stamina recovery during counter-surge
        # ---------------------------------------------------------

        if self.stamina < self.max_stamina:

            if self.counter_surge_active:
                recovery_rate = 1.6
            else:
                recovery_rate = 0.8

            self.stamina = min(
                self.max_stamina,
                self.stamina + recovery_rate
            )

        # ---------------------------------------------------------
        # Win conditions
        # ---------------------------------------------------------

        if self.arm_position <= -self.target_limit:
            self.winner = "PLAYER"
            self.game_state = "GAME_OVER"

        elif self.arm_position >= self.target_limit:
            self.winner = "COMPUTER"
            self.game_state = "GAME_OVER"

    def reset(self):
        self.arm_position = 0.0
        self.stamina = 100.0
        self.last_key = None

        self.winner = None
        self.game_state = "PLAYING"

        # Reset Task 2 cycle
        self.ai_cycle_frame = 0
        self.ai_surge_active = False
        self.ai_cooldown_active = False

        # Reset Task 4 bonus
        self.counter_surge_active = False

    def render(self, screen):
        screen.fill((25, 28, 35))

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        title_surf = self.font_big.render(
            "ARM WRESTLE SHOWDOWN",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 -
                title_surf.get_width() // 2,
                12
            )
        )

        # ---------------------------------------------------------
        # Player / Computer labels
        # ---------------------------------------------------------

        player_header = self.font_med.render(
            "PLAYER",
            True,
            (80, 160, 255)
        )

        computer_header = self.font_med.render(
            "COMPUTER",
            True,
            (255, 100, 80)
        )

        screen.blit(player_header, (60, 55))
        screen.blit(
            computer_header,
            (self.width - 150, 55)
        )

        # ---------------------------------------------------------
        # Table
        # ---------------------------------------------------------

        table_rect = pygame.Rect(
            40,
            100,
            self.width - 80,
            310
        )

        pygame.draw.rect(
            screen,
            (110, 50, 15),
            table_rect,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            (70, 30, 8),
            table_rect,
            width=5,
            border_radius=14
        )

        pygame.draw.line(
            screen,
            (45, 18, 4),
            (self.width // 2, 100),
            (self.width // 2, 410),
            4
        )

        # ---------------------------------------------------------
        # Arm / hands
        # ---------------------------------------------------------

        offset_x = (
            self.arm_position /
            self.target_limit
        ) * 95

        hand_x = (
            self.width // 2
        ) + int(offset_x)

        hand_y = 235

        p_shoulder = (70, 330)
        p_elbow = (140, 215)

        c_shoulder = (
            self.width - 70,
            330
        )

        c_elbow = (
            self.width - 140,
            215
        )

        pygame.draw.line(
            screen,
            (200, 145, 110),
            p_shoulder,
            p_elbow,
            32
        )

        pygame.draw.line(
            screen,
            (215, 160, 125),
            p_elbow,
            (hand_x, hand_y),
            26
        )

        pygame.draw.circle(
            screen,
            (185, 130, 95),
            p_elbow,
            18
        )

        pygame.draw.line(
            screen,
            (170, 110, 85),
            c_shoulder,
            c_elbow,
            32
        )

        pygame.draw.line(
            screen,
            (185, 125, 95),
            c_elbow,
            (hand_x, hand_y),
            26
        )

        pygame.draw.circle(
            screen,
            (150, 95, 70),
            c_elbow,
            18
        )

        pygame.draw.circle(
            screen,
            (225, 175, 140),
            (hand_x, hand_y),
            24
        )

        pygame.draw.circle(
            screen,
            (160, 115, 85),
            (hand_x, hand_y),
            24,
            width=3
        )

        # ---------------------------------------------------------
        # Stamina
        # ---------------------------------------------------------

        stamina_label = self.font_med.render(
            "STAMINA",
            True,
            (220, 220, 220)
        )

        screen.blit(
            stamina_label,
            (40, 445)
        )

        stamina_bg = pygame.Rect(
            140,
            448,
            240,
            22
        )

        stamina_fill = pygame.Rect(
            140,
            448,
            int(
                240 *
                (
                    self.stamina /
                    self.max_stamina
                )
            ),
            22
        )

        pygame.draw.rect(
            screen,
            (45, 50, 60),
            stamina_bg,
            border_radius=6
        )

        bar_color = (
            (60, 210, 100)
            if self.stamina > 25
            else
            (220, 60, 60)
        )

        pygame.draw.rect(
            screen,
            bar_color,
            stamina_fill,
            border_radius=6
        )

        # ---------------------------------------------------------
        # Task 3: AI surge warning
        # ---------------------------------------------------------

        if self.ai_surge_active:
            surge_text = self.font_med.render(
                "WARNING: AI SURGE!",
                True,
                (255, 80, 80)
            )

            screen.blit(
                surge_text,
                (
                    self.width // 2 -
                    surge_text.get_width() // 2,
                    480
                )
            )

        # ---------------------------------------------------------
        # Task 3: Player exhaustion
        # ---------------------------------------------------------

        if self.stamina <= 10:
            exhaustion_text = self.font_med.render(
                "EXHAUSTED! TOO TIRED TO PUSH!",
                True,
                (255, 80, 80)
            )

            screen.blit(
                exhaustion_text,
                (
                    self.width // 2 -
                    exhaustion_text.get_width() // 2,
                    510
                )
            )

        # ---------------------------------------------------------
        # Task 4: Counter-surge indicator
        # ---------------------------------------------------------

        if self.counter_surge_active:
            counter_text = self.font_med.render(
                "COUNTER-SURGE! PUSH!",
                True,
                (80, 240, 100)
            )

            screen.blit(
                counter_text,
                (
                    self.width // 2 -
                    counter_text.get_width() // 2,
                    540
                )
            )

        # ---------------------------------------------------------
        # Game over
        # ---------------------------------------------------------

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 200)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            win_text = (
                "PLAYER WINS THE MATCH!"
                if self.winner == "PLAYER"
                else
                "COMPUTER WINS!"
            )

            color = (
                (80, 240, 100)
                if self.winner == "PLAYER"
                else
                (240, 80, 80)
            )

            text_surf = self.font_big.render(
                win_text,
                True,
                color
            )

            screen.blit(
                text_surf,
                (
                    self.width // 2 -
                    text_surf.get_width() // 2,
                    self.height // 2 - 45
                )
            )

            restart_surf = self.font_med.render(
                "Press [R] to Rematch",
                True,
                (240, 240, 240)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2 -
                    restart_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )