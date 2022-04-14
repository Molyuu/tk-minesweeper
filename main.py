# 救救我
# 我被困在注释里
# 求求你
# 帮帮我！！！！
# 哎呀 这不高嘉麒吗？
# 哈哈哈哈哈
# 还想跑出去？
# 卧槽，生物还有作业？？
# 生物作业咋写……帮帮我……
# 我玩你妈
# 开摆了 

from random import randint

class Lawn():
    def __init__(self, cols, rows, mines_num):
        self.mines_map = [[0 for row in range(rows)] for col in range(cols)]
        self.lawn_map = [['■' for row in range(rows)] for col in range(cols)]
        self.cols, self.rows = cols, rows
        self.mines_num = mines_num
        self.game_active = True

    def initialize(self, col, row):
        self.plant_mines(col, row)
        self.cells_neighbor_mines()

    def sweep_mine(self, col, row):
        if self.game_active:
            self.initialize(col, row)
            self.game_active = False
        self.lawn_map[col][row] = str(self.mines_map[col][row])
        self.check_res(col, row)
        self.unfold_nomine_place(col, row)

    def flag(self, col, row):
        if self.lawn_map[col][row] == '#':
            self.lawn_map[col][row] = '?'
        elif self.lawn_map[col][row] == '?':
            self.lawn_map[col][row] = '■'
        elif self.lawn_map[col][row] == '■':
            self.lawn_map[col][row] = '#'
        
    def unfold_nomine_place(self, col, row):
        check_list, checked_list = [(col, row)], []
        while check_list:
            deal_list, stack = [], []
            i, j = check_list[0][0], check_list[0][1]
            self.cell_neighbor(deal_list, check_list[0][0], check_list[0][1])
            self.get_cell_neighbor(stack, deal_list)
            checked_list.append(check_list.pop(0))
            if self.lawn_map[i][j] == '0':
                for k in range(len(stack)):
                    x, y = stack[k][0], stack[k][1]
                    if self.lawn_map[x][y] in '#?':
                        continue
                    self.lawn_map[x][y] = str(self.mines_map[x][y])
                    if (x, y) not in checked_list and (x, y) not in check_list:
                        check_list.append((x, y))
               
    def show_underlawn(self):
        for col in range(self.cols):
            print(self.mines_map[col])

    def show(self):
        for col in range(self.cols):
            print(self.lawn_map[col])

    def plant_mines(self, col, row):
        deal_list = [] 
        self.cell_neighbor(deal_list, col, row)
        deal_list.append((col, row))
        mines_count = self.mines_num
        while mines_count > 0:
            mine_x, mine_y = randint(0, self.cols - 1), randint(0, self.rows - 1)
            if self.mines_map[mine_x][mine_y] != 9:
                self.mines_map[mine_x][mine_y] = 9
                mines_count -= 1
            for i in range(len(deal_list)):
                x, y= deal_list[i][0], deal_list[i][1]
                if self.mines_map[x][y] != 0:
                    self.mines_map[x][y] = 0
                    mines_count += 1

    def cells_neighbor_mines(self):
        for col in range(self.cols):
            for row in range(self.rows):
                if self.mines_map[col][row] == 9:
                    deal_list, stack = [], []
                    self.cell_neighbor(deal_list, col, row)         
                    self.get_cell_neighbor(stack, deal_list)
                    for i in range(len(stack)):
                        x, y = stack[i][0], stack[i][1]
                        if self.mines_map[x][y] != 9:
                            self.mines_map[x][y] += 1

    def cell_neighbor(self, deal_list, col, row):
        for x in range(col - 1, col + 2):
            for y in range(row - 1, row + 2):
                if x != col or y != row:
                    deal_list.append((x,y))
 
    def get_cell_neighbor(self, stack, deal_list):
        for i in range(len(deal_list)):
            if deal_list[i][0] not in range(self.cols) or deal_list[i][1] not in range(self.rows):
                continue
            else:
                stack.append(deal_list[i])

    def check_res(self, col , row):
        count = 0
        if self.mines_map[col][row] == 9:
            print('你踩到雷了！！！')
        for i in range(self.cols):
            for j in range(self.rows):
                if self.lawn_map[i][j] in '#?■':
                    count += 1              
        if count == self.mines_num:
            print('你胜利了！！！')

def play(col, row, mode = 0):
    if mode == 0:
        lawn.sweep_mine(col, row)
    else:
        lawn.flag(col, row)


col, row, num = eval(input('请输入方阵的大小，地雷的数量【例如：8，8，10。8X8的方阵，10个地雷。】:'))
lawn = Lawn(col, row, num)
while True:
    lawn.show()
    lawn.show_underlawn()
    col,row,mode = eval(input('请输入要铲多少行多少列的地方，并且加一个数。如果最后一个数非0，表示鼠标右键【插旗】：'))
    play(col, row, mode)

