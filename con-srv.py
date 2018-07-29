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
con_onsite_reg_file = "onsite.txt"
con_types_file = "types.txt"
con_type_attendees = ["ATTENDEE","ROOMBLOCK"]
con_type_kids = ["CRYPTKIDS"]
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
title_size = 32
class_title_size = 20
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
text_vertical_spacing = 48
attendees_text = "Attendees"
attendees_offset = (text_left_offset,attendees_top_offset)
attendees_number_offset = (numbers_left_offset,attendees_top_offset)
kids_text = "CryptKids"
kids_top_offset = attendees_top_offset + text_vertical_spacing
kids_offset = (text_left_offset,kids_top_offset)
kids_number_offset = (numbers_left_offset,kids_top_offset)
speakers_text = "Speakers"
speakers_top_offset = kids_top_offset + text_vertical_spacing
speakers_offset = (text_left_offset,speakers_top_offset)
speakers_number_offset = (numbers_left_offset,speakers_top_offset)
sponsors_text = "Sponsors"
sponsors_top_offset = speakers_top_offset + text_vertical_spacing
sponsors_offset = (text_left_offset,sponsors_top_offset)
sponsors_number_offset = (numbers_left_offset,sponsors_top_offset)
manual_text = "Manual"
manual_top_offset = sponsors_top_offset + text_vertical_spacing
manual_offset = (text_left_offset, manual_top_offset)
manual_number_offset = (numbers_left_offset, manual_top_offset)
onsite_text = "Onsite"
onsite_top_offset = manual_top_offset + text_vertical_spacing
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
# Add a Log Message
#------------------------------------------------
def log_msg(msg):
    log.append(time.strftime("%m/%d/%y %H:%M:%S") + ": " + msg)

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
    label_kids_text = title_font.render(kids_text,1,color_dark_blue)
    screen.blit(label_kids_text, kids_offset)
    label_speakers_text = title_font.render(speakers_text,1,color_dark_blue)
    screen.blit(label_speakers_text, speakers_offset)
    label_sponsors_text = title_font.render(sponsors_text,1,color_dark_blue)
    screen.blit(label_sponsors_text, sponsors_offset)
    label_manual_text = title_font.render(manual_text,1,color_dark_blue)
    screen.blit(label_manual_text, manual_offset)
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
    log_msg("Read Full Conference Registration File")
    
    # Read Conference Registration Types File
    with open(con_types_file) as f:
        reg_types = f.readlines()
    reg_types = [x.strip() for x in reg_types]
    reg_type = []
    for i in range(0,len(reg_types)):
        if not (reg_types[i].startswith('#')):
            reg_type.append(reg_types[i])
    log_msg("Read Conference Registration Types File")
    
    # Determine the Badge and Chip Types
    reg_badge = []
    reg_chip = []
    for i in range(0,len(reg_type)):
        l = reg_type[i].split(',')
        if (l[0] == "Badge"):
            reg_badge.append(reg_type[i])
        elif (l[0] == "Chip"):
            reg_chip.append(reg_type[i])
    
    # Determine Different Adders for Attendees, Speakers, and Sponsors
    attendee_adder = 1
    kids_adder = 1
    speaker_adder = 1
    sponsor_adder = 4
    for i in range(0,len(reg_badge)):
        l = reg_badge[i].split(',')
        if (l[1] in con_type_attendees):
            attendee_adder = int(l[3])
        elif (l[1] in con_type_kids):
            kids_adder = int(l[3])
        elif (l[1] in con_type_speakers):
            speaker_adder = int(l[3])
        elif (l[1] in con_type_sponsors):
            sponsor_adder = int(l[3])            
    
    # Find the Maximum Number of Attendees, Speakers, and Sponsors
    attendees_max = 0
    kids_max = 0
    speakers_max = 0
    sponsors_max = 0
    reg_code = []
    for i in range(0,len(reg_content)):
        l = reg_content[i].split(',')
        reg_code.append(l[0])
        if (l[2] in con_type_attendees):
            attendees_max += attendee_adder
        elif (l[2] in con_type_kids):
            kids_max += kids_adder
        elif (l[2] in con_type_speakers):
            speakers_max += speaker_adder
        elif (l[2] in con_type_sponsors):
            sponsors_max += sponsor_adder
    
    # Main Loop
    running = True
    cnt = 0
    attendees_current = 0
    kids_current = 0
    speakers_current = 0
    sponsors_current = 0
    reg_time = 0.0
    manual_current = 0
    manual_time = 0.0
    onsite_current = 0
    onsite_time = 0.0
    while running:
        # Determine Current Registrations
        reg_current_time = os.path.getmtime(con_current_reg_file)
        if (reg_current_time > reg_time):
            # Read Current Registration File
            with open(con_current_reg_file) as f:
                reg_current = f.readlines()
            reg_current = [x.strip() for x in reg_current]
            for i in range(0,len(reg_current)):
                reg_index = reg_code.index(reg_current[i])
                l = reg_content[reg_index].split(',')
                if (l[2] in con_type_attendees):
                    attendees_current += attendee_adder
                elif (l[2] in con_type_kids):
                    kids_current += kids_adder
                elif (l[2] in con_type_speakers):
                    speakers_current += speaker_adder
                elif (l[2] in con_type_sponsors):
                    sponsors_current += sponsor_adder
            reg_time = reg_current_time
        
        # Determine Manual Registrations
        manual_current_time = os.path.getmtime(con_manual_reg_file)
        if (manual_current_time > manual_time):
            # Read Manual Registration File
            with open(con_manual_reg_file) as f:
                reg_manual = f.readlines()
            reg_manual = [x.strip() for x in reg_manual]
            manual_current = len(reg_manual)
            # TODO: Validate the manual registrations against the existing registration file
            manual_time = manual_current_time
            log_msg("Manual Registration File Changed")
        
        # Determine Onsite Registrations
        onsite_current_time = os.path.getmtime(con_onsite_reg_file)
        if (onsite_current_time > onsite_time):
            # Read Onsite Registration File
            with open(con_onsite_reg_file) as f:
                reg_onsite = f.readlines()
            reg_onsite = [x.strip() for x in reg_onsite]
            # Only look at the last line in the file for the number of onsite registrations
            onsite_current = int(reg_onsite[len(reg_onsite)-1])
            log_msg("Onsite Registration File Changed")
            onsite_time = onsite_current_time
        
        # Update Total Values
        total_current = attendees_current + kids_current + speakers_current + sponsors_current + manual_current + onsite_current
        total_max = attendees_max + kids_max + speakers_max + sponsors_max + onsite_current
        
        # Print Current Values
        pygame.draw.rect(screen,color_light_gray,numbers_rect)
        label_attendees_number = title_font.render(str(attendees_current) + " / " + str(attendees_max),1,color_dark_red)
        screen.blit(label_attendees_number, attendees_number_offset)
        label_kids_number = title_font.render(str(kids_current) + " / " + str(kids_max),1,color_dark_red)
        screen.blit(label_kids_number, kids_number_offset)
        label_speakers_number = title_font.render(str(speakers_current) + " / " + str(speakers_max),1,color_dark_red)
        screen.blit(label_speakers_number, speakers_number_offset)
        label_sponsors_number = title_font.render(str(sponsors_current) + " / " + str(sponsors_max),1,color_dark_red)
        screen.blit(label_sponsors_number, sponsors_number_offset)
        label_manual_number = title_font.render(str(manual_current),1,color_dark_red)
        screen.blit(label_manual_number, manual_number_offset)
        label_onsite_number = title_font.render(str(onsite_current),1,color_dark_red)
        screen.blit(label_onsite_number, onsite_number_offset)
        label_total_number = title_font.render(str(total_current) + " / " + str(total_max),1,color_dark_red)
        screen.blit(label_total_number, total_number_offset)
        pygame.draw.rect(screen,color_dark_blue,total_rect)
        
        #log_msg("Server Log #" + str(cnt))
        pygame.draw.rect(screen,color_navy,log_text_rect)
        log_text_offset_top = log_text_offset_start
        for i in range(0,9):
            label_log_text = log_font.render(log[len(log)-i-1],1,color_light_yellow)
            screen.blit(label_log_text,(log_text_offset_left,log_text_offset_top))
            log_text_offset_top += log_text_spacing
        
        pygame.display.update()
        time.sleep(0.1)
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
