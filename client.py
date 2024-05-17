import pygame
from network import Network

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p, scores):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player", 1, (255, 0, 0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("You", 1, (0, 255, 255))
        win.blit(text, (120, 200))
        

        text = font.render("Opponent", 1, (0, 255, 255))
        win.blit(text, (380, 200))
        
        

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if not game.p1Went:  # Nếu player 1 chưa chọn nước đi
                text1 = font.render("Waiting...", 1, (0, 0, 0))
            else:  # Nếu player 1 đã chọn nước đi
                if p == 0:  # Nếu đến lượt của player 1
                    text1 = font.render(move1, 1, (0, 0, 0))
                    if not game.p2Went:  # Nếu player 2 chưa chọn nước đi
                        text2 = font.render("Waiting...", 1, (0, 0, 0))
                    else:  # Nếu player 2 đã chọn nước đi
                        text2 = font.render(move2, 1, (0, 0, 0))
                else:  # Nếu không phải là lượt của player 1
                    text1 = font.render("Locked In", 1, (0, 0, 0))

            if not game.p2Went:  # Nếu player 2 chưa chọn nước đi
                text2 = font.render("Waiting...", 1, (0, 0, 0))
            else:  # Nếu player 2 đã chọn nước đi
                if p == 1:  # Nếu đến lượt của player 2
                    text2 = font.render(move2, 1, (0, 0, 0))
                    if not game.p1Went:  # Nếu player 1 chưa chọn nước đi
                        text1 = font.render("Waiting...", 1, (0, 0, 0))
                    else:  # Nếu player 1 đã chọn nước đi
                        text1 = font.render(move1, 1, (0, 0, 0))
                else:  # Nếu không phải là lượt của player 2
                    text2 = font.render("Locked In", 1, (0, 0, 0))
                
                
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
            
        for btn in btns:
            btn.draw(win)

    pygame.display.update()





btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)), Button("Paper", 450, 500, (0, 255, 0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            scores = game.get_scores()
        except:
            run = False
            print("Couldn't get game")
            break
        
        
        
        if game.bothWent():
            redrawWindow(win, game, player, scores)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            
            
            if game.check_winner() != -1:
                text = font.render("Player",game.check_winner() + 1 , "won the game!", 1, (255, 0, 0))
                print(scores)
                scores = [0, 0] 
                run = False
            
            font = pygame.font.SysFont("comicsans", 90)
            
            if (game.winner() == player):
                text = font.render("You Won!", 1, (255, 0, 0)) 
                scores = game.update_scores(player)
                print(scores)
            elif game.winner() == -1:
                text = font.render("Tie Game", 1, (255, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
                scores = game.update_scores(1-player)
                print(scores)

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            
            
              

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        
        redrawWindow(win, game, player, scores)

def menu_screen(run):
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        play_text = font.render("Play Game", 1, (255, 0, 0))
        exit_text = font.render("Exit Game", 1, (255, 0, 0))
        
        play_x = (width - play_text.get_width()) // 2
        exit_x = (width - exit_text.get_width()) // 2
        
        
        win.blit(play_text, (play_x, 200))
        win.blit(exit_text, (exit_x, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 100 <= pos[0] <= 100 + play_text.get_width() and 200 <= pos[1] <= 200 + play_text.get_height():
                    run = False
                    main()
                elif 100 <= pos[0] <= 100 + exit_text.get_width() and 300 <= pos[1] <= 300 + exit_text.get_height():
                    pygame.quit()
                    run = False

run = True
while run:
    menu_screen(run)