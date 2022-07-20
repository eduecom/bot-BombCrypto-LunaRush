# -*- coding: utf-8 -*-    
from re import X
from turtle import position
from cv2 import cv2


from os import listdir
from src.logger import logger, loggerMapClicked
from random import randint
from random import random
import pygetwindow
import numpy as np
import mss
import pyautogui
import time
import sys

import yaml





cat = """


─────█─▄▀█──█▀▄─█──
────▐▌──────────▐▌──
────█▌▀▄──▄▄──▄▀▐█──
───▐██──▀▀──▀▀──██▌──
──▄████▄──▐▌──▄████▄─





>>---> Bot começou a rodar! Pode descansar em paz enquanto eu farmo pra vc! :3

>>---> Pressione ctrl + c para parar o bot.
"""

# Printa a apresentação/Abertura do programa
print(cat)
time.sleep(2)



# Acessa o arquivo config.yaml e importa algumas infos dele 
if __name__ == '__main__':
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

# Variável Modo 
ct = c['threshold']

# Variável Casa
ch = c['home']

# Verifica se dentro do config.yaml a casa está habilitada
if not ch['enable']:
    print('>>---> Você não tem uma casa! Vamos começar! :(  ')
# Pulando uma linha
print('\n')


# Declarando que Pause carrega os valores de tempo + intervalo entre os movimentos
pause = c['time_intervals']['interval_between_moviments']
# Declara pyautogui.PAUSE recebendo Pause
pyautogui.PAUSE = pause

# Váriaveis interruptores
pyautogui.FAILSAFE = False
hero_clicks = 0
luna_heroClicks = 0
hero_time = 2
login_attempts = 0
last_log_is_progress = False



def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images():
    file_names = listdir('./targets/')
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

images = load_images()

# Função para mandar os Heróis para a House 
def loadHeroesToSendHome():
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        heroes.append(cv2.imread(path))

    print('>>---> %d heróis que devem ser enviados para a House' % len(heroes))
    return heroes

# Se a House estiver habilitada no config.yaml então recebe a função acima
if ch['enable']:
    home_heroes = loadHeroesToSendHome()

# go_work_img = cv2.imread('targets/go-work.png')
# commom_img = cv2.imread('targets/commom-text.png')
# arrow_img = cv2.imread('targets/go-back-arrow.png')
# hero_img = cv2.imread('targets/hero-icon.png')
# x_button_img = cv2.imread('targets/x.png')
# teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
# ok_btn_img = cv2.imread('targets/ok.png')
# connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
# select_wallet_hover_img = cv2.imread('targets/select-wallet-1-hover.png')
# select_metamask_no_hover_img = cv2.imread('targets/select-wallet-1-no-hover.png')
# sign_btn_img = cv2.imread('targets/select-wallet-2.png')
# new_map_btn_img = cv2.imread('targets/new-map.png')
# green_bar = cv2.imread('targets/green-bar.png')
full_stamina = cv2.imread('targets/full-stamina.png')

robot = cv2.imread('targets/robot.png')
# puzzle_img = cv2.imread('targets/puzzle.png')
# piece = cv2.imread('targets/piece.png')
slider = cv2.imread('targets/slider.png')



def show(rectangles, img = None):

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)





def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass
        # print('waiting for "{}" button, timeout of {}s'.format(name, timeout))
    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass
                    # print('timed out')
                return False
            # print('button not found yet')
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        # mudar moveto pra w randomness
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True
        print("THIS SHOULD NOT PRINT")


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():

    commoms = positions(images['bomb_bar'], threshold = ct['commom'])
    if (len(commoms) == 0):
        return
    x,y,w,h = commoms[len(commoms)-1]
#
    moveToWithRandomness(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')

def luna_scroll():

    lv1 = positions(images['luna_lv1'], threshold = ct['commom'])
    if (len(lv1) == 0):
        return
    x,y,w,h = lv1[len(lv1)-1]
#
    moveToWithRandomness(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')

def clickButtons():
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)

def isHome(hero, buttons):
    y = hero[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = 130

    green_bars = positions(images['green-bar'], threshold=ct['green_bar'])
    logger('🟩 %d green bars detected' % len(green_bars))
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    logger('🆗 %d botões detectados' % len(buttons))


    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('🆗 %d botões com barra verde detectados' % len(not_working_green_bars))
        logger('👆 Clicando em %d heróis' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        if hero_clicks > 20:
            logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)
    

def clickFullBarButtons():
    offset = 120
    full_bars = positions(images['bomb_full-stamina'], threshold=ct['default'])
    logger('🟩 %d Hero para trampa' % len(full_bars))
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    logger('🟩 %d botoes pingando' % len(buttons))


    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)
            logger('numero: %d' % len(not_working_full_bars))
        else:
            print("não deu boa mano")

    if len(not_working_full_bars) > 0:
        logger('👆 Clicando em %d heróis' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)

#O escravo (complemento, dependente que somente retorna o n)
#somente retorna o numero e clica
def luna_clickHeroBtn(): 
    logger("chamou Select_Heroes")

    luna_Reconnect()
    luna_stamina_heroes = positions(images['luna_stamina'], threshold=ct['default']) 
    luna_btnSelect = positions(images['luna_btnSelect'], threshold=ct['default'])

    luna_numHeros = positions(images['luna_btnSelect'], threshold=ct['default'])

    luna_notEnergy = positions(images['luna_btnSemStamina'], threshold= ct['default'])
    
    not_working_luna_bars = []
    for bar in luna_stamina_heroes : 
        if not isWorking(bar, luna_stamina_heroes) and len(not_working_luna_bars) < 3:
            not_working_luna_bars.append(bar)

    # logger(f'bota select: {len(luna_numHeros)}')
    
    
    logger(f'PRINT AQUI{len(luna_numHeros)}')
    logger(f'PRINT AQUI{len(luna_btnSelect)}')
    logger(f'PRINT AQUI{len(luna_numHeros)}')
        

    btn_select_heroes = []
    for select in luna_btnSelect:
        if len(luna_btnSelect) > 1:
            btn_select_heroes.append(select)


    for (x1, y1, w1, h1) in btn_select_heroes:
        moveToWithRandomness(x1+(w1/2),y1+(h1/2),1)
        pyautogui.click()

    logger(f'ESTOU RETIRANDO {len(btn_select_heroes)} HEROES QUE ESTÃO SELECIONADOS')

    if len(not_working_luna_bars) > 0:
        logger('👆 Clicando em %d heróinas' % len(not_working_luna_bars))
    

    for (x, y, w, h) in not_working_luna_bars: 
        # isWorking(y, buttons)
        moveToWithRandomness(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global luna_heroClicks
        luna_heroClicks = luna_heroClicks + 1

        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)

    return len(not_working_luna_bars)
       





# Mandar os heróis para trabalhar
def goToHeroes():
    # Clicando no ícone do menu principal
    if clickBtn(images['go-back-arrow']):
        # Resetando o login
        global login_attempts
        login_attempts = 0

    #solveCaptcha(pause)
    #todo tirar o sleep quando colocar o pulling
    time.sleep(1)
    clickBtn(images['hero-icon'])
    time.sleep(1)
    #solveCaptcha(pause)

def goToGame():
    # em caso de pop-up de sobrecarga do servidor
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    clickBtn(images['treasure-hunt-icon'])

# Resetando posição dos heróis
def refreshHeroesPositions():

    logger('🔃 Fazendo o rodízio dos Heróis')
    clickBtn(images['go-back-arrow'])
    clickBtn(images['treasure-hunt-icon'])

    # time.sleep(3)
    clickBtn(images['treasure-hunt-icon'])

# Reconectando sua conta
def login():
    global login_attempts
    logger('😿 Estou verificando se seu jogo está desconectado')

    if pygetwindow.getWindowsWithTitle('MetaMask Notification'):
        windowMeta = pygetwindow.getWindowsWithTitle('MetaMask Notification')[0]
        windowMeta.activate()
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'f4')
        login_attempts = 0
        print("Fechei a MetaMask bugada")

    if clickBtn(images['ok'], name='okBtn', timeout=5):
        time.sleep(15)
        print('Botão OK clicado')
        pass

    if login_attempts > 3:
        logger('🔃 Muitas tentativas de login, recomeçando')
        login_attempts = 0
        pyautogui.hotkey('ctrl','shift','r')
        return

    if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        logger('🎉 Achei o botão connect, estou logando!')
        #solveCaptcha(pause)
        login_attempts = login_attempts + 1
        
        time.sleep(5)
        # mto ele da erro e poco o botao n abre
        # time.sleep(10)

    if clickBtn(images['select-wallet-2'], name='sign button', timeout=10):
        # às vezes, o pop-up do sinal aparece imediatamente
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout = 15):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        return
        # click ok button      

    if not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = ct['select_wallet_buttons'] ):
            pass
            # o ideal era que ele alternasse entre checar cada um dos 2 por um tempo 
            # print('sleep in case there is no metamask text removed')
            # time.sleep(20)
    else:
        pass
        # print('sleep in case there is no metamask text removed')
        # time.sleep(20)

    if clickBtn(images['select-wallet-2'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
        # print('sign button clicked')
        # print('{} login attempt'.format(login_attempts))
        # time.sleep(25)
        if clickBtn(images['treasure-hunt-icon'], name='teasureHunt', timeout=25):
            # print('sucessfully login, treasure hunt btn clicked')
            login_attempts = 0
        # time.sleep(15)

    if clickBtn(images['ok'], name='okBtn', timeout=5):
        pass
        # time.sleep(15)
        # print('ok button clicked')



def sendHeroesHome():
    if not ch['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch['hero_threshold'])
        if not len (hero_positions) == 0:
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(images['send-home'], threshold=ch['home_button_threshold'])
    # todo pass it as an argument for both this and the other function that uses it
    go_work_buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position,go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if(not isWorking(position, go_work_buttons)):
                print ('hero not working, sending him home')
                moveToWithRandomness(go_home_buttons[0][0]+go_home_buttons[0][2]/2,position[1]+position[3]/2,1)
                pyautogui.click()
            else:
                print ('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')


def refreshHeroes():
    logger('🏢 Procurando heróis para trabalhar')

    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger('⚒️ Enviando heróis com stamina completa para o trabalho', 'green')
    elif c['select_heroes_mode'] == "green":
        logger('⚒️ Enviando heróis com stamina verde para o trabalho', 'green')
    else:
        logger('⚒️ Enviando todos os heróis para o trabalho', 'green')

    buttonsClicked = 1
    empty_scrolls_attempts = c['scroll_attemps']

    while(empty_scrolls_attempts >0):
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        sendHeroesHome()

        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    logger('💪 {} heróis enviados para o trabalho'.format(hero_clicks))
    goToGame()

#O primeiro que chama
def luna_refreshHeroes():
    
    logger('🏢 Procurando heróis para trabalhar')

    luna_Reconnect()


    luna_buttonsClicked = 1
    # luna_empty_scrolls = c['luna_scroll_attemps']
    luna_empty_scrolls = 2

    while(luna_empty_scrolls > 0):
        luna_buttonsClicked = luna_clickHeroBtn()

        if luna_buttonsClicked == 0:
            luna_empty_scrolls = luna_empty_scrolls - 1 
        elif luna_buttonsClicked > 0 or luna_buttonsClicked < 3:
            break
        
        luna_scroll()
        time.sleep(2)

    logger('💪 {} heroinas enviados para o trabalho'.format(luna_heroClicks))
    luna_startTurn()
    
#condição da orquestra    
def luna_SendHeroesWork():

    luna_Reconnect()

    luna_SinalMaisHeroes = positions(images['luna_SinalMaisHeroes'], threshold=ct['default'])

    luna_not_energy = positions(images['luna_notStamina'], threshold=ct['default'])

    luna_not_working_heroes = []

    luna_have_energy_set = []

    for Sinal in luna_SinalMaisHeroes:
        if not isWorking(Sinal, luna_SinalMaisHeroes):
            luna_not_working_heroes.append(Sinal)

    for Heroi in luna_not_energy:
        if not isWorking(Heroi, luna_not_energy):
            luna_have_energy_set.append(Heroi)

    if len(luna_not_working_heroes) == 3:
        logger(f'Espaços livres:{len(luna_not_working_heroes)}')
        luna_refreshHeroes()
        return
    elif len(luna_have_energy_set) > 1:
        logger(f'Sem energia:{len(luna_have_energy_set)}')
        luna_ClearHeroes()
        return
    else:
        logger(f'Sem energia:{len(luna_have_energy_set)} Espaços livres:{len(luna_not_working_heroes)}')
        luna_startTurn()
        return

def luna_GoToHeroes():
    logger('Entrando no menu de heroes')

def luna_startTurn():
    if clickBtn(images['luna_startBoss']):
        logger('Botão caçar chefe clicado')
        luna_methVerificar()
        pass

def luna_methVerificar():
    
    time.sleep(2)
    if clickBtn(images['luna_x']):
        logger('Escolheu botão X')
        luna_ClearHeroes()
        return False
    elif clickBtn(images['luna_btnVS']):
        logger('Escolheu botão VS')
        luna_afterTurn()
        return True
    pass


# Logar no LunaRush e deixar na tela de seleção de heroes
def luna_Reconnect():
    print("Chamou luna_Reconnect")

    if clickBtn(images['luna_ok']):
        time.sleep(3)
    elif clickBtn(images['luna_bntChefe']):
        time.sleep(3)

    if luna_selectBoss() == 0:
        
        pass
    time.sleep(2)

def luna_ClearHeroes():
    logger('Retirando todos as heroinas sem energia das posições')
    luna_SinalMaisHeroes = positions(images['luna_SinalMaisHeroes'], threshold=ct['default'])
    luna_not_energy = positions(images['luna_notStamina'], threshold=ct['default'])
    luna_not_working_heroes = []

    if len(luna_not_energy) == 0:
        logger('Função ClearHeroes Cancelada! Motivo: Todos com energias para lutar.')
        return

    for Sinal in luna_SinalMaisHeroes:
        if not isWorking(Sinal, luna_not_energy):
            luna_not_working_heroes.append(Sinal)
    
    if len(luna_not_working_heroes) < 3:
        # logger('ACHEI 3 ARROMBADO MANCANDO AQUI MANO')
        logger(f'luna notheros work: {len(luna_not_energy)}')
        for (x, y, w, h) in luna_not_energy:
            moveToWithRandomness(x+(65)+(w/2),y+(h/2),1)
            time.sleep(2)
            pyautogui.click()
            logger('Ciclou no looping')
    
    if len(luna_SinalMaisHeroes) > 0:
        luna_startTurn()
    luna_refreshHeroes()
    
    

def luna_selectBoss():

    luna_selectBoss = positions(images['luna_selectBoss'], threshold=ct['default'])
    luna_btnWarrior = positions(images['luna_warrior'], threshold=ct['default'])

    luna_bossForWork = []
    for boss in luna_selectBoss:
        if len(luna_selectBoss) == 1:
            clickBtn(images['luna_selectBoss'])
        elif len(luna_selectBoss) > 1:
            luna_bossForWork.append(boss)


    for (x, y, w, h) in luna_bossForWork:
        moveToWithRandomness(x+(65)+(w/2),y+(h/2),1)
        time.sleep(2)
        pyautogui.click()
        if clickBtn(images['luna_warrior']):
            return 0
        logger('Ciclou no looping')

        
    
    # for (x, w, y, h) in luna_bossForWork:
    #     moveToWithRandomness(x+(w/2),y+(h/2),1)
    #     time.sleep(2)
    #     pyautogui.click()
    #     time.sleep(3)
        
    return (len(luna_bossForWork))


def luna_afterTurn():
    logger('Esperando a sua luta acabar...')
    time.sleep(50)

    luna_vitoria = positions(images['luna_vitoria'], threshold=ct['default']) 

    luna_derrota = positions(images['luna_derrota'], threshold=ct['default'])
    logger(f'Luna vitoria: {len(luna_vitoria)} Luna derrota: {len(luna_derrota)}')

    if len(luna_vitoria) > 0:
        clickBtn(images['luna_openBau'])
        time.sleep(3)
        clickBtn(images['luna_vitoria'])
        time.sleep(2)
        luna_startTurn()
        return
    elif len(luna_derrota) > 0:
        time.sleep(2)
        clickBtn(images['luna_derrota'])
        luna_startTurn()
        return
    



def main():
    time.sleep(5)
    t = c['time_intervals']
    

    windows = []
    lunaWindows = []

    for l in pygetwindow.getWindowsWithTitle('Luna Rush'): 
        lunaWindows.append({
            "lunaConnect": 0,
            "lunaWindow": l,
            "lunaHeros": 0,
            "lunaMetClear": 0,
        })
    for w in pygetwindow.getWindowsWithTitle('bombcrypto'):
        windows.append({
            "window": w,
            "login" : 0,
            "heroes" : 0,
            # "new_map" : 0,
            # "check_for_captcha" : 0,
            "refresh_heroes" : 0
            })

  


    while True:
        now = time.time()

        # print('Windows with "Luna Rush" text title found: ', len(gameScreens))[0]


        for last2 in lunaWindows:
            last2["lunaWindow"].activate()
            time.sleep(2)

            # if now - last2["lunaConnect"] > addRandomness(t['luna_Reconnect_time'] * 60):
            #     last2["lunaConnect"] = now
            #     luna_Reconnect()
                    

            # if now - last2["lunaHeros"] > addRandomness(t['luna_send_heroes'] * 60):
            #     print("pingo o tempo luna_send_heroes")
            #     last2 ["lunaHeros"] = now
            #     luna_SendHeroesWork()
        
            #     ###### TESTE ######
            
            if now - last2["lunaMetClear"] > addRandomness(t['luna_methodo_clear'] * 60):
                last2['lunaMetClear'] = now
                luna_SendHeroesWork()
                # luna_afterTurn()
                pass
            
            
            # if now - last2["lunaHeros"] > addRandomness(t['luna_send_heroes'] * 60):
            #     print("teste")
            #     last2 ["lunaHeros"] = now
            #     luna_SendHeroesWork()




        for last in windows:
            last["window"].activate()
            time.sleep(2)

            # if now - last["check_for_captcha"] > addRandomness(t['check_for_captcha'] * 60):
            #     last["check_for_captcha"] = now
            #     #solveCaptcha(pause)

            if now - last["login"] > addRandomness(t['check_for_login'] * 60):
                sys.stdout.flush()
                last["login"] = now
                login()
                # refreshHeroes()

            if now - last["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
                last["heroes"] = now
                refreshHeroes()

            # if now - last["new_map"] > t['check_for_new_map_button']:
            #     last["new_map"] = now

                if clickBtn(images['new-map']):
                    loggerMapClicked()


            if now - last["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
                #solveCaptcha(pause)
                last["refresh_heroes"] = now
                refreshHeroesPositions()

            #clickBtn(teasureHunt)
            logger(None, progress_indicator=True)

            sys.stdout.flush()

            time.sleep(1)
            
main()


#cv2.imshow('img',sct_img)
#cv2.waitKey()
