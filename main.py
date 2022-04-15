from threading import Timer
import time
import random
import tkinter as tk               
import tkinter.messagebox         #第8行中[0,-1]是按钮的雷状态和相邻雷数量,雷状态:-1=有雷,-2=有雷标🚩,接下行
def putMine():#布雷。              -3=有雷标❔,0=无雷未打开,1=无雷已打开，2=无雷标🚩,3=无雷标❔;接下行
    global numOfrow,numOfCol,mineMap      #相邻雷数量:-1未计算相邻地雷数,0-8相邻按钮下的雷数
    mineMap=[[[0,-1] for j in range(numOfCol)] for i in range(numOfrow)]      #矩阵初始化,无雷,未计算雷数  
    for i in random.sample(range(numOfrow*numOfCol), mines):  #随机取出若干(mines指定)数,组成列表,逐次赋给i
        mineMap[i//numOfCol][i%numOfCol][0]=-1      #将随机序号转为行列号，在该行列处按钮下布雷,-1=有雷无标记  
def getAroundBut(x, y):                       #返回列表，列表中包含x行y列按钮的所有相邻块(最多为8个)的行列号  
    return [(i,j) for i in range(max(0,x-1),min(numOfrow-1,x+1)+1)       #行号最小为0不为负,最大numOfrow-1
        for j in range(max(0,y-1),min(numOfCol-1,y+1)+1) if i !=x or j !=y]    #不包括自己，即x行y列方块
def showAllMines(i,j):                          #(i,j)是被鼠标左击按钮的坐标
    buttons[i,j]['background']='red'            #该按钮背景变红，表示被左击的雷
    for row in range(numOfrow):                 #row为行,0到numOfrow-1
        for col in range(numOfCol):             #col为列,0到numOfCol-1
            if mineMap[row][col][0]==-1 or mineMap[row][col][0]==-3:    #雷被正确标记为🚩，不显示雷                
                buttons[row,col]['relief']='groove'                     #按钮变为平面，不再有立体感
                buttons[row,col]['image']=p2
            if mineMap[row][col][0]==2:                                 #不是雷被标记为🚩，显示雷有红叉        
                buttons[row,col]['relief']='groove'                     #按钮变为平面，不再有立体感
                buttons[row,col]['image']=p3
def showNumOfMine():                            #使每个按钮都显示其相邻按钮下的雷数
    for row in range(numOfrow):                 #row为行,0到numOfrow-1,col为列,0到numOfCol-1
        for col in range(numOfCol):          #下句条件是该按钮未打开或标记为？,且计算了该按钮所有相邻块下的雷数
            if (mineMap[row][col][0]==0 or mineMap[row][col][0]==3) and mineMap[row][col][1]>=0:
                mineMap[row][col][0]=1          #设置为打开状态
                buttons[row,col]['text']=mineMap[row][col][1]   #显示该按钮相邻按钮下的雷数
                if mineMap[row][col][1]==0:                     #如果雷数为0，显示空白
                    buttons[row,col]['text']=''                                 
                buttons[row,col]['relief']='groove'             #按钮变为平面，不再有立体感
def getNumOfAroundMine(x,y):        #得到x行y列处按钮所有相邻按钮(最多为8个)下的地雷数
    if mineMap[x][y][0]<0:          #按钮的雷状态值<0,说明此按钮下有雷，点击到雷，游戏结束
        return 0
    aroundBut =getAroundBut(x, y)   #列表aroundBut中是x行y列按钮所有相邻按钮(最多为8个)的行列号
    mineSum = 0                     #变量mineSum记录地雷数，初始为0
    for i, j in aroundBut:
        if mineMap[i][j][0]<0:      #该项为-1=有雷、-2=有雷标🚩,-3=有雷标❔，所以是负数表示块下有雷
            mineSum += 1
    mineMap[x][y][1]=mineSum            #该项为-1未计算相邻地雷数,为0到8是相邻地雷数     
    if mineSum == 0:         #如其相邻按钮下雷数为0,其相邻所有按钮都要打开,要计算这些要打开的按钮所有相邻按钮下雷数
        for i, j in aroundBut:
            if mineMap[i][j][1]==-1:          #该按钮未被计算过其相邻地雷数
                getNumOfAroundMine(i,j)       #递归调用 
    return 1                 
def btnClick(x,y):              #所有鼠标左键单击按钮的事件函数,有两个参数,被点击按钮所在位置行列号
    global gameOver,timer,isTimerRun   #如果游戏结束，不再响应鼠标左键单击及双击和鼠标右键单击事件
    if gameOver or mineMap[x][y][0]==-2 or 0<mineMap[x][y][0]<3:    #游戏结束、做了雷标记按钮都不处理
        return
    if not timer.is_alive():            #子线程只能启动一次，即线程不是激活的时候，才能启动子线程
        isTimerRun=True
        timer.start()                   #启动子线程
    if getNumOfAroundMine(x,y)==0:      #返回值为0，左击了有雷的按钮，游戏结束
        showAllMines(x,y)               #将所有雷显示出来
        gameOver=True                   #游戏结束标志
        isTimerRun=False
        label['text']='你输了'
        return
    showNumOfMine()
    isWin()
def RClick_LDoubleClick(evt,x,y):          #处理鼠标右击和鼠标左键双击事件
    global gameOver,isTimerRun                
    if gameOver:                           #如果游戏结束，不再响应鼠标左键单击及双击和鼠标右键单击事件
        return
    if evt.num==1:                         #=1,是左键,是鼠标左键双击按钮事件            
        if mineMap[x][y][1]!=0 and mineMap[x][y][0]==1:     #被双击按钮邻近按钮有雷且已被单击打开
            aroundBut =getAroundBut(x, y)  #列表aroundBut中是x行y列按钮的所有相邻按钮(最多为8个)的行列号
            mineFlagSum = 0                #变量mineFlagSum记录相邻按钮被标记为红旗标的数量，初始为0
            for i, j in aroundBut:          #计算被双击按钮所有相邻按钮被标记为红旗标的数量
                if mineMap[i][j][0]==-2 or mineMap[i][j][0]==2:             #-2有雷标🚩,2无雷标🚩
                    mineFlagSum += 1                                        #只要被🚩标记，+1
            if mineFlagSum==mineMap[x][y][1]:       #后一项是被双击按钮显示的所有相邻按钮的雷数
                for i, j in aroundBut:              #对所有相邻未标记红旗按钮均进行一次左键单击按钮操作
                    if getNumOfAroundMine(i,j)==0 and mineMap[i][j][0]==-1:  #如是无标记的雷，游戏结束
                        showAllMines(i,j)           #将所有雷显示出来，没标记出来的雷底色变红
                        gameOver=True               #游戏结束标志
                        isTimerRun=False
                        label['text']='你输了'
                        return
            showNumOfMine()
        isWin()
    else:                                   #=3是右键,是鼠标右键单击按钮事件，为未打开的按钮做标记       
        if mineMap[x][y][0]==1:             #该按钮已被打开，已显示其相邻按钮下的地雷数，不能做标记
            return
        m=mineMap[x][y][0]          #不知何故，必须用m作为myDict键，用mineMap[i][j][0]直接作键出错
        myDict={-1:(-2,p,''),-2:(-3,'','?'),-3:(-1,'',''),0:(2,p,''),2:(3,'','?'),3:(0,'','')}
        mineMap[x][y][0]=myDict[m][0]    
        buttons[x,y]['image']=myDict[m][1]
        buttons[x,y]['text']=myDict[m][2]
        isWin()
def isWin():
    global mines,numOfrow,numOfCol,gameOver,isTimerRun
    sumOfmineWithFlag=0                 #所有按钮下有地雷被标🚩的总数
    sumOfNomineWithFlag=0               #所有按钮下无地雷被标🚩的总数
    sumOfOpenBlock=0                    #所有被打开的按钮的总数，等于所有按钮数-所有雷数
    for i in range(numOfrow):           #i为行,0到numOfrow-1
        for j in range(numOfCol):       #j为列,0到numOfCol-1
            if mineMap[i][j][0]==-2:    #如果该按钮下地雷被标🚩
                sumOfmineWithFlag+=1
            elif mineMap[i][j][0]==2:   #如果该按钮下无地雷被标🚩
                sumOfNomineWithFlag+=1
            elif mineMap[i][j][0]==1:   #如果该按钮已被打开
                sumOfOpenBlock+=1
    s=mines-(sumOfmineWithFlag+sumOfNomineWithFlag)     #s为未被标记的地雷数
    if s<0:                             #如无雷也被标记红旗，可能出现标记红旗的按钮数大于地雷数，雷数不能为负
        s=0                             #标记为🚩的所有块>实际雷数，仍显示0个雷
    label['text']=str(s)                #显示剩余地雷数
    if sumOfmineWithFlag==mines and sumOfOpenBlock==numOfCol*numOfrow-mines:        #胜利条件是：(接下行)
        label['text']='你赢了'          #正确标记雷的按钮数=雷的实际数量和单击打开按钮数=按钮总数-雷的实际数量
        gameOver=True
        isTimerRun=False
def reSet():                        #在重玩游戏前调用此程序完成游戏初始化
    global mines,numOfrow,numOfCol,gameOver,buttons,mineMap,timer,isTimerRun
    label['text']=str(mines)        #初始显示该游戏等级初始的雷数，用红旗标记一个雷，该值减1
    label1['text']='0'              #游戏重新开始，秒表清0
    mineMap=[]   #记录指定行列数方块矩阵中每个方块的两个状态值,是3维矩阵，mineMap[i][j][k]，i行号j列号，k=0或1    
    putMine()    #初始化mine_map，并在列表中随机增加地雷
    for row in range(numOfrow):                     #row为行,0到numOfrow-1
        for col in range(numOfCol):                 #col为列,0到numOfCol-1
            buttons[row,col]['text']=''             #按钮标题显示为空                                
            buttons[row,col]['relief']='raised'     #按钮立体状
            buttons[row,col]['image']=''            #去掉按钮显示的图形
            buttons[row,col]['bg']='Silver'         #按钮背景为银白色，以上按钮属性在完成游戏后都有可能被改变
    gameOver=False
    isTimerRun=False
    timer=Timer(1, count)   #建立Timer类对象，1秒后将调用函数count()在子线程中运行，可参见我的有关多线程秒表的博文
    timer.setDaemon(True)   #成为主线程的守护线程,当主进程结束后,子线程也会随之结束。否则计数未停止前，关闭窗口，会抛出异常
def count():                #该函数完成秒表功能，将运行在子线程中
    global isTimerRun       #启动子线程代码timer.start()在函数btnClick(x,y)中
    k=0
    while isTimerRun and k<1000:      #isTimerRun=Ture且秒数<1000，将一直计算秒数。退出该函数，子线程结束，计算秒数结束
        k+=1
        label1['text']=str(k)           #将秒数显示在label1
        time.sleep(1)                   #休眠1秒。
def do_job():
    s='左击方块,是雷游戏结束,否则显示相邻8块地雷数,空相邻无雷\n'+\
    '右击方块标记红旗表示有雷,再右击变？,再右击无标记\n'+\
    '方块显示n,相邻8块标记n块有雷,左键双击等效单击邻近8块无雷块'+\
    '\n如雷标记有错，游戏结束。                保留所有版权'
    tkinter.messagebox.showinfo(title="帮助",message=s)
def setGameLevel(row=0,col=0,mine=0):
    global mines,numOfrow,numOfCol,buttons
    if mines==mine and numOfrow==row and numOfCol==col:         #如果新行列数、地雷数和旧的相同,不必删所有按钮重建
        reSet()
        return
    if len(buttons)!=0:                         #初始还未创建按钮，无按钮可删
        for r in range(numOfrow):               #删除所有按钮
            for c in range(numOfCol):
                buttons[r,c].destroy()
    numOfrow=row                                #设置新行列数、雷数
    numOfCol=col
    mines=mine
    for row in range(numOfrow):         #row为行,0到numOfrow-1，col为列,0到numOfCol-1
        for col in range(numOfCol):     #创建新的numOfrow行，numOfCol列按钮矩阵
            def but_RDclick(event,x=row,y=col): #鼠标右击和鼠标左键双击的事件函数，参数x,y默认值是按钮的行列数
                RClick_LDoubleClick(event,x,y)              #所有事件函数都调用同一函数
            button=tk.Button(root,command=lambda x=row,y=col:btnClick(x,y),bg="Silver",fg='red',font=("Arial",20))
            button.place(x=20+col*32,y=45+row*32,width=30,height=30)
            button.bind("<Button-3>", but_RDclick)                  #鼠标右击按钮事件绑定事件函数为but_RDclick
            button.bind("<Double-Button-1>", but_RDclick)           #鼠标左键双击按钮事件绑定事件函数为but_RDclick        
            buttons[row,col]=button                                 #字典，键为行列号，值为该行列号的按钮对象
    root.geometry(f"{numOfCol*32+40}x{numOfrow*32+65}")             #numOfrow和numOfCol改变,主窗体尺寸也要改变
    label1.place(x=f"{numOfCol*32-15}",y=5,width=40,height=30)      #numOfrow和numOfCol改变,秒表和重玩按钮位置也要改变
    button1.place(x=f"{numOfCol*17-10}",y=5,width=50,height=30)     #在字符串前加f,字符串中的{}内容是表达式
    reSet()
root = tk.Tk()                  #初始化窗口
root.title('扫雷')              #窗口标题
root.resizable(width=False,height=False)            #设置窗口是否可变，宽不可变，高不可变，默认为True
menubar = tk.Menu(root)         #创建一个菜单栏，可把它理解成一个容器，在窗口的上方，可放置多个能下拉菜单项
cameMenu = tk.Menu(menubar, tearoff=0)  #创建1个能下拉菜单项，点击后显示下拉菜单，下拉菜单包括多个子菜单项
menubar.add_cascade(label='游戏', menu=cameMenu)    #将能下拉菜单项放入menubar，并指定其名称为：游戏
cameMenu.add_command(label='重玩', command=reSet)  
cameMenu.add_separator()                        #添加一条分隔线，上句为能下拉菜单项的第一个子菜单项：重玩
cameMenu.add_command(label='初级', command=lambda row=6,col=6,mine=5:setGameLevel(row,col,mine))
cameMenu.add_command(label='中级', command=lambda row=9,col=9,mine=15:setGameLevel(row,col,mine))
cameMenu.add_command(label='高级', command=lambda row=12,col=12,mine=33:setGameLevel(row,col,mine))
cameMenu.add_command(label='自定义')    #修改以上3条语句，可修改每级的行数、列数和地雷数
cameMenu.add_separator()    
cameMenu.add_command(label='退出', command=root.quit) # 用tkinter里面自带的quit()函数
helpMenu = tk.Menu(menubar, tearoff=0)  #创建第2个能下拉菜单项,点击后显示下拉菜单,下拉菜单可包括多个子菜单项
menubar.add_cascade(label='帮助', menu=helpMenu)    #将能下拉菜单项放入menubar，并指定其名称为：帮助
helpMenu.add_command(label='关于本游戏', command=do_job)  #能下拉菜单项的第一个子菜单项：关于本游戏
root.config(menu=menubar)                                #让菜单显示出来
gameOver=isTimerRun=False       #初始游戏结束标志为假，定时器是否运行为假
numOfrow=numOfCol=mines=0       #方块矩阵的行列数和雷数，以下3个变量必须为0，确保函数setGameLevel第2条语句不成立
timer=0  #此变量将引用在reSet()函数中定义的Timer对象，可取消该条语句，不会出错，这条语句只为了说明其是全局变量
buttons={}   #字典，键为行列号，值为该行列号的按钮对象
mineMap=[]   #记录指定行列数方块矩阵中每个方块的两个状态值,是3维矩阵，mineMap[i][j][k]，i行号j列号，k=0或1
label=tk.Label(root,text=str(mines),bd='5',fg='red',font=("Arial",15))
label.place(x=10,y=5,width=60,height=30)
label1=tk.Label(root,text='0',bd='5',fg='red',font=("Arial",15))
button1=tk.Button(root,text='重玩',command=reSet,fg='red',font=("Arial",15))
p = tk.PhotoImage(file='pic/红旗.png') 
p2= tk.PhotoImage(file='pic/地雷2.png')
p3= tk.PhotoImage(file='pic/地雷3.png')
setGameLevel(6,6,5)     #修改函数的3个参数值，改变程序开始扫雷的等级，这里是初级
root.mainloop()	


