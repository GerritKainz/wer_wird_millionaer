import pygame, json, keyboard, random, sys
from time import sleep, time
from pygame import Vector2

class Game():
    def __init__(self):
        self.quest_value = {0: 0, 1: 50, 2: 100, 3: 200, 4: 300, 5: 500, 6: 1_000, 7: 2_000, 8: 4_000, 9: 8_000, 10: 16_000, 11: 32_000, 12: 64_000, 13: 125_000, 14: 500_000, 15: 1_000_000}
        self.question = ''
        self.answer1 = ''
        self.answer2 = ''
        self.answer3 = ''
        self.answer4 = ''
        self.corr_answ = ''
        self.current_cat = 1
        self.won_money = 0
        self.stopped_game =    False
        self.questionrect =    pygame.rect.Rect(50, 600, screen_width-  100, 50) #top
        self.answerrect1 =     pygame.rect.Rect(50, 675, (screen_width - 150) / 2, 50) #topleft
        self.answerrect2 =     pygame.rect.Rect(self.answerrect1.right + 50, 675, (screen_width - 150) / 2, 50) #topright
        self.answerrect3 =     pygame.rect.Rect(50, 750, (screen_width - 150) / 2, 50) #bottomleft
        self.answerrect4 =     pygame.rect.Rect(self.answerrect3.right + 50, 750, (screen_width - 150) / 2, 50) #bottomright
        self.menustartrect =   pygame.rect.Rect(screen_width / 2 - 50, 800, 100, 50)
        self.failedrect =      pygame.rect.Rect(screen_width/2 - 220, 250, 440, 200)
        self.returnmenurect =  pygame.rect.Rect(self.failedrect.left,    self.failedrect.centery, 220, 100)
        self.restartrect =     pygame.rect.Rect(self.failedrect.centerx, self.failedrect.centery, 220, 100)
        self.pause_button_rect=pygame.rect.Rect(20, 10, 50, 50)
        self.exitbuttonrect =  pygame.rect.Rect(screen_width - 70, 20, 50, 50)
        self.normal_color =    (41, 41, 139)
        self.selected_color =  (255, 140, 10)
        self.correct_color =   (10, 150, 10)
        self.wrong_color =     (255, 10, 10)
        self.fifthyfifthycolor=(250, 50, 0)
        self.selected_answ = 0 #currently clicked answer
        self.correct_answer = 0
        self.wrong_answer = 0
        self.state = 'menu'
        self.jokers_used = [False, False, False, False] #50 50, telephone, audienceall, audienceone
        self.fifthyfifthyimg = pygame.transform.scale(pygame.image.load('pictures/50_50_joker.png')      , (69, 50))
        self.telephoneimg    = pygame.transform.scale(pygame.image.load('pictures/telephone_joker.png')  , (69, 50))
        self.audienceallimg  = pygame.transform.scale(pygame.image.load('pictures/audienceall_joker.png'), (69, 50))
        self.audienceoneimg  = pygame.transform.scale(pygame.image.load('pictures/audienceone_joker.png'), (69, 50))
        self.exitbuttonimg   = pygame.image.load('pictures/exit_button.png').convert_alpha()
        self.exitbuttonimg.set_colorkey((255, 255, 255))
        self.fifthyfifthyimg.set_colorkey(self.normal_color)
        self.telephoneimg   .set_colorkey(self.normal_color)
        self.audienceallimg .set_colorkey(self.normal_color)
        self.audienceoneimg .set_colorkey(self.normal_color)
        self.fifthyfifthyrect   = self.fifthyfifthyimg.get_rect(topright = (screen_width - 20, 120))
        self.telephonerect      = self.telephoneimg.get_rect(   topright = (screen_width - 20, 180))
        self.audienceallrect    = self.audienceallimg.get_rect( topright = (screen_width - 20, 240))
        self.audienceonerect    = self.audienceoneimg.get_rect( topright = (screen_width - 20, 300))
        self.questioncategoryrect = pygame.rect.Rect(screen_width - 170, 50, 150, 50)
        self.fifthyfifthyindex  = [None, None] #list of unselected answers by 50 50 joker
        self.telephonecorrect   = 70  #percent
        self.audienceonecorrect = 80 #percent
        self.audienceallcorrect = [45, 60] #percent, lower and upper boundary, at least 45
        self.audienceallrange   = [0.1, 0.5] #lower and upper boundary for second and third answers
        self.telephoneanswerrect = pygame.rect.Rect(0, 0, 300, 180)
        self.telephoneanswerrect.center = (screen_width * 0.2, screen_height * 0.25)
        self.showaudienceall = False
        self.showtelephone = False #also for audienceone
        self.correctindex = 0
        self.index = 0
        self.phrase = 0
        self.percentlist = []

    def get_question(self, categorie):
        self.list = random.choice(data[f'{categorie}'])
        self.question = self.list[0]
        self.answer1 = self.list[1]
        self.answer2 = self.list[2]
        self.answer3 = self.list[3]
        self.answer4 = self.list[4]
        self.corr_answ = self.list[5]
        self.fifthyfifthyindex = [None, None]
        print('\n',self.list[:-1])

    def show_gui(self):
        pygame.draw.rect(screen, self.normal_color, self.questionrect)
        if self.correct_answer == 1: pygame.draw.rect(screen, self.correct_color, self.answerrect1) 
        elif self.wrong_answer == 1:   pygame.draw.rect(screen, self.wrong_color, self.answerrect1)  
        elif self.selected_answ == 1:  pygame.draw.rect(screen, self.selected_color, self.answerrect1) 
        elif self.fifthyfifthyindex[0] == 1 or self.fifthyfifthyindex[1] == 1: pygame.draw.rect(screen, self.fifthyfifthycolor, self.answerrect1)
        else: pygame.draw.rect(screen, self.normal_color, self.answerrect1)
        if self.correct_answer == 2: pygame.draw.rect(screen, self.correct_color, self.answerrect2) 
        elif self.wrong_answer == 2:   pygame.draw.rect(screen, self.wrong_color, self.answerrect2)  
        elif self.selected_answ == 2:  pygame.draw.rect(screen, self.selected_color, self.answerrect2) 
        elif self.fifthyfifthyindex[0] == 2 or self.fifthyfifthyindex[1] == 2: pygame.draw.rect(screen, self.fifthyfifthycolor, self.answerrect2)
        else: pygame.draw.rect(screen, self.normal_color, self.answerrect2)
        if self.correct_answer == 3: pygame.draw.rect(screen, self.correct_color, self.answerrect3) 
        elif self.wrong_answer == 3:   pygame.draw.rect(screen, self.wrong_color, self.answerrect3)  
        elif self.selected_answ == 3:  pygame.draw.rect(screen, self.selected_color, self.answerrect3) 
        elif self.fifthyfifthyindex[0] == 3 or self.fifthyfifthyindex[1] == 3: pygame.draw.rect(screen, self.fifthyfifthycolor, self.answerrect3)
        else: pygame.draw.rect(screen, self.normal_color, self.answerrect3)
        if self.correct_answer == 4: pygame.draw.rect(screen, self.correct_color, self.answerrect4) 
        elif self.wrong_answer == 4:   pygame.draw.rect(screen, self.wrong_color, self.answerrect4)  
        elif self.selected_answ == 4:  pygame.draw.rect(screen, self.selected_color, self.answerrect4) 
        elif self.fifthyfifthyindex[0] == 4 or self.fifthyfifthyindex[1] == 4: pygame.draw.rect(screen, self.fifthyfifthycolor, self.answerrect4)
        else: pygame.draw.rect(screen, self.normal_color, self.answerrect4)
        pygame.draw.rect(screen, self.normal_color, self.questioncategoryrect) #question category rect
        pygame.draw.rect(screen, self.normal_color, self.pause_button_rect) #pause button
        screen.blit(font_40.render('| |', True, (255, 255, 255)), self.pause_button_rect.topleft + Vector2(13, 10)) #pause symbol

    def show_questions(self):
        question_text = font_30.render(self.question, True, (255, 255, 255))
        answer1_text = font_30.render(f'A: {self.answer1}', True, (255, 255, 255))
        answer2_text = font_30.render(f'B: {self.answer2}', True, (255, 255, 255))
        answer3_text = font_30.render(f'C: {self.answer3}', True, (255, 255, 255))
        answer4_text = font_30.render(f'D: {self.answer4}', True, (255, 255, 255))
        current_question_text = font_30.render(f'{self.current_cat} - € {self.quest_value[self.current_cat]}', True, (255, 255, 255))
        screen.blit(question_text, self.questionrect.topleft + Vector2(10, 15))
        screen.blit(answer1_text,  self.answerrect1.topleft +  Vector2(10, 15))
        screen.blit(answer2_text,  self.answerrect2.topleft +  Vector2(10, 15))
        screen.blit(answer3_text,  self.answerrect3.topleft +  Vector2(10, 15))
        screen.blit(answer4_text,  self.answerrect4.topleft +  Vector2(10, 15))
        screen.blit(current_question_text, self.questioncategoryrect.topleft + Vector2(10, 15))

    def show_failed(self, failed):
        pygame.draw.rect(screen, self.normal_color, self.failedrect)
        if failed: you_won_amount = font_40.render(f'Du hast € {self.quest_value[self.current_cat - 1]} gewonnen!', True, (255, 255, 255))
        else: you_won_amount = font_40.render(f'Du hast € {self.won_money} gewonnen!', True, (255, 255, 255))
        menu_text = font_40.render('Menue', True, (255, 255, 255))
        restart_text = font_40.render('Neu starten', True, (255, 255, 255))
        screen.blit(you_won_amount, you_won_amount.get_rect(center = (self.failedrect.centerx, self.failedrect.top + 30)))
        screen.blit(menu_text, menu_text.get_rect(topleft = (self.failedrect.left + 10, self.failedrect.bottom - 30)))
        screen.blit(restart_text, restart_text.get_rect(topright =    (self.failedrect.right - 10, self.failedrect.bottom - 30)))

    def reset(self):
        self.selected_answ = 0 #currently clicked answer
        self.correct_answer = 0
        self.wrong_answer = 0
        self.current_cat = 1
        self.stopped_game = False
        self.get_question(1)
        self.jokers_used = [False, False, False, False]

    def click_failed(self):
        pygame.event.get()
        if pygame.mouse.get_pressed(3)[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.restartrect.collidepoint(mouse_pos):
                pygame.mixer.stop()
                million_music.play(-1)
                pygame.display.update()
                sleep(0.2)
                self.reset()
                self.state = 'game'
            if self.returnmenurect.collidepoint(mouse_pos):
                pygame.mixer.stop()
                # pygame.draw.rect(screen, (255, 255, 255), self.returnmenurect, 2)
                pygame.display.update()
                sleep(0.2)
                self.reset()
                self.state = 'menu'
        
    def show_won_million(self):
        pygame.draw.rect(screen, self.normal_color, self.failedrect)
        you_won_amount = font_40.render(f'Du hast € 1 Million gewonnen!', True, (255, 255, 255))
        menu_text = font_40.render('Menue', True, (255, 255, 255))
        restart_text = font_40.render('Neu starten', True, (255, 255, 255))
        screen.blit(you_won_amount, you_won_amount.get_rect(center = (self.failedrect.centerx, self.failedrect.top + 30)))
        screen.blit(menu_text, menu_text.get_rect(topleft = (self.failedrect.left + 10, self.failedrect.bottom - 30)))
        screen.blit(restart_text, restart_text.get_rect(topright =    (self.failedrect.right - 10, self.failedrect.bottom - 30)))

    def selected_answer_animation(self):
        self.showaudienceall = False
        self.showtelephone = False
        if self.list[self.selected_answ] == self.corr_answ: #if the answer was correct
            self.correct_answer = self.selected_answ #what answer is the correct one
            self.show_gui() #show the gui again but with the answer marked green / red
            self.show_questions() #show the question and answer texts as well
            pygame.display.update() 
            sleep(1)
            self.correct_answer = 0
            self.selected_answ = 0
            if self.current_cat < 15: #if the player hasn't reached the last question yet
                self.current_cat += 1 #go to the next question categorie
                self.get_question(self.current_cat) #get the next question 
            else: #if the current question is the one million question
                pygame.mixer.stop()
                self.state = 'million'
        else: #if the answer was wrong
            self.wrong_answer = self.selected_answ
            self.state = 'failed'        
        if self.current_cat <= 5:
            self.won_money = 0
        if self.current_cat <= 10 and self.current_cat > 5:
            self.won_money = 500
        if self.current_cat > 10:
            self.won_money = 16_000 
        
    def game_click(self):
        pygame.event.get()
        if pygame.mouse.get_pressed(3)[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.answerrect1.collidepoint(mouse_pos):   self.selected_answ = 1
            elif self.answerrect2.collidepoint(mouse_pos): self.selected_answ = 2
            elif self.answerrect3.collidepoint(mouse_pos): self.selected_answ = 3
            elif self.answerrect4.collidepoint(mouse_pos): self.selected_answ = 4
        if keyboard.is_pressed('enter') and self.selected_answ != 0: #if an answer is selected and enter is pressed
            self.selected_answer_animation()

    def blit_menu(self):
        pygame.draw.rect(screen, self.normal_color, self.menustartrect)
        start_text = font_40.render('Start', True, (255, 255, 255))
        screen.blit(start_text, self.menustartrect.topleft + Vector2(10, 15))
        screen.blit(self.exitbuttonimg, self.exitbuttonrect)

    def start_click(self):
        pygame.event.get()
        if pygame.mouse.get_pressed(3)[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.menustartrect.collidepoint(mouse_pos):
                million_music.play(-1)
                self.state = 'game'
            if self.exitbuttonrect.collidepoint(mouse_pos): 
                pygame.draw.circle(screen, (255, 0, 0), self.exitbuttonrect.center, 25, 2)
                pygame.display.update()
                sys.exit()
    
    def show_pause_menu(self):
        pygame.draw.rect(screen, self.normal_color, self.failedrect)
        pause_text = font_40.render('Spiel pausiert', True, (255, 255, 255))
        resume_text = font_40.render('Weiterspielen', True, (255, 255, 255))
        stop_text = font_40.render('Spiel beenden', True, (255, 255, 255))
        screen.blit(pause_text, pause_text.get_rect(center =    (self.failedrect.centerx, self.failedrect.top + 30)))
        screen.blit(resume_text, resume_text.get_rect(topleft = (self.failedrect.left + 10, self.failedrect.bottom - 30)))
        screen.blit(stop_text, stop_text.get_rect(topright =    (self.failedrect.right - 10, self.failedrect.bottom - 30)))

    def pause_button_click(self):
        pygame.event.get()
        if pygame.mouse.get_pressed(3)[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.pause_button_rect.collidepoint(mouse_pos):
                pygame.mixer.pause()
                self.state = 'pause'
                self.show_pause_menu()

    def pause_menu_click(self):
        pygame.event.get()
        if pygame.mouse.get_pressed(3)[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.returnmenurect.collidepoint(mouse_pos): #returnmenurect is same as resume
                self.state = 'game'
                pygame.mixer.unpause()
            if self.restartrect.collidepoint(mouse_pos): #restartrect is same as stop
                self.state = 'failed'
                self.stopped_game = True
                while pygame.mouse.get_pressed(3)[0]:
                    pygame.event.get()

    def draw_cross(self, rect):
        pygame.draw.line(screen, (255, 0, 0), rect.topleft, rect.bottomright, 6)
        pygame.draw.line(screen, (255, 0, 0), rect.topright, rect.bottomleft, 6)

    def show_jokers(self):
        screen.blit(self.audienceoneimg, self.audienceonerect)
        screen.blit(self.audienceallimg, self.audienceallrect)
        screen.blit(self.telephoneimg, self.telephonerect)
        screen.blit(self.fifthyfifthyimg, self.fifthyfifthyrect)
        if self.jokers_used[0]: self.draw_cross(self.fifthyfifthyrect)
        if self.jokers_used[1]: self.draw_cross(self.telephonerect)
        if self.jokers_used[2]: self.draw_cross(self.audienceallrect)
        if self.jokers_used[3]: self.draw_cross(self.audienceonerect)

    def joker_click(self):
        pygame.event.get()
        if pygame.mouse.get_pressed(3)[0]:
            if self.fifthyfifthyrect.collidepoint(pygame.mouse.get_pos()) and not self.jokers_used[0]:
                self.fifthy_fifthy(); self.showaudienceall = False; self.showtelephone = False
            elif self.telephonerect.collidepoint(pygame.mouse.get_pos()) and not self.jokers_used[1]:
                self.telephone(); self.showaudienceall = False
            elif self.audienceallrect.collidepoint(pygame.mouse.get_pos()) and not self.jokers_used[2]:
                self.audienceall(); self.showtelephone = False
            elif self.audienceonerect.collidepoint(pygame.mouse.get_pos()) and not self.jokers_used[3]:
                self.audienceone(); self.showaudienceall = False

    def fifthy_fifthy(self):
        i = 0
        while i < 2:
            index = random.randint(1, 4) #random index for answer
            if self.list[index] != self.list[-1] and index != self.fifthyfifthyindex[0]: #if answer is not the correct answer
                self.fifthyfifthyindex[i] = index
                i += 1
        self.jokers_used[0] = True

    def showtelephoneanswer(self, index, phrase):
        if   index == 1: answer = 'A.'
        elif index == 2: answer = 'B.'
        elif index == 3: answer = 'C.'
        elif index == 4: answer = 'D.'
        pygame.draw.ellipse(screen, (255, 255, 255), self.telephoneanswerrect, 0)
        text = data["telephone"][phrase] + answer
        tel_text = font_30.render(text, True, (0, 0, 0))
        tel_text_rect = tel_text.get_rect(center = self.telephoneanswerrect.center)
        screen.blit(tel_text, tel_text_rect)
        pygame.display.update()

    def telephone(self):
        wronganswers = []
        for i in range(1, 5, 1):
            if self.list[i] == self.list[-1]: correctindex = i #get correct answer
            else: wronganswers.append(i)
        if random.randint(0, 100) < self.telephonecorrect or self.telephonecorrect == 100: index = correctindex#; print('correct')
        else: index = wronganswers[random.randint(0, 2)]#; print('wrong')
        self.index = index
        self.phrase = random.randint(0, len(data["telephone"]) - 1)
        self.jokers_used[1] = True
        self.showtelephone = True

    def showaudienceallanswer(self, percentlist, correctindex):
        pygame.draw.rect(screen, (200, 200, 200), self.telephoneanswerrect)
        abcd = ['A', 'B', 'C', 'D']
        for i in range(4):
            rect = pygame.rect.Rect(0, 0, 50, percentlist[i] / percentlist[correctindex] * 100)
            space = (self.telephoneanswerrect.width - 4 * rect.width ) / 5
            rect.bottom = self.telephoneanswerrect.bottom - 0.2 * self.telephoneanswerrect.height
            rect.centerx = self.telephoneanswerrect.left + i * (space + rect.width) + 1.5 * space
            pygame.draw.rect(screen, self.normal_color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            abcdtext = font_30.render(abcd[i], True, (0, 0, 0))
            abcdtextrect = abcdtext.get_rect(centerx = self.telephoneanswerrect.left + i * (space + rect.width) + 1.5 * space, bottom = self.telephoneanswerrect.bottom - 2)
            screen.blit(abcdtext, abcdtextrect)
            percenttext = font_30.render(f'{percentlist[i]} %', True, (0, 0, 0))
            percenttextrect = percenttext.get_rect(centerx = self.telephoneanswerrect.left + i * (space + rect.width) + 1.5 * space, top = self.telephoneanswerrect.top + 2)
            screen.blit(percenttext, percenttextrect)
        pygame.display.update()

    def audienceall(self):
        wronganswers = []
        percentlist = [None] * 4
        for i in range(1, 5, 1):
            if self.list[i] == self.list[-1]: correctindex = i #get correct answer
            else: wronganswers.append(i)
        percentlist[correctindex - 1] = random.randint(self.audienceallcorrect[0], self.audienceallcorrect[1])
        remaining = 100 - percentlist[correctindex - 1] #remaining percent after substracting correct percent
        j = 0 
        for i in range(4): 
            if percentlist[i-1] == None and j < 2: #if current index of list doesn't lead to the already occupied one (the correct one)
                percentlist[i-1] = random.randint(int(remaining * self.audienceallrange[0]), int(remaining * self.audienceallrange[1]))
                remaining -= percentlist[i-1]
                j += 1
            elif percentlist[i-1] == None and j == 2: 
                percentlist[i-1] = remaining
                break
        self.jokers_used[2] = True
        self.percentlist = percentlist
        self.correctindex = correctindex - 1
        self.showaudienceall = True

    def audienceone(self):
        wronganswers = []
        for i in range(1, 5, 1):
            if self.list[i] == self.list[-1]: correctindex = i #get correct answer
            else: wronganswers.append(i)
        if random.randint(0, 100) < self.audienceonecorrect or self.audienceonecorrect == 100: index = correctindex# ; print('correct')
        else: index = wronganswers[random.randint(0, 2)]#; print('wrong')
        self.index = index
        self.jokers_used[3] = True
        self.showtelephone = True

pygame.init()
screen_width, screen_height = (1536, 864)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Wer Wird millionär?')
font_30 = pygame.font.Font(None, 30)
font_40 = pygame.font.Font(None, 40)
with open('fragen_antworten2.json') as f: data = json.load(f)
jauch_image = pygame.transform.rotozoom(pygame.image.load('pictures/jauch_1.jpg').convert(), 0, screen_width / 2106)
wwm_logo = pygame.transform.rotozoom(pygame.image.load('pictures/wwm_logo.jpg').convert(), 0, screen_width / 1920)
wwm_logo_rect = wwm_logo.get_rect(center = (screen_width/2, screen_height/2))
million_music = pygame.mixer.Sound('sounds/59 $1,000,000 Question.mp3')
pygame.display.set_icon(wwm_logo)

game = Game()
game.get_question(1)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keyboard.is_pressed('esc'):
                pygame.quit()
                sys.exit()

        if game.state == 'game':
            screen.fill('black')
            screen.blit(jauch_image, (0, 0))
            game.show_gui()
            game.show_questions()
            game.show_jokers()
            game.game_click()
            game.joker_click()
            game.pause_button_click()
            if game.showaudienceall: game.showaudienceallanswer(game.percentlist, game.correctindex)
            if game.showtelephone: game.showtelephoneanswer(game.index, game.phrase)

        if game.state == 'pause': game.pause_menu_click()

        if game.state == 'failed':
            screen.fill('black')
            screen.blit(jauch_image, (0, 0))
            game.show_gui()
            game.show_questions()
            if game.stopped_game: game.show_failed(True)
            else: game.show_failed(False)
            game.click_failed()

        if game.state == 'million':
            game.show_won_million()
            game.click_failed()
            
        if game.state == 'menu':
            screen.fill('black')
            screen.blit(wwm_logo, wwm_logo_rect)
            game.blit_menu()
            game.start_click()

        pygame.display.update()

if __name__ == '__main__': main()