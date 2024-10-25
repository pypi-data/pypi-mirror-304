from colorama import Fore, Style

class banner:
    def __init__(self):
        self.blue = Fore.BLUE
        self.green = Fore.GREEN
        self.red = Fore.RED
        self.yellow = Fore.YELLOW
        self.white = Fore.WHITE
        self.reset = Style.RESET_ALL

    def create_banner(self, game_name: str):
        # Create banner with game name
        banner = f"""
{self.cyan}
\n\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  {self.white}ZENON FOX {self.red}✚{self.white} MINIAPP BOT {self.cyan}┃         {self.white}COPYRIGHT BY Zennon{self.cyan}
┣━━━━━━━━━━━━━━━━━━━━━━━━━━┫  {self.white}⟨⟨⟨{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.white}⟩⟩⟩{self.cyan}
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀ {self.cyan}┃     {self.blue} GITHUB    {self.cyan}➤ {self.white}github.com/foxZenonn{self.cyan}
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠙⠻⢶⣄⡀⠀⠀⠀⢀⣤⠶⠛⠛⡇ {self.cyan}┃
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⣙⣿⣦⣤⣴⣿⣁⠀⠀⣸⠇ {self.cyan}┃      {self.blue}TG OWNER  {self.cyan}➤{self.white} t.me/FoxZenon{self.cyan}
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣡⣾⣿⣿⣿⣿⣿⣿⣿⣷⣌⠋⠀ {self.cyan}┃⠀
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣷⣄⡈⢻⣿⡟⢁⣠⣾⣿⣦⠀ {self.cyan}┃      {self.blue}TG GROUP  {self.cyan}➤{self.white} t.me/zzenonFox{self.cyan}
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⠘⣿⠃⣿⣿⣿⣿⡏⠀ {self.cyan}┃  {self.white}⟨⟨⟨{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.white}⟩⟩⟩{self.cyan}
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠈⠛⣰⠿⣆⠛⠁⠀⡀⠀⠀ {self.cyan}┃             {self.white}YOUR PLAY GAME{self.cyan}
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣦⠀⠘⠛⠋⠀⣴⣿⠁⠀⠀ {self.cyan}┃  {self.white}⟨⟨⟨{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.white}⟩⟩⟩{self.cyan}
┃{self.yellow}⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⣏⠀⠀ ⠀{self.cyan}┃      {self.blue}GAME{self.cyan} ➤{self.white} {game_name} {self.cyan}
┃{self.yellow}⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠀⠀⠀⠾⢿⣿⠀⠀ ⠀{self.cyan}┃            {self.red}●   {self.yellow}●   {self.blue}●   {self.white}●   {self.cyan}
┃{self.yellow}⠀⠀⣠⣿⣿⣿⣿⣿⣿⡿⠟⠋⣁⣠⣤⣤⡶⠶⠶⣤⣄⠈⠀⠀ ⠀{self.cyan}┃          ┏━━━━━━━━━━━━━━━┓
┃{self.yellow}⠀⢰⣿⣿⣮⣉⣉⣉⣤⣴⣶⣿⣿⣋⡥⠄⠀⠀⠀⠀⠉⢻⣄⠀ ⠀{self.cyan}┃          ┃{self.magenta}╔═╗╔═╗╔╗╔╔═╗╔╗╔{self.cyan}┃
┃{self.yellow}⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣋⣁⣤⣀⣀⣤⣤⣤⣤⣄⣿⡄⠀ {self.cyan}┃          ┃{self.magenta}╔═╝║╣ ║║║║║║║║║{self.cyan}┃
┃{self.yellow}⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⠁⠀⠀⠀⠀⠈⠛⠃⠀ {self.cyan}┃          ┃{self.magenta}╚═╝╚═╝╝╚╝╚═╝╝╚╝{self.cyan}┃
┃{self.yellow}⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {self.cyan}┃          ┗━━━━━━━━━━━━━━━┛
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛  {self.white}⟨⟨⟨{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.blue}━{self.red}━{self.white}━{self.yellow}{self.red}━{self.white}━{self.yellow}━{self.green}━{self.magenta}━{self.black}━{self.white}⟩⟩⟩{self.cyan}
  {self.reset}
"""
        return banner

banner = banner()