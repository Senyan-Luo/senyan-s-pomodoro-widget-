import time
import datetime as dt
import tkinter as tk
from tkinter import messagebox, simpledialog
import pygame

pygame.init()
pygame.mixer.init()
break_sound = pygame.mixer.Sound("break.wav")
study_sound = pygame.mixer.Sound("study.wav")
long_break_sound = pygame.mixer.Sound("long_break.wav")
# REDO the end sound!
end_sound  = pygame.mixer.Sound("end.wav")

class Pomodoro():
    initial = 0
    ongoing = 1
    short_break = 2
    long_break = 3

    def __init__(self, reps):
        # get the number of pomodoros from user
        self.reps = reps
        self.goal_pomodoro = self.reps
        self.current_pomodoro = 0
        self.long_break_goal = 3
        # length of study time in each pomodoro
        self.pom_study_length = dt.timedelta(seconds=25)
        # length of break time in each pomodoro
        self.short_break_length = dt.timedelta(seconds=5)
        self.long_break_length = dt.timedelta(seconds=15)

        # initialize
        self.pom_status = self.initial

    def start_pom(self):
        # set start + end times
        self.pom_start = dt.datetime.now()
        self.pom_end = self.pom_start + self.pom_study_length
        self.pom_status = self.ongoing
        study_sound.play()
        print('\n********** Pomodoro # {} **********\n'.format(self.current_pomodoro + 1))

    def take_short_break(self):
        # set start & end times
        self.pom_start = dt.datetime.now()
        self.pom_end = self.pom_start + self.short_break_length
        self.pom_status = self.short_break
        break_sound.play()
        print('\n********** Taking a short break **********\n')
        # show messagebox


    def take_long_break(self):
        # set start & end times
        long_break_sound.play()
        self.pom_start = dt.datetime.now()
        self.pom_end = self.pom_start + self.long_break_length
        self.pom_status = self.long_break
        print('\n********** Taking a long break **********\n')

    def increase_pom(self):
        # increase task counter
        self.current_pomodoro += 1

    def check_finished(self):
        return self.current_pomodoro == self.goal_pomodoro

    def get_time_remaining(self):
        return self.pom_end - dt.datetime.now()

    def formatTime(self, tt):
        # find total seconds
        self.total_seconds = int(tt.total_seconds())
        # 3600 seconds in an hour
        hours, remainder = divmod(self.total_seconds, 3600)
        # 60 seconds in a minute
        minutes, seconds = divmod(remainder, 60)

        return ('{} minutes {} seconds remaining: '.format(minutes, seconds))

    def show_info(self):
        status = 'none'
        question = 'what'
        if self.pom_status == self.ongoing:
            status = 'Get work done'
        elif self.pom_status == self.short_break:
            status = 'Take a short break'
            question = 'Short break is up, are you ready to start the next Pomodoro?'
        elif self.pom_status == self.long_break:
            status = 'Take a long break'
            question = 'Long break is up, are you ready to start the next Pomodoro?'
        time_remaining = self.formatTime(self.get_time_remaining())
        print('{} | {}'.format(status, time_remaining))
        # after a short or long break, ask user when to proceed to the next pomorodo
        if self.total_seconds < 1 and (self.pom_status == self.short_break or self.pom_status == self.long_break):
            messagebox.showinfo("Back to work?", question) 


if __name__ == '__main__':
    # hide tk canvas
    # messagebox with button to begin pomodoro
    root = tk.Tk()
    root.withdraw()
    usr_ans = simpledialog.askinteger(
        "Input", "1 pomodoro = 25-min studying + 5-min break\nHow many pomodoros do you want to set?", minvalue=0, maxvalue=20)
    if usr_ans is not None:
        pomodoro = Pomodoro(usr_ans)
        pomodoro.start_pom()
    else:
        print("No problem, see you later!")
        pomodoro = Pomodoro(1)
        pomodoro.start_pom()

    while True:
        # Initialize last_update
        last_update = pomodoro.pom_start - dt.timedelta(seconds=15)

        # while running
        while pomodoro.get_time_remaining() > dt.timedelta(seconds=0):
            current_time = dt.datetime.now()

            # print every 2 seconds
            if (current_time - last_update) > dt.timedelta(seconds=2):
                pomodoro.show_info()
                # update track when the last update was printed
                last_update = current_time

        # complete the current pomo or start a new one. 
        if pomodoro.pom_status == Pomodoro.ongoing:

            # add number of pom
            pomodoro.increase_pom()
            # check to see if need to continue to a break or stop the pomodoro
            if pomodoro.check_finished():
                end_sound.play()
                time.sleep(4)
                # leave enough time to play the end sound
                break
            elif pomodoro.current_pomodoro % pomodoro.long_break_goal == 0:
                pomodoro.take_long_break()
            else:
                pomodoro.take_short_break()
        else:
            pomodoro.start_pom()

    # show how many pomodoro in total are completed
    print('You completed ' + str(pomodoro.current_pomodoro) +' Pomodoro!\nKeep up the good work!')
    messagebox.showinfo("Good job!", 'You completed ' + str(pomodoro.current_pomodoro) +' Pomodoros!\nKeep up the good work! :)') 
