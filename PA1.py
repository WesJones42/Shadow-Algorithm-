import math
import numpy as np
import argparse



count = 0

def getArgs() :
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type = str, help = 'File containing terrain')
    
    parser.add_argument('h', type = float, help = 'h value')
    
    parser.add_argument('theta', type = float, help = 'Angle of elevation for Sun')
    parser.add_argument('algorithm', type = str, help = 'naive | early | fast')
    return parser.parse_args()

def compare(x,y):
    global count
    count += 1
    if abs(x-y) < .000000000001 :
        return False
    if x < y :
        return True
    else:
        return False

def print_shade(boolean_array):
    for row in boolean_array:
        for column in row:
            if column == True:
                print ('*    ', end = '')
            elif column == False:
                print ('0    ', end = '')
        print('\n')
        
def read2Dfloat(fileName) : # read CSV of floats into 2D array
    array2D = []
    # Read input file
    f = open(fileName, "r")
    data = f.read().split('\n')
    
    # Get 2-D array
    for row in data[0:-1]:
        float_list = list(map(float, row.split(',')[0:-1]))
        array2D.append(float_list)

    return array2D

def runTest(args, terrain = None) :

    
    # Initialize counter
    global count
    count = 0

    theta = np.deg2rad(args.theta)
    
    if terrain == None :
      terrain = read2Dfloat(args.input_file)

    N     = len(terrain)
    shade = [[False] * N for i in range(N)]

    if args.algorithm == 'naive':
        result = naive(terrain, args.h, theta, N, shade)
    elif args.algorithm == 'early':
        result = earlyexit(terrain, args.h, theta, N, shade)
    elif args.algorithm == 'fast':
        result = fast(terrain, args.h, theta, N, shade)

    return result



def Equate(y,x,h,image,N,i):
#    print(x,",",y)
    j = image[y][x]
    k = image[y][x+i]

    foo = k-j
    poo = ((x-(x+i))*h)
    x = foo/(poo)
    return x
    
def naive(image,h,angle,N,shade):
    
###### Complete this function
    for Y in range(N):
  #      print(image[Y][0])
        for X in range(N):
            i = -1
            for l in range(X):
                x = Equate(Y,X,h,image,N,i)
                i = i-1
                if(compare(math.tan(angle),x)):
                    shade[Y][X] = 1                 
    return shade

def earlyexit(image,h,angle, N, shade):
    
###### Complete this function
    for Y in range(N):
        for X in range(N):
            i = -1
            for l in range(X):
                x = Equate(Y,X,h,image,N,i)
                i = i-1
                if(compare(math.tan(angle),x)):
                    shade[Y][X] = 1
                    break
                    

    return shade

def fast(image,h,angle, N, shade):

###### Complete this function
    for Y in range(N):
        for X in range(N-1):
            if shade[Y][X] == 1:
                continue
            x = Equate(Y,X,h,image,N,1)
            i = 1
            while(compare(math.tan(angle),x)):
                shade[Y][X+i] = 1
                if (X+i) == N-1:
                    break
                i = i+1
                x = Equate(Y,X,h,image,N,i)
            
    
    return shade
    
if __name__ == '__main__':
    

    answer = runTest(getArgs())
    print_shade(answer)
    print('Number of comparisons: ' + str(count))
