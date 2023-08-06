import os, typing, colorama
class Color:
	def __init__(self, extensionlog: bool = False):
		self.extbool = extensionlog
	def dirListColor(self, dir, color: typing.Literal['LightBlue', 'Blue'], extension: str = 'py'):
		"""The Color Syntax Return Of A Dir"""
		thecolorlist = []
		if self.extbool == True:
			print(f'{colorama.Fore.RED}WARNING: {colorama.Style.BRIGHT}THIS IS ONLY FOR DEBBUGING{colorama.Style.NORMAL}{colorama.Fore.RESET}\nExtension: .{extension}')
		for every in os.listdir(dir):
			if os.path.isdir(every):
				if color == 'Blue':
					thecolorlist.append(colorama.Style.BRIGHT + colorama.Fore.BLUE + every + colorama.Fore.RESET + colorama.Style.NORMAL)
				elif color == 'LightBlue':
					thecolorlist.append(colorama.Style.BRIGHT + colorama.Fore.CYAN + every + colorama.Fore.RESET + colorama.Style.NORMAL)
				else:
					raise ValueError(f'INVALID CHOICE \'{color.upper()}\', Choose LightBlue Or Blue')
			elif every.endswith('.'+extension):
				thecolorlist.append(colorama.Style.BRIGHT + colorama.Fore.YELLOW + every.split('.'+extension)[0] + colorama.Fore.RESET + colorama.Style.NORMAL)
			else:
				thecolorlist.append(colorama.Style.BRIGHT + colorama.Fore.GREEN + every + colorama.Fore.RESET + colorama.Style.NORMAL)
		return thecolorlist
	def dirJsonColor(self, dir, color: typing.Literal['LightBlue', 'Blue'], extension: str = 'py'):
		"""The Color Syntax Return Of A Dir But In JSON"""
		inc = 0
		thecolorlist = {'files' : [], 'ext_files': [], 'dirs': []}
		for every in os.listdir(dir):
			if os.path.isdir(every):
				if color == 'Blue':
					thecolorlist['dirs'].append(colorama.Style.BRIGHT + colorama.Fore.BLUE + every + colorama.Fore.RESET + colorama.Style.NORMAL)
				elif color == 'LightBlue':
					thecolorlist['dirs'].append(colorama.Style.BRIGHT + colorama.Fore.CYAN + every + colorama.Fore.RESET + colorama.Style.NORMAL)
				else:
					raise ValueError(f'INVALID CHOICE \'{color.upper()}\', Choose LightBlue Or Blue')
			elif every.endswith('.'+extension):
				thecolorlist['ext_files'].append( colorama.Style.BRIGHT + colorama.Fore.YELLOW + every.split('.'+extension)[0] + colorama.Fore.RESET + colorama.Style.NORMAL)
			else:
				thecolorlist['files'].append(colorama.Style.BRIGHT + colorama.Fore.GREEN + every + colorama.Fore.RESET + colorama.Style.NORMAL)
		return thecolorlist