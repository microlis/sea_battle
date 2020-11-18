from random import randrange
from time import time
from tkinter import *
from Ship import *
from tkinter.messagebox import *
import _thread

class Application(Frame):
    width = 800
    height = 400
    bg = "white"
    indent = 2
    gauge = 32
    offset_y = 40
    offset_x_user = 30
    offset_x_comp = 430
    fleet_time = 0
    fleet_comp = []
    fleet_user = []
    comp_shoot = []

    def createCanvas(self):
        self.canv = Canvas(self)
        self.canv["height"] = self.height
        self.canv["width"] = self.width
        self.canv["bg"] = self.bg
        self.canv.pack()
        self.canv.bind("<Button-1>",self.userPlay)

    def new_game(self):
        self.canv.delete('all')
        for i in range(10):
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                self.canv.create_rectangle(xn,yn,xk,yk,tag = "my_"+str(i)+"_"+str(j))

        for i in range(10):
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                self.canv.create_rectangle(xn,yn,xk,yk,tag = "nmy_"+str(i)+"_"+str(j),fill="gray")

        for i in reversed(range(10)):
            xc = self.offset_x_user - 15
            yc = i*self.gauge + (i+1)*self.indent + self.offset_y + round(self.gauge/2)
            self.canv.create_text(xc,yc,text=str(i+1))
            xc = self.offset_x_comp - 15
            yc = i*self.gauge + (i+1)*self.indent + self.offset_y + round(self.gauge/2)
            self.canv.create_text(xc,yc,text=str(i+1))
        symbols = "АБВГДЕЖЗИК"
        for i in range(10):
            xc = i*self.gauge + (i+1)*self.indent + self.offset_x_user + round(self.gauge/2)
            yc = self.offset_y - 15
            self.canv.create_text(xc,yc,text=symbols[i])
            xc = i*self.gauge + (i+1)*self.indent + self.offset_x_comp + round(self.gauge/2)
            yc = self.offset_y - 15
            self.canv.create_text(xc,yc,text=symbols[i])

        self.fleet_time = time()
        _thread.start_new_thread(self.createShips,("nmy",))
        self.createShips("my")

    def createShips(self, prefix):
        count_ships = 0
        while count_ships < 10:
            fleet_array = []
            count_ships = 0
            fleet_ships = []
            for length in reversed(range(1,5)):
                for i in range(5-length):
                    try_create_ship = 0
                    while 1:
                        try_create_ship += 1
                        if try_create_ship > 50:
                            break
                        ship_point = prefix+"_"+str(randrange(10))+"_"+str(randrange(10))
                        orientation = randrange(2)
                        new_ship = Ship(length,orientation,ship_point)
                        intersect_array = list(set(fleet_array) & set(new_ship.around_map+new_ship.coord_map))
                        if new_ship.ship_correct == 1 and len(intersect_array) == 0:
                            fleet_array += new_ship.around_map + new_ship.coord_map
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            break
        print(prefix,time() - self.fleet_time,"секунд")
        if prefix == "nmy":
            self.fleet_comp = fleet_ships
        else:
            self.fleet_user = fleet_ships
            self.paintShips(fleet_ships)

    def paintShips(self,fleet_ships):
        for obj in fleet_ships:
            for point in obj.coord_map:
                self.canv.itemconfig(point,fill="gray")

    def paintCross(self,xn,yn,tag):
        xk = xn + self.gauge
        yk = yn + self.gauge
        self.canv.itemconfig(tag,fill="white")
        self.canv.create_line(xn+2,yn+2,xk-2,yk-2,width="3")
        self.canv.create_line(xk-2,yn+2,xn+2,yk-2,width="3")

    def paintMiss(self,point):
        new_str = int(point.split("_")[1])
        new_stlb = int(point.split("_")[2])
        if point.split("_")[0] == "nmy":
            xn = new_stlb*self.gauge + (new_stlb+1)*self.indent + self.offset_x_comp
        else:
            xn = new_stlb*self.gauge + (new_stlb+1)*self.indent + self.offset_x_user
        yn = new_str*self.gauge + (new_str+1)*self.indent + self.offset_y
        self.canv.itemconfig(point,fill="white")
        self.canv.create_oval(xn+13,yn+13,xn+17,yn+17,fill="gray")

    def checkFinish(self,type):
        status = 0
        if type == "user":
            for ship in self.fleet_comp:
                status += ship.death
        else:
            for ship in self.fleet_user:
                status += ship.death
        return status

    def compPlay(self,step = 0):
        print(step)
        if step == 0:
            while 1:
                i = randrange(10)
                j = randrange(10)
                if not("my_"+str(i)+"_"+str(j) in self.comp_shoot):
                    break
        else:
            points_around = []
            i = int(self.comp_shoot[-1].split("_")[1])
            j = int(self.comp_shoot[-1].split("_")[2])
            for ti in range(i-1,i+2):
                for tj in range(j-1,j+2):
                    if ti>=0 and ti<=9 and tj>=0 and tj<=9 and ti != tj and (ti == i or tj == j) and not(ti == i and tj == j) and not("my_"+str(ti)+"_"+str(tj) in self.comp_shoot):
                        points_around.append([ti,tj])
            select = randrange(len(points_around))
            i = points_around[select][0]
            j = points_around[select][1]
        xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
        yn = i*self.gauge + (i+1)*self.indent + self.offset_y
        hit_status = 0
        for obj in self.fleet_user:
            if "my_"+str(i)+"_"+str(j) in obj.coord_map:
                hit_status = 1
                self.paintCross(xn,yn,"my_"+str(i)+"_"+str(j))
                self.comp_shoot.append("my_"+str(i)+"_"+str(j))
                if obj.shoot("my_"+str(i)+"_"+str(j)) == 2:
                    hit_status = 2
                    obj.death = 1
                    for point in obj.around_map:
                        self.paintMiss(point)
                        self.comp_shoot.append(point)
                break
        print("hit_status",hit_status)
        if hit_status == 0:
            self.comp_shoot.append("my_"+str(i)+"_"+str(j))
            self.paintMiss("my_"+str(i)+"_"+str(j))
        else:
            if self.checkFinish("comp") < 10:
                if hit_status == 1:
                    step += 1
                    if step > 4:
                        self.compPlay()
                    else:
                        self.compPlay(step)
                else:
                    self.compPlay()
            else:
                showinfo("Морской бой", "Вы проиграли!")

    def userPlay(self,e):
        for i in range(10):
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                if e.x >= xn and e.x <= xk and e.y >= yn and e.y <= yk:
                    hit_status = 0
                    for obj in self.fleet_comp:
                        if "nmy_"+str(i)+"_"+str(j) in obj.coord_map:
                            hit_status = 1
                            self.paintCross(xn,yn,"nmy_"+str(i)+"_"+str(j))
                            if obj.shoot("nmy_"+str(i)+"_"+str(j)) == 2:
                                obj.death = 1
                                for point in obj.around_map:
                                    self.paintMiss(point)
                            break
                    if hit_status == 0:
                        self.paintMiss("nmy_"+str(i)+"_"+str(j))
                        if self.checkFinish("user") < 10:
                            self.compPlay()
                        else:
                            showinfo("Морской бой", "Вы выиграли!")
                    break

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.m = Menu(master)
        master.config(menu = self.m)
        self.m_play = Menu(self.m)
        self.m.add_cascade(label = "Игра",menu = self.m_play)
        self.m_play.add_command(label="Новая игра", command = self.new_game)
        self.createCanvas()