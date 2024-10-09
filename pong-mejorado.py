import py5
from py5_tools import
import random

# Variables globales
paddle1_y = paddle2_y = 0
paddle_width = paddle_height = 0
paddle_speed = ball_size = 0
ball_x = ball_y = ball_dx = ball_dy = 0
player1_score = player2_score = 0
paddle1_color = paddle2_color = 0

# Estado de las teclas presionadas
keys = set()

def setup():
    py5.size(800, 400)
    global paddle_width, paddle_height, paddle_speed, ball_size
    global ball_x, ball_y, ball_dx, ball_dy
    global paddle1_y, paddle2_y, player1_score, player2_score, paddle1_color, paddle2_color
    paddle_width = 20
    paddle_height = 100
    paddle_speed = 7
    ball_size = 20
    paddle1_color = py5.color(255, 0, 0)  # Rojo
    paddle2_color = py5.color(0, 0, 255)  # Azul
    
    # Sonidos
    py5.load_sound("start.mp3").play()  # Sonido al iniciar el juego
    global bounce_sound, score_sound
    bounce_sound = py5.load_sound("bounce.mp3")
    score_sound = py5.load_sound("score.mp3")

    reset_game()

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    
    # Dificultad
    global difficulty
    difficulty = py5.get_user_input("Selecciona la dificultad (1-3): ", "int")
    if difficulty == 1:
        ball_dx = 3
    elif difficulty == 2:
        ball_dx = 5
    elif difficulty == 3:
        ball_dx = 8
    else:
        difficulty = 2  # Valor por defecto
        ball_dx = 5
    
    ball_dy = random.choice([-3, 3])  # Dirección vertical aleatoria al inicio
    paddle1_y = py5.height / 2 - paddle_height / 2
    paddle2_y = py5.height / 2 - paddle_height / 2
    player1_score = 0
    player2_score = 0

def draw():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score

    py5.background(0)
    
    # Dibujar los paddles
    py5.fill(paddle1_color)
    py5.rect(30, paddle1_y, paddle_width, paddle_height)  # Pala izquierda
    py5.fill(paddle2_color)
    py5.rect(py5.width - 30 - paddle_width, paddle2_y, paddle_width, paddle_height)  # Pala derecha
    
    # Dibujar la pelota
    py5.fill(255)
    py5.ellipse(ball_x, ball_y, ball_size, ball_size)
    
    # Dibujar el marcador
    py5.text_size(32)
    py5.text_align(py5.CENTER)
    py5.fill(255)
    py5.text(f"{player1_score} - {player2_score}", py5.width / 2, 40)
    
    # Dibujar ayuda de teclas
    py5.text_size(16)
    py5.text_align(py5.LEFT)
    py5.fill(255)
    py5.text("Jugador 1: W (Arriba), S (Abajo)", 10, 30)
    py5.text_align(py5.RIGHT)
    py5.text("Jugador 2: O (Arriba), L (Abajo)", py5.width - 10, 30)
    
    # Actualizar posición de la pelota
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Rebote de la pelota en la parte superior e inferior
    if ball_y <= ball_size / 2 or ball_y >= py5.height - ball_size / 2:
        ball_dy *= -1
        bounce_sound.play()
    
    # Verificar colisiones con los paddles
    if ball_x - ball_size / 2 <= 30 + paddle_width:
        if paddle1_y < ball_y < paddle1_y + paddle_height:
            ball_dx *= -1
            ball_x = 30 + paddle_width + ball_size / 2
            bounce_sound.play()
    
    if ball_x + ball_size / 2 >= py5.width - 30 - paddle_width:
        if paddle2_y < ball_y < paddle2_y + paddle_height:
            ball_dx *= -1
            ball_x = py5.width - 30 - paddle_width - ball_size / 2
            bounce_sound.play()
    
    # Si la pelota sale por la izquierda
    if ball_x < 0:
        player2_score += 1
        score_sound.play()
        reset_ball()
    
    # Si la pelota sale por la derecha
    if ball_x > py5.width:
        player1_score += 1
        score_sound.play()
        reset_ball()

    # Limitar el movimiento de los paddles
    if 'w' in keys and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if 's' in keys and paddle1_y < py5.height - paddle_height:
        paddle1_y += paddle_speed
    if 'o' in keys and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if 'l' in keys and paddle2_y < py5.height - paddle_height:
        paddle2_y += paddle_speed

def key_pressed():
    global keys
    keys.add(py5.key)

def key_released():
    global keys
    keys.discard(py5.key)

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx *= -1
    ball_dy = random.choice([-3, 3])  # Dirección vertical aleatoria al reiniciar

if __name__ == "__main__":
    py5.run_sketch()