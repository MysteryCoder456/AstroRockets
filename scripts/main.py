"""
Produced by Rehatbir Singh(MysteryCoder456)
Contact at rehatbir.singh@gmail.com for any questions
Full Rights Reserved under MIT License
"""

import pygame
pygame.init()

from math import sqrt, atan2
from random import randint
from time import sleep
from rocket import Rocket
from bullet import Bullet
from wall import Wall
from powerups import ScatterShot


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

	# ##################### #
	# #### Ignore this #### #
	# ##################### #

	def start(self):
		self.p1 = Rocket(self.width / 2 - 250, self.height / 2, (255, 0, 0))
		self.p2 = Rocket(self.width / 2 + 250, self.height / 2, (0, 0, 255))
		self.p2.heading = 180
		self.p2.drift_heading = 180

		self.levels = [
			(Wall(5, 5, 1, self.height), Wall(5, 5, self.width, 1), Wall(self.width - 5, 5, 1, self.height), Wall(5, self.height - 5, self.width, 1), Wall(100, 100, 300, 135), Wall(900, 450, 150, 250)),
			(Wall(5, 5, 1, self.height/2 - 150), Wall(5, self.height/2 + 150, 1, self.height/2 - 150), Wall(5, 5, self.width, 1), Wall(self.width - 5, 5, 1, self.height / 2 - 150), Wall(self.width - 5, self.height / 2 + 150, 1, self.height / 2 - 150), Wall(5, self.height - 5, self.width, 1))
		]

		self.current_level = randint(0 ,len(self.levels)-1)

		self.powerup_ids = [
			"none", # 0
			"scatter_shot", # 1
			"missile" # 2
		]

		self.powerups = [ScatterShot(self.width / 2, self.height / 2)]

	def logic(self):
		keys = pygame.key.get_pressed()
		# speed = 5
		acceleration = 0.25
		turn_speed = 3
		friction = 0.978
		recoil = -5

		# Player 1 controls
		if keys[pygame.K_w]:
			self.p1.accelerate(acceleration)
		
		self.p1.speed *= friction

		if keys[pygame.K_s]:
			if not self.p1.bullet_is_shot:
				b = Bullet(self.p1.x, self.p1.y, self.p1.drift_heading, self.p1.color)
				self.p1.bullets.append(b)
				self.p1.bullet_is_shot = True
				self.p1.shoot_timer = 0
				self.p1.accelerate(recoil)

		if keys[pygame.K_a]:
			self.p1.drift_heading -= turn_speed

		if keys[pygame.K_d]:
			self.p1.drift_heading += turn_speed

		# PowerUp Shooting for Player 1
		if keys[pygame.K_e] or keys[pygame.K_q]:

			if self.powerup_ids[self.p1.current_powerup] == "none":
				print("No Powerup Collected!")

			elif self.powerup_ids[self.p1.current_powerup] == "scatter_shot":
				bullet_count = 8
				for i in range(bullet_count):
					bullet_hdg = (360 / bullet_count) * i
					b = Bullet(self.p1.x, self.p1.y, bullet_hdg, ScatterShot(0, 0).color)
					b.speed = 8
					self.p1.bullets.append(b)

			self.p1.assign_powerup(0)


		# Player 2 controls
		if keys[pygame.K_UP]:
			self.p2.accelerate(acceleration)

		if keys[pygame.K_DOWN]:
			if not self.p2.bullet_is_shot:
				b = Bullet(self.p2.x, self.p2.y, self.p2.drift_heading, self.p2.color)
				self.p2.bullets.append(b)
				self.p2.bullet_is_shot = True
				self.p2.shoot_timer = 0
				self.p2.accelerate(recoil)

		if keys[pygame.K_LEFT]:
			self.p2.drift_heading -= turn_speed

		if keys[pygame.K_RIGHT]:
			self.p2.drift_heading += turn_speed

		# PowerUp Shooting for Player 2
		if keys[pygame.K_RSHIFT] or keys[pygame.K_QUESTION]:
			
			if self.powerup_ids[self.p2.current_powerup] == "none":
				print("No Powerup Collected!")

			elif self.powerup_ids[self.p2.current_powerup] == "scatter_shot":
				bullet_count = 8
				for i in range(bullet_count):
					bullet_hdg = (360 / bullet_count) * i
					b = Bullet(self.p2.x, self.p2.y, bullet_hdg, ScatterShot(0, 0).color)
					b.speed = 8
					self.p2.bullets.append(b)
			
			self.p2.assign_powerup(0)

		self.p1.update()
		self.p1.speed *= friction
		
		self.p2.update()
		self.p2.speed *= friction

		despawn_time = 200

		# Update Player 1's Bullets
		for bullet in self.p1.bullets:
			bullet.update()

			if bullet.x < 0:
				bullet.x = self.width
			elif bullet.x > self.width:
				bullet.x = 0

			if bullet.y < 0:
				bullet.y = self.height
			elif bullet.y > self.height:
				bullet.y = 0

			bullet.update_collider()
			
			# Collision between player 2 and player 1's bullets
			if self.collision_circle(bullet.x, bullet.y, bullet.radius, self.p2.x, self.p2.y, self.p2.collider_size):
				print("RED WINS!!")
				sleep(3)
				self.running = False

			# Automatic despawn
			if bullet.despawn_timer > despawn_time:
				self.p1.bullets.remove(bullet)
				
		# Update Player 2's Bullets		
		for bullet in self.p2.bullets:
			bullet.update()

			if bullet.x < 0:
				bullet.x = self.width
			elif bullet.x > self.width:
				bullet.x = 0

			if bullet.y < 0:
				bullet.y = self.height
			elif bullet.y > self.height:
				bullet.y = 0

			bullet.update_collider()

			# Collisions between player 1 and player 2's bullets
			if self.collision_circle(bullet.x, bullet.y, bullet.radius, self.p1.x, self.p1.y, self.p1.collider_size):
				print("BLUE WINS!!")
				sleep(3)
				self.running = False

			# Automatic despawn
			if bullet.despawn_timer > despawn_time:
				self.p2.bullets.remove(bullet)


		# Player 1 boundary collisions
		if self.p1.x < 0:
			self.p1.x = self.width
		elif self.p1.x > self.width:
			self.p1.x = 0

		if self.p1.y < 0:
			self.p1.y = self.height
		elif self.p1.y > self.height:
			self.p1.y = 0

		# Player 2 boundary collisions
		if self.p2.x < 0:
			self.p2.x = self.width
		elif self.p2.x > self.width:
			self.p2.x = 0

		if self.p2.y < 0:
			self.p2.y = self.height
		elif self.p2.y > self.height:
			self.p2.y = 0

		self.p1.update_collider()
		self.p2.update_collider()

		# Handle collisions between rockets and walls
		for wall in self.levels[self.current_level]:
			# Player 1
			if wall.collider.colliderect(self.p1.wall_collider):
				self.p1.x = self.p1.old_x
				self.p1.y = self.p1.old_y
				self.p1.speed = 0

			# Player 2
			if wall.collider.colliderect(self.p2.wall_collider):
				self.p2.x = self.p2.old_x
				self.p2.y = self.p2.old_y
				self.p2.speed = 0

		# Handle collisions between bullets and walls
		for wall in self.levels[self.current_level]:
			# Player 1
			for bullet in self.p1.bullets:
				if bullet.wall_collider.colliderect(wall.collider):
					self.p1.bullets.remove(bullet)

			# Player 2
			for bullet in self.p2.bullets:
				if bullet.wall_collider.colliderect(wall.collider):
					self.p2.bullets.remove(bullet)

		# Handle collisions between rockets and powerups
		for powerup in self.powerups:
			# Player 1
			if self.collision_circle(self.p1.x, self.p1.y, self.p1.collider_size, powerup.x, powerup.y, powerup.radius):
				self.p1.assign_powerup(powerup.id)
				self.powerups.remove(powerup)

			# Player 2
			if self.collision_circle(self.p2.x, self.p2.y, self.p2.collider_size, powerup.x, powerup.y, powerup.radius):
				self.p2.assign_powerup(powerup.id)
				self.powerups.remove(powerup)

		self.p1.update_old_coords()
		self.p2.update_old_coords()

	def render(self):
		self.p1.render(self.win)
		self.p2.render(self.win)

		for bullet in self.p1.bullets:
			bullet.render(self.win)

		for bullet in self.p2.bullets:
			bullet.render(self.win)

		for wall in self.levels[self.current_level]:
			wall.render(self.win)

		for powerup in self.powerups:
			powerup.render(self.win)

	# Gameplay functions

	def dist(self, x1, y1, x2, y2):
		"""Finds the distance between 2 points on a 2D plane using the Pythagorean Theorem.
		a^2 + b^2 = c^2
		
		Arguments:
			x1 {int}
			y1 {int}
			x2 {int}
			y2 {int}

		Returns:
			int -- distance between the two points
		"""

		a = x1 - x2
		b = y1 - y2
		c = sqrt((a ** 2) + (b ** 2))
		return c

	def collision_circle(self, x1, y1, r1, x2, y2, r2):
		"""Finds out whether two circlea are overlapping using dist() function
		
		Arguments:
			x1 {int} -- x position of first circle
			y1 {int} -- y position of first circle
			r1 {int} -- radius of first circle
			x2 {int} -- x position of second circle
			y2 {int} -- y position of second circle
			r2 {int} -- radius of second circle
		
		Returns:
			bool -- Are the 2 circle overlapping
		"""
		d = self.dist(x1, y1, x2, y2)

		if d <= r1 + r2:
			return True



































def main():
	game.start()

	while game.running:
		game.clock.tick(game.FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		game.logic()
		game.win.fill(game.background)
		game.render()
		pygame.display.update()


if __name__ == "__main__":
	game = AstroRockets((1280, 720), "AstroRockets", (0, 0, 0))
	while True:
		main()
		game.running = True
