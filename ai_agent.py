
def is_empty(board):
    return board == [[' ']*len(board)]*len(board)

def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)

def is_win(board):
    
    black = score_of_col(board,'r')
    white = score_of_col(board,'b')
    
    sum_sumcol_values(black)
    sum_sumcol_values(white)
    
    if 5 in black and black[5] == 1:
        return 'Red'
    elif 5 in white and white[5] == 1:
        return 'Blue'
        
    if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or possible_moves(board)==[]:
        return 'Draw'
    return 'Continue playing'

def march(board,y,x,dy,dx,length):
    '''
    tìm vị trí xa nhất trong dy,dx trong khoảng length

    '''
    yf = y + length*dy 
    xf = x + length*dx
    # chừng nào yf,xf không có trong board
    while not is_in(board,yf,xf):
        yf -= dy
        xf -= dx
        
    return yf,xf
    
def score_init(scorecol):
    '''
    Khởi tạo hệ thống điểm

    '''
    sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1
            
    return sumcol
    
def sum_sumcol_values(sumcol):
    '''
    hợp nhất điểm của mỗi hướng
    '''
    
    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())
            
def score_of_list(lis,col):
    
    blank = lis.count(' ')
    filled = lis.count(col)
    
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

def row_to_list(board,y,x,dy,dx,yf,xf):
    '''
    trả về list của y,x từ yf,xf
    
    '''
    row = []
    while y != yf + dy or x !=xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row
    
def score_of_row(board,cordi,dy,dx,cordf,col):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    '''
    colscores = []
    y,x = cordi
    yf,xf = cordf
    row = row_to_list(board,y,x,dy,dx,yf,xf)
    for start in range(len(row)-4):
        score = score_of_list(row[start:start+5],col)
        colscores.append(score)
    
    return colscores

def score_of_col(board,col):
    '''
    tính toán điểm số mỗi hướng của column dùng cho is_win;
    '''

    f = len(board)
    
    #scores của 4 hướng đi
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    for start in range(len(board)):
        scores[(0,1)].extend(score_of_row(board,(start, 0), 0, 1,(start,f-1), col))
        scores[(1,0)].extend(score_of_row(board,(0, start), 1, 0,(f-1,start), col))
        scores[(1,1)].extend(score_of_row(board,(start, 0), 1,1,(f-1,f-1-start), col))
        scores[(-1,1)].extend(score_of_row(board,(start,0), -1, 1,(0,start), col))
        
        if start + 1 < len(board):
            scores[(1,1)].extend(score_of_row(board,(0, start+1), 1, 1,(f-2-start,f-1), col)) 
            scores[(-1,1)].extend(score_of_row(board,(f -1 , start + 1), -1,1,(start+1,f-1), col))
            
    return score_init(scores)
    
def score_of_col_one(board,col,y,x):
    '''
    trả lại điểm số của column trong y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    '''
    
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    
    scores[(0,1)].extend(score_of_row(board,march(board,y,x,0,-1,4), 0, 1,march(board,y,x,0,1,4), col))
    
    scores[(1,0)].extend(score_of_row(board,march(board,y,x,-1,0,4), 1, 0,march(board,y,x,1,0,4), col))
    
    scores[(1,1)].extend(score_of_row(board,march(board,y,x,-1,-1,4), 1, 1,march(board,y,x,1,1,4), col))

    scores[(-1,1)].extend(score_of_row(board,march(board,y,x,-1,1,4), 1,-1,march(board,y,x,1,-1,4), col))
    
    return score_init(scores)
    
def possible_moves(board):  
    '''
    trả về các ô trống xung quanh vùng đã đánh 1 đơn vị
    '''
    #mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
    # cord: lưu các vị trí không đi 
    cord = {}
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i,j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
    '''
    for direction in directions:
        dy,dx = direction
        for yx in taken:
            y,x = yx
            #note in[1,2,3,4]
            for length in [1]:
                move = march(board,y,x,dy,dx,length)
                if move not in taken and move not in yx:
                    cord[move]=False
    return cord
    
def TF34score(score3,score4):
    '''
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    '''
    for key4 in score4:
        if score4[key4] >=1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >=2:
                        return True
    return False
    
def evaluation(board,turn,anti,y,x):
    '''
    cố gắng di chuyển y,x
    trả về điểm số tượng trưng lợi thế 
    '''

    M = 1000
    res,adv, dis = 0, 0, 0
    
    #tấn công
    board[y][x]=turn
    #draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board,turn,y,x)       
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    #{0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]
    
    #phòng thủ
    board[y][x]=anti
    sumanticol = score_of_col_one(board,anti,y,x)  
    d = winning_situation(sumanticol)
    dis += d * (M)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

    res = adv + dis
    
    board[y][x]=' '
    return res
    
def winning_situation(sumcol):
    '''
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    '''
    
    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2):
        return 4
    elif TF34score(sumcol[3],sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(), reverse = True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0
    
def best_move(board, turn):
    '''
    trả lại nước đi tốt nhất tính được
    '''
    if turn == 'b':
        anti = 'r'
    else:
        anti = 'b'
        
    movecol = (0,0)
    maxscorecol = 0
    moves = possible_moves(board)

    for move in moves:
        y,x = move
        if maxscorecol == 0:
            scorecol=evaluation(board,turn,anti,y,x)
            maxscorecol = scorecol
            movecol = move
        else:
            scorecol=evaluation(board,turn,anti,y,x)
            if scorecol > maxscorecol:
                maxscorecol = scorecol
                movecol = move
    return movecol

def game_status(board, limit):
    draw  = True
    status = 0
    for row in range(limit):
        for column in range(limit):
            if board[row][column] != ' ':
                # vertical
                if column + 4 < limit:
                    if board[row][column] == board[row][column + 1] == board[row][column + 2] == board[row][column + 3] == board[row][column + 4]:
                        win_row = [[0,1],[row,column]]
                        if board[row][column] == 'r':
                            return -1, win_row
                        else:
                            return 1, win_row
                # diagonal\
                if column + 4 < limit and row + 4 <  limit:
                    if board[row][column] == board[row + 1][column + 1] == board[row + 2][column + 2] == board[row + 3][column + 3] == board[row + 4][column + 4]:
                        win_row = [[1,1],[row,column]]
                        if board[row][column] == 'r':
                            return -1, win_row
                        else:   
                            return 1, win_row
                # diagonal/
                if column + 4 < limit and row - 4 > 0:
                    if board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] == board[row - 3][column + 3] == board[row - 4][column + 4]:
                        win_row = [[-1,1],[row,column]]
                        if board[row][column] == 'r':
                            return -1, win_row
                        else:
                            return 1,win_row
                            # vertical
                if row + 4 < limit:
                    if board[row][column] == board[row + 1][column] == board[row + 2][column] == board[row + 3][column] == board[row + 4][column]:
                        win_row = [[1,0],[row,column]]
                        if board[row][column] == 'r':
                            return -1, win_row
                        else:
                            return 1,win_row
            elif board[row][column] == ' ':
                draw = False
    if draw:
        return 8, []
    return 0, []
