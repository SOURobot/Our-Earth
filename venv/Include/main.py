import pygame
import requests

FULLSCREEN = False
STANDART_RESOLUTION = (600, 450)

if FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(STANDART_RESOLUTION)
running = True

spn = 0.1

spn_min = 0.001
spn_max = 16.0
spn_step = 2

latitude = 55.751244  # shirota, 2nd in request
longitude = 37.618423  # dolgota, 1st in request 180+ => *-1

base_move_step = 0.3
sp = ['sat', 'map', 'sat,skl']
id = 1
curr_sp = sp[id]


def crop_picture(long, lat, spn, curr_sp):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={long},{lat}&spn={spn},{spn}&l={curr_sp}"
    responce = requests.get(map_request)
    bytes = responce.content

    with open("map_file", "wb") as file:
        file.write(bytes)


while running:

    crop_picture(longitude, latitude, spn, curr_sp)
    screen.blit(pygame.image.load("map_file"), (0, 0))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_UP, pygame.K_w):
                if latitude >= 90:
                    if longitude < 0:
                        longitude = 180 + longitude
                    else:
                        longitude = -(180 - longitude)
                else:
                    latitude = min(80, latitude + round(base_move_step * spn, 6))

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if latitude <= -90:
                    if longitude < 0:
                        longitude = 180 + longitude
                    else:
                        longitude = -(180 - longitude)
                else:
                    latitude = max(-80, latitude - round(base_move_step * spn, 6))

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if longitude <= -179:
                    longitude = -round(longitude + base_move_step * spn, 6)
                else:
                    longitude = max(-179, longitude - round(base_move_step * spn, 6))

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if longitude >= 179:
                    longitude = -round(longitude + base_move_step * spn, 6)
                else:
                    longitude = min(179, longitude + round(base_move_step * spn, 6))

            elif event.key == pygame.K_PAGEUP:
                if spn > spn_min:
                    spn = round(spn / spn_step, 3)
            elif event.key == pygame.K_PAGEDOWN:
                if spn < spn_max:
                    spn = round(spn * spn_step, 3)

            elif event.key == pygame.K_SPACE:
                id = (id + 1) % 3
                curr_sp = sp[id]
pygame.quit()