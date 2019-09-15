import pygame
pygame.init()

from rocket import Rocket


class AstroRockets:
	def __init__(self, size, title, background):
		self.width = size[0]
		self.height = size[1]
		self.background = background

		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.running = True

		self.win = pygame.display.set_mode(size)
		pygame.display.set_caption(title)

	# ###################### #
	# ### Ignore this 🔼 ### #
	# ###################### #

	def start(self):
		self.p1 = Rocket(self.width / 2 - 250, self.height / 2, (255, 0, 0))
		self.p2 = Rocket(self.width / 2 + 250, self.height / 2, (0, 0, 255))
		self.p2.heading = 180

	def logic(self):
		keys = pygame.key.get_pressed()
		speed = 5
		turn_speed = 3
		friction = 0.96

		# Player 1 controls
		if keys[pygame.K_w]:
			self.p1.speed = speed
		
		self.p1.speed *= friction

		if keys[pygame.K_a]:
			self.p1.heading -= turn_speed

		if keys[pygame.K_d]:
			self.p1.heading += turn_speed

		# Player 2 controls
		if keys[pygame.K_UP]:
			self.p2.speed = speed
		
		self.p2.speed *= friction

		if keys[pygame.K_LEFT]:
			self.p2.heading -= turn_speed

		if keys[pygame.K_RIGHT]:
			self.p2.heading += turn_speed

		self.p1.update()
		self.p2.update()

	def render(self):
		self.p1.render(self.win)
		self.p2.render(self.win)































def main():
	game = AstroRockets((1280, 720), "AstroRockets", (0, 0, 0))

	game.start()

	while game.running:
		game.clock.tick(game.FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.running = False

		game.logic()
		game.win.fill(game.background)
		game.render()
		pygame.display.update()


if __name__ == "__main__":
	main()
	quit()
