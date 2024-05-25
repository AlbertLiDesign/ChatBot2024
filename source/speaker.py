import pygame
import time

def play_voice(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    time.sleep(1)  # 增加0.5秒延迟，确保音频文件完全加载
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.mixer.quit()  # add this line to stop pygame mixer after playing the sound