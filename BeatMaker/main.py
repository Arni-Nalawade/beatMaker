import pygame, sys
from pygame import mixer
pygame.init() # Setup Pygame

black:tuple = (0, 0, 0)
white:tuple = (255, 255, 255)
# gray:tuple = (128, 128, 128)
gray = (198, 198, 198)
dark_gray:tuple = (50, 50, 50)
light_gray:tuple = (170, 170, 170)
charcoal: tuple = (54, 69, 79)
blue:tuple = (0, 255, 255)
red:tuple = (255, 0, 0)
mauve:tuple = (224, 176, 255)
gold:tuple = (212, 175, 55)
light_blue:tuple = (164,219,232)
WIDTH:int = 1400
HEIGHT:int = 800
active_length:int = 0
active_beat:int = 0


screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Create a screen with Static Width and Height
pygame.display.set_caption('Beat Maker') # Set the title of the window
try:
    pygame.display.set_icon(pygame.image.load('./Images/GameIcon.png'))
except FileNotFoundError:
    print("\033[93m Icon file not found. Continuing Execution without it \033[0m")

beat_changed: bool = True # Boolean to check if the beat has changed
timer = pygame.time.Clock() # Create a timer to keep track of time
fps:int = 10 # Set the FPS of the game
beats:int = 8 # Set the number of beats in a loop
bpm:int = 240 # Set the beats per minute
instruments:int = 6 # Set the number of instruments
playing:bool = True # Boolean to check if the game is playing
clicked:list = [[-1 for _ in range(beats)] for _ in range(instruments)] # List to keep track of which beats are clicked
active_list:list = [1 for _ in range(instruments)] # List to keep track of which instruments are active
pygame.mixer.set_num_channels(instruments * 3) # Set the number of channels to the number of instruments
save_menu:bool = False # Boolean to check if the save menu is open
load_menu:bool = False # Boolean to check if the load menu is open
saved_beats:list = [] # List to keep track of all saved beats
beat_name:str = '' # String to keep track of the name of the beat being saved
typing:bool = False # Boolean to check if the user is typing the name of the beat
index:int = 100 # Integer to keep track of which beat is selected in the load menu

# load ALL sounds                                              [Error Correction Handled]
try:
    hi_hat = mixer.Sound('./Sounds/Guitar.wav')
    snare = mixer.Sound('./Sounds/snare.wav')
    kick = mixer.Sound('./Sounds/Drum.wav')
    crash = mixer.Sound('./Sounds/crash.wav')
    clap = mixer.Sound('./Sounds/clap.wav')
    tom = mixer.Sound("./Sounds/tribal_drum.wav")
except FileNotFoundError:
    print("\033[91m Sound files not found. Please download the sound files from the github repository and place them in the `Sounds` folder \033[0m")
    sys.exit(0)

# load ALL fonts                                               [Error Correction Handled]
try:
    label_font = pygame.font.Font('./Fonts/Roboto-Bold.ttf', 32)
    medium_font = pygame.font.Font('./Fonts/Roboto-Bold.ttf', 24)
except FileNotFoundError:
    print("\033[91m Font files not found. Please download the font files from the github repository and place them in the `Fonts` folder \033[0m")
    sys.exit(0)

# load ALL saved beats                                         [Error Correction Handled]
try:
    with open('SavedBeats.txt', 'r') as file:
        for line in file:
            saved_beats.append(line)
except FileNotFoundError:
    with open("SavedBeats.txt", "w") as file:pass


def draw_grid(clicks, beat, actives):
    boxes = []
    left_box = pygame.draw.rect(screen, dark_gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, dark_gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    for i in range(instruments + 1):
        pygame.draw.line(screen, gray, (0, i * 100), (200, i * 100), 3)
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Guitar', True, light_blue)
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, light_blue)
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render('Bass Drum', True, light_blue)
    screen.blit(kick_text, (17, 230))
    crash_text = label_font.render('Crash', True, light_blue)
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, light_blue)
    screen.blit(clap_text, (35, 430))
    tom_text = label_font.render('Tribal Drum', True, light_blue)
    screen.blit(tom_text, (15, 530))
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = charcoal
            else:
                if actives[j] == 1:
                    color = mauve
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                     90], 0, 3)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, j * 100, ((WIDTH - 200) // beats), 100],
                             5, 5)
            pygame.draw.rect(screen, black,
                             [i * ((WIDTH - 200) // beats) + 200, j * 100, ((WIDTH - 200) // beats), 100],
                             2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue,
                                [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100],
                                5, 3)

    return boxes


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('SAVE MENU: Enter a Name for this beat', True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, black)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    saving_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 100, HEIGHT * 0.75, 200, 100], 0, 5)
    saving_text = label_font.render('Save Beat', True, black)
    screen.blit(saving_text, (WIDTH // 2 - 70, HEIGHT * 0.75 + 30))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, beat_name, entry_rect


def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('Saved Beats', True, white)
    screen.blit(menu_text, (600, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, charcoal)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    loading_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 100, HEIGHT * 0.87, 200, 100], 0, 5)
    loading_text = label_font.render('Load Beat', True, charcoal)
    screen.blit(loading_text, (WIDTH // 2 - 70, HEIGHT * 0.87 + 30))
    delete_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 400, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete Beat', True, charcoal)
    screen.blit(delete_text, (WIDTH // 2 - 385, HEIGHT * 0.87 + 30))
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, light_gray, [190, 100 + index*50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beats_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 8:beats_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat][beats_index_end + 6:bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect = pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)
    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)
    # drawing lower menu
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    if playing:
        play_text = label_font.render('Pause', True, black)
    else:
        play_text = label_font.render('Play', True, black)
    screen.blit(play_text, (90, HEIGHT - 120))
    # beats per minute buttons
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, black)
    screen.blit(add_text, (520, HEIGHT - 140))
    sub_text = medium_font.render('-5', True, black)
    screen.blit(sub_text, (520, HEIGHT - 90))
    # beats per loop buttons
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (612, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (670, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, black)
    screen.blit(add_text2, (820, HEIGHT - 140))
    sub_text2 = medium_font.render('-1', True, black)
    screen.blit(sub_text2, (820, HEIGHT - 90))
    # clear board button
    clear = pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Clear Board', True, black)
    play_text_x = 1150 + (200 - play_text.get_width()) / 2  # calculate the x coordinate to center the text
    screen.blit(play_text, (play_text_x, HEIGHT - 120))  # use the calculated x coordinate
    # save and load buttons
    save_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render('Save Beat', True, black)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 98, 200, 48], 0, 5)
    load_text = label_font.render('Load Beat', True, black)
    screen.blit(load_text, (920, HEIGHT - 90))
    # instrument rectangles
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    if beat_changed:
        play_notes()
        beat_changed = False
    if save_menu:
        exit_button, saving_button, beat_name, entry_rect = draw_save_menu(beat_name, typing)
    elif load_menu:
        exit_button, loading_button, entry_rect, delete_button, loaded_information = draw_load_menu(index)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos) and playing:
                playing = False
            elif play_pause.collidepoint(event.pos) and not playing:
                playing = True
                active_beat = 0
                active_length = 0
            if beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                if beats > 1:
                    beats -= 1
                    for i in range(len(clicked)):
                        clicked[i].pop(-1)
            if bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                if bpm > 5:
                    bpm -= 5
            if clear.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
            if save_button.collidepoint(event.pos):
                save_menu = True
            if load_button.collidepoint(event.pos):
                load_menu = True
                playing = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                typing = False
                beat_name = ''
            if entry_rect.collidepoint(event.pos):
                if save_menu:
                    if typing:
                        typing = False
                    else:
                        typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50
            if save_menu:
                if saving_button.collidepoint(event.pos):
                    file = open('SavedBeats.txt', 'w')
                    saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ''
            if load_menu:
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats = loaded_information[0]
                        bpm = loaded_information[1]
                        clicked = loaded_information[2]
                        index = 100
                        save_menu = False
                        load_menu = False
                        playing = True
                        typing = False
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0:
                beat_name = beat_name[:-1]

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

file = open('SavedBeats.txt', 'w')
for i in range(len(saved_beats)):
    file.write(str(saved_beats[i]))
file.close()
pygame.quit()