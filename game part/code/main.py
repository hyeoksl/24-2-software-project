from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join
from level import Level
from sprites import Sprite
from entities import Player
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Software Project")
        self.clock=pygame.time.Clock()
        
        #groups
        self.all_sprites=AllSprites()
        
        self.level=Level()
        
        self.import_assets()
        #수정 요망 - 현재 위치가 어느 마을인지에 따라 다른 월드맵을 그려야 함.
        self.setup(self.tmx_maps['world'], 'house')
    
    def import_assets(self):
        #맵 가져오기 - 수정 요망
        #마을 당 맵 하나 이렇게 설정할 텐데 마을이 여러 개면 다 가져와야 함
        self.tmx_maps = {'world': load_pygame(join('..','data','maps','world.tmx'))}
        
    def setup(self, tmx_map, player_start_pos):
        #월드맵 그리기 - 수정 요망
        print(tmx_map)
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles(): #tmx file에 따라 나뉜다
            Sprite((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites)
            
        #플레이어 스타팅 포인트 - 수정 요망
        #플레이어 스타팅 포인트를 랜덤하게 설정하는 다른 로직을 짤 것.
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name=='Player' and obj.properties['pos']==player_start_pos:
                self.player=Player((obj.x, obj.y), self.all_sprites)

    def run(self):
        while True:
            # event loop
            self.clock.tick(FPS)
            dt=self.clock.tick()/1000
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            # game logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            self.level.run()
            pygame.display.update()
            
if __name__=='__main__':
    game=Game()
    game.run()