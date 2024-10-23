from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image=pygame.Surface((100,100))
        self.image.fill('red')
        self.rect=self.image.get_frect(center=pos)
        self.direction=vector()
        
    def input(self):
        keys=pygame.key.get_pressed()
        input_vector=vector(0,0)
        
        #속도 결정
        if keys[pygame.K_LCTRL]:  #컨트롤이 달리기 키
            velocity=5    
        elif keys[pygame.K_LSHIFT]: #쉬프트가 은신 키
            velocity=0.5
        else:  #기본 달리기
            velocity=1  
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if keys[pygame.K_UP] and keys[pygame.K_w]:
                input_vector.y-=1
            else:
                input_vector.y-=1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                input_vector.y+=1    
            else:
                input_vector.y+=1 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                input_vector.x+=1    
            else:
                input_vector.x+=1  
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x-=1
            else:
                input_vector.x-=1
                
        if input_vector.magnitude()!=0:
            input_vector=input_vector/input_vector.magnitude()*velocity
        self.direction=input_vector
    
    def move(self, dt):
        self.rect.center+=self.direction*dt
    
    def update(self, dt):
        self.input()
        self.move(dt)