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
from powerups import PowerUp, ScatterShot, Missile


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
			"none", # id = 0
			"scatter_shot", # id = 1
			"missile" # id = 2
		]

		self.powerups = []

	def logic(self):
		# Randomly spawn powerups
		if randint(0, 10000) < 40: # 0.4 percent chance of a powerup spawning randomly
			powerup_id = self.powerup_ids[randint(1, len(self.powerup_ids)-1)]

			if powerup_id == "scatter_shot":
				pos = self.get_spawn_location()
				powerup = ScatterShot(pos[0], pos[1])
				self.powerups.append(powerup)
			
			if powerup_id == "missile":
				pos = self.get_spawn_location()
				powerup = Missile(pos[0], pos[1])
				self.powerups.append(powerup)

		keys = pygame.key.get_pressed()
		# speed = 5
		acceleration = 0.25
		turn_speed = 3
		friction = 0.978
		recoil = -5
		despawn_time = 300

		scattershot_count = 16
		scattershot_speed = 12

		missile_speed = 10
		missile_fade = 80

		# Player 1 controls
		if keys[pygame.K_w]:
			self.p1.accelerate(acceleration)

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
		if keys[pygame.K_e]:

			if self.powerup_ids[self.p1.current_powerup] == "none":
				print("No Powerup Collected!")

			elif self.powerup_ids[self.p1.current_powerup] == "scatter_shot":
				for i in range(scattershot_count):
					bullet_hdg = ((360 / scattershot_count) * i) + self.p1.drift_heading
					b = Bullet(self.p1.x, self.p1.y, bullet_hdg, ScatterShot(0, 0).color)
					b.speed = scattershot_speed
					self.p1.bullets.append(b)
			
			elif self.powerup_ids[self.p1.current_powerup] == "missile":
				m = Bullet(self.p1.x, self.p1.y, self.p1.drift_heading, Missile(0, 0).color)
				m.speed = missile_speed
				self.p1.bullets.append(m)

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
				for i in range(scattershot_count):
					bullet_hdg = ((360 / scattershot_count) * i) + self.p2.drift_heading
					b = Bullet(self.p2.x, self.p2.y, bullet_hdg, ScatterShot(0, 0).color)
					b.speed = scattershot_speed
					self.p2.bullets.append(b)
			
			elif self.powerup_ids[self.p2.current_powerup] == "missile":
				m = Bullet(self.p2.x, self.p2.y, self.p2.drift_heading, Missile(0, 0).color)
				m.speed = missile_speed
				self.p2.bullets.append(m)
			
			self.p2.assign_powerup(0)

		self.p1.update()
		self.p1.speed *= friction
		
		self.p2.update()
		self.p2.speed *= friction

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
				if bullet.color != Missile(0, 0).color:
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
				if bullet.color != Missile(0, 0).color:
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
					if bullet.color == Missile(0, 0).color:
						self.p1.missile_exploded = True
						self.p1.missile_explosion_x = bullet.x
						self.p1.missile_explosion_y = bullet.y
						if self.dist(bullet.x, bullet.y, self.p1.x, self.p1.y) <= self.p1.collider_size + self.p1.missile_explosion_radius:
							print("BLUE WINS")
							# self.running = False
						
						if self.dist(bullet.x, bullet.y, self.p2.x, self.p2.y) <= self.p2.collider_size + self.p2.missile_explosion_radius:
							print("RED WINS")
							# self.running = False
					
					self.p1.bullets.remove(bullet)

			# Player 2
			for bullet in self.p2.bullets:
				if bullet.wall_collider.colliderect(wall.collider):
					if bullet.color == Missile(0, 0).color:
						self.p2.missile_exploded = True
						self.p2.missile_explosion_x = bullet.x
						self.p2.missile_explosion_y = bullet.y
						if self.dist(bullet.x, bullet.y, self.p1.x, self.p1.y) <= self.p1.collider_size + self.p1.missile_explosion_radius:
							print("BLUE WINS")
							# self.running = False
						
						if self.dist(bullet.x, bullet.y, self.p2.x, self.p2.y) <= self.p2.collider_size + self.p2.missile_explosion_radius:
							print("RED WINS")
							# self.running = False
					
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

		# Missile Explosion Fade Player 1
		if self.p1.missile_exploded:
			self.p1.missile_timer += 1

		if self.p1.missile_timer > missile_fade:
			self.p1.missile_exploded = False
			self.running = False

		# Missile Explosion Fade Player 2
		if self.p2.missile_exploded:
			self.p2.missile_timer += 1

		if self.p2.missile_timer > missile_fade:
			self.p2.missile_exploded = False
			self.running = False

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

		if self.p1.missile_exploded:
			pygame.draw.ellipse(self.win, (255, 255, 255), (self.p1.missile_explosion_x - self.p1.missile_explosion_radius,
															self.p1.missile_explosion_y - self.p1.missile_explosion_radius,
															self.p1.missile_explosion_radius * 2,
															self.p1.missile_explosion_radius * 2
															))
		
		if self.p2.missile_exploded:
			pygame.draw.ellipse(self.win, (255, 255, 255), (self.p2.missile_explosion_x - self.p2.missile_explosion_radius,
															self.p2.missile_explosion_y - self.p2.missile_explosion_radius,
															self.p2.missile_explosion_radius * 2,
															self.p2.missile_explosion_radius * 2
															))

		pygame.display.update()

		# if self.p1.missile_exploded or self.p2.missile_exploded:
		# 	if not self.running:
		# 		sleep(3)

	# Gameplay functions

	def get_spawn_location(self):
		"""Finds a suitable random spawn location for a powerup, staying within the
		boundaries and avoiding all walls.
		
		Returns:
			tuple -- Contains the x and y coordinates for the suitable location
		"""

		x = randint(5, self.width - 5)
		y = randint(5, self.height - 5)
		size = ScatterShot(0, 0).radius
		rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
		for wall in self.levels[self.current_level]:
			if wall.collider.colliderect(rect):
				self.get_spawn_location()

		return (x, y)

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


if __name__ == "__main__":
	game = AstroRockets((1280, 720), "AstroRockets", (0, 0, 0))
	while True:
		main()
		game.running = True
