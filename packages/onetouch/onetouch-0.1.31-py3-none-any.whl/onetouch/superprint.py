colors = {
    'default': '\033[0m',  # 默认颜色
    'black': '\033[30m',  # 黑色文本
    'red': '\033[31m',  # 红色文本
    'green': '\033[32m',  # 绿色文本
    'yellow': '\033[33m',  # 黄色文本
    'blue': '\033[34m',  # 蓝色文本
    'magenta': '\033[35m',  # 品红色文本
    'cyan': '\033[36m',  # 青色文本
    'white': '\033[37m',  # 白色文本
    'bright_black': '\033[90m',  # 灰色（变亮的黑色文本）
    'bright_red': '\033[91m',  # 亮红色文本
    'bright_green': '\033[92m',  # 亮绿色文本
    'bright_yellow': '\033[93m',  # 亮黄色文本
    'bright_blue': '\033[94m',  # 亮蓝色文本
    'bright_magenta': '\033[95m',  # 亮品红色文本
    'bright_cyan': '\033[96m',  # 亮青色文本
    'bright_white': '\033[97m'  # 亮白色文本
}


class Style:
    def __init__(self, style=None, morphology=None):
        self.style = style
        self.morphology = morphology
        self.list_style = []

        self.__convert_morphology(self.morphology)
        self.__convert_style()

        self.font = self.__connect_style()

    class Color:
        black = '\033[30m'  # 黑色文本
        red = '\033[31m'  # 红色文本
        green = '\033[32m'  # 绿色文本
        yellow = '\033[33m'  # 黄色文本
        blue = '\033[34m'  # 蓝色文本
        magenta = '\033[35m'  # 品红色文本
        cyan = '\033[36m'  # 青色文本
        white = '\033[37m'  # 白色文本
        bright_black = '\033[90m'  # 灰色（变亮的黑色文本）
        bright_red = '\033[91m'  # 亮红色文本
        bright_green = '\033[92m'  # 亮绿色文本
        bright_yellow = '\033[93m'  # 亮黄色文本
        bright_blue = '\033[94m'  # 亮蓝色文本
        bright_magenta = '\033[95m'  # 亮品红色文本
        bright_cyan = '\033[96m'  # 亮青色文本
        bright_white = '\033[97m'  # 亮白色文本

    class BackgroundColor:
        black = '\033[40m'  # 黑色背景
        red = '\033[41m'  # 红色背景
        green = '\033[42m'  # 绿色背景
        yellow = '\033[43m'  # 黄色背景
        blue = '\033[44m'  # 蓝色背景
        magenta = '\033[45m'  # 品红色背景
        cyan = '\033[46m'  # 青色背景
        white = '\033[47m'  # 白色背景
        bright_black = '\033[100m'  # 灰色背景（变亮的黑色）
        bright_red = '\033[101m'  # 亮红色背景
        bright_green = '\033[102m'  # 亮绿色背景
        bright_yellow = '\033[103m'  # 亮黄色背景
        bright_blue = '\033[104m'  # 亮蓝色背景
        bright_magenta = '\033[105m'  # 亮品红色背景
        bright_cyan = '\033[106m'  # 亮青色背景
        bright_white = '\033[107m'  # 亮白色背景

    def __convert_style(self):
        if self.style is not None:
            attributes = self.style.split(';')[:-1]  # Removing the last empty string after the last semicolon
            attributes = {attr.split(':')[0].strip(): attr.split(':')[1].strip() for attr in attributes}
            self.__convert_morphology(attributes)

    def __convert_morphology(self, morphology):
        if morphology is not None:
            for key, value in morphology.items():
                if key == 'color':
                    self.list_style.append(getattr(Style.Color, value))
                elif key == 'backgroundcolor':
                    self.list_style.append(getattr(Style.BackgroundColor, value))
                elif key == 'bold':
                    if value:
                        self.list_style.append('\033[1m')
                    else:
                        self.list_style.append('\033[21m')
                elif key == 'faint':
                    if value:
                        self.list_style.append('\033[2m')
                    else:
                        self.list_style.append('\033[1m')
                elif key == 'italic':
                    if value:
                        self.list_style.append('\033[3m')
                    else:
                        self.list_style.append('\033[23m')
                elif key == 'underline':
                    if value:
                        self.list_style.append('\033[4m')
                    else:
                        self.list_style.append('\033[24m')
                elif key == 'reverse':
                    if value:
                        self.list_style.append('\033[7m')
                    else:
                        self.list_style.append('\033[27m')
                elif key == 'crossed-out':
                    if value:
                        self.list_style.append('\033[9m')
                    else:
                        self.list_style.append('\033[29m')

    def __connect_style(self):
        if self.list_style:
            list_style = ''.join(self.list_style)
            return list_style
        else:
            return ''


def prints(self, *args, display: bool = True, style: str = None, morphology: dict = None, recover: bool = True, sep='',
           end='\n', file=None):
    styles = Style(style, morphology)

    if recover:
        recovers = '\033[0m'
    else:
        recovers = ''

    if display:
        print(f'{styles.font}' + self, *args, recovers, sep=sep, end=end, file=file)


def printc(self, *args, display: bool = True, color: str = None, sep=' ', end='\n', file=None) -> None:
    color = color.lower()
    color = colors.get(color, colors['default'])

    if display:
        print(f'{color}' + self, *args, '\033[0m', sep=sep, end=end, file=file)
