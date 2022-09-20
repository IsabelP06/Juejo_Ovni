import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ovnis")
clock = pygame.time.Clock()

def agregar_texto(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def escudo_nave(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def disparar(self):
		bala = Bala(self.rect.centerx, self.rect.top)
		all_sprites.add(bala)
		balas.add(bala)
		sonido_laser.play()

class Ovni(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(ovni_imagenes)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-2, 2)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 10)

class Bala(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


def mostrar_vienvenida_juego():
	screen.blit(background, [0,0])
	agregar_texto(screen, "Ovni", 65, WIDTH // 2, HEIGHT // 4)
	agregar_texto(screen, "Ovnis te estan atacando es momento de ver tu habilidad en combate", 14, WIDTH // 2, HEIGHT // 2)
	agregar_texto(screen, "Presiona espacio para inciar", 20, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False


ovni_imagenes = []
lista_ovnis = ["assets/ovni1.png", "assets/ovni2.png", "assets/ovni3.png", "assets/ovni4.png",
				"assets/ovni5.png", "assets/ovni6.png", "assets/ovni7.png", "assets/ovni8.png",
				"assets/ovni9.png","assets/ovni10.png"]
for img in lista_ovnis:
	ovni_imagenes.append(pygame.image.load(img).convert())


####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
	file = "assets/nivel_explosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("assets/fondo.png").convert()

# Cargar sonidos
sonido_laser = pygame.mixer.Sound("assets/laser.mp3")
explosion_sonido = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)


#pygame.mixer.music.play(loops=-1)

#### ----------GAME OVER
game_over = True
running = True
while running:
	if game_over:

		mostrar_vienvenida_juego()

		game_over = False
		all_sprites = pygame.sprite.Group()
		lista_ovnis = pygame.sprite.Group()
		balas = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)
		for i in range(8):
			ovni = Ovni()
			all_sprites.add(ovni)
			lista_ovnis.add(ovni)
		score = 0
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.disparar()


	all_sprites.update()

	#colisiones - meteoro - laser
	hits = pygame.sprite.groupcollide(lista_ovnis, balas, True, True)
	for hit in hits:
		score += 10
		explosion_sonido.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		ovni = Ovni()
		all_sprites.add(ovni)
		lista_ovnis.add(ovni)

	# Checar colisiones - jugador - meteoro
	hits = pygame.sprite.spritecollide(player, lista_ovnis, True)
	for hit in hits:
		player.shield -= 25
		ovni = Ovni()
		all_sprites.add(ovni)
		lista_ovnis.add(ovni)
		if player.shield <= 0:
			game_over = True

	screen.blit(background, [0, 0])

	all_sprites.draw(screen)

	#Marcador
	agregar_texto(screen, str(score), 25, WIDTH // 2, 10)

	# Escudo.
	escudo_nave(screen, 5, 5, player.shield)

	pygame.display.flip()
pygame.quit()