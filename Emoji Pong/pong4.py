import pygame
import random
import sys
import os

def initialize_game():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Emoji Pong")
    return screen, screen_width, screen_height

def create_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect.inflate(-radius*2, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -radius*2))
    pygame.draw.circle(surface, color, (rect.left+radius, rect.top+radius), radius)
    pygame.draw.circle(surface, color, (rect.right-radius-1, rect.top+radius), radius)
    pygame.draw.circle(surface, color, (rect.left+radius, rect.bottom-radius-1), radius)
    pygame.draw.circle(surface, color, (rect.right-radius-1, rect.bottom-radius-1), radius)

def create_paddle(screen_height):
    paddle_width = 150
    paddle_height = 20
    paddle = pygame.Rect(350, screen_height - paddle_height - 50, paddle_width, paddle_height)
    return paddle

def create_ball(emoji_path):
    emoji_image = pygame.image.load(emoji_path)
    emoji_image = pygame.transform.scale(emoji_image, (50, 50))
    ball = emoji_image.get_rect(center=(100, 300))
    return ball, emoji_image

def update_ball_speed(score, ball_speed):
    if score % 10 == 0 and score != 0:
        ball_speed = [int(s * 1.1) for s in ball_speed]
    return ball_speed

def display_selection_screen(screen, screen_width, screen_height):
    font = pygame.font.Font(None, 36)
    selection_text = font.render("Emoji Ball:", True, (255, 255, 255))
    screen.blit(selection_text, selection_text.get_rect(center=(screen_width / 2, screen_height / 2 - 50)))
    emoji1 = pygame.image.load('Emoji.webp')
    emoji2 = pygame.image.load('Emoji2.webp')
    emoji1 = pygame.transform.scale(emoji1, (50, 50))
    emoji2 = pygame.transform.scale(emoji2, (50, 50))
    screen.blit(emoji1, (screen_width / 2 - 100, screen_height / 2))
    screen.blit(emoji2, (screen_width / 2 + 50, screen_height / 2))
    pygame.display.flip()
    emoji_selected = None
    while emoji_selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if screen_width / 2 - 100 <= x <= screen_width / 2 - 50 and screen_height / 2 <= y <= screen_height / 2 + 50:
                    emoji_selected = 'Emoji.webp'
                elif screen_width / 2 + 50 <= x <= screen_width / 2 + 100 and screen_height / 2 <= y <= screen_height / 2 + 50:
                    emoji_selected = 'Emoji2.webp'
    return emoji_selected

def main():
    screen, screen_width, screen_height = initialize_game()
    selected_emoji = display_selection_screen(screen, screen_width, screen_height)
    ball, emoji_image = create_ball(selected_emoji)
    colors = {
        'background': (255, 255, 153),
        'paddle': (0, 0, 0),
        'text': (255, 255, 255),
        'score': (0, 0, 0),
        'restart': (255, 0, 0),
        'speed_msg': (0, 0, 255),
        'continue': (0, 255, 0),
        'quit': (255, 0, 0),
        'quit_border': (0, 0, 0)
    }
    font = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    paddle = create_paddle(screen_height)
    ball_speed = [10, 8]  # Initial ball speed
    score = 0
    highest_score = 0  # Initialize highest score
    game_over = False
    continue_game = False
    paused = False

    # Load highest score from file or set it to 0 if file is empty or does not exist
    try:
        with open('highest_score.txt', 'r') as file:
            data = file.read()
            if data:
                highest_score = int(data)
    except FileNotFoundError:
        pass

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and score >= 200:
                if paused:
                    paused = False
                else:
                    paused = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and score >= 100:
                    continue_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 720 <= x <= 800 and 10 <= y <= 50:  # Check if mouse click is within the quit button area
                    pygame.quit()
                    sys.exit()

        if not paused:
            if continue_game or not game_over:
                mouse_pos = pygame.mouse.get_pos()
                paddle.x = mouse_pos[0] - paddle.width / 2

            if paddle.left < 0:
                paddle.left = 0
            elif paddle.right > screen_width:
                paddle.right = screen_width

            if not continue_game:
                ball.move_ip(ball_speed)
            
                if ball.top <= 0 or ball.bottom >= screen_height:
                    ball_speed[1] = -ball_speed[1]
                if ball.left <= 0 or ball.right >= screen_width:
                    ball_speed[0] = -ball_speed[0]

                if ball.colliderect(paddle) and ball_speed[1] > 0:
                    ball_speed[1] = -ball_speed[1]
                    score += 1
                    ball_speed = update_ball_speed(score, ball_speed)

        # Update highest score if the current score exceeds it
        if score > highest_score:
            highest_score = score

        screen.fill(colors['background'])
        create_rounded_rect(screen, paddle, colors['paddle'], 10)
        screen.blit(emoji_image, ball)

        score_text = score_font.render("Score: " + str(score), True, colors['score'])
        screen.blit(score_text, (10, 10))
        
        highest_score_text = score_font.render("Highest Score: " + str(highest_score), True, colors['score'])
        screen.blit(highest_score_text, (10, 30))

        # Draw quit button
        pygame.draw.rect(screen, colors['quit_border'], pygame.Rect(720, 10, 80, 40), border_radius=10)
        pygame.draw.rect(screen, colors['quit'], pygame.Rect(722, 12, 76, 36), border_radius=10)
        quit_text = font.render("Quit", True, colors['text'])
        screen.blit(quit_text, quit_text.get_rect(center=(771, 30)))  # Adjusted center alignment

        if paused:
            pause_text = font.render("Paused", True, colors['text'])
            screen.blit(pause_text, pause_text.get_rect(center=(screen_width / 2, screen_height / 2)))
        elif score % 100 == 0 and score != 0:
            restart_text = font.render("Restart", True, colors['restart'])
            screen.blit(restart_text, restart_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50)))
            if continue_game:
                continue_text = font.render("Continue (Press 'C')", True, colors['continue'])
                screen.blit(continue_text, continue_text.get_rect(center=(screen_width / 2, screen_height / 2 + 100)))

        pygame.display.flip()
        clock.tick(60)

    # Save highest score to file
    with open('highest_score.txt', 'w') as file:
        file.write(str(highest_score))

    text = font.render("Game Over", True, colors['text'])
    screen.blit(text, text.get_rect(center=(screen_width / 2, screen_height / 2)))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
