import pygame
from sys import exit
import os
import time
import datetime
import random
import numpy
import pandas
import twstock
import talib
from talib import abstract


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
pygame.display.set_caption("Investment Game")
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(color_portfolio)
gaming_msg_background = pygame.Surface((WIDTH,HEIGHT))
gaming_msg_background.set_alpha(100)

font_none = pygame.font.match_font('none')
font_msjh = "微軟正黑體.ttf"

button_send_stock_code_png = pygame.image.load(os.path.join("arrow symbol.png")).convert()
button_send_stock_code_png.set_colorkey(BLACK)
button_send_stock_code_png = pygame.transform.scale(button_send_stock_code_png,(32,32))

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

def identity_date_text(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        date_text_list = date_text.split("-")
        date = datetime.date(int(date_text_list[0]), int(date_text_list[1]), int(date_text_list[2]))
        if date >= datetime.date(2010, 1, 1):
            if date >= datetime.date.today():
                return False
            else:
                return True
        else:
            return False
    except:
        return False

def identity_money_text(money_text):
    global Initial_Money
    try:
        Initial_Money = int(money_text)
        return True if Initial_Money >= 100000 else False
    except:
        return False

def continue_first_page():
    a, b, c = False, False, False
    global Initial_Date, End_Date
    global show_Please_enter_the_start_date, show_Please_enter_the_correct_format_Initial_Date, show_Please_enter_at_least_one_year_ago, show_Please_enter_the_correct_format_End_Date, show_Please_enter_at_least_one_year_of_the_duration, show_Please_enter_the_correct_format_Initial_Money, turn_to_next_page
    if Initial_Date_string == "yyyy-mm-dd":
        show_Please_enter_the_start_date = True
    elif not identity_date_text(Initial_Date_string):
        show_Please_enter_the_correct_format_Initial_Date = True
    else:
        Initial_Date = datetime.date(int(Initial_Date_string.split("-")[0]), int(Initial_Date_string.split("-")[1]), int(Initial_Date_string.split("-")[2]))
        Initial_Date_ = datetime.date.today() - datetime.timedelta(361)
        if Initial_Date > Initial_Date_:
            show_Please_enter_at_least_one_year_ago = True
        else:
            a = True

    if (End_Date_string != "~Yesterday")&(identity_date_text(End_Date_string) == False):
        show_Please_enter_the_correct_format_End_Date = True       
    else:
        if End_Date_string != "~Yesterday":
            End_Date = datetime.date(int(End_Date_string.split("-")[0]), int(End_Date_string.split("-")[1]), int(End_Date_string.split("-")[2]))
        if a:
            End_Date_ = End_Date - datetime.timedelta(360)
            if End_Date_ < Initial_Date:
                show_Please_enter_at_least_one_year_of_the_duration = True
            else:
                b = True

    if (Initial_Money_string != "NT$1000000")&(identity_money_text(Initial_Money_string) == False):
        show_Please_enter_the_correct_format_Initial_Money = True
    else:
        c = True
    
    if a&b&c:
        turn_to_next_page = True

def identity_stock_code(stock_code):
    try:
        if stock_code in twstock.twse:
            stock = twstock.Stock(stock_code)
            return False if not stock.fetch(Initial_Date.year, Initial_Date.month) else True
        else:
            return False
    except:
        return False

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

def draw_paragraph(surf, paragraph, n, size, color, x, y, row_space):
    string_list = split_string(paragraph, n)
    for i in range(len(string_list)):
        draw_text_left(surf, string_list[i], size, color, x, y+row_space*i, font_msjh)

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

def draw_used_strategies_list():
    used_strategy_string_width_list = []
    count = 0
    for i in Used_Strategies_list:
        if i == 1:
            used_strategy_string_width = draw_text_left(screen, ">移動平均線MA", 18, WHITE, 104, 231+count*24, font_msjh)
        elif i == 2:
            used_strategy_string_width = draw_text_left(screen, ">相對強弱指標RSI", 18, WHITE, 104, 231+count*24, font_msjh)
        elif i == 3:
            used_strategy_string_width = draw_text_left(screen, ">隨機指標KD", 18, WHITE, 104, 231+count*24, font_msjh)
        elif i == 4:
            used_strategy_string_width = draw_text_left(screen, ">移動平均離合線MACD", 18, WHITE, 104, 231+count*24, font_msjh)
        elif i == 5:
            used_strategy_string_width = draw_text_left(screen, ">動能振盪指標CMO", 18, WHITE, 104, 231+count*24, font_msjh)
        elif i == 6:
            used_strategy_string_width = draw_text_left(screen, ">威廉指標WMSR", 18, WHITE, 104, 231+count*24, font_msjh)
        elif i == 7:
            used_strategy_string_width = draw_text_left(screen, ">停損點轉向操作系統SAR", 18, WHITE, 104, 231+count*24, font_msjh)
        elif i == 8:
            used_strategy_string_width = draw_text_left(screen, ">商品通道指數CCI", 18, WHITE, 104, 231+count*24, font_msjh)
        pygame.draw.circle(screen, WHITE, (104+used_strategy_string_width+9, 240+count*24), 6)
        draw_text_centerx(screen, "-", 18, BLACK, 104+used_strategy_string_width+9, 233+count*24)

        used_strategy_string_width_list.append(used_strategy_string_width)
        count += 1
    return used_strategy_string_width_list
    
def start_second_page():
    a, b = False, False
    global show_Please_enter_the_investment_aim, show_Please_use_at_least_one_investment_strategy, Game_Start
    if Stock_Code == "":
        show_Please_enter_the_investment_aim = True
    else:
        a = True
    
    if Used_Strategies_count == 0:
        show_Please_use_at_least_one_investment_strategy = True
    else:    
        b = True

    if a&b:
        Game_Start = True

def frech_data_from_twstock(stock_code, initial_year, initial_month, end_year, end_month):
    stock = twstock.Stock(stock_code)
    database = []
    for i in range((end_year-initial_year-1)*12+(13-initial_month)+end_month):
        while initial_month+i>12:
            initial_month -= 12
            initial_year += 1
        database.append(stock.fetch(initial_year, initial_month+i))
        if i != (end_year-initial_year-1)*12+(13-initial_month)+end_month-1:
            time.sleep(random.randint(8, 12))
    return database

def get_last_open_day(df):
    date = Date
    i = 0
    while True:
        if str(date - datetime.timedelta(i)) in df.index:
            return date - datetime.timedelta(i)
        else:
            i += 1

def get_second_to_last_open_day(df):
    date = Date
    i = 0
    while True:
        if str(date - datetime.timedelta(i)) in df.index:
            break
        else:
            i += 1
    i += 1
    while True:
        if str(date - datetime.timedelta(i)) in df.index:
            return date - datetime.timedelta(i)
        else:
            i += 1

def get_20(date, dataframe):
    df = pandas.DataFrame([])
    i = 0
    while len(df) < 20:
        try:
            df = pandas.concat([df, pandas.DataFrame(dataframe.loc[str(date-datetime.timedelta(i))]).transpose()])
            i += 1
        except:
            i += 1
    return df

def draw_candlestick_chart(dataframe):
    max = dataframe["high"].max()
    min = dataframe["low"].min()
    for i in range(len(dataframe)):
        if dataframe["close"][i] < dataframe["open"][i]:
            color = GREEN
            pygame.draw.rect(screen, color, (504-24*i, 400-int((dataframe["open"][i]-min)*320/(max - min)), 24, int((dataframe["open"][i]-dataframe["close"][i])*320/(max - min))))
        else:
            color = RED
            pygame.draw.rect(screen, color, (504-24*i, 400-int((dataframe["close"][i]-min)*320/(max - min)), 24, int((dataframe["close"][i]-dataframe["open"][i])*320/(max - min))))
    draw_text_right(canvas, str(max), 12, WHITE, 45, 72,font_msjh)
    draw_text_right(canvas, str(min), 12, WHITE, 45, 392,font_msjh)

def database_to_dataframe(database):
    df = pandas.DataFrame([])
    for i in range(len(database)):
        df = pandas.concat([df, pandas.DataFrame(database[i])], ignore_index=True)
    df = df.set_index("date")
    df.rename(columns={"capacity":"volume"}, inplace=True)
    df["volume"] = df["volume"].div(1000)
    return df

def use_MA(dataframe):
    Strategies_Result["MA"] = {}
    Strategies_Result["MA"]["短中"] = []
    sSMA = abstract.MA(dataframe, timeperiod = 5)
    sMMA = abstract.MA(dataframe, timeperiod = 10)
    sLMA = abstract.MA(dataframe, timeperiod = 20)
    s1 = sSMA-sMMA
    df1 = pandas.DataFrame(s1)
    df1["date"] = df1.index
    for i in range(len(s1)-1):
        x = s1[i]*s1[i+1]
        if x <= 0:
            if s1[i] < s1[i+1]:
                Strategies_Result["MA"]["短中"].append(df1["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MA"]["短中"].append("buy")
            elif s1[i] > s1[i+1]:
                Strategies_Result["MA"]["短中"].append(df1["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MA"]["短中"].append("sell")

    Strategies_Result["MA"]["短長"] = []
    s2 = sSMA-sLMA
    df2 = pandas.DataFrame(s2)
    df2["date"] = df2.index
    for i in range(len(s2)-1):
        x = s2[i]*s2[i+1]
        if x <= 0:
            if s2[i] < s2[i+1]:
                Strategies_Result["MA"]["短長"].append(df2["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MA"]["短長"].append("buy")
            elif s2[i] > s2[i+1]:
                Strategies_Result["MA"]["短長"].append(df2["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MA"]["短長"].append("sell")
    
    Strategies_Result["MA"]["中長"] = []
    s3 = sMMA-sLMA
    df3 = pandas.DataFrame(s3)
    df3["date"] = df3.index
    for i in range(len(s3)-1):
        x = s3[i]*s3[i+1]
        if x <= 0:
            if s3[i] < s3[i+1]:
                Strategies_Result["MA"]["中長"].append(df3["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MA"]["中長"].append("buy")
            elif s3[i] > s3[i+1]:
                Strategies_Result["MA"]["中長"].append(df3["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MA"]["中長"].append("sell")
    return [sSMA, sMMA, sLMA]

def use_RSI(dataframe):
    Strategies_Result["RSI"] = {}
    Strategies_Result["RSI"]["短中"] = []
    sSRSI = abstract.RSI(dataframe, timeperiod = 5)
    sMRSI = abstract.RSI(dataframe, timeperiod = 10)
    sLRSI = abstract.RSI(dataframe, timeperiod = 20)
    s1 = sSRSI-sMRSI
    df1 = pandas.DataFrame(s1)
    df1["date"] = df1.index
    for i in range(len(s1)-1):
        x = s1[i]*s1[i+1]
        if x <= 0:
            if s1[i] < s1[i+1]:
                Strategies_Result["RSI"]["短中"].append(df1["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["RSI"]["短中"].append("buy")
            elif s1[i] > s1[i+1]:
                Strategies_Result["RSI"]["短中"].append(df1["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["RSI"]["短中"].append("sell")

    Strategies_Result["RSI"]["短長"] = []
    s2 = sSRSI-sLRSI
    df2 = pandas.DataFrame(s2)
    df2["date"] = df2.index
    for i in range(len(s2)-1):
        x = s2[i]*s2[i+1]
        if x <= 0:
            if s2[i] < s2[i+1]:
                Strategies_Result["RSI"]["短長"].append(df2["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["RSI"]["短長"].append("buy")
            elif s2[i] > s2[i+1]:
                Strategies_Result["RSI"]["短長"].append(df2["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["RSI"]["短長"].append("sell")

    Strategies_Result["RSI"]["中長"] = []
    s3 = sMRSI-sLRSI
    df3 = pandas.DataFrame(s3)
    df3["date"] = df3.index
    for i in range(len(s3)-1):
        x = s3[i]*s3[i+1]
        if x <= 0:
            if s3[i] < s3[i+1]:
                Strategies_Result["RSI"]["中長"].append(df3["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["RSI"]["中長"].append("buy")
            elif s3[i] > s3[i+1]:
                Strategies_Result["RSI"]["中長"].append(df3["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["RSI"]["中長"].append("sell")
    return [sSRSI, sMRSI, sLRSI]

def use_KD(dataframe):
    Strategies_Result["KD"] = []
    s = abstract.STOCH(dataframe, fastk_period=9)
    sK = s.loc[:,"slowk"]
    sD = s.loc[:,"slowd"]
    s = sK - sD
    df = pandas.DataFrame(s)
    df["date"] = df.index
    for i in range(len(s)-1):
        x = s[i]*s[i+1]
        if x <= 0:
            if s[i] < s[i+1]:
                Strategies_Result["KD"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["KD"].append("buy")
            elif s[i] > s[i+1]:
                Strategies_Result["KD"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["KD"].append("sell")
    return [sK, sD]

def use_MACD(dataframe):
    Strategies_Result["MACD"] = []
    s = abstract.MACD(dataframe)
    sMACD = s.loc[:,"macd"]
    sMACDsignal = s.loc[:,"macdsignal"]
    sMACDhist = s.loc[:,"macdhist"]
    df = pandas.DataFrame(sMACDhist)
    df["date"] = df.index
    for i in range(len(sMACDhist)-1):
        x = sMACDhist[i]*sMACDhist[i+1]
        if x <= 0:
            if sMACDhist[i] < sMACDhist[i+1]:
                Strategies_Result["MACD"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MACD"].append("buy")
            elif sMACDhist[i] > sMACDhist[i+1]:
                Strategies_Result["MACD"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["MACD"].append("sell")
    return [sMACD, sMACDsignal, sMACDhist]

def use_CMO(dataframe):
    Strategies_Result["CMO"] = []
    sSCMO = abstract.CMO(dataframe, timeperiod = 5)
    sLCMO = abstract.CMO(dataframe, timeperiod = 10)
    s = sSCMO - sLCMO
    df = pandas.DataFrame(s)
    df["date"] = df.index
    for i in range(len(s)-1):
        x = s[i]*s[i+1]
        if x <= 0:
            if s[i] < s[i+1]:
                Strategies_Result["CMO"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["CMO"].append("buy")
            elif s[i] > s[i+1]:
                Strategies_Result["CMO"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["CMO"].append("sell")
    return [sSCMO, sLCMO]

def use_WMSR(dataframe):
    Strategies_Result["WMSR"] = []
    s = abstract.WILLR(dataframe, timeperiod=9)
    df = pandas.DataFrame(s)
    df["date"] = df.index
    for i in range(len(s)):
        if s[i] <= -80:
            Strategies_Result["WMSR"].append(df["date"][i].date()+datetime.timedelta(1))
            Strategies_Result["WMSR"].append("buy")
        elif s[i] >= -20:
            Strategies_Result["WMSR"].append(df["date"][i].date()+datetime.timedelta(1))
            Strategies_Result["WMSR"].append("sell")
    return s

def use_SAR(dataframe):
    Strategies_Result["SAR"] = []
    s = dataframe.loc[:,"close"]
    sSAR = abstract.SAR(dataframe, acceleration=0.02, maximum=0.2)
    s = s - sSAR
    df = pandas.DataFrame(s)
    df["date"] = df.index
    for i in range(len(s)-1):
        x = s[i]*s[i+1]
        if x <= 0:
            if s[i] < s[i+1]:
                Strategies_Result["SAR"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["SAR"].append("buy")
            elif s[i] > s[i+1]:
                Strategies_Result["SAR"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["SAR"].append("sell")
    return sSAR

def use_CCI(dataframe):
    Strategies_Result["CCI"] = []
    s = abstract.CCI(dataframe)
    df = pandas.DataFrame(s)
    df["date"] = df.index
    s1 = s.sub(100)
    s2 = s.add(100)
    for i in range(len(s)-1):
        x = s1[i]*s1[i+1]
        y = s2[i]*s2[i+1]
        if x <= 0:
            if s1[i] < s1[i+1]:
                Strategies_Result["CCI"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["CCI"].append("buy")
        if y <= 0:
            if s2[i] > s2[i+1]:
                Strategies_Result["CCI"].append(df["date"][i+1].date()+datetime.timedelta(1))
                Strategies_Result["CCI"].append("sell")
    return s

def game_display():
    screen.blit(canvas, (0, 0))
    canvas.fill(color_portfolio)
    draw_candlestick_chart(get_20(Date, DF))

    draw_text_left(screen, Stock_Code+" "+Stock_Name, 24, WHITE, 30, 30, font_msjh)
    pygame.draw.circle(screen, (107, 107, 107), (480,42), 18)
    pygame.draw.circle(screen, button_buy_color, (480,42), 16)
    pygame.draw.circle(screen, (107, 107, 107), (540,42), 18)
    pygame.draw.circle(screen, button_sell_color, (540,42), 16)
    draw_text_centerx(screen, "buy ", 16, (224, 224, 224), 481, 37)
    draw_text_centerx(screen, "sell ", 16, (79, 79, 79), 541, 37)

    pygame.draw.rect(screen, color_short_of_indicators_background, (576, 0, WIDTH*2/5, HEIGHT))
    draw_text_left(screen, str(float(DF.loc[str(get_last_open_day(DF)),["close"]]))+"        "+str(float(DF.loc[str(get_last_open_day(DF)),["change"]]))+"        "+str(round(float(DF.loc[str(get_last_open_day(DF)),["change"]])/float(DF.loc[str(get_second_to_last_open_day(DF)),["close"]]),2))+"%", 24, WHITE, 606, 20, font_msjh)
    draw_text_left(screen, "open : "+str(float(DF.loc[str(get_last_open_day(DF)),["open"]]))+"  close : "+str(float(DF.loc[str(get_last_open_day(DF)),["close"]])), 18, WHITE, 606, 60, font_msjh)
    draw_text_left(screen, "high : "+str(float(DF.loc[str(get_last_open_day(DF)),["high"]]))+"  low : "+str(float(DF.loc[str(get_last_open_day(DF)),["low"]])), 18, WHITE, 606, 90, font_msjh)
    draw_text_left(screen, "volume : "+str(int(DF.loc[str(get_last_open_day(DF)),["volume"]])), 18, WHITE, 606, 120, font_msjh)
    draw_text_left(screen, "MA(5):"+str(round(MA[0][str(get_last_open_day(DF))],1))+"  MA(10):"+str(round(MA[1][str(get_last_open_day(DF))],1))+"  MA(20):"+str(round(MA[2][str(get_last_open_day(DF))],1)), 18, WHITE, 606, 150, font_msjh)
    draw_text_left(screen, "RSI(5):"+str(round(RSI[0][str(get_last_open_day(DF))],2))+"  RSI(10):"+str(round(RSI[1][str(get_last_open_day(DF))],2))+"  RSI(20):"+str(round(RSI[2][str(get_last_open_day(DF))],2)), 18, WHITE, 606, 180, font_msjh)
    draw_text_left(screen, "K : "+str(round(KD[0][str(get_last_open_day(DF))],2))+"  D : "+str(round(KD[1][str(get_last_open_day(DF))],2)), 18, WHITE, 606, 210, font_msjh)
    draw_text_left(screen, "MACD : "+str(round(MACD[0][str(get_last_open_day(DF))],2))+"  MACD(9) : "+str(round(MACD[1][str(get_last_open_day(DF))],2)), 18, WHITE, 606, 240, font_msjh)
    draw_text_left(screen, "CMO(5) : "+str(round(CMO[0][str(get_last_open_day(DF))],2))+"  CMO(10) : "+str(round(CMO[1][str(get_last_open_day(DF))],2)), 18, WHITE, 606, 270, font_msjh)
    draw_text_left(screen, "WMSR(9) : "+str(round(WMSR[str(get_last_open_day(DF))],2)), 18, WHITE, 606, 300, font_msjh)
    draw_text_left(screen, "SAR(0.02, 0.2) : "+str(round(SAR[str(get_last_open_day(DF))],2)), 18, WHITE, 606, 330, font_msjh)
    draw_text_left(screen, "CCI(14) : "+str(round(CCI[str(get_last_open_day(DF))],2))+"%", 18, WHITE, 606, 360, font_msjh)

    pygame.draw.rect(screen, color_game_time_board, (0,440,WIDTH,100))
    draw_text_left(screen, "Date "+str(Date), 40, color_game_time_board_text, WIDTH/16, 480)
    if str(Date) in DF.index:
        draw_text_left(screen, "開市", 18, color_game_time_board_text, WIDTH/16+224, 480, font_msjh)
    else:
        draw_text_left(screen, "休市", 18, color_game_time_board_text, WIDTH/16+224, 480, font_msjh)
    if time_pause:
        screen.blit(button_resume_symbol_png, (360,450))
    else:
        screen.blit(button_pause_symbol_png, (360,450))
    draw_text_left(screen, str(fast_forward)+"x", 18, color_game_time_board_text, 586,496)
    screen.blit(button_fast_forward_symbol_png, (540,460))
    screen.blit(button_setting_symbol_png, (720,460))

    #pygame.draw.rect(screen, color_background, (800,-10,WIDTH/6+10,HEIGHT+10), border_radius=6)

def show_setting():
    showing_setting = True
    while showing_setting:
        clock.tick(FPS)
        game_display()
        screen.blit(gaming_msg_background, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if button_End_Game_str.collidepoint(pygame.mouse.get_pos()):
                    the_end(Initial_Date, Date, Initial_Money, Money, Stock_Code)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing_setting = False


        button_setting_str_color = (51, 51, 51) if (button_setting_str.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else BLACK
        button_End_Game_str_color = (51, 51, 51) if (button_End_Game_str.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else BLACK
        
        draw_text_left(screen, "Setting", 32, button_setting_str_color, WIDTH*13/16, 465)
        draw_text_left(screen, "End Game", 32, button_End_Game_str_color, WIDTH*13/16, 495)
        pygame.display.update()

def show_msg(stock_code, text, date, suggest):
    showing_msg = True
    while showing_msg:
        clock.tick(FPS)
        game_display()
        screen.blit(gaming_msg_background, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not output_box_msg.collidepoint(pygame.mouse.get_pos()):
                    showing_msg = False


        pygame.draw.rect(screen, color_game_time_board, (WIDTH*3/8-60, 135, 360, 270))
        pygame.draw.rect(screen, color_game_time_board_text, (WIDTH*3/8-60, 135, 360, 270),2)
        draw_text_left(screen, stock_code, 24, color_game_time_board_text, 300+30, 150, font_msjh)
        draw_text_left(screen, date, 24, color_game_time_board_text, 300+30, 195, font_msjh)
        draw_text_left(screen, text, 20, color_game_time_board_text, 300+30, 240, font_msjh)
        draw_text_left(screen, suggest, 20, color_game_time_board_text, 300+30, 285, font_msjh)
        pygame.display.update()

def show_trading_column(money, hold, direct, input):
    pygame.draw.rect(screen, color_game_time_board, (453,0,114,63))
    pygame.draw.rect(screen, color_game_time_board_text, (453,0,114,63), 1)
    draw_text_left(screen, "Hold", 18, color_game_time_board_text, 470, 8)
    draw_text_centerx(screen, str(hold), 18, color_game_time_board_text, 528, 8)
    draw_text_left(screen, "張", 10, color_game_time_board_text, 540,7, font_msjh)
    draw_text_centerx(screen, "NT$"+str(int(money)), 18, color_game_time_board_text, 510, 25)

    if direct == True:
        draw_text_right(screen, "buy :", 18, color_game_time_board_text, 497, 43)
    else:
        draw_text_right(screen, "sell :", 18, color_game_time_board_text, 497, 43)
    input_box_trading_width = draw_text_centerx(screen, input, 18, color_game_time_board_text, 524, 42)
    pygame.draw.rect(screen, color_game_time_board_text, (507,53,36,1))

    pygame.draw.circle(screen, color_game_time_board_text, (556,49), 8)
    draw_text_left(screen, "->", 18, color_game_time_board, 551,42)
    return input_box_trading_width

def identity_trading_input_text(text, direct, stock_code):
    global Trading_Input, DF, Date, Money, Stock_stored
    try:
        Trading_Input = int(text)
        if direct == True:
            if Trading_Input*float(DF.loc[str(Date),["close"]])*1000 <= Money:
                Money -= Trading_Input*float(DF.loc[str(Date),["close"]])*1000
                Stock_stored[stock_code] += Trading_Input
                return True
            else:
                return False
        else:
            if Trading_Input <= Stock_stored[stock_code]:
                Money += Trading_Input*float(DF.loc[str(Date),["close"]])*1000
                Stock_stored[stock_code] -= Trading_Input
                return True
            else:
                return False
    except:
        return False

def the_end(initial_date, end_date, initial_money, money, stock_code):
    money += Stock_stored[Stock_Code]*float(DF.loc[str(get_last_open_day(DF)),["close"]])*1000
    used_strategies_str = ""
    for i in Used_Strategies_list:
        if i == 1:
            used_strategies_str = used_strategies_str+"MA "
        elif i == 2:
            used_strategies_str = used_strategies_str+"RSI "
        elif i == 3:
            used_strategies_str = used_strategies_str+"KD "
        elif i == 4:
            used_strategies_str = used_strategies_str+"MACD "
        elif i == 5:
            used_strategies_str = used_strategies_str+"CMO "
        elif i == 6:
            used_strategies_str = used_strategies_str+"WMSR "
        elif i == 7:
            used_strategies_str = used_strategies_str+"SAR "
        elif i == 8:
            used_strategies_str = used_strategies_str+"CCI "
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if button_back_to_init.collidepoint(pygame.mouse.get_pos()):
                    init()

        button_back_to_init_color = color_active if (button_back_to_init.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else color_inactive

        screen.fill(color_short_of_indicators_background)
        draw_text_left(screen, "日期："+str(initial_date)+" ~ "+str(end_date), 28, color_active, 90, 60, font_msjh)
        draw_text_left(screen, "起始金錢：NT$"+str(initial_money), 24, color_active, 122, 130, font_msjh)
        draw_text_left(screen, "結束金錢：NT$"+str(int(money)), 24, color_active, 122, 190, font_msjh)
        draw_text_left(screen, "投資報酬率ROI："+str(round((money-initial_money)/initial_money*100,2))+"%", 24, color_active, 122, 250, font_msjh)
        draw_text_left(screen, "標的 "+str(stock_code)+"  參考 "+used_strategies_str, 16, color_active, 442, 130, font_msjh)
        draw_text_centerx(screen, "回主畫面", 24, button_back_to_init_color, 870, 472, font_msjh)
        pygame.display.update()

def init():
    pass


Initial_Date = datetime.date(2010,1,1)
Initial_Date_string = "yyyy-mm-dd"
input_box_Initial_Date = pygame.Rect(0, 0, 140, 32)
input_box_Initial_Date.x = WIDTH/2-input_box_Initial_Date.w
input_box_Initial_Date.y = HEIGHT/4-5
input_box_Initial_Date_active = False
input_box_Initial_Date_triggered = False
input_box_Initial_Date_color = color_inactive
Initial_Date_string_color = color_preset_string
show_Please_enter_the_start_date = False
show_Please_enter_the_correct_format_Initial_Date = False
show_Please_enter_at_least_one_year_ago = False

End_Date = datetime.date.today() - datetime.timedelta(1)
End_Date_string = "~Yesterday"
input_box_End_Date = pygame.Rect(0, 0, 140, 32)
input_box_End_Date.x = WIDTH/2-input_box_End_Date.w
input_box_End_Date.y = HEIGHT*2/4-5
input_box_End_Date_active = False
input_box_End_Date_color = color_inactive
show_Please_enter_the_correct_format_End_Date = False
show_Please_enter_at_least_one_year_of_the_duration = False

Initial_Money = 1000000
Initial_Money_string = "NT$1000000"
input_box_Initial_Money = pygame.Rect(0, 0, 140, 32)
input_box_Initial_Money.x = WIDTH/2-input_box_Initial_Money.w 
input_box_Initial_Money.y = HEIGHT*3/4-5
input_box_Initial_Money_active = False
input_box_Initial_Money_color = color_inactive
show_Please_enter_the_correct_format_Initial_Money = False

button_Continue = pygame.Rect(806, 480, 128, 24)
button_Continue_color = color_inactive

turn_to_next_page = False

button_Back = pygame.Rect(58, 60, 65, 27)
button_Back_color = color_inactive

input_Stock_Code = "2330"
Stock_Code = ""
Stock_Name = ""
input_box_Stock_Code = pygame.Rect(0, 0, 140, 32)
input_box_Stock_Code.x = WIDTH/3-input_box_Stock_Code.w/2
input_box_Stock_Code.y = HEIGHT/4-5
input_box_Stock_Code_active = False
input_box_Stock_Code_color = color_inactive
show_Data_not_found = False

button_send_stock_code = pygame.Rect(input_box_Stock_Code.right+7,input_box_Stock_Code.y+2, 28, 28)

output_box_Portfolio = pygame.Rect(WIDTH/12, HEIGHT*7/20, 360, 300)
Used_Strategies_list = []
Used_Strategies_count = len(Used_Strategies_list)

output_box_Short_Of_Indicators = pygame.Rect(WIDTH/2+60, 60, 360, 432)
Short_Of_Indicators_page = 1#0
button_Using_the_strategy = pygame.Rect(output_box_Short_Of_Indicators.x+264, output_box_Short_Of_Indicators.y+342, 72, 24)
button_Using_the_strategy_color = color_inactive
button_Short_Of_Indicators_last_page = pygame.Rect(output_box_Short_Of_Indicators.x+output_box_Short_Of_Indicators.w/2-60-15, output_box_Short_Of_Indicators.y+398, 30, 18)
button_Short_Of_Indicators_last_page_color = color_inactive
button_Short_Of_Indicators_next_page = pygame.Rect(output_box_Short_Of_Indicators.x+output_box_Short_Of_Indicators.w/2+60-15, output_box_Short_Of_Indicators.y+398, 30, 18)
button_Short_Of_Indicators_next_page_color = color_inactive

button_Start = pygame.Rect(360, 449, 56, 24)
button_Start_color = color_inactive

Game_Start = False
show_Please_enter_the_investment_aim = False
show_Please_use_at_least_one_investment_strategy = False

Database = []
Strategies_Result = {}
Stock_stored = {}

time_pause = True
last_update = pygame.time.get_ticks()
update_rate = 1000
fast_forward = 1

Date = Initial_Date
days = 0

have_shown_msg = False

output_box_msg = pygame.Rect(WIDTH*3/8-60, 135, 360, 270)

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

trading_input = ""
Trading_Direct = True
Trading_Input = 0
Money = Initial_Money

showing_trading_column = False
trading_column = pygame.Rect(453,0,114,63)
button_send_trading = pygame.Rect(550, 43, 12, 12)
show_Unable_to_operate = False

button_back_to_init = pygame.Rect(825, 480, 90, 20)
button_back_to_init_color = color_inactive


while running:
    clock.tick(FPS)
    if not turn_to_next_page:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_Initial_Date.collidepoint(event.pos):
                    input_box_Initial_Date_active = True
                    show_Please_enter_the_start_date = False
                    show_Please_enter_the_correct_format_Initial_Date = False
                    show_Please_enter_at_least_one_year_ago = False
                else:
                    input_box_Initial_Date_active = False
                input_box_Initial_Date_color = color_active if input_box_Initial_Date_active else color_inactive
                if (input_box_Initial_Date.collidepoint(event.pos))&(Initial_Date_string == "yyyy-mm-dd"):
                    Initial_Date_string = ""
                    input_box_Initial_Date_triggered = True

                if input_box_End_Date.collidepoint(event.pos):
                    input_box_End_Date_active = True
                    show_Please_enter_the_correct_format_End_Date = False
                    show_Please_enter_at_least_one_year_of_the_duration = False
                else:
                    input_box_End_Date_active = False
                input_box_End_Date_color = color_active if input_box_End_Date_active else color_inactive
                if (input_box_End_Date.collidepoint(event.pos))&(End_Date_string == "~Yesterday"):
                    End_Date_string = ""

                if input_box_Initial_Money.collidepoint(event.pos):
                    input_box_Initial_Money_active = True
                    show_Please_enter_the_correct_format_Initial_Money = False
                else:
                    input_box_Initial_Money_active = False
                input_box_Initial_Money_color = color_active if input_box_Initial_Money_active else color_inactive
                if (input_box_Initial_Money.collidepoint(event.pos))&(Initial_Money_string == "NT$1000000"):
                    Initial_Money_string = ""

            if event.type == pygame.MOUSEBUTTONUP:
                if button_Continue.collidepoint(pygame.mouse.get_pos()):
                    continue_first_page()
                        
            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_TAB:
                    if input_box_Initial_Date_active:
                        if event.key == pygame.K_RETURN:
                            input_box_Initial_Date_active = False
                            input_box_Initial_Date_color = color_inactive
                        elif event.key == pygame.K_BACKSPACE:
                            Initial_Date_string = Initial_Date_string[:-1]
                        elif event.key == pygame.K_DELETE:
                            Initial_Date_string = ""
                        else:
                            if Initial_Date_string_width <= 120:
                                Initial_Date_string += event.unicode

                    elif input_box_End_Date_active:
                        if event.key == pygame.K_RETURN:
                            input_box_End_Date_active = False
                            input_box_End_Date_color = color_inactive
                        elif event.key == pygame.K_BACKSPACE:
                            End_Date_string = End_Date_string[:-1]
                        elif event.key == pygame.K_DELETE:
                            End_Date_string = ""
                        else:
                            if End_Date_string_width <= 120:
                                End_Date_string += event.unicode

                    elif input_box_Initial_Money_active:
                        if event.key == pygame.K_RETURN:
                            input_box_Initial_Money_active = False
                            input_box_Initial_Money_color = color_inactive
                        elif event.key == pygame.K_BACKSPACE:
                            Initial_Money_string = Initial_Money_string[:-1]
                        elif event.key == pygame.K_DELETE:
                            Initial_Money_string = ""
                        else:
                            Initial_Money_string += event.unicode
                    
                    else:
                        if event.key == pygame.K_RETURN:
                            continue_first_page()

        screen.fill(color_background)
        #更新遊戲
        if input_box_Initial_Date_triggered:
            Initial_Date_string_color = input_box_Initial_Date_color

        button_Continue_color = color_active if (button_Continue.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else color_inactive


        #畫面顯示
        draw_text_right(screen, "Initial Date:", 32, color_active, WIDTH/3, HEIGHT/4)
        Initial_Date_string_width = draw_text_right(screen, Initial_Date_string, 32, Initial_Date_string_color, input_box_Initial_Date.x+input_box_Initial_Date.w-5, input_box_Initial_Date.y+5)
        pygame.draw.rect(screen, input_box_Initial_Date_color, input_box_Initial_Date, 3)
        if show_Please_enter_the_start_date:
            draw_text_left(screen, "Please enter the start date", 16, RED, input_box_Initial_Date.x+2, input_box_Initial_Date.bottom)
        elif show_Please_enter_the_correct_format_Initial_Date:
            draw_text_left(screen, "Please enter the correct format", 16, RED, input_box_Initial_Date.x+2, input_box_Initial_Date.bottom)
        elif show_Please_enter_at_least_one_year_ago:
            draw_text_left(screen, "Please enter at least one year ago", 16, RED, input_box_Initial_Date.x+2, input_box_Initial_Date.bottom)
    
        draw_text_right(screen, "End Date:", 32, color_active, WIDTH/3, HEIGHT*2/4)
        End_Date_string_width = draw_text_right(screen, End_Date_string, 32, input_box_End_Date_color, input_box_End_Date.x+input_box_End_Date.width-5, input_box_End_Date.y+5)
        pygame.draw.rect(screen, input_box_End_Date_color, input_box_End_Date, 3)
        if show_Please_enter_the_correct_format_End_Date:
            draw_text_left(screen, "Please enter the correct format", 16, RED, input_box_End_Date.x+2, input_box_End_Date.bottom)
        elif show_Please_enter_at_least_one_year_of_the_duration:
            draw_text_left(screen, "Please enter at least one year of the duration", 16, RED, input_box_End_Date.x+2, input_box_End_Date.bottom)

        draw_text_right(screen, "Money:", 32, color_active, WIDTH/3, HEIGHT*3/4)
        Initial_Money_string_width = draw_text_right(screen, Initial_Money_string, 32, input_box_Initial_Money_color, input_box_Initial_Money.x+input_box_Initial_Money.w-5, input_box_Initial_Money.y+5)
        input_box_Initial_Money.w = max(140, Initial_Money_string_width+8)
        pygame.draw.rect(screen, input_box_Initial_Money_color, input_box_Initial_Money, 3)
        if show_Please_enter_the_correct_format_Initial_Money:
            draw_text_left(screen, "Please enter the correct format", 16, RED, input_box_Initial_Money.x+2, input_box_Initial_Money.bottom)

        draw_text_centerx(screen, "Continue", 40, button_Continue_color, 870, 480)

        draw_text_left(screen, "2010-01-01 ~ one year ago", 32, color_inactive, input_box_Initial_Date.right+8, input_box_Initial_Date.y+5)
        draw_text_left(screen, "Ex:2022-12-09, at least one year", 32, color_inactive, input_box_End_Date.right+8, input_box_End_Date.y+5)
        draw_text_left(screen, "At least 100000 Ex:30000000", 32, color_inactive, input_box_Initial_Money.right+8, input_box_Initial_Money.y+5)
        #draw_text_left(screen, "Auto-adjusted to the closest market opening date", 32, color_active, input_box_Initial_Date.left+2, input_box_Initial_Date.bottom+18)
        #draw_text_left(screen, "Auto-adjusted to the closest market opening date", 32, color_active, input_box_End_Date.left+2, input_box_End_Date.bottom+18)
    else:
        if not Game_Start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box_Stock_Code.collidepoint(event.pos):
                        input_box_Stock_Code_active = True
                        show_Data_not_found = False
                    else:
                        input_box_Stock_Code_active = False
                    input_box_Stock_Code_color = color_active if input_box_Stock_Code_active else color_inactive

                if event.type == pygame.MOUSEBUTTONUP:
                    if button_Back.collidepoint(pygame.mouse.get_pos()):
                        turn_to_next_page = False
                    if button_send_stock_code.collidepoint(pygame.mouse.get_pos()):
                        if identity_stock_code(input_Stock_Code):
                            show_Data_not_found = False
                            show_Please_enter_the_investment_aim = False
                            Stock_Code = input_Stock_Code
                            Stock_Name = twstock.twse[Stock_Code][2]
                        else:
                            show_Data_not_found = True
                    if button_Using_the_strategy.collidepoint(pygame.mouse.get_pos()):
                        if Short_Of_Indicators_page > 0:
                            show_Please_use_at_least_one_investment_strategy = False
                            Used_Strategies_list.append(Short_Of_Indicators_page)
                            Used_Strategies_list = list(dict.fromkeys(Used_Strategies_list))
                    if button_Short_Of_Indicators_last_page.collidepoint(pygame.mouse.get_pos()):
                        if Short_Of_Indicators_page > 0:
                            Short_Of_Indicators_page -= 1
                    if button_Short_Of_Indicators_next_page.collidepoint(pygame.mouse.get_pos()):
                        if Short_Of_Indicators_page < 8:
                            Short_Of_Indicators_page += 1
                    if pygame.Rect(176+Stock_Code_and_Stock_Name_width+4,197,10,10).collidepoint(pygame.mouse.get_pos()):
                        if Stock_Code != "":
                            Stock_Code = ""
                            Stock_Name = ""
                    for i in range(Used_Strategies_count):
                        if pygame.Rect(104+draw_used_strategies_list()[i]+4,235+i*24,10,10).collidepoint(pygame.mouse.get_pos()):
                            Used_Strategies_list.pop(i)
                            break
                    if button_Start.collidepoint(pygame.mouse.get_pos()):
                        start_second_page()


                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_TAB:
                        if input_box_Stock_Code_active:
                            if event.key == pygame.K_RETURN:
                                input_box_Stock_Code_active = False
                                input_box_Stock_Code_color = color_inactive
                            elif event.key == pygame.K_BACKSPACE:
                                input_Stock_Code = input_Stock_Code[:-1]
                            elif event.key == pygame.K_DELETE:
                                input_Stock_Code = ""
                            else:
                                if Stock_Code_width <= 120:
                                    input_Stock_Code += event.unicode


            screen.fill(color_background)
            #更新遊戲
            button_Back_color = color_active if (button_Back.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else color_inactive
            color_button_send_stock_code = color_button_send_2 if (button_send_stock_code.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else color_button_send_1
            button_Using_the_strategy_color = (251, 253, 254) if (button_Using_the_strategy.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else (66, 155, 215)
            button_Short_Of_Indicators_last_page_color = color_active if (button_Short_Of_Indicators_last_page.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else color_inactive    
            button_Short_Of_Indicators_next_page_color = color_active if (button_Short_Of_Indicators_next_page.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else color_inactive
            Used_Strategies_count = len(Used_Strategies_list)
            button_Start_color = color_active if (button_Start.collidepoint(pygame.mouse.get_pos()))&(not pygame.mouse.get_pressed()[0]) else color_inactive


            #畫面顯示
            draw_text_centerx(screen, "Back", 40, button_Back_color, 90, 60)

            draw_text_right(screen, "Stock Code:", 32, color_active, WIDTH/4, HEIGHT/4)
            Stock_Code_width = draw_text_right(screen, input_Stock_Code, 32, input_box_Stock_Code_color, input_box_Stock_Code.x+input_box_Stock_Code.w-5, input_box_Stock_Code.y+5)
            pygame.draw.rect(screen, input_box_Stock_Code_color, input_box_Stock_Code, 3)
            pygame.draw.circle(screen, color_button_send_stock_code, (input_box_Stock_Code.right+21,input_box_Stock_Code.y+input_box_Stock_Code.h/2), 16)
            screen.blit(button_send_stock_code_png, (input_box_Stock_Code.right+5,input_box_Stock_Code.y))
            if show_Data_not_found:
                draw_text_right(screen, "Data not found", 16, RED, input_box_Stock_Code.right-2, input_box_Stock_Code.bottom)

            pygame.draw.rect(screen, color_portfolio, output_box_Portfolio, border_radius=4)
            draw_text_left(screen, "標的：", 24, WHITE, 104, 199, font_msjh)
            if pygame.font.Font(font_msjh, 24).render(Stock_Code+" "+Stock_Name, True, WHITE).get_width() < 240:
                Stock_Code_and_Stock_Name_width = draw_text_left(screen, Stock_Code+" "+Stock_Name, 24, WHITE, 176, 199, font_msjh)
            else:
                Stock_Code_and_Stock_Name_width = draw_text_left(screen, Stock_Code+" "+Stock_Name, 18, WHITE, 176, 205, font_msjh)
            if Stock_Code != "":
                pygame.draw.circle(screen, RED, (176+Stock_Code_and_Stock_Name_width+9,202), 6)
                draw_text_centerx(screen, "x", 18, WHITE, 176+Stock_Code_and_Stock_Name_width+9, 195)
            draw_used_strategies_list()

            pygame.draw.rect(screen, color_short_of_indicators_background, output_box_Short_Of_Indicators)
            draw_short_of_indicators(Short_Of_Indicators_page)
            if Short_Of_Indicators_page > 0:
                draw_text_right(screen, "使用策略", 18, button_Using_the_strategy_color, 876, 402, font_msjh)
            draw_text_right(screen, "<<         ", 18, button_Short_Of_Indicators_last_page_color, 720, 452, font_msjh)
            draw_text_left(screen, "         >>", 18, button_Short_Of_Indicators_next_page_color, 720, 452, font_msjh)
            draw_text_centerx(screen, str(Short_Of_Indicators_page), 18, color_active, 720, 452, font_msjh)

            draw_text_right(screen, "Start", 36, button_Start_color, 416, 449)
            if show_Please_enter_the_investment_aim:
                draw_text_right(screen, "Please enter the investment aim", 16, RED, output_box_Portfolio.right-2, output_box_Portfolio.bottom)
            elif show_Please_use_at_least_one_investment_strategy:
                draw_text_right(screen, "Please use at least one investment strategy", 16, RED, output_box_Portfolio.right-2, output_box_Portfolio.bottom)
        else:
            if Database == []:
                screen.fill(BLACK)
                draw_text_centerx(screen, "Loading Data", 48, WHITE, WIDTH/2, HEIGHT/2-24)
                pygame.display.update()
                try:
                    if (Initial_Date.year == 2010)&(Initial_Date.month <= 2):
                        Initial_Date_ = Initial_Date
                    else:
                        Initial_Date_ = Initial_Date - datetime.timedelta(59)
                    Database = frech_data_from_twstock(Stock_Code, Initial_Date_.year, Initial_Date_.month, End_Date.year, End_Date.month)
                    DF = database_to_dataframe(Database)

                except:
                    screen.fill(BLACK)
                    draw_text_centerx(screen, "Loading Failed", 48, WHITE, WIDTH/2, HEIGHT/2-24)
                    draw_text_centerx(screen, "Please try to change your IP Address", 20, WHITE, WIDTH/2, HEIGHT/2+8)
                    waiting = True
                    while waiting:
                        clock.tick(FPS)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                        pygame.display.update()
                MA = use_MA(DF)
                RSI   = use_RSI(DF)
                KD = use_KD(DF)
                MACD = use_MACD(DF)
                CMO = use_CMO(DF)
                WMSR = use_WMSR(DF)
                SAR = use_SAR(DF)
                CCI = use_CCI(DF)
                
                Stock_stored[Stock_Code] = 0

                time_pause = True
                last_update = pygame.time.get_ticks()
                update_rate = 1000
                fast_forward = 1

                Date = Initial_Date
                days = 0

                Money = Initial_Money
            else:
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
                        if button_setting.collidepoint(pygame.mouse.get_pos()):
                            show_setting()
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
                                if not identity_trading_input_text(trading_input, Trading_Direct, Stock_Code):
                                    showing_trading_column = False
                                    trading_input = ""
                                    show_Unable_to_operate = True
                                    show_Unable_to_operate_time = pygame.time.get_ticks()
                                        
                    
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
                        have_shown_msg = False
                if Date < End_Date:
                    Date = Initial_Date+datetime.timedelta(days)
                else:
                    pygame.time.wait(1000)
                    the_end(Initial_Date, Date, Initial_Money, Money, Stock_Code)
                if not have_shown_msg:
                    for i in Used_Strategies_list:
                        if i == 1:
                            for date in Strategies_Result["MA"]["短中"]:
                                if Date == date:
                                    index = Strategies_Result["MA"]["短中"].index(date)
                                    if Strategies_Result["MA"]["短中"][index+1] == "buy":
                                        show_msg(Stock_Code, "短期MA已向上突破中期MA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["MA"]["短中"][index+1] == "sell":
                                        show_msg(Stock_Code, "短期MA已向下突破中期MA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                            for date in Strategies_Result["MA"]["短長"]:
                                if Date == date:
                                    index = Strategies_Result["MA"]["短長"].index(date)
                                    if Strategies_Result["MA"]["短長"][index+1] == "buy":
                                        show_msg(Stock_Code, "短期MA已向上突破長期MA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["MA"]["短長"][index+1] == "sell":
                                        show_msg(Stock_Code, "短期MA已向下突破長期MA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                            for date in Strategies_Result["MA"]["中長"]:
                                if Date == date:
                                    index = Strategies_Result["MA"]["中長"].index(date)
                                    if Strategies_Result["MA"]["中長"][index+1] == "buy":
                                        show_msg(Stock_Code, "中期MA已向上突破長期MA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["MA"]["中長"][index+1] == "sell":
                                        show_msg(Stock_Code, "中期MA已向下突破長期MA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                        elif i == 2:
                            for date in Strategies_Result["RSI"]["短中"]:
                                if Date == date:
                                    index = Strategies_Result["RSI"]["短中"].index(date)
                                    if Strategies_Result["RSI"]["短中"][index+1] == "buy":
                                        show_msg(Stock_Code, "短期RSI已向上突破中期RSI", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["RSI"]["短中"][index+1] == "sell":
                                        show_msg(Stock_Code, "短期RSI已向下突破中期RSI", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                            for date in Strategies_Result["RSI"]["短長"]:
                                if Date == date:
                                    index = Strategies_Result["RSI"]["短長"].index(date)
                                    if Strategies_Result["RSI"]["短長"][index+1] == "buy":
                                        show_msg(Stock_Code, "短期RSI已向上突破長期RSI", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["RSI"]["短長"][index+1] == "sell":
                                        show_msg(Stock_Code, "短期RSI已向下突破長期RSI", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                            for date in Strategies_Result["RSI"]["中長"]:
                                if Date == date:
                                    index = Strategies_Result["RSI"]["中長"].index(date)
                                    if Strategies_Result["RSI"]["中長"][index+1] == "buy":
                                        show_msg(Stock_Code, "中期RSI已向上突破長期RSI", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["RSI"]["中長"][index+1] == "sell":
                                        show_msg(Stock_Code, "中期RSI已向下突破長期RSI", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                        elif i == 3:
                            for date in Strategies_Result["KD"]:
                                if Date == date:
                                    index = Strategies_Result["KD"].index(date)
                                    if Strategies_Result["KD"][index+1] == "buy":
                                        show_msg(Stock_Code, "K已向上突破D", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["KD"][index+1] == "sell":
                                        show_msg(Stock_Code, "K已向下突破D", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                        elif i == 4:
                            for date in Strategies_Result["MACD"]:
                                if Date == date:
                                    index = Strategies_Result["MACD"].index(date)
                                    if Strategies_Result["MACD"][index+1] == "buy":
                                        show_msg(Stock_Code, "DIF已向上突破EMA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["MACD"][index+1] == "sell":
                                        show_msg(Stock_Code, "DIF已向下突破EMA", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                        elif i == 5:
                            for date in Strategies_Result["CMO"]:
                                if Date == date:
                                    index = Strategies_Result["CMO"].index(date)
                                    if Strategies_Result["CMO"][index+1] == "buy":
                                        show_msg(Stock_Code, "短期CMO已向上突破長期CMO", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["CMO"][index+1] == "sell":
                                        show_msg(Stock_Code, "短期CMO已向下突破長期CMO", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                        elif i == 6:
                            for date in Strategies_Result["WMSR"]:
                                if Date == date:
                                    index = Strategies_Result["WMSR"].index(date)
                                    if Strategies_Result["WMSR"][index+1] == "buy":
                                        show_msg(Stock_Code, "WMSR 小於 -80", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["WMSR"][index+1] == "sell":
                                        show_msg(Stock_Code, "WMSR 大於 -20", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                        elif i == 7:
                            for date in Strategies_Result["SAR"]:
                                if Date == date:
                                    index = Strategies_Result["SAR"].index(date)
                                    if Strategies_Result["SAR"][index+1] == "buy":
                                        show_msg(Stock_Code, "行情反轉穿破SAR值", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["SAR"][index+1] == "sell":
                                        show_msg(Stock_Code, "行情跌落觸及SAR值", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                        elif i == 8:
                            for date in Strategies_Result["CCI"]:
                                if Date == date:
                                    index = Strategies_Result["CCI"].index(date)
                                    if Strategies_Result["CCI"][index+1] == "buy":
                                        show_msg(Stock_Code, "CCI由下往上突破+100", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日買進")
                                    elif Strategies_Result["CCI"][index+1] == "sell":
                                        show_msg(Stock_Code, "CCI由上往下跌破-100", "發生日："+str(date-datetime.timedelta(1)), "建議於隔開市日賣出")
                                    time_pause = True
                                    last_update = pygame.time.get_ticks()
                    have_shown_msg = True
                if show_Unable_to_operate:
                    if pygame.time.get_ticks() - show_Unable_to_operate_time > 1000:
                        show_Unable_to_operate = False


                #畫面顯示
                game_display()
                if showing_trading_column:
                    input_box_trading_width = show_trading_column(Money, Stock_stored[Stock_Code], Trading_Direct, trading_input)
                if show_Unable_to_operate:
                    draw_text_centerx(screen,"Unable to operate", 24, RED, 510, 0, font_msjh)

    pygame.display.update()
pygame.QUIT