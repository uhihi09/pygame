import pygame
import random
import math

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell Game")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 플레이어 설정
player_size = 40
player = pygame.Rect(WIDTH//2, HEIGHT - 60, player_size, player_size)
player_speed = 5

# 탄막 클래스
class Bullet:
    def __init__(self, x, y, angle, speed, color=RED):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

# 보스 클래스
class Boss:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 100
        self.size = 60
        self.hp = 100
        self.direction = 1
        self.speed = 2
        self.attack_cooldown = 0

    def move(self):
        self.x += self.direction * self.speed
        if self.x < 50 or self.x > WIDTH - 50:
            self.direction *= -1

    def attack(self, bullets):
        if self.attack_cooldown == 0:
            for i in range(0, 360, 20):
                angle = math.radians(i)
                bullets.append(Bullet(self.x, self.y, angle, 3))
            self.attack_cooldown = 60  # 쿨다운 설정
        else:
            self.attack_cooldown -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x - self.size//2, self.y - self.size//2, self.size, self.size))

# 게임 루프
clock = pygame.time.Clock()
running = True
bullets = []
boss = Boss()

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 플레이어 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player_size:
        player.x += player_speed
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.y < HEIGHT - player_size:
        player.y += player_speed

    # 보스 이동 및 공격
    boss.move()
    boss.attack(bullets)
    
    # 탄막 이동
    for bullet in bullets[:]:
        bullet.move()
        if bullet.y < 0 or bullet.y > HEIGHT or bullet.x < 0 or bullet.x > WIDTH:
            bullets.remove(bullet)

    # 충돌 감지
    for bullet in bullets:
        if player.colliderect(pygame.Rect(bullet.x-5, bullet.y-5, 10, 10)):
            print("Game Over!")
            running = False

    # 그리기
    pygame.draw.rect(screen, RED, player)
    boss.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
