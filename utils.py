SCREEN_WIDTH = 150
SCREEN_HEIGHT = 140
BATTLE_WIDTH = 120
BATTLE_HEIGHT = SCREEN_HEIGHT
SPACESHIP_OFFSET_5x4 = 0x0500
SPACESHIP_OFFSET_6x5 = 0x0600
FONT_OFFSET = 0x4000
LEVEL_OFFSET = 0x1000
ALIEN_FINISH = BATTLE_HEIGHT - 40
PLAYER_SPEED = 1
BULLET_SPEED = 2


# there probably is a better way to load fonts in different size than the tiles
def translate_text(s):
    ret = ""
    for line in s.splitlines():
        if ret:
            ret += "\n"
        if line == "":
            ret += "\n\n\n"
        else:
            ret += "".join([chr(ord(c) + FONT_OFFSET) for c in line])
    print(s, ret)
    return ret
