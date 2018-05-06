#!/usr/bin/python
#################################################
#
# PiConSrv
#
# ConQR GUI Front-End
#
# Version
# -----------------------------------------------
# 1.0	jdg	Initial Version (2018-04)
#
# Authors
# -----------------------------------------------
# jdg	Jim Gilsinn
#
#################################################

import sys, os, time, subprocess, numbers, logging
import pygame
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

#################################################

#------------------------------------------------
# Usage Message
#------------------------------------------------
usage = """
Usage:  con-srv.py

GUI Front-End for ConQR
"""

#------------------------------------------------
# Conference Information
#------------------------------------------------
con_image_file = "logo.png"
con_image_size = (250,100)
con_name = "BSidesDC 2018"
con_date = "October 26-28, 2018"
con_full_reg_file = "conference.txt"
con_current_reg_file = "registered.txt"
con_manual_reg_file = "manual.txt"
con_types_file = "types.txt"
con_type_attendees = ["ATTENDEE","ROOMBLOCK","CRYPTKIDS"]
con_type_speakers = ["SPEAKER"]
con_type_sponsors = ["SPONSOR"]

#------------------------------------------------
# Default Values
#------------------------------------------------
default_screen_size = (1024,768)
color_white = (255,255,255)
color_black = (0,0,0)
color_gray = (128,128,128)
color_light_gray = (192,192,192)
color_yellow = (255,255,0)
color_light_yellow = (255,255,128)
color_red = (255,0,0)
color_dark_red = (128,0,0)
color_green = (0,255,0)
color_dark_green = (0,128,0)
color_blue = (0,0,255)
color_dark_blue = (0,0,128)
color_light_blue = (128,128,255)
color_navy = (0,0,64)
con_name_offset = (350,20)
con_date_offset = (350,60)
header_rect = (0,0,1024,100)
main_rect = (0,100,1024,500)
font_family = "sans-serif"
title_size = 40
class_title_size = 28
log_family = "monospace"
log_title_size = 18
log_outer_rect = (0,550,1024,218)
log_inner_rect = (10,560,1004,200)
log_text_offset_left = 20
log_text_offset_start = 570
log_text_offset = (log_text_offset_left,log_text_offset_start)
log_text_rect = (20,570,994,188)
log_text_spacing = 20
log = []

text_left_offset = 20
numbers_left_offset = 220
numbers_botton = 400
numbers_right = 400
attendees_top_offset = 120
text_vertical_spacing = 60
attendees_text = "Attendees"
attendees_offset = (text_left_offset,attendees_top_offset)
attendees_number_offset = (numbers_left_offset,attendees_top_offset)
speakers_text = "Speakers"
speakers_top_offset = attendees_top_offset + text_vertical_spacing
speakers_offset = (text_left_offset,speakers_top_offset)
speakers_number_offset = (numbers_left_offset,speakers_top_offset)
sponsors_text = "Sponsors"
sponsors_top_offset = speakers_top_offset + text_vertical_spacing
sponsors_offset = (text_left_offset,sponsors_top_offset)
sponsors_number_offset = (numbers_left_offset,sponsors_top_offset)
onsite_text = "Onsite"
onsite_top_offset = sponsors_top_offset + text_vertical_spacing
onsite_offset = (text_left_offset, onsite_top_offset)
onsite_number_offset = (numbers_left_offset, onsite_top_offset)
total_text = "Total"
total_top_offset = onsite_top_offset + text_vertical_spacing + 10
total_offset = (text_left_offset, total_top_offset)
total_number_offset = (numbers_left_offset, total_top_offset)
total_line_top = onsite_top_offset + title_size + 10
total_rect = (text_left_offset,total_line_top,numbers_right,2)
numbers_rect = (numbers_left_offset,attendees_top_offset,numbers_right,numbers_botton)


#################################################

#------------------------------------------------
# Check for arguments
#------------------------------------------------
if len(sys.argv) != 1:
    print Usage
    exit()

#------------------------------------------------
# Main Program Loop
#------------------------------------------------
try:
    # Initialize Output Window
    pygame.init()
    pygame.font.init()

    # Load Images & Fonts
    con_image = pygame.image.load(con_image_file)
    title_font = pygame.font.SysFont(font_family,title_size,True)
    log_font = pygame.font.SysFont(log_family,log_title_size)

    # Create Main Display Window
    screen = pygame.display.set_mode(default_screen_size)
    pygame.display.set_caption('PiCon Server')
    pygame.display.flip()
    
    # Display Conference Header
    pygame.draw.rect(screen,color_white,header_rect)
    screen.blit(con_image,(0,0))
    label_con_name = title_font.render(con_name,1,color_dark_blue)
    label_con_date = title_font.render(con_date,1,color_dark_blue)
    screen.blit(label_con_name, con_name_offset)
    screen.blit(label_con_date, con_date_offset)
    
    # Display Main Screen
    pygame.draw.rect(screen,color_light_gray,main_rect)
    
    # Display the Counter Headers
    label_attendees_text = title_font.render(attendees_text,1,color_dark_blue)
    screen.blit(label_attendees_text, attendees_offset)
    label_speakers_text = title_font.render(speakers_text,1,color_dark_blue)
    screen.blit(label_speakers_text, speakers_offset)
    label_sponsors_text = title_font.render(sponsors_text,1,color_dark_blue)
    screen.blit(label_sponsors_text, sponsors_offset)
    label_onsite_text = title_font.render(onsite_text,1,color_dark_blue)
    screen.blit(label_onsite_text, onsite_offset)
    label_total_text = title_font.render(total_text,1,color_dark_blue)
    screen.blit(label_total_text, total_offset)
    
    # Display Log Window
    pygame.draw.rect(screen,color_navy,log_outer_rect)
    pygame.draw.rect(screen,color_yellow,log_inner_rect,2)
    for i in range(0,10):
        log.append(" ")
        
    # Read Full Conference Registration File
    with open(con_full_reg_file) as f:
        reg_content = f.readlines()
    reg_content = [x.strip() for x in reg_content]
    #print "Lines in Full Con Reg File = " + str(len(reg_content))
    
    # Read Conference Registration Types File
    with open(con_types_file) as f:
        reg_types = f.readlines()
    reg_types = [x.strip() for x in reg_types]
    reg_type = []
    for i in range(0,len(reg_types)):
        if not (reg_types[i].startswith('#')):
            reg_type.append(reg_types[i])
    #print "Conference Types = " + str(len(reg_type))
    
    # Determine the Badge and Chip Types
    reg_badge = []
    reg_chip = []
    for i in range(0,len(reg_type)):
        l = reg_type[i].split(',')
        if (l[0] == "Badge"):
            reg_badge.append(reg_type[i])
        elif (l[0] == "Chip"):
            reg_chip.append(reg_type[i])
    #print "Badge Types = " + str(len(reg_badge))
    #print "Chip Types = " + str(len(reg_chip))
    
    # Find the Maximum Number of Attendees, Speakers, and Sponsors
    attendees_max = 0
    speakers_max = 0
    sponsors_max = 0
    for i in range(0,len(reg_content)):
        l = reg_content[i].split(',')
        if (l[2] in con_type_attendees):
            adder = 0
            for i in range(0,len(reg_badge)):
                b = reg_badge[i].split(',')
                if (l[2] == b[1]):
                    adder = int(b[3])
            attendees_max += adder
        elif (l[2] in con_type_speakers):
            adder = 0
            for i in range(0,len(reg_badge)):
                b = reg_badge[i].split(',')
                if (l[2] == b[1]):
                    adder = int(b[3])
            speakers_max += adder
        elif (l[2] in con_type_sponsors):
            adder = 0
            for i in range(0,len(reg_badge)):
                b = reg_badge[i].split(',')
                if (l[2] == b[1]):
                    adder = int(b[3])
            sponsors_max += adder
    
    # Main Loop
    running = True
    cnt = 0
    while running:
        # Determine Current Values
        attendees_current = 0
        speakers_current = 0
        sponsors_current = 0
        onsite_current = 0
        total_current = attendees_current + speakers_current + sponsors_current + onsite_current
        total_max = attendees_max + speakers_max + sponsors_max + onsite_current
        
        # Print Current Values
        pygame.draw.rect(screen,color_light_gray,numbers_rect)
        label_attendees_number = title_font.render(str(attendees_current) + " / " + str(attendees_max),1,color_dark_red)
        screen.blit(label_attendees_number, attendees_number_offset)
        label_speakers_number = title_font.render(str(speakers_current) + " / " + str(speakers_max),1,color_dark_red)
        screen.blit(label_speakers_number, speakers_number_offset)
        label_sponsors_number = title_font.render(str(sponsors_current) + " / " + str(sponsors_max),1,color_dark_red)
        screen.blit(label_sponsors_number, sponsors_number_offset)
        label_onsite_number = title_font.render(str(onsite_current),1,color_dark_red)
        screen.blit(label_onsite_number, onsite_number_offset)
        label_total_number = title_font.render(str(total_current) + " / " + str(total_max),1,color_dark_red)
        screen.blit(label_total_number, total_number_offset)
        pygame.draw.rect(screen,color_dark_blue,total_rect)
        
        log.append(time.strftime("%m/%d/%y %H:%M:%S") + ": Server Log #" + str(cnt))
        pygame.draw.rect(screen,color_navy,log_text_rect)
        log_text_offset_top = log_text_offset_start
        for i in range(0,9):
            label_log_text = log_font.render(log[len(log)-i-1],1,color_light_yellow)
            screen.blit(label_log_text,(log_text_offset_left,log_text_offset_top))
            log_text_offset_top += log_text_spacing
        
        pygame.display.update()
        time.sleep(0.5)
        cnt += 1
        
        pygame.event.pump()
        event=pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False

except Exception, error:
    print "[!] Something went wrong, printing error: " + str(error)

finally:
    pygame.font.quit()
    pygame.quit()
    sys.exit()