import pygame
import sys
import subprocess

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird Homepage")

# Set up the background
background_color = (135, 206, 250)  # Light blue
background_image = pygame.image.load("img/bg.png")  

# Set up the title
title_font = pygame.font.SysFont("Bauhaus 93", 64)  
title_text = title_font.render("Flappy Bird", True, (255, 255, 255))  # White

# Set up the play button
button_font = pygame.font.SysFont("Bauhaus 93", 32)  
button_text = button_font.render("Play", True, (0, 0, 0))  # Black
button_width = 200
button_height = 50
button_x = screen_width // 2 - button_width // 2
button_y = screen_height // 2 - button_height // 2

# Set up the login button
login_button_font = pygame.font.SysFont("Bauhaus 93", 32)  
login_button_text = login_button_font.render("Login", True, (0, 0, 0))  # Black
login_button_width = 200
login_button_height = 50
login_button_x = (screen_width - login_button_width) // 2
login_button_y = (screen_height - login_button_height) // 2 + 100  # Position it below the input fields


def check_credentials(username, password):
    if username == 'admin' and password == 'admin':
        return True
    else:
        return False

#Call the login function
def login(text, font, text_col, x, y):
    username = ''
    password = ''
    input_active = 'username'  # Start with the username field active

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

        username_text = font.render(f"Username: {username}", True, text_col)
        password_text = font.render(f"Password: {'*' * len(password)}", True, text_col)  # Hide the password
        screen.blit(username_text, (x, y))
        screen.blit(password_text, (x, y + 50))

        #Display the login button
        if username and password:
            screen.blit(login_button_text, (login_button_x, login_button_y))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if login_button_x <= mouse_pos[0] <= login_button_x + login_button_width and login_button_y <= mouse_pos[1] <= login_button_y + login_button_height:
                    if check_credentials(username, password):
                        return
                    else:
                        text = font.render("Invalid credentials. Try again.", True, (255, 0, 0))
                        screen.blit(text, (x, y + 100))
                        pygame.display.update()
                        pygame.time.wait(2000)  # Wait for 2 seconds
                        login('', font, text_col, x, y)  # Call the login function again to reset the input fields

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # Switch between fields
                    input_active = 'password' if input_active == 'username' else 'username'
                
                elif event.key == pygame.K_BACKSPACE:  # Delete character
                    if input_active == 'username' and username:
                        username = username[:-1]
                    elif input_active == 'password' and password:
                        password = password[:-1]
                else:  # Add character
                    if input_active == 'username' and len(username) < 20:
                        username += event.unicode
                    elif input_active == 'password' and len(password) < 20:
                        password += event.unicode

# Call the login function
login('',button_font, (0, 0, 0), button_x, button_y)

# Main loop
run = True
while run:
    screen.fill(background_color)
    screen.blit(background_image, (0, 0))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
    screen.blit(button_text, (button_x, button_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                subprocess.run(["python", "flappyBird.py"])

    pygame.display.update()


