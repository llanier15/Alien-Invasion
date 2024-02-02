import sys
from time import sleep

import pygame
import pygame.font
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Respond to keypresses."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_p:
		pause(screen, ai_settings)
		
def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet."""
	# Create a new bullet and add it to the bullets group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		
def check_keyup_events(event, ship):
	"""Respond to key releases."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, help_button):
	"""Respond to keypresses and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, 
			    ship, aliens, bullets, mouse_x, mouse_y)
			check_help_button(ai_settings, screen, stats, sb, help_button, ship,
					  aliens, bullets, mouse_x, mouse_y)
	
def check_play_button(ai_settings, screen, stats, sb, play_button, 
         ship, aliens, bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Reset the game settings.
		ai_settings.initialize_dynamic_settings()
		
		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)
		
		# Reset the game stats.
		stats.reset_stats()
		stats.game_active = True
		
		# Reset the scoreboard images.
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()
		
		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def check_help_button(ai_settings, screen, stats, sb, help_button, ship, aliens, bullets, mouse_x, mouse_y):
	"""Show instructions of the game when player clicks Guide."""
	help_clicked = help_button.rect.collidepoint(mouse_x, mouse_y)
	if help_clicked == True and stats.game_active == False:
		instructions = True
		while instructions:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						instructions = False
					elif event.key == pygame.K_q:
						sys.exit()
			screen.fill((230, 230, 230))
			
			pygame.font.init()
			screen_rect = screen.get_rect()
			
			myfont = pygame.font.SysFont('Consola', 80)
			text = myfont.render('Welcome to Alien Invasion!', True, (0, 185, 0), ai_settings.bg_color)
			text1_rect = text.get_rect()
			text1_rect.centerx = screen_rect.centerx
			text1_rect.centery = screen_rect.centery - 300
			screen.blit(text, text1_rect)
			
			msg1 = 'The objective of this game is to destroy the fleet of aliens before it reaches your spaceship or earth!'
			msg2 = ' 1. You have 4 ships available, but if an alien crashes into your spaceship or onto earth your current'
			msg3 = '    spaceship will be destroyed.'
			msg4 = ' 2. Every time you lose a spaceship, the level which you are on will restart.'
			msg5 = ' 3. It is GAME OVER when you lose all of your spaceships, located in top left corner.'
			msg6 = ' 4. The spaceship can shoot only 3 bullets at a time, but it takes one to shoot down an alien.'
			msg7 = ' 5. Every time you destroy an alien, you accumulate points! Can you get the high score?'
			msg8 = ' 6. Every time you shoot down the fleet of aliens you go to the next level, but the aliens are faster!'
			msg9 = ' 7. Move your spaceship with the Left and Right arrow keys, press Spacebar to shoot!'
			msg10 = ' 8. While playing you can press Q to quit, and P to pause the game.'
			messages = [msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9, msg10]
			
			count = 0
			for message in messages:
				myfont = pygame.font.SysFont('Consola', 30)
				text = myfont.render(message, True, (0, 0, 0), ai_settings.bg_color)
				text2_rect = text.get_rect()
				text2_rect.left = 80
				text2_rect.top = 180 + count*38
				count += 1
				screen.blit(text, text2_rect)
			
			myfont = pygame.font.SysFont('Consola', 32)
			text = myfont.render('Press C to continue to the menu.', True, (185, 0, 0), 
					  ai_settings.bg_color)
			text1_rect = text.get_rect()
			text1_rect.centerx = screen_rect.centerx
			text1_rect.centery = screen_rect.centery + 275
			screen.blit(text, text1_rect)
			
			pygame.display.flip()
                        
def pause(screen, ai_settings):
	paused = True
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					sys.exit()
		screen.fill((230, 230, 230))
		
		pygame.font.init()
		screen_rect = screen.get_rect()
		
		myfont = pygame.font.SysFont('Consola', 80)
		text = myfont.render('Paused Game!', True, (0, 185, 0), ai_settings.bg_color)
		text1_rect = text.get_rect()
		text1_rect.center = screen_rect.center
		screen.blit(text, text1_rect)
		
		myfont = pygame.font.SysFont('Consola', 32)
		text = myfont.render('Press C to continue playing or Q to quit.', True, (185, 0, 0))
		text2_rect = text.get_rect()
		text2_rect.centerx = screen_rect.centerx
		text2_rect.centery = screen_rect.centery + 70
		screen.blit(text, text2_rect)
		pygame.display.flip()
		
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, help_button):
	"""Update images on the screen and flip to the new screen."""
	screen.fill(ai_settings.bg_color)
	
	# Redraw all bullets behind ship and aliens.
	for bullet in bullets:
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	# Draw the score info.
	sb.show_score()
	
	# Draw the play button if the game is inactive.
	if stats.game_active == False:
		play_button.draw_button()
		help_button.draw_help()
		
	# Make the most recently drawn screen visible.
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Update position of bullets and get rid of old bullets."""
	# Update bullet positions.
	bullets.update()
	
	# Get rid of bullets that have disappeared off screen.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
	    aliens, bullets)

def check_high_score(stats, sb):
	"""Check to see if there's a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
	"""Respond to bullet-alien collisions."""
	# Remove any bullets and aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:
		# If the entire fleet is destroyed, start a new level.
		bullets.empty()
		ai_settings.increase_speed()
		
		# Increase level.
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen."""
	available_space_y = (ai_settings.screen_height - 
	                        (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row."""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens."""
	# Create an alien and find the number of aliens in a row.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
	    alien.rect.height)
	
	# Create the fleet of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
			    row_number)

def check_fleet_edges(ai_settings, aliens):
	"""Respond appropriately if any aliens have reached an edge."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to ship being hit by alien."""
	if stats.ships_left > 0:
		# Decrement ships_left.
		stats.ships_left -= 1
		
		# Update scoreboard
		sb.prep_ships()
		
		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()
		
		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		# Pause
		sleep(0.5)
		
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Check if any aliens have reached the bottom of screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break
	
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Check if the fleet is at an edge,
	and then update the positions of all aliens in the fleet."""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	# Look for alien-ship collisions.
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
	
	# Look for aliens hitting the bottom.
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

