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
gaming_msg_background = pygame.Surface((WIDTH,HEIGHT))
gaming_msg_background.set_alpha(100)

font_none = pygame.font.match_font('none')
font_msjh = "微軟正黑體.ttf"

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
    button_setting_str_color = (51, 51, 51) if (button_setting_str.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else BLACK
    button_End_Game_str_color = (51, 51, 51) if (button_End_Game_str.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else BLACK

    screen.blit(gaming_msg_background, (0,0))
    draw_text_left(screen, "Setting", 32, button_setting_str_color, WIDTH*13/16, 465)
    draw_text_left(screen, "End Game", 32, button_End_Game_str_color, WIDTH*13/16, 495)

def show_msg():
    pygame.draw.rect(screen, color_game_time_board, (WIDTH*3/8-60, 135, 360, 270))
    pygame.draw.rect(screen, color_game_time_board_text, (WIDTH*3/8-60, 135, 360, 270),2)
    draw_text_left(screen, "XXX", 24, color_game_time_board_text, 300+30, 150, font_msjh)

def show_trading_column(money, hold, direct, input):
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
    pygame.draw.rect(screen, color_game_time_board_text, (507,53,36,1))

    pygame.draw.circle(screen, color_game_time_board_text, (556,49), 8)
    draw_text_left(screen, "->", 18, color_game_time_board, 551,42)
    return input_box_trading_width


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

button_buy = pygame.Rect(465, 27, 30, 30)
button_buy_color = (173, 0, 0)
button_sell = pygame.Rect(525, 27, 30, 30)
button_sell_color = (0, 219, 0)

showing_trading_column = False
trading_column = pygame.Rect(453,0,114,63)
button_send_trading = pygame.Rect(550, 43, 12, 12)

button_back_to_init = pygame.Rect(825, 480, 90, 20)
button_back_to_init_color = color_inactive

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_pause_and_resume.collidepoint(pygame.mouse.get_pos()):
                time_pause = False if time_pause == True else True
                last_update = pygame.time.get_ticks()
            if button_fast_forward.collidepoint(pygame.mouse.get_pos()):
                if fast_forward<4:
                    fast_forward*=2
                else:
                    fast_forward=1
            if not trading_column.collidepoint(pygame.mouse.get_pos()):
                showing_trading_column = False
                trading_input = ""
        
        if event.type == pygame.MOUSEBUTTONUP:
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
                    else:
                        if input_box_trading_width <= 20:
                            trading_input += event.unicode


    screen.blit(canvas, (0, 0))
    pygame.draw.rect(canvas, WHITE, (48, 80, 480, 320))
    draw_text_right(canvas, "000.0", 12, WHITE, 45, 72,font_msjh)
    draw_text_right(canvas, "000.0", 12, WHITE, 45, 392,font_msjh)
    #更新遊戲
    button_resume_symbol_png.set_alpha(170) if button_pause_and_resume.collidepoint(pygame.mouse.get_pos())&(not pygame.mouse.get_pressed()[0]) else button_resume_symbol_png.set_alpha(255)
    button_pause_symbol_png.set_alpha(170) if button_pause_and_resume.collidepoint(pygame.mouse.get_pos())&(not pygame.mouse.get_pressed()[0]) else button_pause_symbol_png.set_alpha(255)
    button_fast_forward_symbol_png.set_alpha(170) if button_fast_forward.collidepoint(pygame.mouse.get_pos())&(not pygame.mouse.get_pressed()[0]) else button_fast_forward_symbol_png.set_alpha(255)
    button_setting_symbol_png.set_alpha(170) if button_setting.collidepoint(pygame.mouse.get_pos())&(not pygame.mouse.get_pressed()[0]) else button_setting_symbol_png.set_alpha(255)
    button_buy_color = RED if button_buy.collidepoint(pygame.mouse.get_pos())&(not pygame.mouse.get_pressed()[0]) else (173, 0, 0)
    button_sell_color = GREEN if button_sell.collidepoint(pygame.mouse.get_pos())&(not pygame.mouse.get_pressed()[0]) else (0, 219, 0)

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

    pygame.draw.rect(screen, color_short_of_indicators_background, (576,0,WIDTH*2/5,HEIGHT))
    draw_text_left(screen, "000.0        +0.0        +0.00%", 24, WHITE, 606, 20, font_msjh)
    draw_text_left(screen, "open : 000.0  close : 000.0", 18, WHITE, 606, 60, font_msjh)
    draw_text_left(screen, "high : 000.0  low : 000.0", 18, WHITE, 606, 90, font_msjh)
    draw_text_left(screen, "volume : 00000  turnover : 000000000", 18, WHITE, 606, 120, font_msjh)
    draw_text_left(screen, "MA(5):000.0  MA(10):000.0  MA(20):000.0", 18, WHITE, 606, 150, font_msjh)
    draw_text_left(screen, "RSI(5):00.00  RSI(10):00.00  RSI(20):00.00", 18, WHITE, 606, 180, font_msjh)
    draw_text_left(screen, "K : 00.00  D : 00.00", 18, WHITE, 606, 210, font_msjh)
    draw_text_left(screen, "MACD : 00.00  MACD(9) : 00.00", 18, WHITE, 606, 240, font_msjh)
    draw_text_left(screen, "CMO(5) : 00.00  CMO(10) : 00.00", 18, WHITE, 606, 270, font_msjh)
    draw_text_left(screen, "WMSR(9) : 00.00", 18, WHITE, 606, 300, font_msjh)
    draw_text_left(screen, "SAR(0.02, 0.2) : 00.00", 18, WHITE, 606, 330, font_msjh)
    draw_text_left(screen, "CCI(14) : -00.00%", 18, WHITE, 606, 360, font_msjh)

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

    #pygame.draw.rect(screen, color_background, (800,-10,WIDTH/6+10,HEIGHT+10), border_radius=6)
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