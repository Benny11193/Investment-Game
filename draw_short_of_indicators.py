import pygame
import os
import time
import datetime

FPS = 50
WIDTH = 960
HEIGHT = 540

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
LIGHT_BLUE = (0, 255, 255)
WHITE = (255, 255, 255)


color_background = (58, 83, 13)
color_inactive = (207, 158, 68)
color_active = (226, 196, 141)
color_preset_string = (100, 100, 100)
color_button_send_1 = (79, 156, 156)
color_button_send_2 = (130, 192, 192)
color_short_of_indicators_background = (66, 58, 46)
color_portfolio = (43, 57, 69)
color_game_time_board = (151, 137, 125)
color_game_time_board_text = (54, 39, 28)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(color_portfolio)
info_board_height = HEIGHT
info_board_height_const = HEIGHT
info_board = pygame.Surface((WIDTH*2/5, info_board_height))
info_board.fill(color_short_of_indicators_background)
info_board_rect = info_board.get_rect()
info_board_rect.x = 576
info_board_rect.y = 0
gaming_msg_background = pygame.Surface((WIDTH,HEIGHT))
gaming_msg_background.set_alpha(100)

font_none = pygame.font.match_font('none')
font_msjh = "微軟正黑體.ttf"

init_png1 = pygame.image.load(os.path.join("init1.png")).convert()
init_png1 = pygame.transform.scale(init_png1,(960,540))
init_png1.set_alpha(255)
init_png2 = pygame.image.load(os.path.join("init2.png")).convert()
init_png2 = pygame.transform.scale(init_png2,(960,540))
init_png2.set_alpha(200)
init_png3 = pygame.image.load(os.path.join("init3.png")).convert()
init_png3 = pygame.transform.scale(init_png3,(960,540))
init_png3.set_alpha(150)
init_png4 = pygame.image.load(os.path.join("init4.png")).convert()
init_png4 = pygame.transform.scale(init_png4,(960,540))
init_png4 = pygame.transform.flip(init_png4, True, False)
init_png4.set_alpha(150)

button_pause_symbol_png = pygame.image.load(os.path.join("pause symbol.png")).convert()
button_pause_symbol_png.set_colorkey(BLACK)
button_pause_symbol_png = pygame.transform.scale(button_pause_symbol_png,(80,80))

button_resume_symbol_png = pygame.image.load(os.path.join("resume symbol.png")).convert()
button_resume_symbol_png.set_colorkey(BLACK)
button_resume_symbol_png = pygame.transform.scale(button_resume_symbol_png,(80,80))

button_fast_forward_symbol_png = pygame.image.load(os.path.join("fast forward symbol.png")).convert()
button_fast_forward_symbol_png.set_colorkey(BLACK)
button_fast_forward_symbol_png = pygame.transform.scale(button_fast_forward_symbol_png,(60,60))

button_setting_symbol_png = pygame.image.load(os.path.join("setting symbol.png")).convert()
button_setting_symbol_png.set_colorkey(BLACK)
button_setting_symbol_png = pygame.transform.scale(button_setting_symbol_png,(60,60))

def draw_text_left(surf, text, size, color, x, y, font = font_none):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)
    return text_surface.get_width()

def draw_text_right(surf, text, size, color, x, y, font = font_none):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.right = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)
    return text_surface.get_width()

def draw_text_centerx(surf, text, size, color, x, y, font = font_none):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)
    return text_surface.get_width()

def split_list(list, n):
    for i in range(0, len(list), n):
        yield list[i:i+n]

def split_string(string, n):
    string_list = list(string)
    string_list_ = list(split_list(string_list, n))
    string_list__ = []
    for i in range(len(string_list_)):
        string_list__.append(''.join(str(x) for x in string_list_[i]))
    return string_list__

def draw_paragraph(surf, paragraph, n, size, color, x, y, w):
    string_list = split_string(paragraph, n)
    for i in range(len(string_list)):
        draw_text_left(surf, string_list[i], size, color, x, y+w*i, font_msjh)

def draw_short_of_indicators(page):
    if page == 1:
        draw_text_centerx(screen, "移動平均線MA", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "短期MA線由下而上與長期MA交叉（黃金交叉）為買進時機，短期MA由上而下與長期MA交叉（死亡交叉）為賣出時機", 18, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "當短、中、長期MA呈現由上而下的順序排列時為多頭市場，反之為空頭市場", 18, 18, color_inactive, 560, 186, 24)
    elif page == 2:
        draw_text_centerx(screen, "相對強弱指標RSI", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "RSI>50表多頭，RSI<50表空頭，RSI>80表示超買，RSI<20表示超賣", 26, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "分為5、10、20日三種期間，時間越短的RSI指標越不準確", 20, 18, color_active, 560, 162, 24)
        draw_paragraph(screen, "當短期RSI由下而上與長期RSI交叉時為買進時機，短期RSI由上而下與長期RSI交叉時為賣出時機", 21, 18, color_active, 560, 210, 24)
    elif page == 3:
        draw_text_centerx(screen, "隨機指標KD", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "D>80表超買，D<20表超賣，當K向上突破D為買進，K向下突破D為賣出", 21, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "K表示快速隨機指標，D表示慢速隨機指標", 20, 18, color_inactive, 560, 162, 24)
    elif page == 4:
        draw_text_centerx(screen, "移動平均離合線MACD", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "當DIF由下而上與EMA交叉為買進時機", 20, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "當DIF由上而下與EMA交叉為賣出時機", 20, 18, color_active, 560, 138, 24)
        draw_paragraph(screen, "DIF與EMA皆為負時：", 12, 18, color_active, 560, 162, 24)
        draw_paragraph(screen, "當DIF反轉成0或正值時，代表空頭即將結束，為買進時機", 19, 18, color_active, 560, 186, 24)
        draw_paragraph(screen, "DIF與EMA皆為正時：", 12, 18, color_active, 560, 234, 24)
        draw_paragraph(screen, "當DIF反轉成0或負值時，代表多頭即將結束，為賣出時機", 19, 18, color_active, 560, 258, 24)
        draw_paragraph(screen, "EMA為指數平滑移動平均線", 13, 18, color_inactive, 560, 306, 24)
        draw_paragraph(screen, "DIF為短期（12日）EMA減長期（26日）EMA", 22, 18, color_inactive, 560, 330, 24)
    elif page == 5:
        draw_text_centerx(screen, "動能振盪指標CMO", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "CMO>50表超買，CMO<-50表超賣", 20, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "短期由下而上突破長期CMO為買進時機", 18, 18, color_active, 560, 138, 24)
        draw_paragraph(screen, "短期由上而下突破長期CMO為賣出時機", 18, 18, color_active, 560, 162, 24)
        draw_paragraph(screen, "該指標與股價趨勢背離過大時表示股價將會有大反轉（背離：指當市場的價格走勢創出新高或新低時，對應的成交量或技術指標值卻沒有跟隨創出新高或新低）", 18, 18, color_inactive, 560, 186, 24)
    elif page == 6:
        draw_text_centerx(screen, "威廉指標WMSR", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "一般由9日WMSR作為判斷指標", 15, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "<-80為買進時機，>-20為賣出時機", 19, 18, color_active, 560, 138, 24)
        draw_paragraph(screen, "公式：", 3, 18, color_inactive, 554, 162, 24)
        draw_paragraph(screen, "（設定周期內最高價–設定周期內收盤價）/（設定周期內最高價–設定周期內最低價）* 100%", 20, 18, color_inactive, 548, 186, 24)
    elif page == 7:
        draw_text_centerx(screen, "停損點轉向操作系統SAR", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "當行情向下跌落SAR時即為賣出訊號點", 18, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "當行情反轉穿破SAR時則為買進訊號點", 18, 18, color_active, 560, 138, 24)
        draw_paragraph(screen, "公式：SARt=SARt-1+AF*(EP–SARt-1)", 29, 18, color_inactive, 560, 162, 24)
        draw_paragraph(screen, "SARt為當日值，而SARt-1為前一日值，AF為加速因子，AF的起始值設為0.02", 22, 18, color_inactive, 560, 186, 24)
        draw_paragraph(screen, "然後每當此波段有新的行情極值EP出現時（即新高或新低價出現時），AF值每次以0.02值累加上去，直至AF值為0.2", 19, 18, color_inactive, 560, 234, 24)
        draw_paragraph(screen, "EP值為SAR此波段應用以來的最高或最低價位值", 20, 18, color_inactive, 560, 306, 24)
    elif page == 8:
        draw_text_centerx(screen, "商品通道指數CCI", 24, color_active, 720, 68, font_msjh)
        draw_paragraph(screen, "當CCI由下往上突破+100%時買進當CCI由上往下跌破-100%時賣出", 18, 18, color_active, 560, 114, 24)
        draw_paragraph(screen, "CCI=(TP-MA)/0.015*MD", 20, 18, color_inactive, 560, 162, 24)
        draw_paragraph(screen, "TP＝（最高價+最低價+收盤價）/3", 18, 18, color_inactive, 560, 186, 24)
        draw_paragraph(screen, "MA＝n日間的TP移動平均", 13, 18, color_inactive, 560, 210, 24)
        draw_paragraph(screen, "MD＝TP-MA的平均偏差", 13, 18, color_inactive, 560, 234, 24)

def show_setting():
    button_setting_str_color = (51, 51, 51) if (button_setting_str.collidepoint(pygame.mouse.get_pos()))&(not True in pygame.mouse.get_pressed()) else BLACK
    button_End_Game_str_color = (51, 51, 51) if (button_End_Game_str.collidepoint(pygame.mouse.get_pos()))&(not True in pygame.mouse.get_pressed()) else BLACK

    screen.blit(gaming_msg_background, (0,0))
    draw_text_left(screen, "Setting", 32, button_setting_str_color, WIDTH*13/16, 465)
    draw_text_left(screen, "End Game", 32, button_End_Game_str_color, WIDTH*13/16, 495)

def show_msg():
    pygame.draw.rect(screen, color_game_time_board, (WIDTH*3/8-60, 135, 360, 270))
    pygame.draw.rect(screen, color_game_time_board_text, (WIDTH*3/8-60, 135, 360, 270),2)
    draw_text_left(screen, "XXX", 24, color_game_time_board_text, 300+30, 150, font_msjh)

def show_trading_column(money, hold, direct, input):
    global last_cursor_flash
    if pygame.time.get_ticks() - last_cursor_flash > 500:
        cursor_visible = True
        if pygame.time.get_ticks() - last_cursor_flash > 1000:
            last_cursor_flash = pygame.time.get_ticks()
    else:
        cursor_visible = False

    pygame.draw.rect(screen, color_game_time_board, (453,0,114,63))
    pygame.draw.rect(screen, color_game_time_board_text, (453,0,114,63), 1)
    draw_text_left(screen, "Hold", 18, color_game_time_board_text, 470, 8)
    draw_text_centerx(screen, str(hold), 18, color_game_time_board_text, 528, 8)
    draw_text_left(screen, "張", 10, color_game_time_board_text, 540,7, font_msjh)
    draw_text_centerx(screen, "NT$"+str(money), 18, color_game_time_board_text, 510, 25)

    if direct == True:
        draw_text_right(screen, "buy :", 18, color_game_time_board_text, 497, 43)
    else:
        draw_text_right(screen, "sell :", 18, color_game_time_board_text, 497, 43)
    input_box_trading_width = draw_text_centerx(screen, input, 18, color_game_time_board_text, 524, 42)
    if input == "" and cursor_visible:
        draw_text_centerx(screen, "|", 18, color_game_time_board_text, 524, 42)
    pygame.draw.rect(screen, color_game_time_board_text, (507,53,36,1))

    pygame.draw.circle(screen, color_game_time_board_text, (556,49), 8)
    draw_text_left(screen, "->", 18, color_game_time_board, 551,42)
    return input_box_trading_width

def init():
    waiting = True
    while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            #if event.type == pygame.MOUSEBUTTONUP:

            #if event.type == pygame.KEYDOWN:

        button_init_Game_Start_color = (184,115,51) if (button_init_Game_Start.collidepoint(pygame.mouse.get_pos()))&(not True in pygame.mouse.get_pressed()) else (147,92,41)

        screen.blit(init_png1, (0,0))
        screen.blit(init_png2, (0,0))
        screen.blit(init_png3, (0,0))
        screen.blit(init_png4, (0,0))
        draw_text_centerx(screen, "Game Start", 48, button_init_Game_Start_color, 840, 480)

        pygame.display.update()

class Indicator_Info_Col(pygame.Surface):
    def __init__(self, x, y, title, info):
        super().__init__((WIDTH*2/5, 30))
        self.fill(color_short_of_indicators_background)
        self.rect = self.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.const_y = y
        self.title = title
        self.indicator_info = info
        self.unfold = False
        self.draw_on_canvas = False
        self.expand_surface = pygame.Surface((WIDTH*2/5, 30))
        self.expand_surface.fill(color_short_of_indicators_background)
        self.button_unfold = pygame.Rect(info_board_rect.x+self.rect.x+316, info_board_rect.y+self.rect.y+11, 16, 12)
        self.button_unfold_color = color_inactive
        self.button_draw_on_canvas = pygame.Rect(info_board_rect.x+self.rect.x+346, info_board_rect.y+self.rect.y+8, 16, 16)
        self.button_draw_on_canvas_color = (109, 81, 28)
        self.button_not_draw_on_canvas_color = color_inactive

    def event(self):
        if self.button_unfold.collidepoint(pygame.mouse.get_pos()):
            if self.unfold == False:
                self.unfold = True
            else:
                self.unfold = False
        if self.button_draw_on_canvas.collidepoint(pygame.mouse.get_pos()):
            if self.draw_on_canvas == False:
                for surf in Indicator_Info_Col_group:
                    surf.draw_on_canvas = False
                self.draw_on_canvas = True
            else:
                self.draw_on_canvas = False

    def update(self):
        self.button_unfold = pygame.Rect(info_board_rect.x+self.rect.x+316, info_board_rect.y+self.rect.y+11, 16, 12)
        self.button_draw_on_canvas = pygame.Rect(info_board_rect.x+self.rect.x+346, info_board_rect.y+self.rect.y+8, 16, 16)
        self.button_unfold_color = color_active if self.button_unfold.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_inactive
        self.button_draw_on_canvas_color = (146, 108, 38) if self.button_draw_on_canvas.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else (109, 81, 28)
        self.button_not_draw_on_canvas_color = color_active if self.button_draw_on_canvas.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_inactive

    def draw_on_info_board(self):
        info_board.blit(self, self.rect)
        self.fill(color_short_of_indicators_background)
        draw_text_left(self, self.title, 24, WHITE, 30, 0,font_msjh)
        if not self.unfold:
            draw_text_centerx(self, "+", 32, self.button_unfold_color, 324, -8,font_msjh)
        else:
            info_board.blit(self.expand_surface, (self.rect.x, self.rect.bottom))
            draw_text_centerx(self, "_", 32, self.button_unfold_color, 324, -22,font_msjh)
        
        if not self.draw_on_canvas:
            pygame.draw.circle(self, self.button_draw_on_canvas_color, (354, 16), 8)
        else:
            pygame.draw.circle(self, self.button_not_draw_on_canvas_color, (354, 16), 8)
        pygame.draw.circle(self, (107, 107, 107), (354, 16), 8, 3)
        
        self.expand_surface.fill(color_short_of_indicators_background)
        draw_text_left(self.expand_surface, self.indicator_info, 18, WHITE, 30, 0,font_msjh)


Initial_Date = datetime.date(2010, 1, 1)
End_Date = datetime.date(2023, 1, 1)

Stock_Code = "2330"
Stock_Name = "台積電"

time_pause = True
last_update = pygame.time.get_ticks()
update_rate = 1000
fast_forward = 1

Date = Initial_Date
days = 0

trading_input = ""
Trading_Direct = True

button_pause_and_resume = pygame.Rect(380,470,40,40)
button_fast_forward = pygame.Rect(545,475,50,30)
button_setting = pygame.Rect(730,470,40,40)
button_setting_str = pygame.Rect(WIDTH*13/16+1, 465, 75,20)
button_setting_str_color = BLACK
button_End_Game_str = pygame.Rect(WIDTH*13/16+1, 495, 108,20)
button_End_Game_str_color = BLACK

button_20days = pygame.Rect(65,410,62,20)
button_20days_color = color_inactive
button_60days = pygame.Rect(193,410,62,20)
button_60days_color = color_inactive
button_120days = pygame.Rect(316,410,72,20)
button_120days_color = color_inactive
button_240days = pygame.Rect(444,410,72,20)
button_240days_color = color_inactive
button_cancel_cruciform = pygame.Rect(544,412,16,16)
button_cancel_cruciform_color = color_inactive

show_cruciform = False

ma_col = Indicator_Info_Col(0, 120, "MA", "MA(5):000.0  MA(10):000.0  MA(20):000.0")
rsi_col = Indicator_Info_Col(0, 150, "RSI", "RSI(5):00.00  RSI(10):00.00  RSI(20):00.00")
kd_col = Indicator_Info_Col(0, 180, "KD", "K : 00.00  D : 00.00")
macd_col = Indicator_Info_Col(0, 210, "MACD", "MACD : 00.00  MACD(9) : 00.00")
cmo_col = Indicator_Info_Col(0, 240, "CMO", "CMO(5) : 00.00  CMO(10) : 00.00")
wmsr_col = Indicator_Info_Col(0, 270, "WMSR", "WMSR(9) : 00.00")
sar_col = Indicator_Info_Col(0, 300, "SAR", "SAR(0.02, 0.2) : 00.00")
cci_col = Indicator_Info_Col(0, 330, "CCI", "CCI(14) : -00.00%")
Indicator_Info_Col_group = []
Indicator_Info_Col_group.append(ma_col)
Indicator_Info_Col_group.append(rsi_col)
Indicator_Info_Col_group.append(kd_col)
Indicator_Info_Col_group.append(macd_col)
Indicator_Info_Col_group.append(cmo_col)
Indicator_Info_Col_group.append(wmsr_col)
Indicator_Info_Col_group.append(sar_col)
Indicator_Info_Col_group.append(cci_col)

button_buy = pygame.Rect(465, 27, 30, 30)
button_buy_color = (173, 0, 0)
button_sell = pygame.Rect(525, 27, 30, 30)
button_sell_color = (0, 219, 0)

showing_trading_column = False
trading_column = pygame.Rect(453,0,114,63)
last_cursor_flash = 0
button_send_trading = pygame.Rect(550, 43, 12, 12)

showing_holding_board = False
button_unfold_holding_board = pygame.Rect(935,440,25,100)
button_unfold_holding_board_color = color_background

button_back_to_init = pygame.Rect(825, 480, 90, 20)
button_back_to_init_color = color_inactive

button_init_Game_Start = pygame.Rect(750,480,180,30)
button_init_Game_Start_color = (147,92,41)

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1) or (event.button == 2) or (event.button == 3):
                if button_pause_and_resume.collidepoint(pygame.mouse.get_pos()):
                    time_pause = False if time_pause == True else True
                    last_update = pygame.time.get_ticks()
                if button_fast_forward.collidepoint(pygame.mouse.get_pos()):
                    if fast_forward<4:
                        fast_forward*=2
                    else:
                        fast_forward=1
                if pygame.Rect(48,80,480,320).collidepoint(pygame.mouse.get_pos()):
                    show_cruciform = True
                if not trading_column.collidepoint(pygame.mouse.get_pos()):
                    showing_trading_column = False
                    trading_input = ""
            else:
                if pygame.Rect(576,0,WIDTH*2/5,440).collidepoint(pygame.mouse.get_pos()):
                    if event.button == 4:
                        if info_board_rect.y < 0:
                            info_board_rect.y += 30
                    elif event.button == 5:
                        if info_board_rect.y > HEIGHT-info_board_height:
                            info_board_rect.y -= 30

        if event.type == pygame.MOUSEBUTTONUP:
            if (event.button == 1) or (event.button == 2) or (event.button == 3):
                if button_cancel_cruciform.collidepoint(pygame.mouse.get_pos()):
                    show_cruciform = False
                for surf in Indicator_Info_Col_group:
                    surf.event()
                if not showing_trading_column:
                    if button_buy.collidepoint(pygame.mouse.get_pos()):
                        Trading_Direct = True
                        showing_trading_column = True
                        time_pause = True
                        last_update = pygame.time.get_ticks()
                    if button_sell.collidepoint(pygame.mouse.get_pos()):
                        Trading_Direct = False
                        showing_trading_column = True
                        time_pause = True
                        last_update = pygame.time.get_ticks()
                else:
                    if button_send_trading.collidepoint(pygame.mouse.get_pos()):
                        print(trading_input)
                if not showing_holding_board:
                    if button_unfold_holding_board.collidepoint(pygame.mouse.get_pos()):
                        showing_holding_board = True

        if event.type == pygame.KEYDOWN:
            if not showing_trading_column:
                if event.key == pygame.K_SPACE:
                    time_pause = False if time_pause == True else True
                    last_update = pygame.time.get_ticks()
            else:
                if event.key != pygame.K_TAB:
                    if event.key == pygame.K_BACKSPACE:
                        trading_input = trading_input[:-1]
                    elif event.key == pygame.K_DELETE:
                        trading_input = ""
                    elif event.key == pygame.K_RETURN:
                        print(trading_input)
                    else:
                        if input_box_trading_width <= 20:
                            trading_input += event.unicode


    screen.blit(canvas, (0, 0))
    screen.blit(info_board, (info_board_rect.x, info_board_rect.y))

    #更新遊戲
    button_resume_symbol_png.set_alpha(170) if button_pause_and_resume.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else button_resume_symbol_png.set_alpha(255)
    button_pause_symbol_png.set_alpha(170) if button_pause_and_resume.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else button_pause_symbol_png.set_alpha(255)
    button_fast_forward_symbol_png.set_alpha(170) if button_fast_forward.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else button_fast_forward_symbol_png.set_alpha(255)
    button_setting_symbol_png.set_alpha(170) if button_setting.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else button_setting_symbol_png.set_alpha(255)
    button_buy_color = RED if button_buy.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else (173, 0, 0)
    button_sell_color = GREEN if button_sell.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else (0, 219, 0)
    button_20days_color = color_active if button_20days.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_inactive
    button_60days_color = color_active if button_60days.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_inactive
    button_120days_color = color_active if button_120days.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_inactive
    button_240days_color = color_active if button_240days.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_inactive
    button_cancel_cruciform_color = color_active if button_cancel_cruciform.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_inactive
    button_unfold_holding_board_color = (75, 106, 17) if button_unfold_holding_board.collidepoint(pygame.mouse.get_pos())&(not True in pygame.mouse.get_pressed()) else color_background

    unfolding_col_count = 0
    for surf in Indicator_Info_Col_group:
        surf.update()
        surf.rect.y = surf.const_y+unfolding_col_count*30
        if surf.unfold == True:
            unfolding_col_count+=1
    info_board_height = info_board_height_const+unfolding_col_count*30
    info_board = pygame.Surface((WIDTH*2/5, info_board_height))
    if info_board_rect.y < HEIGHT-info_board_height:
        info_board_rect.y += 30
    if info_board_rect.y > 0:
        info_board_rect.y = 0

    if time_pause == False:
        if pygame.time.get_ticks() - last_update >= update_rate/fast_forward:
            last_update = pygame.time.get_ticks()
            days += 1
    if Date < End_Date:
        Date = Initial_Date+datetime.timedelta(days)

    #畫面顯示
    draw_text_left(screen, Stock_Code+" "+Stock_Name, 24, WHITE, 30, 30, font_msjh)
    pygame.draw.circle(screen, (107, 107, 107), (480,42), 18)
    pygame.draw.circle(screen, button_buy_color, (480,42), 16)
    pygame.draw.circle(screen, (107, 107, 107), (540,42), 18)
    pygame.draw.circle(screen, button_sell_color, (540,42), 16)
    draw_text_centerx(screen, "buy ", 16, (224, 224, 224), 481, 37)
    draw_text_centerx(screen, "sell ", 16, (79, 79, 79), 541, 37)

    canvas.fill(color_portfolio)
    pygame.draw.rect(canvas, WHITE, (48, 80, 480, 320))
    draw_text_right(canvas, "000.0", 12, WHITE, 45, 72,font_msjh)
    draw_text_right(canvas, "000.0", 12, WHITE, 45, 392,font_msjh)
    pygame.draw.line(canvas, color_inactive, (48,300), (527,300), 1)
    pygame.draw.line(canvas, color_inactive, (300,80), (300,399), 1)
    if not show_cruciform:
        draw_text_left(canvas, "20days", 18, button_20days_color, 67, 408,font_msjh)
        draw_text_left(canvas, "60days", 18, button_60days_color, 195, 408,font_msjh)
        draw_text_left(canvas, "120days", 18, button_120days_color, 318, 408,font_msjh)
        draw_text_left(canvas, "240days", 18, button_240days_color, 446, 408,font_msjh)
    else:
        draw_text_left(canvas, "2010-01-01", 16, WHITE, 48, 408,font_msjh)
        draw_text_right(canvas, "open:000.0    close:000.0    high:000.0    low:000.0    vol:00000", 12, WHITE, 528, 404,font_msjh)
        #draw_text_right(canvas, "MA(5):000.0    MA(10):000.0    MA(20):000.0", 12, WHITE, 528, 420,font_msjh)
        w1 = draw_text_right(canvas, "MA(20):000.0", 12, PURPLE, 528, 420,font_msjh)
        w2 = draw_text_right(canvas, "MA(10):000.0    ", 12, LIGHT_BLUE, 528-w1, 420,font_msjh)
        draw_text_right(canvas, "MA(5):000.0    ", 12, YELLOW, 528-w1-w2, 420,font_msjh)

        pygame.draw.circle(canvas, button_cancel_cruciform_color, (552, 420), 10, 2)
        draw_text_centerx(canvas, "x", 28, button_cancel_cruciform_color, 552, 409)

    info_board.fill(color_short_of_indicators_background)
    draw_text_left(info_board, "000.0        +0.0        +0.00%", 24, WHITE, 30, 20, font_msjh)
    draw_text_left(info_board, "open : 000.0  close : 000.0", 18, WHITE, 30, 60, font_msjh)
    draw_text_left(info_board, "high : 000.0  low : 000.0  volume : 000000", 18, WHITE, 30, 90, font_msjh)
    for surf in Indicator_Info_Col_group:
        surf.draw_on_info_board()

    pygame.draw.rect(screen, color_game_time_board, (0,440,WIDTH,100))
    draw_text_left(screen, "Date "+str(Date), 40, color_game_time_board_text, WIDTH/16, 480)
    draw_text_left(screen, "休市", 18, color_game_time_board_text, WIDTH/16+224, 480, font_msjh)
    if time_pause:
        screen.blit(button_resume_symbol_png, (360,450))
    else:
        screen.blit(button_pause_symbol_png, (360,450))
    draw_text_left(screen, str(fast_forward)+"x", 18, color_game_time_board_text, 586,496)
    screen.blit(button_fast_forward_symbol_png, (540,460))
    screen.blit(button_setting_symbol_png, (720,460))

    if showing_holding_board:
        pygame.draw.rect(screen, color_background, (800,0,WIDTH/6,HEIGHT))
        pygame.draw.rect(screen, (162, 120, 42), (802,2,WIDTH/6-4,HEIGHT-4),1)
    else:
        pygame.draw.rect(screen, button_unfold_holding_board_color, (935,440,25,100))
        pygame.draw.rect(screen, (162, 120, 42), (937,442,21,96), 1)
    """
    pygame.draw.rect(screen, color_background, (800,440,WIDTH/6,100))
    pygame.draw.rect(screen, (162, 120, 42), (802,442,WIDTH/6-4,96),1)
    draw_text_left(screen, "目前持有", 16, color_active, 808, 444,font_msjh)
    draw_text_left(screen, "2330", 16, color_active, 816, 474,font_msjh)
    draw_text_right(screen, "999", 16, color_active, 932, 474,font_msjh)
    draw_text_right(screen, "張", 16, color_active, 952, 474,font_msjh)
    draw_text_right(screen, "NT$1000000", 16, color_active, 948, 504,font_msjh)
    """

    #show_msg()
    #show_msg()
    #show_setting()
    """
    screen.fill(color_short_of_indicators_background)
    draw_text_left(screen, "日期：2022-01-01 ~ 2023-01-01", 28, color_active, 90, 60, font_msjh)
    draw_text_left(screen, "起始金錢：NT$1000000", 24, color_active, 122, 130, font_msjh)
    draw_text_left(screen, "結束金錢：NT$9999999", 24, color_active, 122, 190, font_msjh)
    draw_text_left(screen, "投資報酬率ROI：899.9999%", 24, color_active, 122, 250, font_msjh)
    draw_text_left(screen, "標的 2330  參考 RSI、MACD", 16, color_active, 442, 130, font_msjh)
    draw_text_left(screen, "標的 2603  參考：MA、SAR", 16, color_active, 442, 160, font_msjh)
    draw_text_left(screen, "標的 0050  參考：CMO、KD", 16, color_active, 442, 190, font_msjh)
    draw_text_left(screen, "標的 2303  參考：WMSR、CCI", 16, color_active, 442, 220, font_msjh)
    draw_text_centerx(screen, "回主畫面", 24, button_back_to_init_color, 870, 472, font_msjh)
    """
    if showing_trading_column:
        input_box_trading_width = show_trading_column(1000000, 999, Trading_Direct, trading_input)

    pygame.display.update()
pygame.QUIT
"""
Initial_Date = datetime.date(2010,1,1)
Initial_Date_string = "yyyy-mm-dd"
input_box_Initial_Date_triggered = False
End_Date = datetime.date.today() - datetime.timedelta(1)
End_Date_string = "~Yesterday"
Initial_Money = 1000000
Initial_Money_string = "NT$1000000"
turn_to_next_page = False
input_Stock_Code = "2330"
Stock_Code = ""
Stock_Name = ""
Used_Strategies_list = []
Used_Strategies_count = len(Used_Strategies_list)
Short_Of_Indicators_page = 0
Game_Start = False
DF = pandas.DataFrame([])
Strategies_Result = {}
Stock_stored = {}
time_pause = True
last_update = pygame.time.get_ticks()
fast_forward = 1
Date = Initial_Date
days = 0
have_shown_msg = False
Data_period = 20
show_cruciform = False
ma_col = Indicator_Info_Col(0, 120, "MA", "")
rsi_col = Indicator_Info_Col(0, 150, "RSI", "")
kd_col = Indicator_Info_Col(0, 180, "KD", "")
macd_col = Indicator_Info_Col(0, 210, "MACD", "")
cmo_col = Indicator_Info_Col(0, 240, "CMO", "")
wmsr_col = Indicator_Info_Col(0, 270, "WMSR", "")
sar_col = Indicator_Info_Col(0, 300, "SAR", "")
cci_col = Indicator_Info_Col(0, 330, "CCI", "")
Indicator_Info_Col_group = []
Indicator_Info_Col_group.append(ma_col)
Indicator_Info_Col_group.append(rsi_col)
Indicator_Info_Col_group.append(kd_col)
Indicator_Info_Col_group.append(macd_col)
Indicator_Info_Col_group.append(cmo_col)
Indicator_Info_Col_group.append(wmsr_col)
Indicator_Info_Col_group.append(sar_col)
Indicator_Info_Col_group.append(cci_col)
trading_input = ""
Trading_Direct = True
Trading_Input = 0
Money = Initial_Money
showing_trading_column = False
last_cursor_flash = 0
show_Unable_to_operate = False"""