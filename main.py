#! /usr/bin/python
# -*- coding: utf-8 -*-

#This file is part of RogueBox Adventures.
#
#    RogueBox Adventures is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RogueBox Adventures is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RogueBox Adventures.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import time
from time import sleep as sleep
import sys
import os

from fluent.runtime import FluentLocalization, FluentResourceLoader

language = input("Choose a language (en for English, ca for Catalan): ")

if language == "en":
    loader = FluentResourceLoader("l10n/en")
    resource_file = "main.ftl"
elif language == "ca":
    loader = FluentResourceLoader("l10n/ca")
    resource_file = "main2.ftl"
else:
    print("Invalid language choice. Defaulting to English.")
    loader = FluentResourceLoader("l10n/en")
    resource_file = "main.ftl"

l10n = FluentLocalization([language], [resource_file], loader)

low_res = False
gcwz_input = False
home_save = False
cheat_mode = False
disable_window_1280 = False

Time_ready = False
entrance_x = 0
entrance_y = 0

basic_path = os.path.dirname(os.path.realpath('main.py')) #just get the execution path for resources

for t in sys.argv:
	
	if t == '-m':
		p = os.path.expanduser(basic_path)
		lf = open('rba.desktop','w')
		lf.write('[Desktop Entry]\n') #DUBTE
		lf.write('Type=Application\n')
		lf.write('Name=RogueBox Adventures\n')
		lf.write('Comment=A RogueBox Game\n')
		lf.write('Exec=sh ' + p + os.sep + 'LIB' + os.sep + 'run.sh\n')
		lf.write('Icon=' + p + os.sep + 'icon_big.png\n')
		lf.write('Terminal=false\n')
		lf.write('Categories=Game;')
		lf.close()
		
		rf_path = p + os.sep + 'LIB' + os.sep + 'run.sh'
		rf = open(rf_path,'w')
		rf.write('#This file was generated automatically. Please don\'t change anything.\n') #DUBTE
		rf.write('cd ' + p + '\n')
		rf.write('python ' + p + os.sep + 'run.py')
		
		sys_com = 'chmod +x ' + p + os.sep + 'rba.desktop'
		os.system(sys_com)
		exit(0)
	
	if t == '-c':
		cheat_mode = True
		
	if t == '-g':
		gcwz_input = True
		
	if t == '-h':
		home_save = True
		
lib_path = basic_path + os.sep + 'LIB'
data_path = basic_path + os.sep + 'DATA'
if home_save == False:
	save_path = basic_path + os.sep + 'SAVE' + os.sep + 'World0'
else:
	save_path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' + os.sep + 'SAVE' + os.sep + 'World0' #DUBTE
 
path = save_path.replace(os.sep+'World0','')
if os.path.exists(path) == False:
	for c in range(0,5):
		ph = path +  os.sep + 'World' + str(c)
		os.makedirs(ph)
del path

playing = False
sys.path.append(lib_path)
max_map_size = 52
monitor = [0,0]

try:
	import cPickle as p
except:
	import pickle as p
	
try:
	p.DEFAULT_PROTOCOL=0
except:
	p.HIGHEST_PROTOCOL=0

import random
from preset_settings import *
if gcwz_input == True:
	from getch_gcwz import *
else:
	from getch import *
from tile import tile
from attribute import attribute
from item import *
from countdown import *
try:
	import pygame_sdl2 as pygame
except:
	import pygame
from gra_files import *
from util import *
from monster import monster
from copy import deepcopy
from buffs import buffs
from quest import *
from itemlist import *
from tilelist import *
from questlist import *
from monsterlist import *
from text import *
from skill import *
from dialog import *
from version import *

game_options = game_options(basic_path,home_save)

if game_options.check_version == 1:
	ver_string = check_version()
else:
	ver_string = ' '
		
class g_screen():
	
	def __init__(self, mode = game_options.screenmode, show_logo = True):
		
		global disable_window_1280
		
		string = 'RogueBoxAdventures ' + version +' "'+version_name+'"' #DUBTE
		pygame.display.set_caption(string)
		icon = pygame.image.load('icon_small.png')
		pygame.display.set_icon(icon)
		
		global monitor
		
		self.fire_mode = 0 #0: normal, 1: fire
		self.win_mode = mode
		self.hit_matrix = []
		
		for y in range(0,12):
			self.hit_matrix.append([])
			for  x in range(0,15):
				self.hit_matrix[y].append(0)
		
		pygame.init()
		
		display_info = pygame.display.Info()
		
		if monitor == [0,0]:
			monitor[0] = display_info.current_w
			monitor[1] = display_info.current_h
		
		self.displayx = monitor[0]
		self.displayy = monitor[1]
		
		if self.displayx < 1280 or self.displayy < 720:
			disable_window_1280 = True
		
		#check if the screenmode is 16:9
		
		self.displayx = monitor[0]-monitor[0]%640
		self.displayy = monitor[1]-monitor[1]%360
		winstyle = pygame.FULLSCREEN
		
		if cheat_mode == True and self.win_mode == 2:
			self.win_mode = 1 #disable fullscreen in cheat mode
			
		if disable_window_1280 == True and self.win_mode == 1:
			self.win_mode = 0
		
		if self.win_mode == 2:  
			self.screen = pygame.display.set_mode((self.displayx,self.displayy),winstyle)
			pygame.mouse.set_visible(game_options.mousepad)		
		elif self.win_mode == 0:
			self.screen = pygame.display.set_mode((640,360))
			self.displayx = 640
			self.displayy = 360
		elif self.win_mode == 1:
			dx = min(1280,int(monitor[0]))
			dy = min(720,int((monitor[1])))
			self.screen = pygame.display.set_mode((dx,dy))
			if disable_window_1280 == False:
				self.displayx = 1280
				self.displayy = 720
		
		font_path = basic_path + os.sep + 'FONT' + os.sep + 'PressStart2P.ttf' #DUBTE
		self.font = pygame.font.Font(font_path,8)
		
		if low_res == True:
			str_ext = '_low_res'
		else:
			str_ext = ''
		
		if __name__ == '__main__':
			show_logo = False
				
		if show_logo == True:
			
			display_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
			ran = random.randint(0,4)
			i_name = display_path + 'logo' + str(ran) + str_ext + '.png'
			i = pygame.image.load(i_name)
			i = pygame.transform.scale(i,(self.displayx,self.displayy))
			self.screen.blit(i,(0,0))
			pygame.display.flip()
			getch(640,360,mode=1)
			
			display_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
			ran = random.randint(0,4)
			i_name = display_path + 'logo_gpl' + str_ext + '.png'
			i = pygame.image.load(i_name)
			i = pygame.transform.scale(i,(self.displayx,self.displayy))
			self.screen.blit(i,(0,0))
			pygame.display.flip()
			getch(640,360,mode=1)
			
			display_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
			i_name = display_path + 'oga' + str_ext + '.png'
			i = pygame.image.load(i_name)
			i = pygame.transform.scale(i,(self.displayx,self.displayy))
			self.screen.blit(i,(0,0))
			pygame.display.flip()
			getch(640,360,mode=1)
			
	def render_fade(self,fadeout,fadein,menu='default',color=(48,48,48)):
		
		if menu == 'inventory': #DUBTE
			bg = player.inventory.render(0,0,simulate=True)
		elif menu == 'screen':
			bg = screen.screen
		elif menu == 'loot':
			bg = world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].inventory(simulated=True)
		elif menu == 'brake':
			bg = screen.render_brake(simulate=True)
		elif menu == 'main':
			bg = screen.render_main_menu(simulate=True)
		else:
			bg = self.render(0,True)
		clock = pygame.time.Clock()
		if fadein:
			for i in range(255,0,-15):
				helpsur = pygame.Surface((self.displayx,self.displayy))
				helpsur.fill(color)
				helpsur.set_alpha(i)
				self.screen.blit(bg,(0,0))
				self.screen.blit(helpsur,(0,0))
				pygame.display.flip()
				clock.tick(510)
		if fadeout:
			for i in range(0,255,15):
				helpsur = pygame.Surface((self.displayx,self.displayy))
				helpsur.fill(color)
				helpsur.set_alpha(i)
				self.screen.blit(bg,(0,0))
				self.screen.blit(helpsur,(0,0))
				pygame.display.flip()
				clock.tick(510)
				
	
	def reset_hit_matrix(self):
		
		self.hit_matrix = []
		
		for y in range(0,12):
			self.hit_matrix.append([])
			for  x in range(0,15):
				self.hit_matrix[y].append(0)
				
	def write_hit_matrix(self,x,y,style):
		
		#style: 0:nothing
		#		1:fire_path
		#		2:fire_path_monster
		#		3:miss
		#		4:hit
		#		5:critical
		#		6:heal
		#		7:teleport
		#		8:minus_gem
		#		9:plus_gem
		#		10:plus_fish
		#		11:plus_shoe
		#		12:monster_lvl_up
		#		13:monster_die
		#		14:attention
		#		15:found
		#		16:drop
		#		17:fear
		#		18:blood_minus
		#		19:blood_plus
		#		20:throw
		#		21:minus_item
		#		22:plus_item
		#		23:spellwave
		#		24:wait
		#		25:sleep
				
		xx = x - player.pos[0] + 8
		yy = y - player.pos[1] + 6
		
		try:
			if xx >= 0 and yy >= 0:
				self.hit_matrix[yy][xx] = style
		except:
			None
	def render_lvl_up(self):
		
		s = pygame.Surface((480,360))
		s.fill((255,0,255))
		
		s.blit(gra_files.gdic['display'][86],(0,0))
		
		str_lvl = 'LEVEL:    ' + str(player.lvl) + ' > ' + str(player.lvl+1)
		img_lvl = self.font.render(str_lvl,1,(255,255,255))
		s.blit(img_lvl,(180,103))
		
		if player.training_attack > 50:
			str_attack = 'STRENGTH: ' + str(player.attribute.p_strength) + ' > ' + str(player.attribute.p_strength+1) #DUBTE
		else:
			str_attack = 'POWER:    ' + str(player.attribute.m_strength) + ' > ' + str(player.attribute.m_strength+1)
		img_attack = self.font.render(str_attack,1,(255,255,255))
		s.blit(img_attack,(180,168))
		
		if player.training_def > 50:
			str_def = 'SKILL:    ' + str(player.attribute.p_defense) + ' > ' + str(player.attribute.p_defense+1)
		else:
			str_def = 'WILL:     ' + str(player.attribute.m_defense) + ' > ' + str(player.attribute.m_defense+1)
		img_def = self.font.render(str_def,1,(255,255,255))
		s.blit(img_def,(180,233))
		
		if player.attribute.max_lp < 30*player.lp_boost:
			new_lp = player.attribute.max_lp + player.lp_boost
		else:
			new_lp = player.attribute.max_lp
		
		str_health = 'MAX. LP:  ' + str(player.attribute.max_lp) + ' > ' + str(new_lp)
		img_health = self.font.render(str_health,1,(255,255,255))
		s.blit(img_health,(180,298))
		
		s = pygame.transform.scale(s,(self.displayx,self.displayy))
		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		self.screen.blit(s,(0,0))
		pygame.display.flip()
		
		run = True
		while run:
			ui = getch(screen.displayx,screen.displayy,False,False,mouse=game_options.mousepad)
			if ui == 'e' or ui == 'x':
				run = False
		
	def render_resource_sell(self):
		
		s = pygame.Surface((480,360))
		s.fill((255,0,255))
		
		s.blit(gra_files.gdic['display'][83],(0,0))
		
		str_ore = str(player.inventory.materials.ore)+'/'+str(player.inventory.materials.ore_max)
		img_ore = self.font.render(str_ore,1,(255,255,255))
		s.blit(img_ore,(210,103))
		
		str_gem = str(player.inventory.materials.gem)+'/'+str(player.inventory.materials.gem_max)
		img_gem = self.font.render(str_gem,1,(255,255,255))
		s.blit(img_gem,(210,183))
		
		str_coin = str(player.coins)
		img_coin = self.font.render(str_coin,1,(255,255,255))
		s.blit(img_coin,(210,260))
		
		s = pygame.transform.scale(s,(self.displayx,self.displayy))
		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		self.screen.blit(s,(0,0))
	
	def render_hits(self):
		
		s = pygame.Surface((480,360))
			
		s.fill((255,0,255))
		
		start = 0
		
		for y in range(start,len(self.hit_matrix)):
			for x in range(start,len(self.hit_matrix[0])):
					
				if self.hit_matrix[y][x] == 1:
					s.blit(gra_files.gdic['display'][11],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 2:
					s.blit(gra_files.gdic['display'][12],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 3:
					s.blit(gra_files.gdic['display'][13],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 4:
					s.blit(gra_files.gdic['display'][14],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 5:
					s.blit(gra_files.gdic['display'][15],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 6:
					s.blit(gra_files.gdic['display'][23],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 7:
					s.blit(gra_files.gdic['display'][24],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 8:
					s.blit(gra_files.gdic['display'][26],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 9:
					s.blit(gra_files.gdic['display'][27],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 10:
					s.blit(gra_files.gdic['display'][42],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 11:
					s.blit(gra_files.gdic['display'][43],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 12:
					s.blit(gra_files.gdic['display'][51],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 13:
					s.blit(gra_files.gdic['display'][58],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 14:
					s.blit(gra_files.gdic['display'][59],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 15:
					s.blit(gra_files.gdic['display'][60],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 16:
					s.blit(gra_files.gdic['display'][61],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 17:
					s.blit(gra_files.gdic['display'][62],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 18:
					s.blit(gra_files.gdic['display'][63],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 19:
					s.blit(gra_files.gdic['display'][64],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 20:
					s.blit(gra_files.gdic['display'][65],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 21:
					s.blit(gra_files.gdic['display'][66],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 22:
					s.blit(gra_files.gdic['display'][67],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 23:
					s.blit(gra_files.gdic['display'][70],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 24:
					s.blit(gra_files.gdic['display'][69],(((x-start)*32),(y-start)*32))
				elif self.hit_matrix[y][x] == 25:
					s.blit(gra_files.gdic['display'][75],(((x-start)*32),(y-start)*32))
					
		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		return s
		
	def render_main_menu(self,simulate=False):
		
		if simulate == False:
			screen.render_fade(False,True,'main')
		
		if home_save == False:
			display_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
			alt_path = display_path
		else:
			display_path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' + os.sep #DUBTE
			alt_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep
	
		num = 0
		
		master_loop = True
		run = True
		
		while run:
			
			s = pygame.Surface((640,360))
		
			s.fill((48,48,48))
			try:
				i_name = display_path + 'tmp.png'
				i = pygame.image.load(i_name)
				i.set_colorkey((255,0,255),pygame.RLEACCEL)
				i = i.convert_alpha()
				s.blit(i,(0,0))
			except:
				i_name = alt_path + 'alt.png'
				i = pygame.image.load(i_name)
				i.set_colorkey((255,0,255),pygame.RLEACCEL)
				i = i.convert_alpha()
				s.blit(i,(0,0))
			
			s.blit(gra_files.gdic['display'][16],(0,0))
			
			menu_list = (l10n.format_value("menu-play"),l10n.format_value("menu-options"),l10n.format_value("menu-credits"),l10n.format_value("menu-quit"))
			
			for c in range(0,len(menu_list)):
				name_image = self.font.render(menu_list[c],1,(0,0,0))
				s.blit(name_image,(210,145+(c*45)))
					
			s.blit(gra_files.gdic['display'][4],(185,138+(num*45)))
			
			version_info = 'v'+version+' "'+version_name+'"'
			ver_info_image1 = self.font.render(version_info,1,(0,0,0))
			ver_info_image2 = self.font.render(version_info,1,(255,255,255))
			
			s.blit(ver_info_image1,(107,85))
			s.blit(ver_info_image2,(105,85))
			
			if game_options.check_version == 1:
				
				if ver_string == 'This version is up to date.': #DUBTE
					ver_image = self.font.render(ver_string,1,(0,255,0))
				elif ver_string == 'Old version!!! Please update.':
					ver_image = self.font.render(ver_string,1,(255,0,0))
				else:
					ver_image = self.font.render(ver_string,1,(255,255,255))
				
				ver_image2 = self.font.render(ver_string,1,(0,0,0))

				s.blit(ver_image2,(12,340))
				s.blit(ver_image,(10,340))
			
			if game_options.mousepad == 0:
				s_h = pygame.Surface((160,360))
				s_h.fill((48,48,48))
				s.blit(s_h,(480,0))
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			else:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			if simulate == True:
				return s
				
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
				master_loop = False
				run = False
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = 0
					
			elif ui == 's':
				num += 1
				if num > 3:
					num = 3
			
			elif ui == 'e':
				if num == 0:
					screen.render_load(21)
					test = screen.choose_save_path()
					if test == 'exit':
						master_loop = False
					run = False
				elif num == 1:
					test = screen.render_options()
					if test == 'exit':
						master_loop = False
						run = False
				elif num == 2:
					test = screen.render_credits()
					if test == 'exit':
						master_loop = False
						run = False
				elif num == 3:
					master_loop = False
					run = False
		
		return master_loop
	
	def render_crash(self):
		
		run = True
		
		while run:
			self.screen.fill((48,48,48))
			string = []
			string.append(l10n.format_value("sorry-wrong"))
			string.append(l10n.format_value("check-out"))
			debug_location = '('+save_path+')'
			for c in range(0,6):
				debug_location = debug_location.replace('World'+str(c),'debug.txt')
			string.append(debug_location)
			st = []
			for i in string:
				st.append(self.font.render(i,1,(255,255,255)))
			for j in range(0,len(st)): 	
				self.screen.blit(st[j],(5,25+j*25))
		
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
		
			if ui != 'none':
				run = False
		
	def choose_save_path(self):
		
		global save_path
		global playing
		global master_loop
		global gra_files
		
		gra_files = g_files()
		
		if home_save == True:
			path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' #DUBTE
		else:
			path = basic_path
		
		run = True
		while run:
			
			menu_items = []
		
			for c in range(0,5):
				save_path = path + os.sep + 'SAVE' + os.sep + 'World' + str(c)
				p_attribute = attribute(2,2,2,2,2,10,10)
				p_inventory = inventory()
				player_help = player_class ('-EMPTY SLOT-', 'elysium_0_0', p_attribute,p_inventory, build= 'Auto')
				
				if player_help.name != '-EMPTY SLOT-':
					try:
						if player_help.difficulty == 4:
							gm_string = ' [SB]'
						elif player_help.lp_boost == 1:
							gm_string = ' [E]'
						else:
							gm_string = ' [N]'
					except:
						gm_string = ' [E]'
						
					item_string = player_help.name + ' LVL:' + str(player_help.lvl) + gm_string
				else:
					item_string = l10n.format_value("empty-slot")
					
				menu_items.append(item_string)
				
			menu_items.append(l10n.format_value("erase"))
			menu_items.append(l10n.format_value("back"))
				
			choice = screen.get_choice(l10n.format_value("choose-game"),menu_items,False)
			if choice == 'exit':
				master_loop = False
				run = False
				return('exit') #DUBTE
			
			if choice < 5:
				save_path = path + os.sep + 'SAVE' + os.sep + 'World' + str(choice)
				playing = True
				run = False
				
			elif choice == 5:
				menu_items_erase = []
				
				for d in range(0,5):
					menu_items_erase.append(menu_items[d])
				
				menu_items_erase.append(l10n.format_value("back"))
					
				choice2 = screen.get_choice(l10n.format_value("erase-game"),menu_items_erase,False,'Warning') #DUBTE
				
				if choice2 < 5:
						
					save_path = path + os.sep + 'SAVE' + os.sep + 'World' + str(choice2)
						
					try:	
						
						choice3 = screen.get_choice(l10n.format_value("sure"),(l10n.format_value("no"),l10n.format_value("yes")),False,'Warning')
						
						if choice3 == 1:
							h = ('world.data','time.data','player.data','gods.data') #DUBTE
							
							for i in h:	
								p = save_path + os.sep + i
								os.remove(p)
					except:
						None
						
			elif choice == 6:
				run = False
	
	def save_tmp_png(self):
		
		x = player.pos[0]
		if x-10 < 0:
			x += -1*(x-11)
		elif x+10 > max_map_size-2:
			x -= 10
			
		y = player.pos[1]
		if y-10 < 0:
			y += -1*(y-11)
		elif y+10 > max_map_size-2:
			y -= 10
			
		z =  player.pos[2]
		
		s = pygame.Surface((480,360))
		
		for yy in range(-5,10):
			for xx in range(-7,8):
				
				
				try:
					s.blit(screen.draw_tile(player.on_map,x+xx,y+yy,z,True),((xx+7)*32,(yy+5)*32))
				except:
					None
		
		if home_save == False:
			tmp_save_path = basic_path +os.sep + 'GRAPHIC' + os.sep + 'DISPLAY' + os.sep + 'tmp.png' #DUBTE
		else:
			tmp_save_path = os.path.expanduser('~') + os.sep + '.config' + os.sep + 'RogueBox-Adventures' + os.sep + 'tmp.png'
					
		pygame.image.save(s,tmp_save_path)
							
	
	def re_init(self): # For changing screenmode
		
		options_path = save_path.replace(os.sep + 'World0','') #DUBTE
		
		if game_options.screenmode == 2 and cheat_mode == True:
			game_options.screenmode = 0
		
		mode = game_options.screenmode
		
		if self.win_mode < 2:
			mode += 1
			if mode == 1 and disable_window_1280 == True:
				mode = 2
		else:
			mode = 0
			
		if mode == 2 and cheat_mode == True:
			mode = 0
			
		game_options.screenmode = mode
		save_options(game_options,options_path,os.sep)
		
		self.__init__(game_options.screenmode,False)
	
	def draw_player(self):
		
		s = pygame.Surface((32,32))
		s.fill((255,0,255))
		
		if player.inventory.wearing['Background'] != player.inventory.nothing:
			s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Background'].gra_pos[player.gender][0]][player.inventory.wearing['Background'].gra_pos[player.gender][1]],(0,0))
		
		skinstring = 'SKIN_' + player.gender + '_' + str(player.style +1)
		s.blit(gra_files.gdic['char'][skinstring],(0,0))
		
		if player.inventory.wearing['Clothing'] == player.inventory.nothing:
			underwear_string = player.gender + '_underwear'
			s.blit(gra_files.gdic['char'][underwear_string],(0,0))
											
		try:
			if player.inventory.wearing['Hat'].override_hair == True: #CUIDAO
				render_hair = False
			else:
				render_hair = True
		except:
			render_hair = True
											
		if player.inventory.wearing['Head'] == player.inventory.nothing and render_hair == True:  
			hairstring = 'HAIR_' + player.gender + '_' + str(player.style +1)
			s.blit(gra_files.gdic['char'][hairstring],(0,0))
			
		if player.inventory.wearing['Hat'] != player.inventory.nothing:
			if render_hair:
				hairstring = 'HAIR_' + player.gender + '_' + str(player.style +1)
				s.blit(gra_files.gdic['char'][hairstring],(0,0))
			s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Hat'].gra_pos[player.gender][0]][player.inventory.wearing['Hat'].gra_pos[player.gender][1]],(0,0))
		else:
			if player.inventory.wearing['Hat'] == player.inventory.nothing:
				if player.inventory.wearing['Head'] != player.inventory.nothing:
					if player.inventory.wearing['Head'].artefact == False:
						helmetstring = player.gender + '_' + player.inventory.wearing['Head'].material + '_' + player.inventory.wearing['Head'].classe
					else:
						helmetstring = player.gender + '_' + player.inventory.wearing['Head'].artefact[1]
					s.blit(gra_files.gdic['char'][helmetstring],(0,0))
			else:
				if render_hair == True:
					hairstring = 'HAIR_' + player.gender + '_' + str(player.style +1)
					s.blit(gra_files.gdic['char'][hairstring],(0,0))
					s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Hat'].gra_pos[player.gender][0]][player.inventory.wearing['Hat'].gra_pos[player.gender][1]],(0,0))
														
		if player.inventory.wearing['Clothing'] == player.inventory.nothing:
			if player.inventory.wearing['Body'] != player.inventory.nothing:
				if player.inventory.wearing['Body'].artefact == False:
					armorstring = player.gender + '_' + player.inventory.wearing['Body'].material + '_' + player.inventory.wearing['Body'].classe
				else:
					armorstring = player.gender + '_' + player.inventory.wearing['Body'].artefact[1]
				s.blit(gra_files.gdic['char'][armorstring],(0,0))
	 								
			if player.inventory.wearing['Legs'] != player.inventory.nothing:
				if player.inventory.wearing['Legs'].artefact == False:
					cuissestring = player.gender + '_' + player.inventory.wearing['Legs'].material + '_' + player.inventory.wearing['Legs'].classe
				else:
					cuissestring = player.gender + '_' + player.inventory.wearing['Legs'].artefact[1]
				s.blit(gra_files.gdic['char'][cuissestring],(0,0))
								
			if player.inventory.wearing['Feet'] != player.inventory.nothing:
				if player.inventory.wearing['Feet'].artefact == False:
					shoestring = player.gender + '_' + player.inventory.wearing['Feet'].material + '_' + player.inventory.wearing['Feet'].classe
				else:
					shoestring = player.gender + '_' + player.inventory.wearing['Feet'].artefact[1]
				s.blit(gra_files.gdic['char'][shoestring],(0,0))
				
		else:
			s.blit(gra_files.gdic['clothe'][player.inventory.wearing['Clothing'].gra_pos[player.gender][0]][player.inventory.wearing['Clothing'].gra_pos[player.gender][1]],(0,0))
						
		if player.inventory.wearing['Hold(R)'] != player.inventory.nothing:
			if player.inventory.wearing['Hold(R)'].artefact == False:
				weaponstring = 'WEAPONS_' + player.inventory.wearing['Hold(R)'].material + '_' + player.inventory.wearing['Hold(R)'].classe
			else:
				weaponstring = player.inventory.wearing['Hold(R)'].artefact[1]
			s.blit(gra_files.gdic['char'][weaponstring],(0,0))
											
		if player.inventory.wearing['Hold(L)'] != player.inventory.nothing:
			if player.inventory.wearing['Hold(L)'].artefact == False:
				weaponstring = 'WEAPONS_' + player.inventory.wearing['Hold(L)'].material + '_' + player.inventory.wearing['Hold(L)'].classe
			else:
				player.inventory.wearing['Hold(L)'].artefact[1]
			s.blit(gra_files.gdic['char'][weaponstring],(0,0))
		
		if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].move_group == 'low_liquid':
			help_s = pygame.Surface((32,5))
			help_s.fill((255,0,255))
			s.blit(help_s,(0,27))
		elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].move_group == 'swim':
			help_s = pygame.Surface((32,13))
			help_s.fill((255,0,255))
			s.blit(help_s,(0,19))
		
		if player.buffs.get_buff('invisible') > 0: #DUBTE
			s.set_alpha(120)		
		s.set_colorkey((255,0,255),pygame.RLEACCEL)
		
		try:
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+1][player.pos[0]].upper_tile != None:
				u1 = world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+1][player.pos[0]].upper_tile[0]
				u2 = world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+1][player.pos[0]].upper_tile[1]
				s.blit(gra_files.gdic['tile32'][u2][u1],(0,0))
		except:
			None	
		
		return s

	def draw_tile(self,on_map,x,y,z,visible):
		
		s = pygame.Surface((32,32))
		s.fill((48,48,48))
		
		if x > max_map_size-1 or y > max_map_size-1 or x < 0 or y < 0:
			return s
		
		if world.maplist[z][on_map].known[y][x] == 0:
			s.blit(gra_files.gdic['tile32'][0][3],(0,0))
		else:
			if world.maplist[z][on_map].tilemap[y][x].replace != None:
				old_tile = world.maplist[z][on_map].tilemap[y][x]
				new_tile = world.maplist[z][on_map].tilemap[y][x]
				run = True
				while run:
					new_tile = old_tile.replace
					if new_tile != None:
						 old_tile = new_tile
					else:
						run = False
						
				if len(old_tile.tile_pos) > 2:
					if time.minute%2 == 0:
						s.blit(gra_files.gdic['tile32'][old_tile.tile_pos[1]][old_tile.tile_pos[0]],(0,0))
					else:
						s.blit(gra_files.gdic['tile32'][old_tile.tile_pos[3]][old_tile.tile_pos[2]],(0,0))
				else:
					s.blit(gra_files.gdic['tile32'][old_tile.tile_pos[1]][old_tile.tile_pos[0]],(0,0))
			
			if len(world.maplist[z][on_map].tilemap[y][x].tile_pos) > 2:
				if time.minute%2 == 0:		
					s.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]],(0,0))
				else:
					s.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y][x].tile_pos[3]][world.maplist[z][on_map].tilemap[y][x].tile_pos[2]],(0,0))
			else:
				s.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]],(0,0))
			
			if game_options.rendermode == 0:
				try:
					if gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]] != False:
						if x > 0 and world.maplist[z][on_map].tilemap[y][x-1].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y][x-1] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['v'],(0,0))
						if x < max_map_size and world.maplist[z][on_map].tilemap[y][x+1].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y][x+1] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['v'],(30,0))
						if y > 0 and world.maplist[z][on_map].tilemap[y-1][x].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y-1][x] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['h'],(0,0))
						if y < max_map_size and world.maplist[z][on_map].tilemap[y+1][x].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y+1][x] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['h'],(0,30))
						if  x > 0 and y > 0 and world.maplist[z][on_map].tilemap[y-1][x-1].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y-1][x-1] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['c'],(0,0))
						if  x < max_map_size and y > 0 and world.maplist[z][on_map].tilemap[y-1][x+1].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y-1][x+1] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['c'],(30,0))
						if  x > 0 and y < max_map_size and world.maplist[z][on_map].tilemap[y+1][x-1].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y+1][x-1] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['c'],(0,30))
						if  x < max_map_size and y < max_map_size and world.maplist[z][on_map].tilemap[y+1][x+1].move_group != world.maplist[z][on_map].tilemap[y][x].move_group and world.maplist[z][on_map].known[y+1][x+1] == 1:
							s.blit(gra_files.gdic['border'][world.maplist[z][on_map].tilemap[y][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x].tile_pos[0]]['c'],(30,30))
				except:
					None
			
				if world.maplist[z][on_map].tilemap[y][x].move_group == 'low_liquid' or world.maplist[z][on_map].tilemap[y][x].move_group == 'swim':
				
					if world.maplist[z][on_map].tilemap[y][x-1].replace != None:
						try:
							if world.maplist[z][on_map].tilemap[y][x-1].replace.ignore_liquid == True:
								mgw = 'solid'
							else:
								mgw = world.maplist[z][on_map].tilemap[y][x-1].replace.move_group
						except:
							mgw = world.maplist[z][on_map].tilemap[y][x-1].replace.move_group
					else:
						try:
							if world.maplist[z][on_map].tilemap[y][x-1].ignore_liquid == True:
								mgw = 'solid'
							else:
								mgw = world.maplist[z][on_map].tilemap[y][x-1].move_group
						except:
							mgw = world.maplist[z][on_map].tilemap[y][x-1].move_group
				
					if world.maplist[z][on_map].tilemap[y][x+1].replace != None:
						try:
							if world.maplist[z][on_map].tilemap[y][x+1].replace.ignore_liquid == True:
								mge = 'solid'
							else:
								mge = world.maplist[z][on_map].tilemap[y][x+1].replace.move_group
						except:
							mge = world.maplist[z][on_map].tilemap[y][x+1].replace.move_group
					else:
						try:
							if world.maplist[z][on_map].tilemap[y][x+1].ignore_liquid == True:
								mge = 'solid'
							else:
								mge = world.maplist[z][on_map].tilemap[y][x+1].move_group
						except:
							mge = world.maplist[z][on_map].tilemap[y][x+1].move_group
					
					if world.maplist[z][on_map].tilemap[y-1][x].replace != None:
						try:
							if world.maplist[z][on_map].tilemap[y-1][x].replace.ignore_liquid == True:
								mgn = 'solid'
							else:
								mgn = world.maplist[z][on_map].tilemap[y-1][x].replace.move_group
						except:
							mgn = world.maplist[z][on_map].tilemap[y-1][x].replace.move_group
					else:
						try:
							if world.maplist[z][on_map].tilemap[y-1][x].ignore_liquid == True:
								mgn = 'solid'
							else:
								mgn = world.maplist[z][on_map].tilemap[y-1][x].move_group
						except:
							mgn = world.maplist[z][on_map].tilemap[y-1][x].move_group
				
					if world.maplist[z][on_map].tilemap[y+1][x].replace != None:
						try:
							if world.maplist[z][on_map].tilemap[y+1][x].replace.ignore_liquid == True:
								mgs = 'solid'
							else:
								mgs = world.maplist[z][on_map].tilemap[y+1][x].replace.move_group
						except:
							mgs = world.maplist[z][on_map].tilemap[y+1][x].replace.move_group
					else:
						try:
							if world.maplist[z][on_map].tilemap[y+1][x].ignore_liquid == True:
								mgs = 'solid'
							else:
								mgs = world.maplist[z][on_map].tilemap[y+1][x].move_group
						except:
							mgs = world.maplist[z][on_map].tilemap[y+1][x].move_group
					
					own_mg = world.maplist[z][on_map].tilemap[y][x].move_group
					
					if (mgw == 'soil' or mgw == 'low_liquid') and own_mg != mgw:
						hs = pygame.Surface((32,32))
						if world.maplist[z][on_map].tilemap[y][x-1].replace == None:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y][x-1].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x-1].tile_pos[0]],(0,0))
						else:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y][x-1].replace.tile_pos[1]][world.maplist[z][on_map].tilemap[y][x-1].replace.tile_pos[0]],(0,0))
						if time.minute%2 == 0:
							hs.blit(gra_files.gdic['edge']['w1'],(0,0))
						else:
							hs.blit(gra_files.gdic['edge']['w2'],(0,0))
						hs.set_colorkey((255,255,255),pygame.RLEACCEL)
						hs = hs.convert_alpha()
						s.blit(hs,(0,0))
				
					if (mge == 'soil' or mge == 'low_liquid') and own_mg != mge:
						hs = pygame.Surface((32,32))  
						if world.maplist[z][on_map].tilemap[y][x+1].replace == None:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y][x+1].tile_pos[1]][world.maplist[z][on_map].tilemap[y][x+1].tile_pos[0]],(0,0))
						else:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y][x+1].replace.tile_pos[1]][world.maplist[z][on_map].tilemap[y][x+1].replace.tile_pos[0]],(0,0))
						if time.minute%2 == 0:
							hs.blit(gra_files.gdic['edge']['e1'],(0,0))
						else:
							hs.blit(gra_files.gdic['edge']['e2'],(0,0))
						hs.set_colorkey((255,255,255),pygame.RLEACCEL)
						hs = hs.convert_alpha()
						s.blit(hs,(0,0))
					
					if (mgn == 'soil' or mgn == 'low_liquid') and own_mg != mgn:
						hs = pygame.Surface((32,32))  
						if world.maplist[z][on_map].tilemap[y-1][x].replace == None:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y-1][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y-1][x].tile_pos[0]],(0,0))
						else:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y-1][x].replace.tile_pos[1]][world.maplist[z][on_map].tilemap[y-1][x].replace.tile_pos[0]],(0,0))
						if time.minute%2 == 0:
							hs.blit(gra_files.gdic['edge']['n1'],(0,0))
						else:
							hs.blit(gra_files.gdic['edge']['n2'],(0,0))
						hs.set_colorkey((255,255,255),pygame.RLEACCEL)
						hs = hs.convert_alpha()
						s.blit(hs,(0,0))
				
					if (mgs == 'soil' or mgs == 'low_liquid') and own_mg != mgs:
						hs = pygame.Surface((32,32))  
						if world.maplist[z][on_map].tilemap[y+1][x].replace == None:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y+1][x].tile_pos[1]][world.maplist[z][on_map].tilemap[y+1][x].tile_pos[0]],(0,0))
						else:
							hs.blit(gra_files.gdic['tile32'][world.maplist[z][on_map].tilemap[y+1][x].replace.tile_pos[1]][world.maplist[z][on_map].tilemap[y+1][x].replace.tile_pos[0]],(0,0))
						if time.minute%2 == 0:
							hs.blit(gra_files.gdic['edge']['s1'],(0,0))
						else:
							hs.blit(gra_files.gdic['edge']['s2'],(0,0))
						hs.set_colorkey((255,255,255),pygame.RLEACCEL)
						hs = hs.convert_alpha()
						s.blit(hs,(0,0))
			
			if visible == False:
				s.blit(gra_files.gdic['display'][6],(0,0))
			
			if world.maplist[z][on_map].npcs[y][x] != 0:
				s.blit(self.draw_monster(x,y,z,on_map,visible),(0,0))
			
			try:
				if world.maplist[z][on_map].tilemap[y+1][x].upper_tile != None:
					u1 = world.maplist[z][on_map].tilemap[y+1][x].upper_tile[0]
					u2 = world.maplist[z][on_map].tilemap[y+1][x].upper_tile[1]
					s.blit(gra_files.gdic['tile32'][u2][u1],(0,0))
					if visible == False:
						s.blit(gra_files.gdic['display'][6],(0,0))
			except:
				None	
			
		return s
	
	def draw_resource_bar(self):
		
		s = pygame.Surface((155,23))
		s.fill((255,0,255))
		s.blit(gra_files.gdic['display'][84],(0,0))
		
		#1 wood
		
		wood_string = str(player.inventory.materials.wood)
		
		if len(wood_string) == 1:
			wood_string = '00'+wood_string
		elif len(wood_string) == 2:
			wood_string = '0'+wood_string
		elif len(wood_string) > 3:
			wood_string = '+++'
			
		hs = pygame.Surface((21,7))
		
		for i in range(0,3):
			hs.blit(gra_files.gdic['num'][wood_string[i]],(i*7,0))
			
		s.blit(hs,(1,15))
		
		if player.inventory.materials.wood >= player.inventory.materials.wood_max:
			s.blit(gra_files.gdic['display'][85],(1,8))
		
		#2 stone
		
		stone_string = str(player.inventory.materials.stone)
		
		if len(stone_string) == 1:
			stone_string = '00'+stone_string
		elif len(stone_string) == 2:
			stone_string = '0'+stone_string
		elif len(stone_string) > 3:
			stone_string = '+++'
			
		hs = pygame.Surface((21,7))
		
		for i in range(0,3):
			hs.blit(gra_files.gdic['num'][stone_string[i]],(i*7,0))
			
		s.blit(hs,(23,15))
		
		if player.inventory.materials.stone >= player.inventory.materials.stone_max:
			s.blit(gra_files.gdic['display'][85],(23,8))
		
		#3 ore
		
		ore_string = str(player.inventory.materials.ore)
		
		if len(ore_string) == 1:
			ore_string = '00'+ore_string
		elif len(ore_string) == 2:
			ore_string = '0'+ore_string
		elif len(ore_string) > 3:
			ore_string = '+++'
			
		hs = pygame.Surface((21,7))
		
		for i in range(0,3):
			hs.blit(gra_files.gdic['num'][ore_string[i]],(i*7,0))
			
		s.blit(hs,(45,15))
		
		if player.inventory.materials.ore >= player.inventory.materials.ore_max:
			s.blit(gra_files.gdic['display'][85],(45,8))
		
		#4 gem
		
		gem_string = str(player.inventory.materials.gem)
		
		if len(gem_string) == 1:
			gem_string = '00'+gem_string
		elif len(gem_string) == 2:
			gem_string = '0'+gem_string
		elif len(gem_string) > 3:
			gem_string = '+++'
			
		hs = pygame.Surface((21,7))
		
		for i in range(0,3):
			hs.blit(gra_files.gdic['num'][gem_string[i]],(i*7,0))
			
		s.blit(hs,(67,15))
		
		if player.inventory.materials.gem >= player.inventory.materials.gem_max:
			s.blit(gra_files.gdic['display'][85],(67,8))
		
		#5 seed
		
		seeds_string = str(player.inventory.materials.seeds)
		
		if len(seeds_string) == 1:
			seeds_string = '00'+seeds_string
		elif len(seeds_string) == 2:
			seeds_string = '0'+seeds_string
		elif len(seeds_string) > 3:
			seeds_string = '+++'
			
		hs = pygame.Surface((21,7))
		
		for i in range(0,3):
			hs.blit(gra_files.gdic['num'][seeds_string[i]],(i*7,0))
			
		s.blit(hs,(89,15))
		
		if player.inventory.materials.seeds >= player.inventory.materials.seeds_max:
			s.blit(gra_files.gdic['display'][85],(89,8))
		
		#6 herbs
		
		herbs_string = str(player.inventory.materials.herb)
		
		if len(herbs_string) == 1:
			herbs_string = '00'+herbs_string
		elif len(herbs_string) == 2:
			herbs_string = '0'+herbs_string
		elif len(herbs_string) > 3:
			herbs_string = '+++'
			
		hs = pygame.Surface((21,7))
		
		for i in range(0,3):
			hs.blit(gra_files.gdic['num'][herbs_string[i]],(i*7,0))
			
		s.blit(hs,(111,15))
		
		if player.inventory.materials.herb >= player.inventory.materials.herb_max:
			s.blit(gra_files.gdic['display'][85],(111,8))
		
		#7 coins
		
		coins_string = str(player.coins)
		
		if len(coins_string) == 1:
			coins_string = '00'+coins_string
		elif len(coins_string) == 2:
			coins_string = '0'+coins_string
		elif len(coins_string) > 3:
			coins_string = '+++'
			
		hs = pygame.Surface((21,7))
		
		for i in range(0,3):
			hs.blit(gra_files.gdic['num'][coins_string[i]],(i*7,0))
			
		s.blit(hs,(133,15))
		
		s.set_colorkey((255,0,255),pygame.RLEACCEL)
		s = s.convert_alpha()
		
		return s
	
	def draw_monster(self,x,y,z,on_map,visible):
		
		invisible = False
		
		if 'invisible' in world.maplist[z][on_map].npcs[y][x].properties and player.buffs.get_buff('see invisible') == 0: #DUBTE
			invisible = True
		
		s = pygame.Surface((32,32))
		s.fill((255,0,255))
		
		if invisible == False:
			if visible == True:
				pos = world.maplist[z][on_map].npcs[y][x].sprite_pos
				s.blit(gra_files.gdic['monster'][pos[1]][pos[0]],(0,0))
			
				if not 'hover' in world.maplist[z][on_map].npcs[y][x].properties:
					if world.maplist[z][on_map].tilemap[y][x].move_group == 'low_liquid':
						help_s = pygame.Surface((32,5))
						help_s.fill((255,0,255))
						s.blit(help_s,(0,27))
					elif world.maplist[z][on_map].tilemap[y][x].move_group == 'swim':
						help_s = pygame.Surface((32,13))
						help_s.fill((255,0,255))
						s.blit(help_s,(0,19))
					
				if '-skill' in world.maplist[z][on_map].npcs[y][x].properties:
					s.blit(gra_files.gdic['display'][73],(0,0))
				elif 'blind' in world.maplist[z][on_map].npcs[y][x].properties:
					s.blit(gra_files.gdic['display'][74],(0,0))
			
				if world.maplist[z][on_map].npcs[y][x].quest_state != 'None':
					s.blit(gra_files.gdic['display'][59],(0,0))
			
				if world.maplist[z][on_map].npcs[y][x].move_border == 10:
					None
				elif world.maplist[z][on_map].npcs[y][x].AI_style == 'ignore':
					s.blit(gra_files.gdic['display'][28],(0,0))
					if not ('pet0' in world.maplist[z][on_map].npcs[y][x].properties or 'pet1' in world.maplist[z][on_map].npcs[y][x].properties or 'pet2' in world.maplist[z][on_map].npcs[y][x].properties or 'npc' in world.maplist[z][on_map].npcs[y][x].properties):
						lvl = str(world.maplist[z][on_map].npcs[y][x].lvl)
						if len(lvl) == 1:
							lvl = '0'+lvl
						elif len(lvl) > 2:
							lvl = lvl[0]+'+'
						s.blit(gra_files.gdic['num'][lvl[0]],(0,6))	
						s.blit(gra_files.gdic['num'][lvl[1]],(0,14))
					elif 'npc' in world.maplist[z][on_map].npcs[y][x].properties:
						s.blit(gra_files.gdic['display'][76],(0,6))
					else:
						s.blit(gra_files.gdic['display'][72],(0,6))
				elif world.maplist[z][on_map].npcs[y][x].AI_style == 'flee':
					s.blit(gra_files.gdic['display'][29],(0,0))
					lvl = str(world.maplist[z][on_map].npcs[y][x].lvl)
					if len(lvl) == 1:
						lvl = '0'+lvl
					elif len(lvl) > 2:
						lvl = lvl[0]+'+'
					s.blit(gra_files.gdic['num'][lvl[0]],(0,6))	
					s.blit(gra_files.gdic['num'][lvl[1]],(0,14))
				elif world.maplist[z][on_map].npcs[y][x].AI_style == 'company':
					s.blit(gra_files.gdic['display'][71],(0,0))
				
					help_sur_0 = pygame.Surface((26,3))
					help_sur_0.fill((48,48,48))
					s.blit(help_sur_0,(3,29))
				
					help_sur_1 = pygame.Surface((24,1))
					help_sur_1.fill((89,0,0))
					s.blit(help_sur_1,(4,30))
				
					hs2_length = max(1,(24*player.pet_lp)/world.maplist[z][on_map].npcs[y][x].basic_attribute.max_lp)
					help_sur_2 = pygame.Surface((hs2_length,1))
					help_sur_2.fill((0,255,0))
					s.blit(help_sur_2,(4,30))
				else:
					s.blit(gra_files.gdic['display'][30],(0,0))
					lvl = str(world.maplist[z][on_map].npcs[y][x].lvl)
					if len(lvl) == 1:
						lvl = '0'+lvl
					elif len(lvl) > 2:
						lvl = lvl[0]+'+'
					s.blit(gra_files.gdic['num'][lvl[0]],(0,6))	
					s.blit(gra_files.gdic['num'][lvl[1]],(0,14))
				
				if world.maplist[z][on_map].npcs[y][x].move_border > 10:
					s.blit(gra_files.gdic['display'][69],(0,0))
				
				if 'invisible' in world.maplist[z][on_map].npcs[y][x].properties:
					s.set_alpha(120)
				
				#lp_string = str(world.maplist[z][on_map].npcs[y][x].lp)
				#lp_image = self.font.render(lp_string,1,(255,255,255))
				#s.blit(lp_image,(0,0))
			
				#lp_string = str(world.maplist[z][on_map].npcs[y][x].basic_attribute.max_lp)
				#lp_image = self.font.render(lp_string,1,(255,255,255))
				#s.blit(lp_image,(0,16))
				
			else:	
				if world.maplist[z][on_map].npcs[y][x].move_border == 10:
					pos = world.maplist[z][on_map].npcs[y][x].sprite_pos
					s.blit(gra_files.gdic['monster'][pos[1]][pos[0]],(0,0))
					s.blit(gra_files.gdic['display'][6],(0,0))
				else:
					coin = random.randint(0,1)
					if coin == 1:
						s.blit(gra_files.gdic['display'][7],(0,0))
					else:
						s.blit(gra_files.gdic['display'][6],(0,0))
		
		s.set_colorkey((255,0,255),pygame.RLEACCEL)
		
		return s
	
	def generate_light_effect(self):
		
		if player.buffs.get_buff('berserk') > 0: #DUBTE
			y = 3
		elif player.buffs.get_buff('night vision') > 0:
			y = 2
		elif player.pos[2] > 0:
			y = 1
		else:
			y= 0
			
		x = time.hour
		
		if player.buffs.get_buff('berserk') > 0:
			alpha = 135
		elif player.buffs.get_buff('night vision') > 0:
			alpha = 60
		elif player.pos[2] == 0:
			if time.hour == 12:
				alpha = 0
			elif time.hour < 12:
				alpha = 60-(time.hour*5)
			elif time.hour > 12:
				alpha = 0+((time.hour-12)*5)
		else:
			alpha = 135
			
		light_color = gra_files.gdic['lightmap'].get_at((x,y))
		
		s = pygame.Surface((640,360))
			
		s.fill(light_color)
		
		if player.buffs.get_buff('light') > 0 and player.buffs.get_buff('berserk') == 0:
			pygame.draw.circle(s,(255,0,255),[270,197],120,0)
			
			help_tile = pygame.Surface((32,32))
			help_tile.fill(light_color)
			fov = world.maplist[player.pos[2]][player.on_map].check_fov(player.pos[0],player.pos[1],6)
			for y in range(0,len(fov)-1):
				for x in range(0,len(fov[y])-1):
					if fov[y][x] == 0:
						s.blit(help_tile,(x*32,y*32))
				
			s.set_colorkey((255,0,255),pygame.RLEACCEL)
		
		s.set_alpha(alpha)
	
		return s
	
	def render(self,mes_num, simulate = False, photo = False):
		
		radius = 6
		
		if player.pos[2] > 0:
			radius = 2
		elif player.pos[2] == 0:
			if time.hour > 22 or time.hour < 4:
				radius = 2 
			elif time.hour > 21 or time.hour < 5:
				radius = 3 
			elif time.hour > 20 or time.hour < 6:
				radius = 4 
			elif time.hour > 19 or time.hour < 7:
				radius = 5 
			
		if player.buffs.get_buff('light') > 0 or player.buffs.get_buff('night vision'):
			radius = 6
			
		if player.buffs.get_buff('blind') > 0:
			radius = 0 
		
		s = pygame.Surface((640,360))
		
		test = message.sget()
		
		s.fill((48,48,48)) #paint it grey(to clear the screen)
		
		start_pos_x = 240 #the center of the main map view
		start_pos_y = 180
					
		ymin = player.pos[1]-6
		ymax = player.pos[1]+6
		xmin = player.pos[0]-8
		xmax = player.pos[0]+7
		
		ry = 0
		
		fow = world.maplist[player.pos[2]][player.on_map].check_fov(player.pos[0],player.pos[1],radius)
		
		for y in range(ymin,ymax):
			rx = 0
			for x in range(xmin,xmax):
				s.blit(screen.draw_tile(player.on_map,x,y,player.pos[2],fow[ry][rx]),(rx*32,ry*32))
				if x == player.pos[0] and y == player.pos[1]:
					s.blit(screen.draw_player(),(rx*32,ry*32))
					player_pos_help = (x,y)
				rx+=1
			ry+=1
		
		s.blit(self.render_hits(),(0,0))
		
		s.blit(screen.generate_light_effect(),(0,0))
		
		if game_options.grit == 1:
			s.blit(gra_files.gdic['display'][77],(0,0)) #render grit
		
		if photo == True:
			
			photo_help = pygame.Surface((480,360))
			photo_help.blit(s,(0,0))
			s = photo_help
			
			return s
		
		if self.fire_mode == 0:
			if (player.lp*100)/player.attribute.max_lp>20 and (player.attribute.hunger*100)/player.attribute.hunger_max>10 and (player.attribute.thirst*100)/player.attribute.thirst_max>10 and (player.attribute.tiredness*100)/player.attribute.tiredness_max>10:
				s.blit(gra_files.gdic['display'][0],(0,0)) #render gui
			else:
				s.blit(gra_files.gdic['display'][25],(0,0)) #render gui_warning #DUBTE
		elif self.fire_mode == 1:
			s.blit(gra_files.gdic['display'][10],(0,0))
			s.blit(gra_files.gdic['display'][41],(start_pos_x+((player_pos_help[0]-player.pos[0])*32)-16,start_pos_y+((player_pos_help[1]-player.pos[1])*32)-16))
		else:
			if (player.lp*100)/player.attribute.max_lp>20 and (player.attribute.hunger*100)/player.attribute.hunger_max>10 and (player.attribute.thirst*100)/player.attribute.thirst_max>10 and (player.attribute.tiredness*100)/player.attribute.tiredness_max>10:
				s.blit(gra_files.gdic['display'][0],(0,0)) #render gui
			else:
				s.blit(gra_files.gdic['display'][25],(0,0)) #render gui_warning
			s.blit(gra_files.gdic['display'][68],(start_pos_x+((player_pos_help[0]-player.pos[0])*32)-16,start_pos_y+((player_pos_help[1]-player.pos[1])*32)-16))
			
		#render tool info
			#1. Axe
		if player.inventory.wearing['Axe'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][44],(0,39))
		else:
			s.blit(gra_files.gdic['display'][46],(0,39))
			if player.inventory.wearing['Axe'].artefact == False:
				axestring = 'WEAPONS_' + player.inventory.wearing['Axe'].material + '_' + player.inventory.wearing['Axe'].classe #DUBTE
			else:
				axestring = player.inventory.wearing['Axe'].artefact[1]
			s.blit(gra_files.gdic['char'][axestring],(0,39))
			s.blit(gra_files.gdic['display'][47],(0,39))
			axe_state = (15*player.inventory.wearing['Axe'].state)/100
			help_sur = pygame.Surface((axe_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(10,67))
			
			#2. Pickaxe
		if player.inventory.wearing['Pickaxe'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][45],(16,39))
		else:
			s.blit(gra_files.gdic['display'][46],(16,39))
			if player.inventory.wearing['Pickaxe'].artefact == False:
				pickaxestring = 'WEAPONS_' + player.inventory.wearing['Pickaxe'].material + '_' + player.inventory.wearing['Pickaxe'].classe
			else:
				pickaxestring = player.inventory.wearing['Pickaxe'].artefact[1]
			s.blit(gra_files.gdic['char'][pickaxestring],(16,39))
			s.blit(gra_files.gdic['display'][47],(16,39))
			pickaxe_state = (15*player.inventory.wearing['Pickaxe'].state)/100
			help_sur = pygame.Surface((pickaxe_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(26,67))
			
			#3. Melee weapon
		if player.inventory.wearing['Hold(R)'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][52],(32,39))
		else:
			s.blit(gra_files.gdic['display'][46],(32,39))
			if player.inventory.wearing['Hold(R)'].artefact == False:
				melee_string = 'WEAPONS_' + player.inventory.wearing['Hold(R)'].material + '_' + player.inventory.wearing['Hold(R)'].classe
			else:
				melee_string = player.inventory.wearing['Hold(R)'].artefact[1]
			s.blit(gra_files.gdic['char'][melee_string],(32,39))
			s.blit(gra_files.gdic['display'][47],(32,39))
			melee_state = (15*player.inventory.wearing['Hold(R)'].state)/100
			help_sur = pygame.Surface((melee_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(42,67))
			
			#4. Magic weapon
		if player.inventory.wearing['Hold(L)'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][53],(48,39))
		else:
			s.blit(gra_files.gdic['display'][46],(48,39))
			if player.inventory.wearing['Hold(L)'].artefact == False:
				magic_string = 'WEAPONS_' + player.inventory.wearing['Hold(L)'].material + '_' + player.inventory.wearing['Hold(L)'].classe
			else:
				magic_string = player.inventory.wearing['Hold(L)'].artefact[1]
			if player.inventory.wearing['Hold(L)'].classe != 'rune staff':
				s.blit(gra_files.gdic['char'][magic_string],(42,39))
			else:
				h_sur = pygame.Surface((32,19))
				h_sur.fill((255,0,255))
				h_sur.blit(gra_files.gdic['char'][magic_string],(0,0))
				h_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
				h_sur = h_sur.convert_alpha()
				s.blit(h_sur,(42,48))	
			s.blit(gra_files.gdic['display'][47],(48,39))
			magic_state = (15*player.inventory.wearing['Hold(L)'].state)/100
			help_sur = pygame.Surface((magic_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(58,67))
			
			#5. Necklace
		if player.inventory.wearing['Neck'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][40],(64,39))
		else:
			s.blit(gra_files.gdic['display'][46],(64,39))
			if player.inventory.wearing['Neck'].artefact == False:
				necklacestring = 'WEAPONS_' + player.inventory.wearing['Neck'].material + '_' + player.inventory.wearing['Neck'].classe
			else:
				necklacestring = player.inventory.wearing['Neck'].artefact[1]
			s.blit(gra_files.gdic['char'][necklacestring],(64,39))
			s.blit(gra_files.gdic['display'][47],(64,39))
			necklace_state = (15*player.inventory.wearing['Neck'].state)/100
			help_sur = pygame.Surface((necklace_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(74,67))
		
			#6. Helmet
		if player.inventory.wearing['Head'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][54],(0,54))
		else:
			s.blit(gra_files.gdic['display'][46],(0,54))
			if player.inventory.wearing['Head'].artefact == False:
				helmet_string = player.gender + '_' + player.inventory.wearing['Head'].material + '_' + player.inventory.wearing['Head'].classe
			else:
				helmet_string = player.gender + '_' + player.inventory.wearing['Head'].artefact[1]
			h_sur = pygame.Surface((32,32))
			h_sur.fill((255,0,255))
			h_sur.blit(gra_files.gdic['char'][helmet_string],(0,0))
			pygame.draw.rect(h_sur,(255,0,255),(0,0,10,32),0)
			pygame.draw.rect(h_sur,(255,0,255),(0,0,32,4),0)
			pygame.draw.rect(h_sur,(255,0,255),(25,0,7,32),0)
			h_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
			h_sur = h_sur.convert_alpha()
			s.blit(h_sur,(0,65))	
			s.blit(gra_files.gdic['display'][47],(0,54))
			helmet_state = (15*player.inventory.wearing['Head'].state)/100
			help_sur = pygame.Surface((helmet_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(10,82))
		
			#7. Armor
		if player.inventory.wearing['Body'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][55],(16,54))
		else:
			s.blit(gra_files.gdic['display'][46],(16,54))
			if player.inventory.wearing['Body'].artefact == False:
				armor_string = player.gender + '_' + player.inventory.wearing['Body'].material + '_' + player.inventory.wearing['Body'].classe
			else:
				armor_string = player.gender + '_' + player.inventory.wearing['Body'].artefact[1]
			h_sur = pygame.Surface((32,32))
			h_sur.fill((255,0,255))
			h_sur.blit(gra_files.gdic['char'][armor_string],(0,0))
			pygame.draw.rect(h_sur,(255,0,255),(0,0,10,32),0)
			pygame.draw.rect(h_sur,(255,0,255),(25,0,7,32),0)
			h_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
			h_sur = h_sur.convert_alpha()
			s.blit(h_sur,(16,55))	
			s.blit(gra_files.gdic['display'][47],(16,54))
			armor_state = (15*player.inventory.wearing['Body'].state)/100
			help_sur = pygame.Surface((armor_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(26,82))
			
			#8. Cuisse
		if player.inventory.wearing['Legs'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][56],(32,54))
		else:
			s.blit(gra_files.gdic['display'][46],(32,54))
			if player.inventory.wearing['Legs'].artefact == False:
				cuisse_string = player.gender + '_' + player.inventory.wearing['Legs'].material + '_' + player.inventory.wearing['Legs'].classe
			else:
				cuisse_string = player.gender + '_' + player.inventory.wearing['Legs'].artefact[1]
			s.blit(gra_files.gdic['char'][cuisse_string],(32,50))	
			s.blit(gra_files.gdic['display'][47],(32,54))
			cuisse_state = (15*player.inventory.wearing['Legs'].state)/100
			help_sur = pygame.Surface((cuisse_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(42,82))
		
			#9. Shoes
		if player.inventory.wearing['Feet'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][57],(48,54))
		else:
			s.blit(gra_files.gdic['display'][46],(48,54))
			if player.inventory.wearing['Feet'].artefact == False:
				shoes_string = player.gender + '_' + player.inventory.wearing['Feet'].material + '_' + player.inventory.wearing['Feet'].classe
			else:
				shoes_string = player.gender + '_' + player.inventory.wearing['Feet'].artefact[1]
			s.blit(gra_files.gdic['char'][shoes_string],(49,46))	
			s.blit(gra_files.gdic['display'][47],(48,54))
			shoes_state = (15*player.inventory.wearing['Feet'].state)/100
			help_sur = pygame.Surface((shoes_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(58,82))	
		
			#10. Ring
		if player.inventory.wearing['Hand'] == player.inventory.nothing:
			s.blit(gra_files.gdic['display'][39],(64,54))
		else:
			s.blit(gra_files.gdic['display'][46],(64,54))
			if player.inventory.wearing['Hand'].artefact == False:
				ring_string = 'WEAPONS_' + player.inventory.wearing['Hand'].material + '_' + player.inventory.wearing['Hand'].classe
			else:
				ring_string = player.inventory.wearing['Hand'].artefact[1]
			s.blit(gra_files.gdic['char'][ring_string],(64,54))
			s.blit(gra_files.gdic['display'][47],(64,54))
			ring_state = (15*player.inventory.wearing['Hand'].state)/100
			help_sur = pygame.Surface((ring_state,1))
			help_sur.blit(gra_files.gdic['display'][48],(0,0))
			s.blit(help_sur,(74,82))
			
		#render resources
		s.blit(screen.draw_resource_bar(),(320,0))
		#render icons
			#1. Use
		if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].use_group == 'None' and world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] == 0:
			s.blit(gra_files.gdic['display'][32],(0,161))
			s.blit(gra_files.gdic['display'][34],(0,161))
		else:
			s.blit(gra_files.gdic['display'][31],(0,161))
			s.blit(gra_files.gdic['display'][33],(0,161))
			use_string = '['+key_name['e']+']action' #DUBTE
			use_image1 = self.font.render(use_string,1,(0,0,0))
			use_image2 = self.font.render(use_string,1,(255,255,255))
			s.blit(use_image1,(36,173))
			s.blit(use_image2,(34,173))
			
			#2. Fire
		if player.inventory.wearing['Hold(L)'] == player.inventory.nothing or player.mp < 2:
			s.blit(gra_files.gdic['display'][32],(0,129))
			s.blit(gra_files.gdic['display'][36],(0,129))
		else:
			s.blit(gra_files.gdic['display'][31],(0,129))
			s.blit(gra_files.gdic['display'][35],(0,129))
			if self.fire_mode == False:
				fire_string = '['+key_name['f']+']fire'
			else:
				fire_string = '['+key_name['x']+']cancel'
			fire_image1 = self.font.render(fire_string,1,(0,0,0))
			fire_image2 = self.font.render(fire_string,1,(255,255,255))
			s.blit(fire_image1,(36,141))
			s.blit(fire_image2,(34,141))
		
			#4.Focus
		s.blit(gra_files.gdic['display'][32],(0,97))#65
		try:
			focus_state = (32*player.mp/player.attribute.max_mp)
		except:
			focus_state = 1
		
		help_sur = pygame.Surface((focus_state,32))
		help_sur.fill((255,0,255))
		help_sur.blit(gra_files.gdic['display'][31],(0,0))
		help_sur.set_colorkey((255,0,255),pygame.RLEACCEL)
		help_sur = help_sur.convert_alpha()
		s.blit(help_sur,(0,97))
		
		if player.mp < player.attribute.max_mp:
			s.blit(gra_files.gdic['display'][38],(0,97))
			focus_string = 'unfocused'
		else:
			s.blit(gra_files.gdic['display'][37],(0,97))
			focus_string = 'focused'
			
		focus_image1 = self.font.render(focus_string,1,(0,0,0))
		focus_image2 = self.font.render(focus_string,1,(255,255,255))
		s.blit(focus_image1,(36,109))#77
		s.blit(focus_image2,(34,109))
		
		# render messages
		
		help_sur = pygame.Surface((480,60))
		help_sur.fill((48,48,48))
		help_sur.set_alpha(120)
		
		mes_pos_y = 345
		
		s.blit(help_sur,(0,300))
		
		mlist = test
		
		for c in range(0,5):
			if c > 2:
				color = (160,160,160)
			elif c > 0:
				color = (206,206,206)
			else:
				color = (255,255,255)
			shadow_image = self.font.render(mlist[c],1,(0,0,0))
			text_image = self.font.render(mlist[c],1,color)
			s.blit(shadow_image,(2,mes_pos_y-(c*10)))
			s.blit(text_image,(0,mes_pos_y-(c*10)))
		
		#render lvl info
		
		lvl_string = str(player.lvl)
		if len(lvl_string) == 1:
			lvl_string = '0'+lvl_string
		lvl_image = self.font.render(lvl_string,1,(255,255,255))
		s.blit(lvl_image,(153,48))
		
		bar_length = 1 + ((319/100)*player.xp)
		xp_surface = pygame.Surface((bar_length,64))
		xp_surface.fill((255,0,255))
		xp_surface.blit(gra_files.gdic['display'][19],(0,0))
		xp_surface.set_colorkey((255,0,255),pygame.RLEACCEL)	
		xp_surface = xp_surface.convert_alpha()
		s.blit(xp_surface,(0,0))
		
		if game_options.mousepad == 1:
			if self.fire_mode == 0:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s.blit(gra_files.gdic['display'][9],(480,0))
		else:
			s_help = pygame.Surface((160,360))
			s_help.fill((48,48,48))
			s.blit(s_help,(480,0))
		
		#render buffs
		
		buffs = player.buffs.sget()
		
		posx = 358 
		posy = 35
		
		for i in buffs:
			if i != ' ':
				buff_shadow = self.font.render(i,1,(0,0,0))
				s.blit(buff_shadow,(posx+2,posy))
				buff_image = self.font.render(i,1,(200,200,200))
				s.blit(buff_image,(posx,posy))
			else:
				None
				
			posy += 20
		
		
		#render date
		
		date_string = time.sget()
		posx = 235
		posy = 10
		
		date_image = self.font.render(date_string[0],1,(0,0,0))
		s.blit(date_image,(posx,posy))
		posy = 20
		time_image = self.font.render(date_string[1],1,(0,0,0))
		s.blit(time_image,(posx,posy))
		
		#render player info
			#lp
		lp_string = str(player.lp) + '/' + str(player.attribute.max_lp)
			
		posx = 13
		posy = 12
		
		if player.lp < 4: 
			lp_image = self.font.render(lp_string,1,(200,0,0))
		else:
			lp_image = self.font.render(lp_string,1,(0,0,0))
		s.blit(lp_image,(posx,posy))
			
			#hunger
		
		hunger_percent = int((100 * player.attribute.hunger) / player.attribute.hunger_max)
		
		hunger_string = str(hunger_percent) + '%'
		
		posx = 75
		posy = 12
		if hunger_percent < 11:
			hunger_image = self.font.render(hunger_string,1,(200,0,0))
		else:
			hunger_image = self.font.render(hunger_string,1,(0,0,0))
		s.blit(hunger_image,(posx,posy))
		
			#trirst
			
		thirst_percent = int((100 * player.attribute.thirst) / player.attribute.thirst_max)
		
		thirst_string = str(thirst_percent) + '%'
		
		posx = 125
		posy = 12
		
		if thirst_percent < 11:
			thirst_image = self.font.render(thirst_string,1,(200,0,0))
		else:
			thirst_image = self.font.render(thirst_string,1,(0,0,0))
		s.blit(thirst_image,(posx,posy))
		
			#tiredness
			
		tiredness_percent = int((100 * player.attribute.tiredness) / player.attribute.tiredness_max)
		
		tiredness_string = str(tiredness_percent) + '%'
		
		posx = 180
		posy = 12
		if tiredness_percent < 11:
			tiredness_image = self.font.render(tiredness_string,1,(200,0,0))
		else:
			tiredness_image = self.font.render(tiredness_string,1,(0,0,0))
		s.blit(tiredness_image,(posx,posy))
		
		if game_options.mousepad == 0:
			s_help = pygame.Surface((640,360))
			s_help.fill((48,48,48))
			s_help.blit(s,(80,0))
			s = s_help		
			
		s = pygame.transform.scale(s,(self.displayx,self.displayy))
		
		self.screen.blit(s,(0,0))
		
		if simulate == False:	
			pygame.display.flip()
		else:
			return s
		
		if test[1] == '~*~':
			return True
		else:
			return False
	
	def render_load(self,num,progress=None):
		
		s = pygame.Surface((640,360))
		
		s.fill((48,48,48)) #paint it grey(to clear the screen)
		
		if num == 0:
			string = l10n.format_value("saved-data")
		elif num == 1:
			string = l10n.format_value("world-data")
		elif num == 2:
			string = l10n.format_value("nothing-found")
		elif num == 3:
			string = l10n.format_value("generate-overworld")
		elif num == 4:
			string = l10n.format_value("generate-caves")
		elif num == 5:
			string = l10n.format_value("saving")
		elif num == 6:
			string = l10n.format_value("time-data")
		elif num == 7:
			string = l10n.format_value("player-data")
		elif num == 8:
			string = l10n.format_value("set-time")
		elif num == 9:
			string = l10n.format_value("generate-player")
		elif num == 10:
			string = l10n.format_value("making-time")
		elif num == 11:
			string = l10n.format_value("something-wrong")
		elif num == 12:
			string = ' '
		elif num == 13:
			string = l10n.format_value("generate-deus")
		elif num == 14:
			string = l10n.format_value("loading-deus")
		elif num == 15:
			string = l10n.format_value("generate-grot")
		elif num == 16:
			string = l10n.format_value("generate-elfish")
		elif num == 17:
			string = l10n.format_value("generate-orcish")
		elif num == 18:
			string = l10n.format_value("generate-desert")
		elif num == 19:
			string = l10n.format_value("initialize-level")
		elif num == 20:
			string = l10n.format_value("please-use")
		elif num == 21:
			string = l10n.format_value("loading-data")
		elif num == 22:
			string = l10n.format_value("generate-elysium")
		
		######add more here
		
		if low_res == False:
			posx = 150
			posy = 200
		else:
			posx=50
			posy= 100
		
		image = self.font.render(string,1,(255,255,255))
		s.blit(image,(posx,posy))
		
		if progress != None:
			s.blit(gra_files.gdic['display'][20],(posx-50,posy+20))
		
			help_sur = pygame.Surface((((progress*320)/100),12))
			help_sur.fill((255,0,255))
			help_sur.blit(gra_files.gdic['display'][21],(0,0))
			help_sur.set_colorkey((255,0,255),pygame.RLEACCEL)	
			help_sur = help_sur.convert_alpha()
		
			s.blit(help_sur,(posx-50,posy+20))
		
		if low_res == False:
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
		
		self.screen.blit(s,(0,0))
			
		pygame.display.flip()
			
	def render_built(self,xmin,xmax,ymin,ymax,style):
		
		start_pos_x = 256 #the center of the main map view
		start_pos_y = 192
		
		price = 0
		
		bg = self.render(0, True)
		
		s = pygame.Surface((640,360))
		s.fill((255,0,255))
		
		if style == 'Room':
			
			build_total = True
			
			for y in range (-ymin,ymax+1):
				for x in range (-xmin,xmax+1):
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
						built_here = 1
						price += 2
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
						built_here = 2
						price += 1
					else: 
						built_here = 0
						
					if world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] != 0:
						built_here = 0
					
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
						built_here = 0
							
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
						if built_here == 1:
							price -= 2 
						elif built_here == 2:
							price -= 1
							built_here = 0
					
					if built_here == 0:
						build_total = False
						
			if build_total == False:
				price = 0
				
			for y in range (-ymin,ymax+1):
				for x in range (-xmin,xmax+1):
							
					if build_total != 0:
					
						if x == xmax or x == -xmin or y == ymax or y == -ymin:
							if x == xmax or x == -xmin:
								if built_here == 1:
									s.blit(gra_files.gdic['built'][1],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_true here #DUBTE
								elif built_here == 2:
									s.blit(gra_files.gdic['built'][6],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_over here
							elif y == ymax or y == -ymin:
								if built_here == 1:
									s.blit(gra_files.gdic['built'][1],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_true here
								elif built_here == 2:
									s.blit(gra_files.gdic['built'][6],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_over here
						else:
							if built_here == 1:
								s.blit(gra_files.gdic['built'][5],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_true here
							elif built_here == 2:
								s.blit(gra_files.gdic['built'][7],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_over
									
					else:
					
						if x == xmax or x == -xmin or y == ymax or y == -ymin:
							if x == xmax or x == -xmin:
								s.blit(gra_files.gdic['built'][0],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_false here
							elif y == ymax or y == -ymin:
								s.blit(gra_files.gdic['built'][0],(start_pos_x+(x*32),start_pos_y+(y*32))) #wall_false here
						else:
							s.blit(gra_files.gdic['built'][4],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_false here
							
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Build Room~' #DUBTE
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
		
			# render wood needed
		
			wood_need = int(price/2) 
			if wood_need == 0 and price != 0:
				wood_need = 1
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' #DUBTE
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = int(price/2)
			if stone_need == 0 and price != 0:
				stone_need = 1
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' #DUBTE
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']change Size' #TIPO2
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!' #TIPO2
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
		
		elif style == 'Doorway': #DUBTE
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'solid' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == True and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] == 0:
				built_here = 1
				price += 2
			else: 
				built_here = 0
				
			if world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] != 0:
						built_here = False
						
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == False:
				if built_here == 1:
					price -= 2 
				elif built_here == 2:
					price -= 1
				built_here = 0
			
			if built_here != 0:
				if built_here == 1:
					s.blit(gra_files.gdic['built'][3],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_true here
				elif built_here == 2:
					s.blit(gra_files.gdic['built'][8],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_over
				
			else:
				s.blit(gra_files.gdic['built'][2],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_false here		
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Built Doorway~' #DUBTE
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
				
			wood_need = 0
		
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' #DUBTE
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = 0
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' #DUBTE
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']change Position' #TIPO2
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!' #TIPO2
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			
		elif style == 'Door':
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] == 0:
				built_here = 1
				price += 2
			elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == True:
				built_here = 2
				price += 1
			else: 
				built_here = 0
				
			if world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] != 0:
						built_here = False
						
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == False:
				if built_here == 1:
					price -= 2 
				elif built_here == 2:
					price -= 1
				built_here = 0
			
			if built_here != 0:
				if built_here == 1:
					s.blit(gra_files.gdic['built'][3],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_true here
				elif built_here == 2:
					s.blit(gra_files.gdic['built'][8],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_over
				
			else:
				s.blit(gra_files.gdic['built'][2],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #door_false here		
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Built Door~' #DUBTE
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
				
			wood_need = price
		
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' #DUBTE
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = 0
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']change Position' #TIPO2
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!' #TIPO2
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
		elif style == 'Stair up': #DUBTE

			if player.pos[2] > 0:
					
				if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]-1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False:
					build_here = 0
				else: 
					build_here = 1
							
				if build_here == 0:
					s.blit(gra_files.gdic['built'][10],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up true icon here
				else:
					s.blit(gra_files.gdic['built'][11],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			else:
				s.blit(gra_files.gdic['built'][11],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Built stair up~' #DUBTE
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
				
			wood_need = 10 
		
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' 
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
		
			stone_need = 40
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']change Position' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
		elif style == 'Stair down':
			
			if player.pos[2] < 15:
				
				if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]+1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False:
					build_here = 0
				else: 
					build_here = 1
							
				if build_here == 0:
					s.blit(gra_files.gdic['built'][12],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up true icon here
				else:
					s.blit(gra_files.gdic['built'][13],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			else:
				s.blit(gra_files.gdic['built'][12],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #stair up false icon here
			
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Built stair down~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render wood needed
				
			wood_need = 10 
		
			wood_string = 'Wood: ' + str(wood_need) + '(' + str(player.inventory.materials.wood) + ')' 
		
			posx = 0
			posy = 15
		
			if wood_need <= player.inventory.materials.wood:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
		
			# render stone needed
			if player.pos[2] > 0:
				stone_need = 40
			else:
				stone_need = 15
		
			stone_string = 'Stone: ' + str(stone_need) + '(' + str(player.inventory.materials.stone) + ')' 
		
			posx = 160
			posy = 15
		
			if stone_need <= player.inventory.materials.stone:
				stone_image = self.font.render(stone_string,1,(255,255,255))
			else:
				stone_image = self.font.render(stone_string,1,(200,0,0))
			
			s.blit(stone_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']change Position' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
		elif style == 'Agriculture':
			
			for y in range (-ymin,ymax+1):
				for x in range (-xmin,xmax+1):
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == False:
						built_here = 1
						price += 1
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
						built_here = 2
						price += 1
					else: 
						built_here = 0
						
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
						if built_here == 1:
							price -= 2 
						elif built_here == 2:
							price -= 1
						built_here = 0
							
					if built_here != 0:
					
						
						if built_here == 1:
							s.blit(gra_files.gdic['built'][15],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_true here
						elif built_here == 2:
							s.blit(gra_files.gdic['built'][16],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_over
									
					else:
					
						s.blit(gra_files.gdic['built'][14],(start_pos_x+(x*32),start_pos_y+(y*32))) #floor_false here
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
			
			# render mode name
			
			name = '~Build Agriculture~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render seeds needed
		
			seed_need = price 
			if seed_need == 0:
				seed_need = 1
			wood_need = seed_need
			stone_need = 0
			wood_string = 'Seeds: ' + str(seed_need) + '(' + str(player.inventory.materials.seeds) + ')' 
		
			posx = 120
			posy = 15
		
			if wood_need <= player.inventory.materials.seeds:
				wood_image = self.font.render(wood_string,1,(255,255,255))
			else:
				wood_image = self.font.render(wood_string,1,(200,0,0))
			
			s.blit(wood_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']change Size' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']BUILT!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
					
		elif style == 'remove':
			
			shape = world.maplist[player.pos[2]][player.on_map].float_building_shape(player.pos[0]+xmin,player.pos[1]+ymin)
			
			for y in range(max(player.pos[1]-8,0),min(player.pos[1]+8,max_map_size)):
				for x in range(max(player.pos[0]-6,0),min(player.pos[0]+6,max_map_size)):
					rx = x-player.pos[0]
					ry = y-player.pos[1]
					if shape[y][x] == 1:
						s.blit(gra_files.gdic['built'][9],(start_pos_x+(rx*32),start_pos_y+(ry*32))) #remove icon here
					
					s.blit(gra_files.gdic['built'][19],(start_pos_x+(xmin*32),start_pos_y+(ymin*32))) #remove icon here
			
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
			# render mode name
			
			name = '~Remove~'
			name_image = self.font.render(name,1,(255,255,255))
			
			posx = 0
			posy = 0
			
			s.blit(name_image,(posx,posy))
			
			# render ---
				
			wood_string = '---' 
		
			posx = 120
			posy = 15
		
			wood_image = self.font.render(wood_string,1,(255,255,255))
			
			s.blit(wood_image,(posx,posy))
			
			# render info line
			
			info_string_0 = '['+key_name['wasd']+']change Size' 
			info_string_1 = '['+key_name['x']+']Leave ['+key_name['e']+']REMOVE!'
		
			posx = 0
			posy = 30
		
			info_image = self.font.render(info_string_0,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			posx = 0
			posy = 40
		
			info_image = self.font.render(info_string_1,1,(255,255,255))
			s.blit(info_image,(posx,posy))
			
			wood_need = 0
			stone_need = 0
		
		if game_options.mousepad == 0:
			s_help = pygame.Surface((640,360))
			s_help.fill((255,0,255))
			s_help.blit(s,(80,0))
			s = s_help
			
		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		s = pygame.transform.scale(s,(self.displayx,self.displayy))
		
		bg.blit(s,(0,0))
		
		self.screen.blit(bg,(0,0))
		
		pygame.display.flip()
		
		return (wood_need,stone_need)
	
	def render_place(self,tile,use_name,no_replace=False):
		
		global player
		
		x = player.pos[0]
		y = player.pos[1]
		
		start_pos_x = 256 #the center of the main map view
		start_pos_y = 192
				
		run = True
		
		while run:
			
			lootable = False
			placeable = True
			plantable = False
			
			#1: check if lootable
			for i in range(9,15):
				if tile.techID == tl.tlist['functional'][i].techID:#this is a workbench
					lootable = True
			
			if tile.techID == tl.tlist['toys'][11].techID:#this is a thinker workshop
				lootable = True
					
			if tile.use_group == 'gather' or tile.use_group == 'switch' or tile.use_group == 'enchantment':
				lootable = True
				
			#2: check if placeable
			if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'dry_entrance':
				placeable = False
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace != None:
				placeable = False
				
			if world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:
				placeable = False
				
			if tile.move_group != 'soil':
				if x == player.pos[0] and y == player.pos[1]:
					placeable = False
			
			if use_name == 'place(indoor)':
				if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].indoor == False:
					placeable = False
					
			if use_name == 'place(outdoor)':
				if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].indoor == True:
					placeable = False
			
			#2.5: check if plantable
			if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].can_grown == True:
				plantable = True
				
			if use_name != 'plant':
				plantable = True #if the object to be placeced no plant plantable is always true 
			
			#3: render
			self.render(0,True)
			
			s = pygame.Surface((640,360))
			
			s.fill((255,0,255))
		
			s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
			
			string1 ='~'+tile.name+'~'
			string1_image = self.font.render(string1,1,(255,255,255))
			s.blit(string1_image,(0,0))
			
			if lootable == False:
				warning = self.font.render('Can\'t be moved later!',1,(200,0,0))
				s.blit(warning,(0,20))
				
			string2 = '['+key_name['wasd']+']Move ['+key_name['e']+']Place! ['+key_name['x']+']Leave'
			string2_image = self.font.render(string2,1,(255,255,255))
			s.blit(string2_image,(0,40))
			
			xx = x - player.pos[0]
			yy = y - player.pos[1]
			
			if placeable == True and plantable == True:
				s.blit(gra_files.gdic['built'][18],(start_pos_x+(xx*32),start_pos_y+(yy*32)))
			else:
				s.blit(gra_files.gdic['built'][17],(start_pos_x+(xx*32),start_pos_y+(yy*32)))
				
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((255,0,255))
				s_help.blit(s,(80,0))
				s = s_help
			
			s.set_colorkey((255,0,255),pygame.RLEACCEL)	
			s = s.convert_alpha()
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
		
			self.screen.blit(s,(0,0))
		
			pygame.display.flip()
			
			#4: user input
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
				global master_loop
				global playing
				global exitgame
				exitgame = True
				try:
					save_options(game_options,options_path,os.sep)
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					del player
				except:
					None
				master_loop = False
				playing = False
				run = False
				return('exit')
			
			if ui == 'w':
				if y > 0 and y > player.pos[1]-2:
					y -= 1
			elif ui == 's':
				if y < max_map_size-1 and y < player.pos[1]+2:
					y += 1
			elif ui == 'a':
				if x > 0 and x > player.pos[0]-2:
					x -= 1
			elif ui == 'd':
				if x < max_map_size-1 and x < player.pos[0]+2:
					x += 1
			elif ui == 'e':
				if placeable == True and plantable == True:
					if no_replace == False:
						replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
					else:
						replace = None
					world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tile)
					world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = deepcopy(replace)
					world.maplist[player.pos[2]][player.on_map].tilemap[y][x].civilisation = True
					if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['misc'][0].techID or world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['global_caves'][4].techID or world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['sewer'][2].techID:
						world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = None
						world.maplist[player.pos[2]][player.on_map].tilemap[y][x].civilisation = False
					if use_name == 'plant':
						mes = 'You planted a '+tile.name+'.'
					else:
						mes = 'You placed a '+tile.name+'.'
					message.add(mes)
					return(x,y)
			elif ui == 'x':
				run = False
				return False
				
		return False#only to be sure
	
	def render_textbox_open(self):
		clock = pygame.time.Clock()
		for i in range(-64,1,6):
			s = pygame.Surface((320,240))
			s.fill((255,0,255))
			s.blit(gra_files.gdic['display'][5],(0,i)) #render gui_transparent over gui
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((255,0,255))
				s_help.blit(s,(80,0))
				s = s_help
			s.set_colorkey((255,0,255),pygame.RLEACCEL)	
			s = s.convert_alpha()
			#s = pygame.transform.scale(s,(self.displayx,self.displayy))
			self.screen.blit(s,(0,0))
			pygame.display.flip()
			clock.tick(256)
		
	def render_request(self,line1,line2,line3,first_call=True,portrait=None):
		#this function just renders 3 lines of text in the textbox
		
		#self.render(0, True)
		
		if first_call == True:
			self.render_textbox_open()
		
		s = pygame.Surface((640,380))
		
		s.fill((255,0,255))
		
		if portrait != None:
			s.blit(gra_files.portraits[portrait],(180,0))
		
		s.blit(gra_files.gdic['display'][5],(0,0)) #render gui_transparent over gui
		
		# render lines
			
		line1_image = self.font.render(line1,1,(255,255,255))
			
		posx = 0
		posy = 0
			
		s.blit(line1_image,(posx,posy))
			
		line2_image = self.font.render(line2,1,(255,255,255))
		posx = 0
		posy = 20
		
		s.blit(line2_image,(posx,posy))
			
			
		line3_image = self.font.render(line3,1,(255,255,255)) 
		
		posx = 0
		posy = 40
		
		s.blit(line3_image,(posx,posy))
		
		if game_options.mousepad == 0:
			s_help = pygame.Surface((640,360))
			s_help.fill((255,0,255))
			s_help.blit(s,(80,0))
			s = s_help
		
		s.set_colorkey((255,0,255),pygame.RLEACCEL)	
		s = s.convert_alpha()
		s = pygame.transform.scale(s,(self.displayx,self.displayy))
		self.screen.blit(s,(0,0))
					
		pygame.display.flip()

	def render_map(self,level=0):
		
		run = True
		
		while run:
			
			m = pygame.Surface((max_map_size,max_map_size))
		
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					try:
						t_col = world.maplist[level][player.on_map].tilemap[y][x].tile_color
					except:
						level = 0
						t_col = world.maplist[level][player.on_map].tilemap[y][x].tile_color
					
					if x > player.pos[0]-2 and x < player.pos[0]+2 and y > player.pos[1]-2 and y < player.pos[1]+2 and level == player.pos[2]: #mark players pos
						m.blit(gra_files.gdic['tile1']['white'],(x,y))
					else:
						if world.maplist[level][player.on_map].known[y][x] == 1:
							m.blit(gra_files.gdic['tile1'][t_col],(x,y))
						elif world.maplist[level][player.on_map].known[y][x] == 0:
							m.blit(gra_files.gdic['tile1']['black'],(x,y))
						else:
							m.blit(gra_files.gdic['tile1']['black'],(x,y))
						
			m = pygame.transform.scale(m,(270,270))
			
			s = pygame.Surface((640,360))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			s.blit(bg,(0,0))
			
			if game_options.mousepad == 1:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			text = '~Map~ [Press['+key_name['x']+'] to leave' #TIPO2
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			lvl_string = 'Level ' + str(level)
			text_image = screen.font.render(lvl_string,1,(0,0,0))
			
			if low_res == False:
				s.blit(text_image,(300,70))
			else:
				s.blit(text_image,(190,50))
			
			s.blit(m,(25,55))
			
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)	
			
			if ui == 'exit':
				global master_loop
				global playing
				global exitgame
				exitgame = True
				screen.render_load(5)
				save(world,player,time,gods,save_path,os.sep)
				screen.save_tmp_png()
				master_loop = False
				playing = False
				run = False
				return('exit')
			
			if ui == 'x':
				run = False
	
	def render_credits(self):
		
		global master_loop
		#global credits_txt
		
		run = True
		
		while run:
			
			ui = screen.get_choice(l10n.format_value("credits"),(l10n.format_value("code"),l10n.format_value("graphic"),l10n.format_value("music"),l10n.format_value("sounds"),l10n.format_value("font"),l10n.format_value("special-thanks")),True)
			
			if ui == 0:
				screen.render_text(credits_txt['code']) #TIPUS3
			elif ui == 1:
				screen.render_multi_text(credits_txt['graphics']) 
			elif ui == 2:
				screen.render_multi_text(credits_txt['music'])
			elif ui == 3:
				screen.render_text(credits_txt['sound'])
			elif ui == 4:
				screen.render_text(credits_txt['font'])
			elif ui == 5:
				screen.render_text(credits_txt['thanks'])
			else:
				run = False
			
			#s = pygame.Surface((640,360))
				
			#bg = pygame.Surface((480,360))
			#bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			#s.blit(bg,(0,0))
			
			#if game_options.mousepad == 1 and low_res == False:
			#	s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			#else:
			#	s_help = pygame.Surface((160,360))
			#	s_help.fill((48,48,48))
			#	s.blit(s_help,(480,0))
			
			#text = '~Credits~ [Press ['+key_name['x']+'] to leave]'
			#text_image = screen.font.render(text,1,(255,255,255))
			#s.blit(text_image,(5,2))#menue title
			
			#credit_items = ('Code & Art: The Mighty Glider [GPL3+/CC0]', 'BGM: Various Artists [CC0]' , 'SFX: Various Artists [CC0]', 'Portraits: PlayCraft/ZeNeRIA29 [CC-BY-SA 3.0]' , 'Font: Cody Boisclair', 'Testing: eugeneloza', 'Special Thanks: forum.freegamedev.net', '                !freegaming@quitter.se')
			
			#for i in range (0,len(credit_items)):
			
			#	text_image = screen.font.render(credit_items[i],1,(0,0,0))
			#	s.blit(text_image,(21,120+i*25))#blit credit_items
				
			#if game_options.mousepad == 0:
			#	s_help = pygame.Surface((640,360))
			#	s_help.fill((48,48,48))
			#	s_help.blit(s,(80,0))
			#	s = s_help
			
			#s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			#self.screen.blit(s,(0,0))
			
			#pygame.display.flip()
			
			#ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			#if ui == 'exit':
			#	master_loop = False
			#	run = False
			#	return('exit')
			
			#if ui == 'x':
			#	run = False
	
	def render_status(self):
		
		player_attribute = (l10n.format_value("strength")+str(player.attribute.p_strength),
							l10n.format_value("skill")+str(player.attribute.p_defense),
							l10n.format_value("power")+str(player.attribute.m_strength),
							l10n.format_value("will")+str(player.attribute.m_defense),
							l10n.format_value("health")+str(player.lp)+'/'+str(player.attribute.max_lp),
							l10n.format_value("skills"))
		attribute_info = ('Strength','Skill','Power','Will','Health') #TIPO3
		
		if player.skill.woodcutting == 'Novice':
			woodcutting_next_lvl = '200'
		else:
			woodcutting_next_lvl = '1000'
		
		if player.skill.mining == 'Novice':
			mining_next_lvl = '200'
		else:
			mining_next_lvl = '1000'
		
		if len(player.buffs.buff_list) > 0:
			next_str = l10n.format_value("buffs")
		else:
			next_str = l10n.format_value("attributes3")
		
		player_skills = (l10n.format_value("weapon-crafting")+player.skill.weapon_crafting,
					  	 l10n.format_value("metallurgy")+player.skill.metallurgy,
						 l10n.format_value("alchemy")+player.skill.alchemy,
						 l10n.format_value("woodcutting")+player.skill.woodcutting+' ('+str(player.skill.woodcutting_progress)+'/'+woodcutting_next_lvl+')',
						 l10n.format_value("mining")+player.skill.mining+' ('+str(player.skill.mining_progress)+'/'+mining_next_lvl+')',
						 next_str)
						 
		skill_info = ('Weapon Crafting','Metallurgy','Alchemy','Woodcutting','Mining') #TIPO3
		
		buff_strings = list(player.buffs.buff_list.keys())
		
		player_buffs = []
		if len(player.buffs.buff_list) > 0:
			for i in buff_strings:
				player_buffs.append(i.upper())
		player_buffs.append(l10n.format_value("attributes"))
		
		run = True
		
		while run:
			c = screen.get_choice(l10n.format_value("attributes2"),player_attribute,True)
			
			if c == 'Break':
				run = False
				return False
				
			if c < 5:
				screen.render_text(texts[attribute_info[c]])
			elif c == 5:
				run2 = True
			
				while run2:
					d = screen.get_choice(l10n.format_value("skills2"),player_skills,True)
					
					if d == 'Break':
						run = False
						run2 = False
						return False
											
					if d < 5:
						screen.render_text(texts[skill_info[d]])
					elif d == 5:
						if len(player.buffs.buff_list) > 0:
							run3 = True
							
							while run3:
								d = screen.get_choice(l10n.format_value("buffs2"),player_buffs,True)
								
								if d == 'Break':
									run = False
									run2 = False
									run3 = False
									return False
									
								if d < len(player.buffs.buff_list):
									try:
										screen.render_text(texts[buff_strings[d]])
									except:
										screen.render_text(texts['unknown buff']) #DUBTE
								elif d == len(player.buffs.buff_list):
									run2 = False
									run3 = False
								
						else:		
							run2 = False
		
	def render_text(self,text,replace_keys=True,more_txt=False,simulation= False):
 		
		run = True
 		
		while run:
 			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if simulation == False:
				if more_txt == False:
					top_text = '[Press ['+key_name['x']+'] to leave]' #TIPO2
				else:
					top_text = '[Press ['+key_name['e']+'] for next page]'
				text_image = screen.font.render(top_text,1,(255,255,255))
				s.blit(text_image,(5,2))#menue title
							
			for i in range (0,len(text)):
			
				text_image = screen.font.render(text[i],1,(0,0,0))
				if low_res == False:
					s.blit(text_image,(60,80+i*25))#blit credit_items
				else:
					s.blit(text_image,(21,36+i*20))#blit credit_items
			
			if simulation == True:
				return s
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					try:
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
						del player
					except:
						None
					master_loop = False
					playing = False
					run = False
					return('exit') #DUBTE
			
			if ui == 'x':
				run = False
			elif ui == 'e' and more_txt == True:
				run = False
							
	def render_multi_text(self,texts):
		
		run = True
		page = 0
		total_pages = len(texts)
		
		while run:
			s = self.render_text(texts[page],simulation=True)
			
			page_txt = 'Page '+str(page+1)+ ' of '+str(total_pages)+' ['+key_name['x']+'] - leave' #TIPO2
			page_image = screen.font.render(page_txt,1,(255,255,255))
			s.blit(page_image,(5,2))#menue title
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 's' or ui == 'd':
				page += 1
				if page > total_pages-1:
					page = 0
			elif ui == 'w' or ui == 'a':
				page -= 1
				if page < 0:
					page = total_pages-1
			elif ui == 'x':
				run = False
				
							  
	def render_options(self):
		
		global key_name
		
		run = True
		num = 0
		options_path = save_path
		for c in range(0,5):
			options_path = options_path.replace(os.sep + 'World' + str(c),'')
		
		while run:
			if screenmode == 'default':
				if game_options.screenmode == 2:
					winm = l10n.format_value("screenmode1")
				elif game_options.screenmode == 1:
					winm = l10n.format_value("screenmode2")
				else:
					winm = l10n.format_value("screenmode3")
			else:
				winm = l10n.format_value("not-option")	
			
			if bgmmode == 'default':
				if game_options.bgmmode != 0:
					audiom = l10n.format_value("bgm1") + str(int(game_options.bgmmode*100)) + '%'
				else:
					audiom = l10n.format_value("bgm2")
			else:
				audiom = l10n.format_value("not-option")
			
			if sfxmode == 'default':
				if game_options.sfxmode != 0:
					sfxm = l10n.format_value("sfx1") +str(int(game_options.sfxmode*100)) + '%'
				else:
					sfxm = l10n.format_value("sfx2")
			else:
				sfxm = l10n.format_value("not-option")
			
			if turnmode == 'default':
				if game_options.turnmode == 1:
					turnm = l10n.format_value("gamemode1")
				else:
					turnm = l10n.format_value("gamemode2")
			else:
				turnm = l10n.format_value("not-option")
			
			if mousepad == 'default':
				if game_options.mousepad == 1:
					mousem = l10n.format_value("use-mouse1")
				else:
					mousem = l10n.format_value("use-mouse2")
			else:
				mousem = l10n.format_value("not-option")
			
			if version_check == 'default':
				if game_options.check_version == 1:
					versm = l10n.format_value("check-version1")
				else:
					versm = l10n.format_value("check-version2")
			else:
				versm = l10n.format_value("not-option")
			
			if rendermode == 'default':
				if game_options.rendermode == 1:
					renderm = l10n.format_value("rendermode1")
				else:
					renderm = l10n.format_value("rendermode2")
			else:
				renderm = l10n.format_value("not-option")
			if grit == 'default':		
				if game_options.grit == 1:
					gritm = l10n.format_value("grit1")
				else:
					gritm = l10n.format_value("grit2")
			else:
				gritm = l10n.format_value("not-option")
			
			if input_nomination == 'default':
				if game_options.input_nomination == 0:
					inputm = l10n.format_value("input-keyboard1")
				elif game_options.input_nomination == 1:
					inputm = l10n.format_value("input-keyboard2")
				else:
					inputm = l10n.format_value("input-keyboard3")
			else:
				inputm = l10n.format_value("not-option")
			
			s = pygame.Surface((640,360))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			s.blit(bg,(0,0))
			
			text = l10n.format_value("choose-option", {"keyname": key_name['e']}) #TIPO2
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
		
			menu_items = (winm,renderm,gritm,audiom,sfxm,turnm,mousem,inputm,versm,l10n.format_value("options-done"))
		
			for i in range (0,len(menu_items)):
			
				text_image = screen.font.render(menu_items[i],1,(0,0,0))
				
				s.blit(text_image,(21,80+i*25))#blit menu_items
				
			s.blit(gra_files.gdic['display'][4],(0,73+num*25))#blit marker
			
			if game_options.mousepad == 1:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
				global master_loop
				global playing
				global exitgame
				global player
				exitgame = True
				try:
					save_options(game_options,options_path,os.sep)
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					del player
				except:
					None
				master_loop = False
				playing = False
				run = False
				return('exit') #DUBTE
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = len(menu_items)-1
				
			if ui == 's':
				num += 1
				if num >= len(menu_items):
					num = 0
			
			if ui == 'x':
				run = False
			
			if ui == 'e':
				
				if num == 0 and screenmode == 'default':
					screen.re_init()
					pygame.display.flip()
					save_options(game_options,options_path,os.sep)
				
				if num == 1 and rendermode == 'default':
					if game_options.rendermode == 0:
						game_options.rendermode = 1
					else:
						game_options.rendermode = 0
						save_options(game_options,options_path,os.sep)
				
				if num == 2 and grit == 'default':
					if game_options.grit == 0:
						game_options.grit = 1
					else:
						game_options.grit = 0
						save_options(game_options,options_path,os.sep)
					
				if num == 3 and bgmmode == 'default':
					ui = screen.get_choice(l10n.format_value("bgm3"),(l10n.format_value("bgm4"),'25%','50%','75%','100%'),True)
					
					if ui == 0:
						game_options.bgmmode = 0
						pygame.mixer.music.pause()
					elif ui == 1:
						game_options.bgmmode = 0.25
						pygame.mixer.music.unpause()
						bgm.check_for_song(force_play=True)
					elif ui == 2:
						game_options.bgmmode = 0.5
						pygame.mixer.music.unpause()
						bgm.check_for_song(force_play=True)
					elif ui == 3:
						game_options.bgmmode = 0.75
						pygame.mixer.music.unpause()
						bgm.check_for_song(force_play=True)
					elif ui == 4:
						game_options.bgmmode = 1
						pygame.mixer.music.unpause()
						bgm.check_for_song(force_play=True)
						
					save_options(game_options,options_path,os.sep)
						
				if num == 4 and sfxmode == 'default':
					
					ui = screen.get_choice(l10n.format_value("sfx3"),(l10n.format_value("sfx4"),'25%','50%','75%','100%'),True)
					
					if ui == 0:
						game_options.sfxmode = 0
					elif ui == 1:
						game_options.sfxmode = 0.25
						sfx.set_loudness()
					elif ui == 2:
						game_options.sfxmode = 0.5
						sfx.set_loudness()
					elif ui == 3:
						game_options.sfxmode = 0.75
						sfx.set_loudness()
					elif ui == 4:
						game_options.sfxmode = 1
						sfx.set_loudness()
						
					save_options(game_options,options_path,os.sep)
				
				if num == 5 and turnmode == 'default':
					if game_options.turnmode == 1:
						game_options.turnmode = 0
					else:
						game_options.turnmode = 1
						
					save_options(game_options,options_path,os.sep)
				
				if num == 6 and mousepad == 'default':
					if game_options.mousepad == 1:
						game_options.mousepad = 0
					else:
						game_options.mousepad = 1
						
					pygame.mouse.set_visible(game_options.mousepad)
						
					save_options(game_options,options_path,os.sep)
				
				if num == 7 and input_nomination == 'default':
					if game_options.input_nomination == 0:
						game_options.input_nomination = 1
					elif game_options.input_nomination == 1:
						game_options.input_nomination = 2
					else:
						game_options.input_nomination = 0
						
					if game_options.input_nomination == 0:
						key_name = {'e':'e','b':'b','x':'x','f':'f','i':'i','.':'.','wasd':'w,s,a,d','ws':'w,s'} #DUBTE
					elif game_options.input_nomination == 1:
						key_name = {'e':'1','b':'3','x':'2','f':'5','i':'4','.':'6','wasd':'D-Pad','ws':'D-Pad'}
					else:
						key_name = {'e':'A','b':'X','x':'B','f':'R','i':'Y','.':'R','wasd':'D-Pad','ws':'D-Pad'}
				
				if num == 8 and version_check == 'default':
					if game_options.check_version == 1:
						game_options.check_version = 0
					else:
						game_options.check_version = 1
					
					save_options(game_options,options_path,os.sep)
					
				if num == 9:
					save_options(game_options,options_path,os.sep)
					run = False
					
			
	def render_brake(self,simulate= False):
		
		run = True
		num = 0
		global exitgame
		global playing
		global player
		
		while run:
			
			s = pygame.Surface((640,360))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			s.blit(bg,(0,0))

			text = l10n.format_value("choosegame-option", {"keyname": key_name['e']})
			text_image = screen.font.render(text,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			menu_items = (l10n.format_value("resume"),l10n.format_value("status"),l10n.format_value("quest-log"),l10n.format_value("message-history"),l10n.format_value("save-exit"),l10n.format_value("options-game"),)
		
			for i in range (0,len(menu_items)):
			
				text_image = screen.font.render(menu_items[i],1,(0,0,0))
				s.blit(text_image,(21,120+i*25))#blit menu_items
				
			s.blit(gra_files.gdic['display'][4],(0,112+num*25))#blit marker
			
			if game_options.mousepad == 1:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
				
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			s = pygame.transform.scale(s,(self.displayx,self.displayy))
			
			if simulate == True:
				return s
			
			self.screen.blit(s,(0,0))
			
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = len(menu_items)-1
				
			if ui == 's':
				num += 1
				if num >= len(menu_items):
					num = 0
			
			if ui == 'x':
				run = False
				screen.render_fade(True,False,'screen')
			
			if ui == 'e':
				
				if num == 0:
					run = False
					screen.render_fade(True,False,'screen')
					
				if num == 1:
					screen.render_status() 
				
				if num == 2:
					screen.render_questlog()
					
				if num == 3:
				
					do = message.render_history()
					if do == 'exit':
						run = False
					
				if num == 4:
					if 'made_intro' in player.quest_variables:
						dungeon_list = ('dungeon_0_0','dungeon_0_1','shop_0_0')
						if not player.on_map in dungeon_list:
							ui = screen.get_choice(l10n.format_value("what-do"),(l10n.format_value("save-here"),l10n.format_value("return-home"),l10n.format_value("save-continuehere"),l10n.format_value("save-continuehome")),True,infos=(l10n.format_value("save-here2"),l10n.format_value("return-home2"),l10n.format_value("save-continuehere2"),l10n.format_value("save-continuehome2")))
						else:
							ui = screen.get_choice(l10n.format_value("what-do"),(l10n.format_value("save-here"),l10n.format_value("save-continuehere")),True,infos=(l10n.format_value("save-here2"),l10n.format_value("save-continuehere2")))
							if ui == 1:
								ui = 2
					else:
						ui = 0
					
					if ui != 'Break':
						if ui < 2:
							exitgame = True
							playing = False
						if ui == 1 or ui == 3:
							sfx.play('teleport')
							player.on_map = 'elysium_0_0'
							pos = world.maplist[0][player.on_map].find_first(tl.tlist['sanctuary'][2])
							player.pos[0] = pos[0]
							player.pos[1] = pos[1]
							player.pos[2] = 0
							player.stand_check()
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
						if ui < 2:
							del player
						run = False
					
				if num == 5:
					do = screen.render_options()
					if do == 'exit':
						run = False
											
		return exitgame
	
	def get_choice(self,headline,choices,allow_chancel,style='Default',infos=None): 
		
		#this function allows the player to make a coice. The choices-variable is a tulpel with strings. The function returns the number of the chosen string inside the tulpel
		
		run = True
		num = 0
		
		while run:
			
			if num > 6:
				plus = 7
			else:
				plus = 0
			
			s = pygame.Surface((640,360))
				
			bg = pygame.Surface((480,360))
			
			if style == 'Default':
				bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			elif style == 'Warning':
				bg.blit(gra_files.gdic['display'][17],(0,0))
				
			s.blit(bg,(0,0))
		
			text_image = screen.font.render(headline,1,(255,255,255))
			
			s.blit(text_image,(5,2))#menue title
			
			menu_items = choices
		
			for i in range (0+plus,min(7+plus,len(menu_items))):
				text_image = screen.font.render(menu_items[i],1,(0,0,0))
				s.blit(text_image,(21,120+(i-plus)*25))#blit menu_items
			
			if infos != None:
				string = infos[num]
				text_image = screen.font.render(string,1,(255,255,255))
				s.blit(text_image,(5,335))
			elif allow_chancel == True:
				string = '['+key_name['e']+'] - choose ['+key_name['x']+'] - leave' #TIPO2
				text_image = screen.font.render(string,1,(255,255,255))
				s.blit(text_image,(5,335))
			else:
				string = '['+key_name['e']+'] - choose'
				text_image = screen.font.render(string,1,(255,255,255))
				s.blit(text_image,(5,335))
			
			if num < 7 and len(menu_items) > 7:
				if style == 'Default':
					s.blit(gra_files.gdic['display'][79],(224,314))
				elif style == 'Warning':
					s.blit(gra_files.gdic['display'][81],(224,314))
					
			if num > 6:
				if style == 'Default':
					s.blit(gra_files.gdic['display'][78],(224,78))
				elif style == 'Warning':
					s.blit(gra_files.gdic['display'][80],(224,78))
			
			if style == 'Default':
				s.blit(gra_files.gdic['display'][4],(0,112+(num-plus)*25))#blit marker
					
			elif style == 'Warning':
				s.blit(gra_files.gdic['display'][18],(0,112+(num-plus)*25))#blit marker
				
			if game_options.mousepad == 1:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			else:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			
			s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			screen.screen.blit(s,(0,0))
			
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					global player
					exitgame = True
					try:
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
					except:
						None
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w':
				num -= 1
				if num < 0:
					num = len(menu_items)-1
				
			if ui == 's':
				num += 1
				if num >= len(menu_items):
					num = 0
				
			if ui == 'e':
				run = False
				return num
				
			if ui == 'x' and allow_chancel == True:
				run = False
				return 'Break' 
		
	def string_input(self, input_message, length, ran_input = 'neutral'):			
			
		run = True
		string = ''
		pos = 0
		x = 0
		y = 0
		
		char_field = (('A','B','C','D','E','F','G','H','a','b','c','d','e','f','g','h'),('I','J','K','L','M','N','O','P','i','j','k','l','m','n','o','p'),('Q','R','S','T','U','V','W','X','q','r','s','t','u','v','w','x'),('Y','Z','y','z','0','1','2','3','4','5','6','7','8','9', '.',','),('(','[','<','{',')',']','>','}','\'','+','-','_','*','/','&','%'))
		
		while run:
			
			s = pygame.Surface((640,360))
			
			s.blit(gra_files.gdic['display'][1],(0,0)) #render background
	
			text_image = screen.font.render(input_message,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			num_stars = length - len(string)
			
			star_string = ''
			
			if num_stars > 0:
				
				for i in range (0,num_stars):
					star_string += '*'
			
			shown_string = string + '_' + star_string 
			
			string_image = screen.font.render(shown_string,1,(255,255,255))
			s.blit(string_image,(5,35))#string so far
				
			for i in range (0,5):#blit chars
				for j in range (0,len(char_field[1])):
						
					if i == y and j == x:
						
						char_image = screen.font.render(char_field[i][j],1,(255,255,255))
						xx = char_image.get_width()
						yy = char_image.get_height()
						hs = pygame.Surface((xx,yy))
						hs.fill((0,0,0))
						hs.blit(char_image,(0,0))
						char_image = hs
						 
					else:
						char_image = screen.font.render(char_field[i][j],1,(0,0,0))
						
					if low_res == False:		
						s.blit(char_image,(55+(j*20),150+(i*20)))
					else:
						s.blit(char_image,(5+(j*20),90+(i*20)))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			text = '['+key_name['e']+'] - Add Char ['+key_name['x']+'] - Del Char ['+key_name['i']+'] - Ran Name ['+key_name['b']+'] - Done' #CUIDAO
			text_image = screen.font.render(text,1,(255,255,255))
			
			if low_res == False:
				s.blit(text_image,(5,335))
			else:
				help_sur = pygame.Surface((320,16))
				help_sur.fill((48,48,48))
				help_sur.blit(text_image,(5,5))
				s.blit(help_sur,(0,224))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			
			screen.screen.blit(s,(0,0))
				
			pygame.display.flip()
						
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
		
			if ui == 'w':
				y -= 1
				if y < 0:
					y = 4
				
			if ui == 's':
				y += 1
				if y > 4:
					y = 0
				
			if ui == 'a':
				x -= 1
				if x < 0:
					x = len(char_field[1])-1
				
			if ui == 'd':
				x += 1
				if x > len(char_field[1])-1:
					x = 0
				
			if ui == 'e':
					
				if pos <= length:
					string += char_field[y][x]
					pos += 1
						
			if ui == 'b':
				run = False
			
			if ui == 'i':
				string = name_generator(ran_input)
				pos = len(string)-1
				
			if ui == 'x':
				if pos > 0:
					pos -= 1
					string = string[:pos]
					
		return string
		
	def render_questlog(self):
		run = True
		while run:
			q = player.questlog.get_quests()
			names = list(q.keys())
			items = []
			for i in names:
				if q[i].status == 0:
					items.append(i+l10n.format_value("new"))
				else:
					items.append(i)
			ui = self.get_choice(l10n.format_value("quest-log2"),items,True)
			if ui != 'Break':
				self.render_text(q[names[ui]].info)
				player.questlog.log[names[ui]].status = 1
			else:
				run = False
		
	def render_boss_defeated(self):
		
		self.reset_hit_matrix()
		
		clock = pygame.time.Clock()
		
		s = pygame.Surface((640,360))
		sh =pygame.Surface((640,360))
		sh.fill((255,255,255))
		
		for si in range(0,640,15):
			s.blit(gra_files.gdic['display'][82],(0,0))
			s.blit(sh,(0+si,0))
		
			if game_options.mousepad == 1:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
		
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			
			screen.screen.blit(s,(0,0))
				
			pygame.display.flip()
			
			clock.tick(510)
			
		sfx.play('win')
						
		ui = getch(screen.displayx,screen.displayy,0,game_options.turnmode,mouse=game_options.mousepad)
		
		for so in range(0,640,15):
			s.blit(gra_files.gdic['display'][82],(0,0))
			s.blit(sh,(-640+so,0))
		
			if game_options.mousepad == 1:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
		
			if game_options.mousepad == 0:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			
			screen.screen.blit(s,(0,0))
				
			pygame.display.flip()
			
			clock.tick(510)
		
	def render_dead(self):
		
		global exitgame
		
		self.reset_hit_matrix()
		
		if player.godmode == True:
			player.respawn()
			message.add(l10n.format_value("you-notdie"))
			return True
		
		run = True
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
			
			s.fill((48,48,48)) #paint it grey(to clear the screen)
		
			text_image = screen.font.render(l10n.format_value("you-die"),1,(255,255,255))
			
			if low_res == False:
				s.blit(text_image,(175,60))
			else:
				s.blit(text_image,(75,60))
		
			if player.difficulty == 3: #you play on roguelike mode
				choose_string = '------------- ['+key_name['x']+'] - END GAME' #TIPO2
			else:#you play on a other mode
				choose_string = '['+key_name['e']+'] - RESPAWN ['+key_name['x']+'] - END GAME' #TIPO2
		
			choose_image = screen.font.render(choose_string,1,(255,255,255))
			
			if low_res == False:
				s.blit(choose_image,(125,200))
			else:
				s.blit(choose_image,(25,200))
			
			if game_options.mousepad == 1 and low_res == False:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			else:
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			
			screen.screen.blit(s,(0,0))
			
			pygame.display.flip()
		
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					if player.difficulty !=3:
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
					else:
						files_to_remove = ('gods.data','player.data','world.data','time.data') #DUBTE
						for i in files_to_remove:
							del_file = save_path + os.sep + i
						try:
							os.remove(del_file)
						except:
							None
					master_loop = False
					playing = False
					run = False
					return('exit') #DUBTE
			
			if ui == 'e' and player.difficulty != 3:
				player.respawn()
				save(world,player,time,gods,save_path,os.sep)
				run = False
			elif ui == 'x':
				player.respawn()
				if player.difficulty != 3:
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
				else:
					files_to_remove = ('gods.data','player.data','world.data','time.data')
					for i in files_to_remove:
						del_file = save_path + os.sep + i
						try:
							os.remove(del_file)
						except:
							None
				run = False
				exitgame = True
					
class maP():
	
	def __init__(self, name, tilemap, visit=False, map_type='overworld',monster_num=1):
		
		self.name = name
		self.known = []
		self.containers = []
		self.tilemap = tilemap
		self.visit = visit
		self.last_visit = 0 #-------test only
		self.map_type = map_type
		self.monster_num = monster_num
		self.build_type = 'Full' #Full: build everything you want, Part: no stairs, None: Buildmode is not callable
		self.thirst_multi_day = 1
		self.thirst_multi_night = 1
		self.no_monster_respawn = False
		self.countdowns = []
		self.npcs = []
		self.monster_plus = 0
		self.monster_count = 0
		self.music_day_original = 'overworld'
		self.music_day = self.music_day_original
		self.music_night_original = 'night'
		self.music_night = self.music_night_original
		self.generation_release = release_number
		
		for y in range (0,max_map_size):
			self.known.append([])
			for x in range (0,max_map_size):
				self.known[y].append(0) 
				
		for y in range (0,max_map_size):
			self.containers.append([])
			for x in range (0,max_map_size):
				self.containers[y].append(0)
				
		for y in range (0,max_map_size):
			self.npcs.append([])
			for x in range (0,max_map_size):
				self.npcs[y].append(0) 
	
	def fill(self, tile):
		for y in range (0,max_map_size):
			for x in range(0,max_map_size):
				self.tilemap[y][x] = deepcopy(tile)
	
	def set_signal(self,x,y):
		
		for yy in range(y-2,y+3):
			for xx in range(x-2,x+3):
				try:
					if (xx == x and yy != y)or(xx != x and yy == y):
						if self.tilemap[yy][xx].techID == tl.tlist['toys'][0].techID: #this is a waiting transmitter
							dist = (((xx-player.pos[0])**2)+((yy-player.pos[1])**2))**0.5
							if dist < 5:
								sfx.play('click2')
							replace = self.tilemap[yy][xx].replace
							self.tilemap[yy][xx] = deepcopy(tl.tlist['toys'][2])
							self.tilemap[yy][xx].replace = replace
							self.countdowns.append(countdown('set_signal',xx,yy,1))
							self.countdowns.append(countdown('transmitter_off',xx,yy,2))
					
						if self.tilemap[yy][xx].techID == tl.tlist['toys'][3].techID: #this is a signal
							dist = (((xx-player.pos[0])**2)+((yy-player.pos[1])**2))**0.5
							if dist < 5:
								sfx.play('click2')
							self.tilemap[yy][xx] = deepcopy(self.tilemap[yy][xx])
							if self.tilemap[yy][xx].tile_pos == (14,4):
								self.tilemap[yy][xx].tile_pos = (14,5)
							else:
								self.tilemap[yy][xx].tile_pos = (14,4)
								
						if self.tilemap[yy][xx].techID == tl.tlist['toys'][6].techID: #this is a auto-door
							dist = dist = (((xx-player.pos[0])**2)+((yy-player.pos[1])**2))**0.5 
							self.tilemap[yy][xx] = deepcopy(self.tilemap[yy][xx])
							if self.tilemap[yy][xx].tile_pos == (14,8):
								self.tilemap[yy][xx].tile_pos = (15,11)
								self.tilemap[yy][xx].move_group = 'soil'
								self.tilemap[yy][xx].transparency = True
								if dist < 9:
									sfx.play('autodoor')
							else:
								if (xx != player.pos[0] or yy != player.pos[1]) and self.npcs[yy][xx] == 0:
									self.tilemap[yy][xx].tile_pos = (14,8)
									self.tilemap[yy][xx].move_group = 'solid'
									self.tilemap[yy][xx].transparency = False
									if dist < 9:
										sfx.play('autodoor')
						
						if self.tilemap[yy][xx].techID == tl.tlist['toys'][8].techID: #this is a fire pit (off)
							dist = (((xx-player.pos[0])**2)+((yy-player.pos[1])**2))**0.5
							if dist < 9:
								sfx.play('flame')
							replace = self.tilemap[yy][xx].replace
							self.tilemap[yy][xx] = deepcopy(tl.tlist['toys'][9]) #set burning fire pit
							self.tilemap[yy][xx].replace = replace
						elif self.tilemap[yy][xx].techID == tl.tlist['toys'][9].techID: #this is a fire pit (burning)
							replace = self.tilemap[yy][xx].replace
							self.tilemap[yy][xx] = deepcopy(tl.tlist['toys'][8]) #set fire pit (off)
							self.tilemap[yy][xx].replace = replace	
					
				except:
					print('error') #DUBTE
	
	def check_fov(self,x,y,dist):
		
		fov = []
		startx = x-8
		starty = y-6
		extreme_coordinates = []
		dist_coordinates = []
		
		for yy in range(0,12):
			fov.append([])
			for xx in range(0,15):
				fov[yy].append(0)
				dist1 = ((8-xx)**2+(6-yy)**2)**0.5
				if dist1 > 0:
					extreme_coordinates.append((xx,yy)) 
					dist_coordinates.append(dist1)
		
		for i in range(0,len(extreme_coordinates)-1):
			c = 0
			run = True
			while run:
				dir_x = (8-extreme_coordinates[i][0])/dist_coordinates[i]
				dir_y = (6-extreme_coordinates[i][1])/dist_coordinates[i]
				
				lx = int(round(8+c*dir_x))
				ly = int(6+c*dir_y)
				
				if ly < 6:
					ly += 1
				elif ly > 6:
					ly -= 1
				
				ldist = ((8-lx)**2+(6-ly)**2)**0.5
				
				try:
					fov[ly][lx] = 1
				except:
					None
				c+=1
				try:
					if lx < 0 or lx > 14 or ly < 0 or ly > 11:
						run = False
					elif ldist >= dist:
						run = False
					elif self.tilemap[starty+ly][startx+lx].transparency == False:
						run = False
				except:
					run = False
		
		return fov
				
	
	def check_los(self,startx,starty,endx,endy):
		
		try:
			if startx > max_map_size or startx < 0 or endx > max_map_size or endx < 0 or starty > max_map_size or starty < 0 or endy > max_map_size or endy < 0:
				return False
			
			vector = (endx-startx,endy-starty)
			dist = (vector[0]**2+vector[1]**2)**0.5
			
			try:
				test1 = self.npcs[starty][startx].inner_view_range
				test2 = self.npcs[starty][startx].outer_view_range
				test3 = self.npcs[starty][startx].active
			except:
				self.npcs[starty][startx].inner_view_range = 5
				self.npcs[starty][startx].outer_view_range = 8
				self.npcs[starty][startx].active = False
				
			
			if dist <= self.npcs[starty][startx].inner_view_range and self.npcs[starty][startx].active == False:
				self.npcs[starty][startx].active = True
				
			if dist > self.npcs[starty][startx].outer_view_range and self.npcs[starty][startx].active == True:
				self.npcs[starty][startx].active = False
			
			if self.npcs[starty][startx].active == False:
				return False
			else:
				return True	
			#uvector = (vector[0]/dist,vector[1]/dist)
		
			#c = 0
			#run = True
		
			#while run:
			#	x = int(round(startx+(c*uvector[0]),0))
			#	y = int(round(starty+(c*uvector[1]),0))
			
				#screen.write_hit_matrix(x,y,15)
			
			#	if x < 0 or x > max_map_size or y < 0 or y > max_map_size:
			#		return False #only to be sure
			#	
			#	if x == endx and y == endy:
			#		return True
			#	
			#	if self.tilemap[y][x].transparency == False:
			#		return False
				
			#	c += 1
				
		except:
			return False
				
	def set_round_frame(self,tile,radius):
		center = int(max_map_size/2)
		for y in range(0,max_map_size):
			for x in range(0,max_map_size):
				range_x = x-center
				range_y = y-center
				if ((range_x**2+range_y**2)**0.5) > radius:
					self.tilemap[y][x] = tile
	
	def set_music(self,day,night,change_original=False):
		
		if day != None:
			self.music_day = day
			if change_original == True:
				self.music_day_original = day
				
		if night != None:
			self.music_night = night
			if change_original == True:
				self.music_night_original = night
	
	def set_monster_view_range(self,inner_range=5,outer_range=8):
		
		for y in range(0,max_map_size):
			for x in range(0,max_map_size):
				if self.npcs[y][x] != 0:
					self.npcs[y][x].inner_view_range = inner_range
					self.npcs[y][x].outer_view_range = outer_range
					
	def make_old_neko_house(self,x,y):
		
		design = (	('*******'),
					('*#####*'), #DUBTE
					('*#c.c#*'),
					('*#.<.+*'),
					('*#c.c#o'),
					('*#####*'),
					('***g***'))
					
		for yy in range (0,7):
			for xx in range(0,7):
				if design[yy][xx] == '*':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['extra'][0])
				elif design[yy][xx] == '#':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['extra'][2])
				elif design[yy][xx] == '.':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['extra'][1])
				elif design[yy][xx] == '<':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['dungeon'][18])
					self.tilemap[y+yy][x+xx].move_group = 'house'
				elif design[yy][xx] == '+':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['functional'][47])
				elif design[yy][xx] == 'g':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['functional'][45])
				elif design[yy][xx] == 'c':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['functional'][43])
					self.tilemap[y+yy][x+xx].replace = deepcopy(tl.tlist['extra'][1])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['overworld'][3])
					self.set_monster_strength(x+xx,y+yy,1)
					self.npcs[y+yy][x+xx].behavior = 'talk'
					self.npcs[y+yy][x+xx].message = 'swap_place'
					self.npcs[y+yy][x+xx].move_groups = ('house','house')
				elif design[yy][xx] == 'o':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['extra'][0])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['special'][27])
					self.set_monster_strength(x+xx,y+yy,1)
				###go on here
	def make_naga_house(self,x,y):
		design = (('I.I'),
				('...'),
				('I.I'))
				
		for yy in range(0,3):
			for xx in range(0,3):
				if design[yy][xx] == 'I':
					ran = random.randint(0,1)
					if ran == 0:
						self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][20])
					else:
						self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][35])
				elif design[yy][xx] == '.':
					ran = random.randint(0,2)
					if ran == 0:
						self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][19])
						self.tilemap[y+yy][x+xx].move_group = 'soil'
					elif ran == 1:
						self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][34])
						self.tilemap[y+yy][x+xx].move_group = 'soil'
					else:
						self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][0])
						
				#add code for container here!!!!
							
	def make_dwarf_bastion(self,x,y):
		
		design = (	('??~~~~~??'),
					('~~~~~~~~~'),
					('~#######~'),
					('~#d.k.d#~'),
					('~#d.w.d#~'),
					('~#d...d#~'),
					('~###+###~'),
					('~~~~-~~~~'),
					('??~~-~~??'))
					
		for yy in range (0,9):
			for xx in range(0,9):
				if design[yy][xx] == '~':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['global_caves'][4])
				elif design[yy][xx] == '#':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['dungeon'][9])
				elif design[yy][xx] == '-':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][31])
				elif design[yy][xx] == '.':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][30])
				elif design[yy][xx] == 'd':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][30])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['statue'][1])
					self.set_monster_strength(x+xx,y+yy,0,preset_lvl=3)
					self.npcs[y+yy][x+xx].lp = 999
				elif design[yy][xx] == '+':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['dungeon'][9])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['special'][23])
					self.set_monster_strength(x+xx,y+yy,0,preset_lvl=3)
					self.npcs[y+yy][x+xx].lp = 999
				elif design[yy][xx] == 'k':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][30])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['special'][24])
					self.set_monster_strength(x+xx,y+yy,0,preset_lvl=3)
					self.npcs[y+yy][x+xx].lp = 999
				elif design[yy][xx] == 'w':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][30])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['special'][25])
					self.set_monster_strength(x+xx,y+yy,2,lvl_bonus=2)
					self.npcs[y+yy][x+xx].lp = 10*player.lp_boost
					if player.difficulty == 4:
						self.npcs[y+yy][x+xx].AI_style = 'ignore'
					
	def make_elfish_hall(self,x,y):
		
		design = (  ('l ##+##  '),
					('  #I.I#  '),
					('###c.e###'),
					('#eI.O.Id#'),
					('+.......+'),
					('#eI...Ie#'),
					('###d.e###'),
					('  #I.I#  '),
					('  ##+##  '))
					
		for yy in range (0,9):
			for xx in range(0,9):
				if design[yy][xx] == ' ':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['local'][0])
				elif design[yy][xx] == '#':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['building'][12])
					self.tilemap[y+yy][x+xx].civilisation = False
				elif design[yy][xx] == '.':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][19])
				elif design[yy][xx] == '+':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['dungeon'][2])
				elif design[yy][xx] == 'I':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][20])
				elif design[yy][xx] == 'O':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['portal'][8])
				elif design[yy][xx] == 'e':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][19])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['statue'][0])
					self.set_monster_strength(x+xx,y+yy,0,preset_lvl=3)
					self.npcs[y+yy][x+xx].lp = 999
				elif design[yy][xx] == 'd':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][19])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['statue'][3])
					self.set_monster_strength(x+xx,y+yy,0,preset_lvl=3)
					self.npcs[y+yy][x+xx].lp = 999
				elif design[yy][xx] == 'c':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['misc'][19])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['statue'][4])
					self.set_monster_strength(x+xx,y+yy,0,preset_lvl=3)
					self.npcs[y+yy][x+xx].lp = 999
				elif design[yy][xx] == 'l':
					self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist['local'][0])
					self.npcs[y+yy][x+xx] = deepcopy(ml.mlist['special'][18])
					self.set_monster_strength(x+xx,y+yy,0,preset_lvl=3)
					self.npcs[y+yy][x+xx].lp = 999
	
	def drunken_finder(self,startx,starty,tile):
		
		x = startx
		y = starty
		
		run = True
		
		while run:
				
			direction = random.randint(0,3)
			
			if direction == 0:
				y -= 1
			elif direction == 1:
				x += 1
			elif direction == 2:
				y += 1
			else:
				x -= 1
				
			if self.tilemap[y][x].techID == tile.techID:
				run = False
		
		return (x,y)
	
	def drunken_walker(self,startx,starty,tile_replace,num_replace):
		
		num = 1
		x = startx
		y = starty
		
		self.tilemap[y][x] = tile_replace
		
		while num < num_replace:
			#step 0: get possible directions
			dir_list = []
			for n in range(-1,2):
				if x+n < max_map_size-2 and x+n > 2:
					if x+n < max_map_size-7 and x+n > 7:
						count = 5
					else:
						count = min((max_map_size-2)-(x+n),(x+n),3)
						
					count = max(count,1)#only to be sure count < 1	
						
					for c in range(0,count):
						dir_list.append([x+n,y])
				if y+n < max_map_size-2 and y+n > 2:
					if y+n < max_map_size-7 and y+n > 7:
						count = 5
					else:
						count = min((max_map_size-2)-(y+n),(y+n),3)
					
					count = max(count,1)#only to be sure count < 1	
						
					for c in range(0,count):
						dir_list.append([x,y+n])
					
			#step 1: set tile new tile
			ran = random.randint(0,len(dir_list)-1)
			x = dir_list[ran][0]
			y = dir_list[ran][1]
			if self.tilemap[y][x].techID != tile_replace.techID:
				self.tilemap[y][x] = tile_replace
				num += 1
				
	def floating(self,startx,starty,tile_fill,tile_border):
		#its important to use a tile_fill that isn't on the map and a tile_border that is on the map 
		
		run = True
		
		self.tilemap[starty][startx] = deepcopy(tile_fill)
		
		while run:
			
			count = 0
			
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					
					if self.tilemap[y][x].techID == tile_fill.techID:
						
						for yy in range(y-1,y+2):
							for xx in range(x-1,x+2):
								
								try:
									if self.tilemap[yy][xx].techID != tile_border.techID and self.tilemap[yy][xx].techID != tile_fill.techID:
										self.tilemap[yy][xx] = deepcopy(tile_fill)
										count += 1
								except:
									None
									
			if count == 0:
				run = False
	
	def float_civilisation(self,start_x,start_y):
				
		tm = []
		
		for y in range(0,max_map_size):
			tm.append([])
			for x in range(0,max_map_size):
				tm[y].append(0)
		
		tm[start_y][start_x] = 1
				
		run = True
		total_count = 1
		
		while run:
			
			count = 0
			
			for yy in range(0,max_map_size):
				for xx in range(0,max_map_size):
					
					if tm[yy][xx] == 1:
						
						for yyy in range(yy-1,yy+2):
							for xxx in range(xx-1,xx+2):
								
								try:
									if tm[yyy][xxx] == 0 and self.tilemap[yyy][xxx].move_group == 'soil' and self.tilemap[yyy][xxx].civilisation == True:
										tm[yyy][xxx] = 1
										count += 1
										total_count += 1
									elif self.tilemap[yyy][xxx].civilisation == False:
										return 0
								except:
									None
					
				if count == 0:
					run = False
		return total_count
	
	def float_building_shape(self,start_x,start_y,mode=1):
		#mode = 0 : single-tile-mode
		#mode = 1 : full-structure-mode
		help_map = []
		for i in range(0,max_map_size):
			help_map.append([])
			for j in range(0,max_map_size):
				help_map[i].append(0)
		
		if self.tilemap[start_y][start_x].civilisation == True:
			help_map[start_y][start_x] = 1
		else:
			return help_map
		
		run = True
		while run == True and mode == 1:
			count = 0
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					if help_map[y][x] == 1:
						for yy in range(y-1,y+2):
							for xx in range(x-1,x+2):
								if self.tilemap[yy][xx].civilisation == True and help_map[yy][xx] == 0:
									help_map[yy][xx] = 1
									count += 1
			
			if count == 0:
				run = False
		
		return help_map	
			
	def get_quarter_size(self,startx,starty):
		
		#this funktion gives back a tulpel with the width and height of a quarter made out of the same tile like the start position
		
		techID = self.tilemap[starty][startx].techID
		
		q_width = 0
		q_height = 0
		
		run_w = True
		run_h = True
		
		while run_w:
			
			if self.tilemap[starty][startx+q_width].techID == techID:
				q_width += 1
			else:
				run_w = False
				
		while run_h:
			
			if self.tilemap[starty+q_height][startx].techID == techID:
				q_height += 1
			else:
				run_h = False
				
		return (q_width,q_height)
			
	def set_frame(self,tile):
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if x == 0 or x == max_map_size-1 or y == 0 or y == max_map_size-1:
					self.tilemap[y][x] = tile
		
	def cut(self, minx, maxx, miny, maxy, replace):
		#everything that is not between min and mx is replaced abainst a tile
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if x < minx or x > maxx or y < miny or y > maxy:
					self.tilemap[y][x] = replace 
		
	def imp(self, start_x, start_y, replace_inner, replace_outer, step_min, step_max, circles, replace_except=None): #dig random caves
		
		#was made to generate random caves but dosn't pleased me. maybe this can be used for mazes.(unused atm)
		
		x = start_x
		y = start_y
		
		for l in range (0,circles):
			
			run = True
			
			while run:
				
				direction = random.randint(0,3)
				
				move_x = 0
				move_y = 0
				
				if direction == 0:
					move_y = -1
				elif direction == 1:
					move_x = 1 
				elif direction == 2:
					move_y = 1
				else:
					move_x= -1
					
				length = random.randint(step_min, step_max)
				
				for m in range (0,length):
					
					x = x + move_x
					y = y + move_y
					
					if x <= 1 or x >= 78 or y <= 1 or y >= 78:
						break
						run = False
					
					self.tilemap[y][x] = replace_inner
					
					for b in range (-1,2):
						for a in range (-1,2):
					
							if self.tilemap[y+a][x+b] != replace_outer and self.tilemap[y+a][x+b] != replace_inner and self.tilemap[y+a][x+b] != replace_except:
								self.tilemap[y+a][x+b] = replace_outer
					
				run = False

	def imp_connect(self,xpos,ypos,replace_inner,replace_except=None,except_replacer=None,style='straight'): #conects two or more points #DUBTE
						
		for a in range (0,len(ypos)-1):
			for b in range(0,len(xpos)-1):
				
				y = ypos[a]
				x = xpos[b]
				
				go = True
				direction = 0 #needed for natural ways. jumps between 0 and 1
				
				while go:
					
					try:
						y_goal = ypos[a+1]
						x_goal = xpos[b+1]
				  
					except:
						y_goal = ypos[0]
						x_goal = xpos[0]
						
					if x == x_goal and y == y_goal:
						go = False
						
					if x_goal - x < 0: #find out if you need to go right or left
						x_direction = -1
					else:
						x_direction = 1
						
					if y_goal - y < 0: #find out if you need to go up or down
						y_direction = -1
					else:
						y_direction = 1
					
					if style == 'straight':	
						if x != x_goal:
						
							x = x + x_direction
					
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
									
						elif y != y_goal:
						
							y = y + y_direction
						
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
								
					elif style == 'natural':
						
						if x != x_goal and direction == 0:
						
							x = x + x_direction
					
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
									
						elif y != y_goal and direction == 1:
						
							y = y + y_direction
						
							if self.tilemap[y][x] != replace_except:
								self.tilemap[y][x] = replace_inner
							elif self.tilemap[y][x] == replace_except:
								self.tilemap[y][x] = except_replacer
						
						if direction == 0:
							direction = 1
						elif direction == 1:
							direction = 0
	
	def spawn_monsters(self,depth):
		#This function spawns monsters on the map
		
		if self.map_type == 'elfish_fortress':
			monster_max = 0
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					if self.tilemap[y][x].techID == tl.tlist['functional'][8].techID:#this is a bed
						monster_max += 1
		else:
			monster_max = (max_map_size*max_map_size)/30
		
		monster_max = int(monster_max * self.monster_num)
		
		if self.map_type == 'grot':
			spawnpoints = self.find_all_moveable(ignore_water = False, ignore_no_spawn = False)
		else:
			spawnpoints = self.find_all_moveable(ignore_no_spawn = False)
		
		del_list = []
		monster_count = self.monster_count
		
		for i in range (0,len(spawnpoints)):
			
			if self.npcs[spawnpoints[i][1]][spawnpoints[i][0]] != 0: #there is a monster here
				spawnpoints[i] = 'del'
				#monster_count += 1#count the monsters that are already on the map
			
		newlist = []
		
		for k in spawnpoints:
			if k != 'del':
				newlist.append(k)
				
		spawnpoints = newlist
			
		monster_max -= monster_count
		
		if monster_max > len(spawnpoints):
			monster_max = len(spawnpoints)
		for k in range(0,monster_max):
			
			ran = random.randint(0,len(ml.mlist[self.map_type])-1)
			ran2 = random.randint(0,len(spawnpoints)-1)
			ran3 = random.randint(0,len(ml.mlist['civilian'])-1)
				
			self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]] = deepcopy(ml.mlist[self.map_type][ran])#deepcopy is used that every monster on the map is saved separate
			self.set_monster_strength(spawnpoints[ran2][0],spawnpoints[ran2][1],depth)
			self.monster_count += 1
			if self.no_monster_respawn == False:
				self.countdowns.append(countdown('spawner',spawnpoints[ran2][1],spawnpoints[ran2][0],random.randint(5,60)))
			try:
				if player.difficulty == 4:
					self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]].AI_style = 'ignore'
			except:
				None
					
			#set monsters personal_id
			
			self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]].personal_id = str(self.npcs[spawnpoints[ran2][1]][spawnpoints[ran2][0]].techID)+'_'+str(spawnpoints[ran2][0])+'_'+str(spawnpoints[ran2][1])+'_'+str(random.randint(0,9999))
			
			#set monster groups
			
			self.spawn_monster_groups(ml.mlist['kobold'][0],ml.mlist['kobold'][1],9)#kobolds
			
	def set_monster_strength(self,x,y,z,preset_lvl=None,lvl_bonus=0):
		
		self.npcs[y][x] = deepcopy(self.npcs[y][x])
		
		if self.npcs[y][x] != 0:
			old_lvl = self.npcs[y][x].lvl
			
			ran = random.randint(1,3)
			if Time_ready == True:
				if player.difficulty == 3:
					base_lvl = 25
				elif player.difficulty == 2:
					base_lvl = 20
				elif player.difficulty == 1:
					base_lvl = 15
				elif player.difficulty == 0:
					base_lvl = 10
				else:
					base_lvl = 0

				time_coeff = int(base_lvl*((time.year-1)*28*12 + time.day_total)/150) #base_lvl levels each 150 days of gameplay # 
			else:
				time_coeff = 0
			
			if self.npcs[y][x].techID == ml.mlist['overworld'][0] or self.npcs[y][x].techID == ml.mlist['angry_monster'][2]: #this is a dryade
				try:
					time_coeff = player.lvl
				except:
					None
			
			monster_lvl = z + ran + self.monster_plus + time_coeff
			
			if monster_lvl >= old_lvl and old_lvl > 0:
				try:
					screen.write_hit_matrix(x,y,12) #render monster_lvl_up
				except:
					None
				
			if preset_lvl != None:
				self.npcs[y][x].lvl = preset_lvl
			else:
				self.npcs[y][x].lvl = monster_lvl
			
			self.npcs[y][x].lvl += lvl_bonus
			
			attribute_list =[] 
		
			al = ('p_strength','p_defense','m_strength','m_defense','health') #DUBTE
		
			for c in range(0,5):
				if self.npcs[y][x].attribute_prev[c] > 0:
					for h in range(0,self.npcs[y][x].attribute_prev[c]):
						attribute_list.append(al[c])
		
			for i in range(0,self.npcs[y][x].lvl):
				choice = attribute_list[random.randint(0,len(attribute_list)-1)]
				
				if choice == 'p_strength':
					self.npcs[y][x].basic_attribute.p_strength +=3
				elif choice == 'p_defense':
					self.npcs[y][x].basic_attribute.p_defense +=3
				elif choice == 'm_strength':
					self.npcs[y][x].basic_attribute.m_strength +=3
				elif choice == 'm_defense':
					self.npcs[y][x].basic_attribute.m_defense +=3
				elif choice == 'health':
					self.npcs[y][x].basic_attribute.max_lp += 1
					self.npcs[y][x].lp = self.npcs[y][x].basic_attribute.max_lp	
			
			if old_lvl == 0:
				el = [['knife','dagger','axe','sword'],['rune','wand','rune staff','artefact'],['armor','armor'],['amulet','talisman'],['seal ring','ring']] #CUIDAO
				e_nr = 0
			
				for q in range(0,len(el)-1):
					ran = random.randint(0,len(el[q])-1)
					
					if self.npcs[y][x].worn_equipment[q] == 1:
						help_equipment = item_wear(el[q][ran],random.randint(0,min((z*3),21)),random.randint(-2,2))
					
						self.npcs[y][x].basic_attribute.p_strength += help_equipment.attribute.p_strength
						self.npcs[y][x].basic_attribute.p_defense += help_equipment.attribute.p_defense
						self.npcs[y][x].basic_attribute.m_strength += help_equipment.attribute.m_strength
						self.npcs[y][x].basic_attribute.m_defense += help_equipment.attribute.m_defense
						self.npcs[y][x].basic_attribute.luck += help_equipment.attribute.luck
						
			if 'cattle' in self.npcs[y][x].properties:
				self.npcs[y][x].basic_attribute.max_lp = 1
				self.npcs[y][x].lp = self.npcs[y][x].basic_attribute.max_lp
				self.npcs[y][x].lp = self.npcs[y][x].basic_attribute.p_defense = 1
				self.npcs[y][x].lp = self.npcs[y][x].basic_attribute.m_defense = 1
			
			if 'pet0' in self.npcs[y][x].properties:
				self.npcs[y][x].basic_attribute.max_lp = 5
			if 'pet1' in self.npcs[y][x].properties:
				self.npcs[y][x].basic_attribute.max_lp = 10
			if 'pet2' in self.npcs[y][x].properties:
				self.npcs[y][x].basic_attribute.max_lp = 15
				
			if 'npc' in self.npcs[y][x].properties:
				self.npcs[y][x].basic_attribute.max_lp = 10
			
			if 'double_lp' in self.npcs[y][x].properties:
				self.npcs[y][x].basic_attribute.max_lp *= 2 
			
			self.npcs[y][x].lp = self.npcs[y][x].basic_attribute.max_lp
	
	def make_vault(self,on_tile,depth):
		
		run = True
		
		while run:
			pos = self.find_any(on_tile)
			test = True
			orientation = random.randint(0,3)#0:north, 1:east, 2:south, 3:west
			try:			
				if pos[0] < 6 or pos[0] > max_map_size-6 or pos[1] < 6 or pos[1] > max_map_size-6:
					test = False
					
				if orientation == 0:
					x_offset = -2
					y_offset = random.randint(-1,1)
				elif orientation == 1:
					x_offset = random.randint(-1,1)
					y_offset = -2
				elif orientation == 2:
					x_offset = 2
					y_offste = random.randint(-1,1)
				else:
					x_offset = random.randint(-1,1)
					y_offset = 2
					
				for ty in range(pos[1]+y_offset-1,pos[1]+y_offset+6):
					for tx in range(pos[0]+x_offset-1,pos[0]+x_offset+6):
						if self.tilemap[ty][tx].techID == tl.tlist['dungeon'][0].techID:
							test = False
						elif self.tilemap[ty][tx].techID == tl.tlist['dungeon'][6].techID:
							test = False
						elif self.tilemap[ty][tx].techID == tl.tlist['dungeon'][9].techID:
							test = False
						elif self.tilemap[ty][tx].techID == tl.tlist['functional'][2].techID:
							test = False
			except:
				test = False
			
			if test:
				run = False
		
		for yy in range(pos[1]+y_offset-2,pos[1]+y_offset+3):
			for xx in range(pos[0]+x_offset-2,pos[0]+x_offset+3):
				if xx == pos[0]+x_offset-2 or xx == pos[0]+x_offset+2 or yy == pos[1]+y_offset-2 or yy == pos[1]+y_offset+2:
					self.tilemap[yy][xx] = deepcopy(tl.tlist['dungeon'][9])
					self.tilemap[yy][xx].no_spawn = True
				else:
					self.tilemap[yy][xx] = deepcopy(tl.tlist['dungeon'][0])
					self.tilemap[yy][xx].no_spawn = True
		
		make_loot = True # if make_loot is set on False no gems or ore will spawn inside the vault 
		
		vault_center_x = pos[0]+x_offset
		vault_center_y = pos[1]+y_offset
		
		door_pos = self.drunken_finder(vault_center_x,vault_center_y,tl.tlist['dungeon'][9])
		self.tilemap[door_pos[1]][door_pos[0]] = deepcopy(tl.tlist['dungeon'][6])
		self.tilemap[door_pos[1]][door_pos[0]].no_spawn = True
		
		vault_type = random.randint(0,4)
		#vault_type = 4
		
		if vault_type == 0: #Libary
			
			replace = self.tilemap[vault_center_y][vault_center_x]
			self.tilemap[vault_center_y][vault_center_x] = deepcopy(tl.tlist['functional'][19])#set a bookshelf
			self.tilemap[vault_center_y][vault_center_x].replace = replace
			self.tilemap[vault_center_y][vault_center_x].no_spawn = True
			
			replace = self.tilemap[vault_center_y+1][vault_center_x]
			self.tilemap[vault_center_y+1][vault_center_x] = deepcopy(tl.tlist['functional'][4])#set a chest
			self.tilemap[vault_center_y+1][vault_center_x].replace = replace
			self.tilemap[vault_center_y+1][vault_center_x].no_spawn = True
			
			num_spellbooks = random.randint(2,3)#fill the chest
			spellbook_list = []
			sb = (il.ilist['misc'][26],il.ilist['misc'][30],il.ilist['misc'][32],il.ilist['misc'][34],il.ilist['misc'][36],il.ilist['misc'][38],il.ilist['misc'][45],il.ilist['misc'][83])
			for i in range(0,num_spellbooks):
				ran = random.randint(0,len(sb)-1)
				spellbook_list.append(sb[ran])
			self.containers[vault_center_y+1][vault_center_x] = container(spellbook_list)
			
			self.npcs[vault_center_y-1][vault_center_x-1] = deepcopy(ml.mlist['grot'][0])			#
			self.set_monster_strength(vault_center_x-1,vault_center_y-1,depth,lvl_bonus=3)			#
			self.npcs[vault_center_y-1][vault_center_x+1] = deepcopy(ml.mlist['grot'][0])			#
			self.set_monster_strength(vault_center_x+1,vault_center_y-1,depth,lvl_bonus=3)			#set blue nagas
			self.npcs[vault_center_y+1][vault_center_x-1] = deepcopy(ml.mlist['grot'][0])			#
			self.set_monster_strength(vault_center_x-1,vault_center_y+1,depth,lvl_bonus=3)			#
			self.npcs[vault_center_y+1][vault_center_x+1] = deepcopy(ml.mlist['grot'][0])			#
			self.set_monster_strength(vault_center_x+1,vault_center_y+1,depth,lvl_bonus=3)			#
		
		if vault_type == 1: #Slime pit
			replace = self.tilemap[vault_center_y][vault_center_x]
			self.npcs[vault_center_y][vault_center_x] = deepcopy(ml.mlist['statue'][2])#set a blob statue
			self.set_monster_strength(vault_center_y,vault_center_x,depth,lvl_bonus=3)
			self.npcs[vault_center_y][vault_center_x].lp = 999
			
			self.npcs[vault_center_y-1][vault_center_x-1] = deepcopy(ml.mlist['special'][10])			#
			self.set_monster_strength(vault_center_x-1,vault_center_y-1,depth,lvl_bonus=3)				#
			self.npcs[vault_center_y-1][vault_center_x+1] = deepcopy(ml.mlist['special'][10])			#
			self.set_monster_strength(vault_center_x+1,vault_center_y-1,depth,lvl_bonus=3)				#set giant blobs
			self.npcs[vault_center_y+1][vault_center_x-1] = deepcopy(ml.mlist['special'][10])			#
			self.set_monster_strength(vault_center_x-1,vault_center_y+1,depth,lvl_bonus=3)				#
			self.npcs[vault_center_y+1][vault_center_x+1] = deepcopy(ml.mlist['special'][10])			#
			self.set_monster_strength(vault_center_x+1,vault_center_y+1,depth,lvl_bonus=3)				#
		
		if vault_type == 2: #Kobold Lair
			replace = self.tilemap[vault_center_y][vault_center_x]
			self.tilemap[vault_center_y][vault_center_x] = deepcopy(tl.tlist['deco'][9])#set a stony throne
			self.tilemap[vault_center_y][vault_center_x].replace = replace				#
			self.tilemap[vault_center_y][vault_center_x].no_spawn = True				#
			
			for posy in range(vault_center_y-1,vault_center_y+2):				#
				for posx in range(vault_center_x-1,vault_center_x+2):			#set Kobolds
					self.npcs[posy][posx] = deepcopy(ml.mlist['kobold'][1])		#
					self.set_monster_strength(posx,posy,depth,lvl_bonus=3)		#
			
			self.npcs[vault_center_y][vault_center_x] = deepcopy(ml.mlist['kobold'][0])				#set kobold shaman
			self.set_monster_strength(vault_center_x,vault_center_y,depth,lvl_bonus=3)				#
		
		if vault_type == 3: #Bat Cave
			make_loot = False
			for posy in range(vault_center_y-1,vault_center_y+2):				#
				for posx in range(vault_center_x-1,vault_center_x+2):			#set bats
					self.npcs[posy][posx] = deepcopy(ml.mlist['cave'][2])		#
					self.set_monster_strength(posx,posy,depth)					#
		
		if vault_type == 4: #mimic chamber
			make_loot = False
			ranx = random.randint(-1,1)																	#
			rany = random.randint(-1,1)																	#
			replace = self.tilemap[vault_center_y+rany][vault_center_x+ranx]							#
			self.tilemap[vault_center_y+rany][vault_center_x+ranx] = deepcopy(tl.tlist['functional'][4])#set a chest
			self.tilemap[vault_center_y+rany][vault_center_x+ranx].replace = replace					#
			self.tilemap[vault_center_y+rany][vault_center_x+ranx].no_spawn = True						#
			
			sb = (il.ilist['misc'][26],il.ilist['misc'][30],il.ilist['misc'][32],il.ilist['misc'][34],il.ilist['misc'][36],il.ilist['misc'][38],il.ilist['misc'][45],il.ilist['misc'][83])
			ransb = random.randint(0,len(sb)-1)
			
			book = sb[ransb]
			pick = item_wear('pickaxe', 20,0)
			axe = item_wear('axe',20,0)
			
			self.containers[vault_center_y+rany][vault_center_x+ranx] = container([book,axe,pick])#fill chest
			
			for posy in range(vault_center_y-1,vault_center_y+2):							#
				for posx in range(vault_center_x-1,vault_center_x+2):						#set sleeping mimics
					if self.tilemap[posy][posx].techID != tl.tlist['functional'][4].techID:	#
						self.npcs[posy][posx] = deepcopy(ml.mlist['special'][3])			#
		
		if make_loot == True:
			for yyy in range(vault_center_y-2,vault_center_y+3):
				for xxx in range(vault_center_x-2,vault_center_x+3):
					if self.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][0].techID:
						ran2 = random.randint(0,2)
						replace = self.tilemap[yyy][xxx]
						if ran2 > 1:
							self.tilemap[yyy][xxx] = deepcopy(tl.tlist['misc'][9])#set gem
							self.tilemap[yyy][xxx].no_spawn = True
						else:
							self.tilemap[yyy][xxx] = deepcopy(tl.tlist['misc'][11])#set ore
							self.tilemap[yyy][xxx].no_spawn = True
						self.tilemap[yyy][xxx].replace = replace
		
		#print('Made vault at: '+str(pos[0])+','+str(pos[1])+' Type:'+str(vault_type))
		####go on here
	
	def make_orc_cave(self,on_tile):
		
		run = True
		
		while run:
			pos = self.find_any(on_tile)
			
			test = True
			try:
				for ty in range(pos[1]-2,pos[1]+3):
					for tx in range(pos[0]-2,pos[0]+3):
						if self.tilemap[ty][tx].techID == tl.tlist['misc'][16].techID:
							test = False
						elif self.tilemap[ty][tx].techID == tl.tlist['mine'][0].techID:
							test = False
						elif self.tilemap[ty][tx].techID == tl.tlist['dungeon'][3].techID:
							test = False
						elif self.tilemap[ty][tx].techID == tl.tlist['misc'][12].techID:
							test = False
			except:
				test = False
			
			if ((pos[0]-(max_map_size/2))**2+(pos[1]-(max_map_size/2))**2)**0.5 > 10:
				if pos[0] > 5 and pos[0] < max_map_size-5 and pos[1] > 5 and pos[1] < max_map_size-5 and test == True:
					run = False
					
		for y in range(pos[1]-2,pos[1]+3):
			for x in range(pos[0]-2,pos[0]+3):
				self.tilemap[y][x] = tl.tlist['misc'][16] #fill with solid orcish wall
		for y in range(pos[1]-1,pos[1]+2):
			for x in range(pos[0]-1,pos[0]+2):
				self.tilemap[y][x] = tl.tlist['mine'][0] #fill inner with orcish mine floor
				
				if x != pos[0] or y != pos[1]:
					self.npcs[y][x] = deepcopy(ml.mlist['orc'][random.randint(0,len(ml.mlist['orc'])-1)])	#
				else:																						#
					self.npcs[y][x] = deepcopy(ml.mlist['orcish_mines'][1])								#
				self.set_monster_strength(x,y,1)															#generate orcs
				self.countdowns.append(countdown('orc_spawner',x,y,random.randint(5,60)))					#
				
		self.tilemap[pos[1]-2][pos[0]] = deepcopy(tl.tlist['dungeon'][3])#
		self.tilemap[pos[1]+2][pos[0]] = deepcopy(tl.tlist['dungeon'][3])# make dungeon doors
		self.tilemap[pos[1]][pos[0]-2] = deepcopy(tl.tlist['dungeon'][3])#
		self.tilemap[pos[1]][pos[0]+2] = deepcopy(tl.tlist['dungeon'][3])#
		
		self.tilemap[pos[1]-2][pos[0]-2] = deepcopy(tl.tlist['misc'][12])#
		self.tilemap[pos[1]-2][pos[0]-2].replace = deepcopy(on_tile)	 #
		self.tilemap[pos[1]-2][pos[0]+2] = deepcopy(tl.tlist['misc'][12])#
		self.tilemap[pos[1]-2][pos[0]+2].replace = deepcopy(on_tile)	 # add orc deko to the connors
		self.tilemap[pos[1]+2][pos[0]-2] = deepcopy(tl.tlist['misc'][12])#
		self.tilemap[pos[1]+2][pos[0]-2].replace = deepcopy(on_tile)	 #
		self.tilemap[pos[1]+2][pos[0]+2] = deepcopy(tl.tlist['misc'][12])#
		self.tilemap[pos[1]+2][pos[0]+2].replace = deepcopy(on_tile)	 #
		
		self.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['misc'][18])#set a crystal orb
		
	def AI_move(self):
		#This function moves all monsters that are 7 or less fields away from the player.
		#It dosn't move all monsters to save performance 
		
		xmin = 0
		ymin = 0
		xmax = max_map_size
		ymax = max_map_size
			
		#for y in range (0,max_map_size):#reset the move_done switches
		#	for x in range (0,max_map_size):
		#		
		#		if self.npcs[y][x] != 0:
		#			if self.npcs[y][x].lp > 0:
		#				self.npcs[y][x].move_done = 0
		#			else:
		#				test = False
		#				while test == False:
		#					test = self.monster_die(x,y)
		
		for y in range (ymin,ymax):
			for x in range (xmin,xmax):
				
				if self.npcs[y][x] != 0 and self.npcs[y][x].move_done == 0:#if there is a monster at this place
					
					#-2. get AI_style
					AI_style = self.npcs[y][x].AI_style
					
					#-1. remove blind
					if 'blind' in self.npcs[y][x].properties:
						rand = random.randint(0,9)
						if rand < 2:
							for i in range(0,len(self.npcs[y][x].properties)):
								if self.npcs[y][x].properties[i] == 'blind':
									p = i
							try:
								del self.npcs[y][x].properties[p]
							except:
								None
					
					#0. Get LoS
					
					los = self.check_los(x,y,player.pos[0],player.pos[1])
					
					if 'blind' in self.npcs[y][x].properties:
						los = False
					
					if los == True:
						self.npcs[y][x].last_known_player_pos = (player.pos[0],player.pos[1])
							
					if player.buffs.get_buff('invisible') > 0: #DUBTE
						los = False
							
					if self.npcs[y][x].last_known_player_pos != 'Unknown':
						if x == self.npcs[y][x].last_known_player_pos[0] and y == self.npcs[y][x].last_known_player_pos[1]:
							self.npcs[y][x].last_known_player_pos = 'Unknown'
					
					if player.buffs.get_buff('invisible') > 0 or 'blind' in self.npcs[y][x].properties:
						self.npcs[y][x].last_known_player_pos = 'Unknown'
						
					#I. Get possible fields for a move
						
					moves = [(x,y)]
						
					yy = (-1,0,0,1)
					xx = (0,-1,1,0)
						
					for i in range (0,4):
							
						try:
								
							monster_move_groups = self.npcs[y][x].move_groups
							tile_move_group = self.tilemap[y+yy[i]][x+xx[i]].move_group
							
							move_group_check = tile_move_group in monster_move_groups
									
							if self.npcs[y+yy[i]][x+xx[i]] == 0:
								npc = False
							else:
								npc = True
									
							if self.tilemap[y+yy[i]][x+xx[i]].techID == tl.tlist['functional'][1].techID or self.tilemap[y+yy[i]][x+xx[i]].techID == tl.tlist['functional'][2].techID: #this is a stair up/down
								stair = True
							else:
								stair = False
									
							if x + xx[i] == player.pos[0] and y + yy[i] == player.pos[1]:
								playerpos = True
							else:
								playerpos = False
							
							if move_group_check == True and npc == False and stair == False and playerpos == False:
									
								moves.append((x+xx[i],y+yy[i]))		
									
						except:
							print('Debug:Error') #DUBTE
						
						#II. Find out which possible move leads to which distance between monster and player
					distances = []
					
					for j in range (0,len(moves)):
						
						if self.npcs[y][x].last_known_player_pos != 'Unknown':
							a = self.npcs[y][x].last_known_player_pos[0] - moves[j][0]
							b = self.npcs[y][x].last_known_player_pos[1] - moves[j][1]
						else:
							a = 100
							b = 100
						
						c = (a**2 + b**2)**0.5 # this is just the good old pythagoras (c² = a² + b²)
						
						distances.append(c)
					
						#III. Choose the right move (or special action)
					
					do_move = 'foo'
					
					if AI_style == 'hostile' and los == False:# and self.npcs[y][x].last_known_player_pos == 'Unknown':
						AI_style = 'ignore'
					
					if AI_style == 'hostile':
						
						comp = False
						
						for yy in range(y-1,y+2):
							if self.npcs[yy][x] != 0 and self.npcs[yy][x].AI_style == 'company':
								comp = [x,yy]
						for xx in range(x-1,x+2):
							if self.npcs[y][xx] != 0 and self.npcs[y][xx].AI_style == 'company':
								comp = [xx,y]
								
						if comp != False and not 'blind' in self.npcs[y][x].properties:
							ran = random.randint(0,99)
							if ran < 40:
								self.npcs[y][x].move_done = 1
								mes = self.npcs[y][x].name + ' hurts ' + self.npcs[comp[1]][comp[0]].name #DUBTE
								message.add(mes)
								screen.write_hit_matrix(comp[0],comp[1],4)
								sfx.play('hit')
								player.pet_lp -= 1
								if player.pet_lp < 1:
									self.npcs[comp[1]][comp[0]].relation = int(self.npcs[comp[1]][comp[0]].relation*0.8)
									return_done = False
									
									if 'npc' in world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties:
										seeked_tile = tl.tlist['functional'][18]
									else:
										seeked_tile = tl.tlist['sanctuary'][4]
									
									for yyy in range(0,max_map_size):
										for xxx in range(0,max_map_size):
											if world.maplist[0]['elysium_0_0'].tilemap[yyy][xxx].techID == seeked_tile.techID and world.maplist[0]['elysium_0_0'].npcs[yyy][xxx] == 0 and return_done == False:
												string = self.npcs[comp[1]][comp[0]].name + ' returns home.' #TIPO2
												message.add(string)
												screen.write_hit_matrix(comp[0],comp[1],7)
												self.npcs[comp[1]][comp[0]].AI_style = 'ignore'
												world.maplist[0]['elysium_0_0'].npcs[yyy][xxx] = deepcopy(self.npcs[comp[1]][comp[0]])
												self.npcs[comp[1]][comp[0]] = 0
												player.pet_pos = False
												player.pet_on_map = False
												return_done = True
									
									if return_done == False:
										string = self.npcs[comp[1]][comp[0]].name + ' dies!' #DUBTE
										message.add(string)
										self.npcs[comp[1]][comp[0]] = 0
										player.pet_pos = False
										player.pet_on_map = False
						
						ability_keys = self.npcs[y][x].ability.keys()
						
						if self.npcs[y][x].lp < self.npcs[y][x].basic_attribute.max_lp/2 and player.lp > player.attribute.max_lp/2 and distances[0] < 3 and self.npcs[y][x].num_special > 0 :#this is a defensive situation for the monster
							
							if 'def_teleport' in ability_keys:
								ran = random.randint(0,99)
								if ran < self.npcs[y][x].ability['def_teleport'] and self.npcs[y][x].move_done != 1:
									moves = self.find_all_moveable(ignore_player_pos = False)
									if moves != False:
										if len(moves) == 1:
											pos_num = 0
										else:
											pos_num = random.randint(0,len(moves)-1)
											
										self.npcs[y][x].move_done = 1
										self.npcs[y][x].num_special -= 1
										tp_string = 'A ' + self.npcs[y][x].name + ' teleports.' #TIPO2
										message.add(tp_string)
										screen.write_hit_matrix(x,y,7)
										sfx.play('teleport')
										self.npcs[moves[pos_num][1]][moves[pos_num][0]] = self.npcs[y][x]
										self.npcs[y][x] = 0
							
							if 'def_flee' in ability_keys:
								ran = random.randint(0,99)
								if self.npcs[y][x] != 0:		
									if ran < self.npcs[y][x].ability['def_flee'] and self.npcs[y][x].move_done != 1 and self.npcs[y][x].lp < self.npcs[y][x].basic_attribute.max_lp:
										flee_string = 'A ' + self.npcs[y][x].name + ' turns to flee.' #TIPO2
										message.add(flee_string)
										self.npcs[y][x].AI_style = 'flee'
										self.npcs[y][x].move_done = 1
										self.npcs[y][x].num_special -= 1
								
								if 'def_potion' in ability_keys:
									ran = random.randint(0,99)
									if ran < self.npcs[y][x].ability['def_potion'] and self.npcs[y][x].move_done != 1:
										if self.npcs[y][x].lp < self.npcs[y][x].basic_attribute.max_lp:
											potion_string = 'A ' + self.npcs[y][x].name + ' quaffes a potion of healing.' #TIPO2
											message.add(potion_string)
											screen.write_hit_matrix(x,y,6)
											lp = min(self.npcs[y][x].basic_attribute.max_lp, self.npcs[y][x].lp+7)
											self.npcs[y][x].lp = lp
											sfx.play('drink')
											self.npcs[y][x].move_done = 1
											self.npcs[y][x].num_special -= 1
									
						if self.npcs[y][x] != 0:
							if (distances[0] > 1 or player.buffs.get_buff('invisible') > 0) and self.npcs[y][x].move_done != 1: #moves[0] is always the position of the monster right now, so distances 0 is always it's distance towards the player
								if 'spawn' in ability_keys and distances[0] < 8: #the value of spawn is a tulpel with 2 elements; 0: chance that something is spawned 1: number that determines what is spawned
									ran = random.randint(0,99)
									if ran < self.npcs[y][x].ability['spawn'][0]:
										spawn_kind = self.npcs[y][x].ability['spawn'][1] 
										xlist = []
										ylist = []
										for yy in range(y-1,y+2):
											for xx in range(x-1,x+2):
												if self.tilemap[yy][xx].move_group == 'soil' and self.npcs[yy][xx] == 0 and xx != player.pos[0] and yy != player.pos[1]:
													xlist.append(xx)
													ylist.append(yy)
												
										if len(xlist) == len(ylist) and len(xlist) > 0:
											if len(xlist) > 1:
												num = random.randint(0,len(xlist)-1)
											else:
												num = 0
									
											if self.npcs[y][x].move_done != 1 and self.npcs[y][x].num_special > 0:
												self.npcs[ylist[num]][xlist[num]] = deepcopy(ml.mlist['special'][spawn_kind]) #all spawnlings must be a part of ml.mlist['special']
												self.npcs[ylist[num]][xlist[num]].personal_id = self.npcs[y][x].personal_id + '_child'
												self.set_monster_strength(xlist[num],ylist[num],player.pos[2])
												mes = 'A ' + self.npcs[y][x].name + ' summons a ' + ml.mlist['special'][spawn_kind].name + '.' #TIPO2
												message.add(mes)
												sfx.play('teleport')
												screen.write_hit_matrix(xlist[num],ylist[num],7)
												self.npcs[y][x].move_done = 1
												self.npcs[y][x].num_special -= 1
								if 'blink' in ability_keys:
									ran = random.randint(0,99)
									if ran < self.npcs[y][x].ability['blink'] and self.npcs[y][x].move_done != 1 and self.npcs[y][x].num_special > 0:
										xlist = []
										ylist = []
									
										for yy in range(player.pos[1]-3,player.pos[1]+4):
											for xx in range(player.pos[0]-3,player.pos[0]+4):
												if self.tilemap[yy][xx].move_group in self.npcs[y][x].move_groups and self.npcs[yy][xx] == 0:
													if yy != player.pos[1] or xx != player.pos[0]:
														xlist.append(xx)
														ylist.append(yy)
										if len(xlist) != 0:
											try:
												rand = random.randint(0,len(xlist)-1)
											except:
												rand = 0
										
											screen.write_hit_matrix(x,y,7)
											screen.write_hit_matrix(xlist[rand],ylist[rand],7)
											mes = 'A '+self.npcs[y][x].name+' blinks!' #TIPO2
											message.add(mes)
											self.npcs[ylist[rand]][xlist[rand]] = self.npcs[y][x]
											self.npcs[y][x] = 0
											self.npcs[ylist[rand]][xlist[rand]].num_special -= 1
											self.npcs[ylist[rand]][xlist[rand]].move_done = 1
								
								if (x == player.pos[0] or y == player.pos[1]) and los == True:
									straight_line = True
								else:
									straight_line = False
								
								shoot = False
								throw = False
								
								if 'range_shoot' in ability_keys:
									shoot = True
								elif 'range_throw' in ability_keys:
									throw = True
								
								if self.npcs[y][x] != 0 and straight_line == True and los == True and (shoot == True or throw == True) and distances[0] < 5:
										#Step 0: Random
										if shoot == True:
											chance = self.npcs[y][x].ability['range_shoot']
										else:
											chance = self.npcs[y][x].ability['range_throw'][0]
										ran = random.randint(0,99)
										if ran < chance and self.npcs[y][x].num_special > 0 and self.npcs[y][x].move_done != 1:
											#Step 1: find the right direction
											if y > player.pos[1]:
												y_dir = -1
											elif y < player.pos[1]:
												y_dir = 1
											else:
												y_dir = 0
											
											if x > player.pos[0]:
												x_dir = -1
											elif x < player.pos[0]:
												x_dir = 1
											else:
												x_dir = 0
										
											#Step 2: Check for borders
										
											run = True
											count = 1
											fire_free = True 
										
											while run:
												cx = x + (count*x_dir)
												cy = y + (count*y_dir)
												
												if self.tilemap[cy][cx].transparency == False:
													fire_free = False
													run = False
												
												count +=1
												
												if cx == player.pos[0] and cy == player.pos[1]:
													run = False
											
											#Step 3: Fire!
											if fire_free == True:
												run = True
												count = 1
												if 'range_shoot' in ability_keys:
													sfx.play('fire')
												else:
													sfx.play('miss')
										
												while run:
													xx = x + (count*x_dir)
													yy = y + (count*y_dir)
											
													if xx != player.pos[0] or yy != player.pos[1]:
														screen.write_hit_matrix(xx,yy,2)
														if self.tilemap[yy][xx].transparency == False:
															screen.write_hit_matrix(player.pos[0],player.pos[1],3)
															if 'range_throw' in ability_keys:
																sfx.play('throw')
															run = False
													else:
														if shoot == True:#----------> go on here!!!!!!!!
															self.npcs[y][x].move_done = 1
															try:
																player.monster_attacks(x,y)
															except:
																None
														elif self.npcs[y][x].ability['range_throw'][1] == 0:
															self.npcs[y][x].move_done = 1
															message.add(l10n.format_value("stone-throw", {"stonegob": self.npcs[y][x].name}))
															chance = 9 - count
															coin = random.randint(0,7)
															if coin < chance:
																sfx.play('hit')
																screen.write_hit_matrix(player.pos[0],player.pos[1],4)
																message.add(l10n.format_value("stone-hit"))
																player.lp -= 1
															else:
																sfx.play('throw')
																screen.write_hit_matrix(player.pos[0],player.pos[1],3)
																message.add(l10n.format_value("stone-miss"))
																
														elif self.npcs[y][x].ability['range_throw'][1] == 1:
															self.npcs[y][x].move_done = 1
															message.add(l10n.format_value("dart-throw", {"dartgob": self.npcs[y][x].name}))
															chance = 9 - count
															coin = random.randint(0,7)
															if coin < chance:
																sfx.play('hit')
																screen.write_hit_matrix(player.pos[0],player.pos[1],4)
																message.add(l10n.format_value("dart-hit"))
																player.lp -= 2
															else:
																sfx.play('throw')
																screen.write_hit_matrix(player.pos[0],player.pos[1],3)
																message.add(l10n.format_value("dart-miss"))
														
														elif self.npcs[y][x].ability['range_throw'][1] == 2:
															self.npcs[y][x].move_done = 1
															message.add('A '+self.npcs[y][x].name+' throws a throwing knife') #TIPO2
															chance = 9 - count
															coin = random.randint(0,7)
															if coin < chance:
																sfx.play('hit')
																screen.write_hit_matrix(player.pos[0],player.pos[1],4)
																message.add(l10n.format_value("knife-hit"))
																player.lp -= 3
															else:
																sfx.play('throw')
																screen.write_hit_matrix(player.pos[0],player.pos[1],3)
																message.add(l10n.format_value("knife-miss"))
														run = False
											
													count += 1
												self.npcs[y][x].move_done = 1
												if 'range_throw' in ability_keys:
													self.npcs[y][x].num_special -= 1
								
								if self.npcs[y][x] != 0 and self.npcs[y][x].move_done == 0:
									
									if len(moves) > 0:#if no move is possible at least the 'move' of stay still must remain
										good_moves = []
										for k in range (0, len(moves)):
											if player.buffs.get_buff('invisible') == 0:
												if distances[k] <= distances[0]:#if the possible move makes the distance between player and monster smaller
													good_moves.append(moves[k])
											else:
												good_moves = moves
											
										if 'blind' in self.npcs[y][x].properties or player.buffs.get_buff('invisible') != 0:
											good_moves = moves
											
									else:
										good_moves = moves
									
									
									if len(good_moves) <= 1:
										good_moves = moves
								
									if len(good_moves) > 1:
										ran = random.randint(0,len(good_moves)-1)
									else:
										ran = 0
								
									do_move = good_moves[ran]
						
							else:
								if self.npcs[y][x].move_done == 0 and self.npcs[y][x].last_known_player_pos == (player.pos[0],player.pos[1]) and distances[0] == 1 and los == True:
									#the most important thing about stealing monsters is that their default corps_style has to be 'thief' and their corps_lvl has to be 0. Otherwise they would not work proper.
									if player.inventory.materials.gem > 0 and 'close_steal' in ability_keys:
										ran = random.randint(0,99)
										if ran < self.npcs[y][x].ability['close_steal']:
											player.inventory.materials.gem -= 1
											self.npcs[y][x].corps_lvl += 1
											screen.write_hit_matrix(player.pos[0],player.pos[1],8)
											screen.write_hit_matrix(x,y,9)
											sfx.play('steal')											
											steal_string = 'A ' + self.npcs[y][x].name + ' steals a gem from you.' #TIPO2
											message.add(steal_string)
											self.npcs[y][x].move_done = 1#set the move_done switch on
									
									if self.npcs[y][x].move_done == 0:
										#casting flames
										if 'close_flames' in ability_keys:
											ran = random.randint(0,99)
											if ran < self.npcs[y][x].ability['close_flames'] and self.npcs[y][x].num_special > 0:
												#Step 0: Check if any (other) monsters are near by
												sfx.play('flame')
												monster_num = 0
												for yy in range(y-1,y+2):
													for xx in range(x-1,x+2):
														if self.npcs[yy][xx] != 0:
															monster_num += 1
													
												if monster_num == 1:#there is no other monster near by
												
													num_flames = 0
												
													for yyy in range(y-1,y+2):
														for xxx in range(x-1,x+2):
															if xxx != x or yyy != y:
																if self.tilemap[yyy][xxx].replace == None and self.tilemap[yyy][xxx].move_group != 'solid' and self.tilemap[yyy][xxx].move_group != 'low_liquid' and self.tilemap[yyy][xxx].move_group != 'swim':
																	replace = self.tilemap[yyy][xxx]
																	self.tilemap[yyy][xxx] = deepcopy(tl.tlist['effect'][4])
																	self.tilemap[yyy][xxx].replace = replace
																	self.countdowns.append(countdown('flame',xxx,yyy,3))
																	num_flames+=1	
																											
													if num_flames > 0:
														flame_string = 'A '+ self.npcs[y][x].name + ' casts a flame spell!' #TIPO2
														message.add(flame_string)
														self.npcs[y][x].num_special -= 1
														self.npcs[y][x].move_done = 1
									
									if self.npcs[y][x].move_done == 0 and self.npcs[y][x].num_special > 0:
										#vampirism
										if 'close_vampirism' in ability_keys:
											ran = random.randint(0,99)
											if ran < self.npcs[y][x].ability['close_vampirism']:
												player.lp -= 1
												self.npcs[y][x].lp += 1
												screen.write_hit_matrix(player.pos[0],player.pos[1],18)
												screen.write_hit_matrix(x,y,19)
												sfx.play('vampire')
												vamp_string = 'A ' + self.npcs[y][x].name +' sucks your blood.' #TIPO2
												message.add(vamp_string)
												self.npcs[y][x].num_special -= 1
												self.npcs[y][x].move_done = 1
									
									if self.npcs[y][x].move_done == 0 and self.npcs[y][x].num_special > 0:
										#steal items
										if 'close_stealItem' in ability_keys:
											ran = random.randint(0,99)
											if ran < self.npcs[y][x].ability['close_stealItem']:
												#0: Find parent
												parent_pos = False
												parent_id = self.npcs[y][x].personal_id.replace('_child','')
												for yy in range(0,max_map_size):
													for xx in range(0,max_map_size):
														if self.npcs[yy][xx] != 0 and self.npcs[yy][xx].personal_id == parent_id:
															parent_pos = (xx,yy)
												#1: Check Parent Status 
												if parent_pos != False:
													if len(self.containers[parent_pos[1]][parent_pos[0]].items) < 7:
														p_check = True
													else:
														p_check = False
												#2: Steal Item
													if p_check == True:
														all_bp = ('Head','Body','Legs','Feet','Hold(R)','Hold(L)','Neck','Axe','Pickaxe','Hand') #CUIDAO
														final_bp = ['None',]
														for i in range(0,len(all_bp)-1):
															if player.inventory.wearing[all_bp[i]] != player.inventory.nothing:
																final_bp.append(all_bp[i])
														del final_bp[0]
													
														if len(final_bp) > 0:
															if len(final_bp) == 1:
																ran = 0
															else:
																ran = random.randint(0,len(final_bp)-1)
															
														item = player.inventory.wearing[final_bp[ran]]
														player.inventory.wearing[final_bp[ran]] = player.inventory.nothing
														self.containers[parent_pos[1]][parent_pos[0]].items.append(item)
														mes = 'A '+self.npcs[y][x].name+' steals your '+item.name+'!' #TIPO2
														message.add(mes)
														sfx.play('steal')
														screen.write_hit_matrix(player.pos[0],player.pos[1],21)
														screen.write_hit_matrix(parent_pos[0],parent_pos[1],22)
														self.npcs[y][x].lp = 0
										
									if self.npcs[y][x].move_done == 0 and self.npcs[y][x].num_special > 0:
										#throw explosives
										if 'close_throwExplosive' in ability_keys:
											ran = random.randint(0,99)
											if ran < self.npcs[y][x].ability['close_throwExplosive']:
												positions = []
												for yy in range(player.pos[1]-1,player.pos[1]+2):
													for xx in range(player.pos[0]-1,player.pos[0]+2):
														if self.tilemap[yy][xx].replace == None and self.tilemap[yy][xx].move_group == 'soil' and self.tilemap[yy][xx].use_group == 'None':
															positions.append((xx,yy))
												
												if len(positions) > 0:
													sfx.play('throw')
													screen.write_hit_matrix(x,y,20)
													ran = random.randint(0,len(positions)-1)
													pos = positions[ran] 
													screen.write_hit_matrix(pos[0],pos[1],16)
													coin = random.randint(0,3)
													if coin == 0:
														message.add('A '+self.npcs[y][x].name+' throws a bomb!') #TIPO2
														replace = self.tilemap[pos[1]][pos[0]]
														self.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['effect'][0])
														self.countdowns.append(countdown('bomb3',pos[0],pos[1],1))
														self.tilemap[pos[1]][pos[0]].replace = replace
													else:
														message.add('A '+self.npcs[y][x].name+' throws an explosive!') #TIPO2
														replace = self.tilemap[pos[1]][pos[0]]
														self.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['effect'][7])
														self.tilemap[pos[1]][pos[0]].replace = replace
													self.npcs[y][x].move_done = 1
													self.npcs[y][x].num_special -= 1
														
											
								if self.npcs[y][x].move_done == 0 and los == True:
									try:
										player.monster_attacks(x,y)
									except:
										None
										self.npcs[y][x].move_done = 1#set the move_done switch on
					
					elif AI_style == 'flee':
						
						if distances[0] > 4: #moves[0] is always the position of the monster right now, so distances 0 is always it's distance towards the player
								
							if len(moves) > 1:
								ran = random.randint(0,len(moves)-1)
							else:
								ran = 0
								
							do_move = moves[ran]
						
						else:
							
							if len(moves) > 0:#if no move is possible at least the 'move' of stay still must remain
								
								good_moves = []
								
								for k in range (0, len(moves)):
									if distances[k] > distances[0] or distances[k] == distances[0]:#if the possible move makes the distance between player and monster bigger or at least the same
										good_moves.append(moves[k])
							else:
								good_moves = moves
									
							if len(good_moves) == 0:
								good_moves = moves
								
							if len(good_moves) > 1:
								ran = random.randint(0,len(good_moves)-1)
							else:
								ran = 0
								
							do_move = good_moves[ran]
							
					elif AI_style == 'ignore':
						
						ability_keys = self.npcs[y][x].ability.keys()
						
						if self.npcs[y][x].move_done == 0:
							if 'produce_egg' in ability_keys:
								ran = random.randint(0,999)
								if ran < self.npcs[y][x].ability['produce_egg'] and self.tilemap[y][x].replace == None:
									replace = self.tilemap[y][x]
									self.tilemap[y][x] = deepcopy(tl.tlist['functional'][33])
									self.tilemap[y][x].replace = replace
						
						if self.npcs[y][x].move_done == 0:
							if len(moves) > 1:
								ran = random.randint(0,len(moves)-1)
							else:
								ran = 0
								
							do_move = moves[ran]
	
					elif self.npcs[y][x].AI_style == 'company':
						
						ability_keys = self.npcs[y][x].ability.keys()
						
						if self.npcs[y][x].move_done == 0:
							if 'attack_monster' in ability_keys:
								
								monsters_list = []
								for yy in range (y-1,y+2):
									if self.npcs[yy][x] != 0 and self.npcs[yy][x].AI_style == 'hostile':
											monsters_list.append([x,yy])
								for xx in range(x-1,x+2):
									if self.npcs[y][xx] != 0 and self.npcs[y][xx].AI_style == 'hostile':
										monsters_list.append([xx,y])
											
								if len(monsters_list) > 0:
									
									if len(monsters_list) == 1:
										ran = 0
									else:
										ran = random.randint(0,len(monsters_list)-1)
										
									xxx = monsters_list[ran][0]
									yyy = monsters_list[ran][1]
									
									rand = random.randint(0,99)
									
									if 'eat_monster' in ability_keys:
										if rand < self.npcs[y][x].ability['eat_monster']:
											if not 'uneatable' in self.npcs[yyy][xxx].properties:
												mes = self.npcs[y][x].name + ' eats ' + self.npcs[yyy][xxx].name + '.' #TIPO2
												message.add(mes)
												sfx.play('eat')
												self.npcs[yyy][xxx] = 0
												self.npcs[y][x].relation += 100
												self.npcs[y][x].move_done = 1
											
									if rand < self.npcs[y][x].ability['attack_monster'] and self.npcs[y][x].move_done == 0:
										mes = self.npcs[y][x].name + ' hits ' + self.npcs[yyy][xxx].name + '.' #TIPO2
										message.add(mes)
										self.npcs[yyy][xxx].lp -= 1
										screen.write_hit_matrix(xxx,yyy,4)
										sfx.play('hit')
										if '-skill' in ability_keys and not '-skill' in self.npcs[yyy][xxx].properties:
											self.npcs[yyy][xxx].properties.append('-skill')
										if self.npcs[yyy][xxx].lp < 1:
											self.monster_die(xxx,yyy)
										self.npcs[y][x].move_done = 0
						
						if self.npcs[y][x].move_done == 0:
							if 'light' in ability_keys:
								
								time_night = False
								if time.hour < 6 or time.hour > 19:
									time_night = True
									
								if time_night == True or player.pos[2] > 0:
									player.buffs.set_buff('light',1,False)
									
						if self.npcs[y][x].move_done == 0:
							if 'blind' in ability_keys:
								
								monsters_list = []
								for yy in range (y-1,y+2):
									if self.npcs[yy][x] != 0 and self.npcs[yy][x].AI_style == 'hostile' and not 'blind' in self.npcs[yy][x].properties:
											monsters_list.append([x,yy])
								for xx in range(x-1,x+2):
									if self.npcs[y][xx] != 0 and self.npcs[y][xx].AI_style == 'hostile' and not 'blind' in self.npcs[y][xx].properties:
										monsters_list.append([xx,y])
											
								if len(monsters_list) > 0:
									
									if len(monsters_list) == 1:
										ran = 0
									else:
										ran = random.randint(0,len(monsters_list)-1)
										
									xxx = monsters_list[ran][0]
									yyy = monsters_list[ran][1]
									
									rand = random.randint(0,99)
									
									if rand < self.npcs[y][x].ability['blind']:
										mes = self.npcs[y][x].name + ' blinds ' + self.npcs[yyy][xxx].name + '.' #TIPO2
										message.add(mes)
										self.npcs[yyy][xxx].properties.append('blind')
										self.npcs[y][x].move_done = 1
										
							if 'stasis' in ability_keys:
								
								wr = self.npcs[y][x].ability['stasis'][1] 
								monsters_list = []
								for yy in range (y-wr,y+wr+1):
									for xx in range(x-wr,x+wr+1):
										try:
											if self.npcs[yy][xx] != 0 and self.npcs[yy][xx].AI_style == 'hostile':
												if self.check_los(player.pet_pos[0],player.pet_pos[1],xx,yy) == True:
													monsters_list.append([xx,yy])
										except:
											None
											
								if len(monsters_list) > 0:
									
									if len(monsters_list) == 1:
										ran = 0
									else:
										ran = random.randint(0,len(monsters_list)-1)
										
									xxx = monsters_list[ran][0]
									yyy = monsters_list[ran][1]
									
									rand = random.randint(0,99)
									
									if rand < self.npcs[y][x].ability['stasis'][0]:
										try:
											mes = self.npcs[y][x].name + ' stares at ' + self.npcs[yyy][xxx].name + '.' #TIPO2
											message.add(mes)
											duration = self.npcs[y][x].ability['stasis'][2]
											self.npcs[yyy][xxx].move_border += 10
											if self.npcs[yyy][xxx].move_border == 10:
												self.npcs[yyy][xxx].move_border += 1
											world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('stasis',xxx,yyy,duration))
											self.npcs[y][x].move_done = 1
										except:
											None
							
							if 'burn' in ability_keys:
								
								rand = random.randint(0,99)
								if rand < self.npcs[y][x].ability['burn']:
									monster_list = []
									for yy in range(y-1,y+2):
										for xx in range(x-1,x+2):
											if self.npcs[yy][xx] != 0 and self.tilemap[yy][xx].replace == None:
												if self.npcs[yy][xx].AI_style == 'hostile':
													if not 'flaming' in self.npcs[yy][xx].properties and not 'hot' in self.npcs[yy][xx].properties and not 'unflamable' in self.npcs[yy][xx].properties:
														monster_list.append((xx,yy))
									if len(monster_list) > 0:
										if len(monster_list) == 1:
											rand2 = 0
										else:
											rand2 = random.randint(0,len(monster_list)-1)
											
										xxx = monster_list[rand2][0]
										yyy = monster_list[rand2][1]
										
										mes = self.npcs[y][x].name + ' burns '+ self.npcs[yyy][xxx].name + '.' #TIPO2
										message.add(mes)
										
										sfx.play('flame')
										
										self.npcs[yyy][xxx] = 0
										replace = deepcopy(self.tilemap[yyy][xxx])
										self.tilemap[yyy][xxx] = deepcopy(tl.tlist['effect'][4])
										self.tilemap[yyy][xxx].replace = replace
										self.countdowns.append(countdown('flame',xxx,yyy,3))
							
							if 'eat_rock' in ability_keys:
								
								rand = random.randint(0,99)
								if rand < self.npcs[y][x].ability['eat_rock']:
									rock_list = []
									for yy in range(y-1,y+2):
										for xx in range(x-1,x+2):
											if self.tilemap[yy][xx].move_group == 'rock' and self.tilemap[yy][xx].replace != None:
												rock_list.append((xx,yy))
									if len(rock_list) > 0:
										if len(rock_list) == 1:
											rand2 = 0
										else:
											rand2 = random.randint(0,len(rock_list)-1)
											
										xxx = rock_list[rand2][0]
										yyy = rock_list[rand2][1]
										
										self.tilemap[yyy][xxx] = deepcopy(self.tilemap[yyy][xxx].replace)
										
										sfx.play('eat')
										
										mes = self.npcs[y][x].name + ' eats a rock.' #TIPO2
										message.add(mes)
							
							if 'warchant' in ability_keys or 'protectionspell' in ability_keys:
								if player.lp < player.attribute.max_lp*0.5:
									monster_count = 0
									for yy in range(player.pos[1]-3,player.pos[1]+4):
										for xx in range(player.pos[0]-3,player.pos[0]+4):
											try:
												if self.npcs[yy][xx] != 0:
													if	self.npcs[yy][xx].AI_style == 'hostile':
														monster_count += 1
											except:
												None
									if monster_count > 2:
										if 'protectionspell' in ability_keys:
											if player.buffs.get_buff('ironskin') == 0:
												mes = self.npcs[y][x].name + ' casts a spell of protection on you.' #TIPUS2
												message.add(mes)
												message.add('You feel your skin harden!') #TIPUS1
												screen.write_hit_matrix(x,y,7)
												player.buffs.set_buff('ironskin',30)
										elif 'warchant' in ability_keys:
											if player.buffs.get_buff('berserk') == 0:
												mes = self.npcs[y][x].name + ' intones a war chant.' #TIPO2
												message.add(mes)
												message.add('You are going berserk!') #TIPO1
												screen.write_hit_matrix(x,y,7)
												player.buffs.set_buff('berserk',30)
										
					#IV. Move the monster
					if do_move != 'foo':
						
						border = random.randint(1,9)
						
						if border > self.npcs[y][x].move_border:
							
							self.npcs[y][x].move_done = 1#set the move_done switch on
							helper = self.npcs[y][x]#copy the monster
							self.npcs[y][x] = 0 #del the monster at the old position
							self.npcs[do_move[1]][do_move[0]] = helper# set monster to the new position
	
		for y in range (0,max_map_size):#reset the move_done switches
			for x in range (0,max_map_size):
				
				if self.npcs[y][x] != 0:
					if self.npcs[y][x].lp > 0:
						self.npcs[y][x].move_done = 0
					else:
						test = False
						while test == False:
							test = self.monster_die(x,y)	
	def monster_die(self,x,y,xp = None):
		#this function is called when the player kills a monster. the x and the y variables are to define the location of the monster
		
		monster_x = x
		monster_y = y
		
		real_death = True
		real_drop = False
		
		if self.tilemap[y][x].replace == None:
			test_replace = True
		else:
			test_replace = False
		
		exception_list = ('make_blobs','wizard0','cage','vase')
		
		if self.npcs[monster_y][monster_x].corps_style in exception_list:
			test_replace = True
		
		die_mess = 'The ' + self.npcs[monster_y][monster_x].name + ' vanishes!' #TIPO2
		
		if test_replace != True or self.tilemap[y][x].drops_here != True:
			
			location_list = []
			
			for yy in range(y-1,y+2):
				for xx in range(x-1,x+2):
					if self.tilemap[yy][xx].replace == None and self.npcs[yy][xx] == 0:
						test_replace = True
					else:
						test_replace = False
						
					if test_replace == True and self.tilemap[yy][xx].drops_here and (self.tilemap[yy][xx].move_group == 'soil' or self.tilemap[yy][xx].move_group == 'dry_entrance') and self.containers[yy][xx] == 0:
						location_list.append((xx,yy))
			
			if len(location_list) < 1:
				real_death = False
				x = monster_x
				y = monster_y
			elif len(location_list) == 1:
				x = location_list[0][0]
				y = location_list[0][1]
			else:
				ran = random.randint(0,len(location_list)-1)
				x = location_list[ran][0]
				y = location_list[ran][1]
					
		if test_replace == True and self.tilemap[y][x].drops_here and real_death == True: #only on empty fields corps can be spawned
			
			if self.npcs[monster_y][monster_x].corps_style == 'dryade' and self.tilemap[y][x].techID != tl.tlist['misc'][0].techID and self.tilemap[y][x].can_grown: #dryades can leave behind a seppling when they are killed(corpse_lvl dosn't matter)/low water isn't allowed
				
				coin = random.randint(0,99)
				
				if coin < 50:#there is a chance of 50%
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = tl.tlist['local'][10]#<---sepling
					self.tilemap[y][x].replace = replace
					self.make_monsters_angry(x,y,'tree')
					
					die_mess = 'The ' + self.npcs[monster_y][monster_x].name + ' turns into a new tree!' #TIPO2
					 
			elif self.npcs[monster_y][monster_x].corps_style == 'troll' and self.tilemap[y][x].techID != tl.tlist['misc'][0]: #trolls can leave behind a rock when they are killed(corpse_lvl dosn't matter)/low water isn't allowed
				
				coin = random.randint(0,99)
				
				if coin < 50:#there is a chance of 50%
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['local'][14])#<---rock
					self.tilemap[y][x].replace = replace
					
					die_mess = 'The ' + self.npcs[monster_y][monster_x].name + ' turns to stone!' #TIPO2
					
			elif self.npcs[monster_y][monster_x].corps_style == 'human': #humanoid monsters can leave behind humanoid remains when they die. the corps_lvl says how much items are stored inside them
				
				coin = random.randint(0,99)
				
				if coin < 15:#there is a chance of 15%
					real_drop = True
					die_mess = 'The ' + self.npcs[monster_y][monster_x].name + ' dies!' #TIPO2
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][6])#<--humanoid remains
					self.tilemap[y][x].replace = replace
					
					items = []
					
					max_items = max(1,self.npcs[monster_y][monster_x].corps_lvl)
					
					for i in range (0, max_items):
						#possible drops of a humanoid monster are equipment items and food items
						
						coin = random.randint(0,99)
						
						if coin < 65: #there is a chance of 65% that a item becomes a eqipment item
							
							material = random.randint(0,20) #all materials are allowed
							classes = ('knife','sword','axe','dagger','shoes','cuisse','helmet','armor','wand','rune','rune staff','artefact','ring','amulet','seal ring','talisman','pickaxe') #CUIDAO
							kind = classes[random.randint(0,len(classes)-1)]#all classes of objects are allowed
							plus = random.randint(-2,+2)# a plus between -2 and +2 is possible
							state = random.randint(10,85)#the state of this used objects will always be between 10% and 80%
							curse_chance = random.randint(0,30)
							if curse_chance < material:
								curse = 0
							elif curse_chance == material:
								curse = 2
							else:
								curse = 1
 							
							item = item_wear(kind,material,plus,state,curse)
							
						elif coin < 68: #there is a chance of 3% to drop a simple blueprint
							
							blueprint = random.randint(15,20)
							item = deepcopy(il.ilist['misc'][blueprint])
						
						elif coin < 80: #there is a	chance of 12% to drop a torch or a throwable:
							
							item_list = (il.ilist['misc'][44],il.ilist['misc'][44],il.ilist['misc'][44],il.ilist['misc'][78],il.ilist['misc'][79],il.ilist['misc'][80])
							ran = random.randint(0,len(item_list)-1)
							item = deepcopy(item_list[ran])
							
						else:
							coin2 = random.randint(0,1)
							if coin == 1:
								item = deepcopy(il.ilist['food'][random.randint(0,len(il.ilist['food'])-1)])
							else:
								item_list = (il.ilist['misc'][74],il.ilist['misc'][75],il.ilist['misc'][76],il.ilist['misc'][77])
								ran = random.randint(0,len(item_list)-1)
								item = deepcopy(item_list[ran])
							
						items.append(item)
					
					self.add_container(items,x,y,deep_copy=True,checkIt=True)
			
			elif self.npcs[monster_y][monster_x].corps_style == 'animal': #humanoid monsters can leave behind humanoid remains when they die. the corps_lvl says how much items are stored inside them
				
				coin = random.randint(0,99)
				
				if player.inventory.check_suffix('Hunting') == True:
					coin = 0
				
				if coin < 15:#there is a chance of 15%
					real_drop = True
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][21])#<--animal remains
					self.tilemap[y][x].replace = replace
					
					items = []
					
					max_items = max(1,self.npcs[monster_y][monster_x].corps_lvl)
					
					for i in range (0, max_items):
						#animals drop flesh. the corpslvl says how much
							
						items.append(deepcopy(il.ilist['food'][9]))#<---raw meat
						
					self.add_container(items,x,y,deep_copy=True,checkIt=True)
					
					die_mess = 'The ' + self.npcs[monster_y][monster_x].name + ' dies!' #TIPO2
			
			elif self.npcs[monster_y][monster_x].corps_style == 'scrollkeeper': #scrollkeepers can leave behind humanoid remains with scrolls and spellbooks when they die. the corps_lvl says how much items are stored inside them
				
				coin = random.randint(0,99)
				
				if coin < 10:#there is a chance of 10%
					real_drop = True
					die_mess = 'The ' + self.npcs[monster_y][monster_x].name + ' dies!' #TIPO2
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][6])#<--humanoid remains
					self.tilemap[y][x].replace = replace
					
					items = []
					
					max_items = max(1,self.npcs[monster_y][monster_x].corps_lvl)
					
					for i in range (0, max_items):
						#possible drops of a scrollkeeper are scrolls and spellbooks
						
						coin = random.randint(0,99)
						
						if coin < 75: #there is a chance of 75% that a item becomes a scroll
							
							scrolls = (il.ilist['misc'][25],il.ilist['misc'][27],il.ilist['misc'][29],il.ilist['misc'][31],il.ilist['misc'][33],il.ilist['misc'][35],il.ilist['misc'][37],il.ilist['misc'][45],il.ilist['misc'][82])
							
							ran = random.randint(0,len(scrolls)-1)
							
							item = deepcopy(scrolls[ran])
								
						else:
							
							books = (il.ilist['misc'][26],il.ilist['misc'][30],il.ilist['misc'][32],il.ilist['misc'][34],il.ilist['misc'][36],il.ilist['misc'][38],il.ilist['misc'][46],il.ilist['misc'][83])
							
							ran = random.randint(0,len(books)-1)
							
							item = deepcopy(books[ran])
							
						items.append(item)
						
					self.add_container(items,x,y,deep_copy=True,checkIt=True)
			
			elif self.npcs[monster_y][monster_x].corps_style == 'explode': #this monster explodes when it dies
				
				die_mess = 'The ' + self.npcs[monster_y][monster_x].name + ' explodes!' #TIPO2
				self.countdowns.append(countdown('bomb1',monster_x,monster_y,1))
			
			elif self.npcs[monster_y][monster_x].corps_style == 'wizard0':
				screen.render_request('[Wizard]','Slowly I become really angry!','Time to finish this!',False,portrait='wizard_angry') #TIPO1
				ui = getch(screen.displayx,screen.displayy,0,0,mouse=game_options.mousepad)
			
			elif self.npcs[monster_y][monster_x].corps_style == 'wizard1':
				screen.render_request('[Wizard]','You beat me!?',' ',False,portrait='wizard_angry') #TIPO1
				ui = getch(screen.displayx,screen.displayy,0,0,mouse=game_options.mousepad)
				screen.render_request('[Wizard]','Incredible!',' ',False,portrait='wizard_angry') #TIPO1
				ui = getch(screen.displayx,screen.displayy,0,0,mouse=game_options.mousepad)
				screen.render_request('[Wizard]','But in the end... the forces...','of chaos... will always win...',False,portrait='wizard_neutral') #TIPO1
				ui = getch(screen.displayx,screen.displayy,0,0,mouse=game_options.mousepad)
				screen.render_fade(True,False,color=(255,255,255))
				screen.render_boss_defeated()
				screen.render_fade(False,True,color=(255,255,255))
				player.xp += 50
				if player.xp > 100:
					player.lvl_up()
				real_drop = True
				replace = self.tilemap[y][x]
				self.tilemap[y][x] = deepcopy(tl.tlist['misc'][32])#set a ring
				self.tilemap[y][x].replace = replace
				player.quest_variables.append('wizard_defeated')
				try:
					player.questlog.log['[Main] Showdown!'].status = 2 #TIPO1
				except:
					None
			
			elif self.npcs[monster_y][monster_x].corps_style == 'miner':
				
				if self.npcs[monster_y][monster_x].techID == ml.mlist['special'][0].techID:#this is a vase
					die_mess = 'The vase shatters.' #DUBTE
					
				ran = random.randint(0,99)
					
				if ran <= self.npcs[monster_y][monster_x].corps_lvl: #for miners the corps_lvl determinates the chance of getting a gem
					
					real_drop = True
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['misc'][9])#set a lost gem
					self.tilemap[y][x].replace = replace
					
				elif ran <= self.npcs[monster_y][monster_x].corps_lvl*4:#for miners the corps_lvl determinates the chance of getting some ore. Its the chance to get a gem
					
					real_drop = True	
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['misc'][11])#set a lost ore
					self.tilemap[y][x].replace = replace
				
				elif ran <= self.npcs[monster_y][monster_x].corps_lvl*10:#for miners the corps_lvl determinates the chance of getting some ore. Its the chance to get a gem
					
					real_drop = True	
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['misc'][33])#set a lost coin
					self.tilemap[y][x].replace = replace
			
			elif self.npcs[monster_y][monster_x].corps_style == 'thief':
				
				if self.tilemap[y][x].replace == None and self.npcs[monster_y][monster_x].corps_lvl > 0:
					
					real_drop = True
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['misc'][9])#set a lost gem
					self.tilemap[y][x].replace = replace
					self.tilemap[y][x].conected_resources = ('gem',self.npcs[monster_y][monster_x].corps_lvl)#for thiefs the corps lvl determinates the number of gems they are dropping
			
			elif self.npcs[monster_y][monster_x].corps_style == 'reset_parent':
				
				parent_id = self.npcs[monster_y][monster_x].personal_id.replace('_child','')
				
				for yy in range(0,max_map_size):
					for xx in range(0,max_map_size):
						if self.npcs[yy][xx] != 0:
							if self.npcs[yy][xx].personal_id == parent_id:
								self.npcs[yy][xx].num_special += 1
							
			elif self.npcs[monster_y][monster_x].corps_style == 'kill_childs':
				
				child_id = self.npcs[monster_y][monster_x].personal_id + '_child'
				
				for yy in range(0,max_map_size):
					for xx in range(0,max_map_size):
						if self.npcs[yy][xx] != 0:
							if self.npcs[yy][xx].personal_id == child_id:
								self.npcs[yy][xx] = 0
			
			elif self.npcs[monster_y][monster_x].corps_style == 'kobold_fear':
				for yy in range(y-7,y+8):
					for xx in range(x-7,x+8):
						try:
							if self.npcs[yy][xx].techID == ml.mlist['kobold'][1].techID and self.npcs[yy][xx].name != 'frightened kobold':
								self.npcs[yy][xx] = deepcopy(self.npcs[yy][xx])#only to be sure
								
								self.npcs[yy][xx].name = 'frightened kobold'
								self.npcs[yy][xx].sprite_pos = (5,3)
								
								self.npcs[yy][xx].basic_attribute.p_strength = int(self.npcs[yy][xx].basic_attribute.p_strength*0.6)
								self.npcs[yy][xx].basic_attribute.m_strength = int(self.npcs[yy][xx].basic_attribute.m_strength*0.6)
								self.npcs[yy][xx].basic_attribute.p_defense = int(self.npcs[yy][xx].basic_attribute.p_defense*0.6)
								self.npcs[yy][xx].basic_attribute.m_defense = int(self.npcs[yy][xx].basic_attribute.m_defense*0.6)
								
								screen.write_hit_matrix(xx,yy,17)
								
								coin = random.randint(0,1)
								if coin == 1:
									self.npcs[yy][xx].AI_style = 'flee'
						except:
							None
					
			elif self.npcs[monster_y][monster_x].corps_style == 'vase':
				
				die_mess = 'The vase shatters and monsters jump out.' #DUBTE
				monster_count = 0
				
				for yy in range(y-1,y+2):
					for xx in range(x-1,x+2):
						
						if yy != player.pos[1] or xx!= player.pos[0]:
							if self.npcs[yy][xx] == 0 and self.tilemap[yy][xx].move_group == 'soil' and self.tilemap[yy][xx].damage == 0:
								self.npcs[yy][xx] = deepcopy(ml.mlist['special'][2])#set vase monsters
								self.set_monster_strength(xx,yy,player.pos[2])
								if player.difficulty == 4:
									self.npcs[yy][xx].AI_style = 'ignore'
								monster_count += 1
								
				if monster_count > 0:
					die_mess = 'The vase shatters and '+str(monster_count)+' monsters jump out.' #TIPO2
				else:
					die_mess = 'The vase shatters.' #DUBTE
								
			elif self.npcs[monster_y][monster_x].corps_style == 'mimic':
				
				die_mess = 'The mimic wakes up.' #DUBTE
			
			elif self.npcs[monster_y][monster_x].corps_style == 'cage':
				
				die_mess = 'You smash the cage!' #DUBTE
				sfx.play('destroy_cage')
				
			elif self.npcs[monster_y][monster_x].corps_style == 'make_blobs':
				
				counter = 0
				blob_lvl = max(self.npcs[monster_y][monster_x].lvl-1,0)
				
				for yy in range(y-1,y+2):
					for xx in range(x-1,x+2):
						if yy != y or xx != x:
							not_player_pos = yy != player.pos[1] or xx != player.pos[0]
							if self.tilemap[yy][xx].move_group == 'soil' and not_player_pos == True and self.npcs[yy][xx] == 0:
								self.npcs[yy][xx] = deepcopy(ml.mlist['special'][15])#set a green blob
								self.set_monster_strength(xx,yy,player.pos[2],preset_lvl=blob_lvl)
								if player.difficulty == 4:
									self.npcs[yy][xx].AI_style = 'ignore'
								counter += 1
				
				if counter == 1:
					die_mess = 'The giant blob leaves behind a small blob.' #DUBTE
				elif counter > 1:
					die_mess = 'The giant blob bursts into '+str(counter)+' small blobs.' #TIPO2
						
			elif self.npcs[monster_y][monster_x].corps_style == 'life_essence':
				
				real_drop = True
				replace = self.tilemap[y][x]
				self.tilemap[y][x] = deepcopy(tl.tlist['functional'][35])#set a heart-shaped crystall
				self.tilemap[y][x].replace = replace
			
			elif self.npcs[monster_y][monster_x].corps_style == 'mummy':
				
				coin = random.randint(0,1)
				if coin == 1:
					real_drop = True
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][36])#set a heap of mummy dust
					self.tilemap[y][x].replace = replace
					
			elif self.npcs[monster_y][monster_x].corps_style == 'spider':
				
				coin = random.randint(0,self.npcs[monster_y][monster_x].corps_lvl)
				if coin == 1:
					real_drop = True
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][37])#set a spider eye
					self.tilemap[y][x].replace = replace
			
			elif self.npcs[monster_y][monster_x].corps_style == 'jelly':
				
				coin = random.randint(0,1)
				if coin == 1:
					lvl = self.npcs[monster_y][monster_x].corps_lvl
					real_drop = True
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['functional'][38+lvl])#set a jelly
					self.tilemap[y][x].replace = replace
			
			elif self.npcs[monster_y][monster_x].corps_style == 'toolbox':
				
				lvl = self.npcs[monster_y][monster_x].corps_lvl
				real_drop = True
				replace = self.tilemap[y][x]
				self.tilemap[y][x] = deepcopy(tl.tlist['quest'][0])#set lost tool box
				self.tilemap[y][x].replace = replace
			
			elif self.npcs[monster_y][monster_x].corps_style == 'neko_amulet':
				
				lvl = self.npcs[monster_y][monster_x].corps_lvl
				real_drop = True
				replace = self.tilemap[y][x]
				self.tilemap[y][x] = deepcopy(tl.tlist['quest'][1])#set a neko amulet
				self.tilemap[y][x].replace = replace
				
			elif self.npcs[monster_y][monster_x].corps_style == 'vanish':
				
				ran = random.randint(0,99)
					
				if ran <= self.npcs[monster_y][monster_x].corps_lvl: #the corps_lvl determinates the chance of getting a present
					
					real_drop = True
					replace = self.tilemap[y][x]
					self.tilemap[y][x] = deepcopy(tl.tlist['misc'][13])#set a present
					self.tilemap[y][x].replace = replace
						
					item_ran = random.randint(0,99)
						
					if item_ran < 25:
							
						items = [il.ilist['misc'][43]]#set a heavy bag
						self.add_container(items,x,y,deep_copy=True,checkIt=True)
					
					elif item_ran < 50:
						
						choose_ran = random.randint(0,len(il.ilist['clothe'])-1)	
						items = [il.ilist['clothe'][choose_ran]]
						self.add_container(items,x,y,deep_copy=True,checkIt=True)
							
					elif item_ran < 95:
							
						r = random.randint(3,7)
							
						items = [il.ilist['misc'][r]]#set a workbench
						self.add_container(items,x,y,deep_copy=True,checkIt=True)
							
					else:
							
						items = [il.ilist['misc'][70]]#set a book of skill
						self.add_container(items,x,y,deep_copy=True,checkIt=True)
						
				
			############ADD MORE HERE###############
		if real_drop == True:
			screen.write_hit_matrix(x,y,16)
		
		if self.npcs[monster_y][monster_x].move_border < 10 and self.npcs[monster_y][monster_x].corps_style not in exception_list:
			screen.write_hit_matrix(monster_x,monster_y,13)
		
		if self.npcs[monster_y][monster_x].corps_style == 'mimic':
			self.npcs[monster_y][monster_x] = deepcopy(ml.mlist['special'][4])#set a mimic
			self.set_monster_strength(monster_x,monster_y,player.pos[2])
			if player.difficulty == 4:
				self.npcs[monster_y][monster_x].AI_style = 'ignore'
		elif self.npcs[monster_y][monster_x].corps_style == 'cage':
			self.npcs[monster_y][monster_x] = deepcopy(ml.mlist['rescued'][0])
			self.set_monster_strength(monster_x,monster_y,player.pos[2])
		elif self.npcs[monster_y][monster_x].corps_style == 'wizard0':
			lvl = self.npcs[monster_y][monster_x].lvl
			self.npcs[monster_y][monster_x] = deepcopy(ml.mlist['special'][30])#set angry wizard
			self.set_monster_strength(monster_x,monster_y,player.pos[2],preset_lvl = lvl)
			self.npcs[monster_y][monster_x].lp = 10*player.lp_boost
			if player.difficulty == 4:
				self.npcs[monster_y][monster_x].AI_style = 'ignore'
		else:
			self.npcs[monster_y][monster_x] = 0 #always del the monster if it is no mimic or cage
		
		self.make_monsters_angry(monster_x,monster_y,'kill')
		self.monster_count -= 1
		if xp != None:
			die_mess = die_mess + ' [+' + str(xp) + 'xp]' #DUBTE
		message.add(die_mess)
		return True
	
	def make_shops(self):
		
		num = int((max_map_size*max_map_size) / (50*50))
		
		for i in range (0,num):
			
			run = True
				
			while run:
				poses = self.find_all_moveable(False,False)
				ran = random.randint(0,len(poses)-1)
				pos = poses[ran]
				
				if min(pos[0],pos[1]) > 4 and max(pos[0],pos[1]) < max_map_size-4:
					run = False
			
			x = pos[0]
			y = pos[1]
			
			for yy in range(y-2,y+3):
				for xx in range(x-2,x+3):
					
					self.npcs[yy][xx] = 0 #always del the monsters
					
					if xx == x-2 or xx == x+2 or yy == y-2 or yy == y+2:
						self.tilemap[yy][xx] = deepcopy(tl.tlist['shop'][1])
					else:
						self.tilemap[yy][xx] = deepcopy(tl.tlist['shop'][0])
						
			self.tilemap[y][x-2] = deepcopy(tl.tlist['shop'][2])
			self.tilemap[y][x+2] = deepcopy(tl.tlist['shop'][2])
			self.tilemap[y-2][x] = deepcopy(tl.tlist['shop'][2])
			self.tilemap[y+2][x] = deepcopy(tl.tlist['shop'][2])   
			
			if self.map_type == 'orcish_mines':			
				self.npcs[y][x] = deepcopy(ml.mlist['shop'][1])
			elif self.map_type == 'grot':			
				self.npcs[y][x] = deepcopy(ml.mlist['shop'][2])
			else:
				self.npcs[y][x] = deepcopy(ml.mlist['shop'][0])#the elfish shopkeeper is only for fallback...In the elfish fortress the shops are spawned on a other way
	
	def make_monsters_angry(self,x,y,style):
		
		for yy in range(y-3,y+4):
			for xx in range(x-3,x+4):
				
				try:
					if self.npcs[yy][xx] != 0:
						if self.npcs[yy][xx].anger == style:
							lvl = self.npcs[yy][xx].lvl
							self.npcs[yy][xx] = deepcopy(ml.mlist['angry_monster'][self.npcs[yy][xx].anger_monster])
							self.set_monster_strength(xx,yy,player.pos[2],lvl)
							if player.difficulty == 4:
								self.npcs[yy][xx].AI_style = 'ignore'		
				except:
					None
	
	def time_pass(self):
		#This function refresches the map for every day that past since players last visit... make plants growing etc.
		
		if self.last_visit != time.day_total:
			
			screen.render_load(10)
			
			past_time = time.day_total - self.last_visit
			
			if past_time < 0:
				past_time = 364 - past_time
				
			for c in range (0,past_time):
				
				for y in range (0,max_map_size):
					for x in range(0,max_map_size):
						
						tile = self.tilemap[y][x]
						
						#######Life of plants######
						
						#1. Scrub
						if tile.grow_group == 'scrub':
							rand = random.randint(0,99)
							if rand < 50:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
							
						if tile.grow_group == 'scrub_buds':
							rand = random.randint(0,99)
							if rand < 90:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
						
						if tile.grow_group == 'scrub_blossom':
							rand = random.randint(0,99)
							if rand < 80:
								scrubs = random.randint(0,2)
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[scrubs][0]][tile.conected_tiles[scrubs][1]])
								self.tilemap[y][x].replace = replace
							
						if tile.grow_group == 'scrub_berries':
							rand = random.randint(0,99)
							if rand < 50:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
								self.tilemap[y][x].replace = replace
							elif rand > 49 and rand < 75:
								numbers =(-1,1)
								
								for yy in numbers:
									for xx in numbers:
										try:
											
											if self.tilemap[y+yy][x+xx].can_grown == True:
											
												coin = random.randint(0,99)
												
												if coin < 25: #25%
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy([tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
													self.tilemap[y+yy][x+xx].replace = replace
										except:
											None
											
						if tile.grow_group == 'scrub_scruffy':
							rand = random.randint(0,99)
							if rand < 90:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
								self.tilemap[y][x].replace = replace
							else:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
								self.tilemap[y][x].replace = replace
								
						
						if tile.grow_group == 'scrub_grow':
							rand = random.randint(0,99)
							if rand < 90:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
								
						#2.Tree
						
						if tile.grow_group == 'tree_grow':
							rand = random.randint(0,99)
							if rand < 80 and self.npcs[y][x] == 0:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
						
						if tile.grow_group == 'tree':
							rand = random.randint(0,99)
							if rand < 5:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
								self.tilemap[y][x].replace = replace

							elif rand > 69:
								numbers =(-2,2)
								
								for yy in numbers:
									for xx in numbers:
										try:
											
											if self.tilemap[y+yy][x+xx].can_grown == True:
											
												coin = random.randint(0,3)
												
												if coin == 0:
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
													self.tilemap[y+yy][x+xx].replace = replace
										except:
											None
						
						#3.Herb
						
						if tile.grow_group == 'herblike':
							rand = random.randint(0,99)
							if rand < 20:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
								self.tilemap[y][x].replace = replace
								
						
						#4. Blue Mushrooms
						
						if tile.grow_group == 'mushroom_mud':
							
							rand = random.randint(0,99)
							
							if rand < 5:
								
								for yy in range(-1,1):
									for xx in range(-1,1):
										try:
											
											if self.tilemap[y+yy][x+xx].techID == tl.tlist['misc'][1].techID:#here is mud 
											
												cent = random.randint(0,99)
												
												if cent < 25 :
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
													self.tilemap[y+yy][x+xx].replace = replace
										except:
											None
						
						#5. Brown Mushrooms
						
						if tile.grow_group == 'mushroom_treelike':
							rand = random.randint(0,99)
							if rand < 5:
								
								for yy in range(-1,1):
									for xx in range(-1,1):
										try:
											
											if self.tilemap[y+yy][x+xx].techID == tl.tlist['global_caves'][0].techID:#here is cave ground
											
												cent = random.randint(0,99)
												
												if cent < 25 :
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]])
													self.tilemap[y+yy][x+xx].replace = replace
													
										except:
											None
							
							elif rand < 30:#make a giant mushroom
								
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]])
								self.tilemap[y][x].replace = replace
									
						#6. Purple Mushrooms
						
						if tile.grow_group == 'mushroom': #let grow new mushrooms and let the old ones die(5%)
							rand = random.randint(0,99)
							if rand < 5:
								
								for yy in range(-1,1):
									for xx in range(-1,1):
										try:
											
											if self.tilemap[y+yy][x+xx].techID == tl.tlist['global_caves'][0].techID:#here is cave ground
											
												cent = random.randint(0,99)
												
												if cent < 25 :
													replace = self.tilemap[y+yy][x+xx]
													self.tilemap[y+yy][x+xx] = deepcopy(tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]])
													self.tilemap[y+yy][x+xx].replace = replace
												
										except:
											None
											
						#7. Agriculture
						
						if tile.grow_group == 'agri0':
							rand = random.randint(0,99)
							if rand < 50:
								if self.map_type == 'overworld': 
									self.tilemap[y][x] = tl.tlist[tile.conected_tiles[0][0]][tile.conected_tiles[0][1]]
								elif self.map_type == 'cave' or self.map_type == 'desert_cave':
									self.tilemap[y][x] = tl.tlist[tile.conected_tiles[1][0]][tile.conected_tiles[1][1]]
								elif self.map_type == 'desert':
									self.tilemap[y][x] = tl.tlist[tile.conected_tiles[2][0]][tile.conected_tiles[2][1]]
									
						if tile.grow_group == 'agri1': #let something grow on a acriculture (final, at the overworld) (50%)
							rand = random.randint(0,99)
							if rand < 50:
									self.tilemap[y][x] = tl.tlist[tile.conected_tiles[0]][tile.conected_tiles[1]]
						
						#8. Vanish
						if tile.grow_group == 'vanish':
							rand = random.randint(0,99)
							if rand < 50:
								self.tilemap[y][x] = self.tilemap[y][x].replace
								self.containers[y][x] = 0
								
					#######Misc#######
						
						#0. Rubble
						if tile.techID == tl.tlist['functional'][26].techID:
							rand = random.randint(0,99)
							if rand < 20:
								count_rubble = 0
								count_sand = 0
								count_grass = 0
								count_cave = 0
								for yy in range(y-1,y+2):
									for xx in range(x-1,x+2):
										if self.tilemap[yy][xx].techID == tl.tlist['functional'][26].techID:#this is rubble
											count_rubble += 1
										elif self.tilemap[yy][xx].techID == tl.tlist['local'][0].techID:#this is grass
											count_grass += 1
										elif self.tilemap[yy][xx].techID == tl.tlist['extra'][0].techID:#this is sand
											count_sand += 1
										elif self.tilemap[yy][xx].techID == tl.tlist['global_caves'][0].techID:#this is cave
											count_cave +=1
								if count_rubble < 8: #this tile isn't surrounded by rubble
									if count_cave > 0:
										self.tilemap[y][x] = deepcopy(tl.tlist['global_caves'][0])
									elif count_grass > count_sand and count_grass > 0:
										self.tilemap[y][x] = deepcopy(tl.tlist['local'][0])
									elif count_sand > 0:
										self.tilemap[y][x] = deepcopy(tl.tlist['extra'][0])
					
						#1. nest box (with egg)
						if tile.grow_group == 'hatch':
							rand = random.randint(0,99)
							if rand < 80 and self.npcs[y][x] == 0:
								replace = self.tilemap[y][x].replace
								self.tilemap[y][x] = deepcopy(tl.tlist['sanctuary'][4])
								self.tilemap[y][x].replace = replace
								pet_num = []
								for i in range(0,len(ml.mlist['pet']),3):
									pet_num.append(i)
								ran = random.randint(0,len(pet_num)-1)
								num = pet_num[ran]
								self.npcs[y][x] = deepcopy(ml.mlist['pet'][num])
								self.set_monster_strength(x,y,1)
						
						#2. chicklet to chicken
						if self.npcs[y][x] != 0:
							if self.npcs[y][x].techID == ml.mlist['special'][29].techID:
								lvl = self.npcs[y][x].lvl
								self.npcs[y][x] = deepcopy(ml.mlist['overworld'][3])
								self.set_monster_strength(x,y,1,preset_lvl=lvl)
						
						#3. chicken nest
						if tile.grow_group == 'hatch_chicken':
							replace = self.tilemap[y][x].replace
							self.tilemap[y][x] = deepcopy(tl.tlist['functional'][43])
							self.tilemap[y][x].replace = replace
							self.npcs[y][x] = deepcopy(ml.mlist['special'][29])
							self.set_monster_strength(x,y,1)
						#4. mud
						if tile.techID == tl.tlist['misc'][1].techID:
							test = self.find_first(tl.tlist['local'][0]) #tests if grass grows on this map ==> this is a surface map
							if test != False:
								coin = random.randint(0,1)
								if coin == 1:
									self.tilemap[y][x] = deepcopy(tl.tlist['local'][0])
						#5. make flowers
						if tile.techID == tl.tlist['local'][0].techID: #this is grass
							coin = random.randint(0,10)
							if coin == 1:
								ran = random.randint(0,len(tl.tlist['flower'])-1)
								self.tilemap[y][x] = deepcopy(tl.tlist['flower'][ran])
								self.tilemap[y][x].replace = deepcopy(tl.tlist['local'][0])
						#6. flower die
						id_list = []
						for i in tl.tlist['flower']:
							id_list.append(i.techID)
							
						if tile.techID in id_list: #this is a flower
							coin = random.randint(0,1)
							if coin == 1:
								self.tilemap[y][x] = self.tilemap[y][x].replace
						#7. despawn (chicken) eggs
						if tile.techID == tl.tlist['functional'][33].techID:
							coin = random.randint(0,1)
							if coin == 1:
								self.tilemap[y][x] = self.tilemap[y][x].replace
								
						#########add other events for growing plants etc here########
				
				self.last_visit = time.day_total #change the day of last visit to today to prevent the map of changed a second time for this day
				
			screen.render_load(5)
			save(world,player,time,gods,save_path,os.sep)
			
	def exchange(self,old_tile,new_tile,use_deepcopy=False):
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if self.tilemap[y][x].techID == old_tile.techID:
					if use_deepcopy == False:
						self.tilemap[y][x] = new_tile
					else:
						self.tilemap[y][x] = deepcopy(new_tile)
					
	def find_first(self,tile):
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				if self.tilemap[y][x].techID == tile.techID and self.npcs[y][x] == 0:
					return [x,y]
					
				if self.tilemap[y][x].name == tile.name and self.npcs[y][x] == 0:#fallback
					return [x,y]
		
		return False
					
	def find_any(self,tile):
		
		found = []
		
		for y in range(0,max_map_size):
			for x in range(0,max_map_size):
				
				if self.tilemap[y][x].techID == tile.techID and self.npcs[y][x] == 0:
					found.append((x,y))
					
		if found == []:
			return False
		elif len(found) == 1:
			return found[0]
		else:
			ran = random.randint(0,len(found)-1)
			return found[ran]
	
	def find_all_moveable(self,ignore_water = True,ignore_player_pos = False, ignore_no_spawn = True):

		cordinates_list = []
		for y in range (0, max_map_size):
			for x in range (0,max_map_size):
				
				moveable = False
				
				if ignore_water == True:
					if self.tilemap[y][x].move_group == 'soil':
						moveable = True
				else:
					if self.tilemap[y][x].move_group == 'soil' or self.tilemap[y][x].move_group == 'low_liquid':
						moveable = True
				
				if ignore_player_pos == True:
					player_pos_check = False
				else:
					if (x - entrance_x < -7) or (y - entrance_y < -7) or (x - entrance_x > 7) or (y - entrance_y > 7):
						player_pos_check = False
					else:
						player_pos_check = True
				
				spawn_check = True
				if ignore_no_spawn == False:
					if self.tilemap[y][x].no_spawn == True:
						spawn_check = False
				
				if (moveable == True) and (self.tilemap[y][x].damage == False) and (player_pos_check == False) and (spawn_check == True) and self.npcs[y][x] == 0:
					cordinates_list.append((x,y))
						
		if len(cordinates_list) > 0:
			return cordinates_list
				
		else:
					
			return False
	
	def add_container(self, inventory, x, y, deep_copy = True, checkIt = False):
		
		self.containers[y][x] = container(inventory,deep_copy)
		
		if checkIt == True:
			if self.check_container(x,y) != True:
				print('Container creation failed!') #TIPO1
				self.containers[y][x] = 0
				self.tilemap[y][x] = self.tilemap[y][x].replace
	
	def check_container(self,x,y):
		
		if self.tilemap[y][x].replace != None and len(self.containers[y][x].items) > 0:
			return True
		else:
			return False 
	
	def special_check(self,x,y):
		sfx_flame = False
		sfx_vapor = False
		for yy in range(y-7,y+8):
			for xx in range(x-7,x+8):
				try:
					if self.tilemap[yy][xx].techID == tl.tlist['misc'][4].techID or self.tilemap[yy][xx].techID == tl.tlist['misc'][5].techID:
						if player.inventory.check_suffix('See Ore') == True:
							self.known[yy][xx] = 1
					
					if (self.tilemap[yy][xx].special_group == 'flamable' or self.tilemap[yy][xx].special_group == 'highly flamable') and self.tilemap[yy][xx].replace != None:
						heat_source = 0
						
						for yyy in range(yy-1,yy+2):
							for xxx in range(xx-1,xx+2):
								try:
									if self.tilemap[yyy][xxx].special_group == 'hot':
										heat_source += 1
									if self.npcs[yyy][xxx] != 0:
										if 'hot' in self.npcs[yyy][xxx].properties:
											heat_source += 1
											if yyy == yy and xxx == xx:
												heat_source +=3
								except:
									None
										
						if heat_source > 0:
							if self.tilemap[yy][xx].special_group == 'flamable':
								ran = random.randint(0,9)
							else:
								ran = 9	
				
							if ran > 5:
								sfx_flame = True
								self.containers[yy][xx] = 0
								if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] != 0:
										if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].techID == ml.mlist['special'][14].techID: #this is a demonic chest
											world.maplist[player.pos[2]][player.on_map].monster_die(xx,yy)
										else:
											burn_mob = True
											exception_list = ('hot','unflamable','flaming')
											for i in exception_list:
												if i in world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].properties:
													burn_mob = False
											if burn_mob == True:
												world.maplist[player.pos[2]][player.on_map].monster_die(xx,yy)
								self.countdowns.append(countdown('flame',xx,yy,self.tilemap[yy][xx].special_num+3))
								replace = self.tilemap[yy][xx].replace
								self.tilemap[yy][xx] = deepcopy(tl.tlist['effect'][4])
								self.tilemap[yy][xx].replace = replace			
											
					elif self.tilemap[yy][xx].special_group == 'explosive' or self.tilemap[yy][xx].special_group == 'highly explosive':				
							heat_sources = 0
							for yyy in range(yy-1,yy+2):
								for xxx in range(xx-1,xx+2):
									try:
										if self.tilemap[yyy][xxx].special_group == 'hot':
											heat_sources += 1 
										if self.npcs[yyy][xxx] != 0:
											if 'hot' in self.npcs[yyy][xxx].properties:
												heat_sources += 1
												if yyy == yy and xxx == xx:
													heat_sources += 2
									except:
										None
							
							if heat_sources > 0:
								if self.tilemap[yyy][xxx].special_group == 'explosive':
									ran = random.randint(0,9)
								else:
									ran = 9	
								
								if ran > 5:
									self.countdowns.append(countdown('bomb1',xx,yy,1))
									for yyy in range(yy-1,yy+2):
										for xxx in range(xx-1,xx+2):
											try:
												if self.tilemap[yyy][xxx].special_group == 'explosive' or elf.tilemap[yyy][xxx].special_group == 'highly explosive':
													self.countdowns.append(countdown('bomb1',xxx,yyy,1))
											except:
												None
									
											
					elif self.tilemap[yy][xx].special_group == 'vaporable':
							heat_sources = 0
							for yyy in range(yy-1,yy+2):
								for xxx in range(xx-1,xx+2):
									try:
										if self.tilemap[yyy][xxx].special_group == 'hot':
											heat_sources += 1
										if self.npcs[yyy][xxx] != 0:
											if 'hot' in self.npcs[yyy][xxx].properties:
												heat_sources += 1
												if yyy == yy and xxx == xx:
													heat_sources +=3
									except:
										None
							if heat_sources >= self.tilemap[yy][xx].special_num:
								sfx_vapor = True
								self.tilemap[yy][xx] = deepcopy(tl.tlist['misc'][1])#mud
					
					if self.tilemap[yy][xx].techID == tl.tlist['sewer'][2].techID or self.tilemap[yy][xx].techID == tl.tlist['sewer'][5].techID:#dirty water
						for yyy in range(yy-1,yy+2):
								for xxx in range(xx-1,xx+2):
									try:
										if self.tilemap[yyy][xxx].techID == tl.tlist['misc'][0].techID: #clean water gets dirty
											self.tilemap[yyy][xxx] = deepcopy(tl.tlist['sewer'][2])
										if self.tilemap[yyy][xxx].techID == tl.tlist['misc'][3].techID:
											self.tilemap[yyy][xxx] = deepcopy(tl.tlist['sewer'][5])
									except:
										None
				except:
					None
		if sfx_flame == True:
			sfx.play('flame')
		if sfx_vapor == True:
			sfx.play('steam')
	
	def spawn_monster_groups(self,leader,follower,max_group_size):
		
		for y in range(0,max_map_size):
			for x in range(0,max_map_size):
				
				if self.npcs[y][x] != 0 and self.npcs[y][x].techID == leader.techID:
					m_count = 1
					for yy in range(y-1,y+2):
						for xx in range(x-1,x+2):
							if m_count < max_group_size and self.npcs[yy][xx] == 0 and self.tilemap[yy][xx].move_group in follower.move_groups:
								self.npcs[yy][xx] = deepcopy(follower)
								self.set_monster_strength(xx,yy,max(self.npcs[y][x].lvl-5,1))
								if player.difficulty == 4:
									self.npcs[yy][xx].AI_style = 'ignore'
								m_count += 1
						
	
	def make_special_monsters(self, min_no, max_no, on_tile, depth, monster_type='vase'):
		
		size = int((max_map_size*max_map_size)/(50*50))
		
		for i in range(0,size):
			
			num_monster = random.randint(min_no,max_no)
			
			if num_monster > 0:
				
				for z in range (0,num_monster):
					
					pos = self.find_any(on_tile)
					
					if monster_type == 'vase':
						
						ran = random.randint(0,99)
						
						if ran < 10:
							self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][1]) #spawn a monster vase
							self.npcs[pos[1]][pos[0]].attribute = attribute(0,0,0,0,0,1,0)
						else:
							self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][0]) #spawn a vase
							self.npcs[pos[1]][pos[0]].attribute = attribute(0,0,0,0,0,1,0)
							
					elif monster_type == 'mimic':
						
						pos = self.find_any(on_tile)
						self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][3]) #spawn a sleeping mimic
						self.npcs[pos[1]][pos[0]].attribute = attribute(0,0,0,0,0,1,0)
					
					elif monster_type == 'animated statue':
						pos = self.find_any(on_tile)
						self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][17])
						self.set_monster_strength(pos[0],pos[1],depth)
						if player.difficulty == 4:
							self.npcs[pos[1]][pos[0]].AI_style = 'ignore'
					
					elif monster_type == 'drowner':
						pos = self.find_any(on_tile)
						self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][13])
						self.set_monster_strength(pos[0],pos[1],depth)
						if player.difficulty == 4:
							self.npcs[pos[1]][pos[0]].AI_style = 'ignore'
					
					elif monster_type == 'demonic chest':
						pos = self.find_any(on_tile)
						self.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][4])#cest
						self.tilemap[pos[1]][pos[0]].replace = deepcopy(on_tile)
						sb = (il.ilist['misc'][26],il.ilist['misc'][30],il.ilist['misc'][32],il.ilist['misc'][34],il.ilist['misc'][36],il.ilist['misc'][38],il.ilist['misc'][46],il.ilist['misc'][83])
						ran1 = random.randint(0,len(sb)-1)
						ran2 = random.randint(0,len(sb)-1)
						items = [sb[ran1],sb[ran2]]
						self.containers[pos[1]][pos[0]] = container(items,True)			
						
						self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][14])
						self.set_monster_strength(pos[0],pos[1],depth)
						if player.difficulty == 4:
							self.npcs[pos[1]][pos[0]].AI_style = 'ignore'
					
					elif monster_type == 'tame_orc':
						pos = self.find_any(on_tile)
						coin = random.randint(0,1)
						self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['civilian'][2+coin])
						self.set_monster_strength(pos[0],pos[1],depth)
					
					elif monster_type == 'rowdy':
						pos = self.find_any(on_tile)
						coin = random.randint(0,1)
						self.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['elfish_special'][4+coin])
						self.set_monster_strength(pos[0],pos[1],depth)
					
					#set monsters personal_id
					self.npcs[pos[1]][pos[0]].personal_id = str(self.npcs[pos[1]][pos[0]].techID)+'_'+str(pos[0])+'_'+str(pos[1])+'_'+str(random.randint(0,9999))
			
	def make_containers(self, min_no, max_no, on_tile, item_min, item_max, container_type='remains'):
		
		size = int((max_map_size*max_map_size)/(50*50))
		
		for i in range(0,size):
		
			num_container = random.randint(min_no,max_no)
			
			if num_container > 0:
				
				for z in range (0,num_container):
					
					c_type = container_type
					
					if c_type == 'chest':
						ch = random.randint(0,99)
						if ch < 5:
							c_type = 'fridge'
					
					place = self.find_any(on_tile)
					
					inventory = []
					
					num_items = random.randint(item_min,item_max)##############item_min,item_max
					
					for t in range (0,num_items):
					
						if c_type == 'chest':
							
							coin = random.randint(0,1)
							
							if coin == 0:#add equipmen
								classes = ['sword', 'axe', 'dagger', 'knife', 'helmet', 'armor', 'cuisse', 'shoes', 'wand', 'rune', 'rune staff', 'artefact', 'amulet', 'ring', 'talisman', 'seal ring', 'pickaxe'] #CUIDAO
					
								class_num = random.randint(0,len(classes)-1)
								material = random.randint(0,20)
								plus = random.randint(-3,3)
								state = random.randint(80,100)
								
								curse_chance = random.randint(0,30)
								if curse_chance < material:
									curse = 0
								elif curse_chance == material:
									curse = 2
								else:
									curse = 1
								
								item = item_wear(classes[class_num], material, plus, state, curse, False)
								inventory.append(item)
								
							elif coin == 1:
								items = []
								
								for i in range(14,21):
									items.append(il.ilist['misc'][i])
								for i in range(22,40):
									items.append(il.ilist['misc'][i])
								for i in range(44,47):
									items.append(il.ilist['misc'][i])
								
								for j in range(6,9):
									items.append(il.ilist['food'][j])	
								for j in range(13,25):
									items.append(il.ilist['food'][j])
								for j in range(29,32):
									items.append(il.ilist['food'][j])
									
								ran = random.randint(0,len(items)-1)
								inventory.append(deepcopy(items[ran]))
									
						elif c_type == 'remains':
						
							classes = ['sword', 'axe', 'dagger', 'knife', 'helmet', 'armor', 'cuisse', 'shoes', 'wand', 'rune', 'rune staff', 'artefact', 'amulet', 'ring', 'talisman', 'seal ring', 'pickaxe'] #CUIDAO
						
							class_num = random.randint(0,len(classes)-1)
							material = random.randint(0,20)
							plus = random.randint(-3,3)
							state = random.randint(20,60)
					
							curses = (0,1,2)
							curse_num = random.randint(0,2) 
					
							item = item_wear(classes[class_num], material, plus, state, curses[curse_num], False)
							inventory.append(item)
						
						elif c_type == 'fridge':
							ran = random.randint(0,len(il.ilist['food'])-1)
							inventory.append(deepcopy(il.ilist['food'][ran]))
					
					if c_type == 'chest':
						self.add_container(inventory, place[0], place[1])
						replace = self.tilemap[place[1]][place[0]]
						self.tilemap[place[1]][place[0]] = deepcopy(tl.tlist['functional'][4])#chest
						self.tilemap[place[1]][place[0]].replace = replace
					
					elif c_type == 'remains':
						replace_tile = self.tilemap[place[1]][place[0]]
						self.add_container(inventory, place[0], place[1])
						self.tilemap[place[1]][place[0]] = deepcopy(tl.tlist['functional'][6])#remains
						self.tilemap[place[1]][place[0]].replace = replace_tile
						
					elif c_type == 'fridge':
						replace_tile = self.tilemap[place[1]][place[0]]
						self.add_container(inventory, place[0], place[1])
						self.tilemap[place[1]][place[0]] = deepcopy(tl.tlist['functional'][25])#fridge
						self.tilemap[place[1]][place[0]].replace = replace_tile

	def exchange_when_surrounded(self, tile_check, tile_replace, number_neighbors):
		
		#check all cordinates for their neighbors(including them self) and exchange th tile when the number of neighbors with the same techID => number_neighbors
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				
				count = 0
				
				for yy in range (-1,2):
					for xx in range (-1,2):
						
						try:
							if self.tilemap[y+yy][x+xx].techID == tile_check.techID or self.tilemap[y+yy][x+xx].techID == tile_replace.techID:
								count += 1
						except:
							None
							
				if count >= number_neighbors:
					self.tilemap[y][x] = tile_replace
									
	def sget(self):
		
		string = ''
		
		for c in range (0,max_map_size):
			for d in range (0,max_map_size):
				
				
				if d != player.pos[0] or c != player.pos[1]:
					
					if self.known[c][d] != 0:
						string = string + self.tilemap[c][d].char
					else:
						string += '\033[0;30;40m '
				else:
					string = string + player.char
				
			string = string + '\n'
		
		return string
	
	def spawn_magic_shops(self,num=1):
		if self.name == 'shop_0_0':
			return False
		pos = []
		for i in range(0,num):
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					if self.tilemap[y][x].move_group == 'solid':
						num_soil = 0
						try:
							if self.tilemap[y-1][x].move_group == 'soil':
								num_soil += 1
						except:
							None
						try:
							if self.tilemap[y+1][x].move_group == 'soil':
								num_soil += 1
						except:
							None
						try:	
							if self.tilemap[y][x-1].move_group == 'soil':
								num_soil += 1
						except:
							None
						try:
							if self.tilemap[y][x+1].move_group == 'soil':
								num_soil += 1
						except:
							None
						
						if num_soil > 0:
							pos.append((x,y))
		
			if len(pos) < 1:
				return False
			
			ran = random.randint(0,len(pos)-1)
			replace = deepcopy(self.tilemap[pos[ran][1]][pos[ran][0]])
			self.tilemap[pos[ran][1]][pos[ran][0]] = deepcopy(tl.tlist['shop'][4])
			self.tilemap[pos[ran][1]][pos[ran][0]].replace = replace
		
	def set_sanctuary(self,startx,starty):
		
		for y in range (starty-2, starty+3):
			for x in range (startx-2, startx+3):
				
				self.tilemap[y][x] = deepcopy(tl.tlist['sanctuary'][0])#sanctuary floor
				
				if x == startx-2 or x == startx or x == startx+2: 
					if y == starty-2 or y == starty or y == starty+2:
						
						self.tilemap[y][x] = deepcopy(tl.tlist['sanctuary'][1])#sanctuary pilar
						
		self.tilemap[starty][startx] = deepcopy(tl.tlist['sanctuary'][2])#sanctuary spawn point
		
		self.tilemap[starty-1][startx] = deepcopy(tl.tlist['functional'][20])#divine gift
		self.tilemap[starty-1][startx].replace = tl.tlist['sanctuary'][0]
		self.countdowns.append(countdown('gift_to_workbench',startx,starty-1,1))
		
		material_pick = random.randint(0,10)
		material_axe = random.randint(0,10)
		material_amo = random.randint(0,10)
		amo_classes = ('shoes','cuisse','armor','helmet') #DUBTE
		ran = random.randint(0,3)
		amo_class = amo_classes[ran]
		
		pick = item_wear('pickaxe', material_pick,0) #DUBTE
		axe = item_wear('axe',material_axe,0)
		amo = item_wear(amo_class,material_amo,0)
		ran_tunica = random.randint(0,2)
		
		#original
		self.add_container([pick,axe,amo,il.ilist['misc'][53],il.ilist['misc'][2],il.ilist['misc'][51],il.ilist['clothe'][ran_tunica]],startx,starty-1)
		#/original
		
		# statue demo: 
		#list_t = [pick,axe]
		#for f in range(55,70):
		#	list_t.append(il.ilist['misc'][f])
		#self.add_container(list_t,startx,starty-1)
		
		# build demo: self.add_container([pick,axe,amo,il.ilist['misc'][3],il.ilist['misc'][16],il.ilist['misc'][22],il.ilist['misc'][23],il.ilist['clothe'][ran_tunica]],startx,starty-1)
		
		# cloth demo: self.add_container([il.ilist['clothe'][8],il.ilist['clothe'][1],il.ilist['clothe'][2],il.ilist['clothe'][3],il.ilist['clothe'][4],il.ilist['clothe'][5],il.ilist['clothe'][6],il.ilist['clothe'][7]],startx,starty-1)
		
		# magic demo: self.add_container([pick,axe,amo,il.ilist['misc'][81],il.ilist['misc'][24],il.ilist['misc'][24],il.ilist['misc'][24],il.ilist['clothe'][ran_tunica]],startx,starty-1)
		
		self.tilemap[starty+1][startx] = deepcopy(tl.tlist['functional'][1])#stair down
		
		self.tilemap[starty+1][startx].damage = -1
		self.tilemap[starty+1][startx].damage_mes = 'Your wounds are cured.' #DUBTE
		self.tilemap[starty+1][startx].build_here = False
		self.tilemap[starty+1][startx].move_group = 'holy'
		
class world_class():
	
	def __init__(self,tilelist):
		
		global max_map_size
		
		screen.render_load(0)
		
		name = save_path + os.sep + 'world.data'
		
		self.map_size = 52
		
		self.startx = 4
		self.starty = 3
		
		try:
			
			f = open(name, 'rb')
			temp = p.load(f)
			screen.render_load(1)
			self.maplist = temp.maplist
			self.map_size = temp.map_size
			max_map_size = self.map_size
			self.startx = temp.startx
			self.starty = temp.starty
			
		except:
			screen.render_load(2)
			
			self.maplist = []
		
			for x in range (0,7):
				self.maplist.append({})
				
			screen.render_load(3)
			
			self.startx = 4
			self.starty = 3
			
			screen.render_load(5)
			
			self.elysium_generator()
			self.elfish_generator(0)
			
	def default_map_generator(self, name, tiles, tilelist):	#check if tilelist can be deleted
		
		tilemap = []
		
		for i in range (0,max_map_size):
			tilemap.append([])
		
		a = 0
		
		for b in range (0,max_map_size):
			
			ran_num = random.randint(0,len(tl.tlist[tiles])-1)
			tilemap[a].append(tl.tlist[tiles][ran_num])
			
		b = 0
		
		for a in range (1,max_map_size):
		
			ran_num = random.randint(0,len(tl.tlist[tiles])-1)
			tilemap[a].append(tl.tlist[tiles][ran_num])
			
		for a in range (1,max_map_size):
			for b in range (1,max_map_size):
				
				ran_same = random.randint(0,9)
				
				if ran_same < 5 :
					tilemap[a].append(tilemap[a-1][b])
				elif ran_same < 8:
					tilemap[a].append(tilemap[a][b-1])
				else:
					ran_num = random.randint(0,len(tl.tlist[tiles])-1)
					tilemap[a].append(tl.tlist[tiles][ran_num])
					
		m = maP(name ,tilemap)
		
		return m
		
	def border_generator(self,layer,style='default'):
		
		if style == 'default':
			cave_name = 'local_0_0'
		elif style == 'desert':
			cave_name = 'desert_0_0'
		m = self.default_map_generator(cave_name,'global_caves', tilelist)
		m.map_type = 'border'
		
		m.fill(tl.tlist['functional'][0])#fill with border
		
		self.maplist[layer][cave_name] = m
		
	def grot_generator(self,layer):
		
		screen.render_load(15,1)
		
		cave_name = 'dungeon_0_1'
		m = self.default_map_generator(cave_name,'global_caves', tilelist)
		m.map_type = 'grot'
		m.set_music('grot','grot',True)
		m.build_type = 'None'
		
		m.fill(tl.tlist['global_caves'][3])#fill with hard rock
		m.drunken_walker(int(max_map_size/2),int(max_map_size/2),tl.tlist['misc'][0],(((max_map_size*max_map_size)/100)*40))#set low water
		
		m.set_frame(tl.tlist['functional'][0])
		
		chance_ore = layer*5
		chance_gem = layer*3
		
		screen.render_load(15,10)
			
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
					
				if m.tilemap[y][x].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						
					replace = m.tilemap[y][x].replace
						
					coin = random.randint(0,1)
					percent = random.randint(1,100) 
						
					if coin == 0 and percent <= chance_ore:
						m.tilemap[y][x] = tl.tlist['misc'][4]#set ore here
						m.tilemap[y][x].replace = replace
					elif coin == 1 and percent <= chance_gem:
						m.tilemap[y][x] = tl.tlist['misc'][5]#set gem here
						m.tilemap[y][x].replace = replace
		
		screen.render_load(15,40)
		
		for y in range (0,max_map_size):
				for x in range (0,max_map_size):
					
					if m.tilemap[y][x].techID == tl.tlist['misc'][1].techID:#this is mud
						
						cent = random.randint(0,99)
						
						if cent < 10: #its a chance of 10% that a blue mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][6]
							m.tilemap[y][x].replace = replace
							
							m.containers[y][x] = container([deepcopy(il.ilist['food'][1])])
		
		screen.render_load(15,75)
		
		num_lilys = int(((max_map_size*max_map_size)/100)*3)
		
		for i in range (0,num_lilys):
			pos = m.find_any(tl.tlist['misc'][0])#find low wather
			try:
				coin = random.randint(0,1)
				if coin == 0:
					m.tilemap[pos[1]][pos[0]] = tl.tlist['misc'][10]#set a water lily
				else:
					m.tilemap[pos[1]][pos[0]] = tl.tlist['misc'][14]#set a water lily with blossom
					
			except:
				None
		
		screen.render_load(15,90)
		
		pos = m.find_any(tl.tlist['misc'][0])#find any low water tile
		m.tilemap[pos[1]][pos[0]] = tl.tlist['dungeon'][15]#set stair up
		entrance_x = pos[0]
		entrance_y = pos[1]
		
		for x in range(5,46,5):
			for y in range(5,46,5):
				if m.tilemap[y][x].techID != tl.tlist['global_caves'][3].techID:
					test = random.randint(0,2)
					if test == 0:
						m.make_naga_house(x+random.randint(-2,2),y+random.randint(-2,2))
		
		m.spawn_monsters(11)
		
		for sy in range(entrance_y-5,entrance_y+6):
			for sx in range(entrance_x-5,entrance_x+6):
				try:
					m.npcs[sy][sx] = 0
				except:
					None
		
		if 'naga_rescue' in player.quest_variables:
			if not 'saved_all_nagas' in player.quest_variables:
				for i in range(0,5):
					coin = random.randint(31,32)
					pos = m.find_any(tl.tlist['misc'][0])
					m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][coin])
					m.set_monster_strength(pos[0],pos[1],1)
		
		m.set_monster_view_range(3,5)
		
		screen.render_load(15,99)
							
		self.maplist[layer][cave_name] = m
		
	def elfish_generator(self,layer):
		
		screen.render_load(16,0)
		
		lillya_set = False
		
		map_name = 'fortress_0_0'
		m = self.default_map_generator(map_name,'global_caves', tilelist)
		m.map_type = 'elfish_fortress'
		m.set_music('elfish_fortress','elfish_fortress',True)
		m.no_monster_respawn = True
		m.build_type = 'None'
		
		m.fill(tl.tlist['functional'][0])
		
		ran = random.randint(0,2)
		
		lvl = gra_files.level['elfish_fortress_'+str(ran)]
		
		for y in range(0,50):
			screen.render_load(16,y)
			for x in range(0,50):
				pixel = lvl.get_at((x,y))
				if pixel == (0,114,0,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['local'][0])
				elif pixel == (255,255,255,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['functional'][27])
					m.tilemap[y+1][x+1].replace = deepcopy(tl.tlist['local'][0])
				elif pixel == (0,255,0,255):
					coin = random.randint(0,5)
					if coin == 0:
						m.tilemap[y+1][x+1] = deepcopy(tl.tlist['flower'][random.randint(0,len(tl.tlist['flower'])-1)])
						m.tilemap[y+1][x+1].replace = deepcopy(tl.tlist['local'][0])
					else:
						m.tilemap[y+1][x+1] = deepcopy(tl.tlist['local'][0])
				elif pixel == (185,0,185,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['elfish'][3])
				elif pixel == (255,0,0,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['elfish'][3])
					m.tilemap[y+1][x+1].tile_pos = (7,10)
					m.tilemap[y+1][x+1].move_message = 'You walk through a open door.' #DUBTE
					m.tilemap[y+1][x+1].move_group = 'shop'
					m.tilemap[y+1][x+1].transparency = True
				elif pixel == (0,0,255,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['elfish'][0])
				elif pixel == (194,194,194,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['elfish'][1])
				elif pixel == (150,150,150,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['elfish'][1])
					m.tilemap[y+1][x+1].move_group = 'shop'
				elif pixel == (117,113,97,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['shop'][0])
				elif pixel == (0,237,255,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['functional'][7])
					m.tilemap[y+1][x+1].replace = deepcopy(tl.tlist['shop'][0])
				elif pixel == (115,0,211,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['functional'][22])
					m.tilemap[y+1][x+1].replace = deepcopy(tl.tlist['shop'][0])
				elif pixel == (48,48,48,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['sewer'][3])
					m.tilemap[y+1][x+1].replace = deepcopy(tl.tlist['shop'][0])
				elif pixel == (255,255,0,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['portal'][2])
				elif pixel == (112,57,0,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['elfish'][2])
					coin = random.randint(0,20)
					if coin == 0:
						m.npcs[y+1][x+1] = deepcopy(ml.mlist['elfish_special'][2])
						m.set_monster_strength(x+1,y+1,1)
				elif pixel == (0,115,190,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['misc'][0])
				elif pixel == (0,75,124,255):
					m.tilemap[y+1][x+1] = deepcopy(tl.tlist['misc'][3])
		
		building_count = 8
		
		screen.render_load(16,50)
				
		if building_count < 6:
			return False #return false to make a loop if there are to less buildings inside the map
		
		num_temples = int((float(building_count)/100)*10)
		
		if num_temples == 0:
			num_temples = 1
			
		num_meetingarea = int((float(building_count)/100)*10)
		
		if num_meetingarea == 0:
			num_meetingarea = 1
		
		num_libaries = int((float(building_count)/100)*10)
		
		if num_libaries == 0:
			num_libaries = 1
			
		num_dwellings = building_count-num_temples-num_meetingarea-num_libaries
		
		screen.render_load(16,60)
							
		for i in range(0,num_temples):
			
			pos = m.find_any(tl.tlist['elfish'][0])#find any elfish_floor_indoor
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			size = m.get_quarter_size(pos[0],pos[1])
			
			for y in range(pos[1]-1,pos[1]+size[1]+1):
				for x in range(pos[0]-1,pos[0]+size[0]+1):
					m.tilemap[y][x]= deepcopy(tl.tlist['elfish'][5])
			
			for y in range(pos[1],pos[1]+size[1],2):
				for x in range(pos[0],pos[0]+size[0],2):
					m.tilemap[y][x] = deepcopy(tl.tlist['functional'][22])
					m.tilemap[y][x].replace = deepcopy(tl.tlist['elfish'][0])
					m.tilemap[y][x].civilisation = False
			
			m.tilemap[pos[1]+int(size[1]/2)][pos[0]+int(size[0]/2)] = deepcopy(tl.tlist['functional'][15])#set a altar
			m.tilemap[pos[1]+int(size[1]/2)][pos[0]+int(size[0]/2)].replace = tl.tlist['elfish'][0]
			m.tilemap[pos[1]+int(size[1]/2)][pos[0]+int(size[0]/2)].civilisation = False
			m.npcs[pos[1]+int(size[1]/2)][pos[0]+int(size[0]/2)] = deepcopy(ml.mlist['elfish_special'][3])
			m.set_monster_strength(pos[0]+int(size[0]/2),pos[1]+int(size[1]/2),1,lvl_bonus=5)
			
			m.exchange(tl.tlist['elfish'][4],tl.tlist['elfish'][5])
		
		screen.render_load(16,70)
		
		for i in range(0,num_meetingarea):
			
			pos = m.find_any(tl.tlist['elfish'][0])
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			size = m.get_quarter_size(pos[0],pos[1])
			
			m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['elfish_special'][0]) #set elfish landlord
			m.set_monster_strength(pos[0],pos[1],1,lvl_bonus=5) 
			
			for y in range(pos[1]+2,pos[1]+size[1]-2):
				for x in range(pos[0]+2,pos[0]+size[0]-1,4):
					m.tilemap[y][x] = deepcopy(tl.tlist['functional'][16]) #set table
					m.tilemap[y][x].replace = tl.tlist['elfish'][0]
					m.tilemap[y][x].civilisation = False
					m.npcs[y][x] = 0 #override wrong set drunkards
					
					for xx in range(x-1,x+2):
						if m.tilemap[y][xx].techID == tl.tlist['elfish'][4].techID:
							m.tilemap[y][xx] = deepcopy(tl.tlist['functional'][18])
							m.tilemap[y][xx].replace = tl.tlist['elfish'][0]
							m.tilemap[y][xx].civilisation = False
							coin = random.randint(0,3)
							if coin == 1:
								m.npcs[y][xx] = deepcopy(ml.mlist['elfish_special'][1]) #set elfish drunkard
								m.set_monster_strength(xx,y,1,lvl_bonus=5)
			
					for yy in range(y-1,y+2):
						if m.tilemap[yy][x].techID == tl.tlist['elfish'][4].techID:
							m.tilemap[yy][x] = deepcopy(tl.tlist['functional'][18])
							m.tilemap[yy][x].replace = tl.tlist['elfish'][0]
							m.tilemap[yy][x].civilisation = False
							coin = random.randint(0,3)
							if coin == 1:
								m.npcs[yy][x] = deepcopy(ml.mlist['elfish_special'][1]) #set elfish drunkard
								m.set_monster_strength(x,yy,1,lvl_bonus=5)
			
			m.exchange(tl.tlist['elfish'][4],tl.tlist['elfish'][5])
		
		screen.render_load(16,80)
			
		for i in range(0,num_libaries):
			
			pos = m.find_any(tl.tlist['elfish'][0])
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			size = m.get_quarter_size(pos[0],pos[1])
			
			for y in range(pos[1]+1,pos[1]+size[1]-1,2):
				for x in range(pos[0]+1,pos[0]+size[0]-1,2):
					
					m.tilemap[y][x] = deepcopy(tl.tlist['functional'][19])
					m.tilemap[y][x].civilisation = False
			
			if lillya_set == False:		
				lillya_pos = m.find_any(tl.tlist['functional'][19]) #set lillya
				m.npcs[lillya_pos[1]+1][lillya_pos[0]] = deepcopy(ml.mlist['rescued'][2]) 
				m.set_monster_strength(lillya_pos[0],lillya_pos[1],1)
				lillya_set = True
			
			m.exchange(tl.tlist['elfish'][4],tl.tlist['elfish'][5])
		
		screen.render_load(16,85)
		
		for i in range(0,num_dwellings):
			
			pos = m.find_any(tl.tlist['elfish'][0])
			m.floating(pos[0],pos[1],tl.tlist['elfish'][4],tl.tlist['elfish'][3])#fill this building with elfish_active
			pos = m.find_first(tl.tlist['elfish'][4])
			pos_original = pos
			size = m.get_quarter_size(pos[0],pos[1])
			
			num_beds = 4
			num_furniture = int((size[0]*size[1])/25)
			
			for y in range(pos[1],pos[1]+size[1]):
				for x in range(pos[0],pos[0]+size[0]):
					m.tilemap[y][x] = tl.tlist['elfish'][5]
			
			for y in range(pos[1]+1,pos[1]+size[1]-1):
				for x in range(pos[0]+1,pos[0]+size[0]-1):
					m.tilemap[y][x] = tl.tlist['elfish'][4]
			
			bed_pos = ((pos_original[0]+1,pos_original[1]+1),(pos_original[0]+size[0]-2,pos_original[1]+1),(pos_original[0]+1,pos_original[1]+size[1]-2),(pos_original[0]+size[0]-2,pos_original[1]+size[1]-2))		
			for i in range(0,num_beds):#set beds
				pos = bed_pos[i]
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][8])
				m.tilemap[pos[1]][pos[0]].replace = deepcopy(tl.tlist['building'][9])
				m.tilemap[pos[1]][pos[0]].civilisation = False
				m.tilemap[pos[1]][pos[0]].replace.civilisation = False
				coin = random.randint(0,1)
				m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['elfish_fortress'][coin])
				m.set_monster_strength(pos[0],pos[1],6)
				
			
			for i in range(0,num_furniture):#set furnaces
				pos = m.find_any(tl.tlist['elfish'][4])
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][14])
				m.tilemap[pos[1]][pos[0]].replace = deepcopy(tl.tlist['building'][9])
				m.tilemap[pos[1]][pos[0]].civilisation = False
				m.tilemap[pos[1]][pos[0]].replace.civilisation = False
				
			for i in range(0,num_furniture):#set wb's
				pos = m.find_any(tl.tlist['elfish'][4])
				ran = random.randint(9,13)
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][ran])
				m.tilemap[pos[1]][pos[0]].replace = deepcopy(tl.tlist['building'][9])
				m.tilemap[pos[1]][pos[0]].civilisation = False
				m.tilemap[pos[1]][pos[0]].replace.civilisation = False
				
			for y in range(pos_original[1]+1,pos_original[1]+size[1]-1):#set blue floor
				for x in range(pos_original[0]+1,pos_original[0]+size[0]-1):
					if m.tilemap[y][x].techID == tl.tlist['elfish'][4].techID:
						 m.tilemap[y][x] = deepcopy(tl.tlist['building'][9])
						 m.tilemap[y][x].civilisation = False
		
		screen.render_load(16,90)
		 
		m.exchange(tl.tlist['elfish'][5],tl.tlist['elfish'][0])
		
		#set sewer entrance
		pos_sewer = m.find_any(tl.tlist['sewer'][3])
		m.npcs[pos_sewer[1]+1][pos_sewer[0]] = deepcopy(ml.mlist['special'][19])
		m.set_monster_strength(pos_sewer[0],pos_sewer[1]+1,1)
		
		#set merchant
		pos_merchant = m.find_any(tl.tlist['shop'][0])
		m.npcs[pos_merchant[1]][pos_merchant[0]] = deepcopy(ml.mlist['shop'][0])
		m.set_monster_strength(pos_merchant[0],pos_merchant[1],1)
		
		screen.render_load(16,95)
		
		m.make_special_monsters(5,10,tl.tlist['elfish'][1],6,'rowdy')
		
		screen.render_load(16,97)
		
		self.maplist[layer][map_name] = m
		
		screen.render_load(16,99)
		
	def mine_generator(self,layer):
		
		screen.render_load(17,1)
		
		cave_name = 'dungeon_0_1'
		m = self.default_map_generator(cave_name,'global_caves', tilelist)
		m.map_type = 'orcish_mines'
		m.set_music('orcish_mines','orcish_mines',True)
		m.build_type = 'None'
		m.monster_plus = 3
		
		screen.render_load(17,10)
		
		m.fill(tl.tlist['mine'][1])#fill with mine wall
		screen.render_load(17,30)
		m.drunken_walker(int(max_map_size/2),int(max_map_size/2),tl.tlist['mine'][0],((max_map_size**2/100)*45))
		screen.render_load(17,50)
		
		screen.render_load(17,60)
		
		m.exchange_when_surrounded(tl.tlist['mine'][1],tl.tlist['global_caves'][3],8) #only the outer tiles become mine wall
		
		screen.render_load(17,70)
		
		for y in range (0, max_map_size):
			for x in range(0,max_map_size):
				 
				if m.tilemap[y][x].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
				 
					ran = random.randint(0,99)
					 
					if ran > 69:
						 m.tilemap[y][x] = tl.tlist['misc'][4]#set ore
						 m.tilemap[y][x].replace = tl.tlist['global_caves'][0]
					elif ran < 10:
						m.tilemap[y][x] = tl.tlist['misc'][5]#set gem
						m.tilemap[y][x].replace = tl.tlist['global_caves'][0]
					
		num_evo_stone = random.randint(1,3)
		for i in range(0,num_evo_stone):
			pos = m.find_any(tl.tlist['mine'][1])
			m.tilemap[pos[1]][pos[0]] = tl.tlist['misc'][36]#set evolution stone in rock
			m.tilemap[pos[1]][pos[0]].replace = tl.tlist['global_caves'][0]
		
		screen.render_load(17,80)
		
		m.set_frame(tl.tlist['functional'][0])
		
		m.make_containers(15,30,tl.tlist['mine'][0],1,4,'remains')
		
		num_moss = int(((max_map_size*max_map_size)/100)*3)
		
		for i in range (0,num_moss):
			pos = m.find_any(tl.tlist['mine'][0])#find mine floor
			try:
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['mine'][2])#set blood moss
				m.tilemap[pos[1]][pos[0]].replace = deepcopy(tl.tlist['mine'][0])
			except:
				None
		
		screen.render_load(17,90)
		
		pos = m.find_any(tl.tlist['mine'][0])#find any mine floor tile
		m.tilemap[pos[1]][pos[0]] = tl.tlist['dungeon'][17]#set stair up
		entrance_x = pos[0]
		entrance_y = pos[1]
		
		m.spawn_monsters(0)
		
		for sy in range(entrance_y-5,entrance_y+6):
			for sx in range(entrance_x-5,entrance_x+6):
				try:
					m.npcs[sy][sx] = 0
				except:
					None
		
		m.set_monster_view_range(3,5)
		
		screen.render_load(17,99)
							
		self.maplist[layer][cave_name] = m
		
	def sewer_generator(self,layer):
		
		screen.render_load(17,1)
		
		cave_name = 'dungeon_0_1'
		m = self.default_map_generator(cave_name,'global_caves', tilelist)
		m.map_type = 'sewer'
		m.set_music('sewer','sewer',True)
		m.build_type = 'None'
		m.monster_plus = 0
		
		screen.render_load(19,10)
		
		m.fill(tl.tlist['sewer'][1])#fill with sewer wall
		screen.render_load(19,30)
		run = True
		x = 5+random.randint(0,2)
		
		while run:
			for yy in range (5,max_map_size-5):
				m.tilemap[yy][x] = deepcopy(tl.tlist['sewer'][2])
			x += random.randint(4,12)
			if x > max_map_size-5:
				run = False
		
		run = True
		y = 5+random.randint(0,2)
		
		while run:
			for xx in range (5,max_map_size-5):
				m.tilemap[y][xx] = deepcopy(tl.tlist['sewer'][2])
			y += random.randint(4,12)
			if y > max_map_size-5:
				run = False	
		screen.render_load(19,50)
				
		m.exchange_when_surrounded(tl.tlist['sewer'][1],tl.tlist['sewer'][0],8) #only the outer tiles become mine wall
		
		screen.render_load(19,70)
		
		for yyy in range(0,max_map_size):
			for xxx in range(0,max_map_size):
					
				if m.tilemap[yyy][xxx].techID == tl.tlist['sewer'][0].techID:		#Randomize wall design
					m.tilemap[yyy][xxx] = deepcopy(tl.tlist['sewer'][0])			#
					ran_test = random.randint(0,99)									#
					if ran_test > 75:												#
							ran = random.randint(0,2)								#
							m.tilemap[yyy][xxx].tile_pos = (11,0+ran)				#
		
		screen.render_load(19,80)
		
		m.set_frame(tl.tlist['functional'][0])
		
		screen.render_load(19,90)
		
		pos = m.find_any(tl.tlist['sewer'][1])#find any sewer floor tile
		m.tilemap[pos[1]][pos[0]] = tl.tlist['sewer'][4]#set ladder up
		entrance_x = pos[0]
		entrance_y = pos[1]
		
		for y in range(0,max_map_size): #set bitter moss
			for x in range(0,max_map_size):
				if m.tilemap[y][x].techID == tl.tlist['sewer'][1].techID: #this is sewer floor
					ran = random.randint(0,99)
					if ran < 3:
						m.tilemap[y][x] = deepcopy(tl.tlist['sewer'][6])
						m.tilemap[y][x].replace = deepcopy(tl.tlist['sewer'][1])
		
		m.spawn_monsters(5)
		
		for sy in range(entrance_y-5,entrance_y+6):
			for sx in range(entrance_x-5,entrance_x+6):
				try:
					m.npcs[sy][sx] = 0
				except:
					None
		
		m.make_special_monsters(10,15,tl.tlist['sewer'][2],5,'drowner')#set some drowners
		
		if 'find_albino_rat' in player.quest_variables:
			pos = m.find_any(tl.tlist['sewer'][1])#find any sewer floor tile
			if 'killed_albino_rat' in player.quest_variables:
				m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][20])#elfish worker 2
			else:
				m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['special'][16])#albino rat
			m.set_monster_strength(pos[0],pos[1],7)
			if player.difficulty == 4:
				m.npcs[pos[1]][pos[0]].AI_style = 'ignore'
		
		screen.render_load(19,99)
							
		self.maplist[layer][cave_name] = m
		
	def cave_generator(self, deep, style='default'):
		
		if style == 'desert':
			cave_name='desert_0_0'
		else:	
			cave_name = 'local_0_0'
		
		p = 9
				
		for d in range(1,deep+2):
			
			screen.render_load(4,p+(d*20))
			
			m = self.default_map_generator(cave_name,'global_caves', tilelist)
			
			if d < 2:
				if style == 'desert':
					m.map_type = 'desert_cave'
					m.monster_plus = 7
				else:
					m.map_type = 'cave'
				m.set_music('cave','cave',True)
			else:
				if style == 'desert':
					m.map_type = 'desert_lava_cave'
					m.monster_plus = 7
				else:
					m.map_type = 'lava_cave'
				m.set_music('lava_cave','lava_cave',True)
				m.thirst_multi_day = 2
				m.thirst_multi_night = 2
			
			if d > 1:
				m.exchange(tl.tlist['global_caves'][4],tl.tlist['misc'][2])#exchange lava against hot cave ground
				m.exchange(tl.tlist['global_caves'][1],tl.tlist['misc'][28])#exchange worn rock against obsidian
				if d > 1:
					m.exchange_when_surrounded(tl.tlist['misc'][2],tl.tlist['global_caves'][4],8)#make lava spots between hot cave ground
					num = int((max_map_size*max_map_size)/(50*50))
					for i in range(0,num):
						ran = random.randint(0,1)
						if ran > 0:
							pos = m.find_any(tl.tlist['global_caves'][0]) #cave ground
							m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['functional'][23])# make master forges
			else:
				m.exchange(tl.tlist['global_caves'][4],tl.tlist['misc'][1])#exchange lava against mud
				m.exchange_when_surrounded(tl.tlist['misc'][1],tl.tlist['misc'][0],8)#make low water spots between mud
				
			#######set mushrooms, ore and gems
		
			chance_ore = d*6
			chance_gem = d
			
			for y in range (0,max_map_size):
				for x in range (0,max_map_size):
					
					if m.tilemap[y][x].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						
						replace = m.tilemap[y][x].replace
						
						coin = random.randint(0,1)
						percent = random.randint(1,100) 
						
						if coin == 0 and percent <= chance_ore:
							m.tilemap[y][x] = tl.tlist['misc'][4]#set ore here
							m.tilemap[y][x].replace = replace
						elif coin == 1 and percent <= chance_gem:
							m.tilemap[y][x] = tl.tlist['misc'][5]#set gem here
							m.tilemap[y][x].replace = replace
							
					if m.tilemap[y][x].techID == tl.tlist['misc'][1].techID:#this is mud
						
						cent = random.randint(0,99)
						
						if cent < 10: #its a chance of 10% that a blue mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][6]
							m.tilemap[y][x].replace = replace
					
					if m.tilemap[y][x].techID == tl.tlist['global_caves'][0].techID:#this is cave ground
						
						cent = random.randint(0,99)
						
						if cent < 10 and d < 2: #its a chance of 10% that a brown mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][7]
							m.tilemap[y][x].replace = replace
							
						elif cent < 15 and d < 2: #its a chance of 5% that a purple mushroom spawns here
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][8]
							m.tilemap[y][x].replace = replace
						
						elif cent < 10 and d > 1: #10% chance to spawn fire leaves in deep underground
							
							replace = m.tilemap[y][x]
							m.tilemap[y][x] = tl.tlist['misc'][27]
							m.tilemap[y][x].replace = replace
			
			m.set_frame(tl.tlist['functional'][0])
			
			if d == 1 and style == 'default':#set stair up on lvl 1
				pos = (int(max_map_size/2),int(max_map_size/2))
				m.tilemap[pos[1]+1][pos[0]] = deepcopy(tl.tlist['functional'][2])#stair down
				m.tilemap[pos[1]+1][pos[0]].damage = -1
				m.tilemap[pos[1]+1][pos[0]].damage_mes = 'Your wounds are cured.' #DUBTE
				m.tilemap[pos[1]+1][pos[0]].build_here = False
				for yy in range(pos[1]-3,pos[1]+4):
					for xx in range(pos[0]-3,pos[0]+4):
						m.tilemap[yy][xx].no_spawn = True
				
				for x in range(0,max_map_size):
					if m.tilemap[x][pos[0]].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						ran = random.randint(1,2)
						m.tilemap[x][pos[0]] = deepcopy(tl.tlist['global_caves'][ran])
						
				for y in range(0,max_map_size):
					if m.tilemap[pos[1]+1][y].techID == tl.tlist['global_caves'][3].techID:#this is hard rock
						ran = random.randint(1,2)
						m.tilemap[pos[1]+1][y] = deepcopy(tl.tlist['global_caves'][ran])
			
			#set vaults
			if style != 'desert' or d !=2:
				for i in range(0,int(max_map_size**2/50**2)):
					m.make_vault(tl.tlist['global_caves'][0],d)
			
			#set grot/mine at lvl 1
			if style == 'desert':
				if d == 1:
					ran_pos = m.find_any(tl.tlist['global_caves'][0])
					m.tilemap[ran_pos[1]][ran_pos[0]] = tl.tlist['dungeon'][14]
					ran_pos2 = m.find_any(tl.tlist['global_caves'][0])
					m.npcs[ran_pos2[1]][ran_pos2[0]] = deepcopy(ml.mlist['special'][33])
					m.set_monster_strength(ran_pos2[0],ran_pos2[1],1)
					m.npcs[ran_pos2[1]][ran_pos2[0]].lp = 999
					
				if  d == 2:
					x_square = 1+(9*random.randint(0,4))
					y_square = 1+(9*random.randint(0,4))
					m.make_dwarf_bastion(x_square,y_square)
			
			if style == 'default':
				if d == 1:
					ran_pos = m.find_any(tl.tlist['global_caves'][0])
					m.tilemap[ran_pos[1]][ran_pos[0]] = tl.tlist['dungeon'][16]
					ran_pos2 = m.find_any(tl.tlist['global_caves'][0])
					m.npcs[ran_pos2[1]][ran_pos2[0]] = deepcopy(ml.mlist['special'][21])
					m.set_monster_strength(ran_pos2[0],ran_pos2[1],1)
					m.npcs[ran_pos2[1]][ran_pos2[0]].lp = 999
					
					ran_pos3 = m.find_any(tl.tlist['global_caves'][0])
					m.npcs[ran_pos3[1]][ran_pos3[0]] = deepcopy(ml.mlist['special'][34])
					m.set_monster_strength(ran_pos3[0],ran_pos3[1],1)
					m.npcs[ran_pos3[1]][ran_pos3[0]].lp = 999
				
			m.make_containers(1,2,tl.tlist['global_caves'][0],2,5,'chest')#set some chests
			m.make_special_monsters(0,1,tl.tlist['global_caves'][0],d,'mimic')#maybe set some mimics
			m.make_special_monsters(15,25,tl.tlist['global_caves'][0],d,'vase')#set some vases
			
			m.spawn_monsters(d)
			
			if style == 'desert': #replace rock etc.
				for y in range(0,max_map_size):
					for x in range(0,max_map_size):
						
						if m.tilemap[y][x].techID == tl.tlist['global_caves'][3].techID: #this is hard rock
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][24])
						elif m.tilemap[y][x].techID == tl.tlist['global_caves'][1].techID: #this is worn rock
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][23])
						elif m.tilemap[y][x].techID == tl.tlist['global_caves'][2].techID: #this is soft soil
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][23])
						elif m.tilemap[y][x].techID == tl.tlist['misc'][4].techID: #this is ore
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][21])
						elif m.tilemap[y][x].techID == tl.tlist['misc'][5].techID: #this is gem
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][22])
						elif m.tilemap[y][x].techID == tl.tlist['misc'][7].techID: #this is a brown mushroom
							replace = m.tilemap[y][x].replace
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][25])
							m.tilemap[y][x].replace = replace
						elif m.tilemap[y][x].techID == tl.tlist['misc'][8].techID: #this is a purple mushroom
							replace = m.tilemap[y][x].replace
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][29])
							m.tilemap[y][x].replace = replace
						elif m.tilemap[y][x].techID == tl.tlist['misc'][6].techID: #this is a blue mushroom
							replace = m.tilemap[y][x].replace
							m.tilemap[y][x] = deepcopy(tl.tlist['misc'][26])
							m.tilemap[y][x].replace = replace
							
			self.maplist[d][cave_name] = m
	
	def elysium_generator(self):
		
		screen.render_load(22,0)
		name = 'elysium_0_0'
		
		tilemap = []
		for a in range (0,max_map_size):
			tilemap.append([])
			for b in range (0,max_map_size):
				tilemap[a].append(0)
				
		m = maP(name,tilemap)
		m.map_type = 'elysium'
		m.set_music('elysium','night',True)
		m.build_type = 'None'
		
		m.fill(tl.tlist['sanctuary'][0])
		
		for x in range(0,max_map_size):
			for y in range(0,max_map_size):
				if x%2 == 0 and y%2 == 0:
					m.tilemap[y][x] = deepcopy(tl.tlist['sanctuary'][1])
				elif x%2 != 0 and y%2 != 0:
					m.tilemap[y][x] = deepcopy(tl.tlist['sanctuary'][1])
		
		screen.render_load(22,10)
		
		center = int(max_map_size/2)
		
		for yy in range(center-2,center+3):
			for xx in range(center-2,center+3):
				m.tilemap[yy][xx] = deepcopy(tl.tlist['sanctuary'][0])
				
		m.tilemap[center][center] = deepcopy(tl.tlist['sanctuary'][2])
		
		for yyy in range(center-7,center-3):
			for xxx in range(center-2,center+3):
				m.tilemap[yyy][xxx] = deepcopy(tl.tlist['sanctuary'][0])
				
		for yyy in range(center-2,center+3):
			for xxx in range(center-7,center-3):
				m.tilemap[yyy][xxx] = deepcopy(tl.tlist['sanctuary'][0])
				
		for yyy in range(center-2,center+3):
			for xxx in range(center+4,center+8):
				m.tilemap[yyy][xxx] = deepcopy(tl.tlist['sanctuary'][0])
		
		for yyy in range(center+4,center+8):
			for xxx in range(center-2,center+3):
				m.tilemap[yyy][xxx] = deepcopy(tl.tlist['sanctuary'][0])
		
		help_map = deepcopy(m)
				
		for yyy in range(0,max_map_size):
			for xxx in range(0,max_map_size):
				if m.tilemap[yyy][xxx].techID == tl.tlist['sanctuary'][0].techID:
					count = 0
					for yyyy in range(yyy-1,yyy+2):
						for xxxx in range(xxx-1,xxx+2):
							try:
								if m.tilemap[yyyy][xxxx].techID == tl.tlist['sanctuary'][1].techID:
									count += 1
							except:
								None
					if count == 4:
						help_map.tilemap[yyy][xxx] = deepcopy(tl.tlist['sanctuary'][1])
						
		m = help_map
		
		screen.render_load(22,30)
		
		 #spawn players room
		for y5 in range(2,6):
			for x5 in range(2,6):
				m.tilemap[y5][x5] = deepcopy(tl.tlist['sanctuary'][0])
				
		for y6 in range(3,5):
			for x6 in range(3,5):
				m.tilemap[y6][x6] = deepcopy(tl.tlist['building'][9])
				
		m.tilemap[3][1] = deepcopy(tl.tlist['sanctuary'][7])
		m.tilemap[3][4] = deepcopy(tl.tlist['functional'][8])
		m.tilemap[3][4].replace = deepcopy(tl.tlist['building'][9])
		m.tilemap[4][4] = deepcopy(tl.tlist['functional'][4])
		m.tilemap[4][4].replace = deepcopy(tl.tlist['building'][9])
		m.containers[4][4] = container([item_wear('axe',0,0,known=True),item_wear('pickaxe',0,0,known=True),item_wear('knife',0,0,known=True),item_wear('wand',0,0,known=True),il.ilist['clothe'][random.randint(0,2)]]) #DUBTE
		m.tilemap[center-6][center+4] = deepcopy(tl.tlist['sanctuary'][6])
		m.npcs[3][2] = deepcopy(ml.mlist['seraph'][8])
		m.set_monster_strength(2,3,1)
		
		m.tilemap[center][center-1] = deepcopy(tl.tlist['sanctuary'][3])
		m.tilemap[center][center+1] = deepcopy(tl.tlist['sanctuary'][3])
		m.tilemap[center][center-5] = deepcopy(tl.tlist['sanctuary'][3])
		m.tilemap[center][center+5] = deepcopy(tl.tlist['sanctuary'][3])
		m.tilemap[center][center-1] = deepcopy(tl.tlist['sanctuary'][3])
		m.tilemap[center-5][center] = deepcopy(tl.tlist['sanctuary'][3])
		m.tilemap[center-7][center] = deepcopy(tl.tlist['portal'][6])
		m.tilemap[center-8][center+1] = deepcopy(tl.tlist['portal'][0])
		m.tilemap[center-8][center-1] = deepcopy(tl.tlist['portal'][3])
		
		screen.render_load(22,50)
		
		#set nest boxes
		m.tilemap[23][30] = deepcopy(tl.tlist['sanctuary'][4])
		m.tilemap[23][30].replace = deepcopy(tl.tlist['sanctuary'][0])
		
		m.tilemap[23][32] = deepcopy(tl.tlist['sanctuary'][4])
		m.tilemap[23][32].replace = deepcopy(tl.tlist['sanctuary'][0])
		
		m.tilemap[25][34] = deepcopy(tl.tlist['sanctuary'][4])
		m.tilemap[25][34].replace = deepcopy(tl.tlist['sanctuary'][0])
		
		m.tilemap[27][34] = deepcopy(tl.tlist['sanctuary'][4])
		m.tilemap[27][34].replace = deepcopy(tl.tlist['sanctuary'][0])
		
		m.tilemap[29][32] = deepcopy(tl.tlist['sanctuary'][4])
		m.tilemap[29][32].replace = deepcopy(tl.tlist['sanctuary'][0])
		
		m.tilemap[29][30] = deepcopy(tl.tlist['sanctuary'][4])
		m.tilemap[29][30].replace = deepcopy(tl.tlist['sanctuary'][0])
		
		screen.render_load(22,60)
		
		#set tutorial npcs
		m.npcs[center-3][center-6] = deepcopy(ml.mlist['seraph'][0])
		m.set_monster_strength(center-6,center-3,1)
		m.npcs[center-3][center-6].lp = 999
		
		m.npcs[center][center+6] = deepcopy(ml.mlist['seraph'][1])
		m.set_monster_strength(center+6,center,1)
		m.npcs[center][center+6].lp = 999
		
		m.npcs[center+4][center-3] = deepcopy(ml.mlist['seraph'][2])
		m.set_monster_strength(center-3,center+4,1)
		m.npcs[center+4][center-3].lp = 999
		
		m.npcs[center+4][center+3] = deepcopy(ml.mlist['seraph'][3])
		m.set_monster_strength(center+3,center+4,1)
		m.npcs[center+4][center+3].lp = 999
		
		m.npcs[center-3][center-4] = deepcopy(ml.mlist['seraph'][4])
		m.set_monster_strength(center-4,center-3,1)
		m.npcs[center-3][center-4].lp = 999
		
		m.npcs[center+8][center+1] = deepcopy(ml.mlist['seraph'][5])
		m.set_monster_strength(center+1,center+8,1)
		m.npcs[center+8][center+1].lp = 999
		
		m.npcs[center-6][center] = deepcopy(ml.mlist['seraph'][6])
		m.set_monster_strength(center,center-6,1)
		m.npcs[center-6][center].lp = 999
		
		m.npcs[center+6][center+3] = deepcopy(ml.mlist['seraph'][7])
		m.set_monster_strength(center+3,center+6,1)
		m.npcs[center+6][center+3].lp = 999
		
		screen.render_load(22,80)
		
		m.tilemap[center+8][center-1] = deepcopy(tl.tlist['functional'][9])		#carpenters workbench
		m.tilemap[center+8][center-1].replace = tl.tlist['sanctuary'][0]		#
		
		m.tilemap[center+6][center] = deepcopy(tl.tlist['functional'][16])		#table
		m.tilemap[center+6][center].special_group = 'None'						#
		m.tilemap[center+6][center].replace = tl.tlist['sanctuary'][0]			#
		
		m.tilemap[center+5][center] = deepcopy(tl.tlist['functional'][18])		#stone seat
		m.tilemap[center+5][center].use_group = 'None'							#
		m.tilemap[center+5][center].replace = tl.tlist['sanctuary'][0]			#
		
		m.tilemap[center+7][center] = deepcopy(tl.tlist['functional'][18])		#stone seat
		m.tilemap[center+7][center].use_group = 'None'							#
		m.tilemap[center+7][center].replace = tl.tlist['sanctuary'][0]			#
		
		m.tilemap[center+6][center+1] = deepcopy(tl.tlist['functional'][18])		#stone seat
		m.tilemap[center+6][center+1].use_group = 'None'							#
		m.tilemap[center+6][center+1].replace = tl.tlist['sanctuary'][0]			#
		
		m.tilemap[center+6][center-1] = deepcopy(tl.tlist['functional'][18])		#stone seat
		m.tilemap[center+6][center-1].use_group = 'None'							#
		m.tilemap[center+6][center-1].replace = tl.tlist['sanctuary'][0]			#
		
		screen.render_load(22,99)
		
		self.maplist[0][name] = m
								
	def grassland_generator(self,x,y,chance_scrubs, chance_trees, chance_herbs, number_rocks):
		# chance_scrubs and chance_trees must be between 0 and 99
		
		screen.render_load(3,1)
		name = 'local_0_0'
		
		helpmap = self.default_map_generator('1','help',tilelist)
		
		tilemap = []
		for a in range (0,max_map_size):
			tilemap.append([])
			for b in range (0,max_map_size):
				tilemap[a].append(0)
	
		m = maP(name,tilemap)
		m.map_type = 'overworld'
		m.set_music('overworld','night',True)
		
		screen.render_load(3,2)
		
		m.fill(tl.tlist['local'][0])#fill the map with grass
				
		# set scrubs
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][0].techID: #<---scrub here
					chance = random.randint(0,99)
					if chance < chance_scrubs:
						scrubs = (1,3,4,6,7,8,9)
						coin = random.randint(0,len(scrubs)-1)
						m.tilemap[y][x] = deepcopy(tl.tlist['local'][scrubs[coin]])
						m.tilemap[y][x].replace = deepcopy(tl.tlist['local'][0])
						
		screen.render_load(3,3)
							
		#set trees
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][1].techID: #<---tree here
					chance = random.randint(0,99)
					if chance < chance_trees:
						coin = random.randint(10,13)
						m.tilemap[y][x] = deepcopy(tl.tlist['local'][coin])
						m.tilemap[y][x].replace = deepcopy(tl.tlist['local'][0])#grass
		
		screen.render_load(3,4)
		
		#set herbs
		
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][0].techID: #<---scrub here
					chance = random.randint(0,99)
					if chance < chance_herbs:
						coin = random.randint(15,16)
						m.tilemap[y][x] = deepcopy(tl.tlist['local'][coin])
						m.tilemap[y][x].replace = deepcopy(tl.tlist['local'][0])#grass
		
		screen.render_load(3,5)
			
		# set rocks
		
		for n in range (0,number_rocks):
			x = random.randint(0,max_map_size-1)
			y = random.randint(0,max_map_size-1)
			m.tilemap[y][x] = deepcopy(tl.tlist['local'][14])
			m.tilemap[y][x].replace = deepcopy(tl.tlist['local'][0])#grass
		
		screen.render_load(3,6)
		
		#set water
			
		for y in range (0,max_map_size):
			for x in range (0,max_map_size):
				if helpmap.tilemap[y][x].techID == tl.tlist['help'][2].techID: #<---water here
					m.tilemap[y][x] = deepcopy(tl.tlist['misc'][0]) # set low water here
		
		screen.render_load(3,7)
					
		m.exchange_when_surrounded(tl.tlist['misc'][0],tl.tlist['misc'][3],8) # exchange low wather against deep water
		
		pos = (int(max_map_size/2),int(max_map_size/2))
		
		#set elfish hall
		m.make_elfish_hall(pos[0]-4,pos[1]-4)
		
		#set stair down
		m.tilemap[pos[1]+1][pos[0]] = deepcopy(tl.tlist['functional'][1])
		m.tilemap[pos[1]+1][pos[0]].move_group = 'house'
		
		m.set_frame(tl.tlist['functional'][0])
		
		screen.render_load(3,8)
		
		#set dungeon
		ran_pos = m.find_any(tl.tlist['local'][0])
		m.tilemap[ran_pos[1]][ran_pos[0]] = deepcopy(tl.tlist['dungeon'][7])
		
		for q in range(0,int(max_map_size**2/50**2)*3):
			m.make_orc_cave(tl.tlist['local'][0])#generate orc caves on grass
			
		m.spawn_monsters(0)
		
		#set hammer dryad
		hammer_pos = m.find_any(tl.tlist['local'][0])
		m.npcs[hammer_pos[1]][hammer_pos[0]] = deepcopy(ml.mlist['special'][26])
		m.set_monster_strength(hammer_pos[0],hammer_pos[1],0)
					
		self.maplist[0][name] = m
		
		screen.render_load(3,9)
		
		return pos
	
	def shop_generator(self,style):
		
		#0: Basic initializing
		
		screen.render_load(19,0)
		
		name = 'shop_0_0'
		
		tilemap = []
		for a in range (0,max_map_size):
			tilemap.append([])
			for b in range (0,max_map_size):
				tilemap[a].append(0)
		m = maP(name,tilemap)
		m.map_type = style
		m.build_type = 'None'
		m.monster_plus = 0
		m.monster_num = 0
		
		m.set_music('shop','shop',True)
		
		m.fill(tl.tlist['functional'][0])
		
		screen.render_load(19,10)
		
		center_x = int(max_map_size/2)
		center_y = int(max_map_size/2)
		
		for y in range(center_y-4,center_y+5):
			for x in range(center_x-4,center_x+5):
				m.tilemap[y][x] = deepcopy(tl.tlist['shop'][1])#wall
		
		screen.render_load(19,20)
		
		for y in range(center_y-3,center_y+4):
			for x in range(center_x-3,center_x+4):
				m.tilemap[y][x] = deepcopy(tl.tlist['dungeon'][1])#corridor
		
		screen.render_load(19,30)
				
		for y in range(center_y-2,center_y+3):
			for x in range(center_x-2,center_x+3):
				m.tilemap[y][x] = deepcopy(tl.tlist['shop'][1])#shop wall
		
		screen.render_load(19,50)
		
		for y in range(center_y-1,center_y+2):
			for x in range(center_x-1,center_x+2):
				m.tilemap[y][x] = deepcopy(tl.tlist['shop'][0])#shop floor
		
		screen.render_load(19,70)
				
		m.tilemap[center_y-2][center_x] = deepcopy(tl.tlist['shop'][2])#shop door
		m.tilemap[center_y-3][center_x-1] = deepcopy(tl.tlist['shop'][5])#sign
		m.tilemap[center_y-3][center_x-1].replace = deepcopy(tl.tlist['dungeon'][1])
		m.tilemap[center_y-3][center_x].techID = -9999#nothing shall spawn here
		m.tilemap[center_y-4][center_x] = deepcopy(tl.tlist['shop'][3])#shop exit
		
		if style == 'pharmacy':
			m.tilemap[center_y-3][center_x-1].move_mes = '[Naeria\'s Pharmacy]' #DUBTE
			m.npcs[center_y][center_x] = deepcopy(ml.mlist['shop'][3])
		elif style == 'pickaxe':
			m.tilemap[center_y-3][center_x-1].move_mes = '[Eklor\'s Pickaxe Empire]'
			m.npcs[center_y][center_x] = deepcopy(ml.mlist['shop'][4])
		elif style == 'hardware':
			m.tilemap[center_y-3][center_x-1].move_mes = '[Grimork\'s Hardware Store]'
			m.npcs[center_y][center_x] = deepcopy(ml.mlist['shop'][5])
		elif style == 'deco':
			m.tilemap[center_y-3][center_x-1].move_mes = '[Larosa\'s Decoration Store]'
			m.npcs[center_y][center_x] = deepcopy(ml.mlist['shop'][6])
		elif style == 'book':
			m.tilemap[center_y-3][center_x-1].move_mes = '[Xirazzzia\'s Bookshelf]'
			m.npcs[center_y][center_x] = deepcopy(ml.mlist['shop'][7])
		elif style == 'bomb':
			m.tilemap[center_y-3][center_x-1].move_mes = '[Torguly\'s eXplozives Of al kinD]'
			m.npcs[center_y][center_x] = deepcopy(ml.mlist['shop'][8])
		elif style == 'general':
			m.tilemap[center_y-3][center_x-1].move_mes = '[Arialu\'s General Store]'
			m.npcs[center_y][center_x] = deepcopy(ml.mlist['shop'][9])
				
		screen.render_load(19,90)
		
		coin = random.randint(0,1)
		if coin == 1:
			pos = m.find_any(tl.tlist['dungeon'][1])
			coin2 = random.randint(0,3)
			if coin2 == 0:
				replace = m.tilemap[pos[1]][pos[0]]
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['misc'][9])
				m.tilemap[pos[1]][pos[0]].replace = replace
			elif coin2 == 1:
				replace = m.tilemap[pos[1]][pos[0]]
				m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['misc'][11])
				m.tilemap[pos[1]][pos[0]].replace = replace
			elif coin2 == 2:
				m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['cave'][2])
				m.set_monster_strength(pos[0],pos[1],1)
			else:
				m.make_special_monsters(1,2,tl.tlist['dungeon'][1],1,'vase')
				
		
		self.maplist[1][name] = m
		
		screen.render_load(19,99)
	
	def dungeon_generator(self,monster_plus,stair_down=True,num_traps=10,style='Dungeon'):#possible other style = 'Tomb'
		
		#0: Basic initializing
		
		screen.render_load(19,0)#Render progress bar 0%
		
		if player.pet_pos != False and player.pet_on_map != False:
			pet_help = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]])
			world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]] = 0
			player.pet_pos = [0,0,1]
			player.pet_on_map = 'dungeon_0_0'
		
		if style == 'Tomb':								#Set the graphics
			tl.tlist['dungeon'][1].tile_pos = (4,6)		#
			tl.tlist['dungeon'][6].tile_pos = (4,7)		#Sandstone walls,hidden doors and corridors for the acient tomb
			tl.tlist['dungeon'][9].tile_pos = (4,7)		#
		else:											#
			tl.tlist['dungeon'][1].tile_pos = (10,6)	#
			tl.tlist['dungeon'][6].tile_pos = (2,6)		#Default walls,hidden doors and corridors for the default dungeon
			tl.tlist['dungeon'][9].tile_pos = (2,6)		#
		
		name = 'dungeon_0_0'#map name
		
		tilemap = []							#Initializing a empty tilemap
		for a in range (0,max_map_size):		#
			tilemap.append([])					#
			for b in range (0,max_map_size):	#
				tilemap[a].append(0)			#
		
		m = maP(name,tilemap)					 #Generate a Map-object
		if style == 'Tomb':						 #
			m.map_type = 'tomb'					 #
			m.set_music('tomb','tomb',True)		 #
		else:									 #
			m.map_type = 'dungeon'				 #and set a few constants for the new map
			m.set_music('dungeon','dungeon',True)#
		m.build_type = 'None'					 #
		m.monster_plus = monster_plus			 #
		m.monster_num = 0.3						 #
		m.no_monster_respawn = True				 #
		
		m.fill(tl.tlist['dungeon'][9])#fill the map with dungeon wall tiles
		
		screen.render_load(19,10)#Render progress bar 10%
		
		#1: Set rooms
			#Important fact: No matter how big the mapsize is set, 
			#dundeons only use the 52x52 tiles in the upper left connor.
			#Thats as big as a small map.
		test_build = True								#Seperate the dungeon in a 3x3 grit.
		while test_build:								#Every part of the grit has a 66% chance to be a room
			parts_with_rooms = []						#
														#
			for part_y in range(0,3):					#
				for part_x in range(0,3):				#
					ran = random.randint(0,9)			#
					if ran > 3:							#
						pick = (part_x,part_y)			#
						parts_with_rooms.append(pick)	#
			
			if len(parts_with_rooms) > 5:	#every dungeon level needs at least 5 rooms
				test_build = False			#
			
		coord_x = []						#transform the coordinates from the 3x3 grit into
		coord_y = []						#real coordinates on the tilemap(center of the rooms)
											#
		for c in parts_with_rooms:			#
			x_offset = random.randint(0,5)	#
			y_offset = random.randint(0,5)	#
											#
			real_x = 9+(15*c[0])+x_offset	#
			real_y = 9+(15*c[1])+y_offset	#
											#
			coord_x.append(real_x)			#
			coord_y.append(real_y)			#
		
		m.imp_connect(coord_x,coord_y,tl.tlist['dungeon'][1],tl.tlist['dungeon'][0],tl.tlist['dungeon'][0])#connect the room cooardinathe with corridor
			
		for i in range(0,len(coord_x)-1):#set variable roome size for all rooms
			x_minus = random.randint(2,4)#
			x_plus = random.randint(3,5) #
			y_minus = random.randint(2,4)#
			y_plus = random.randint(3,5) #
				
			for yy in range(coord_y[i]-y_minus-1,coord_y[i]+y_plus+1):			#draw walls around the rooms
				for xx in range(coord_x[i]-x_minus-1,coord_x[i]+x_plus+1):		#
					m.tilemap[yy][xx] = deepcopy(tl.tlist['dungeon'][9])		#
																				
			for yy in range(coord_y[i]-y_minus,coord_y[i]+y_plus):				#draw the room floor
				for xx in range(coord_x[i]-x_minus,coord_x[i]+x_plus):			#
					m.tilemap[yy][xx] = tl.tlist['dungeon'][0]					#
		
		screen.render_load(19,25) #progress bar 25%
			
		#2: Set doors			
						
		for yyy in range(0,52):
			for xxx in range(0,52):			#the 52 is hard scripted to safe performance
					
				if m.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][9].techID:										#Set all tiles that are surrounded by two moveable tiles on two opponent sides as doors 
					if m.tilemap[yyy-1][xxx].move_group == 'soil' and m.tilemap[yyy+1][xxx].move_group == 'soil':	#
						m.tilemap[yyy][xxx] = tl.tlist['dungeon'][3]												#
					elif m.tilemap[yyy][xxx-1].move_group == 'soil' and m.tilemap[yyy][xxx+1].move_group == 'soil':	#
						m.tilemap[yyy][xxx] = tl.tlist['dungeon'][3]												#
				
		for yyy in range(0,52):
			for xxx in range(0,52):			#the 52 is hard scripted to safe performance
				
				if m.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][3].techID:		#Remove all doors that are next to another door.
					size = m.get_quarter_size(xxx,yyy)								#Only spare one door per wall
					if size[0] > 1:													#
						for rx in range(xxx,xxx+size[0]+1):							#
							m.tilemap[yyy][rx] = deepcopy(tl.tlist['dungeon'][9])	#
						rrx = int(xxx+((rx-xxx)/2))									#
						m.tilemap[yyy][rrx] = tl.tlist['dungeon'][3]				#
																					#
						if m.tilemap[yyy-1][rrx].move_group != 'soil':				#
							m.tilemap[yyy-1][rrx] = tl.tlist['dungeon'][1]			#
						if m.tilemap[yyy+1][rrx].move_group != 'soil':				#
							m.tilemap[yyy+1][rrx] = tl.tlist['dungeon'][1]			#
																					#
					if size[1] > 1:													#
						for ry in range(yyy,yyy+size[1]+1):							#
							m.tilemap[ry][xxx] = deepcopy(tl.tlist['dungeon'][9])	#
						rry = int(yyy+((ry-yyy)/2))									#
						m.tilemap[rry][xxx] = tl.tlist['dungeon'][3]				#
																					#
						if m.tilemap[rry][xxx-1].move_group != 'soil':				#
							m.tilemap[rry][xxx-1] = tl.tlist['dungeon'][1]			#
						if m.tilemap[rry][xxx+1].move_group != 'soil':				#
							m.tilemap[rry][xxx+1] = tl.tlist['dungeon'][1]			#
		
		screen.render_load(19,40)#Render progress bar 40%
		
		test = deepcopy(m)														#Make a copy of the map as is
		pos = test.find_first(tl.tlist['dungeon'][0])							#and performe a float test,
		test.floating(pos[0],pos[1],tl.tlist['misc'][0],tl.tlist['dungeon'][9])	#in order to find not conected parts.
		
		screen.render_load(19,50) #Render progress bar 50%
		
		for yyy in range(0,52):																														#Remove not connected parts
			for xxx in range(0,52):																													#
				if test.tilemap[yyy][xxx].techID != tl.tlist['dungeon'][9].techID and test.tilemap[yyy][xxx].techID != tl.tlist['misc'][0].techID:	#
					m.tilemap[yyy][xxx] = tl.tlist['dungeon'][9]																					#
		
		screen.render_load(19,60)#Render progress bar c60%
		
		for yyy in range(0,52):														#Randomize doors:
			for xxx in range(0,52):													#-normal door
																					#-resisting door
				if m.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][3].techID:		#-etc.
					ran = random.randint(3,6)										#
					m.tilemap[yyy][xxx] = tl.tlist['dungeon'][ran]					#
					
				if m.tilemap[yyy][xxx].techID == tl.tlist['dungeon'][9].techID:		#Randomize wall design
					ran_test = random.randint(0,99)									#
					if ran_test > 75:												#
						if style == 'Dungeon':										#
							ran = random.randint(0,2)								#
							m.tilemap[yyy][xxx].tile_pos = (11,0+ran)				#
						if style == 'Tomb':											#
							ran = random.randint(0,2)								#
							m.tilemap[yyy][xxx].tile_pos = (12,0+ran)				#
					
		
		screen.render_load(19,70)#Render progress bar 70%
						
		#3: Make stairs
		stair_up_pos = m.find_any(tl.tlist['dungeon'][0])							#Set a up leading stair on any floor tile.
		entrance_x = stair_up_pos[0]												#
		entrance_y = stair_up_pos[1]												#
		if style == 'Tomb':															#
			m.tilemap[stair_up_pos[1]][stair_up_pos[0]] = tl.tlist['dungeon'][19]	#
		else:																		#
			m.tilemap[stair_up_pos[1]][stair_up_pos[0]] = tl.tlist['dungeon'][8]	#
			
		for sy in range(stair_up_pos[1]-4,stair_up_pos[1]+5):
			for sx in range(stair_up_pos[0]-4,stair_up_pos[0]+5):
				try:
					if m.tilemap[sy][sx].move_group == 'soil':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group = 'dry_entrance'
					elif m.tilemap[sy][sx].move_group == 'low_liquid':
						m.tilemap[sy][sx] = deepcopy(m.tilemap[sy][sx])
						m.tilemap[sy][sx].move_group = 'wet_entrance'
				except:
					None
		
		if style != 'Tomb':
			if monster_plus == 5 and 'find_gilmenor' in player.quest_variables and not 'gilmenor_rescued' in player.quest_variables:#set gilmenor
				pos = m.find_any(tl.tlist['dungeon'][0])																			#
				m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['cage'][0])																#
				m.set_monster_strength(pos[0],pos[1],1,lvl_bonus=9)
				poses_kobold = []
				for yy in range(pos[1]-2,pos[1]+3):
					for xx in range(pos[0]-2,pos[0]+3):
						if m.tilemap[yy][xx].techID == tl.tlist['dungeon'][0].techID:
							poses_kobold.append([xx,yy])
				if len(poses_kobold) == 0:
					pos_kobold = None
				elif len(poses_kobold) == 1:
					pos_kobold = poses_kobold[0]
				else:
					pos_kobold = poses_kobold[random.randint(0,len(poses_kobold)-1)]
					
				if pos_kobold != None:
					message.add('You feel an evil presence on this floor.') #TIPO1
					m.npcs[pos_kobold[1]][pos_kobold[0]] = deepcopy(ml.mlist['kobold'][0])																#
					m.set_monster_strength(pos_kobold[0],pos_kobold[1],2,lvl_bonus=1)
					if player.difficulty == 4:
						m.npcs[pos_kobold[1]][pos_kobold[0]].AI_style = 'ignore'
				pos2 = m.find_any(tl.tlist['dungeon'][0])																			#
				m.tilemap[pos2[1]][pos2[0]] = deepcopy(tl.tlist['portal'][9])														#
				m.tilemap[pos2[1]][pos2[0]].replace = deepcopy(tl.tlist['dungeon'][0])
			
		if stair_down == True:																#If we are not on the deepest lvl:
			stair_down_pos = m.find_any(tl.tlist['dungeon'][0])								#Set a down leading stair on any floor tile.
			if style == 'Tomb':																#
				m.tilemap[stair_down_pos[1]][stair_down_pos[0]] = tl.tlist['dungeon'][18]	#
			else:																			#
				m.tilemap[stair_down_pos[1]][stair_down_pos[0]] = tl.tlist['dungeon'][7]	#
		else: 																		#Make a chest whit a reward on the deepest lvl instead
			chest_pos = m.find_any(tl.tlist['dungeon'][0])							#
			m.tilemap[chest_pos[1]][chest_pos[0]] = tl.tlist['dungeon'][20]			#
			m.tilemap[chest_pos[1]][chest_pos[0]].replace = tl.tlist['dungeon'][0]	#
			
			if style == 'Tomb':
				m.add_container([il.ilist['special_clothe'][0],il.ilist['misc'][33],il.ilist['misc'][40]],chest_pos[0],chest_pos[1])# set the interior of the chest
			else:																											#
				m.add_container([il.ilist['special_clothe'][1],il.ilist['misc'][33],il.ilist['misc'][41]],chest_pos[0],chest_pos[1])#
				
			egg_pos = stair_up_pos = m.find_any(tl.tlist['dungeon'][0])				#set monster egg
			m.tilemap[egg_pos[1]][egg_pos[0]] = tl.tlist['functional'][34]			#
			m.tilemap[egg_pos[1]][egg_pos[0]].replace = tl.tlist['dungeon'][0]		#
		
		screen.render_load(19,80)#Render progress bar 80%
		
		#4: Make Traps
		
		for i in range(0,num_traps):										#Set hidden traps on random floor tiles.
			pos = m.find_any(tl.tlist['dungeon'][0])						#
			replace = m.tilemap[pos[1]][pos[0]]								#
			m.tilemap[pos[1]][pos[0]] = deepcopy(tl.tlist['dungeon'][10])	#Traps have to be deepcopied to work proper.
			m.tilemap[pos[1]][pos[0]].replace = replace						#
		
		screen.render_load(19,90) #Render Progress bar 90%
		#5: Make interior
		num_rooms = len(parts_with_rooms)														#Make chests with random loot
		m.make_containers(int(num_rooms/3),int(num_rooms/2),tl.tlist['dungeon'][0],1,3,'chest')	#
		
		for c in range(0,num_rooms):						#Set random fontains on floor tiles
			pos = m.find_any(tl.tlist['dungeon'][0])		#
			ran = random.randint(0,99)						#
			if ran < 15:									#
				tile = deepcopy(tl.tlist['dungeon'][12])	#acid fontain
			elif ran > 84:									#
				tile = deepcopy(tl.tlist['dungeon'][13])	#healing fontain
			else:											#
				tile = deepcopy(tl.tlist['functional'][7])	#fontain
				tile.civilisation = False					#
				tile.build_here = False						#
				tile.can_grown = False						#
			tile.replace = tl.tlist['dungeon'][0]			#
			m.tilemap[pos[1]][pos[0]] = tile				#
			
		coin = random.randint(0,1)						#Set a Altar on 50% of all maps
		if coin == 1:									#that are generated with this function
			pos = m.find_any(tl.tlist['dungeon'][0])	#
			tile = deepcopy(tl.tlist['functional'][15])	#
			tile.civilisation = False					#
			tile.build_here = False						#
			tile.can_grown = False						#
			tile.replace = tl.tlist['dungeon'][0]		#
			m.tilemap[pos[1]][pos[0]] = tile			#
		
		#num_statue = random.randint(4,6)						#generate random statues
		#for l in range(0,num_statue):							#
		#	kind = random.randint(0,len(tl.tlist['statue'])-1)	#
		#	pos = m.find_any(tl.tlist['dungeon'][0])			#
		#	tile = deepcopy(tl.tlist['statue'][kind])			#
		#	tile.replace = tl.tlist['dungeon'][0]				#
		#	m.tilemap[pos[1]][pos[0]] = tile					#
			
		num_deco = random.randint(8,10)							#generate random deco
		for l in range(0,num_deco):								#
			if style == 'Tomb':									#
				kind = random.randint(3,5)						#
			else:												#
				kind = random.randint(0,2)						#
			pos = m.find_any(tl.tlist['dungeon'][0])			#
			tile = deepcopy(tl.tlist['deco'][kind])				#
			tile.replace = tl.tlist['dungeon'][0]				#
			m.tilemap[pos[1]][pos[0]] = tile					#
			
		#coin_cage = random.randint(0,2)																		#spawn cages
		#if coin_cage == 1:																						#
		#	pos = m.find_any(tl.tlist['dungeon'][0])															#
		#	m.npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['cage'][random.randint(0,len(ml.mlist['cage'])-1)])		#
		#	m.set_monster_strength(pos[0],pos[1],1,lvl_bonus=9)													#
		#	pos2 = m.find_any(tl.tlist['dungeon'][0])															#
		#	m.tilemap[pos2[1]][pos2[0]] = deepcopy(tl.tlist['portal'][9])										#
		#	m.tilemap[pos2[1]][pos2[0]].replace = deepcopy(tl.tlist['dungeon'][0])								#
		
		ran_statue = random.randint(0,99)																	#make animated statues
		num_statue = 0																						#
		if ran_statue > 49 and ran_statue < 90:																#
			num_statue = 1																					#
		elif ran_statue > 89:																				#
			num_statue = 2																					#
																											#
		if num_statue > 0:																					#
			m.make_special_monsters(1,num_statue,tl.tlist['dungeon'][0],m.monster_plus,'animated statue')	#
				
		m.spawn_monsters(0)																		#Spawn initial monsters
		m.make_special_monsters(10,20,tl.tlist['dungeon'][0],m.monster_plus,'vase')				#
		m.make_special_monsters(1,2,tl.tlist['dungeon'][0],m.monster_plus,'mimic')				#
		
		if style == 'Tomb' and stair_down == False:												#set a demonic chest
			m.make_special_monsters(1,3,tl.tlist['dungeon'][0],m.monster_plus,'demonic chest')	#
			if 'meet_old_neko' in player.quest_variables:
				if not 'saved_neko_soul' in player.quest_variables:
					mummy_pos = m.find_any(tl.tlist['dungeon'][0])
					m.npcs[mummy_pos[1]][mummy_pos[0]] = deepcopy(ml.mlist['special'][28])
					m.set_monster_strength(mummy_pos[0],mummy_pos[1],1,lvl_bonus=2)
					if player.difficulty == 4:
						m.npcs[mummy_pos[1]][mummy_pos[0]].AI_style = 'ignore'
					message.add('You feel the presence of a doomed soul here.') #TIPO1
		
		coin = random.randint(0,1)
		if coin == 1:
			m.spawn_magic_shops()
		
		if player.pet_pos != False and player.pet_on_map != False:
			m.npcs[0][0] = pet_help
			
		self.maplist[1][name] = m # Add map to world.maplist
		
		screen.render_load(19,99) #Render progress bar 99%
		
	def desert_generator(self,chance_object):
		#chance_objects must be between 0 and 99
		
		screen.render_load(18,1)
		
		name = 'desert_0_0'
		
		tilemap = []
		for a in range (0,max_map_size):
			tilemap.append([])
			for b in range (0,max_map_size):
				tilemap[a].append(0)
	
		m = maP(name,tilemap)
		m.map_type = 'desert'
		m.build_type = 'Full'
		m.monster_plus = 7
		m.thirst_multi_day = 2
		m.set_music('desert','night',True)
		
		m.fill(tl.tlist['extra'][0])
		
		y_river = random.randint((17),(max_map_size-25))
		river_offset = random.randint(-3,3)
		plus = 0
		minus = 0
		
		screen.render_load(18,20)
		
		for c in range (0,max_map_size):
			
			for g in range (-2,7):
				m.tilemap[y_river+river_offset+g][c] = tl.tlist['local'][0]#set grass
				
			for w in range (0,5):
				m.tilemap[y_river+river_offset+w][c] = tl.tlist['misc'][0]#set low water
				
			if river_offset < 4:
				plus = 1
			else:
				plus = 0
				
			if river_offset > -4:
				minus = -1
			else:
				minus = 0
				
			offset_change = random.randint(minus,plus)
			river_offset += offset_change
			
		m.exchange_when_surrounded(tl.tlist['misc'][0],tl.tlist['misc'][3],7)
		
		screen.render_load(18,40)
		
		for b in range(2,max_map_size-2,10):
			
			#north side of the river
			building_offset =random.randint(0,4)
			number_beds = 0
			
			for y in range(y_river-12,y_river-7):
				for x in range(b+building_offset,b+building_offset+5):
					
					if x == b+building_offset or x == b+building_offset+4:
						if y == y_river-10:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					elif y == y_river-12 or y == y_river-8:
						if x == b+building_offset+2:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					else:
						m.tilemap[y][x] = deepcopy(tl.tlist['extra'][1])
						
					if x == b+building_offset+1 or x == b+building_offset+3:
						if y == y_river-11 or y == y_river-9:
							
							obj_here = random.randint(0,2) #0: nothing, 1:bed 2:workbench
							
							if number_beds == 0:
								obj_here = 1
								
							if obj_here != 0:
								if obj_here == 1:
									obj = ('functional',8)
									number_beds += 1
								else:
									ran = random.randint(9,15)
									obj = ('functional',ran)
								
								m.tilemap[y][x] = deepcopy(tl.tlist[obj[0]][obj[1]])
								m.tilemap[y][x].replace = deepcopy(tl.tlist['extra'][1])
								m.tilemap[y][x].civilisation = False
								m.tilemap[y][x].build_here = False
								m.tilemap[y][x].move_group = 'house'
							
			#south side of the river			
			building_offset = random.randint(0,4)
			number_beds = 0
			
			screen.render_load(18,60)
			
			for y in range(y_river+8,y_river+13):
				for x in range(b+building_offset,b+building_offset+5):
					
					if x == b+building_offset or x == b+building_offset+4:
						if y == y_river+10:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					elif y == y_river+12 or y == y_river+8:
						if x == b+building_offset+2:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][9])
						else:
							m.tilemap[y][x] = deepcopy(tl.tlist['extra'][2])
					else:
						m.tilemap[y][x] = deepcopy(tl.tlist['extra'][1])
		
					if x == b+building_offset+1 or x == b+building_offset+3:
						if y == y_river+9 or y == y_river+11:
							
							obj_here = random.randint(0,2) #0: nothing, 1:bed 2:workbench
							
							if number_beds == 0:
								obj_here = 1
								
							if obj_here != 0:
								if obj_here == 1:
									obj = ('functional',8)
									number_beds += 1
								else:
									ran = random.randint(9,15)
									obj = ('functional',ran)
								
								m.tilemap[y][x] = deepcopy(tl.tlist[obj[0]][obj[1]])
								m.tilemap[y][x].replace = deepcopy(tl.tlist['extra'][1])
								m.tilemap[y][x].civilisation = False
								m.tilemap[y][x].build_here = False
								m.tilemap[y][x].move_group = 'house'
		
		make_bridges = True
		num_bridges = 0
		num_bridges_max = ((max_map_size/50)*3)+1
		
		screen.render_load(18,80)
		
		while num_bridges < num_bridges_max:
			x_pos = random.randint(5,max_map_size-5)
				
			num_wall = 0
				
			for test in range(0,max_map_size):
				if m.tilemap[test][x_pos].techID == tl.tlist['extra'][2].techID:
					num_wall += 1
				
			if num_wall == 0:
				num_bridges += 1
				for y in range(0,max_map_size):
					if m.tilemap[y][x_pos].techID == tl.tlist['misc'][0].techID or m.tilemap[y][x_pos].techID == tl.tlist['misc'][3].techID: #this is low wather or deep water
						replace = deepcopy(m.tilemap[y][x_pos])
						m.tilemap[y][x_pos] = deepcopy(tl.tlist['extra'][8])
						m.tilemap[y][x_pos].replace = replace
				
		for y in range (0,max_map_size):
			for x in range (0,max_map_size): 
				if m.tilemap[y][x].techID == tl.tlist['extra'][0].techID:
					chance = random.randint(0,99)
					if chance < chance_object:
						obj_numbers = (3,4,5,14)
						coin = random.randint(0,len(obj_numbers)-1)
						m.tilemap[y][x] = tl.tlist['extra'][obj_numbers[coin]]
						m.tilemap[y][x].replace = tl.tlist['extra'][0]#sand
				elif m.tilemap[y][x].techID == tl.tlist['local'][0].techID:
					chance = random.randint(0,99)
					if chance < chance_object:
						coin = random.randint(10,13)
						m.tilemap[y][x] = tl.tlist['extra'][coin]
						m.tilemap[y][x].replace = tl.tlist['local'][0]#grass
				elif m.tilemap[y][x].techID == tl.tlist['extra'][9].techID:
					for yy in range(y-1,y+2):
						if m.tilemap[yy][x].replace != None:
							m.tilemap[yy][x] = m.tilemap[yy][x].replace
					for xx in range(x-1,x+2):
						if m.tilemap[y][xx].replace != None:
							m.tilemap[y][xx] = m.tilemap[y][xx].replace
						
				if m.tilemap[y][x].techID == tl.tlist['functional'][8].techID:#bed
					ran = random.randint(5,6)
					m.npcs[y][x] = deepcopy(ml.mlist['special'][ran])
					m.set_monster_strength(x,y,0)
					
		
		m.set_frame(tl.tlist['functional'][0])
		
		screen.render_load(18,99)
		
		#set portal
		y = 2
		x = random.randint(2,max_map_size-2)
		m.tilemap[y][x] = tl.tlist['portal'][5]
		m.tilemap[y+1][x] = tl.tlist['extra'][0]#sand
		
		#set old neko house
		x = random.randint(1,42)
		y = random.randint(40,42)
		m.make_old_neko_house(x,y)
		
		m.spawn_monsters(0)
					
		self.maplist[0][name] = m
				
class mob():
	
	def __init__(self, name, on_map, attribute, pos =[40,40,0],glob_pos=[0,0],build='Manual'):
		
		self.name = name
		self.on_map = on_map
		self.attribute = attribute
		self.lp = attribute.max_lp
		self.mp = attribute.max_mp
		self.pos = pos	
		self.glob_pos = glob_pos
		self.last_map = 'Foo'
		self.cur_map = 'Bar'
		self.cur_z = self.pos[2]
		self.last_z = 'Baz'
		
	def move(self, x=0, y=0):
				
		mc = self.move_check(x,y)
		try:
			tile_move_group = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group
		except:
			tile_move_group = 'solid'
			print('move ERROR')
		
		player_move_groups = ['soil','low_liquid','shop','house','wet_entrance','dry_entrance']
		
		swim_check = True
		
		for i in ('Head','Body','Legs','Feet'): #DUBTE
			if player.inventory.wearing[i] != player.inventory.nothing:
				swim_check = False
				
		if swim_check == True:
			player_move_groups.append('swim')
		
		if player.buffs.get_buff('hexed') < 1:
			player_move_groups.append('holy')
		
		if self.buffs.get_buff('immobilized') > 0:
			player_move_groups = ['not_existent_group1','not_existent_group2']
		
		move_check2 = False	
		
		for j in player_move_groups:
			if j == tile_move_group:
				move_check2 = True
		
		if self.pet_pos != False and self.pet_on_map != False:
			try:
				if player.on_map != player.pet_on_map and 'stay_at_lvl' in world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties:
					mes = world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].name + ' can\'t follow you.' #TIPO2
					message.add(mes)
					player.pet_pos = False
					player.pet_on_map = False
			except:
				print('PET ERROR') #DUBTE
				player.pet_pos = False
				player.pet_on_map = False
		
		multi = 1
		
		if tile_move_group == 'jump' and world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]+(y*2)][self.pos[0]+(x*2)] == 0:
			test = self.move_check(x*2,y*2)
			try:
				tile_move_group2 = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+(y*2)][self.pos[0]+(x*2)].move_group
			except:
				tile_move_group2 = 'solid'
				print('move ERROR') #DUBTE
			if tile_move_group2 in player_move_groups:
				sfx.play('jump')
				mc = True
				move_check2 = True
				multi = 2
				
		if mc == True:
			if x > 0 and move_check2 == True and self.pos[0] < max_map_size - 1:
				if self.pet_pos != False and self.pet_on_map != False:
					try:
						if world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].anger == 'pet':
							world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].lp = 999 #set pets lp to 999 to make them unbreakable
						if player.pet_pos[0] != player.pos[0] or player.pet_pos[1] != player.pos[1]:
							world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]][self.pos[0]] = world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]]
							world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]] = 0
						self.pet_pos = deepcopy(self.pos)
						self.pet_on_map = deepcopy(self.on_map)
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].relation += 1
						if world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger < 300:
							world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger += 1
						if not 'found_item' in world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties:
							ran = random.randint(0,299)
							if ran == 1:
								world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties.append('found_item')
					except:
						message.add('[PET ERROR: Unfollow pet]') #DUBTE
						player.pet_pos = False
						player.pet_on_map = False
				self.pos[0] += 1*multi
			
			if x < 0 and move_check2 == True and self.pos[0] > 0:
				if self.pet_pos != False and self.pet_on_map != False:
					try:
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].lp = 999 #set pets lp to 999 to make them unbreakable
						world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]][self.pos[0]] = world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]]
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]] = 0
						self.pet_pos = deepcopy(self.pos)
						self.pet_on_map = deepcopy(self.on_map)
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].relation += 1
						if world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger < 300:
							world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger += 1
						if not 'found_item' in world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties:
							ran = random.randint(0,299)
							if ran == 1:
								world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties.append('found_item')
					except:
						message.add('[PET ERROR: Unfollow pet]') #DUBTE
						player.pet_pos = False
						player.pet_on_map = False
				self.pos[0] -= 1*multi
			
			if y > 0 and move_check2 == True and self.pos[1] < max_map_size - 1:
				if self.pet_pos != False and self.pet_on_map != False:
					try:
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].lp = 999 #set pets lp to 999 to make them unbreakable
						world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]][self.pos[0]] = world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]]
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]] = 0
						self.pet_pos = deepcopy(self.pos)
						self.pet_on_map = deepcopy(self.on_map)
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].relation += 1
						if world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger < 300:
							world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger += 1
						if not 'found_item' in world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties:
							ran = random.randint(0,299)
							if ran == 1:
								world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties.append('found_item')
					except:
						message.add('[PET ERROR: Unfollow pet]')
						player.pet_pos = False
						player.pet_on_map = False
				self.pos[1] += 1*multi
			
			if y < 0 and move_check2 == True and self.pos[1] > 0:
				if self.pet_pos != False and self.pet_on_map != False:
					try:
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].lp = 999 #set pets lp to 999 to make them unbreakable
						world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]][self.pos[0]] = world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]]
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]] = 0
						self.pet_pos = deepcopy(self.pos)
						self.pet_on_map = deepcopy(self.on_map)
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].relation += 1
						if world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger < 300:
							world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].hunger += 1
						if not 'found_item' in world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties:
							ran = random.randint(0,299)
							if ran == 1:
								world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]].properties.append('found_item')
					except:
						message.add('[PET ERROR: Unfollow pet]')
						player.pet_pos = False
						player.pet_on_map = False
				self.pos[1] -= 1*multi
		self.stand_check()
		
	def move_check(self,x,y):
		
		pickaxe_damage = True
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'door' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['dungeon'][6].techID:
			if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['dungeon'][4].techID or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['dungeon'][5].techID or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['dungeon'][6].techID:
				#this is a resisting door or a hidden door
				sfx.play('locked')
			else:
				sfx.play('open')
			message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_mes)
			tcat = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_tiles[0]
			tnum = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_tiles[1]
			world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(tl.tlist[tcat][tnum])
			return False
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'shop_enter':
			sfx.play('open')
			screen.render_fade(True,False)
			shop_types = ('pharmacy','pickaxe','hardware','deco','book','bomb','general') #DUBTE
			ran = random.randint(0,len(shop_types)-1)
			world.shop_generator(shop_types[ran])
			self.save_pos=(self.pos[0],self.pos[1],self.pos[2],self.on_map)
			world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace
			shop_pos = world.maplist[1]['shop_0_0'].find_first(tl.tlist['shop'][3])
			self.pos[0] = shop_pos[0]
			self.pos[1] = shop_pos[1]+1
			self.pos[2] = 1
			self.on_map = 'shop_0_0'
			player.stand_check()
			screen.render_fade(False,True)
			return False
			
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'shop_exit':
			sfx.play('open')
			self.pos[0] = self.save_pos[0]
			self.pos[1] = self.save_pos[1]
			self.pos[2] = self.save_pos[2]
			self.on_map = self.save_pos[3]
			player.stand_check()
			screen.render_fade(False,True)
			return False
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'enter_players_room':
			sfx.play('open')
			screen.render_fade(True,False)
			pos = world.maplist[self.pos[2]][self.on_map].find_first(tl.tlist['sanctuary'][7])
			player.pos[0] = pos[0]+1
			player.pos[1] = pos[1]
			player.stand_check()
			screen.render_fade(False,True)
			return False
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'exit_players_room':
			sfx.play('open')
			screen.render_fade(True,False)
			pos = world.maplist[self.pos[2]][self.on_map].find_first(tl.tlist['sanctuary'][6])
			player.pos[0] = pos[0]-1
			player.pos[1] = pos[1]
			player.stand_check()
			screen.render_fade(False,True)
			return False
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'holy' and player.buffs.get_buff('hexed') > 0:
			message.add('You can\'t pass blessed ground while you are hexed!') #TIPO1
			return False
		
		try:
			
			if world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]+y][self.pos[0]+x] != 0:
				player.attack_monster(self.pos[0]+x,self.pos[1]+y)
				return False
			
			if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].destroy != False: #for digging
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['misc'][28].techID:#this is obsidian
					heated_stone = True
				else:
					heated_stone = False
					
				if player.pos[2] > 1 and heated_stone == False:
					brimstone = True
				else:
					brimstone = False
				
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['misc'][36].techID:#this is an evolution stone in rock
					evolution_stone = True
				else:
					evolution_stone = False
				
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID != tl.tlist['misc'][28].techID and world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID != tl.tlist['global_caves'][2].techID:
					#this is not obsidian or soft soil
					stone = True
				else:
					stone = False
					
				if self.attribute.pickaxe_power + player.inventory.wearing['Pickaxe'].attribute.pickaxe_power >= world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].destroy:
					if self == player:
						message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_mes)
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID != tl.tlist['building'][3].techID: #this isn't a door
							if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].destroy > 1:
								sfx.play('rock_break')
							else:
								sfx.play('break')
						
						try:
							if self.skill.mining == 'Adept':
								mat_addition = 2
							elif self.skill.mining == 'Master':
								mat_addition = 5
							else:
								mat_addition = 0
								
							if player.inventory.check_suffix('Mining') == True:
								mat_addition += 1
								
							material = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[0]
							mat_num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[1] + mat_addition
							mes = player.inventory.materials.add(material,mat_num)
							message.add(mes)
							if player.skill.mining != 'Master':
								player.skill.mining_progress += 1
								if player.skill.mining_progress == 200 and player.skill.mining != 'Adept':
									player.skill.raise_skill('mining')
									message.add('Your mining skill reaches adept level!') #TIPO1
									sfx.play('lvl_up')
								if player.skill.mining_progress == 1000 and player.skill.mining != 'Master':
									player.skill.raise_skill('mining')
									message.add('Your mining skill reaches master level!')
									sfx.play('lvl_up')
						except:
							None
							
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['building'][3].techID: #this is a closed door
							world.maplist[self.pos[2]][self.on_map].countdowns.append(countdown('door', self.pos[0]+x, self.pos[1]+y,3))
							sfx.play('open')
							stone = False
							heated_stone = False
							brimstone = False
							pickaxe_damage = False
							
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace)
					if heated_stone == True:#drop heated stone
						ran = random.randint(0,99)
						if ran < 5:
							replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x]
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(tl.tlist['functional'][28])
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace = replace
					elif brimstone == True:#drop brimstone
						ran = random.randint(0,99)
						if ran < 5:
							replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x]
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(tl.tlist['functional'][29])
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace = replace
					elif stone == True:#drop stone
						ran = random.randint(0,99)
						if ran < 5:
							replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x]
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(tl.tlist['functional'][30])
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace = replace
					
					if evolution_stone == True:#drop evolution stone
						replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x]
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(tl.tlist['misc'][37])
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace = replace
					
					if player.inventory.wearing['Pickaxe'] != player.inventory.nothing and pickaxe_damage == True:
					
						player.inventory.wearing['Pickaxe'].take_damage()
					
						if player.inventory.wearing['Pickaxe'].state > 0:
							player.inventory.wearing['Pickaxe'].set_name()
						else:
							message.add('Your tool breaks into pieces.') #TIPO1
							player.inventory.wearing['Pickaxe'] = player.inventory.nothing
							sfx.play('item_break')
					
				else:
					if self == player:
							message.add('You are unable to destroy this with the tool in your hand.') #TIPO1
					
				return False
			
			else:
				None
				
			if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'tree':
				
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].techID == tl.tlist['local'][12].techID:#this is a ordenary tree
					apple = True
				else:
					apple = False
				
				if player.inventory.wearing['Axe'] != player.inventory.nothing: #if player has a axe in his hand			
					chop_success = True
					player.inventory.wearing['Axe'].take_damage()
					
					if player.inventory.wearing['Axe'].state > 0:
						player.inventory.wearing['Axe'].set_name()
					else:
						message.add('Your axe breaks into pieces.') #TIPO1
						player.inventory.wearing['Axe'] = player.inventory.nothing
						sfx.play('item_break')
					
				else:
					message.add('That hurts!') #TIPO1
					player.lp -= 1
					sfx.play('hit')
					if random.randint(0,9) != 0: #90% to fail chopping down the wood with bare hands
						chop_success = False
					else:
						chop_success = True
				
				if chop_success == True:
					
					if self.skill.woodcutting == 'Adept':
						mat_addition = 2
					elif self.skill.woodcutting == 'Master':
						mat_addition = 5
					else:
						mat_addition = 0
					
					material = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[0]
					mat_num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].conected_resources[1] + mat_addition
					mes = player.inventory.materials.add(material,mat_num)
					message.add(mes)
					sfx.play('chop')
					if player.skill.woodcutting != 'Master':
						player.skill.woodcutting_progress += 1
						if player.skill.woodcutting_progress == 200 and player.skill.woodcutting != 'Adept':
							player.skill.raise_skill('woodcutting')
							message.add('Your woodcutting skill reaches adept level!') #TIPO1
							sfx.play('lvl_up')
						if player.skill.woodcutting_progress == 1000 and player.skill.woodcutting != 'Master':
							player.skill.raise_skill('woodcutting')
							message.add('Your woodcutting skill reaches master level!')
							sfx.play('lvl_up')
					world.maplist[self.pos[2]][self.on_map].make_monsters_angry(self.pos[0],self.pos[1],'tree')
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace) #let the tree disappear
					
					if apple == True:
						ran = random.randint(0,99)
						if ran < 5:
							ran2 = random.randint(0,99)
						replace = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x])
						if ran2 < 20:
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(tl.tlist['functional'][32])
						else:
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x] = deepcopy(tl.tlist['functional'][31])
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].replace = replace
						
				return False
						
					
			if self.buffs.get_buff('immobilized') == 0:
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'low_liquid' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'swim' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]+y][self.pos[0]+x].move_group == 'wet_entrance':
					sfx.play('walk_wet')
				else:
					sfx.play('walk_dry')
			else:
				sfx.play('immobilized')
			
			return True
			
		except:
			
			None
			
	def stand_check(self):
		
		if self.on_map != 'shop_0_0':
			
			if self.on_map != self.cur_map:
				self.last_map = self.cur_map
				self.cur_map = self.on_map
		 	
			if self.pos[2] != self.cur_z:
				self.last_z = self.cur_z
				self.cur_z = self.pos[2]
		
		world.maplist[self.pos[2]][self.on_map].special_check(self.pos[0],self.pos[1])
		
		radius = 5
		
		if player.pos[2] > 0:
			radius = 2
		elif player.pos[2] == 0:
			if time.hour > 22 or time.hour < 4:
				radius = 2 
			elif time.hour > 21 or time.hour < 5:
				radius = 3 
			elif time.hour > 20 or time.hour < 6:
				radius = 4 
			elif time.hour > 19 or time.hour < 7:
				radius = 5 
			
		if player.buffs.get_buff('light') > 0 or player.buffs.get_buff('night vision') > 0:
			radius = 5
			
		if player.buffs.get_buff('blind') > 0:
			radius = 1
		
		message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].move_mes,True)
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage > 0 and player.buffs.get_buff('fire resistance') == 0:
			self.lp = self.lp - world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage
			if self == player:
				try:
					message.add(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage_mes + ' (' + str(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage) + ' Damage)')
				except:
					None
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage > 0 and world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].special_group == 'hot':
			sfx_flame = False
			body_list = ('Head','Body','Legs','Feet','Hold(R)','Hold(L)','Neck','Hand','Pickaxe','Axe') #CUIDAO
			for i in body_list:
				if player.inventory.wearing[i] != player.inventory.nothing and player.inventory.wearing[i].material == 'wooden':
					ran = random.randint(0,9)
					if ran < 4:
						message.add('Your '+player.inventory.wearing[i].name+' burns to ashes!') #TIPO2
						player.inventory.wearing[i] = player.inventory.nothing
						sfx_flame = True
			if sfx_flame == True:
				sfx.play('flame')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage < 0:
			if self.lp < self.attribute.max_lp:
				self.lp = self.lp - world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].damage
		
		luck = player.attribute.luck + player.inventory.wearing['Neck'].attribute.luck
		
		if player.buffs.get_buff('blessed') != 0:
				luck += 2
		
		for y in range(player.pos[1]-1,player.pos[1]+2):
			for x in range(player.pos[0]-1,player.pos[0]+2):
				if world.maplist[self.pos[2]][self.on_map].tilemap[y][x].techID == tl.tlist['dungeon'][6].techID:#this is a secret door
					ran = random.randint(0,25)#check players luck
					if ran < luck:
						world.maplist[self.pos[2]][self.on_map].tilemap[y][x] = deepcopy(tl.tlist['dungeon'][3])
						message.add('You notice a hidden door.') #TIPO1
						screen.write_hit_matrix(player.pos[0],player.pos[1],14)
						screen.write_hit_matrix(x,y,15)
						sfx.play('found')
				
				if world.maplist[self.pos[2]][self.on_map].tilemap[y][x].techID == tl.tlist['dungeon'][10].techID and world.maplist[self.pos[2]][self.on_map].tilemap[y][x].tile_pos == (10,10):#this is a trap which isn't already found
					ran = random.randint(0,25)#check players luck
					if ran < luck:
						world.maplist[self.pos[2]][self.on_map].tilemap[y][x].tile_pos = (10,8)
						message.add('You notice a trap.') #TIPO1
						screen.write_hit_matrix(player.pos[0],player.pos[1],14)
						screen.write_hit_matrix(x,y,15)
						sfx.play('found')
				
				if world.maplist[self.pos[2]][self.on_map].tilemap[y][x].techID == tl.tlist['dungeon'][12].techID and world.maplist[self.pos[2]][self.on_map].tilemap[y][x].tile_pos == (6,3,10,12):#this is a fontain that isn't already known
					ran = random.randint(0,15)#check players luck
					if ran < luck:
						world.maplist[self.pos[2]][self.on_map].tilemap[y][x].tile_pos = (12,11,12,12)
						world.maplist[self.pos[2]][self.on_map].tilemap[y][x].use_group = 'dont_drink'
						message.add('You notice a strange smell.') #TIPO1
						screen.write_hit_matrix(player.pos[0],player.pos[1],14)
						screen.write_hit_matrix(x,y,15)
						sfx.play('found')
				
				if world.maplist[self.pos[2]][self.on_map].tilemap[y][x].techID == tl.tlist['dungeon'][13].techID and world.maplist[self.pos[2]][self.on_map].tilemap[y][x].tile_pos == (6,3,10,12):#this is a fontain that isn't already known
					ran = random.randint(0,15)#check players luck
					if ran < luck:
						world.maplist[self.pos[2]][self.on_map].tilemap[y][x].tile_pos = (11,11,11,12)
						message.add('You notice a strange sparkle.')
						screen.write_hit_matrix(player.pos[0],player.pos[1],14)
						screen.write_hit_matrix(x,y,15)
						sfx.play('found')
				
		for y in range (-radius,radius+1):#line of sight
			for x in range (-radius,radius+1):
				try:
				
					dist = ((x)**2+(y)**2)**0.5
				
					if dist <= radius+1 or dist >= radius-1:
						
						run = True
						c = 0
						
						while run:
						
							try:
								yy = ((y*c)/dist)
							except:
								yy = 1
						
							try:
								xx = ((x*c)/dist)
							except:
								xx = 1
							
							view_x = int(xx) + self.pos[0]
							view_y = int(yy) + self.pos[1]
							
							world.maplist[self.pos[2]][self.on_map].known[view_y][view_x] = 1
							
							
							if world.maplist[self.pos[2]][self.on_map].tilemap[view_y][view_x].transparency == True and c < radius:
								c+=1
							else:
								run = False
				except:
					None
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['dungeon'][10].techID:
			
			kind =random.randint(0,3)
			position = deepcopy(player.pos)#copy player pos before the trap is triggered because teleport traps could change it
			
			if kind == 0:#dart trap
				ran = random.randint(0,25)
				
				if ran < luck:
					screen.write_hit_matrix(player.pos[0],player.pos[1],3)
					message.add('A flying dagger miss you.') #TIPO1
					sfx.play('miss')
				else:
					player.lp -= 3
					screen.write_hit_matrix(player.pos[0],player.pos[1],4)
					message.add('A flying dagger hits you.')
					sfx.play('hit')
					
					
			elif kind == 1:#teleport trap
				t=world.maplist[self.pos[2]][self.on_map].find_all_moveable()
				if len(t) > 0:
					rt = []
					for i in t:
						if world.maplist[self.pos[2]][self.on_map].npcs[i[1]][i[0]] == 0:
							rt.append((i[0],i[1]))
					if len(rt) > 0:
						screen.render_fade(True,False)
						ran = random.randint(0,len(rt)-1)
						player.pos[0] = rt[ran][0]
						player.pos[1] = rt[ran][1]
						screen.reset_hit_matrix()
						message.add('You are teleported randomly.') #TIPO1
						sfx.play('teleport')
						player.stand_check()
						screen.render_fade(False,True)
					else:
						message.add('Nothing seems to happen.')
						sfx.play('throw')
				
			elif kind == 2:#blinding trap
				ran = random.randint(10,30)
				player.buffs.set_buff('blind',ran)
				message.add('A garish flash blinds you.')
				
			elif kind == 3:#magic trap
				player.mp = 0
				screen.write_hit_matrix(player.pos[0],player.pos[1],7)
				message.add('You loose your focus.')
				
			replace = world.maplist[self.pos[2]][self.on_map].tilemap[position[1]][position[0]].replace
			world.maplist[self.pos[2]][self.on_map].tilemap[position[1]][position[0]] = deepcopy(tl.tlist['dungeon'][11])
			world.maplist[self.pos[2]][self.on_map].tilemap[position[1]][position[0]].replace = replace
					
		if player.lp <= 0:
			screen.render_dead()
		
		self.lp = int(self.lp)
		
		bgm.check_for_song()
		
		if time.hour%2 == 0 and time.minute == 0:
			help_player = deepcopy(player)
			help_player.on_map = 'elysium_0_0'
			help_player.pos[0] = max_map_size/2
			help_player.pos[1] = max_map_size/2
			help_player.pos[2] = 0
			save(None,help_player,time,gods,save_path,os.sep)
					
	def enter(self):
		
		if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'stair_down':
			if world.maplist[self.pos[2]+1][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][2].techID: #if there is a stair up below this
				screen.render_fade(True,False)
				player.pos[2] += 1
				player.stand_check()#to unveil the surroundings
				screen.render_fade(False,True)
			else:
				message.add('This stair seem to be blocked.') #TIPO1
			
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'stair_up': #this is a stair up
			if world.maplist[self.pos[2]-1][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][1].techID: #if there is a stair down above
				screen.render_fade(True,False)
				player.pos[2] -= 1
				player.stand_check()#to unveil the surroundings
				screen.render_fade(False,True)
			else:
				message.add('This stair seem to be blocked.')
			
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'drink':#this is a low wather or a fontain
			#drink water
			if player.attribute.thirst < player.attribute.thirst_max:
				sfx.play('no_fish')
				message.add('You take a sip of water.')
				player.attribute.thirst += 240 #this is 1/3 of the water te player needs per day
				if player.attribute.thirst > player.attribute.thirst_max:
					player.attribute.thirst = player.attribute.thirst_max+1#the +1 is because the player will lose one point at the same round so you would get just 99%
			else:
				message.add('You are not thirsty right now.')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'drink_acid':#this is a acid fontain
			#drink acid water
			if player.attribute.thirst < player.attribute.thirst_max:
				message.add('You take a sip of water.')
				player.lp -= 5
				message.add('It hurts like acid.')
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].tile_pos = (12,11,12,12)
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group = 'dont_drink'
			else:
				message.add('You are not thirsty right now.')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'dont_drink':
			message.add('You shouldn\'t drink this water!')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'drink_heal':#this is a healing fontain
			#drink healing water
			if player.attribute.thirst < player.attribute.thirst_max:
				message.add('You take a sip of water.')
				if player.lp < player.attribute.max_lp:
					player.lp += 5
					if player.lp > player.attribute.max_lp:
						player.lp = player.attribute.max_lp
						message.add('Your wounds are cured.')
				
				replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist['functional'][7])
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].civilisation = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].build_here = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].can_grown = False
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
			else:
				message.add('You are not thirsty right now.')
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'resource':
			res = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_resources[0]
			num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_resources[1]
			try:
				conected_tile = (world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[0],world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[1])
			except:
				None
			if res != 'coin':
				test = player.inventory.materials.add(res,num)
			else:
				player.coins += num
				test = '+' + str(num) + ' ' + res
				
			if test != 'Full!':
				sfx.play('pickup')
				message.add(test)
				replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				try:
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist[conected_tile[0]][conected_tile[1]])
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
				except:
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = replace
			else:
				message.add(test)
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'sleep':#this is a bed
			#sleep a bit
			sleeping = True
			lp = player.lp
			global sleep
			
			screen.render_request('Sleep: '+str(int((player.attribute.tiredness/player.attribute.tiredness_max)*100))+'%',' ','[Press ['+key_name['x']+' to wake up]',True) #TIPO2
			
			while sleeping:
				time.tick()
				screen.write_hit_matrix(player.pos[0],player.pos[1],25)
				if time.minute == 0 or time.minute%2 == 0:
					screen.render(0,True)
					screen.render_request('Sleep: '+str(int((player.attribute.tiredness/player.attribute.tiredness_max)*100))+'%',' ','[Press ['+key_name['x']+'] to wake up',False) #TIPO2
				sleep(0.01)
				player.attribute.tiredness += 5
				if player.buffs.get_buff('adrenalised') > 0:
					player.buffs.buff_list['adrenalised'] -= 5
				
				if player.buffs.get_buff('adrenalised') < 0:
					player.buffs.buff_list['adrenalised'] = 0
				
				if player.lp < lp:
					message.add('You were hurt!') #TIPO1
					sleeping = False
				
				if player.attribute.tiredness >= player.attribute.tiredness_max:#wake up because you've slept enough
					player.attribute.tiredness = player.attribute.tiredness_max +1 #the +1 is because the player will lose one point at the same round so you would get just 99%
					message.add('You feel refreshed.') #TIPO1
					sleeping = False
					
				if int((player.attribute.hunger_max*100)/max(player.attribute.hunger,1)) < 11:
					message.add('You feel hungry.') #TIPO1
					sleeping = False
					
				if int((player.attribute.thirst_max*100)/max(player.attribute.thirst,1)) < 11:
					message.add('You feel thirsty.') #TIPO1
					sleeping = False
					
				monster_test = False
					
				for y in range (player.pos[1]-2, player.pos[1]+3):#check for a monster
					for x in range (player.pos[0]-2, player.pos[0]+3):
						
						try:
							if world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]][self.pos[0]] != 0:#<-------change this so that friendly npcs are ignored 
								if world.maplist[self.pos[2]][self.on_map].npcs[self.pos[1]][self.pos[0]].AI_style == 'hostile':
									monster_test = True	
						except:
							None
						
				if monster_test == True:#wake up because a monster borders the players sleep
					message.add('You wake up with a sense of danger.') #TIPO1
					sleeping = False
				
				ui = getch(screen.displayx,screen.displayy,0,2,mouse=game_options.mousepad)
				if ui == 'x':
					message.add('You wake up.') #TIPO1
					sleeping = False
				
			screen.reset_hit_matrix()
			screen.render(0)
			
			
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'gather':
			help_container = container([world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_items])
			item_name = help_container.items[0].name
			test_loot = help_container.loot(0)
			if test_loot == True:
				sfx.play('pickup')
				string = '+[' + item_name + ']'
				message.add(string)
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = 0
			else:
				message.add('Your inventory is full!') #TIPO1
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'gather_scrub':
			help_container = container([world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_items])
			item_name = help_container.items[0].name
			test_loot = help_container.loot(0)
			if test_loot == True:
				sfx.play('pickup')
				string = '+[' + item_name + ']'
				message.add(string)
				cat = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[2][0]
				num = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[2][1]
				replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = tl.tlist[cat][num]
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
			else:
				message.add('Your inventory is full!') #TIPO1
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'chicken_nest':
			
			pos_egg = -1
			for c in range(0,len(player.inventory.food)):
				if player.inventory.food[c] != player.inventory.nothing and player.inventory.food[c].techID == il.ilist['food'][44].techID and player.inventory.food[c].rotten == False:
					pos_egg = c
			
			if pos_egg == -1:
				message.add('You need a egg to use a chicken nest.') #TIPO1
			else:
				screen.render_request('Put an egg in the nest?','['+key_name['e']+'] - Yes','['+key_name['x']+'] - No') #TIPO2
				run = True
				while run:
					ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
					
					if ui == 'exit':
						exitgame = True
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
						master_loop = False
						playing = False
						run = False
						return('exit')
					
					if ui == 'e':
						replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist['functional'][44])
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
						player.inventory.food[pos_egg] = player.inventory.nothing
						run = False
					elif ui == 'x':
						run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'nest':
			num_nest_free = 0
			for y in range(0,max_map_size):
				for x in range(0,max_map_size):
					if world.maplist[0]['elysium_0_0'].tilemap[y][x].techID == tl.tlist['sanctuary'][4].techID and world.maplist[0]['elysium_0_0'].npcs[y][x] == 0:#this is an empty nest box
						num_nest_free += 1
			if player.pet_pos != False and player.pet_on_map != False:
				num_nest_free -= 1 
			if num_nest_free > 0:		
				pos_egg = -1
				for c in range(0,len(player.inventory.misc)):
					if player.inventory.misc[c] != player.inventory.nothing and player.inventory.misc[c].techID == il.ilist['misc'][87].techID:
						pos_egg = c
				if pos_egg == -1:
					message.add('You need a monster egg to use a nest box.') #TIPO1
				else:
					screen.render_request('Put an egg in the nest box?','['+key_name['e']+'] - Yes','['+key_name['x']+'] - No') #TIPO2
					run = True
					while run:
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
					
						if ui == 'exit':
							exitgame = True
							screen.render_load(5)
							save(world,player,time,gods,save_path,os.sep)
							screen.save_tmp_png()
							master_loop = False
							playing = False
							run = False
							return('exit')
					
						if ui == 'e':
							replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist['sanctuary'][5])
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
							player.inventory.misc[pos_egg] = player.inventory.nothing
							run = False
						elif ui == 'x':
							run = False
			else:
				message.add('You can\'t hatch any more pets!') #TIPO1
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'carpenter': 
			#this is a carpenter's workbench
			
			run = True
			first_call = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request(l10n.format_value("carpenter-produce", {"keyname1": key_name['e']}),l10n.format_value("carpenter-take", {"keyname2": key_name['b']}), '['+key_name['x']+'] - leave',first_call) #TIPO2
					else:
						screen.render_request(l10n.format_value("workbench-full", {"keyname1": key_name['e']}),l10n.format_value("carpenter-take", {"keyname2": key_name['b']}), '['+key_name['x']+'] - leave',first_call)
				else:
					screen.render_request(l10n.format_value("carpenter-produce", {"keyname1": key_name['e']}),l10n.format_value("carpenter-pick", {"keyname2": key_name['b']}), '['+key_name['x']+'] - leave',first_call)
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						
						if player.inventory.materials.wood >= 10:
							gc = screen.get_choice(l10n.format_value("what-produce"),(l10n.format_value("carpenter-workbench"),l10n.format_value("carver-workbench"),l10n.format_value("stonecuter-workbench"),l10n.format_value("forger-workbench"),l10n.format_value("alchemist-workshop"),l10n.format_value("miscellaneous"),),True)
							
							if gc == 'Break':
								run = False
							elif gc < 5:# give the chosen workbench to the player
								items = (il.ilist['misc'][3],il.ilist['misc'][4],il.ilist['misc'][5],il.ilist['misc'][6],il.ilist['misc'][7])
								choose = gc
							elif gc == 5:
								fence = deepcopy(il.ilist['misc'][107])
								fence.stack_size = fence.max_stack_size
								items = (il.ilist['misc'][1], il.ilist['misc'][2],il.ilist['misc'][10],il.ilist['misc'][11],il.ilist['misc'][68],il.ilist['misc'][13],fence)
								#chest, bed, table, w. seat, bookshelf
								gc2 = screen.get_choice(l10n.format_value("what-producexactly"), (l10n.format_value("chest"),l10n.format_value("bed"),l10n.format_value("table"),l10n.format_value("seat"),l10n.format_value("throne"),l10n.format_value("bookshelf"),l10n.format_value("fence")),True)
								choose = gc2
							try:
								hc = container([items[choose],])
								test = hc.loot(0)
								if test == False:
									if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose],],False)
									else:
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
								sfx.play('craft')	
								message_string = l10n.format_value("produced-a", {"item1": items[choose].name})
								message.add(message_string)
								if test == False:
									message.add(l10n.format_value("store-workbench"))
								player.inventory.materials.wood -= 10
							except:
								None
								
							run = False
						
						else:
							message.add(l10n.format_value("not-enoughwood"))
							run = False
						
				elif ui == 'b':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
					else:
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace.techID != tl.tlist['sanctuary'][0].techID:
							#this wb dosen't stand inside the sanctuary
							helpc = container([il.ilist['misc'][3]],True)
							item_name = helpc.items[0].name
							test_loot = helpc.loot(0)
							run = False
							if test_loot == True:
								sfx.play('pickup')
								string = '+[' + item_name + ']'
								message.add(string)
								world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						else:
							message.add(l10n.format_value("workbench-attached"))
							run = False
						
				elif ui == 'x':
					
					run = False
					
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'carver': 
			#this is a carvers's workbench
			
			run = True
			first_call = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request(l10n.format_value("carver-produce", {"keyname1": key_name['e']}),l10n.format_value("carver-take", {"keyname2": key_name['b']}), '['+key_name['x']+'] - leave',first_call)
					else:
						screen.render_request(l10n.format_value("workbench-full", {"keyname1": key_name['e']}),l10n.format_value("carver-take", {"keyname2": key_name['b']}), '['+key_name['x']+'] - leave',first_call)
				else:
					screen.render_request(l10n.format_value("carver-produce", {"keyname1": key_name['e']}),l10n.format_value("carver-pick", {"keyname2": key_name['b']}), '['+key_name['x']+'] - leave',first_call)
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						if player.inventory.materials.wood >= 5:
							
							final_choice = 'Foo'
							gc = screen.get_choice(l10n.format_value("what-produce"), (l10n.format_value("tool"),l10n.format_value("weapon"),l10n.format_value("armor"),l10n.format_value("jewelry")), True)
							
							if gc == 0: #make a tool
								torch = deepcopy(il.ilist['misc'][44])
								torch.stack_size = 4
								items = (torch, item_wear('axe',0,0), item_wear('pickaxe',0,0),il.ilist['misc'][14])
								final_choice = screen.get_choice(l10n.format_value("what-producexactly"), (l10n.format_value("torch"),l10n.format_value("axe"),l10n.format_value("pickaxe"),l10n.format_value("fishing-rod")),True)
							elif gc == 1: #make a weapon
								items = (item_wear('knife',0,0), item_wear('dagger',0,0), item_wear('sword',0,0), item_wear('wand',0,0), item_wear('rune',0,0), item_wear('rune staff',0,0), item_wear('artefact',0,0))
								class_choice = screen.get_choice(l10n.format_value("what-producexactly"), (l10n.format_value("melee-weapon"),l10n.format_value("magic-weapon")), True)
								if class_choice == 0:
									ran = random.randint(0,99)
									if player.skill.weapon_crafting == 'Novice':
										if ran < 90:
											final_choice = 0
										else:
											finnal_choice = 1
									elif player.skill.weapon_crafting == 'Adept':
										if ran < 10:
											final_choice = 0
										elif ran < 90:
											final_choice = 1
										else:
											final_choice = 2
									elif player.skill.weapon_crafting == 'Master':
										if ran < 5:
											final_choice = 0
										elif ran < 15:
											final_choice = 1
										else:
											final_choice = 2	
								else:
									ran = random.randint(0,99)
									if player.skill.weapon_crafting == 'Novice':
										if ran < 90:
											final_choice = 3
										else:
											finnal_choice = 4
									elif player.skill.weapon_crafting == 'Adept':
										if ran < 10:
											final_choice = 3
										elif ran < 90:
											final_choice = 4
										else:
											final_choice = 5
									elif player.skill.weapon_crafting == 'Master':
										if ran < 5:
											final_choice = 3
										elif ran < 15:
											final_choice = 4
										else:
											final_choice = 5
							elif gc == 2: #make some armor
								items = (item_wear('shoes',0,0), item_wear('cuisse',0,0), item_wear('helmet',0,0), item_wear('armor',0,0))
								final_choice = screen.get_choice(l10n.format_value("what-producexactly"), (l10n.format_value("shoes"),l10n.format_value("cuisse"),l10n.format_value("helmet"),l10n.format_value("armor")), True)
							elif gc == 3:#make some jewlry
								items = (item_wear('ring',0,0,suffix = 'Emptiness'),  item_wear('amulet',0,0,suffix = 'Emptiness'),  item_wear('seal ring',0,0,suffix = 'Emptiness'), item_wear('talisman',0,0,suffix = 'Emptiness'))
								final_choice = screen.get_choice(l10n.format_value("what-producexactly"), (l10n.format_value("ring"),l10n.format_value("amulet"),l10n.format_value("seal-ring"),l10n.format_value("talisman")), True)
							else:
								final_choice = 'Foo'
							
							choose = final_choice
							try:
								if choose != 'Foo':
									hc = container([items[choose],])
									test = hc.loot(0)
									if test == False:
										if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
											world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
										else:
											world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
									sfx.play('craft')
									
								message_string = l10n.format_value("produced-a", {"item1": items[choose].name})
								message.add(message_string)
								if choose != 'Foo':
									if test == False:
										message.add(l10n.format_value("store-workbench"))
									player.inventory.materials.wood -= 5
							except:
								None
								
							run = False
						
						else:
							message.add(l10n.format_value("not-enoughwood"))
							run = False
						
				elif ui == 'b':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
					else:
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace.techID != tl.tlist['sanctuary'][0].techID:
							#this wb dosen't stand inside the sanctuary
							helpc = container([il.ilist['misc'][4]],True)
							item_name = helpc.items[0].name
							test_loot = helpc.loot(0)
							run = False
							if test_loot == True:
								sfx.play('pickup')
								string = '+[' + item_name + ']'
								message.add(string)
								world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						else:
							message.add(l10n.format_value("workbench-attached"))
							run = False
						
				elif ui == 'x':
					
					run = False
									
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'stonecutter': 
			#this is a stonecutter's workbench
			
			run = True
			first_call = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - produce something (-10 Stone)', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave',first_call)
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave',first_call)
				else:
					screen.render_request('['+key_name['e']+'] - produce something (-10 Stone)', '['+key_name['b']+'] - pick up workbench', '['+key_name['x']+'] - leave',first_call)
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						if player.inventory.materials.stone >= 10:
							
							gc = screen.get_choice('What do you want to produce?' ,('Functional Things', 'Decorative Things'), True)
							
							if gc == 0: #make something functional
								planter = deepcopy(il.ilist['misc'][115])
								planter.stack_size = 5
								items = (il.ilist['misc'][0], il.ilist['misc'][8], il.ilist['misc'][9],il.ilist['misc'][114],planter)
								#items: fontain, furnace, altar, enchantment table, planter
								gc2 = screen.get_choice('What do you want to produce exactly?' ,('Fountain','Furnace','Altar','Enchantment Table','Planter (5x)'), True)
							elif gc == 1:#make something decorative
								menhir = deepcopy(il.ilist['misc'][113])
								menhir.stack_size = 5
								items = (il.ilist['misc'][12],il.ilist['misc'][21],il.ilist['misc'][69],menhir)
								#items: stone seat, pilar, throne, menhir(5x)
								gc2 = screen.get_choice('What do you want to produce?' ,('Seat','Pilar','Throne','Menhir (5x)'), True)
							else:
								return False
							
							choose = gc2
							try:
								hc = container([items[choose],])
								test = hc.loot(0)
								if test == False:
									if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
									else:
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
								sfx.play('stonecutter')
								message_string = 'You produced a ' + items[choose].name + '.'
								message.add(message_string)
								if test == False:
									message.add('You store it in the workbench.')
								player.inventory.materials.stone -= 10
							except:
								None
								
							run = False
						
						else:
							message.add('You do not have enough Stone!')
							run = False
						
				elif ui == 'b':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
					else:
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace.techID != tl.tlist['sanctuary'][0].techID:
							#this wb dosen't stand inside the sanctuary
							helpc = container([il.ilist['misc'][5]],True)
							item_name = helpc.items[0].name
							test_loot = helpc.loot(0)
							run = False
							if test_loot == True:
								sfx.play('pickup')
								string = '+[' + item_name + ']'
								message.add(string)
								world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						else:
							message.add('This workbench seems to be attached to the floor.')
							run = False
						
				elif ui == 'x':
					
					run = False
					
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'forger' or world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'masterforge': 
			#this is a forger's workbench or a master forge
			
			run = True
			first_call = True
			
			while run:
				
				price = 5
				if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][23].techID: #this is a master forge
					price = 15
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						string = ('['+key_name['e']+'] - produce something (-' + str(price) + ' Ore)', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave',first_call)
						screen.render_request(string[0],string[1],string[2])
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a produced item', '['+key_name['x']+'] - leave',first_call)
				else:
					string = '['+key_name['e']+'] - produce something (-' + str(price) + ' Ore)', '['+key_name['b']+'] - pick up workbench', '['+key_name['x']+'] - leave'
					screen.render_request(string[0],string[1],string[2],first_call)
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					
					if test == True:
						if player.inventory.materials.ore >= price:
							if player.skill.metallurgy == 'Novice':
								material = random.randint(6,11)#tin to bronze
							elif player.skill.metallurgy == 'Adept':
								material = random.randint(11,18)#bronze to titan
							elif player.skill.metallurgy == 'Master':
								material = random.randint(18,20)#titan to magnicum
							
							if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].techID == tl.tlist['functional'][23].techID: #this is a master forge
								material = 20 #magnicum only
							
							final_choice = 'Foo'
							gc = screen.get_choice('What do you want to procuce?', ('Tool', 'Weapon', 'Armor','Jewelry'), True)
							
							if gc == 0: #make a tool
								final_choice = screen.get_choice('What do you want to procuce exactly?', ('Axe', 'Pickaxe', 'Bucket'), True)
								items = (item_wear('axe',material,0), item_wear('pickaxe',material,0), il.ilist['misc'][84]) 
							elif gc == 1: #make a weapon
								items = (item_wear('knife',material,0), item_wear('dagger',material,0), item_wear('sword',material,0), item_wear('wand',material,0), item_wear('rune',material,0), item_wear('rune staff',material,0), item_wear('artefact',material,0))
								class_choice = screen.get_choice('What do you want to prodcuce?', ('Melee Weapon','Magic Weapon'), True)
								if class_choice == 0:
									ran = random.randint(0,99)
									if player.skill.weapon_crafting == 'Novice':
										if ran < 90:
											final_choice = 0
										else:
											finnal_choice = 1
									elif player.skill.weapon_crafting == 'Adept':
										if ran < 10:
											final_choice = 0
										elif ran < 90:
											final_choice = 1
										else:
											final_choice = 2
									elif player.skill.weapon_crafting == 'Master':
										if ran < 5:
											final_choice = 0
										elif ran < 15:
											final_choice = 1
										else:
											final_choice = 2	
								else:
									ran = random.randint(0,99)
									if player.skill.weapon_crafting == 'Novice':
										if ran < 90:
											final_choice = 3
										else:
											finnal_choice = 4
									elif player.skill.weapon_crafting == 'Adept':
										if ran < 10:
											final_choice = 3
										elif ran < 90:
											final_choice = 4
										else:
											final_choice = 5
									elif player.skill.weapon_crafting == 'Master':
										if ran < 5:
											final_choice = 3
										elif ran < 15:
											final_choice = 4
										else:
											final_choice = 5
							elif gc == 2: #make some armor
								final_choice = screen.get_choice('What do you want to procuce exactly?', ('Shoes', 'Cuisse', 'Helmet', 'Armor'), True)
								items = (item_wear('shoes',material,0), item_wear('cuisse',material,0), item_wear('helmet',material,0), item_wear('armor',material,0))
							elif gc == 3:#make some  jewelry
								items = (item_wear('ring',material,0,suffix = 'Emptiness'),  item_wear('amulet',material,0,suffix = 'Emptiness'),  item_wear('seal ring',material,0,suffix = 'Emptiness'), item_wear('talisman',material,0,suffix = 'Emptiness'))
								final_choice = screen.get_choice('What do you want to prodcuce?', ('Ring','Amulet','Seal Ring','Talisman'), True)
							else:
								return False
							
							choose = final_choice
							try:
								if choose != 'Foo':
									hc = container([items[choose],])
									test = hc.loot(0)
									if test == False:
										if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
											world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
										else:
											world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
								
								sfx.play('forger')
								message_string = 'You produced a ' + items[choose].name + '.'
								message.add(message_string)
								if choose != 'Foo':
									if test == False:
										message.add('You store it in the workbench.')
									player.inventory.materials.ore -= price
							except:
								None
								
							run = False
						
						else:
							message.add('You do not have enough ore!')
							run = False
						
				elif ui == 'b':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
					else:
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace.techID != tl.tlist['sanctuary'][0].techID:
							#this wb dosen't stand inside the sanctuary
							helpc = container([il.ilist['misc'][6]],True)
							item_name = helpc.items[0].name
							test_loot = helpc.loot(0)
							run = False
							if test_loot == True:
								sfx.play('pickup')
								string = '+[' + item_name + ']'
								message.add(string)
								world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						else:
							message.add('This workbench seems to be attached to the floor.')
							run = False
						
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'alchemist': 
			#this is a alchemists's workshop
			
			run = True
			first_call = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - brew a potion (-5 Herbs)', '['+key_name['b']+'] - take a potion', '['+key_name['x']+'] - leave',first_call)
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take a potion', '['+key_name['x']+'] - leave',first_call)
				else:
					screen.render_request('['+key_name['e']+'] - brew a potion (-5 Herbs)', '['+key_name['b']+'] - pick up workshop', '['+key_name['x']+'] - leave',first_call)
				
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					if test == True:
						if player.inventory.materials.herb >= 5:
							
							weak_potions = (il.ilist['food'][50],il.ilist['food'][51],il.ilist['food'][52],il.ilist['food'][53])
							#weak potions are: w.p.o. healing, w.p.o. feeding, w.p.o. refreshing, w.p.o. vitalising
							ordenary_potions = (il.ilist['food'][13],il.ilist['food'][14],il.ilist['food'][15],il.ilist['food'][16])
							#ordenary potions are: p.o. healing, p.o. feeding, p.o. refreshing, p.o. vitalising 
							strong_potions = (il.ilist['food'][17],il.ilist['food'][18],il.ilist['food'][19],il.ilist['food'][20])
							#strong potions are: s.p.o. healing, s.p.o. feeding, s.p.o. refreshing, s.p.o. vitalising 
							upgrade_potions = (il.ilist['food'][24],il.ilist['food'][21],il.ilist['food'][22],il.ilist['food'][23])
							#upgrade potions are: p.o. life, p.o. hunger, p.o. thirst, p.o. tiredness
							
							choose = random.randint(0,99) 
							
							if player.skill.alchemy == 'Novice':
								items = weak_potions
							elif player.skill.alchemy == 'Adept':
								ran = random.randint(0,99)
								if ran < 1:
									items = upgrade_potions
								else:
									items = ordenary_potions
							elif player.skill.alchemy == 'Master':
								ran = random.randint(0,99)
								if ran < 1:
									items = upgrade_potions
								else:
									items = ordenary_potions
									
							choose = screen.get_choice('What do you like to brew?',('Potion of Healing','Potion of Feeding','Potion of Refreshing','Potion of Vitalising'),True)
							try:
								hc = container([items[choose],])
								test = hc.loot(0)
								if test == False:
									if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
									else:
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
							
								sfx.play('alchemy')	
								message_string = 'You brewed a ' + items[choose].name + '.'
								message.add(message_string)
								if test == 0:
									message.add('You store it in the workshop.')
								player.inventory.materials.herb -= 5
								run = False
							except:
								run = False
						
						else:
							message.add('You do have not enough herbs!')
							run = False
						
				elif ui == 'b':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
					else:
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace.techID != tl.tlist['sanctuary'][0].techID:
							#this ws dosen't stand inside the sanctuary
							helpc = container([il.ilist['misc'][7]],True)
							item_name = helpc.items[0].name
							test_loot = helpc.loot(0)
							run = False
							if test_loot == True:
								sfx.play('pickup')
								string = '+[' + item_name + ']'
								message.add(string)
								world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						else:
							message.add('This workshop seems to be attached to the floor.')
							run = False
						
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'thinker_workshop': 
			#this is a Thinker workshop
			
			run = True
			first_call = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - produce something (-1 gem)', '['+key_name['b']+'] - take something', '['+key_name['x']+'] - leave',first_call)
					else:
						screen.render_request('['+key_name['e']+'] -     XXXXXXXXXXXX            ', '['+key_name['b']+'] - take something', '['+key_name['x']+'] - leave',first_call)
				else:
					screen.render_request('['+key_name['e']+'] - produce something (-1 gem)', '['+key_name['b']+'] - pick up workshop', '['+key_name['x']+'] - leave',first_call)
				
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					test = False
					
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
							test = True
					else:
						test = True
					
					if test == True:
						if player.inventory.materials.gem >= 1:
							
							transmitter = deepcopy(il.ilist['misc'][93])
							transmitter.stack_size = transmitter.max_stack_size
							
							signal = deepcopy(il.ilist['misc'][94])
							signal.stack_size = signal.max_stack_size
							
							switch = deepcopy(il.ilist['misc'][95])
							switch.stack_size = switch.max_stack_size
							
							door = deepcopy(il.ilist['misc'][96])
							door.stack_size = door.max_stack_size
							
							plate = deepcopy(il.ilist['misc'][97])
							plate.stack_size = plate.max_stack_size
							
							pit = deepcopy(il.ilist['misc'][98])
							pit.stack_size = pit.max_stack_size
							
							emitter = deepcopy(il.ilist['misc'][99])
							emitter.stack_size = emitter.max_stack_size
							
							items = [transmitter,switch,plate,emitter,signal,door,pit]
							names = []
							for i in items:
								n = i.name+' ('+str(i.stack_size)+'x)'
								names.append(n) 
									
							choose = screen.get_choice('What do you like to produce?',names,True)
							
							try:
								hc = container([items[choose],])
								test2 = hc.loot(0)
								if test2 == False:
									if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0: 
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([items[choose]],False)
									else:
										world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(items[choose])
							
								sfx.play('craft')	
								message_string = 'You produced: ' + names[choose]
								message.add(message_string)
								if test2 == False:
									message.add('You store it in the workshop.')
								player.inventory.materials.gem -= 1
								run = False
							except:
								run = False
						
						else:
							message.add('You do have not enough gems!')
							run = False
						
				elif ui == 'b':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory(False)
						run = False
					else:
						if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace.techID != tl.tlist['sanctuary'][0].techID:
							#this ws dosen't stand inside the sanctuary
							helpc = container([il.ilist['misc'][100],],True)
							item_name = helpc.items[0].name
							test_loot = helpc.loot(0)
							run = False
							if test_loot == True:
								sfx.play('pickup')
								string = '+[' + item_name + ']'
								message.add(string)
								world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						else:
							message.add('This workshop seems to be attached to the floor.')
							run = False
						
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'enchantment': 
			#this is a enchantment table
			
			run = True
			first_call = True
			
			while run:
				
				if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
					if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						screen.render_request('['+key_name['e']+'] - enchant item ['+str(len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items))+'x]', '['+key_name['b']+'] - extract magic (-1 item)', '['+key_name['x']+'] - leave',first_call)
					else:
						screen.render_request('['+key_name['e']+'] - enchant item ['+str(len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items))+'x]', '['+key_name['b']+'] -     XXXXXXXXXXXX            ', '['+key_name['x']+'] - leave',first_call)
				else:
					screen.render_request('['+key_name['e']+'] - pick up table', '['+key_name['b']+'] - extract magic (-1 item)', '['+key_name['x']+'] - leave',first_call)
				
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
					
				if ui == 'e':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:
						name_list = []
						num_list = []
						for i in range(0,len(player.inventory.equipment)):
							if player.inventory.equipment[i].cursed == 1 and player.inventory.equipment[i].artefact == False and player.inventory.equipment[i].suffix == 'Emptiness':
								name_list.append(player.inventory.equipment[i].name)
								num_list.append(i)
								
						if len(num_list) > 0:
							ui2 = screen.get_choice('Choose an item for enchantment!',name_list,True)
							if ui2 != 'Break':
								if player.inventory.equipment[num_list[ui2]].classe == 'amulet' or player.inventory.equipment[num_list[ui2]].classe == 'seal ring':
									enchantment_list = ['Rage','Protection','Regeneration','Learning','Concentration']
								else:
									enchantment_list = ['Pois. Prot.','Blind Prot.','Hex. Prot.','Bleed. Prot.','Instab. Prot.']
							else:
								run = False
								return False
							ui3 = screen.get_choice('Choose an enchantment!',enchantment_list,True)
							if ui3 != 'Break':
								sfx.play('aura')
								message.add('Your '+player.inventory.equipment[ui2].classe+' has been enchanted!')
								del world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items[0]
								if len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) == 0:
									world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = 0
								player.inventory.equipment[num_list[ui2]].suffix = enchantment_list[ui3]
								player.inventory.equipment[num_list[ui2]].identification()
								run = False
							else:
								run = False
								return False
						else:
							message.add('You do not own an enchantable item!')
							run = False
							return False
					else:
						hc = container([il.ilist['misc'][114],])
						test = hc.loot(0)
						if test == True:
							sfx.play('pickup')
							world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
							run = False
						else:
							message.add('Your inventory is full!')
		
				if ui == 'b':
					if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0 or len(world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items) < 7:
						name_list = []
						num_list = []
						for i in range(0,len(player.inventory.equipment)):
							if player.inventory.equipment[i].known == True and player.inventory.equipment[i].artefact == False and player.inventory.equipment[i].suffix != 'Emptiness' and player.inventory.equipment[i].suffix != ' ' and player.inventory.equipment[i].cursed > 0:
								name_list.append(player.inventory.equipment[i].name)
								num_list.append(i)
						if len(num_list) > 0:
							ui2 = screen.get_choice('Choose an item for extraction!',name_list,True)
							if ui2 != 'Break':
								sfx.play('item_break')
								message.add('You remove the magic from your '+player.inventory.equipment[ui2].classe+'!')
								if world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] == 0:
									world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] = container([player.inventory.equipment[ui2],])
								else:
									world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].items.append(player.inventory.equipment[ui2])
								player.inventory.equipment[ui2] = player.inventory.nothing
								run = False
							else:
								run = False
								return False
						else:
							message.add('You have no suitable item for extraction!')
							run = False
							return False
				
				if ui == 'x':
					run = False
					
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'furnace': 
			#this is a furnace
			
			run = True
			first_call = True
			
			while run:
				
				screen.render_request(l10n.format_value("fire-furnace", {"furn1": key_name['e']}),l10n.format_value("pick-furnace", {"furn2": key_name['b']}),l10n.format_value("leave-furnace", {"furn3": key_name['x']}),first_call)
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					
					screen.render_request(l10n.format_value("cook-furnace", {"furn1": key_name['e']}),l10n.format_value("heat-furnace", {"furn2": key_name['b']}),l10n.format_value("cancel-furnace", {"furn3": key_name['x']}),False)
					ui2 = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
					
					if ui2 == 'e' and player.inventory.materials.wood >= 2:
						
						name_list = []
						food_list = []
						slot_list = []
						
						for i in range(0,len(player.inventory.food)):
							if player.inventory.food[i] != player.inventory.nothing:
								if player.inventory.food[i].rotten == False:
									name_list.append(player.inventory.food[i].name)
									try:
										food_list.append(player.inventory.food[i].cooking_result)
									except:
										food_list.append(47)
									slot_list.append(i)
								
						if len(name_list) == 0:
							message.add(l10n.format_value("no-cook"))
							run = False
						else:
							result = screen.get_choice(l10n.format_value("choose-cook", {"furn3": key_name['x']}),name_list,True)
							
							if result != 'Break' and result != 'exit':
								player.inventory.materials.wood -= 2
								sfx.play('flame')
								message.add(l10n.format_value("light-fire"))
								message.add('-['+player.inventory.food[slot_list[result]].name+']') #DUBTE
								player.inventory.food[slot_list[result]] = deepcopy(il.ilist['food'][food_list[result]])
								message.add('+['+player.inventory.food[slot_list[result]].name+']')
							else:
								message.add(l10n.format_value("nevermind"))
														
							run = False
						
					elif ui2 == 'e' and player.inventory.materials.wood < 2:	
						message.add(l10n.format_value("not-enoughwood"))
						run = False
				
					if ui2 == 'b' and player.inventory.materials.wood >= 5:
						sfx.play('flame')
						player.inventory.materials.wood -= 5
						replace = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist['toys'][12])
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
						world.maplist[self.pos[2]][self.on_map].countdowns.append(countdown('hot_furnace',player.pos[0],player.pos[1],10))
						message.add(l10n.format_value("heat-up"))
						run = False
					elif ui2 == 'b' and player.inventory.materials.wood < 5:
						message.add(l10n.format_value("not-enoughwood"))
						run = False
				
				elif ui == 'b':
					hc = container([il.ilist['misc'][8],])
					test = hc.loot(0)
					if test == True:
						sfx.play('pickup')
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
					else:
						message.add('Your inventory is full!') #TIPO1
					run = False
				elif ui == 'x':
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'altar':
			 #this is a altar
			
			run = True
			first_call = True
			
			while run:
				
				if player.difficulty == 0 or player.difficulty == 4: #playing on easy or sandbox
					if gods.judgement() == True:
						pray_string = l10n.format_value("pray-save", {"keyname1": key_name['e']})
					else:
						pray_string = l10n.format_value("pray-notsave", {"keyname1": key_name['e']})
				else:
					pray_string = l10n.format_value("pray", {"keyname1": key_name['e']})
				
				screen.render_request(pray_string, l10n.format_value("altar-identify", {"keyname2": key_name['b']}), l10n.format_value("altar-leave", {"keyname3": key_name['x']}),first_call)
					
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
				first_call = False
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					
					judgement = gods.judgement() # see if the player is supported by the gods
					
					if judgement == True:
						sfx.play('holy')
						cursed_items = 0
						bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck', 'Axe', 'Pickaxe')
						
						for i in bodyparts:#check if player wears some cursed equipment
							
							if player.inventory.wearing[i].cursed < 1 and i != player.inventory.nothing:
								cursed_items += 1
						
						if (player.lp*100)/player.attribute.max_lp < 20:#player has less then 20% of lp -> heal
							player.lp = player.attribute.max_lp
							message.add(l10n.format_value("gods-heal"))
							gods.mood -= 10
							run = False
							
						elif (player.attribute.hunger*100)/player.attribute.hunger_max < 20 or (player.attribute.thirst*100)/player.attribute.thirst_max < 20 or (player.attribute.tiredness*100)/player.attribute.tiredness_max < 20:
							#player is very hungry,thirsty or tired -> refresh
							player.attribute.hunger = player.attribute.hunger_max
							player.attribute.thirst = player.attribute.thirst_max
							player.attribute.tiredness = player.attribute.tiredness_max
							message.add(l10n.format_value("gods-refresh"))
							gods.mood -= 10
							run = False
							
						elif cursed_items > 0:#player has some cursed items
							
							bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck', 'Axe', 'Pickaxe')
							
							for j in bodyparts:
								
								if player.inventory.wearing[j].cursed  < 1 and player.inventory.wearing[j] != player.inventory.nothing:
									item = item_wear(player.inventory.wearing[j].classe, player.inventory.wearing[j].material, player.inventory.wearing[j].plus, player.inventory.wearing[j].state, 1, player.inventory.wearing[j].known)
									player.inventory.wearing[j] = item
							
							message.add(l10n.format_value("gods-removecurse"))
							gods.mood -= 10
							run = False
						
						else:
							message.add(l10n.format_value("gods-pleased"))
							run = False
							
					else:
						sfx.play('thunder')
						
						uncursed_items = 0
						bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck','Axe','Pickaxe')
						
						for i in bodyparts:#check if player wears some cursed equipment
							
							if player.inventory.wearing[i].cursed > 0 and player.inventory.wearing[i] != player.inventory.nothing:
								uncursed_items += 1
						
						if uncursed_items > 0:
							
							for j in bodyparts:
								
								if player.inventory.wearing[j].cursed > 0 and player.inventory.wearing[j] != player.inventory.nothing:
									item = item_wear(player.inventory.wearing[j].classe,player.inventory.wearing[j].material,player.inventory.wearing[j].plus, player.inventory.wearing[j].state, 0, player.inventory.wearing[j].known)
									player.inventory.wearing[j] = item
							
							message.add(l10n.format_value("gods-angry"))
							run = False
						else:
							
							player.lp -= 5
							message.add(l10n.format_value("gods-angry2"))
							run = False
				
				
				elif ui == 'b':
					if gods.judgement() == True:
						sfx.play('identify')
						
						num_ident = 0
						bodyparts = ('Hold(R)', 'Hold(L)', 'Head', 'Body', 'Legs', 'Feet', 'Hand', 'Neck', 'Axe', 'Pickaxe')
					
						for i in bodyparts:
						
							if player.inventory.wearing[i] != player.inventory.nothing and player.inventory.wearing[i].known == False:
								player.inventory.wearing[i].identification()
								num_ident += 1
							
						for j in range (0, len(player.inventory.equipment)):
						
							if player.inventory.equipment[j] != player.inventory.nothing and player.inventory.equipment[j].known == False:
								player.inventory.equipment[j].identification()
								num_ident += 1
						if num_ident > 0:	
							message.add(l10n.format_value("awareof-equipment"))
							gods.mood -= num_ident
						else:
							message.add(l10n.format_value("no-identify"))
						run = False
					else:
						sfx.play('thunder')
						message.add(l10n.format_value("gods-noidentify"))
						run = False
					
				elif ui == 'x':
					
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'activate_portal':
			head_string = 'Portal (requires: LVL '+str(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].special_num)+' & '+ str(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_resources[1])+' gems)'
			if player.lvl >= world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].special_num and player.inventory.materials.gem >= world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_resources[1]:
				a_string = '['+key_name['e']+'] - activate'
				activate = True
			else:
				a_string = ' '
				activate = False
			l_string = '['+key_name['x']+'] - leave' #TIPO2
			
			screen.render_request(head_string,a_string,l_string)
			
			run = True
			while run:
				
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e' and activate == True:
					player.inventory.materials.gem -= world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_resources[1]
					if player.inventory.materials.gem < 0:#only to be sure
						player.inventory.materials.gem = 0#
					replace = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace)
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(tl.tlist[world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[0]][world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_tiles[1]])
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace = replace
					sfx.play('portal')
					run = False
					
				if ui == 'x':
					run = False
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'go_grassland':
			screen.render_fade(True,False)
			try:
				pos = world.maplist[0]['local_0_0'].find_first(tl.tlist['portal'][8])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.pos[2] = 0#only to be sure
			except:
				world.grassland_generator(0,0,30,80,5,int((max_map_size*max_map_size)/20))
				world.cave_generator(2)
				world.border_generator(3)
				pos = world.maplist[0]['local_0_0'].find_first(tl.tlist['portal'][8])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.pos[2] = 0#only to be sure
			
			player.on_map = 'local_0_0'
			player.stand_check()
			sfx.play('portal')
			screen.render_fade(False,True)
			
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'return_grassland':
			pos = world.maplist[self.pos[2]]['elysium_0_0'].find_first(tl.tlist['portal'][7])
			screen.render_fade(True,False)
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.pos[2] = 0#only to be sure
			player.on_map = 'elysium_0_0'
			player.stand_check()
			sfx.play('portal')
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'go_fortress':
			screen.render_fade(True,False)
			try:
				pos = world.maplist[0]['fortress_0_0'].find_first(tl.tlist['portal'][2])
			except:
				test = False
				while test == False:
					test = world.elfish_generator(0)
				pos = world.maplist[0]['fortress_0_0'].find_first(tl.tlist['portal'][2])
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.pos[2] = 0#only to be sure
			player.on_map = 'fortress_0_0'
			player.stand_check()
			sfx.play('portal')
			screen.render_fade(False,True)
			
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'return_fortress':
			pos = world.maplist[self.pos[2]]['elysium_0_0'].find_first(tl.tlist['portal'][1])
			screen.render_fade(True,False)
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.pos[2] = 0#only to be sure
			player.on_map = 'elysium_0_0'
			player.stand_check()
			sfx.play('portal')
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'go_desert':
			screen.render_fade(True,False)
			try:
				pos = world.maplist[self.pos[2]]['desert_0_0'].find_first(tl.tlist['portal'][5])
			except:
				world.desert_generator(20)
				world.cave_generator(2,'desert')
				world.border_generator(3,'desert')
				pos = world.maplist[self.pos[2]]['desert_0_0'].find_first(tl.tlist['portal'][5])
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.pos[2] = 0#only to be sure
			player.on_map = 'desert_0_0'
			player.stand_check()
			sfx.play('portal')
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'return_desert':
			pos = world.maplist[self.pos[2]]['elysium_0_0'].find_first(tl.tlist['portal'][4])
			screen.render_fade(True,False)
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.pos[2] = 0#only to be sure
			player.on_map = 'elysium_0_0'
			player.stand_check()
			sfx.play('portal')
			screen.render_fade(False,True)
								
		elif world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]] != 0:#interaction with a container eg.: a chest
			world.maplist[self.pos[2]][self.on_map].containers[self.pos[1]][self.pos[0]].inventory()
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grassland_down':#this is a grassland dungeon stair down
			screen.render_fade(True,False)
			plus = world.maplist[self.pos[2]][self.on_map].monster_plus
			pos = False
			while pos == False:
				if plus < 4:
					world.dungeon_generator(plus+1,True)
				else:
					world.dungeon_generator(plus+1,False)
				
				if player.on_map != 'dungeon_0_0':
					player.last_z = player.pos[2]
				
				player.on_map = 'dungeon_0_0'
				player.pos[2] = 1
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][8])
			
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grassland_up':#this is a grassland dungeon stair up
			choose = screen.get_choice('Do you want to leave?',['No','Yes'],True) #TIPO1
			if choose == 1:
				screen.render_fade(True,False)
				player.on_map = 'local_0_0'
				player.pos[2] = 0
				
				if player.pet_pos != False and player.pet_on_map != False and player.pet_on_map != player.on_map:
					world.maplist[0]['elysium_0_0'].npcs[0][0] = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]])
					player.pet_pos = [0,0,0]
					player.pet_on_map = 'elysium_0_0'
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][7])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
				screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'tomb_down':#this is a tomb stair down
			screen.render_fade(True,False)
			plus = world.maplist[self.pos[2]][self.on_map].monster_plus
			pos = False
			while pos == False:
				if plus < 12:
					world.dungeon_generator(plus+1,stair_down=True,style='Tomb')
				else:
					world.dungeon_generator(plus+1,stair_down=False,style='Tomb')
			
				if player.on_map != 'dungeon_0_0':
					player.last_z = player.pos[2]
				
				player.on_map = 'dungeon_0_0'
				player.pos[2] = 1
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][19])
			
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'tomb_up':#this is a grassland dungeon stair up
			choose = screen.get_choice('Do you want to leave?',['No','Yes'],True)
			if choose == 1:
				screen.render_fade(True,False)
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				if player.pet_pos != False and player.pet_on_map != False and player.pet_on_map != player.on_map:
					world.maplist[0]['elysium_0_0'].npcs[0][0] = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]])
					player.pet_pos = [0,0,0]
					player.pet_on_map = 'elysium_0_0'
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][18])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
				screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grot_down':#this is a grassland dungeon stair down
			screen.render_fade(True,False)
			pos = False
			while pos == False:
				plus = world.grot_generator(1)
				if player.on_map != 'dungeon_0_1':
					player.last_z = player.pos[2]
				player.on_map = 'dungeon_0_1'
				player.pos[2] = 1
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][15])
			
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'grot_up':#this is a grot stair up
			choose = screen.get_choice('Do you want to leave?',['No','Yes'],True)
			if choose == 1:
				screen.render_fade(True,False)
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				if player.pet_pos != False and player.pet_on_map != False and player.pet_on_map != player.on_map:
					world.maplist[0]['elysium_0_0'].npcs[0][0] = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]])
					player.pet_pos = [0,0,0]
					player.pet_on_map = 'elysium_0_0'
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][14])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
				screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'sewer_down':#this is a sewer stair down
			screen.render_fade(True,False)
			pos = False
			while pos == False:
				plus = world.sewer_generator(1)
				if player.on_map != 'dungeon_0_1':
					player.last_z = player.pos[2]
				player.on_map = 'dungeon_0_1'
				player.pos[2] = 1
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['sewer'][4])
			
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'sewer_up':#this is a sewer stair up
			choose = screen.get_choice('Do you want to leave?',['No','Yes'],True)
			if choose == 1:
				screen.render_fade(True,False)
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				if player.pet_pos != False and player.pet_on_map != False and player.pet_on_map != player.on_map:
					world.maplist[0]['elysium_0_0'].npcs[0][0] = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]])
					player.pet_pos = [0,0,0]
					player.pet_on_map = 'elysium_0_0'
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['sewer'][3])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
				screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'mine_down':#this is a mine stair down
			screen.render_fade(True,False)
			pos = False
			while pos == False:
				plus = world.mine_generator(1)
				if player.on_map != 'dungeon_0_1':
					player.last_z = player.pos[2]
				player.on_map = 'dungeon_0_1'
				player.pos[2] = 1
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][17])
			
			player.pos[0] = pos[0]
			player.pos[1] = pos[1]
			player.stand_check()
			screen.render_fade(False,True)
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'mine_up':#this is a mine stair up
			choose = screen.get_choice('Do you want to leave?',['No','Yes'],True)
			if choose == 1:
				screen.render_fade(True,False)
				player.on_map = player.last_map
				player.pos[2] = player.last_z
				
				if player.pet_pos != False and player.pet_on_map != False and player.pet_on_map != player.on_map:
					world.maplist[0]['elysium_0_0'].npcs[0][0] = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]])
					player.pet_pos = [0,0,0]
					player.pet_on_map = 'elysium_0_0'
				
				pos = world.maplist[player.pos[2]][player.on_map].find_first(tl.tlist['dungeon'][16])
				player.pos[0] = pos[0]
				player.pos[1] = pos[1]
				player.stand_check()
				screen.render_fade(False,True)
				
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'loot':
			message.add('You find nothing interesting.') #TIPO1
			if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace != None:
				world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace)	
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'gilmenor_portal':#gilmenor's escape portal
			if player.pet_pos != False and player.pet_on_map != False:
				if world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].personal_id == 'gilmenor':
					screen.render_request('[Gilmenor]','We have made it! Thank you so much!','Let\'s meet at the elysium.',False,portrait='gilmenor_happy') #TIPO1
					ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
					screen.write_hit_matrix(player.pet_pos[0],player.pet_pos[1],7)
					sfx.play('teleport')
					world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]] = 0
					pos = world.maplist[0]['elysium_0_0'].find_first(tl.tlist['functional'][18])
					world.maplist[0]['elysium_0_0'].npcs[pos[1]][pos[0]] = deepcopy(ml.mlist['rescued'][1])
					world.maplist[0]['elysium_0_0'].set_monster_strength(pos[0],pos[1],0)
					player.pet_pos = False
					player.pet_on_map = False
					player.quest_variables.append('gilmenor_rescued')
		
		elif world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].use_group == 'switch':#using a switch
			
			screen.render_request('['+key_name['e']+'] - use switch','['+key_name['b']+'] - take switch','['+key_name['x']+'] - chancel') #TIPO2
			run = True
			while run:
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					run = False
					world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = deepcopy(world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]])
					if world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].tile_pos == (14,6):
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].tile_pos = (14,7)
					else:
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].tile_pos = (14,6)
					sfx.play('lever')
					world.maplist[self.pos[2]][self.on_map].set_signal(self.pos[0],self.pos[1])
				elif ui == 'b':
					run = False
					hc = container([world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].conected_items,])
					test = hc.loot(0,True)
					if test == True:
						sfx.play('pickup')
						world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]] = world.maplist[self.pos[2]][self.on_map].tilemap[self.pos[1]][self.pos[0]].replace
				elif ui == 'x':
					run = False
		
		else:
			wait_10m = l10n.format_value("wait1", {"waitkey1": key_name['e']})
			wait_30m = l10n.format_value("wait2", {"waitkey2": key_name['b']})
			wait_1h = l10n.format_value("wait3", {"waitkey3": key_name['i']})
			screen.render_request(wait_10m,wait_30m,wait_1h)
			
			run = True
			while run:
				turns = 0
				
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
				if ui == 'exit':
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'e':
					turns = 9
					run = False
				elif ui == 'b':
					run = False
					turns = 29
				elif ui == 'i':
					turns = 59
					run = False
				elif ui == 'x':
					return
				
				if turns > 0:
					old_lp = player.lp
					while turns > 0:
						old_lp = player.lp
						hostile_count = 0
						
						for my in range(player.pos[1]-2,player.pos[1]+3):
							for mx in range(player.pos[0]-2,player.pos[0]+3):
								try:
									if world.maplist[self.pos[2]][self.on_map].npcs[my][mx] != 0:
										if world.maplist[self.pos[2]][self.on_map].npcs[my][mx].AI_style == 'hostile':
											hostile_count += 1
								except:
									None
								
						
						if (player.attribute.hunger*100)/player.attribute.hunger_max < 10:
							message.add(l10n.format_value("hungry-wait"))
							return
						elif (player.attribute.thirst*100)/player.attribute.thirst_max < 10:
							message.add(l10n.format_value("thirsty-wait"))
							return
						elif (player.attribute.tiredness*100)/player.attribute.tiredness_max < 10:
							message.add(l10n.format_value("tired-wait"))
							return
						elif hostile_count == 1:
							message.add(l10n.format_value("interupted-wait"))
							return
						elif hostile_count > 1:
							message.add(l10n.format_value("interupted-wait2"))
							return
						
						time.tick()
						screen.write_hit_matrix(player.pos[0],player.pos[1],24)
						if time.minute == 0 or time.minute%2 == 0:
							screen.render(0)
						sleep(0.01)
						if player.lp < old_lp:
							message.add(l10n.format_value("hurt-wait"))
							return
						turns -= 1
						
					message.add(l10n.format_value("finished-wait"))
					screen.reset_hit_matrix()
					screen.render(0)
			
			#message.add('There is nothing to interact with at this place.')
			
class player_class(mob):
	
	def __init__(self, name, on_map, attribute, inventory, pos =[10,10,0], build='Manual'):
		
		lname = save_path + os.sep + 'player.data'
		
		try:
			
			mob.__init__(self, name, on_map, attribute, pos)
			
			f = open(lname, 'rb')
			screen.render_load(7)
			temp = p.load(f)
			
			self.name = temp.name
			self.on_map = temp.on_map
			
			self.gender = temp.gender
			self.style = temp.style
			self.difficulty = temp.difficulty
			
			#attribute
			self.attribute.p_strength = temp.attribute.p_strength
			self.attribute.p_defense = temp.attribute.p_defense
			self.attribute.m_strength = temp.attribute.m_strength
			self.attribute.m_defense = temp.attribute.m_defense
			self.attribute.luck = temp.attribute.luck
			self.attribute.max_lp = temp.attribute.max_lp
			self.attribute.max_mp = temp.attribute.max_mp
			self.lp = temp.lp
			self.mp = temp.mp
			self.attribute.hunger_max = temp.attribute.hunger_max
			self.attribute.hunger = temp.attribute.hunger
			self.attribute.thirst_max = temp.attribute.thirst_max
			self.attribute.thirst = temp.attribute.thirst
			self.attribute.tiredness_max = temp.attribute.tiredness_max
			self.attribute.tiredness = temp.attribute.tiredness
			self.attribute.pickaxe_power = temp.attribute.pickaxe_power
			try:
				self.lp_boost = temp.lp_boost
			except:
				self.lp_boost = 1
			
			self.inventory = temp.inventory
			self.pos = [int(temp.pos[0]),int(temp.pos[1]),int(temp.pos[2])]
			
			self.buffs = temp.buffs
			self.xp = temp.xp
			self.lvl = temp.lvl
			
			self.cur_map = temp.cur_map
			self.last_map = temp.last_map
			self.cur_z = temp.cur_z
			self.last_z = temp.last_z
			self.last_lp = temp.lp
			self.save_pos = temp.save_pos
			
			self.activ_quests = temp.activ_quests
			self.quest_variables = temp.quest_variables
			
			self.pet_pos = temp.pet_pos
			self.pet_on_map = temp.pet_on_map
			self.pet_lp = temp.pet_lp
			
			self.skill = temp.skill
			self.villager = temp.villager
			self.godmode = temp.godmode
			self.lost_lp = temp.lost_lp
			try:
				self.coins = temp.coins
			except:
				self.coins = 10
			
			try:
				self.questlog = temp.questlog
			except:
				self.questlog = questlog()
			
			try:
				self.training_attack = temp.training_attack
				self.training_def = temp.training_def
			except:
				self.training_attack  = 50
				self.training_def = 50
			
		except:
			self.pos[2] = 0
			if build == 'Manual':
				accept = False
				while accept == False:
				
					num = 0
					gender_list = ('FEMALE','MALE')
					run = True
					
					if low_res == False:
						marker_y = 115
					else:
						marker_y = 46
					
					while run:
					
						if low_res == False:
							s = pygame.Surface((640,360))
						else:
							s = pygame.Surface((320,240))
				
						bg = pygame.Surface((480,360))
						bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
						if low_res == True:
							bg = pygame.transform.scale(bg,(320,240))

						s.blit(bg,(0,0))
				
						text_image = screen.font.render(l10n.format_value("choose-gender"),1,(255,255,255))
						s.blit(text_image,(5,2))#menue title
				
						s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
						for i in range (0,2): 
							string = gender_list[i]
							text_image = screen.font.render(string,1,(0,0,0))
							s.blit(text_image,(21,(marker_y+5)+i*25))#blit item names
						
						text = l10n.format_value("choose-gender2", {"gender1": key_name['e']})
						text_image = screen.font.render(text,1,(255,255,255))
						if low_res == False:
							s.blit(text_image,(5,335))
						else:
							s.blit(text_image,(2,225))
					
						if game_options.mousepad == 1 and low_res == False:
							s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
						else:
							s_help = pygame.Surface((160,360))
							s_help.fill((48,48,48))
							s.blit(s_help,(480,0))
					
						if game_options.mousepad == 0 and low_res == False:
							s_help = pygame.Surface((640,360))
							s_help.fill((48,48,48))
							s_help.blit(s,(80,0))
							s = s_help
						
						if low_res == False:
							s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
						screen.screen.blit(s,(0,0))
					
						pygame.display.flip()
					
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
						if ui == 's':
							num += 1
							if num > 1:
								num = 0
						
						if ui == 'w':
							num -= 1
							if num < 0:
								num = 1
						
						if ui == 'e':
							self.gender = gender_list[num]
							run = False
					
					run2 = True
					num2 = 0
				
					while run2:
						
						if low_res == False:
							s = pygame.Surface((640,360))
						else:
							s = pygame.Surface((320,240))
				
						bg = pygame.Surface((480,360))
						bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
						if low_res == True:
							bg = pygame.transform.scale(bg,(320,240))

						s.blit(bg,(0,0))
						
						text_image = screen.font.render(l10n.format_value("choose-style"),1,(255,255,255))
						s.blit(text_image,(5,2))#menue title
				
						s.blit(gra_files.gdic['display'][4],(0,marker_y+num2*32))#blit marker
				
						for i in range (1,5): 
							skinstring = 'SKIN_' + self.gender + '_' + str(i)
							hairstring = 'HAIR_' + self.gender + '_' +  str(i)
							underwearstring = self.gender + '_underwear'
							s.blit(gra_files.gdic['char'][skinstring],(26,marker_y+(i-1)*32))
							s.blit(gra_files.gdic['char'][hairstring],(26,marker_y+(i-1)*32))
							s.blit(gra_files.gdic['char'][underwearstring],(26,marker_y+(i-1)*32))
						
						text = l10n.format_value("choose-gender2", {"gender1": key_name['e']})
						text_image = screen.font.render(text,1,(255,255,255))
						if low_res == False:
							s.blit(text_image,(5,335))
						else:
							s.blit(text_image,(2,225))
					
						if game_options.mousepad == 1 and low_res == False:
							s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
						else:
							s_help = pygame.Surface((160,360))
							s_help.fill((48,48,48))
							s.blit(s_help,(480,0))
					
						if game_options.mousepad == 0 and low_res == False:
							s_help = pygame.Surface((640,360))
							s_help.fill((48,48,48))
							s_help.blit(s,(80,0))
							s = s_help
						
						if low_res == False:
							s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
						screen.screen.blit(s,(0,0))
					
						pygame.display.flip()
				
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
						if ui == 's':
							num2 += 1
							if num2 > 3:
								num2 = 0
						
						if ui == 'w':
							num2 -= 1
							if num2 < 0:
								num2 = 3
						
						if ui == 'e':
							self.style = num2
							run2 = False
					
					ask_punishment = True
					d_choice = screen.get_choice(l10n.format_value("choose-gamemode"),(l10n.format_value("choose-gamemode1"),l10n.format_value("choose-gamemode2"),l10n.format_value("choose-gamemode3")),False,infos=(l10n.format_value("gamemode1-text"),l10n.format_value("gamemode2-text"),l10n.format_value("gamemode3-text")))
					if d_choice == 0:
						self.lp_boost = 2
					elif d_choice == 1:
						self.lp_boost = 1
					else:
						self.lp_boost = 2
						ask_punishment = False
						self.difficulty = 4
					
					if ask_punishment == True:
						num3 = 0
						dificulty_list = (l10n.format_value("difficulty1"),l10n.format_value("difficulty2"),l10n.format_value("difficulty3"),l10n.format_value("difficulty4"))
						description_list = (l10n.format_value("difficulty1-text"),l10n.format_value("difficulty2-text"),l10n.format_value("difficulty3-text"),l10n.format_value("difficulty4-text")) 
						run3 = True
			
						while run3:
							
							s = pygame.Surface((640,360))
				
							bg = pygame.Surface((480,360))
							bg.blit(gra_files.gdic['display'][1],(0,0)) #render background

							s.blit(bg,(0,0))
						
							text_image = screen.font.render(l10n.format_value("choose-punishment"),1,(255,255,255))
							s.blit(text_image,(5,2))#menue title
				
							s.blit(gra_files.gdic['display'][4],(0,marker_y+num3*25))#blit marker
				
							for i in range (0,4): 
								string = dificulty_list[i]
								text_image = screen.font.render(string,1,(0,0,0))
								s.blit(text_image,(21,(marker_y+5)+i*25))#blit item names
					
								text_image = screen.font.render(description_list[num3],1,(255,255,255))
							
							s.blit(text_image,(5,335))
						
							if game_options.mousepad == 1:
								s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
							else:
								s_help = pygame.Surface((160,360))
								s_help.fill((48,48,48))
								s.blit(s_help,(480,0))
					
							if game_options.mousepad == 0:
								s_help = pygame.Surface((640,360))
								s_help.fill((48,48,48))
								s_help.blit(s,(80,0))
								s = s_help
						
							s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
							screen.screen.blit(s,(0,0))
					
							pygame.display.flip()
					
							ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
							if ui == 's':
								num3 += 1
								if num3 > 3:
									num3 = 0
						
							if ui == 'w':
								num3 -= 1
								if num3 < 0:
									num3 = 3
						
							if ui == 'e':
								self.difficulty = num3
								run3 = False
					
					if self.gender == 'MALE':
						name = screen.string_input(l10n.format_value("name-gender"),15,'male')
					else:
						name = screen.string_input(l10n.format_value("name-gender"),15,'female')
					
					if name == '':
						name = l10n.format_value("no-name")
						
					self.godmode = False
				
					num4 = 0
					choose_list = (l10n.format_value("yes"),l10n.format_value("no")) 
					run4 = True
					
					if low_res == False:
						char_x = 160
					else:
						char_x = 60
											
					while run4:
					
						if low_res == False:
							s = pygame.Surface((640,360))
						else:
							s = pygame.Surface((320,240))
				
						bg = pygame.Surface((480,360))
						bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
						if low_res == True:
							bg = pygame.transform.scale(bg,(320,240))

						s.blit(bg,(0,0))
						
						text_image = screen.font.render(l10n.format_value("everything-alright"),1,(255,255,255))
						s.blit(text_image,(5,2))#menue title
					
						skinstring = 'SKIN_' + self.gender + '_' + str(self.style +1)
						s.blit(gra_files.gdic['char'][skinstring],(char_x,80))
						
						underwearstring = self.gender + '_underwear'
						s.blit(gra_files.gdic['char'][underwearstring],(char_x,80))
						
						hairstring = 'HAIR_' + self.gender + '_' + str(self.style +1)
						s.blit(gra_files.gdic['char'][hairstring],(char_x,80))
					
						n_string = 'NAME: ' + name
						name_image = screen.font.render(n_string,1,(0,0,0))
						s.blit(name_image,(char_x,120))
					
						if self.difficulty == 4:
							gm_string = 'Gamemode: Sandbox'
						elif self.lp_boost == 1:
							gm_string = 'Gamemode: Expert'
						else:
							gm_string = 'Gamemode: Normal'
							
						name_image = screen.font.render(gm_string,1,(0,0,0))
						s.blit(name_image,(char_x,140))
						
						d_list = ('Low', 'Medium', 'High', 'Rougelike', '-')
						
						d_string = 'Punishment: ' + d_list[self.difficulty]
						name_image = screen.font.render(d_string,1,(0,0,0))
						s.blit(name_image,(char_x,160))
					
						s.blit(gra_files.gdic['display'][4],(char_x-5,180+num4*25))#blit marker
				
						for i in range (0,2): 
							string = choose_list[i]
							text_image = screen.font.render(string,1,(0,0,0))
							s.blit(text_image,(char_x+16,185+i*25))#blit item names
						
						text = l10n.format_value("choose-gender2", {"gender1": key_name['e']})
						text_image = screen.font.render(text,1,(255,255,255))
						s.blit(text_image,(5,335))
						
						if game_options.mousepad == 1:
							s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
						else:
							s_help = pygame.Surface((160,360))
							s_help.fill((48,48,48))
							s.blit(s_help,(480,0))
					
						if game_options.mousepad == 0:
							s_help = pygame.Surface((640,360))
							s_help.fill((48,48,48))
							s_help.blit(s,(80,0))
							s = s_help
						
						s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
						
						screen.screen.blit(s,(0,0))
					
						pygame.display.flip()
					
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
						if ui == 's':
							num4 += 1
							if num4 > 1:
								num4 = 0
						
						if ui == 'w':
							num4 -= 1
							if num4 < 0:
								num4 = 1
						
						if ui == 'e':
						
							if num4 == 0:
								accept = True
							
							run4 = False
						
				if self.difficulty == 4:
				
					for i in range (0,len(world.maplist)-1):
					
						for y in range(0,max_map_size):
							for x in range(0,max_map_size):
								try:
									if world.maplist[i]['local_0_0'].npcs[y][x] != 0:
										world.maplist[i]['local_0_0'].npcs[y][x].AI_style = 'ignore'
								except:
									None
								try:	
									if world.maplist[i]['desert_0_0'].npcs[y][x] != 0:
										world.maplist[i]['desert_0_0'].npcs[y][x].AI_style = 'ignore'
								except:
									None
					
			###############
			mob.__init__(self, name, on_map, attribute, pos)
			
			self.skill = skill()
			self.inventory = inventory
			
			self.training_attack  = 50
			self.training_def = 50
			
			self.xp = 0
			self.lvl = 0
			self.last_lp = self.lp
			
			self.buffs = buffs()
			
			self.activ_quests = []
			self.quest_variables = []
			
			self.pet_pos = False
			self.pet_on_map = False
			self.pet_lp = 0
			
			try:
				self.lp *= self.lp_boost
				self.attribute.max_lp *= self.lp_boost
			except:
				self.lp_boost = 1
			
			self.lost_lp = 0
			
			self.coins = 10
			
			self.questlog = questlog()
			
			self.villager = {'high' : [], 'medium' : [], 'low' : []}
			
			try:
				self.pos[0] = world.startx
				self.pos[1] = world.starty
			except:
				self.pos[0] = 0
				self.pos[1] = 0
			
			self.save_pos = (self.pos[0],self.pos[1],self.pos[2],self.on_map)
			
			screen.render_load(5)
	
	def make_grave(self):
		
		if self.difficulty == 4:
			return True
		
		count = 0
		found_location = False
		
		#0: Check if player can drop something
		slots = ('Hold(R)','Hold(L)','Head','Body','Legs','Feet','Neck','Hand')
		slots_token = []
		for i in slots:
			if self.inventory.wearing[i] != self.inventory.nothing:
				slots_token.append(i)
		if len(slots_token) == 0:#the player has nothing dropable equiped
			return True
		
		#1: Find location
		while found_location == False:
			for y in range(self.pos[1]-count,self.pos[1]+count+1):
				for x in range(self.pos[0]-count,self.pos[0]+count+1):
					try:
						t_move_group = world.maplist[self.pos[2]][self.on_map].tilemap[y][x].move_group
						t_replace = world.maplist[self.pos[2]][self.on_map].tilemap[y][x].replace
						t_use_group = world.maplist[self.pos[2]][self.on_map].tilemap[y][x].use_group
						if t_move_group == 'soil' and t_replace == None and found_location == False and t_use_group == 'None':
							found_location = (x,y)
						count += 1
						if count > max_map_size:
							return False
					except:
						None
		
		#2:Set tile
		replace = world.maplist[self.pos[2]][self.on_map].tilemap[found_location[1]][found_location[0]]
		world.maplist[self.pos[2]][self.on_map].tilemap[found_location[1]][found_location[0]] = deepcopy(tl.tlist['functional'][27])
		world.maplist[self.pos[2]][self.on_map].tilemap[found_location[1]][found_location[0]].replace = replace
		world.maplist[self.pos[2]][self.on_map].tilemap[found_location[1]][found_location[0]].move_mes = '[R.I.P '+self.name+']' #DUBTE
		
		#3:Drop items
		item_list = []
		if self.difficulty == 0:#easy-mode
			num_items = 2
		elif self.difficulty == 1:#normal-mode
			num_items = 4
		else:
			num_items = 6
			
		if len(slots_token) > num_items:
			for j in range(0,num_items):
				try:
					ran = random.randint(0,len(slots_taken)-1)
				except:
					ran = 0
					
				item_list.append(self.inventory.wearing[slots_token[ran]])
				self.inventory.wearing[slots_token[ran]] = self.inventory.nothing
				del slots_token[ran]
		else:
			for j in slots_token:
				item_list.append(self.inventory.wearing[j])
				self.inventory.wearing[j] = self.inventory.nothing
		
		world.maplist[self.pos[2]][self.on_map].containers[found_location[1]][found_location[0]] = container(item_list,True)
		
		#4:Spawn ghost
		if self.difficulty == 1:#normal-mode
			chance = 25
		elif self. difficulty == 2:#hard-mode
			chance = 75
		else:
			chance = 0
			
		ran2 = random.randint(0,99)
		
		if chance > ran2 and player.on_map != 'dundeon_0_0':
			world.maplist[self.pos[2]][self.on_map].npcs[found_location[1]][found_location[0]] = deepcopy(ml.mlist['special'][9])
			world.maplist[self.pos[2]][self.on_map].set_monster_strength(found_location[0],found_location[1],player.lvl,None,1)
			world.maplist[self.pos[2]][self.on_map].npcs[found_location[1]][found_location[0]].lp += 5
		
	def user_input(self,immobilized=False):
		
		ui = getch(screen.displayx,screen.displayy,0,game_options.turnmode,mouse=game_options.mousepad)
		
		if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
		
		if immobilized == True:
			if ui != 'x':
				ui = 'none'
		
		if ui == 'w':
			if screen.fire_mode == 0:
				self.move(0,-1)
				time.tick()
			else:
				self.player_fire((0,-1),screen.fire_mode)
				screen.fire_mode = 0
				time.tick()
			
		if ui == 's':
			if screen.fire_mode == 0:
				self.move(0,1)
				time.tick()
			else:
				self.player_fire((0,1),screen.fire_mode)
				screen.fire_mode = 0
				time.tick()
			
		if ui == 'a':
			if screen.fire_mode == 0:
				self.move(-1,0)
				time.tick()
			else:
				self.player_fire((-1,0),screen.fire_mode)
				screen.fire_mode = 0
				time.tick()
			
		if ui == 'd':
			if screen.fire_mode == 0:
				self.move(1,0)
				time.tick()
			else:
				self.player_fire((1,0),screen.fire_mode)
				screen.fire_mode = 0
				time.tick()
			
		if ui == 'e':
			if screen.fire_mode == 0:
				self.enter()
				time.tick()
		
		if ui == 'i':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction()
				time.tick()
				
		if ui == '1':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction()
				time.tick()
		
		if ui == '2':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction(1)
				time.tick()
				
		if ui == '3':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction(2)
				time.tick()
		
		if ui == '4':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction(3)
				time.tick()
				
		if ui == '5':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction(4)
				time.tick()
				
		if ui == '6':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction(5)
				time.tick()
				
		if ui == '7':
			if screen.fire_mode == 0:
				sfx.play('loot')
				screen.render_fade(False,True,'inventory')
				self.inventory.inv_user_interaction(6)
				time.tick()
		
		if ui == 'q':
			screen.render_questlog()
			
		if ui == 'c':
			screen.render_status()
			
		if ui == 't':
			player.inventory.find_use_name('throw')
		
		if ui == 'r':
			player.inventory.find_use_name('read')
			
		if ui == 'b':
			if screen.fire_mode == 0:
				if world.maplist[self.pos[2]][self.on_map].build_type != 'None':
					if self.pet_pos != False and self.pet_on_map != False:
						world.maplist[0]['elysium_0_0'].npcs[0][0] = deepcopy(world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]])
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]] = 0
						#self.pet_pos = [0,0,0]
						#self.pet_on_map = 'elysium_0_0'
					self.built()
					if self.pet_pos != False and self.pet_on_map != False:
						world.maplist[self.pet_pos[2]][self.pet_on_map].npcs[self.pet_pos[1]][self.pet_pos[0]] = deepcopy(world.maplist[0]['elysium_0_0'].npcs[0][0]) 
						world.maplist[0]['elysium_0_0'].npcs[0][0] = 0
					time.tick()
				else:
					message.add(l10n.format_value("cant-build"))
		
		if ui == 'f':
			if screen.fire_mode == 0:
				if player.mp >= 2:
					if player.inventory.wearing['Hold(L)'] != player.inventory.nothing:
						screen.fire_mode = 1
						message.add(l10n.format_value("magic-powers"))
					else:
						message.add(l10n.format_value("magic-need"))
				else:
					message.add(l10n.format_value("magic-not"))
			
		if ui == 'x':
			if screen.fire_mode == 0:
				screen.render_fade(False,True,'brake')
				screen.render_brake()
			else:
				screen.fire_mode = 0
		
		if ui == '.':
			screen.write_hit_matrix(player.pos[0],player.pos[1],24)
			time.tick()
		
		if ui == 'TAB' and cheat_mode == True:
			sfx.play('loot')
			if sys.version_info < (3,0):
				ui = raw_input('>')
			else:
				ui = input('>')
			try:
				if ui.find('cheat') != -1:
					help_ui = ui.replace('cheat ','')
					help_file = open(help_ui,"r")
					commands = help_file.read()
					exec(commands)
					print('Execution done!') #TIPO1
				else:
					exec(ui)
			except:
				print('[EXECUTION ERROR]')
			
		if ui == 'none':
			time.tick()
			player.stand_check()
	
	def skill_up(self):
		
		string_list = []
		skill_list = []
		up_dict = {'Novice':'Adept','Adept':'Master'}
		
		if self.skill.weapon_crafting != 'Master':
			 string_list.append('Weapon Crafting ('+self.skill.weapon_crafting+' -> '+up_dict[self.skill.weapon_crafting]+')')
			 skill_list.append('weapon crafting')
		if self.skill.metallurgy != 'Master':
			string_list.append('Metallurgy ('+self.skill.metallurgy+' -> '+up_dict[self.skill.metallurgy]+')')
			skill_list.append('metallurgy')
		if self.skill.alchemy != 'Master':
			string_list.append('Alchemy ('+self.skill.alchemy+' -> '+up_dict[self.skill.alchemy]+')')
			skill_list.append('alchemy')
			
		if len(skill_list) == 0:
			return 'No skills to improve!' #TIPO1
		elif len(skill_list) == 1:
			player.skill.raise_skill(skill_list[0])
			return 'Improved skill: '+skill_list[0].title()
		else:
			ui = screen.get_choice('Choose a skill to improve!',string_list,False)
			player.skill.raise_skill(skill_list[ui])
			return 'Improved skill: '+skill_list[ui].title()
			
	def lvl_up(self):
		
		sfx.play('lvl_up')
		screen.render_lvl_up()
		
		self.lvl += 1
		self.xp = max(0,self.xp-100)
		
		if self.inventory.materials.wood_max < 200:
			self.inventory.materials.wood_max += 10
			if self.inventory.materials.wood_max > 200:
				self.inventory.materials.wood_max = 200
		
		if self.inventory.materials.stone_max < 200:
			self.inventory.materials.stone_max += 10
			if self.inventory.materials.stone_max > 200:
				self.inventory.materials.stone_max = 200
		
		if self.inventory.materials.ore_max < 30:
			self.inventory.materials.ore_max += 1
			if self.inventory.materials.ore_max > 30:
				self.inventory.materials.ore_max = 30
		
		if self.inventory.materials.herb_max < 30:
			self.inventory.materials.herb_max += 1
			if self.inventory.materials.herb_max > 30:
				self.inventory.materials.herb_max = 30
				
		if self.inventory.materials.gem_max < 30:
			self.inventory.materials.gem_max += 1
			if self.inventory.materials.gem_max > 30:
				self.inventory.materials.gem_max = 30		
		
		if self.attribute.max_lp < 30*self.lp_boost:
			self.attribute.max_lp += self.lp_boost
			
		if self.training_attack <= 50:
			self.attribute.m_strength += 1
			message.add('Your magic powers are increasing!')
		else:
			self.attribute.p_strength += 1
			message.add('You feel stronger!')
			
		if self.training_def <= 50:
			self.attribute.m_defense += 1
			message.add('Your will is increasing!') #TIPO1
		else:
			self.attribute.p_defense += 1
			message.add('You feel handier!')
			
		player.training_attack = 50
		player.training_def = 50
		
	def built(self):
		
		if world.maplist[self.pos[2]][self.on_map].build_type == 'Part':
			styles = ('Room','Doorway','Door','Agricultur','remove') #DUBTE
		else:
			styles = ('Room','Doorway','Door','Stair up','Stair down','Agriculture','remove')
		try:
			style = styles[screen.get_choice('What dou you like to build?',styles,True)]
		except:
			message.add('You can\'t build here!')
			return False
		
		if style == 'Room':
			xymin = 1
		else:
			xymin = 0
		
		xymax = 6
		
		xmin = xymin
		xmax = xymin
		ymin = xymin
		ymax = xymin
		
		run = True
		
		while run:
			
			res_need = screen.render_built(xmin,xmax,ymin,ymax,style)
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w':
				
				if style != 'Door' and style != 'Stair up' and style != 'Stair down' and style != 'Doorway' and style != 'remove':
					if player.pos[1]-ymin > 0:
						ymin += 1
				
					if ymin >= xymax:
						ymin = xymin
				
				else:
					if ymin >= -3 and player.pos[1]+ymin > 0:
						ymin -= 1
					
			if ui == 's':
				
				if style != 'Door' and style != 'Stair up' and style != 'Stair down' and style != 'Doorway'  and style != 'remove':
					if player.pos[1]+ymax < max_map_size-1:
						ymax += 1
				
					if ymax >= xymax:
						ymax = xymin
					
				else:
					if ymin <= 3 and player.pos[1]+ymin < max_map_size-1:
						ymin += 1
					
			if ui == 'a':
				if style != 'Door' and style != 'Stair up' and style != 'Stair down'and style != 'Doorway'  and style != 'remove':
					if player.pos[0]-xmin > 0:
						xmin += 1
				
					if xmin >= xymax:
						xmin = xymin
						
				else:
					if xmin >= -4 and player.pos[0]+xmin > 0:
						xmin -= 1
					
			if ui == 'd':
				if style != 'Door' and style != 'Stair up' and style != 'Stair down' and style != 'Doorway' and style != 'remove':
					if player.pos[0]+xmax < max_map_size-1:
						xmax += 1
				
					if xmax >= xymax:
						xmax = xymin
				
				else:
					if xmin <= 4 and player.pos[0]+xmin < max_map_size-1:
						xmin += 1
					
			if ui == 'e':
				if style == 'Room':
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone and res_need != (0,0):
						sfx.play('place')
						player.inventory.materials.wood -= res_need[0]
						player.inventory.materials.stone -= res_need[1]
					
						for y in range (-ymin,ymax+1):
							for x in range (-xmin,xmax+1):
				
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
									built_here = True
								elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
									built_here = True
								else: 
									built_here = False
									
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
									built_here = False
								
								if world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] != 0:
									built_here = False
								
								if built_here == True:
									
									world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+y][player.pos[0]+x] = 0 #first of all erase all items that are at this pos
									
									if x == xmax or x == -xmin or y == ymax or y == -ymin:
										if x == xmax or x == -xmin:
												world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist[player.inventory.blueprint.place_cat][player.inventory.blueprint.place_num+1] #set a wall here
					
										if y == ymax or y == -ymin:
												world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist[player.inventory.blueprint.place_cat][player.inventory.blueprint.place_num+1] #set a wall here
									else:
										world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist[player.inventory.blueprint.place_cat][player.inventory.blueprint.place_num]
					else:
						if res_need == (0,0):
							message.add('You can\'t build this here.')
						else:
							message.add('Not enough Resources.')
				
				elif style == 'Doorway':
					
					sfx.play('place')
					player.inventory.materials.wood -= res_need[0]
					player.inventory.materials.stone -= res_need[1]
						
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'solid' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] == 0 and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == True:
						built_here = True
					else: 
						built_here = False
							
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == False:
						built_here = False
					
					if world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] != 0:
						built_here = False
								
					if built_here == True:
						world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0 #first of all erase all items that are at this pos			
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = deepcopy(tl.tlist['building'][27]) #set doorway here
				
				elif style == 'Door':
					
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
						sfx.play('place')
						player.inventory.materials.wood -= res_need[0]
						player.inventory.materials.stone -= res_need[1]
						
						if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] == 0:
							built_here = True
						elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].civilisation == True:
							built_here = True
						else: 
							built_here = False
								
						if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == False:
							built_here = False
						
						if world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] != 0:
							built_here = False
								
						if built_here == True:
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0 #first of all erase all items that are at this pos
							world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = deepcopy(tl.tlist['building'][3]) #set door here
				
				elif style == 'Stair up':
					
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
						if player.pos[2] > 0:
						
							if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]-1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0+xmin]].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False:
								build_here = 0
							else: 
								build_here = 1
							
							if build_here == 0:
								sfx.play('place')
								world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0 #first of all erase all items that are at this pos
								world.maplist[player.pos[2]-1][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0
								player.inventory.materials.wood -= res_need[0]
								player.inventory.materials.stone -= res_need[1]
								world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][2]
								world.maplist[player.pos[2]-1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][1]
								if world.maplist[player.pos[2]-1][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] != 0:
									moveable = world.maplist[player.pos[2]-1][player.on_map].find_all_moveable()
									ran = random.randint(0,len(moveable)-1)
									pos = moveable[ran]
									world.maplist[player.pos[2]-1][player.on_map].npcs[pos[1]][pos[0]] = deepcopy(world.maplist[player.pos[2]-1][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin])
									world.maplist[player.pos[2]-1][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] = 0
							else:
								message.add('Not here.')
					else:
						message.add('Not enough Resources.')
			
				elif style == 'Stair down':
					
					if res_need[0] <= player.inventory.materials.wood and res_need[1] <= player.inventory.materials.stone:
						if player.pos[2] < 15:
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].replace == None and world.maplist[player.pos[2]+1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].build_here == True and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin].damage == False:
								build_here = 0
							else: 
								build_here = 1
							
							if build_here == 0:
								sfx.play('place')
								world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+ymin][player.pos[0]+xmin] = 0 #first of all erase all items that are at this pos
								world.maplist[player.pos[2]+1][player.on_map].containers[player.pos[1]+xmin][player.pos[0]+ymin] = 0
								player.inventory.materials.wood -= res_need[0]
								player.inventory.materials.stone -= res_need[1]
								world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][1]
								world.maplist[player.pos[2]+1][player.on_map].tilemap[player.pos[1]+ymin][player.pos[0]+xmin] = tl.tlist['functional'][2]
								if world.maplist[player.pos[2]+1][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] != 0:
									moveable = world.maplist[player.pos[2]+1][player.on_map].find_all_moveable()
									ran = random.randint(0,len(moveable)+1)
									pos = moveable[ran]
									world.maplist[player.pos[2]+1][player.on_map].npcs[pos[1]][pos[0]] = deepcopy(world.maplist[player.pos[2]+1][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin])
									world.maplist[player.pos[2]+1][player.on_map].npcs[player.pos[1]+ymin][player.pos[0]+xmin] = 0
							else:
								message.add('Not here.')
					else:
						message.add('Not enough Resources')
				
				elif style == 'Agriculture':
					if res_need[0] <= player.inventory.materials.seeds:
						player.inventory.materials.seeds -= res_need[0]
						
						play_sound = False
						
						for y in range (-ymin,ymax+1):
							for x in range (-xmin,xmax+1):
				
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].damage == False and world.maplist[player.pos[2]][player.on_map].npcs[player.pos[1]+y][player.pos[0]+x] == 0:
									built_here = True
								elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].civilisation == True:
									built_here = True
								else: 
									built_here = False
								
								if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x].build_here == False:
									built_here = False
								
								if built_here == True:
									play_sound = True
									world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]+y][player.pos[0]+x] = 0 #first of all erase all items that are at this pos
									world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]+y][player.pos[0]+x] = tl.tlist['building'][4] #set aggriculture here
								else:
									message.add('Not here!')
					
						if play_sound == True:
							sfx.play('place')
					else: 
						message.add('Not enough Resources.')
					
				elif style == 'remove':
					ui = screen.get_choice('Choose a mode!',('Single-Tile-Mode','Full-Structure-Mode'),True)
					if ui != 'Break':
						sfx_remove = False
						shape = world.maplist[player.pos[2]][player.on_map].float_building_shape(player.pos[0]+xmin,player.pos[1]+ymin,ui)
					
						for y in range(0,max_map_size):
							for x in range(0,max_map_size):
								if shape[y][x] == 1:
									sfx_remove = True
									world.maplist[player.pos[2]][player.on_map].containers[y][x] = 0 #first of all erase all items that are at this pos
									world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = tl.tlist['functional'][26] #set rubble here
								
						if sfx_remove == True:
							sfx.play('remove')
				
				run = False
			
					
			if ui == 'x':
				
				run = False
		
	def monster_attacks(self,x,y):
		#This function is called when a monster attacks the player. The x and the y variable are to define the monsters pos 
		
		if player.difficulty == 2 or player.difficulty == 3:#on hard or rouelike mode
			difficulty_bonus = 2
		else:
			difficulty_bonus = 1
		
		if 'invisible' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties and not 'perma-invisible' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties:
			world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties = [w.replace('invisible','visible') for w in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties]
		
		random_attack = None
		
		if world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'attack_random':
			coin_random = random.randint(0,1)
			if coin_random == 0:
				random_attack = 'melee'
			else:
				random_attack = 'magic'
		
		if world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'attack_melee' or random_attack == 'melee':
			
			self.training_def += 1
			
			bodypart = world.maplist[self.pos[2]][self.on_map].npcs[y][x].attack_were[random.randint(0,len(world.maplist[self.pos[2]][self.on_map].npcs[y][x].attack_were)-1)]
			
			monster_strength  = 0
			for i in range(0,world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.p_strength):
				 monster_strength += random.randint(1,6)
				 
			player_defense = 0
			for j in range(0,self.attribute.p_defense + self.inventory.wearing[bodypart].attribute.p_defense):
				player_defense += random.randint(1,6)
				
			if self.buffs.get_buff('ironskin') > 0:
				player_defense = player_defense + int(player_defense/2)
			
			if monster_strength >= player_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#give the monster a chance to have luck and hit the player
				chance = random.randint(0,25)
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:
					attack_success = True
					
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border >= 9:
				attack_success = True
					
			if attack_success == True:
				
				chance = random.randint(0,25)
				
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:#monster hits critical
					sfx.play('hit')
					message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' hits your ' + bodypart.lower() + ' critical!'
					screen.write_hit_matrix(player.pos[0],player.pos[1],5)
					message.add(message_string)
					player.lp -= 2*difficulty_bonus
					if self.inventory.wearing[bodypart] != self.inventory.nothing:
						self.inventory.wearing[bodypart].take_damage()
						if 'corrosive' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties:
							message.add('Acid corrodes your '+self.inventory.wearing[bodypart].classe+'!')
							for c in range(0,5):
								self.inventory.wearing[bodypart].take_damage()
						if 'flaming' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties and self.inventory.wearing[bodypart].material == 'wooden':
							ran = random.randint(0,9)
							if ran < 4:
								message.add('Flames burn your '+self.inventory.wearing[bodypart].classe+' to ashes!') #TIPO2
								self.inventory.wearing[bodypart] = self.inventory.nothing
								sfx.play('flame')
								
						if self.inventory.wearing[bodypart] != self.inventory.nothing and self.inventory.wearing[bodypart].state > 0:
							self.inventory.wearing[bodypart].set_name()
						else:
							if self.inventory.wearing[bodypart] != self.inventory.nothing:
								mes = 'Your '+self.inventory.wearing[bodypart].classe+' breaks!' #TIPO2
								self.inventory.wearing[bodypart] = self.inventory.nothing
								message.add(mes)
								sfx.play('item_break')
				else:
					sfx.play('hit')
					message_string = l10n.format_value("monster-hit", {"mons2": world.maplist[self.pos[2]][self.on_map].npcs[y][x].name , "body2" :bodypart.lower()})
					message.add(message_string)
					screen.write_hit_matrix(player.pos[0],player.pos[1],4)
					player.lp -= 1*difficulty_bonus
					if self.inventory.wearing[bodypart] != self.inventory.nothing:
						self.inventory.wearing[bodypart].take_damage()
						if 'corrosive' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties:
							message.add('Acid corrodes your '+self.inventory.wearing[bodypart].classe+'!')
							for c in range(0,5):
								self.inventory.wearing[bodypart].take_damage()
						if 'flaming' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties and self.inventory.wearing[bodypart].material == 'wooden':
							ran = random.randint(0,9)
							if ran < 4:
								message.add('Flames burn your '+self.inventory.wearing[bodypart].classe+' to ashes!')
								self.inventory.wearing[bodypart] = self.inventory.nothing
								sfx.play('flame')
								
						if self.inventory.wearing[bodypart] != self.inventory.nothing and self.inventory.wearing[bodypart].state > 0:
							self.inventory.wearing[bodypart].set_name()
						else:
							if self.inventory.wearing[bodypart] != self.inventory.nothing:
								mes = 'Your '+self.inventory.wearing[bodypart].classe+' breaks!'
								self.inventory.wearing[bodypart] = self.inventory.nothing
								message.add(mes)
								sfx.play('item_break')
						
				if world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect != None:
					
					chance = random.randint(0,99)
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_probability > chance:
						player.buffs.set_buff(world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect,world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_duration)
						message.add(world.maplist[self.pos[2]][self.on_map].npcs[y][x].message)
				
			else:
				sfx.play('miss')
				message_string = l10n.format_value("monster-miss", {"mons1": world.maplist[self.pos[2]][self.on_map].npcs[y][x].name})
				message.add(message_string)
				screen.write_hit_matrix(player.pos[0],player.pos[1],3)
		
		elif world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'attack_magic' or random_attack == 'magic':
			
			self.training_def -= 1
			
			monster_strength = 0
			for i in range(world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.m_strength):
				monster_strength += random.randint(1,6)
				
			player_defense = 0
			for j in range(0,player.attribute.p_defense + player.inventory.wearing['Neck'].attribute.m_defense + self.inventory.wearing['Hand'].attribute.m_defense):
				player_defense += random.randint(1,6)
			
			if self.buffs.get_buff('ironskin') > 0:
				player_defense = player_defense + int(player_defense/2)
			
			if monster_strength >= player_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#give the monster a chance to have luck and hit the player
				chance = random.randint(0,25)
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:
					attack_success = True
					
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border >= 9:
				attack_success = True
					
			if attack_success == True:
				
				chance = random.randint(0,25)
				
				if chance < world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.luck:#monster hits critical
					sfx.play('hit')
					message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '\'s magic attack hits you critical!'
					message.add(message_string)
					screen.write_hit_matrix(player.pos[0],player.pos[1],5)
					player.lp -= 2*difficulty_bonus
					if self.inventory.wearing['Neck'] != self.inventory.nothing:
						self.inventory.wearing['Neck'].take_damage()#your amor at this bodypart take twice damage
						self.inventory.wearing['Neck'].take_damage()
						if self.inventory.wearing['Neck'].state > 0:
							self.inventory.wearing['Neck'].set_name()
						else:
							mes = 'Your '+self.inventory.wearing['Neck'].classe+' breaks!'
							self.inventory.wearing['Neck'] = self.inventory.nothing
							message.add(mes)
							sfx.play('item_break')
						
					if self.inventory.wearing['Hand'] != self.inventory.nothing:
						self.inventory.wearing['Hand'].take_damage()#your amor at this bodypart take twice damage
						self.inventory.wearing['Hand'].take_damage()
						if self.inventory.wearing['Hand'].state > 0:
							self.inventory.wearing['Hand'].set_name()
						else:
							mes = 'Your '+self.inventory.wearing['Hand'].classe+' breaks!'
							self.inventory.wearing['Hand'] = self.inventory.nothing
							message.add(mes)
							sfx.play('item_break')
				else:
					sfx.play('hit')
					message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '\'s magic attack hits you!'
					message.add(message_string)
					screen.write_hit_matrix(player.pos[0],player.pos[1],4)
					player.lp -= 1*difficulty_bonus
					
					if self.inventory.wearing['Neck'] != self.inventory.nothing:
						self.inventory.wearing['Neck'].take_damage()
						if self.inventory.wearing['Neck'].state > 0:
							self.inventory.wearing['Neck'].set_name()
						else:
							mes = 'Your '+self.inventory.wearing['Neck'].classe+' breaks!'
							self.inventory.wearing['Neck'] = self.inventory.nothing
							message.add(mes)
							sfx.play('item_break')
						
					if self.inventory.wearing['Hand'] != self.inventory.nothing:
						self.inventory.wearing['Hand'].take_damage()
						if self.inventory.wearing['Hand'].state > 0:
							self.inventory.wearing['Hand'].set_name()
						else:
							mes = 'Your '+self.inventory.wearing['Hand'].classe+' breaks!'
							self.inventory.wearing['Hand'] = self.inventory.nothing
							message.add(mes)
							sfx.play('item_break')
				
				if world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect != None:
					
					chance = random.randint(0,99)
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_probability > chance:
						player.buffs.set_buff(world.maplist[self.pos[2]][self.on_map].npcs[y][x].possible_effect,world.maplist[self.pos[2]][self.on_map].npcs[y][x].effect_duration)
						message.add(world.maplist[self.pos[2]][self.on_map].npcs[y][x].message)
					
			else:
				sfx.play('miss')
				message_string = 'A ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '\'s magic attack miss you!'
				message.add(message_string)
				screen.write_hit_matrix(player.pos[0],player.pos[1],3)
		
		if self.lp <= 0:
			screen.render_dead()
	
	def attack_monster(self,x,y,style='melee'):
		#This function is called when the player try to move at the same position like a monster. The x and the y variable definates the monsters pos.
		
		check_lvl_up = False
		
		if self.buffs.get_buff('invisible') > 0:
			self.buffs.remove_buff('invisible')
		
		if 'invisible' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties and not 'perma-invisible' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties:
			world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties = [w.replace('invisible','visible') for w in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties]
		
		if world.maplist[self.pos[2]][self.on_map].npcs[y][x].behavior == 'talk':
			try:
				#Step 0: check if a coded dialog is available
				code = dialog.dlist[world.maplist[self.pos[2]][self.on_map].npcs[y][x].message]
				
				#Step 1: gather mob position
				pos_string = 'mob_x= '+ str(x) + '; mob_y= '+ str(y) + '; mob_z= '+ str(self.pos[2]) + '; mob_on_map= "' + self.on_map + '";'
				
				#Step 2: prepare memory
				mem_string = world.maplist[self.pos[2]][self.on_map].npcs[y][x].memory+'\n'
				
				#Step 3: load utils
				util = dialog.dlist['dialog_util']
				
				#Step 4: combine everything
				
				len_string = pos_string + mem_string + util
				len_list = len_string.split('\n')
				lnminus = str(len(len_list)+1)
				
				code_name = world.maplist[self.pos[2]][self.on_map].npcs[y][x].message + '.py'
				
				exec_string = pos_string + mem_string + util + code
				exec_string = exec_string.replace('*lnminus*',lnminus)
				exec_string = exec_string.replace('*code_name*',code_name)
				
				#Step 5: execute string
				try:
					exec(exec_string)
					return 'Done'
				except:
					message.add('[DIALOG EXECUTION ERROR]')
					import traceback
					exc_type, exc_obj, exc_tb = sys.exc_info()
					traceback.print_exception(exc_type, exc_obj, exc_tb, limit=9)
					return 'Done'
				 
			except:	
				message.add(world.maplist[self.pos[2]][self.on_map].npcs[y][x].message)
			
				return 'Done'
		
		if style == 'magic':
			
			self.training_attack -= 1
			player_strength = 0
			for i in range(0,self.attribute.m_strength + self.inventory.wearing['Hold(L)'].attribute.m_strength + int(self.lvl*0.6)):
				player_strength += random.randint(1,6)
			
			if self.buffs.get_buff('berserk') > 0:
				player_strength = player_strength + int(player_strength/2)
				
			monster_defense = 0
			for j in range(0,world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.m_defense):
				monster_defense += random.randint(1,6)
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border > 9:
				monster_defense = 0
			
			player_luck = self.attribute.luck + self.inventory.wearing['Hand'].attribute.luck +self.inventory.wearing['Neck'].attribute.luck
			
			if player.buffs.get_buff('blessed') != 0:
				player_luck += 2
			
			if player_strength >= monster_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#let the player have luck and hit the monster
				chance = random.randint(0,25)
				if chance < player_luck:
					attack_success = True
					
			if attack_success == True:
				
				if player.inventory.check_suffix('Life Extr.') == True:
					ran = random.randint(0,99)
					if ran < 5:
						world.maplist[self.pos[2]][self.on_map].npcs[y][x].corps_style = 'life_essence'
						
				if player.inventory.check_suffix('Drop Treas.') == True:
					ran = random.randint(0,99)
					if ran < 10:
						world.maplist[self.pos[2]][self.on_map].npcs[y][x].corps_style = 'miner'
						world.maplist[self.pos[2]][self.on_map].npcs[y][x].corps_lvl = 10
						
				
				chance = random.randint(0,25)
				
				if chance < player_luck:#player hits critical
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name == 'cage':
						sfx.play('hit_cage')
					elif world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'Your magic attack hits the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' critical!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,5)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 2
					 
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl + 1
						
						plus = 0
						
						for yy in range(y-1,y+2):
							for xx in range(x-1,x+2):
								if world.maplist[self.pos[2]][self.on_map].npcs[yy][xx] != 0:
									if world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].AI_style == 'hostile' and (xx != x or yy != y):
										plus += 1
										
						xp += plus
						
						if xp < 0:
							xp = 0
						if player.inventory.check_suffix('Ignorance'):
							coin = random.randint(0,1)
							if coin == 1:
								self.xp -= 1 
						elif player.inventory.check_suffix('Learning') == True:
							self.xp += int(xp*1.25)
						else:
							self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
							check_lvl_up = True
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y,xp)	
						
					if self.inventory.wearing['Hold(L)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(L)'].take_damage()
						if self.inventory.wearing['Hold(L)'].state > 0:
							self.inventory.wearing['Hold(L)'].set_name()
						else:
							mes = 'Your '+self.inventory.wearing['Hold(L)'].classe+' breaks!'
							self.inventory.wearing['Hold(L)'] = self.inventory.nothing
							message.add(mes)
							sfx.play('item_break')
					 
				else:
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name == 'cage':
						sfx.play('hit_cage')
					elif world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'Your magic attack hits the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,4)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 1
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl +1
						
						plus = 0
						
						for yy in range(y-1,y+2):
							for xx in range(x-1,x+2):
								if world.maplist[self.pos[2]][self.on_map].npcs[yy][xx] != 0:
									if world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].AI_style == 'hostile' and (xx != x or yy != y):
										plus += 1
										
						xp += plus
						
						if xp < 0:
							xp = 0
						if player.inventory.check_suffix('Learning') == True:
							self.xp += int(xp*1.25)
						else:
							self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
							check_lvl_up = True
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y,xp)
					
					if self.inventory.wearing['Hold(L)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(L)'].take_damage()
						if self.inventory.wearing['Hold(L)'].state > 0:
							self.inventory.wearing['Hold(L)'].set_name()
						else:
							mes = 'Your '+self.inventory.wearing['Hold(L)'].classe+' breaks!'
							self.inventory.wearing['Hold(L)'] = self.inventory.nothing
							message.add(mes)
							sfx.play('item_break')
			else:
				sfx.play('miss')
				message_string = 'You miss the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '.'
				message.add(message_string)
				screen.write_hit_matrix(x,y,3)
		else:
			
			self.training_attack += 1
			
			player_strength = 0
			for i in range(0,self.attribute.p_strength + self.inventory.wearing['Hold(R)'].attribute.p_strength + int(self.lvl*0.6)):
				player_strength += random.randint(1,6)
			
			if self.buffs.get_buff('berserk') > 0:
				player_strength = player_strength + int(player_strength/2)
				
			monster_defense = 0
			for i in range(0,world.maplist[self.pos[2]][self.on_map].npcs[y][x].basic_attribute.p_defense):
				monster_defense += random.randint(1,6)
				if '-skill' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties:
					monster_defense = int(monster_defense*0.75)
			if world.maplist[self.pos[2]][self.on_map].npcs[y][x].move_border > 9:
				monster_defense = 0
			
			player_luck = self.attribute.luck + self.inventory.wearing['Hand'].attribute.luck +self.inventory.wearing['Neck'].attribute.luck
			
			if player.buffs.get_buff('blessed') != 0:
				player_luck += 2
				
			if player_strength >= monster_defense:
				attack_success = True
			else:
				attack_success = False
				
			if attack_success == False:#let the player have luck and hit the monster
				chance = random.randint(0,25)
				if chance < player_luck:
					attack_success = True
			
			if attack_success == True:
				
				if player.inventory.check_suffix('Life Extr.') == True:
					ran = random.randint(0,99)
					if ran < 5:
						world.maplist[self.pos[2]][self.on_map].npcs[y][x].corps_style = 'life_essence'
				
				if player.inventory.check_suffix('Drop Treas.') == True:
					ran = random.randint(0,99)
					if ran < 10:
						world.maplist[self.pos[2]][self.on_map].npcs[y][x].corps_style = 'miner'
						world.maplist[self.pos[2]][self.on_map].npcs[y][x].corps_lvl = 10
				
				chance = random.randint(0,25)
				
				if chance < player_luck:#player hits critical
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name == 'cage':
						sfx.play('hit_cage')
					elif world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'You hit the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + ' critical!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,5)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 2
					 				
					if self.inventory.wearing['Hold(R)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(R)'].take_damage()
						if 'corrosive' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties:
							message.add('Acid corrodes your '+self.inventory.wearing['Hold(R)'].classe+'!')
							for c in range(0,5):
								self.inventory.wearing['Hold(R)'].take_damage()
						if 'flaming' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties and self.inventory.wearing['Hold(R)'].material == 'wooden':
							ran = random.randint(0,9)
							if ran < 4:
								message.add('Flames burn your '+self.inventory.wearing['Hold(R)'].classe+' to ashes!')
								self.inventory.wearing['Hold(R)'] = self.inventory.nothing
								sfx.play('flame')
								
						if self.inventory.wearing['Hold(R)'] != self.inventory.nothing and self.inventory.wearing['Hold(R)'].state > 0:
							self.inventory.wearing['Hold(R)'].set_name()
						else:
							if self.inventory.wearing['Hold(R)'] != self.inventory.nothing:
								mes = 'Your '+self.inventory.wearing['Hold(R)'].classe+' breaks!'
								self.inventory.wearing['Hold(R)'] = self.inventory.nothing
								message.add(mes)
								sfx.play('item_break')
					
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl +1
						
						if xp < 0:
							xp = 0
						if player.inventory.check_suffix('Learning') == True:
							self.xp += int(xp*1.25)
						else:
							self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
							check_lvl_up = True
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y,xp)
					 
				else:
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].name == 'cage':
						sfx.play('hit_cage')
					elif world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'vase' and world.maplist[self.pos[2]][self.on_map].npcs[y][x].name != 'monster vase':
						sfx.play('hit')
					else:
						sfx.play('shatter')
					message_string = 'You hit the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '!'
					message.add(message_string)
					screen.write_hit_matrix(x,y,4)
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp -= 1	
					
					if self.inventory.wearing['Hold(R)'] != self.inventory.nothing:
						self.inventory.wearing['Hold(R)'].take_damage()
						if 'corrosive' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties:
							message.add('Acid corrodes your '+self.inventory.wearing['Hold(R)'].classe+'!')
							for c in range(0,5):
								self.inventory.wearing['Hold(R)'].take_damage()
						if 'flaming' in world.maplist[self.pos[2]][self.on_map].npcs[y][x].properties and self.inventory.wearing['Hold(R)'].material == 'wooden':
							ran = random.randint(0,9)
							if ran < 4:
								message.add('Flames burn your '+self.inventory.wearing['Hold(R)'].classe+' to ashes!')
								self.inventory.wearing['Hold(R)'] = self.inventory.nothing
								sfx.play('flame')
								
						if self.inventory.wearing['Hold(R)'] != self.inventory.nothing and self.inventory.wearing['Hold(R)'].state > 0:
							self.inventory.wearing['Hold(R)'].set_name()
						else:
							if self.inventory.wearing['Hold(R)'] != self.inventory.nothing:
								mes = 'Your '+self.inventory.wearing['Hold(R)'].classe+' breaks!'
								self.inventory.wearing['Hold(R)'] = self.inventory.nothing
								message.add(mes)
								sfx.play('item_break')
								
					if world.maplist[self.pos[2]][self.on_map].npcs[y][x].lp <= 0:
						
						xp = world.maplist[self.pos[2]][self.on_map].npcs[y][x].lvl - self.lvl + 1
						
						if xp < 0:
							xp = 0
						if player.inventory.check_suffix('Learning') == True:
							self.xp += int(xp*1.25)
						else:
							self.xp += xp
						
						if self.xp >= 100:
							self.lvl_up()
							check_lvl_up = True
						
						test = False
						while test == False:
							test = world.maplist[self.pos[2]][self.on_map].monster_die(x,y,xp)
			
			else:
				sfx.play('miss')
				message_string = 'You miss the ' + world.maplist[self.pos[2]][self.on_map].npcs[y][x].name + '.'
				message.add(message_string)
				screen.write_hit_matrix(x,y,3)
			
			if check_lvl_up == True:
				mes = 'Congratulations! You reached level ' + str(player.lvl) + '!'
				message.add(mes)
	
	def player_fire(self,direction,style=1):
		
		if style == 1:
			sfx.play('fire')
		else:
			sfx.play('miss')
			
		#direction must be a tulpel like (0,1) [style: (x,y)]
		x=player.pos[0]
		y=player.pos[1]
		c = 1
		run = True
		
		while run:
			
			xx = player.pos[0] + (direction[0]*c)
			yy = player.pos[1] + (direction[1]*c)
			c += 1
			
			pet_here = False
			if self.pet_pos != False and self.pet_on_map != False:
				if xx == self.pet_pos[0] and yy == self.pet_pos[1] and player.pos[2] == self.pet_pos[2] and self.on_map == self.pet_on_map:
					pet_here = True
			
			if world.maplist[self.pos[2]][self.on_map].npcs[yy][xx] == 0 or pet_here == True or world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].behavior == 'talk':
				screen.write_hit_matrix(xx,yy,1)
			elif world.maplist[self.pos[2]][self.on_map].npcs[yy][xx] != 0 and pet_here == False and world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].behavior != 'talk':#there is a monster here
				if style == 1:
					player.attack_monster(xx,yy,'magic')
				else:
					chance = 9 - int(c/2)
					coin = random.randint(0,9)
					if coin < chance:
						sfx.play('hit')
						message.add('You hit the '+world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].name+'!')
						screen.write_hit_matrix(xx,yy,4)
						world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].lp -= (style-1)
						if world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].lp <= 0:
							world.maplist[self.pos[2]][self.on_map].monster_die(xx,yy)
					else:
						message.add('You miss the '+world.maplist[self.pos[2]][self.on_map].npcs[yy][xx].name+'!')
						screen.write_hit_matrix(xx,yy,3)
						
				run = False
			
			if c > 4 or world.maplist[self.pos[2]][self.on_map].tilemap[yy][xx].transparency == False:
				if style != 1:
					sfx.play('throw')
				run = False
				
		for i in range(0,len(self.inventory.misc)):
			if self.inventory.misc[i] != self.inventory.nothing:
				self.inventory.misc[i] = deepcopy(self.inventory.misc[i])
				if self.inventory.misc[i].use_name == 'throw' and self.inventory.misc[i].effect == style:
					self.inventory.misc[i].stack_size -=1
					if self.inventory.misc[i].stack_size <= 0:
						self.inventory.misc[i] = self.inventory.nothing
					return True
				
	def respawn(self):
		
		if self.godmode == True:
			self.lp = self.attribute.max_lp
			self.attribute.hunger = self.attribute.hunger_max
			self.attribute.thirst = self.attribute.thirst_max
			self.attribute.tiredness = self.attribute.tiredness_max
			return True
		
		for y in range(0,max_map_size):
			for x in range(0,max_map_size):
				if world.maplist[self.pos[2]][self.on_map].npcs[y][x] != 0:
					world.maplist[self.pos[2]][self.on_map].npcs[y][x].last_known_player_pos = 'Unknown'
		
		self.make_grave()
		
		screen.reset_hit_matrix()
		
		self.pos[2] = 0
		self.pos[0] = world.startx
		self.pos[1] = world.starty
		self.on_map = 'elysium_0_0'
		
		self.xp = 0 #the player always lose all xp on dead
		old_lp = deepcopy(self.attribute.max_lp)
		if self.difficulty == 1:#normal
			self.attribute.max_lp = max(self.attribute.max_lp-1,7)
		elif self.difficulty == 2:#hard
			self.attribute.max_lp = max(self.attribute.max_lp-2,6)
		self.lost_lp += old_lp-self.attribute.max_lp
		self.lp = self.attribute.max_lp
		self.attribute.hunger = self.attribute.hunger_max
		self.attribute.thirst = self.attribute.thirst_max
		self.attribute.tiredness = self.attribute.tiredness_max
		self.buffs = buffs()
		
		if self.difficulty != 0 and self.difficulty != 3:
			self.inventory.materials = materials()#reset materials
		
		if self.difficulty == 0: #easy
			self.coins = max(int(self.coins*0.8),0)
		elif self.difficulty == 1: #normal
			self.coins = max(int(self.coins*0.5),0)
		elif self.difficulty == 2: #hard
			self.coins = max(int(self.coins*0.25),0)

		if self. difficulty == 3:#the player plays on Roguelike
			#del everything
			
			try:
				player_path = save_path + 'player.data'
				os.remove(player_path)
			except:
				None
									
			try:
				world_path = save_path + 'world.data'
				os.remove(world_path)
			except:
				None	
									
			try:
				gods_path = save_path + 'gods.data'
				os.remove(gods_path)
			except:
				None
									
			try:
				time_path = save_path + 'time.data'
				os.remove(time_path)
			except:
				None
		
		self.stand_check()
		
			
class messager():
	
	def __init__(self):
		self.mes_list = []
		self.last_mes = 'foo'
		self.mes_history = [[]]
		self.history_page = 0
		self.last_output = [' ',' ',' ',' ',' ']
		self.more_messages = False
		
	def add(self, new_message, check_if_new = False):
		# check_if_new is only needed by the (mob)player.stand_check function to prove there is only shown a new message about the ground when the player enters a new kind of ground
		if check_if_new == False:
			self.mes_list.append(new_message)
			self.mes_history[self.history_page].append(new_message)
			
			if len(self.mes_history[self.history_page]) == 7:
				self.mes_history.append([])
				if len(self.mes_history) > 10:
					del self.mes_history[0]
				else:
					self.history_page +=1
			
		elif check_if_new == True and self.last_mes != new_message:
			self.last_mes = new_message
			self.mes_list.append(new_message)
			
			self.mes_history[self.history_page].append(new_message)
			
			if len(self.mes_history[self.history_page]) == 7:
				self.mes_history.append([])
				if len(self.mes_history) > 10:
					del self.mes_history[0]
				else:
					self.history_page +=1
			
	def clear(self):
		
		if self.more_messages == False:
			del self.mes_list[0]
		
	def render_history(self):
		
		page = self.history_page
		run = True
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
				
			bg = pygame.Surface((480,360))
			bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
			if low_res == True:
				bg = pygame.transform.scale(bg,(320,240))

			s.blit(bg,(0,0))

			text_string = '~Message History~ [Page(' + str(page+1) + ' of ' + str(len(self.mes_history)) +')]'
			text_image = screen.font.render(text_string,1,(255,255,255))
			s.blit(text_image,(5,2))#menue title
			
			for i in range (0, len(self.mes_history[page])):
				mes_image = screen.font.render(self.mes_history[page][i],1,(0,0,0))
				if low_res == False:
					s.blit(mes_image,(5,100+i*25))#blit menu_items
				else:
					s.blit(mes_image,(5,46+i*25))#blit menu_items
			text = '['+key_name['ws']+'] - Turn page ['+key_name['x']+'] - leave'	
			text_image = screen.font.render(text,1,(255,255,255))
			if low_res == True:
				s.blit(text_image,(2,225))
			else:
				s.blit(text_image,(5,335))
			
			if game_options.mousepad == 1 and low_res == False:	
				s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
			else:
				s_help = pygame.Surface((160,360))
				s_help.fill((48,48,48))
				s.blit(s_help,(480,0))
			
			if game_options.mousepad == 0 and low_res == False:
				s_help = pygame.Surface((640,360))
				s_help.fill((48,48,48))
				s_help.blit(s,(80,0))
				s = s_help
			
			if low_res == False:
				s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
			screen.screen.blit(s,(0,0))
			
			pygame.display.flip()
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'w' or ui == 'a':
				page -= 1
				if page < 0:
					page = len(self.mes_history)-1
					
			if ui == 's' or ui == 'd':
				page += 1
				if page > len(self.mes_history)-1:
					page = 0
					
			if ui == 'x':
				run = False
			
	def sget(self):
		
		s_list = self.mes_list
		s_list = s_list[::-1]
		
		if len(self.mes_list) > 0:
			
			if len(s_list) < 5: 
				for c in range(0,5-len(s_list)):
					s_list.append(' ')
			
			self.last_output = s_list	
		else:
			return self.last_output
				
		return s_list
		
class inventory():
	
	def __init__(self, equipment=7, food=14, misc=14):
		
		self.nothing = item_wear('Nothing',21,0,0)
		self.wearing = {'Head' : self.nothing, 'Body' : self.nothing, 'Legs' : self.nothing, 'Feet' : self.nothing, 'Hand' : self.nothing, 'Neck' : self.nothing, 'Hold(R)' : self.nothing, 'Hold(L)' : self.nothing, 'Background' : self.nothing, 'Clothing' : self.nothing, 'Hat' : self.nothing, 'Axe' : self.nothing, 'Pickaxe' : self.nothing}
		self.item_change = self.nothing
		self.equipment = []
		self.food = []
		self.misc = []
		self.materials = materials()
		self.blueprint = il.ilist['misc'][15]#a ordenary blueprint
		self.inv_mes = '~*~'
		
		for i in range (0,equipment):
			self.equipment.append(self.nothing)
		for i in range (0,food):
			self.food.append(self.nothing)
		for i in range (0,misc):
			self.misc.append(self.nothing)
			
		#go on here
	def clean_spaces(self):
		#equipment
		del_list = []
		for i in range(0,len(self.equipment)):
			if self.equipment[i] == self.nothing:
				del_list.append(i)
		if len(del_list) > 0:
			for d in del_list:
				del self.equipment[d]
				self.equipment.append(self.nothing)
				for j in range(0,len(del_list)):
					del_list[j] -= 1		
		#food
		del_list = []
		for i in range(0,len(self.food)):
			if self.food[i] == self.nothing:
				del_list.append(i)
		if len(del_list) > 0:
			for d in del_list:
				del self.food[d]
				self.food.append(self.nothing)
				for j in range(0,len(del_list)):
					del_list[j] -= 1
		#misc
		del_list = []
		for i in range(0,len(self.misc)):
			if self.misc[i] == self.nothing:
				del_list.append(i)
		if len(del_list) > 0:
			for d in del_list:
				del self.misc[d]
				self.misc.append(self.nothing)
				for j in range(0,len(del_list)):
					del_list[j] -= 1
		
	def check_suffix(self,suffix):
		key_list = self.wearing.keys()
		test = False
		for i in key_list:
			if self.wearing[i].suffix == suffix:
				test = True
		return test
		
	
	def wear(self,slot):
		
		if self.equipment[slot] != self.nothing:
		
			self.inv_mes = 'Now you wear a  %s.' %(self.equipment[slot].name)
		
			if self.wearing[self.equipment[slot].worn_at] != self.nothing and self.wearing[self.equipment[slot].worn_at].cursed != 0:
				self.item_change = self.wearing[self.equipment[slot].worn_at]
				if self.equipment[slot].cursed == 0:
					self.inv_mess = 'This feels deadly cold!'
				elif self.equipment[slot].cursed == 2:
					self.inv_mes = 'This feels superb!'
				
				self.equipment[slot].identification()
				self.wearing[self.equipment[slot].worn_at] = self.equipment[slot]
				self.equipment[slot] = self.item_change
				self.item_change = self.nothing
			elif self.wearing[self.equipment[slot].worn_at].cursed == 0:
				self.inv_mes = 'You can\'t! It\'s cursed!'
				self.wearing[self.equipment[slot].worn_at].identification()
			else:
				if self.equipment[slot].cursed == 0:
					self.inv_mess = 'This feels deadly cold!'
				elif self.equipment[slot].cursed == 2:
					self.inv_mes = 'This feels superb!'
				self.equipment[slot].identification()
				self.wearing[self.equipment[slot].worn_at] = self.equipment[slot]
				self.equipment[slot] = self.nothing
		
	def unwear(self,slot):
		
		worn = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck','Axe','Pickaxe','Background','Clothing','Hat']	
		
		if self.wearing[worn[slot]].cursed != 0: #this is no cursed item
		
			num = -1
			found = -1
		
			for i in self.equipment:
			
				if found != -1:
					break
				
				num += 1
				if i == self.nothing:
					found = num
				
			if found > -1:
				self.equipment[num] = self.wearing[worn[slot]]
				self.inv_mes = 'You unwear a %s.' %( self.wearing[worn[slot]].name)
				self.wearing[worn[slot]] = self.nothing
			else:
				self.inv_mes = 'You have no free space in your inventory!'
		else: #this item is cursed
			
			self.inv_mes = 'You can\'t! It\'s cursed!'
			self.wearing[worn[slot]].identification()
	
	def drop_check(self,x,y,z,check_exceptions=True):
		#This function chencks if a tile is suitable to drop a item on it
		exceptions = (tl.tlist['functional'][3],#empty chest
					tl.tlist['functional'][4],#chest
					tl.tlist['functional'][5],#stack
					tl.tlist['functional'][24],#empty fridge
					tl.tlist['functional'][25])#fridge
		
		if world.maplist[z][player.on_map].tilemap[y][x].replace == None:
			if world.maplist[z][player.on_map].tilemap[y][x].move_group == 'soil' or world.maplist[z][player.on_map].tilemap[y][x].move_group == 'house':
				return True
		
		exception_found = False
		if check_exceptions == True:
			for i in exceptions:
				if world.maplist[z][player.on_map].tilemap[y][x].techID == i.techID:
					exception_found = True
			if exception_found == True:
				return True
			else: 
				return False
		else:
			return False
			
	def drop(self,category, slot):
		
		self.inv_mes = 'You can\'t drop an item here!'
		
		worn = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck','Axe','Pickaxe','Background','Clothing','Hat']
		
		try:
			field_full = False
			sacrifice = False
			fridge = False
			exception = False
			
			string = 'foo'
			
			if not self.drop_check(player.pos[0],player.pos[1],player.pos[2]):
				field_full = True
				string = 'Not here!'

			if self.drop_check(player.pos[0],player.pos[1],player.pos[2],False) != self.drop_check(player.pos[0],player.pos[1],player.pos[2]):
				exception = True
				
			if self.drop_check(player.pos[0],player.pos[1],player.pos[2]):
				if 	world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] != 0: #there are already things here
					if len(world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items) > 6:
						field_full = True
						string = 'There are already too many items at this place!'
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][24].techID or world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][25].techID: #this is a Fridge (full or empty)
				fridge = True
			
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][15].techID:#this is a altar 
				field_full = False
				sacrifice = True
				
			if string != 'foo':
				self.inv_mes = string
			
		except: 
			field_full = False
			
		if category > 1 or self.wearing[worn[slot]].cursed != 0:#there is no worn cursed item you wanna drop
			if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].damage == 0 and field_full == False: #you only can drop thing on save tiles with 7 or less other items on it
			
				if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] == 0: #if there is no container
					world.maplist[player.pos[2]][player.on_map].add_container([self.nothing],player.pos[0],player.pos[1],False) #make new container
				
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID != tl.tlist['functional'][3].techID and sacrifice == False and exception == False: #if there is no empty chest at this pos and this is no sacrifice and no other exception make a stack
						help_tile = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]]) #get old tile at player pos
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][5]) #set new tile on player pos
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = help_tile #set replace tile at the new position to the old tile at this pos
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][3].techID:
						replace = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace)
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][4])#else make a full chest out of the empty one
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = replace
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][24].techID and category == 3:
						replace = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace)
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][25])#else make a full fridge out of the empty one
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = replace
					
				if (category == 0 or category == 1) and fridge == False:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.wearing[worn[slot]])
					if self.wearing[worn[slot]] != self.nothing: #this slot isn't empty
						self.inv_mes = 'You drop a %s.' %(self.wearing[worn[slot]].name)
					self.wearing[worn[slot]] = self.nothing
				elif fridge == True and (category == 0 or category == 1):
					self.inv_mes = 'Only food can be stored in a fridge!'
					
				if category == 2 and fridge == False:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.equipment[slot])
					if self.equipment[slot] != self.nothing:
						self.inv_mes = 'You drop a %s.' %(self.equipment[slot].name)
					self.equipment[slot] = self.nothing
				elif fridge == True and category == 2:
					self.inv_mes = 'Only food can be stored in a fridge!'
					
				if category == 3:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.food[slot])
					if self.food[slot] != self.nothing:
						self.inv_mes = 'You drop a %s.' %(self.food[slot].name)
					self.food[slot] = self.nothing
				
				if category == 4 and fridge == False:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items.append(self.misc[slot])
					if self.misc[slot] != self.nothing:
						self.inv_mes = 'You drop a %s.' %(self.misc[slot].name)
					self.misc[slot] = self.nothing
				elif fridge == True and category == 4:
					self.inv_mes = 'Only food can be stored in a fridge!'
				
				for i in range (0, len(world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items)): #check for empty slots and errase them if necessary ---------- unsure because the -1
					try:#try-except is needed because the length of the list can change
						if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[i] == self.nothing:
							del world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[i]
					except:
						None
						
				if sacrifice == True:
					
					for j in range (0, len(world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items)):
						
						equipment = False
						food = False
						mood_change = 0
						
						try:
							# if this is working this must be a equipment item
							if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].state > 40:#this is equipment in a good state
								equipment = True
								if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'wooden':
									mood_change += 1
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'tin':
									mood_change += 2
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'copper':
									mood_change += 4
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'steel':
									mood_change += 6
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'titan':
									mood_change += 8
								elif world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].material == 'magnicum':
									mood_change += 10
						except:
							# if this is working this must be a food item
							try:
								if world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].items[j].rotten == False: #this is unrotten food
									food = True
									mood_change += 2
							except:
								None
								
						finally:
							 
							if equipment == False and food == False:
								mood_change = -1*(random.randint(1,10))
							
							if mood_change == 0:
								self.inv_mes = 'The gods accept your sacrifice.'
							elif mood_change > 0:
								self.inv_mes = 'The gods seem to be pleased...'
							else:
								self. inv_mes = 'It seems the gods dislike your gift...'
									 
							gods.mood += mood_change
							
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = 0 # del all sacrificed items 
								 
		else:#you try to drop a worn, cursed item
			
			self.inv_mes = 'You can\'t! It\'s cursed!'
			self.wearing[worn[slot]].identification()
		
	def use(self,slot):
		
		if self.misc[slot] != self.nothing:
			
			if self.misc[slot].use_name.find('place') != -1  or self.misc[slot].use_name == 'plant':
				
				cat = self.misc[slot].place_cat
				num = self.misc[slot].place_num
				
				if self.misc[slot].name.find('Bucket') != -1:
					test = screen.render_place(tl.tlist[cat][num],self.misc[slot].use_name,True)
				else:
					test = screen.render_place(tl.tlist[cat][num],self.misc[slot].use_name)
				
				if test != False:
					if self.misc[slot].use_name == 'plant':
						sfx.play('plant')
					else:
						sfx.play('place')
					if self.misc[slot].name == 'Bomb':
						world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('bomb3',test[0],test[1],1))
					if self.misc[slot].name == 'Pressure Plate':
						world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('plate_wait',test[0],test[1],1))
					if self.misc[slot].name == 'Timed Emitter':
						world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('timer_wait',test[0],test[1],3))
					if self.misc[slot].name == 'Menhir':
						world.maplist[player.pos[2]][player.on_map].tilemap[test[1]][test[0]] = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[test[1]][test[0]])
						engraving = screen.get_choice('Chose engraving!',('Empty','North','South','West','East','O','X'),False)
						world.maplist[player.pos[2]][player.on_map].tilemap[test[1]][test[0]].tile_pos = (16,7+engraving)
					#if self.misc[slot].name == 'Bed':
					#	ran = random.randint(5,60)
					#	world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('spawn_villager',test[0],test[1],ran))
					self.misc[slot].stack_size -= 1
					if self.misc[slot].name.find('Bucket') != -1:
						self.misc[slot] = deepcopy(il.ilist['misc'][84]) 
					if self.misc[slot].stack_size <= 0:
						self.misc[slot] = self.nothing
					return True #if use returns a true this means after this action the inventory is closed. this action needs a turn
			
			elif self.misc[slot].use_name == 'apply':#this is a blueprint. only blueprints are allowed to use 'apply'
				helpslot = player.inventory.blueprint
				player.inventory.blueprint = self.misc[slot]
				self.misc[slot] = helpslot
			
			elif self.misc[slot].use_name == 'fill':#fill is only for buckets
				if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['misc'][0].techID:#this is low water
					world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['misc'][1])#set mud
					self.misc[slot] = deepcopy(il.ilist['misc'][85]) #water bucket
					sfx.play('no_fish')
				elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['misc'][3].techID:#this is water
					world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['misc'][0])#set low water
					self.misc[slot] = deepcopy(il.ilist['misc'][85]) #water bucket
					sfx.play('no_fish')
				elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['sewer'][2].techID:#this is sewer water
					world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['misc'][1])#set low mud
					self.misc[slot] = deepcopy(il.ilist['misc'][91]) #dirty water bucket
					sfx.play('no_fish')
				elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['sewer'][5].techID:#this is deep sewer water
					world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['sewer'][2])#set sewer water
					self.misc[slot] = deepcopy(il.ilist['misc'][91]) #dirty water bucket
					sfx.play('no_fish')
				elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['global_caves'][4].techID:#this is lava
					world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['misc'][2])#set hot cave ground
					self.misc[slot] = deepcopy(il.ilist['misc'][86]) #lava bucket
					sfx.play('no_fish')
				else:
					self.inv_mes = 'This won\'t work here!'
			
			elif self.misc[slot].name == 'Heart-Shaped Crystal':
				sfx.play('shatter')
				old_lp = deepcopy(player.attribute.max_lp)
				if player.lost_lp > 0:
					message.add('Your lost health returns to your body.')
					player.attribute.max_lp + player.lost_lp
					player.lost_lp = 0
				if player.lp < old_lp:
						message.add('All your wounds are healed.')
				player.lp = player.attribute.max_lp
				self.misc[slot] = self.nothing
				return True
			
			elif self.misc[slot].name == 'Mysterious Blue Crystal':
				sfx.play('shatter')
				if player.mp < player.attribute.max_mp:
					player.mp = player.attribute.max_mp
					message.add('You are suddenly concentrated again.')
				else:
					message.add('Nothing happens.')
				self.misc[slot] = self.nothing
				return True
			
			elif self.misc[slot].name == 'Magic Map':
				if player.on_map != 'dungeon_0_0':
					screen.render_map(player.pos[2])
				else:
					self.inv_mes = 'The magic map does not work here!'
			
			elif self.misc[slot].name == 'Pet Medicine':
				if player.pet_pos != False and player.pet_on_map != False:
					prop = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties
					if 'pet0' in prop or 'pet1' in prop or 'pet2' in prop:
						if player.pet_lp < world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].basic_attribute.max_lp:
							player.pet_lp = min(player.pet_lp+2,world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].basic_attribute.max_lp)
							world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].relation += 100
							self.inv_mes = 'You give '+ world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+' some medicine.'
							self.misc[slot].stack_size -= 1
							if self.misc[slot].stack_size == 0:
								self.misc[slot] = self.nothing
						else:
							self.inv_mes = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+' dosn\'t need medicine.'
					else:
						self.inv_mes = 'Your companion is no pet!'
				else:
					self.inv_mes = 'You travel alone.'
					
			elif self.misc[slot].name == 'Pet Candy':
				if player.pet_pos != False and player.pet_on_map != False:
					prop = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties
					if 'pet0' in prop or 'pet1' in prop or 'pet2' in prop:
						world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].relation += 100
						self.inv_mes = 'You give '+ world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+' some candy.'
						self.misc[slot].stack_size -= 1
						if self.misc[slot].stack_size == 0:
							self.misc[slot] = self.nothing
					else:
						self.inv_mes = 'Your companion is no pet!'
				else:
					self.inv_mes = 'You travel alone.'
			
			elif self.misc[slot].name == 'Evolution Stone':
				if player.pet_pos != False and player.pet_on_map != False:
					prop = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties
					if 'pet0' in prop or 'pet1' in prop:
						if 'pet0' in prop:
							relation_needed = 999
						else:
							relation_needed = 2999
							
						if world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].relation > relation_needed:
							name = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name)
							memory = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].memory)
							relation = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].relation)
							world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]] = ml.mlist['pet'][world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].anger_monster]
							world.maplist[player.pet_pos[2]][player.pet_on_map].set_monster_strength(player.pet_pos[0],player.pet_pos[1],1)
							self.inv_mes = name+' envolves into a '+world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+'.'
							#memo to myself: add a cool animation here
							world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name = name
							world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].memory = memory
							world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].relation = relation
							world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].AI_style = 'company'
							self.misc[slot].stack_size -= 1
							if self.misc[slot].stack_size == 0:
								self.misc[slot] = self.nothing
						else:
							self.inv_mes = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+' isn\'t ready to envolve.'
					elif 'pet2' in prop:
						self.inv_mes = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+' has reached its maximum evolution level already.'
					else:
						self.inv_mes = 'Your companion is no pet!'
				else:
					self.inv_mes = 'You travel alone.'
			
			elif self.misc[slot].name == 'Enchanted Enhancement Powder':
				
				l = ('Hold(R)','Hold(L)','Head','Body','Legs','Feet')
				fl = []
				for i in l:
					if (self.wearing[i] != self.nothing) and (self.wearing[i].plus < 3):
						fl.append(i)
				
				if len(fl) == 0:
					self.inv_mes = 'You wear nothing that can be enhanced.'
					return False
				elif len(fl) == 1:
					if fl[0] == 'Feet':
						self.inv_mes = 'Your ' + self.wearing[fl[0]].name + ' glow blue.'
					else:
						self.inv_mes = 'Your ' + self.wearing[fl[0]].name + ' glows blue.'
					self.wearing[fl[0]].plus += 1
					self.wearing[fl[0]].set_name()
					self.misc[slot] = self.nothing
				else:
					nl = []
					for j in fl:
						nl.append(self.wearing[j].name)
					c = screen.get_choice('Which item do you like to enhance?',nl,True)
					if c == 'Break':
						self.inv_mes = 'Never mind'
					else:
						if fl[c] == 'Feet':
							self.inv_mes = 'Your ' + self.wearing[fl[c]].name + ' glow blue.'
						else:
							self.inv_mes = 'Your ' + self.wearing[fl[c]].name + ' glows blue.'
						self.wearing[fl[c]].plus += 1
						self.wearing[fl[c]].set_name()
						self.misc[slot] = self.nothing
			
			elif self.misc[slot].name == 'Heavy Bag':
				message.add('You open the bag.')
				if self.materials.wood < self.materials.wood_max:
					wood_num = random.randint(1,9)
				else:
					wood_num = 0
				if self.materials.stone < self.materials.stone_max:
					stone_num = random.randint(1,9)
				else:
					stone_num = 0
				if self.materials.ore < self.materials.ore_max:
					ore_num = random.randint(-3,3)
					if ore_num < 0:
						ore_num = 0
				else:
					ore_num = 0
				if self.materials.gem < self.materials.gem_max:
					gem_num = random.randint(-6,2)
					if gem_num < 0:
						gem_num = 0
				else:
					gem_num = 0
				
				string = 'It contains: ' + str(wood_num) + ' wood, ' +str(stone_num) + ' stone'
				
				if ore_num > 0:
					string = string + ', ' + str(ore_num) + ' ore'
				if gem_num > 0:
					string = string + ', ' + str(gem_num) + ' gem'
					
				wood_num = self.materials.add('wood', wood_num)
				stone_num = self.materials.add('stone', stone_num)
				ore_num = self.materials.add('ore', ore_num)
				gem_num = self.materials.add('gem', gem_num)
				
				string = ''
				
				if wood_num != 'Full!':
					string = string + str(wood_num)
				if stone_num != 'Full!':	 
					string = string + ',' + str(stone_num)
				if ore_num != 'Full!':
					string = string + ',' + str(ore_num)
				if gem_num != 'Full!':
					string = string + ',' + str(gem_num)
					
				if wood_num+stone_num+ore_num+gem_num == 0:
					string = 'Your bags are to full to keep anything out of the bag.'
					
				message.add(string)
				
				self.misc[slot] = self.nothing
				
				return True
				
			elif self.misc[slot].name == 'Bandage':
				if player.buffs.get_buff('bleeding') > 0:
					message.add('You bandage your wounds.')
					player.buffs.remove_buff('bleeding')
					self.misc[slot].stack_size -= 1
					if self.misc[slot].stack_size <= 0:
						self.misc[slot] = self.nothing
					return True
				else:
					self.inv_mes = 'You are not wounded.'
					return False
					
			elif self.misc[slot].name == 'Eyedrops':
				if player.buffs.get_buff('blind') > 0:
					message.add('Your blindness is cured.')
					player.buffs.remove_buff('blind')
					self.misc[slot].stack_size -= 1
					if self.misc[slot].stack_size <= 0:
						self.misc[slot] = self.nothing
					return True
				else:
					message.add('Everything blurs.')
					player.buffs.set_buff('blind',60)
					self.misc[slot].stack_size -= 1
					if self.misc[slot].stack_size <= 0:
						self.misc[slot] = self.nothing
					return True
			
			elif self.misc[slot].name == 'Antidote':
				if player.buffs.get_buff('poisoned') > 0:
					message.add('Your poisoning is cured.')
					player.buffs.remove_buff('poisoned')
					self.misc[slot].stack_size -= 1
					if self.misc[slot].stack_size <= 0:
						self.misc[slot] = self.nothing
					return True
				else:
					self.inv_mes = 'You are not poisoned.'
					return False
					
			elif self.misc[slot].name == 'Holy Water':
				if player.buffs.get_buff('hexed') > 0:
					message.add('The hex is removed from you.')
					player.buffs.remove_buff('hexed')
					self.misc[slot].stack_size -= 1
					if self.misc[slot].stack_size <= 0:
						self.misc[slot] = self.nothing
					return True
				else:
					self.inv_mes = 'You are not hexed.'
					return False
					
			elif self.misc[slot].use_name == 'throw':
				screen.fire_mode = self.misc[slot].effect
				return True
			
			elif self.misc[slot].use_name == 'read':#this is a scroll or a spellbook
				
				if self.misc[slot].name.count('Scroll') > 0 or self.misc[slot].name == 'Book of Skill':
					scroll = True
				else:
					scroll = False
					
				if player.mp < player.attribute.max_mp and scroll == False:
					self.inv_mes = 'You are not focused.'
					return False #this dosnt need a turn
				
				test = random.randint(0,19)
				success = 'normal'
					
				if test < player.attribute.m_strength:
					success = 'critical'
				elif test-player.attribute.m_strength > 9:
					success = 'miss'
						
				if scroll == True:
					success = 'normal'
					
				if self.misc[slot].effect == 0: #identify
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						message.add('The spell failed!')
						return True
					
					ident_list = []
					
					for j in range(0,len(self.equipment)):
						if self.equipment[j] != self.nothing and self.equipment[j].known == False:
							ident_list.append(j)
							
					if len(ident_list) == 0:
						self.inv_mes = 'You own nothing that could be identified'
						return False
						
					else:
						if success == 'normal':
							names = []
							for i in ident_list:
								names.append(self.equipment[i].name)
						
							c = screen.get_choice('Choose an item for identification!',names,True)
							if c == 'Break':
								self.inv_mess = 'Nevermind'
								scroll = False
								return False
							else:
								self.equipment[ident_list[c]].identification()
								message.add(self.equipment[ident_list[c]].name.title()+' identified!')
						elif success == 'critical':
							for k in ident_list:
								try:
									self.equipment[k].identification()
								except:
									None
							message.add('You are aware of your equipments states now!')
						sfx.play('identify')
						
				elif self.misc[slot].effect == 1: #repair
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						message.add('The spell failed!')
					
					bodyparts = ('Head','Body','Legs','Feet','Hand','Neck','Hold(R)','Hold(L)', 'Axe', 'Pickaxe')
					final_bodyparts = []
					
					for i in bodyparts:
						
						if self.wearing[i] != self.nothing and self.wearing[i].state != 0:
							final_bodyparts.append(i)
							
					if len(final_bodyparts) != 0:	
						ran = random.randint(0, len(final_bodyparts)-1) # select a random item for repair, migt be replaced just with zero
						# select the most damaged equipped inventory item
						for i in range(0,len(final_bodyparts)):
							if self.wearing[final_bodyparts[i]].state<self.wearing[final_bodyparts[ran]].state:
								ran = i
								
						if success == 'critical':		
							self.wearing[final_bodyparts[ran]].state = 100 # actually repair the item
							self.wearing[final_bodyparts[ran]].set_name() # and reset its name accordingly
							
							mes = 'Your ' + self.wearing[final_bodyparts[ran]].classe + ' '
							if final_bodyparts[ran] == 'Feet':
								mes = mes + 'have'
							else:
								mes = mes + 'has'
							mes = mes + ' been fully repaired.'
							message.add(mes)
							
						elif success == 'normal':
							self.wearing[final_bodyparts[ran]].state = min(self.wearing[final_bodyparts[ran]].state+20,100) # actually repair the item
							self.wearing[final_bodyparts[ran]].set_name() # and reset its name accordingly
							
							mes = 'Your ' + self.wearing[final_bodyparts[ran]].classe + ' '
							if final_bodyparts[ran] == 'Feet':
								mes = mes + 'have'
							else:
								mes = mes + 'has'
							mes = mes + ' been repaired.'
							message.add(mes)
							
						elif success == 'miss':
							self.wearing[final_bodyparts[ran]].state = max(self.wearing[final_bodyparts[ran]].state-20,0) # actually damage the item
							self.wearing[final_bodyparts[ran]].set_name() # and reset its name accordingly
							
							mes = 'Your ' + self.wearing[final_bodyparts[ran]].classe + ' '
							if final_bodyparts[ran] == 'Feet':
								mes = mes + 'have'
							else:
								mes = mes + 'has'
							mes = mes + ' been damaged.'
							message.add(mes)
							
							if self.wearing[final_bodyparts[ran]].state < 1:
								mes = 'Your ' + self.wearing[final_bodyparts[ran]].classe + ' '
								if final_bodyparts[ran] == 'Feet':
									mes = mes + 'break!'
								else:
									mes = mes + 'breaks!'
								message.add(mes)
								sfx.play('item_break')
								self.wearing[final_bodyparts[ran]] = self.nothing
								return True
							
					else:
						message.add('Nothing seems to happen.')
						
				elif self.misc[slot].effect == 2: #healing
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						message.add('The spell failed!')
						return True
					
					if player.lp < player.attribute.max_lp:
						if success == 'critical':
							screen.write_hit_matrix(player.pos[0],player.pos[1],6)
							player.lp = player.attribute.max_lp
							player.buffs.remove_buff('bleeding')
							message.add('All your wounds heal immediately.')
						elif success == 'normal':
							screen.write_hit_matrix(player.pos[0],player.pos[1],6)
							player.lp = min(player.lp+5,player.attribute.max_lp)
							player.buffs.remove_buff('bleeding')
							message.add('You feel much better now.')
					else:
						if player.buffs.get_buff('bleeding') > 0:
							screen.write_hit_matrix(player.pos[0],player.pos[1],6)
							player.buffs.remove_buff('bleeding')
							message.add('Your bleeding wounds close immediately.')
						else:
							message.add('Nothing seems to happen.')
						
				elif self.misc[slot].effect == 3: #teleport
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						message.add('The spell failed!')
						return True
					
					pos_list = world.maplist[player.pos[2]][player.on_map].find_all_moveable(False)
					
					if len(pos_list) > 1:
						run = True
						while run:
							ran = random.randint(0,len(pos_list)-1)
							pos = pos_list[ran]
							if world.maplist[player.pos[2]][player.on_map].npcs[pos[1]][pos[0]] == 0:
								run = False
						screen.render_fade(True,False)
						player.pos[0] = pos[0]
						player.pos[1] = pos[1]
						player.stand_check()
						sfx.play('teleport')
						message.add('You teleport your self.')
						if success == 'critical' and player.lp < player.attribute.max_lp:
							message.add('All your wounds close immediately.')
							screen.write_hit_matrix(player.pos[0],player.pos[1],6)
							player.lp = player.attribute.max_lp
						screen.render_fade(False,True)
					else:
						message.add('Nothing seems to happen')
					
				elif self.misc[slot].effect == 4:#return
						
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						message.add('The spell failed!')
						return True
					
					if player.pos[0] != world.startx or player.pos[1] != world.starty or player.pos[2] != 0:
						screen.render_fade(True,False)
						player.pos[0] = world.startx
						player.pos[1] = world.starty
						player.pos[2] = 0
						player.on_map = 'elysium_0_0'
						sfx.play('teleport')
						if success == 'critical' and player.lp < player.attribute.max_lp:
							message.add('All your wounds close immediately.')
							screen.write_hit_matrix(player.pos[0],player.pos[1],6)
							player.lp = player.attribute.max_lp
						player.stand_check()
						player.buffs.remove_buff('hexed')
						message.add('You returned home.')
						screen.render_fade(False,True)
					else:
						message.add('Nothing seems to happen.')

				elif self.misc[slot].effect == 5: #flames
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						message.add('The spell failed!')
						if player.buffs.get_buff('fire resistance') == 0:
							player.lp -= 2
							message.add('Magic flames hurt your flesh!')
						return True
					
					num_flames = 0
					
					radius = 1
					
					if success == 'critical':
						radius = 2
					
					for y in range(player.pos[1]-radius,player.pos[1]+radius+1):
						for x in range(player.pos[0]-radius,player.pos[0]+radius+1):
							try:
								if x != player.pos[0] or y !=player.pos[1]:
									if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace == None and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'solid' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'low_liquid' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'solid_border' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'swim' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'wet_entrance':
										replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
										world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['effect'][4])
										world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
										world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('flame',x,y,3))
										num_flames+=1
										if world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:
											try:
												world.maplist[player.pos[2]][player.on_map].npcs[y][x].lp -=3
												if world.maplist[player.pos[2]][player.on_map].npcs[y][x].lp < 1 or world.maplist[player.pos[2]][player.on_map].npcs[y][x].techID == ml.mlist['special'][14].techID:
													world.maplist[player.pos[2]][player.on_map].monster_die(x,y)
													world.maplist[player.pos[2]][player.on_map].make_monsters_angry(x,y,'kill')
											except:
												None
							except:
								None
								
					if num_flames != 0:
						sfx.play('flame')
						message.add('Magical flames start to burn close to you.')
					else:
						message.add('Nothing seems to happen.')
				
				elif self.misc[slot].effect == 6:#healing aura
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						message.add('The spell failed!')
						return True
					
					num_aura = 0
					
					duration = 10
					
					if success == 'critical':
						duration = 60 
					
					for y in range(player.pos[1]-1,player.pos[1]+2):
						for x in range(player.pos[0]-1,player.pos[0]+2):
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace == None and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group != 'solid' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].damage == False:
								replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['effect'][5])
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
								world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('healing_aura',x,y,duration))
								num_aura+=1
								
					if num_aura != 0:
						sfx.play('aura')
						message.add('A healing aura spreades under your feet.')
						player.buffs.remove_buff('hexed')
					else:
						message.add('Nothing seems to happen.')
				
				elif self.misc[slot].effect == 7: #light
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						player.buffs.set_buff('blind',30)
						message.add('The spell failed!')
						return True
					
					duration = 180
					
					if success == 'critical':
						duration = 360
					
					player.buffs.set_buff('light',duration,add = False)
					message.add('A magical light surrounds your body.')
					player.stand_check()
					
				elif self.misc[slot].effect == 8: #book of skill
					mes = player.skill_up()
					message.add(mes)
				
				elif self.misc[slot].effect == 9: #stasis
					
					if success == 'miss':
						sfx.play('spell_fail')
						player.buffs.set_buff('confused',60)
						player.buffs.set_buff('immobilized',10)
						message.add('The spell failed!')
						return True
					
					duration = 10
					
					if success == 'critical':
						duration = 20
					
					sfx.play('fire')
						
					for y in range(player.pos[1]-2,player.pos[1]+3):
						for x in range(player.pos[0]-2,player.pos[0]+3):
							try:
								screen.write_hit_matrix(x,y,23)
								if world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:
									if world.maplist[player.pos[2]][player.on_map].npcs[y][x].move_border != 10:
										world.maplist[player.pos[2]][player.on_map].npcs[y][x].move_border += 10
										if world.maplist[player.pos[2]][player.on_map].npcs[y][x].move_border == 10:
											world.maplist[player.pos[2]][player.on_map].npcs[y][x].move_border += 1
										world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('stasis',x,y,duration))
							except:
								None
				
				if scroll == True:
					if self.misc[slot].name == 'Book of Skill':
						self.misc[slot].stack_size -= 1
						if self.misc[slot].stack_size <= 0:
							self.misc[slot] = self.nothing
						message.add('The book turns to dust.')
					else:
						self.misc[slot].stack_size -= 1
						if self.misc[slot].stack_size <= 0:
							self.misc[slot] = self.nothing
						message.add('The scroll turns to dust.')
				else:
					player.mp = 0
					message.add('You lose your focus.')
				
				return True
			
			elif self.misc[slot].name == 'Chalk':
				
				x = player.pos[0]
				y = player.pos[1]
				
				if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group == 'soil' and world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace == None:
					replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
					world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['effect'][6])
					world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
					duration = random.randint(10,30)
					world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('elbereth',x,y,duration))
					message.add('You write the magic word on the ground.')
					
					breaking = random.randint(0,99)
					if breaking < 11:
						message.add('The chalk breaks.')
						self.misc[slot] = self.nothing
					
					return True
				else:
					self.inv_mes = 'Not here!'
					return False
				
			elif self.misc[slot].name == 'Fishing rod':
				
				chance = 0 
				
				for y in range (player.pos[1]-1, player.pos[1]+1):
					for x in range (player.pos[0]-1, player.pos[0]+1):
						
						if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['misc'][0].techID: #this is low water
							chance += 1
						elif world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['misc'][3].techID: #this is water
							chance += 2
						
				if chance == 0:
					self.inv_mes ='Not here!'
					return False
				
				run = True
				
				while run:
					got_fish = random.randint(0,20)
					
					if chance > got_fish:
						status_quo = world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] #save the container at this ülace
						coin = random.randint(0,99)
					
						if coin < 75:
						
							items = (il.ilist['food'][4],il.ilist['food'][25])#catch a fish or a jellyfish
						
							choose = random.randint(0,len(items)-1)
						
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = container([items[choose]])#set a temporary container
							test = world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].loot(0)
						
							if test == True:
								message.add('You got a ' + items[choose].name + '.')
								screen.write_hit_matrix(player.pos[0],player.pos[1],10)
								sfx.play('got_fish')
							else:
								message.add('You got a ' + items[choose].name + ', but you can\'t keep it.')
								sfx.play('got_fish')
							
						else:
							#catch old shoes
							material = random.randint(6,20) #no wooden shoes. they would swim ;-)
							curse = random.randint(0,2)
							plus = random.randint(-2,2)
							state = random.randint(4,11)
						
							item = item_wear('shoes',material,plus,state,curse)
						
							world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = container([item])
							test = world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]].loot(0)
							
							if test == True:
								message.add('You got some old ' + item.name + '.')
								screen.write_hit_matrix(player.pos[0],player.pos[1],11)
								sfx.play('got_fish')
							else:
								message.add('You got some old ' + item.name + ', but you can\'t keep it.')
								sfx.play('got_fish')
							
						world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = status_quo #recover the old container 
					
					else:
						message.add('It seems nothing want to bite...')
						sfx.play('no_fish')
					
					for yy in range(player.pos[1]-1,player.pos[1]+2):
						for xx in range(player.pos[0]-1,player.pos[0]+2):
							
							if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] != 0:
								message.add('A monster interrupts you!')
								return True
					
					screen.render_request('['+key_name['e']+']-Go on!',' ','['+key_name['x']+']-Stop')
					
					run2 = True
					
					while run2:
						ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
					
						if ui == 'e':
							time.tick()
							screen.reset_hit_matrix()
							run2 = False
						elif ui == 'x':
							run = False
							run2 = False
				return True
				
			elif self.misc[slot].name == 'Torch':
				
				player.buffs.set_buff('light',180, add = False)
				self.misc[slot].stack_size -= 1
				if self.misc[slot].stack_size <= 0:
					self.misc[slot] = self.nothing
					sfx.play('flame')
				message.add('The burning torch illumines your surroundings.')
				player.stand_check()
				return True
			
			elif self.misc[slot].name == 'Camera':
				
				screenshot_path = basic_path + os.sep + 'SCREENSHOT'
				
				if os.path.exists(screenshot_path) == False:
					os.makedirs(screenshot_path)
				
				screenshot_name = player.name + '_' + str(time.hour) + '_' + str(time.minute) + '_' + str(time.day_total) + '.png'
				pic = screen.render(0,photo = True)
				final_path = screenshot_path + os.sep + screenshot_name
				pygame.image.save(pic,final_path)
				message.add('You take a photo.')
				message.add('[Saved as: '+screenshot_name+']')
				sfx.play('photo')
				return True
			
			elif self.misc[slot].name == 'Crystal orb':
				
				found = 0
				
				for y in range(0,max_map_size):
					for x in range(0,max_map_size):
						portal = False
						for h in range(0,len(tl.tlist['portal'])):
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID ==tl.tlist['portal'][h].techID:
								portal = True
						if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID ==tl.tlist['dungeon'][7].techID or world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['dungeon'][14].techID or world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID ==tl.tlist['dungeon'][16].techID or world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID ==tl.tlist['dungeon'][18].techID or portal == True:
							#this is a dungeon entrance
							mes = 'foo'
							for i in range(0,len(tl.tlist['portal'])):
								if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID ==tl.tlist['portal'][i].techID:
									mes = 'You see a portal in the '
							if mes == 'foo':
								mes = 'You see a dungeon stair in the '
							ns = y - player.pos[1]
							ew = x - player.pos[0]
							
							dir_north_south = ''
							dir_east_west = ''
							binding = ''
							
							if ns < -5:
								dir_north_south = 'north'
							elif ns > 5:
								dir_north_south = 'south'
								
							if ew < -5:
								dir_east_west = 'west'
							elif ew > 5:
								dir_east_west = 'east'
								
							if dir_north_south != '' and dir_east_west != '':
								binding = '-'
								
							dir_final = dir_north_south + binding + dir_east_west
							if dir_final != '': 
								mes = mes +  dir_final + '.'
							else:
								mes = 'foo'
								for i in range(0,len(tl.tlist['portal'])):
									if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID ==tl.tlist['portal'][i].techID:
										mes = 'You see a portal close to you.'
								if mes == 'foo':
									mes = 'You see a dungeon stair close to you.'
							message.add(mes)
							found += 1
				
				if found == 0:
					message.add('You can not se anything inside the orb.')
				return True
				
							
	def eat(self,slot):
		
		if self.food[slot] != self.nothing:
			
			if self.food[slot].give_seed > 0:
				c = screen.get_choice('What do you want exactly?',(self.food[slot].eat_name.title(),'Extract Seeds'),True)
			else:
				c = 0
			
			if c == 0:
				if self.food[slot].eat_name == 'drink':
					sfx.play('drink')
				else:
					sfx.play('eat')
				player.attribute.hunger += self.food[slot].satisfy_hunger
				if player.attribute.hunger > player.attribute.hunger_max:
					player.attribute.hunger = player.attribute.hunger_max+1 #the +1 is because the attribute will fall one point at the same turn
			
				player.attribute.thirst += self.food[slot].satisfy_thirst
				if player.attribute.thirst > player.attribute.thirst_max:
					player.attribute.thirst = player.attribute.thirst_max+1 #the +1 is because the attribute will fall one point at the same turn
			
			
				player.buffs.set_buff('adrenalised',self.food[slot].satisfy_tiredness,maximum = 1440)
			
				player.lp += self.food[slot].heal*player.lp_boost
				if player.lp > player.attribute.max_lp:
					player.lp = player.attribute.max_lp
			
				player.attribute.hunger_max += self.food[slot].rise_hunger_max
				player.attribute.thirst_max += self.food[slot].rise_thirst_max	
				player.attribute.tiredness_max += self.food[slot].rise_tiredness_max
				player.attribute.max_lp += self.food[slot].rise_lp_max
			
				if self.food[slot].effect != None:
					player.buffs.set_buff(self.food[slot].effect,self.food[slot].effect_duration)
			
				if self.food[slot].rotten == False:
					self.inv_mes = self.food[slot].eat_mes
				else:
					blind_coin = random.randint(0,1)
					if blind_coin == 1:
						blind_dur = random.randint(60,180)
						player.buffs.set_buff('blind',blind_dur)
					
					poison_coin = random.randint(0,1)
					if poison_coin == 1:
						posion_dur = random.randint(60,240)
						player.buffs.set_buff('poisoned',posion_dur)
					
					self.inv_mes = 'BAH! Rotten food...'
			
				self.food[slot] = self.nothing
			elif c == 1:
				sfx.play('extract')
				player.inventory.materials.add('seeds', self.food[slot].give_seed)
				self.food[slot] = self.nothing
			
	def render(self, category, slot, info=False, drop_info=False, simulate=False):
		
		self.clean_spaces()
		
		test = True
		
		s = pygame.Surface((640,360))
		
		if category != 1:
			s.blit(gra_files.gdic['display'][1],(0,0)) #render background
		else:
			s.blit(gra_files.gdic['display'][49],(0,0))
		
		text_y = 120
		marker_y = 115
		
		num = 0
		text = '~Inventory~ [Press ['+key_name['x']+'] to leave]'
				
		text_image = screen.font.render(text,1,(255,255,255))
		s.blit(text_image,(5,2))#menue title
		
		tab_names = ('Worn1','Worn2','Equi.','Cons.','Misc', 'Reso.', 'Comp.')
		
		for c in range(0,len(tab_names)):
			s.blit(gra_files.gdic['display'][2],(c*50,25))#blit empty tabs
			
		s.blit(gra_files.gdic['display'][3],(category*50,25))#blit used tab
		
		for d in range (0,len(tab_names)):
			
			text_image = screen.font.render(tab_names[d],1,(0,0,0))
			s.blit(text_image,(d*50+5,27))#blit tb names
			
		if category == 0 or category == 1:
			
			if category == 0:
				h = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck']
			else:
				h = ['Axe','Pickaxe','Background','Clothing','Hat']
				
			s.blit(gra_files.gdic['display'][4],(0,marker_y+slot*23))#blit marker
			 
			for i in h:
				
				color = (0,0,0)
				
				if self.wearing[i] != self.nothing: 
					if self.wearing[i].known == True:
						if self.wearing[i].cursed < 1:#cursed item
							color = (130,0,190)
						elif self.wearing[i].cursed > 1:#holy item
							color = (100,115,0)
					if self.wearing[i].state < 11:
						color = (200,0,0)
				else:
					if i == h[slot]:
						test = False
				
				string = i + ' : ' + self.wearing[i].name
				text_image = screen.font.render(string,1,color)
				s.blit(text_image,(21,text_y+num*23))#blit item names
				
				num += 1
			
		elif category == 2:
			
			for i in self.equipment:
				
				color = (0,0,0)
				
				if i != self.nothing: 
					if i.known == True:
						if i.cursed < 1:#cursed item
							color = (130,0,190)
						elif i.cursed > 1:#holy item
							color = (100,115,0)
					if i.state < 11:
						color = (200,0,0)
		
				
				if slot == num:
					s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
				if self.equipment[slot] == self.nothing:
					test = False
				
				text_image = screen.font.render(i.name,1,color)
				s.blit(text_image,(21,text_y+num*25))#blit item names
			
				num += 1
		
		elif category == 3:
			
			if slot < 7:
				plus = 0
			else:
				plus = 7
			
			for i in range(0,7):
				
				color = (0,0,0)
				
				if self.food[i+plus] != self.nothing:
					if self.food[i+plus].rotten == True:
						color = (200,0,0)
				
				if slot < 7:
					s.blit(gra_files.gdic['display'][79],(204,308))#blit page_down
				else:
					s.blit(gra_files.gdic['display'][78],(204,78))#blit page_up
					
				
				if slot-plus == num:
					s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
				if self.food[slot] == self.nothing:
					test = False
				
				text_image = screen.font.render(self.food[i+plus].name,1,color)
				s.blit(text_image,(21,text_y+num*25))#blit item names
				
				num += 1
				
		elif category == 4:
			
			if slot < 7:
				plus = 0
			else:
				plus = 7
			
			for i in range(0,7):
				
				if self.misc[i+plus] == self.nothing:
					use_name = False
				
				if slot < 7:
					s.blit(gra_files.gdic['display'][79],(204,308))#blit page_down
				else:
					s.blit(gra_files.gdic['display'][78],(204,78))#blit page_up

				
				if slot-plus == num:
					s.blit(gra_files.gdic['display'][4],(0,marker_y+num*25))#blit marker
				
				if self.misc[slot] == self.nothing:
					test = False
				
				text_string = self.misc[i+plus].name
				if self.misc[i+plus].max_stack_size > 1:
					text_string = text_string +' '+str(self.misc[i+plus].stack_size)+'x'
				text_image = screen.font.render(text_string,1,(0,0,0))
				s.blit(text_image,(21,text_y+num*25))#blit item names
			
				num += 1
		
		elif category == 5:
			
			string = 'Wood: ' + str(self.materials.wood) + '/' + str(self.materials.wood_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y))#blit wood line
			
			string = 'Stone: ' + str(self.materials.stone) + '/' + str(self.materials.stone_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+20))#blit stone line
			
			string = 'Ore: ' + str(self.materials.ore) + '/' + str(self.materials.ore_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+40))#blit ore line
			
			string = 'Herbs: ' + str(self.materials.herb) + '/' + str(self.materials.herb_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+60))#blit herbs line
			
			string = 'Gem: ' + str(self.materials.gem) + '/' + str(self.materials.gem_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+80))#blit gem line
		
			string = 'Seeds: ' + str(self.materials.seeds) + '/' + str(self.materials.seeds_max)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+100))#blit gem line
			
			string = 'Coins: ' + str(player.coins)
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+130))#blit coin line
			
			string = 'Built with: ' + player.inventory.blueprint.name 
			text_image = screen.font.render(string,1,(0,0,0))
			s.blit(text_image,(21,text_y+160))#blit blueprint line
		
		elif category == 6:
			if player.pet_pos == False and player.pet_on_map == False:
				string = 'You travel without company.'
				text_image = screen.font.render(string,1,(0,0,0))
				s.blit(text_image,(21,text_y+50))
			else:
				string = 'Name: ' + world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name
				text_image = screen.font.render(string,1,(0,0,0))
				s.blit(text_image,(21,text_y))
				
				string = 'Health: ' + str(player.pet_lp) + '/' + str(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].basic_attribute.max_lp)
				text_image = screen.font.render(string,1,(0,0,0))
				s.blit(text_image,(21,text_y+25))
				
				string = 'Relation: ' + str(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].relation)
				text_image = screen.font.render(string,1,(0,0,0))
				s.blit(text_image,(21,text_y+50))
				
				string = '[Send home]'
				text_image = screen.font.render(string,1,(0,0,0))
				s.blit(text_image,(21,text_y+100))
				
				string = '[Dismiss]'
				text_image = screen.font.render(string,1,(0,0,0))
				s.blit(text_image,(21,text_y+125))
				
				s.blit(gra_files.gdic['display'][4],(0,marker_y+100+(slot*25)))#blit marker
				
		text_image = screen.font.render(self.inv_mes,1,(255,255,255))
		s.blit(text_image,(5,335))
		self.inv_mes = '~*~'
		
		drop_name = 'drop'
		if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][15].techID: #this is an altar
			drop_name = 'sacrifice'
		elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][3].techID or world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][4].techID:
			drop_name = 'store'
		
		if info == True:
			screen.render_textbox_open()
			s.blit(gra_files.gdic['display'][5],(0,0))
			
			use_name = 'use'
			if category == 0 or category == 1:
				use_name = 'unequip'
			elif category == 2:
				use_name = 'equip'
			elif category == 3:
				if self.food[slot].give_seed < 1:
					use_name = self.food[slot].eat_name
				else:
					use_name = self.food[slot].eat_name+'/extract'
			elif category == 4:
				use_name = self.misc[slot].use_name
			
			use_image = screen.font.render('['+key_name['e']+'] - '+use_name,1,(255,255,255))
			s.blit(use_image,(5,0))
			drop_image = screen.font.render('['+key_name['b']+'] - manage',1,(255,255,255))
			s.blit(drop_image,(5,15))
			info_image = screen.font.render('['+key_name['i']+'] - info',1,(255,255,255))
			s.blit(info_image,(5,30))
			cancel_image = screen.font.render('['+key_name['x']+'] - cancel',1,(255,255,255))
			s.blit(cancel_image,(5,45))
		
		if drop_info == True:
			s.blit(gra_files.gdic['display'][5],(0,0))
			
			drop_image = screen.font.render('['+key_name['b']+'] - '+drop_name,1,(255,255,255))
			s.blit(drop_image,(5,0))
			dispose_image = screen.font.render('['+key_name['f']+'] - '+'dispose',1,(255,255,255))
			s.blit(dispose_image,(5,15))
			dispose_image = screen.font.render('['+key_name['i']+'] - '+'send home',1,(255,255,255))
			s.blit(dispose_image,(5,30))
			cancel_image = screen.font.render('['+key_name['x']+'] - cancel',1,(255,255,255))
			s.blit(cancel_image,(5,45))
		
		if game_options.mousepad == 1:
			s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
		else:
			s_help = pygame.Surface((160,360))
			s_help.fill((48,48,48))
			s.blit(s_help,(480,0))
		
		if game_options.mousepad == 0:
			s_help = pygame.Surface((640,360))
			s_help.fill((48,48,48))
			s_help.blit(s,(80,0))
			s = s_help
			
		s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
		
		if simulate == True:
			return s
			
		screen.screen.blit(s,(0,0))
		
		pygame.display.flip()
		
		return test
	
	def wear_right(self,worn_at):
		
		pos = []
		name = []
		
		for i in range(0,len(self.equipment)):
			if self.equipment[i].worn_at == worn_at:
				pos.append(i)
				name.append(self.equipment[i].name)
			
		if len(pos) > 0:
			ui = screen.get_choice('What do you like to equip?',name,True)
			if ui != 'Break':
				self.wear(pos[ui])
		else:
			self.inv_mes = 'You have no item you can equip here.'
	
	def find_use_name(self,use_name):
		
		pos = []
		name = []
		
		for i in range(0,len(self.misc)):
			if self.misc[i] != self.nothing:
				if self.misc[i].use_name == use_name:
					pos.append(i)
					name.append(self.misc[i].name)
			
		if len(pos) > 0:
			if len(pos) > 1:
				ui = screen.get_choice('What do you like to '+use_name+'?',name,True)
			else:
				ui = 0
				 
			if ui != 'Break':
				self.use(pos[ui])
		else:
			message.add('You have nothing you could '+use_name+'.')
				
	def inv_user_interaction(self,category=0):
		
		run = True
		slot = 0
		info = False
		drop_info = False
		worn = ['Hold(R)','Hold(L)','Head','Body','Legs','Feet','Hand','Neck','Axe','Pickaxe','Background','Clothing','Hat']
		render = True
		
		while run:
			if render:
				try:
					master_test = self.render(category, slot, info, drop_info)
				except:
					master_test = False
			else: 
				render = True
			
			ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,0,mouse=game_options.mousepad)
			
			if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
			
			if ui == 'd' and info == False:	
				slot = 0
				category += 1
				if category > 6: ######change######
					category = 0
			elif ui == 'a' and info == False:
				slot = 0
				category -= 1
				if category < 0: ######change######
					category = 6
			elif ui == 'x' and info == False:
				run = False
				screen.render_fade(True,False,'screen')
				break
			elif ui == 'x' and info == True:
				info = False
				drop_info = False
			elif ui == 'w' and info == False:
				slot -= 1
				if category == 0:
					if slot < 0:
						slot = 7
				elif category == 1:
					if slot < 0:
						slot  = 4
				elif category == 2:
					if slot < 0:
						slot = len(self.equipment)-1
				elif category == 3:
					if slot < 0:
						slot = len(self.food)-1
				elif category == 4:
					if slot < 0:
						slot = len(self.misc)-1
				elif category == 6:
					if slot < 0:
						slot = 1
						
			elif ui == 's' and info == False:
				slot += 1
				if category == 0:
					if slot == 8:
						slot = 0
				elif category == 1:
					if slot > 4:
						slot = 0
				elif category == 2:
					if slot == len(self.equipment):
						slot = 0
				elif category == 3:
					if slot == len(self.food):
						slot = 0
				elif category == 4:
					if slot == len(self.misc):
						slot = 0
				elif category == 6:
					if slot > 1:
						slot = 0
						
			elif ui == 'e' and info == True and drop_info == False:
				
				if category == 0 and self.wearing[worn[slot]] != self.nothing:
					self.unwear(slot)
				elif category == 1 and self.wearing[worn[slot+8]] != self.nothing:
					self.unwear(slot+8)
				elif category == 2:
					self.wear(slot)
				elif category == 3:
					self.eat(slot)
				elif category == 4:
					test = self.use(slot)
					if test == True:
						run = False
				
				info = False
			
			elif ui == 'e' and info == False and drop_info == False and category == 0 and self.wearing[worn[slot]] == self.nothing:
				self.wear_right(worn[slot])
			
			elif ui == 'e' and info == False and drop_info == False and category == 1 and self.wearing[worn[slot+8]] == self.nothing:
				self.wear_right(worn[slot+8])
					
			elif ui == 'e' and info == False and master_test == True and category != 5:
				
				if category == 6:
					if player.pet_pos != False and player.pet_on_map != False:
						if slot == 0 and not 'stay_at_lvl' in world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties:
							
							if 'npc' in world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties:
								seeked_tile = tl.tlist['functional'][18]
							else:
								seeked_tile = tl.tlist['sanctuary'][4]
							
							for yy in range(0,max_map_size):
								for xx in range(0,max_map_size):
									if world.maplist[0]['elysium_0_0'].tilemap[yy][xx].techID == seeked_tile.techID and world.maplist[0]['elysium_0_0'].npcs[yy][xx] == 0:
										string = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name + ' returns home.'
										message.add(string)
										screen.write_hit_matrix(player.pet_pos[0],player.pet_pos[1],7)
										world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].AI_style = 'ignore'
										world.maplist[0]['elysium_0_0'].npcs[yy][xx] = deepcopy(world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]])
										world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]] = 0
										player.pet_pos = False
										player.pet_on_map = False
										run = False
										return True
					
						elif slot == 0 and 'stay_at_lvl' in world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties:
							self.inv_mes = 'You can\'t send '+world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+' to elysium!'
				
						elif slot == 1 and not 'no_dismiss' in world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties:
							if player.pet_pos != False and player.pet_on_map != False:
								mes = 'Really dismiss ' + world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name + '?'
								test= screen.get_choice(mes,('No','Yes'),True)
								if test == 1:
									mes = world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name + ' is gone forever!'
									message.add(mes)
									screen.write_hit_matrix(player.pet_pos[0],player.pet_pos[1],7)
									world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]] = 0
									player.pet_pos = False
									player.pet_on_map = False
									run = False
									return True
						elif slot == 1 and 'no_dismiss' in world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties:
							self.inv_mes = 'You can\'t dismiss '+world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].name+'.'
				else:
					info = True
						
			elif ui == 'b' and (info == False or drop_info == True):
				
				drop_test =  True
				if category == 0:
					if self.wearing[worn[slot]] == self.nothing:
						drop_test = False
				elif category == 1:
					if self.wearing[worn[slot+8]] == self.nothing:
						drop_test = False
				elif category == 2:
					if self.equipment[slot] == self.nothing:
						drop_test = False
				elif category == 3:
					if self.food[slot] == self.nothing:
						drop_test = False
				elif category == 4:
					if self.misc[slot] == self.nothing:
						drop_test = False
				elif category > 4:
					drop_test = False
						
				if drop_test == True:
					if category != 1:
						self.drop(category,slot)
					else:
						self.drop(0,slot+8)
					
				info = False
				drop_info = False
			
			elif ui == 'b' and info == True:
				drop_info = True
				
			elif ui == 'f' and drop_info == True:
				self.inv_mes = 'Item disposed!'
				if category == 0 or category == 1:
					if category == 1:
						sl = slot + 8
					else:
						sl = slot
					if self.wearing[worn[sl]].cursed != 0:	
						self.wearing[worn[sl]] = self.nothing
					else:
						self.inv_mes = 'You can\'t! It\'s cursed!'
						self.wearing[worn[sl]].identification()
				elif category == 2:
					self.equipment[slot] = self.nothing
				elif category == 3:
					self.food[slot] = self.nothing
				elif category == 4:
					self.misc[slot] = self.nothing
				info = False
				drop_info = False
			
			elif ui == 'i' and master_test == True and category < 5:
				
				if drop_info == False:
					static_txt = True
					multi_txt = False
				
					if category == 0:
						static_txt = False
						txt = list(texts[self.wearing[worn[slot]].classe])
						test = self.wearing[worn[slot]].state_addition()
						if test == 'Unknown':
							string = 'Value: Unknown'
						else:
							string = 'Value: ' + str(test)
						txt.append(' ')
						txt.append(string)
						
						if self.wearing[worn[slot]].suffix != ' ':
							try:
								multi_txt = True
								if self.wearing[worn[slot]].artefact != False:
									txt = (txt,list(texts[self.wearing[worn[slot]].suffix]),list(texts['artefact']))
								else:
									txt = (txt,list(texts[self.wearing[worn[slot]].suffix]))
							except:
								None
					
					elif category == 2:
						if self.equipment[slot].name.find('[D]') != -1:#this is decorative clothing
							txt = 'decorative_clothes'
						else:
							static_txt = False
							txt = list(texts[self.equipment[slot].classe])
							test = self.equipment[slot].state_addition()
							if test == 'Unknown':
								string = 'Value: Unknown'
							else:
								string = 'Value: ' + str(test)	
							txt.append(' ')
							txt.append(string)
							
							if self.equipment[slot].suffix != ' ':
								try:
									txt = (txt,list(texts[self.equipment[slot].suffix]))
									multi_txt = True
								except:
									None
					
					elif category == 1:
						if self.wearing[worn[slot+8]].name.find('[D]') != -1:
							txt = 'decorative_clothes'
						else:
							static_txt = False
							txt = list(texts[self.wearing[worn[slot+8]].classe])
							test = self.wearing[worn[slot+8]].state_addition()
							if test == 'Unknown':
								string = 'Value: Unknown'
							else:
								string = 'Value: ' + str(test)
							txt.append(' ')
							txt.append(string)
							
							if self.wearing[worn[slot+8]].suffix != ' ':
								try:
									txt = (txt,list(texts[self.wearing[worn[slot+8]].suffix]))
									multi_txt = True
								except:
									None
							
					elif category == 3:
						static_txt = False
						txt = []
						txt.append(self.food[slot].name)
						txt.append(' ')
						if self.food[slot].satisfy_hunger > 0:
							txt.append('Reduces hunger.')
						if self.food[slot].satisfy_hunger < 0:
							txt.append('Raises hunger.')
						if self.food[slot].satisfy_thirst > 0:
							txt.append('Reduces thirst.')
						if self.food[slot].satisfy_thirst < 0:
							txt.append('Raises thirst.')
						if self.food[slot].satisfy_tiredness > 0:
							txt.append('Can adrenalise!')
						if self.food[slot].rise_hunger_max > 0:
							txt.append('Lets you go longer without food.')
						if self.food[slot].rise_thirst_max > 0:
							txt.append('Lets you go longer without water.')
						if self.food[slot].rise_tiredness_max > 0:
							txt.append('Lets you go longer without sleep.')
						if self.food[slot].heal > 0:
							txt.append('Can heal your wounds.')
						if self.food[slot].heal < 0:
							txt.append('Can hurt you!')
						if self.food[slot].rise_lp_max > 0:
							txt.append('Raises your max. LP.')
						if self.food[slot].give_seed > 0:
							txt.append('Seeds can be extracted.')
						if self.food[slot].rotten:
							txt.append('Rotten food may harm you!')
						elif self.food[slot].life_period < 720:
							if self.food[slot].life_period != False:
								txt.append('May rot soon.')
							else:
								txt.append('Won\'t rot.')
						if self.food[slot].effect != None:
							txt.append('Grants '+self.food[slot].effect.title())
					elif category == 4:
						if self.misc[slot].name.find('Blueprint') != -1:
							txt = 'Blueprint'
						elif self.misc[slot].name.find('Scroll') != -1:
							txt = 'Scroll'
						elif self.misc[slot].name.find('Spellbook') != -1:
							txt = 'Spellbook'
						else:
							if texts[self.misc[slot].name]:
								txt = self.misc[slot].name
							else:
								txt = 'info_soon' 	
				
					else:
						txt = 'info_soon'
				
					if static_txt:	
						t = screen.render_text(texts[txt])
					elif multi_txt:
						t = screen.render_multi_text(txt)
					else:
						t = screen.render_text(txt)
					
					info = False
					self.render(category,slot)
				
					if t == 'exit':
						exitgame = True
						screen.render_load(5)
						save(world,player,time,gods,save_path,os.sep)
						screen.save_tmp_png()
						master_loop = False
						playing = False
						run = False
						return('exit')
			
					else: 
						render = False
				
				else:
					
					if category < 2:
						info = False
						drop_info = False
						self.inv_mes = 'You can\'t send home a worn item!'
					elif category == 2:
						if world.maplist[0]['elysium_0_0'].containers[24][19] == 0:
							world.maplist[0]['elysium_0_0'].containers[24][19] = container([self.equipment[slot]])
							self.equipment[slot] = self.nothing
							replace = world.maplist[0]['elysium_0_0'].tilemap[24][19]
							world.maplist[0]['elysium_0_0'].tilemap[24][19] = deepcopy(tl.tlist['functional'][20])
							world.maplist[0]['elysium_0_0'].tilemap[24][19].replace = replace
							info = False
							drop_info = False
							self.inv_mes = 'Item returned home!'
							sfx.play('teleport')
						elif len(world.maplist[0]['elysium_0_0'].containers[24][19].items) > 6:
							info = False
							drop_info = False
							self.inv_mes = 'The magic chest is already full!'
						else:
							world.maplist[0]['elysium_0_0'].containers[24][19].items.append(deepcopy(self.equipment[slot]))
							self.equipment[slot] = self.nothing
							info = False
							drop_info = False
							self.inv_mes = 'Item returned home!'
							sfx.play('teleport')
					elif category == 3:
						if world.maplist[0]['elysium_0_0'].containers[26][19] == 0:
							world.maplist[0]['elysium_0_0'].containers[26][19] = container([self.food[slot]])
							self.food[slot] = self.nothing
							replace = world.maplist[0]['elysium_0_0'].tilemap[26][19]
							world.maplist[0]['elysium_0_0'].tilemap[26][19] = deepcopy(tl.tlist['functional'][20])
							world.maplist[0]['elysium_0_0'].tilemap[26][19].replace = replace
							info = False
							drop_info = False
							self.inv_mes = 'Item returned home!'
							sfx.play('teleport')
						elif len(world.maplist[0]['elysium_0_0'].containers[26][19].items) > 6:
							info = False
							drop_info = False
							self.inv_mes = 'The magic chest is already full!'
						else:
							world.maplist[0]['elysium_0_0'].containers[26][19].items.append(deepcopy(self.food[slot]))
							self.food[slot] = self.nothing
							info = False
							drop_info = False
							self.inv_mes = 'Item returned home!'
							sfx.play('teleport')
					elif category == 4:
						if world.maplist[0]['elysium_0_0'].containers[28][19] == 0:
							world.maplist[0]['elysium_0_0'].containers[28][19] = container([self.misc[slot]])
							self.misc[slot] = self.nothing
							replace = world.maplist[0]['elysium_0_0'].tilemap[28][19]
							world.maplist[0]['elysium_0_0'].tilemap[28][19] = deepcopy(tl.tlist['functional'][20])
							world.maplist[0]['elysium_0_0'].tilemap[28][19].replace = replace
							info = False
							drop_info = False
							self.inv_mes = 'Item returned home!'
							sfx.play('teleport')
						elif len(world.maplist[0]['elysium_0_0'].containers[28][19].items) > 6:
							info = False
							drop_info = False
							self.inv_mes = 'The magic chest is already full!'
						else:
							world.maplist[0]['elysium_0_0'].containers[28][19].items.append(deepcopy(self.misc[slot]))
							self.misc[slot] = self.nothing
							info = False
							drop_info = False
							self.inv_mes = 'Item returned home!'
							sfx.play('teleport')
							
class container():
	
	def __init__(self, items, deep_copy = True):
		
		if deep_copy:
			self.items = deepcopy(items)
		else:
			self.items = items
		self.con_mes = '~*~'
					
	def loot(self,num,real_mes= False):
		
		if self.items[num].inv_slot == 'equipment':
			
			found_place = False
			
			for i in range (0, len(player.inventory.equipment)):
				
				if found_place != True:
					if player.inventory.equipment[i] == player.inventory.nothing:
						player.inventory.equipment[i] = self.items[num]
						self.con_mes = '+['+self.items[num].name+']'
						if real_mes == True:
							message.add('+['+self.items[num].name+']')
						del self.items[num]
						found_place = True
			
		elif self.items[num].inv_slot == 'food':
			
			found_place = False
			
			for i in range (0, len(player.inventory.food)):
				
				if found_place != True:
					if player.inventory.food[i] == player.inventory.nothing:
						player.inventory.food[i] = self.items[num]
						self.con_mes = '+['+self.items[num].name+']'
						if real_mes == True:
							message.add('+['+self.items[num].name+']')
						del self.items[num]
						found_place = True
		
		elif self.items[num].inv_slot == 'misc':
			
			self.items[num] = deepcopy(self.items[num]) #only to be sure
			
			found_place = False
			
			for h in range (0, len(player.inventory.misc)):
				if  found_place == False and player.inventory.misc[h] != player.inventory.nothing and player.inventory.misc[h].techID == self.items[num].techID and player.inventory.misc[h].stack_size < player.inventory.misc[h].max_stack_size:
					while self.items[num].stack_size > 0 and player.inventory.misc[h].stack_size < player.inventory.misc[h].max_stack_size:
						player.inventory.misc[h].stack_size += 1
						self.items[num].stack_size -= 1	
					
					self.con_mes = '+['+self.items[num].name+']'
					if real_mes == True:
						message.add('+['+self.items[num].name+']')
						
					found_place = True
			
			for i in range (0, len(player.inventory.misc)):
				
				if found_place != True:
					if player.inventory.misc[i]  == player.inventory.nothing:
						player.inventory.misc[i]  = deepcopy(self.items[num])
						self.con_mes = '+['+self.items[num].name+']'
						if real_mes == True:
							message.add('+['+self.items[num].name+']')
						self.items[num].stack_size = 0
						found_place = True
		
			if self.items[num].stack_size <= 0:
				del self.items[num]
				
			if found_place == False:
				if real_mes == True:
					message.add('Your inventory is full!')
		
		return found_place
						
	def inventory(self, tile_change = True,simulated=False):
		
		if simulated == False:
			sfx.play('loot')
			screen.render_fade(False,True,'loot')
		
		run = True
		
		while run:
			
			if low_res == False:
				s = pygame.Surface((640,360))
			else:
				s = pygame.Surface((320,240))
			
			running = True
			
			num = 0
			
			self.con_mes = '~*~'
			
			while running:
				
				if low_res == False:
					s = pygame.Surface((640,360))
				else:
					s = pygame.Surface((320,240))
				
				bg = pygame.Surface((480,360))
				bg.blit(gra_files.gdic['display'][1],(0,0)) #render background
			
				if low_res == True:
					bg = pygame.transform.scale(bg,(320,240))

				s.blit(bg,(0,0))
			
				text = '~Loot~ [Press ['+key_name['x']+'] to leave]'
				text_image = screen.font.render(text,1,(255,255,255))
				s.blit(text_image,(5,2))#menue title
			
				for i in range (0,len(self.items)):
					
					color = (0,0,0)
					
					if self.items[i].inv_slot == 'equipment':
						if self.items[i].known == True:
							if self.items[i].cursed < 1:#cursed item
								color = (130,0,190)
							elif self.items[i].cursed > 1:#holy item
								color = (100,115,0)
						if self.items[i].state < 11:
							color = (200,0,0)
					elif self.items[i].inv_slot == 'food':
						if self.items[i].rotten == True:
							color = (200,0,0)
					
					if i == num:
						
						if low_res == False:
							s.blit(gra_files.gdic['display'][4],(0,112+num*25))#blit marker
						else:
							s.blit(gra_files.gdic['display'][4],(0,38+num*25))#blit marker
						name = self.items[i].name
						try:
							if self.items[i].stack_size > 1:
								name = name+' '+str(self.items[i].stack_size)+'x'
						except:
							None
						text_string = name + '  >['+key_name['e']+']-loot   ['+key_name['i']+']-info'
						text_image = screen.font.render(text_string,1,color)
						if low_res == False:
							s.blit(text_image,(21,120+i*25))#blit menu_items
						else:
							s.blit(text_image,(21,46+i*25))#blit menu_items
							
					else:
						name = self.items[i].name
						try:
							if self.items[i].stack_size > 1:
								name = name+' '+str(self.items[i].stack_size)+'x'
						except:
							None
						text_image = screen.font.render(name,1,color)
						if low_res == False:
							s.blit(text_image,(21,120+i*25))#blit menu_items
						else:
							s.blit(text_image,(21,46+i*25))#blit menu_items
				
				text_image = screen.font.render(self.con_mes,1,(255,255,255))
				if low_res == True:
					s.blit(text_image,(2,225))
				else:
					s.blit(text_image,(5,335))
				
				if game_options.mousepad == 1 and low_res == False:
					s.blit(gra_files.gdic['display'][8],(480,0)) #render mouse pad
				else:
					s_help = pygame.Surface((160,360))
					s_help.fill((48,48,48))
					s.blit(s_help,(480,0))
				
				if game_options.mousepad == 0 and low_res == False:
					s_help = pygame.Surface((640,360))
					s_help.fill((48,48,48))
					s_help.blit(s,(80,0))
					s = s_help
				
				if low_res == False:
					s = pygame.transform.scale(s,(screen.displayx,screen.displayy))
				
				if simulated == True:
					return s
					
				screen.screen.blit(s,(0,0))
				
				pygame.display.flip()
			
				ui = getch(screen.displayx,screen.displayy,game_options.sfxmode,game_options.turnmode,mouse=game_options.mousepad)
				
				if ui == 'exit':
					global master_loop
					global playing
					global exitgame
					global player
					exitgame = True
					screen.render_load(5)
					save(world,player,time,gods,save_path,os.sep)
					screen.save_tmp_png()
					master_loop = False
					playing = False
					run = False
					return('exit')
				
				if ui == 'x':
					running = False
					run = False
					screen.render_fade(True,False,'screen')
				elif ui == 'e':
					item_num = len(self.items)
					self.loot(num)
					if item_num > len(self.items):
						self.con_mes = '~*~'
						num = 0
				elif ui == 'w':
					self.con_mes = '~*~'
					num -=1
					if num < 0:
						num = len(self.items)-1
				elif ui == 's':
					self.con_mes = '~*~'
					num += 1
					if num > len(self.items)-1:
						num = 0
				elif ui == 'i':
					item = deepcopy(self.items[num])
					try:
						#assuming this is eqipment
						if item.name.find('[D]') != -1:
							txt = texts['decorative_clothes']
						else:
							txt = texts[item.classe]  
					except:
						try:
							if item.name.find('Blueprint') != -1:#assuming this is a misc item
								txt = texts['Blueprint']
							elif item.name.find('Scroll') != -1:
								txt = texts['Scroll']
							elif item.name.find('Spellbook') != -1:
								txt = texts['Spellbook']
							else:
								txt = texts[item.name]
						except:
							try:
								txt = [] #assuming this is a consumable
								txt.append(item.name)
								txt.append(' ')
								if item.satisfy_hunger > 0:
									txt.append('Reduces hunger.')
								if item.satisfy_hunger < 0:
									txt.append('Raises hunger.')
								if item.satisfy_thirst > 0:
									txt.append('Reduces thirst.')
								if item.satisfy_thirst < 0:
									txt.append('Raises thirst.')
								if item.satisfy_tiredness > 0:
									txt.append('Can adrenalise!')
								if item.rise_hunger_max > 0:
									txt.append('Lets you go longer without food.')
								if item.rise_thirst_max > 0:
									txt.append('Lets you go longer without water.')
								if item.rise_tiredness_max > 0:
									txt.append('Lets you go longer without sleep.')
								if item.heal > 0:
									txt.append('Can heal your wounds.')
								if item.heal < 0:
									txt.append('Can hurt you!')
								if item.rise_lp_max > 0:
									txt.append('Raises your max. LP.')
								if item.give_seed > 0:
									txt.append('Seeds can be extracted.')
								if item.rotten:
									txt.append('Rotten food may harm you!')
								elif item.life_period < 720:
									if item.life_period != False:
										txt.append('May rot soon.')
									else:
										txt.append('Won\'t rot.')
								if item.effect != None:
									txt.append('Grants '+item.effect.title())
							except:
								txt = texts['info_soon']#if everything else fails
					screen.render_text(txt)
					
					
				if len(self.items) == 0 and tile_change == True:
					
					if world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][4].techID:#this is a chest
						replace = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace)
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][3])
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = replace
					elif world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].techID == tl.tlist['functional'][25].techID:#this is a fridge
						replace = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace)
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = deepcopy(tl.tlist['functional'][24])
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace = replace
					else:
						world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]] = world.maplist[player.pos[2]][player.on_map].tilemap[player.pos[1]][player.pos[0]].replace
						
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = 0
					message.add('You looted everything.')
					run = False
					break
					
				elif len(self.items) == 0:
					world.maplist[player.pos[2]][player.on_map].containers[player.pos[1]][player.pos[0]] = 0
					message.add('You looted everything.')
					run = False
					break

class time_class():
	
	def __init__(self):
		
		name = save_path + os.sep + 'time.data'
		Time_ready = True
		
		try:
			
			f = open(name, 'rb')
			screen.render_load(6)
			temp = p.load(f)
			self.minute = temp.minute
			self.hour = temp.hour
			self.day = temp.day
			self.day_total = temp.day_total
			self.month = temp.month
			self.year = temp.year
			
		except:
			
			screen.render_load(8)
			
			self.minute = 0
			self.hour = 7
			self.day = 1
			self.day_total = 0
			self.month = 1
			self.year = 1
		
	def tick(self):
		
		Time_ready = True
		
		for i in range(0,len(player.inventory.food)):#let the food rot in the players inventory
			if player.inventory.food[i] != player.inventory.nothing:
					player.inventory.food[i].rot()
		
		for i in range (0,len(world.maplist[player.pos[2]][player.on_map].countdowns)): # check for countdown events
			
					test = world.maplist[player.pos[2]][player.on_map].countdowns[i].countdown()
			
					if test == True:
				
						if world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'door':
							if world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].techID == tl.tlist['building'][2].techID:
								if world.maplist[player.pos[2]][player.on_map].countdowns[i].x != player.pos[0] or world.maplist[player.pos[2]][player.on_map].countdowns[i].y != player.pos[1]:
									if world.maplist[player.pos[2]][player.on_map].npcs[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] == 0: #if there is no player or npc on the same tile like the countdown event
										world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = tl.tlist['building'][3]
										message.add('A door falls shut.')
										sfx.play('locked')
										world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'hot_furnace':
							if world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].techID == tl.tlist['toys'][12].techID:
								replace = world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
								world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = deepcopy(tl.tlist['functional'][14])
								world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace = replace
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'bomb3':
							sfx.play('fuse')
							replace =  world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = tl.tlist['effect'][1]
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace = replace
							world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('bomb2', world.maplist[player.pos[2]][player.on_map].countdowns[i].x, world.maplist[player.pos[2]][player.on_map].countdowns[i].y,1))
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'bomb2':
							sfx.play('fuse')
							replace =  world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = tl.tlist['effect'][2]
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace = replace
							world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('bomb1', world.maplist[player.pos[2]][player.on_map].countdowns[i].x, world.maplist[player.pos[2]][player.on_map].countdowns[i].y,1))
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'bomb1':
							
							for yy in range(world.maplist[player.pos[2]][player.on_map].countdowns[i].y-1,world.maplist[player.pos[2]][player.on_map].countdowns[i].y+2):
								for xx in range(world.maplist[player.pos[2]][player.on_map].countdowns[i].x-1,world.maplist[player.pos[2]][player.on_map].countdowns[i].x+2):
									
									if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] != 0:
										if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].techID == ml.mlist['special'][14].techID: #this is a demonic chest
											world.maplist[player.pos[2]][player.on_map].monster_die(xx,yy)
									
									if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] != 0:
										world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].lp -= 5
										if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].lp < 1:
											world.maplist[player.pos[2]][player.on_map].monster_die(xx,yy)
									world.maplist[player.pos[2]][player.on_map].containers[yy][xx] = 0
									world.maplist[player.pos[2]][player.on_map].make_monsters_angry(xx,yy,'destroy')
									
									if player.pos[0] == xx and player.pos[1] == yy:
										player.lp -= 5
									if player.pet_pos != False and player.pet_on_map != False:
										if player.pet_pos[0] == xx and player.pet_pos[1] == yy and player.on_map == player.pet_on_map:
											player.pet_lp -= 5
											
											if player.pet_lp < 1:
												world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].relation = int(self.npcs[player.pet_pos[1]][player.pet_pos[0]].relation*0.8)
												return_done = False
									
												if 'npc' in world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].properties:
													seeked_tile = tl.tlist['functional'][18]
												else:
													seeked_tile = tl.tlist['sanctuary'][4]
									
												for yyy in range(0,max_map_size):
													for xxx in range(0,max_map_size):
														if world.maplist[0]['elysium_0_0'].tilemap[yyy][xxx].techID == seeked_tile.techID and world.maplist[0]['elysium_0_0'].npcs[yyy][xxx] == 0 and return_done == False:
															string = self.npcs[player.pet_pos[1]][player.pet_pos[0]].name + ' returns home.'
															message.add(string)
															screen.write_hit_matrix(player.pet_pos[0],player.pet_pos[1],7)
															self.npcs[player.pet_pos[1]][player.pet_pos[0]].AI_style = 'ignore'
															world.maplist[0]['elysium_0_0'].npcs[yyy][xxx] = deepcopy(self.npcs[player.pet_pos[1]][player.pet_pos[0]])
															self.npcs[player.pet_pos[1]][player.pet_pos[0]] = 0
															player.pet_pos = False
															player.pet_on_map = False
															return_done = True
									
									if world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].techID != tl.tlist['effect'][4].techID and world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].techID != tl.tlist['effect'][3].techID and world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].techID != tl.tlist['effect'][2].techID and world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].techID != tl.tlist['effect'][1].techID and world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].techID != tl.tlist['effect'][0].techID:#this tile isn't already burning or exploding
										if world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace != None:
											replace =  deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace)
										else:
											replace =  deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx])
									
										if replace == None:
											replace = deepcopy(tl.tlist['functional'][26])
											
										world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx] = deepcopy(tl.tlist['effect'][3])
										world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace = deepcopy(replace)
										world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('boom', xx, yy,1))
										
									else:
										replace =  deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace)
										if replace == None:
											replace = deepcopy(tl.tlist['functional'][26])
										world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx] = deepcopy(tl.tlist['effect'][3])
										world.maplist[player.pos[2]][player.on_map].tilemap[yy][xx].replace = replace
										world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('boom', xx, yy,1))
							
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							sfx.play('boom')
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'boom':
							if world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace != None:
								world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'flame':
							if world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace != None:
								world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'healing_aura' or world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'elbereth':
							if world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'elbereth':
								message.add('The magic word fades.')
							world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x] = world.maplist[player.pos[2]][player.on_map].tilemap[world.maplist[player.pos[2]][player.on_map].countdowns[i].y][world.maplist[player.pos[2]][player.on_map].countdowns[i].x].replace
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'		
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'stasis':
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							if world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:
								world.maplist[player.pos[2]][player.on_map].npcs[y][x].move_border -= 10
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'spawner' or world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'orc_spawner':
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							if world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'orc_spawner':
								map_type = 'orc'
							else:
								map_type = world.maplist[player.pos[2]][player.on_map].map_type
							
							spawn_here = False
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group == 'soil':
								spawn_here = True
							if map_type == 'grot':
								if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group == 'low_liquid':
									spawn_here = True
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].civilisation == True:
								spawn_here = False
							
							if world.maplist[player.pos[2]][player.on_map].npcs[y][x] == 0:
								no_monsters = True
							else:
								no_monsters = False
							
							player_distance = ((player.pos[0]-x)**2+(player.pos[1]-y)**2)**0.5
							
							monster_max = (max_map_size*max_map_size)/30
							#monster_max = int(monster_max * world.maplist[player.pos[2]][player.on_map].monster_num)
							
							if world.maplist[player.pos[2]][player.on_map].monster_count < monster_max:
								if player_distance > 8:
									if spawn_here == True and no_monsters == True:
										ran = random.randint(0,len(ml.mlist[map_type])-1)
										world.maplist[player.pos[2]][player.on_map].npcs[y][x] = deepcopy(ml.mlist[map_type][ran])
										world.maplist[player.pos[2]][player.on_map].set_monster_strength(x,y,player.pos[2])
										try:
											if player.difficulty == 4:
												world.maplist[player.pos[2]][player.on_map].npcs[y][x].AI_style = 'ignore'
										except:
											None
										world.maplist[player.pos[2]][player.on_map].monster_count += 1
							world.maplist[player.pos[2]][player.on_map].countdowns[i].count = random.randint(5,60)
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'spawn_villager' and world.maplist[player.pos[2]][player.on_map].countdowns[i].count < 1:
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['functional'][8].techID:#this is a bed
								if world.maplist[player.pos[2]][player.on_map].npcs[y][x] == 0:
									ran = None
									if len(player.villager['high']) > 0:
										if len(player.villager['high']) == 1:
											ran = player.villager['high'][0]
											del player.villager['high'][0]
										else:
											list_num = random.randint(0,len(player.villager['high'])-1)
											ran = player.villager['high'][list_num]
											del player.villager['high'][list_num]
									elif len(player.villager['medium']) > 0:
										if len(player.villager['medium']) == 1:
											ran = player.villager['medium'][0]
											del player.villager['medium'][0]
										else:
											list_num = random.randint(0,len(player.villager['medium'])-1)
											ran = player.villager['medium'][list_num]
											del player.villager['medium'][list_num]
									elif len(player.villager['low']) > 0:
										if len(player.villager['low']) == 1:
											ran = player.villager['low'][0]
											del player.villager['low'][0]
										else:
											list_num = random.randint(0,len(player.villager['low'])-1)
											ran = player.villager['low'][list_num]
											del player.villager['low'][list_num]
									if ran != None:	
										world.maplist[player.pos[2]][player.on_map].npcs[y][x] = deepcopy(ml.mlist['civilian'][ran])
										world.maplist[player.pos[2]][player.on_map].set_monster_strength(x,y,player.pos[2])
										world.maplist[player.pos[2]][player.on_map].npcs[y][x].personal_id = str(x)+str(y)+str(random.randint(0,9999))+'_villager'
										mes = 'A '+world.maplist[player.pos[2]][player.on_map].npcs[y][x].name+' arrived.'
										message.add(mes)
										world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('despawn_villager',x,y,random.randint(5,60),world.maplist[player.pos[2]][player.on_map].npcs[y][x].personal_id))
										world.maplist[player.pos[2]][player.on_map].monster_count += 1
										world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
									else:
										world.maplist[player.pos[2]][player.on_map].countdowns[i].count = random.randint(5,60)
								else:
									world.maplist[player.pos[2]][player.on_map].countdowns[i].count = random.randint(5,60)
									
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'despawn_villager' and world.maplist[player.pos[2]][player.on_map].countdowns[i].count < 1:
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID != tl.tlist['functional'][8].techID:
								for yy in range(0,max_map_size):
									for xx in range(0,max_map_size):
										if world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] != 0 and world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].personal_id == world.maplist[player.pos[2]][player.on_map].countdowns[i].data:
											mes = 'A '+world.maplist[player.pos[2]][player.on_map].npcs[yy][xx].name+' has left.'
											message.add(mes)
											world.maplist[player.pos[2]][player.on_map].npcs[yy][xx] = 0
											world.maplist[player.pos[2]][player.on_map].monster_count -= 1
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i].count = random.randint(5,60)
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'set_signal':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							world.maplist[player.pos[2]][player.on_map].set_signal(x,y)
							world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'transmitter_off':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['toys'][2].techID:
								replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['toys'][1])
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
								world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('transmitter_ready',x,y,1))
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
								
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'transmitter_ready':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['toys'][1].techID:
								replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['toys'][0])
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'	
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'plate_wait':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['toys'][7].techID:
								if x == player.pos[0] and y == player.pos[1]:
									world.maplist[player.pos[2]][player.on_map].set_signal(x,y)
									sfx.play('click')
									world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
									world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('plate_ready',x,y,1))
								elif world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0:
									if not 'hover' in world.maplist[player.pos[2]][player.on_map].npcs[y][x].properties:
										world.maplist[player.pos[2]][player.on_map].set_signal(x,y)
										dist = (((x-player.pos[0])**2)+((y-player.pos[1])**2))**0.5
										if dist < 9:
											sfx.play('click')
										world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
										world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('plate_ready',x,y,1))
								else:
									world.maplist[player.pos[2]][player.on_map].countdowns[i].count = 1
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'plate_ready':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['toys'][7].techID:
								if ((x != player.pos[0] or y != player.pos[1]) and world.maplist[player.pos[2]][player.on_map].npcs[y][x] == 0) or (world.maplist[player.pos[2]][player.on_map].npcs[y][x] != 0 and 'hover' in world.maplist[player.pos[2]][player.on_map].npcs[y][x].properties):
									dist = (((x-player.pos[0])**2)+((y-player.pos[1])**2))**0.5
									if dist < 9:
										sfx.play('click')
									world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
									world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('plate_wait',x,y,1))
								else:
									world.maplist[player.pos[2]][player.on_map].countdowns[i].count = 1
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'timer_wait':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['toys'][10].techID:
								dist = (((x-player.pos[0])**2)+((y-player.pos[1])**2))**0.5
								if dist < 9:
									sfx.play('buzz')
								world.maplist[player.pos[2]][player.on_map].set_signal(x,y)
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[y][x])
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].tile_pos = (15,14)
								world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('timer_ready',x,y,1))
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
								
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'timer_ready':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['toys'][10].techID:
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(world.maplist[player.pos[2]][player.on_map].tilemap[y][x])
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].tile_pos = (14,14)
								world.maplist[player.pos[2]][player.on_map].countdowns.append(countdown('timer_wait',x,y,3))
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
						
						elif world.maplist[player.pos[2]][player.on_map].countdowns[i].kind == 'gift_to_workbench':
							
							x = world.maplist[player.pos[2]][player.on_map].countdowns[i].x
							y = world.maplist[player.pos[2]][player.on_map].countdowns[i].y
							
							if world.maplist[player.pos[2]][player.on_map].tilemap[y][x].techID == tl.tlist['sanctuary'][0].techID: #this is bar sanctuary floor, ergo the devine gift has already disapeared
								replace = world.maplist[player.pos[2]][player.on_map].tilemap[y][x]
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x] = deepcopy(tl.tlist['functional'][9])#set carpenter's workbench
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].replace = replace
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].damage = -1
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].move_group = 'holy'
								world.maplist[player.pos[2]][player.on_map].tilemap[y][x].build_here = False
								screen.write_hit_matrix(x,y,7)
								message.add('A workbench appears all of a sudden.')
								world.maplist[player.pos[2]][player.on_map].countdowns[i] = 'del'
								sfx.play('lvl_up')
							else:
								world.maplist[player.pos[2]][player.on_map].countdowns[i].count = 2
						
		newcountdown = []
		
		for k in world.maplist[player.pos[2]][player.on_map].countdowns:
			if k != 'del':
				newcountdown.append(k)
				
		world.maplist[player.pos[2]][player.on_map].countdowns = newcountdown
		
		self.minute += 1
		
		if self.hour > 6 and self.hour < 20:
			thirst_multi = world.maplist[player.pos[2]][player.on_map].thirst_multi_day
		else:
			thirst_multi = world.maplist[player.pos[2]][player.on_map].thirst_multi_night
		
		if player.buffs.get_buff('hexed') <= 0:
			change = 1
		else:
			change = 5
			
		if player.buffs.get_buff('poisoned') > 0:
			change = 2
		
		if player.buffs.get_buff('healthy') != 0:
			if player.buffs.get_buff('sick') != 0:
				message.add('You feel a sickness leave your body.')
				player.buffs.remove_buff('sick')
		
		if player.buffs.get_buff('sick') != 0:
			if player.buffs.get_buff('sick')%60 == 0:
				test = False
				if player.attribute.hunger_max > 1000:
					player.attribute.hunger_max -= 5
					test = True
					if player.attribute.hunger > player.attribute.hunger_max:
						player.attribute.hunger = player.attribute.hunger_max
				if player.attribute.thirst_max > 800:
					player.attribute.thirst_max -= 5
					test = True
					if player.attribute.thirst > player.attribute.thirst_max:
						player.attribute.thirst = player.attribute.thirst_max
					
				if test == True:
					message.add('Your sickness lets your stomach shrink.')
			
		if player.attribute.hunger > 0:
			player.attribute.hunger -= change
		if player.attribute.thirst > 0:	
			player.attribute.thirst -= change * thirst_multi
		if player.attribute.tiredness > 0 and player.buffs.get_buff('adrenalised') <= 0:
			player.attribute.tiredness -= change
		
		if player.attribute.hunger <= 0 or player.attribute.thirst <= 0 or player.attribute.tiredness <= 0:
			player.lp -= 1
		
		if player.buffs.get_buff('confused') > 0:
			player.mp = 0
			
		if self.minute % 5 == 0:#every 5th turn
			
			if player.buffs.get_buff('bleeding') <= 0 and player.buffs.get_buff('poisoned') <= 0 and player.buffs.get_buff('hexed') <= 0 and player.lp < player.attribute.max_lp and player.lp >= player.last_lp:
				player.lp += 1
				if player.inventory.check_suffix('Slow Reg.') == True:
					coin = random.randint(0,1)
					if coin == 1:
						player.lp -= 1
				elif player.inventory.check_suffix('Regeneration') == True:
					player.lp += 1
			elif player.buffs.get_buff('bleeding') > 0:
				player.lp -= 1
				message.add('The loss of blood weakens you.')
				
			if player.buffs.get_buff('confused') <= 0:
				if player.mp < player.attribute.max_mp and player.attribute.tiredness > ((player.attribute.tiredness_max/100)*50):
					if player.inventory.check_suffix('Inattention'):
						coin = random.randint(0,1)
						if coin == 1:
							player.mp -= 1
					elif player.inventory.check_suffix('Concentration') == True:
						player.mp += 1
					
					if player.attribute.tiredness > ((player.attribute.tiredness_max/100)*70):
						player.mp += 1
					else:
						coin = random.randint(0,1)
						player.mp += coin
						
					if player.mp == player.attribute.max_mp:
						message.add('You are focused again.')
			else:
				player.mp = 0
				
			if player.buffs.get_buff('instable') > 0:
				coin = random.randint(0,1)
				if coin == 1:
					pos = world.maplist[player.pos[2]][player.on_map].find_all_moveable()
					if pos != False:
						real_pos = []
						for i in pos:
							if world.maplist[player.pos[2]][player.on_map].npcs[i[1]][i[0]] == 0:
								real_pos.append((i[0],i[1]))
						if len(real_pos) > 0:
							screen.render_fade(True,False)
							ran = random.randint(0,len(real_pos)-1)
							player.pos[0] = real_pos[ran][0]
							player.pos[1] = real_pos[ran][1]
							screen.reset_hit_matrix()
							player.stand_check()
							sfx.play('teleport')
							message.add('You randomly teleport around.')
							screen.render_fade(False,True)
		
		if self.minute % 10 == 0:#every 10th turn	
			if player.pet_pos != False and player.pet_on_map != False:
				try:
					if player.pet_lp < world.maplist[player.pet_pos[2]][player.pet_on_map].npcs[player.pet_pos[1]][player.pet_pos[0]].basic_attribute.max_lp:
						player.pet_lp += 1
				except:
					print('[PET ERROR]')
		
		player.last_lp = player.lp
				
		player.buffs.buff_tick()
		
		#Item suffixes
		
		if player.inventory.check_suffix('Pois. Prot.') == True and player.buffs.get_buff('poisoned') > 0:
			message.add('You feel poison leave your body.')
			player.buffs.remove_buff('poisoned')
		
		if player.inventory.check_suffix('Blind Prot.') == True and player.buffs.get_buff('blind') > 0:
			message.add('Your vision returns to normal.')
			player.buffs.remove_buff('blind')
			
		if player.inventory.check_suffix('Hex. Prot.') == True and player.buffs.get_buff('hexed') > 0:
			message.add('You feel a hex falling of from you.')
			player.buffs.remove_buff('hexed')
			
		if player.inventory.check_suffix('Bleed. Prot.') == True and player.buffs.get_buff('bleeding') > 0:
			message.add('A bleeding wound closes immediately.')
			player.buffs.remove_buff('bleeding')
			
		if player.inventory.check_suffix('Instab. Prot.') == True and player.buffs.get_buff('instable') > 0:
			message.add('You feel instability pass away.')
			player.buffs.remove_buff('instable')
			
		if player.inventory.check_suffix('Rage') == True and ((player.lp*100)/player.attribute.max_lp)< 30 and player.buffs.get_buff('berserk') == 0:
			message.add('You feel berserk range rise up in you.')
			player.buffs.set_buff('berserk',30)
		
		if player.inventory.check_suffix('Protection') == True and ((player.lp*100)/player.attribute.max_lp)< 30 and player.buffs.get_buff('ironskin') == 0:
			message.add('You feel your skin get harder.')
			player.buffs.set_buff('ironskin',30)
			
			###################go on here!!!!!!!!!
		
		world.maplist[player.pos[2]][player.on_map].AI_move()
		
		if self.minute > 59:
			
			self.hour += 1
			self.minute = 0
			
			if self.hour > 23:
				
				self.day += 1
				self.day_total +=1
				self.hour = 0
				screen.render_load(5)
				save(world,player,time,gods,save_path,os.sep)#save the game
				
				if self.day > 28:
						
					self.month += 1
					self.day = 1
						
					if self.month > 13:
							
						self.year +=1
						self.month = 1
						self.day_total = 0 #eventually will cause a little bug when the year is changing but prevent the number of total days of become endless big
						
						if self.year > 9999:
							self.year = 0 #just to be save ;-)
				
	def sget(self):
		
		monthnames = ('None', 'Prim', 'Secut', 'Trilus', 'Quarz', 'Vivis', 'Sis', 'Septur', 'Huiles', 'Neurat', 'Dixa', 'Seprim', 'Tweflaf', 'Dritum')
		
		if self.day == 1:
			daystring = '1st'
		elif self.day == 2:
			daystring = '2nd'
		else:
			daystring = str(self.day) + 'th'
			
		if self.hour > 11:
			hourstring = str(self.hour-12)
			ampmstring = 'PM'
		else:
			hourstring = str(self.hour)
			ampmstring = 'AM'	
			
		if len(hourstring) == 1:
			hourstring = '0' + hourstring

		if hourstring == '00':
			hourstring = '12'
			
		if len(str(self.minute)) == 1:
			minutestring = '0' + str(self.minute)
		else:
			minutestring = str(self.minute)	
		
		date = daystring + ' ' + monthnames[self.month]
		time = hourstring + ':' + minutestring + ampmstring
		strings = (date,time)
		
		return strings
	
class gods_class():
	#this class stores the goods mood about the player
	def __init__(self):
		
		name = save_path + os.sep + 'gods.data'
		
		try:
			
			f = open(name, 'rb')
			screen.render_load(14)
			temp = p.load(f)
			self.mood = temp.mood
			
		except:
			
			screen.render_load(13)
			self.mood = 10
			#the mood of goods is raised by good sacrifices at the altar(see mob.enter()) and sinks if their help is needed or the player give them crap
	
	def judgement(self):
		#this function check the mood of the gods and returns a False if they are unhappy about the player or a True if they are happy
		if self.mood > 0:
			return True
		else:
			return False
class sfX():
	
	def __init__(self):
		
		sfx_path = basic_path + os.sep + 'AUDIO' + os.sep + 'SFX' + os.sep
		
		self.sfx_list = {'walk_dry': pygame.mixer.Sound(sfx_path + 'walk_dry.ogg'),
						'walk_wet': pygame.mixer.Sound(sfx_path + 'walk_wet.ogg'),
						'miss': pygame.mixer.Sound(sfx_path + 'miss.ogg'),
						'hit': pygame.mixer.Sound(sfx_path + 'hit.ogg'),
						'fire': pygame.mixer.Sound(sfx_path + 'fire.ogg'),
						'boom': pygame.mixer.Sound(sfx_path + 'boom.ogg'),
						'chop': pygame.mixer.Sound(sfx_path + 'chop.ogg'),
						'break': pygame.mixer.Sound(sfx_path + 'break.ogg'),
						'lvl_up': pygame.mixer.Sound(sfx_path + 'lvl_up.ogg'),
						'steal' : pygame.mixer.Sound(sfx_path + 'steal.ogg'),
						'loot' : pygame.mixer.Sound(sfx_path + 'loot.ogg'),
						'open' : pygame.mixer.Sound(sfx_path + 'open.ogg'),
						'locked' : pygame.mixer.Sound(sfx_path + 'locked.ogg'),
						'immobilized' : pygame.mixer.Sound(sfx_path + 'immobilized.ogg'),
						'item_break' : pygame.mixer.Sound(sfx_path + 'item_break.ogg'),
						'shatter' : pygame.mixer.Sound(sfx_path + 'shatter.ogg'),
						'got_fish' : pygame.mixer.Sound(sfx_path + 'got_fish.ogg'),
						'no_fish' : pygame.mixer.Sound(sfx_path + 'no_fish.ogg'),
						'photo'	: pygame.mixer.Sound(sfx_path + 'photo.ogg'),
						'found' : pygame.mixer.Sound(sfx_path + 'found.ogg'),
						'hit_cage' : pygame.mixer.Sound(sfx_path + 'hit_cage.ogg'),
						'destroy_cage' : pygame.mixer.Sound(sfx_path + 'destroy_cage.ogg'),
						'vampire' : pygame.mixer.Sound(sfx_path + 'vampire.ogg'),
						'flame' : pygame.mixer.Sound(sfx_path + 'flame.ogg'),
						'steam' : pygame.mixer.Sound(sfx_path + 'steam.ogg'),
						'eat' : pygame.mixer.Sound(sfx_path + 'eat.ogg'),
						'drink' : pygame.mixer.Sound(sfx_path + 'drink.ogg'),
						'extract' : pygame.mixer.Sound(sfx_path + 'extract.ogg'),
						'fuse' : pygame.mixer.Sound(sfx_path + 'fuse.ogg'),
						'throw' : pygame.mixer.Sound(sfx_path + 'throw.ogg'),
						'pickup' : pygame.mixer.Sound(sfx_path + 'pickup.ogg'),
						'place' : pygame.mixer.Sound(sfx_path + 'place.ogg'),
						'remove' : pygame.mixer.Sound(sfx_path + 'remove.ogg'),
						'teleport' : pygame.mixer.Sound(sfx_path + 'teleport.ogg'),
						'craft' : pygame.mixer.Sound(sfx_path + 'craft.ogg'),
						'alchemy' : pygame.mixer.Sound(sfx_path + 'alchemy.ogg'),
						'portal' : pygame.mixer.Sound(sfx_path + 'portal.ogg'),
						'shop' : pygame.mixer.Sound(sfx_path + 'shop.ogg'),
						'aura' : pygame.mixer.Sound(sfx_path + 'aura.ogg'),
						'autodoor' : pygame.mixer.Sound(sfx_path + 'autodoor.ogg'),
						'win' : pygame.mixer.Sound(sfx_path + 'win.ogg'),
						'buzz' : pygame.mixer.Sound(sfx_path + 'buzz.ogg'),
						'click' : pygame.mixer.Sound(sfx_path + 'click.ogg'),
						'click2' : pygame.mixer.Sound(sfx_path + 'click2.ogg'),
						'lever' : pygame.mixer.Sound(sfx_path + 'lever.ogg'),
						'jump' : pygame.mixer.Sound(sfx_path + 'jump.ogg'),
						'stonecutter' : pygame.mixer.Sound(sfx_path + 'stonecutter.ogg'),
						'forger' : pygame.mixer.Sound(sfx_path + 'forger.ogg'),
						'plant' : pygame.mixer.Sound(sfx_path + 'plant.ogg'),
						'got_item' : pygame.mixer.Sound(sfx_path + 'got_item.ogg'),
						'got_quest' : pygame.mixer.Sound(sfx_path + 'got_quest.ogg'),
						'holy' : pygame.mixer.Sound(sfx_path + 'holy.ogg'),
						'thunder' : pygame.mixer.Sound(sfx_path + 'thunder.ogg'),
						'identify' : pygame.mixer.Sound(sfx_path + 'identify.ogg'),
						'spell_fail' : pygame.mixer.Sound(sfx_path + 'spell_fail.ogg'),
						'rock_break' : pygame.mixer.Sound(sfx_path + 'rock_break.ogg'),
						}
	def set_loudness(self):
		
		name_list = self.sfx_list.keys()
		
		for i in name_list:
			self.sfx_list[i].set_volume(game_options.sfxmode)
							
	def play(self,sfx_name):
		
		try:
			if pygame.mixer.get_busy():
				sleep(0.1)
				
			if game_options.sfxmode != 0:
				self.sfx_list[sfx_name].play()
		except:
			print('SFX error')
				
class bgM():
	
	def  __init__(self):
		
		self.song_played_now = 'No'
		self.last_song = 'No'
	
	def set_volume(self):
		try:
			if world.maplist[player.pos[2]][player.on_map].music_day != world.maplist[player.pos[2]][player.on_map].music_night:
				if time.hour == 5:
					pygame.mixer.music.set_volume((1-(time.minute/60))*game_options.bgmmode)
				elif time.hour == 6:
					pygame.mixer.music.set_volume((time.minute/60)*game_options.bgmmode)
				elif time.hour == 19:
					pygame.mixer.music.set_volume((1-(time.minute/60))*game_options.bgmmode)
				elif time.hour == 20:
					pygame.mixer.music.set_volume((time.minute /60)*game_options.bgmmode)
				else:
					pygame.mixer.music.set_volume(game_options.bgmmode)
			else:
				pygame.mixer.music.set_volume(game_options.bgmmode)
		except:
			print('BGM:Error')
		
	def check_for_song(self,play_menu_sound = False,force_play = False):
		
		music_path = basic_path + os.sep + 'AUDIO' + os.sep + 'BGM' + os.sep
		
		try:
			if play_menu_sound == False:
				if time.hour < 6 or time.hour > 19:
					test = self.song_played_now = world.maplist[player.pos[2]][player.on_map].music_night
				else:
					test = self.song_played_now = world.maplist[player.pos[2]][player.on_map].music_day
		except:
			play_menu_sound = True
		
		if game_options.bgmmode != 0 and play_menu_sound == False:
			if force_play == False:
				if time.hour < 6 or time.hour > 19:
					test = self.song_played_now = world.maplist[player.pos[2]][player.on_map].music_night
				else:
					test = self.song_played_now = world.maplist[player.pos[2]][player.on_map].music_day
			else:
				self.last_song = 'FOO'
		else:
			pygame.mixer.music.stop()
		
		if play_menu_sound == False and game_options.bgmmode != 0:
			self.set_volume()
		
		if self.song_played_now != self.last_song and play_menu_sound == False and game_options.bgmmode != 0:
			
			try:
				pygame.mixer.music.stop()
			except:
				None
				
			track = music_path + self.song_played_now + '.ogg'
			
			pygame.mixer.music.load(track)
			pygame.mixer.music.play(-1)
		
		elif play_menu_sound == True and game_options.bgmmode != 0:
			
			track = music_path + 'menu.ogg'
			
			pygame.mixer.music.load(track)
			pygame.mixer.music.play(-1)
			pygame.mixer.music.set_volume(game_options.bgmmode)
		
		self.last_song = self.song_played_now


def main():
	
	if cheat_mode == True:
		print('Cheat mode activated!')
		if sys.version_info < (3,0):
			ui = raw_input('Press ENTER to continue.')
		else:
			ui = input('Press ENTER to continue.')
	
	global key_name	
	global screen
	global gra_files
	global tl
	global il
	global ml
	global ql
	global bgm
	global world
	global gods
	global message
	global player
	global time
	global exitgame
	global playing
	global dialog
	global sfx
	global master_loop
	global game_options
	
	sfx = sfX()
	screen = g_screen()
	screen.render_load(21)
	gra_files = g_files()
	
	if game_options.input_nomination == 0:
		key_name = {'e':'e','b':'b','x':'x','f':'f','i':'i','.':'.','wasd':'w,s,a,d','ws':'w,s'}
	elif game_options.input_nomination == 1:
		key_name = {'e':'1','b':'3','x':'2','f':'5','i':'4','.':'6','wasd':'D-Pad','ws':'D-Pad'}
	else:
		key_name = {'e':'A','b':'X','x':'B','f':'R','i':'Y','.':'R','wasd':'D-Pad','ws':'D-Pad'}
	
	tl = tilelist()
	il = itemlist()
	ml = monsterlist()
	ql = questlist()
	dialog = dialog()
	master_loop = True
	while master_loop:
		bgm = bgM()
		bgm.check_for_song(True,True)
		master_loop = screen.render_main_menu()	
		if playing == True:
			exitgame = False
			time = time_class()
			world = world_class(tl)
			gods = gods_class()
			message = messager()
			p_attribute = attribute(2,2,2,2,2,10,10)
			p_inventory = inventory()
			player = player_class ('Testificate', 'elysium_0_0', p_attribute,p_inventory)
			mes = 'Welcome to Roguebox Adventures[' + version +']'
			message.add(mes)
			player.stand_check()
			bgm.check_for_song()
			save(world,player,time,gods,save_path,os.sep)
			time.tick()
		
			running = True
	
			while running:
				
				world.maplist[player.pos[2]][player.on_map].time_pass() #make the changes of passing time every new day 
				
				screen.render(0)
				
				if len(message.mes_list) > 5:
					message.clear()
				
				move_border = 0
		
				bodyparts = ('Head', 'Body', 'Legs' , 'Feet')
		
				for i in bodyparts:
			
					if player.inventory.wearing[i] != player.inventory.nothing:
						move_border += 1
				
				if player.buffs.get_buff('drunk') != 0:
					move_border += 2
					if move_border > 8:
						move_border = 8
				
				move_chance = random.randint(1,9)
				if move_border < move_chance:
					screen.reset_hit_matrix()
					plus = 1
					r = True
					while r:
						test = player.user_input()
						if test == 'next_mes':
							screen.render(0)
						else:
							message.more_messages = False
							r = False
				
				if exitgame == True:
					running = False
					playing = False

if __name__ != '__main__':
	
	everything_fine = True
	
	try:
		main()
	except Exception as e:
		import traceback
		everything_fine = False
		exc_type, exc_obj, exc_tb = sys.exc_info()
		bs = save_path
		for c in range(0,9):
			bs = bs.replace('/World'+str(c),'')
		logfile = bs + os.sep + 'debug.txt'
		f = open(logfile,'a')
		f.write('###############################################')
		f.write('\n')
		traceback.print_exception(exc_type, exc_obj, exc_tb, limit=9, file=f)
		f.close()
	finally:
		if everything_fine == False:
			screen.render_crash()
else:
	import run	
