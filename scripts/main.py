import pygame
pygame.init()


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





	def start(self):
		pass

	def logic(self):
		pass

	def render(self):
		pass































def main():
	game = AstroRockets((1280, 720), "AstroRockets", (0, 0, 0))

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
