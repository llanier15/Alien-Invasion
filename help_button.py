import pygame.font

class HelpButton():
	
	def __init__(self, ai_settings, screen, msg):
		"""Initialize button attributes."""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		
		# Set the dimensions of the button.
		self.width, self.height = 180, 56
		self.button_color = (0, 0, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont('arialblack', 36)
		
		# Buttons rect and center it.
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.centerx = self.screen_rect.centerx + 150
		self.rect.centery = self.screen_rect.centery
		
		# Prepping button message.
		self.prep_msg(msg)
		
		def prep_msg(self, msg):
			"""Turn msg into a rendered img and center text."""
			self.msg_img = self.font.render(msg, True, self.text_color,
			                               self.button_color)
			self.msg_img_rect = self.msg_img.get_rect()
			self.msg_img_rect.center = self.rect.center
			
		def draw_help(self):
			"""Draw blank button and message."""
			self.screen.fill(self.button_color, self.rect)
			self.screen.blit(self.msg_img, self.msg_img_rect)
