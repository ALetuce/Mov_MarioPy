import re

# funciones 

'''
Remove_UsingSpan
———————–
string : str
span : tuple
————————
Extrae y borra una parte de un string dado por su span, retornando el string actualizado  '''
def Remove_UsingSpan(string, span):
    HeadStr = string[:span[0]]
    TailStr = string[span[1]:]
    return HeadStr + TailStr
'''
getNew_XY
———————–
x : int
y : int
dir : str
N : int
......
————————
Busca las coordenadas dadas por dir y las retorna '''
def getNew_XY(x, y, dir, N):
    info = Breakdown_ExtendedDir(dir)
    dirX = info[0]
    dirY = info[1]
    stepsX = info[2]
    stepsY = info[3]

    # Para x
    if dirX == "L":
        x -= stepsX
        if not (0 < x < N-1):
            x = x % N
    elif dirX == "R":
        x += stepsX
        if not (0 < x < N-1):
            x = x % N
        
    # Para y
    if dirY == "U":
        y -= stepsY
        if not (0 < y < N-1):
            y = y % N
    elif dirY == "D":
        y += stepsY
        if not (0 < y < N-1):
            y = y % N

    return (x,y)
'''
Breakdown_ExtendedDir
———————–
dir : str
————————
Analiza una lista de direcciones y las reduce a 1 solo valor/direccion para cada eje, X e Y, que luego retorna  '''
def Breakdown_ExtendedDir(dir):
    # filtramos todo el bloque de direcciones en en solo 2 (D|U)[num] (<|>)[num]
    stepsXaxis = 0
    stepsYaxis = 0
    pos = 0
    while pos < len(dir):
        if re.match('U', dir[pos]):
            num = re.match('\d+', dir[pos+1:]).group()
            stepsYaxis += int(num)
        elif re.match('D', dir[pos]):
            num = re.match('\d+', dir[pos+1:]).group()
            stepsYaxis -= int(num)
        elif re.match('<', dir[pos]):
            num = re.match('\d+', dir[pos+1:]).group()
            stepsXaxis -= int(num)
        elif re.match('>', dir[pos]):
            num = re.match('\d+', dir[pos+1:]).group()
            stepsXaxis += int(num)
        pos += 1

    # establecemos las variables dir[X|Y] y steps[X|Y]axis
    if stepsXaxis > 0:
        dirX = "R"
    else:
        dirX = "L"
        stepsXaxis *= -1
    if stepsYaxis > 0:
        dirY = "U"
    else:
        dirY = "D"
        stepsYaxis *= -1
        
    return(dirX, dirY, stepsXaxis, stepsYaxis)

'''
get_CompleteDir
———————–
line : str
————————
Extrae y retorna todos los comandos direccionales consecutivos al comienzo de la linea '''
def get_CompleteDir(line):
    complete_dir = ""
    firstDir_expected = True
    flag = True
    while flag:
        if re.match('D|U|<|>', line):
            firstDir_expected = False
            dir = re.match('D|U|<|>', line).group()
            complete_dir += dir
            line = Remove_UsingSpan(line, (0,1))

            if re.match('\d+', line):
                num = re.match('\d+', line).group()  
                span = re.match('\d+', line).span()

                if num[0] == 0:
                    return False
                complete_dir += num
                line = Remove_UsingSpan(line, span)
            else:
                return False
        
        if re.match('A|B|L(c|e)|S(c|e)|R|Z|\?|X|Y', line):
            if firstDir_expected:
                return False
            else:
                flag = False
        if line == '':
            flag = False

    return (complete_dir, line)

'''
ProcessCommands
———————–
commands : list
Matrix : MatrixClass
————————
Procesa una lista de comandos valida. Interactua con la Matriz, no retorna nada  '''
def ProcessCommands(commands, Matrix):
    pos = 0
    while pos < len(commands):
        command = commands[pos]

        if re.match('A', command):
            Matrix.A()

        elif re.match('B', command):
            Matrix.B()

        elif re.match('X', command):
            pos+=1
            dir = re.match('[A-Z0-9><]+', commands[pos]).group()
            Matrix.X(dir)

        elif re.match('Y', command):
            pos +=1
            dir = re.match('[A-Z0-9<>]+', commands[pos]).group()
            Matrix.Y(dir)
        
        elif re.match('\?', command):
            directions_to_check = []
            pos +=1
            dir = re.match('[A-Z0-9<>]+', commands[pos]).group()
            directions_to_check.append(dir)
            pos+=1
            if re.match('A|B|L(c|e)|S(c|e)|R|Z', commands[pos]):
                action = re.match('A|B|L(c|e)|S(c|e)|R|Z', commands[pos]).group()

            elif re.match('X|Y', commands[pos]):
                action = re.match('X|Y', commands[pos]).group()
                pos+=1
                dir = re.match('[A-Z0-9<>]+', commands[pos]).group()
                action += dir

            elif re.match('\?', commands[pos]):
                # en caso de recursion
                flag = True
                while flag:
                    directions_to_check.append(dir)
                    # buscamos la nueva direccion 
                    pos+= 1
                    dir = re.match('[A-Z0-9<>]+', commands[pos]).group()
                    # buscamos la accion 
                    pos+=1
                    if re.match('A|B|L(c|e)|S(c|e)|R|Z', commands[pos]):
                        action = re.match('A|B|L(c|e)|S(c|e)|R|Z', commands[pos]).group()
                        flag = False
                    elif re.match('X|Y', commands[pos]):
                        action = re.match('X|Y', commands[pos]).group()
                        pos+=1
                        dir = re.match('[A-Z0-9<>]+', commands[pos]).group()
                        action += dir
                        flag = False
                
            all_good = True
            for dir in directions_to_check:
                if Matrix.get_Value(dir) <= 0:
                    all_good = False
            if all_good:
                if action == 'A':
                    Matrix.A()
                elif action == 'B':
                    Matrix.B()
                elif re.match('X', action):
                    dir = re.search('\d+', action).group()
                    Matrix.X(dir)
                elif re.match('Y', action):
                    dir = re.search('\d+', commands[pos]).group()
                    Matrix.Y(dir)
                elif action == 'Lc':
                    Matrix.LogASCII()
                elif action == 'Le':
                    Matrix.LogValue()
                elif action == 'Se':
                    Matrix.ViewASCII()
                elif action == 'Sc':
                    Matrix.ViewValue()
                elif action == 'R':
                    Matrix.R()
                elif action == 'Z':
                    Matrix.Z() 
            
        elif re.match('U\d+', command):
            num = re.search('\d+', command).group()
            Matrix.Up(int(num))

        elif re.match('D\d+', command):
            num = re.search('\d+', command).group()
            Matrix.Down(int(num))

        elif re.match('>\d+', command):
            num = re.search('\d+', command).group()
            Matrix.Right(int(num))

        elif re.match('<\d+', command):
            num = re.search('\d+', command).group()
            Matrix.Left(int(num))

        elif re.match('Lc', command):
            Matrix.LogASCII()

        elif re.match('Le', command):
            Matrix.LogValue()

        elif re.match('R', command):
            Matrix.R()

        elif re.match('Z', command):
            Matrix.Z()

        elif re.match('Sc',command):
            Matrix.ViewASCII()

        elif re.match('Se', command):
            Matrix.ViewValue()

        pos += 1

'''
ProcessRawLine
———————–
line : str
————————
Procesa una lista de comandos en bruto sin parentesis, evalua errores de sintaxix 
Si la linea es valida retorna la lista de comandos ordenada por prioridad. Si no, retorna False'''
def ProcessRawLine(line):
    correct_CommandsList = []

    while line != "":
        if re.match('A|B|L(c|e)|S(c|e)|R|Z', line):
            match = re.match('A|B|L(c|e)|S(c|e)|R|Z', line).group()
            span = re.match('A|B|L(c|e)|S(c|e)|R|Z', line).span()
            correct_CommandsList.append(match)
            line = Remove_UsingSpan(line, span)

        elif re.match('U|D|<|>', line):
            if re.match('[U|D|<|>]\d+', line):
                match = re.match('[U|D|<|>]\d+', line).group()
                span = re.match('[U|D|<|>]\d+', line).span()

                num = re.search('\d+', match).group()
                if num[0] == "0":
                    return False

                correct_CommandsList.append(match)
                line = Remove_UsingSpan(line, span)
            else:
                return False

        elif re.match('X|Y', line):
            match_XY = re.match('X|Y', line).group()
            line = Remove_UsingSpan(line, (0,1))

            # buscamos el conjunto de direcciones o error/False (si la linea esta mala), almacenamos en Result
            dir_and_newline = get_CompleteDir(line)
            if dir_and_newline:
                CompleteDir = dir_and_newline[0]
                line = dir_and_newline[1] # new line

                correct_CommandsList.append(match_XY)
                correct_CommandsList.append(CompleteDir)
            else:
                return False

        elif re.match('\?', line):
            accion = ""
            line = Remove_UsingSpan(line, (0,1))
            flag = True
            while flag:
                dir_and_newline = get_CompleteDir(line)
                if dir_and_newline:
                    CompleteDir = dir_and_newline[0]
                    line = dir_and_newline[1] # new line
                else:
                    return False

                # buscamos la accion a realizar
                if re.match('A|B|L(c|e)|S(c|e)|R|Z', line):
                    accion = re.match('A|B|L(c|e)|S(c|e)|R|Z', line).group()
                    span = re.match('A|B|L(c|e)|S(c|e)|R|Z', line).span()
                    line = Remove_UsingSpan(line, span)
                    flag = False

                elif re.match('X|Y', line):
                    match_XY = re.match('X|Y', line).group()
                    line = Remove_UsingSpan(line, (0,1))

                    dir_and_newline = get_CompleteDir(line)
                    if dir_and_newline:
                        CompleteDir = dir_and_newline[0]
                        line = dir_and_newline[1] # new line
                    else:
                        return False

                    flag = False

                elif re.match('\?', line):
                    correct_CommandsList.append("?")
                    correct_CommandsList.append(CompleteDir)
                    line = Remove_UsingSpan(line, (0,1))

            correct_CommandsList.append("?")
            correct_CommandsList.append(CompleteDir)
            correct_CommandsList.append(accion)

    return correct_CommandsList

'''
Compiler
———————–
line : str
......
————————
Procesa los parentesis de la linea, evalua prioridad. 
Si la linea es valida retorna la lista de comandos ordenada por prioridad. Si no, retorna False'''
def Compiler(line):
    CommandsList = []
    
    # busca el parentesis bien definido con mayor prioridad
    while re.search('\([A-Za-z0-9?<>]*\)', line):
        if re.search('\(\)', line):
            return False
        match = re.search('\([A-Za-z0-9?<>]+\)', line).group()
        span = re.search('\([A-Za-z0-9?<>]+\)', line).span()
        
        match = match[1:-1]     # le quito los parentesis
        com = ProcessRawLine(match)

        if com == False:
            return False
        else:
            for c in com:
                CommandsList.append(c) 
        line = Remove_UsingSpan(line, span) 

    # verifica que no queden parentesis, si quedan es porque no estaba bien balanceada
    if re.search('\(|\)', line):
        return False
    
    # preguntamos si queda algo mas, si queda lo procesamos
    if re.search('[A-Za-z0-9?<>]+', line):
        match = re.search('[A-Za-z0-9?<>]+', line).group()
        span = re.search('[A-Za-z0-9?<>]+', line).span()
        
        com = ProcessRawLine(match)

        if com:
            for c in com:
                CommandsList.append(c) 
        else:
            return False

        line = Remove_UsingSpan(line, span)
    
    if line != '':
        return False
    return CommandsList

'''
NewMatrixHelp
———————–
N : int
————————
Crea una matriz de tamaño N y retorna su direccion de memoria '''
def NewMatrixHelp(N):
    Matrix = []
    i = 0
    j = 0
    while i < N:
        Matrix.append([])
        while j < N:
            Matrix[i].append(0)
            j += 1
        i += 1
        j = 0
    return Matrix

# clases

class MatrixClass:
    def __init__(self, N):
        self.N = N
        self.pos_row = 0
        self.pos_column = 0
        self.Matrix = NewMatrixHelp(N)
    # muestra en consola un modelo de la matriz
    def View(self):
        print("")
        row = ""
        k = 0
        while k < self.N:
            for elem in self.Matrix[k]:
                row += str(elem) + " "
            print(row)
            row = ""
            k += 1
        print("")
    # mueve una cantidad num hacia arriba dentro de la matriz
    def Up(self, num):
        self.pos_row -= num
        if not (0 < self.pos_row < self.N-1):
            self.pos_row = self.pos_row % self.N
    # mueve una cantidad num hacia abajo dentro de la matriz
    def Down(self, num):
        self.pos_row += num
        if not (0 < self.pos_row < self.N-1):
            self.pos_row = self.pos_row % self.N
    # mueve una cantidad num hacia la derecha dentro de la matriz
    def Right(self, num):
        self.pos_column += num
        if not (0 < self.pos_column < self.N-1):
            self.pos_column = self.pos_column % self.N
    # mueve una cantidad num hacia la izquierda dentro de la matriz
    def Left(self, num):
        self.pos_column -= num
        if not (0 < self.pos_column < self.N-1):
            self.pos_column = self.pos_column % self.N
    # aumenta en 1 el valor actual
    def A(self):
        self.Matrix[self.pos_row][self.pos_column] += 1
    # disminuye en 1 en valor actual 
    def B(self):
        self.Matrix[self.pos_row][self.pos_column] -= 1
    # multiplica el valor actual por el valor en la direccion dir 
    def X(self, dir):
        x = self.pos_column
        y = self.pos_row
        
        newCoordinates = getNew_XY(x,y, dir, self.N)
        x = newCoordinates[0]
        y = newCoordinates[1]

        self.Matrix[self.pos_row][self.pos_column] *= self.Matrix[y][x]
    # multiplica el valor actual por el valor en la direccion dir 
    def Y(self, dir):
        x = self.pos_row
        y = self.pos_column

        newCoordinates = getNew_XY(x,y, dir, self.N)
        x = newCoordinates[0]
        y = newCoordinates[1]

        self.Matrix[self.pos_row][self.pos_column] //= self.Matrix[y][x]
    # muestra por pantalla el valor ASCII actual 
    def LogASCII(self):     # Lc
        Value = self.Matrix[self.pos_row][self.pos_column]
        print(chr(Value), end='')
    # muestra por pantalla el valor numerico actual
    def LogValue(self):     # Le
        Value = self.Matrix[self.pos_row][self.pos_column]
        if Value > 0:
            print(Value, end='')
        else:
            print("No se pudo imprimir, valor menor a 0")
    # reinicia el valor actual a 0
    def R(self):
        self.Matrix[self.pos_row][self.pos_column] = 0
    # reinicia todos los valores de la matriz a 0 
    def Z(self):
        i = 0
        j = 0
        while i < N:
            while j < N:
                self.Matrix[i][j] = 0
                j += 1
            i += 1
            j = 0
    # muestra por pantalla todos los valores de la matriz, en formato ASCII (32-127) 
    def ViewASCII(self):        # Sc
        i = 0
        j = 0
        output = ''
        while i < N:
            while j < N:
                if 32 < self.Matrix[i][j] < 127:
                    output += chr(self.Matrix[i][j])
                j += 1
            i += 1
            j = 0
        print(output, end='')
    # muestra por pantalla todos los valores de la matriz  
    def ViewValue(self):         # Se
        i = 0
        j = 0
        output = ''
        while i < N:
            while j < N:
                if self.Matrix[i][j] >= 0:
                    output += str(self.Matrix[i][j])
                j += 1
            i += 1
            j = 0
        print(output, end='') 
    '''
    get_Value
    ———————–
    dir : str  
    ————————
    Retorna el valor de la matriz en la direccion dir (con respecto a la actual) '''
    def get_Value(self, dir):
        x = self.pos_column
        y = self.pos_row

        newCoordinates = getNew_XY(x,y, dir, self.N)
        x = newCoordinates[0]
        y = newCoordinates[1]

        value = self.Matrix[y][x]
        return value
    '''
    get_Value
    ———————–
    sin parametros 
    ————————
    Retorna la posicion actual '''
    def position(self):
        return (self.pos_row, self.pos_column)

#########################
#  lectura de archivo   #
#########################

with open('codigo.txt', 'r') as f:
    N = int(f.readline())  
    Matrix = MatrixClass(N)
    ErrorFile = open('errores.txt','w')
    No_Error = True
    line_number = 1

    for line in f:
        line = line.strip()

        Commands = Compiler(line)

        if Commands:
            ProcessCommands(Commands, Matrix)
        else:
            No_Error = False
            ErrorFile.write(str(line_number) + ' ' + line + "\n")

        line_number += 1
    if No_Error:
        ErrorFile.write("No hay errores! :D")
