#! /usr/bin/env python3.5

import mlbgame
from tkinter import *
import datetime

"""
A game id is yyyy_mm_dd_away(lc)mlb_home(lc)mlb_gamenum
Examples
2019_06_08_oakmlb_texmlb_1
2019_06_08_oakmlb_texmlb_2
"""
class MLBapp:
    def __init__(self,parent):
        #Init data grab
        self.teams = mlbgame.teams()
        self.standings = mlbgame.standings()
        #Init vars
        self.teamselect = StringVar(window)
        self.gamedate = StringVar(window)
        #Init navigation
        self.navigation()
        self.show_calendar()

    def navigation(self):
        self.btn_stats = Button(window,text="Standings")
        self.btn_stats.grid(column=0,row=0)
        self.btn_stats.bind("<Button-1>",self.team_standings)
        self.btn_team = Button(window,text="Games")
        self.btn_team.grid(column=2,row=0)
        self.btn_team.bind("<Button-1>",self.team_games)
        self.team_dropdown()

    def team_dropdown(self):
        self.team_select = {}
        self.teamselect.set("Choose a team")
        for team in self.teams:
            #print(dir(team))
            self.team_select[team.club_full_name] = team

        self.team_dropdown = OptionMenu(window,self.teamselect,*self.team_select)
        self.team_dropdown.grid(column=1,row=0,padx=3,sticky=W)
        #self.team_dropdown.bind("<Button-1>",self.team_games)
        self.teamselect.trace('w', self.change_dropdown)

    def change_dropdown(self,*args):
        print(self.team_select[self.teamselect.get()].team_code)

    def team_standings(self,event):
        for index,division in enumerate(self.standings.divisions):
            #print(dir(division))
            self.lbl = Label(window, text=division.name, font=("Arial",14))
            self.lbl.grid(column=index, row=1, pady=1)

            for tdx,team in enumerate(division.teams):
                #print(dir(team))
                isfirst = "Roboto" if (team.gb == "-") else "Arial"
                self.teamstg = Label(window,text=team.team_full+" "+str(team.gb),font=(isfirst,10))
                self.teamstg.grid(column=index,row=2+tdx, sticky=W, padx=2)

    def team_games(self,event):
        today = datetime.date.today()
        tyear = today.year
        tmonth = today.month
        tday = today.day
        print("Games for %s on %s %s, %s" % (self.team_select[self.teamselect.get()].club_common_name, tmonth, tday, tyear))
        month = mlbgame.games(tyear, tmonth, tday, home=self.team_select[self.teamselect.get()].club_common_name, away=self.team_select[self.teamselect.get()].club_common_name)
        games = mlbgame.combine_games(month)

        #print("Games in June 2019")
        #for game in games:
        #    print(game)

        for game_objs in month:
            for daygames in game_objs:
                print("ID:", daygames.game_id)
                print("Away team", daygames.away_team)
                print("Home team", daygames.home_team)
                print("Date", daygames.date)
                print("Score: ", daygames.home_team_runs, "to", daygames.away_team_runs)

    def show_calendar(self):
        pass

window = Tk()
window.title("MLB Stats")
app = MLBapp(window)
window.mainloop()
