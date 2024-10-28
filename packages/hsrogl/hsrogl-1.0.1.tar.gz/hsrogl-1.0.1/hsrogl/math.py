
###############################
# hsrogl.math     Make by H.S.S.
###############################

class ClassInfo():
    def main(self):
        return ["hsrogl.math","Make by H.S.S.","3582930858@qq.com","License: HSCDL","Cannot edit and update"]

def inf():
    return float('inf')

def subinf():
    return float('-inf')

def nan():
    return float('inf')*0

def pi():
    return 3.1415926

def extpi():
    return 3.14159265358979323

def e():
    return 2.718282

def sqrt(num:eval):
        onum=num**0.5
        return onum

def exp10(num):
    return 10**num

def cuberoot(num:eval):
        x=1
        while abs(x**3-num) > 1e-7:
            x=(2*x/3)+num/3/x/x
        return x

def fib(num):
    lis=[]
    i=0
    while i<num:
        if i==0 or i==1:
            lis.append(1)
        else:
            lis.append((lis[i-2]+lis[i-1]))
        i+=1
    return lis

def add(x,y):
    return x+y

def mul(x,y):
    return x*y

def sub(x,y):
    return x-y

def div(x,y):
    return x/y

def lossdiv(x,y):
    return x%y

def pow(x,y):
        num=x**y
        return num

def round(num):
        a=round(num)
        return a

def f_abs(num):
    a = abs(num)
    return a

def guess_abs(num):
    if num<0:
        pass
    else:
        return [num,-num]

def tau():
    return pi()*2

def exttau():
    return extpi()*2

def nulltype():
    return None

def falsetype():
    return False

def truetype():
    return True

def expressif(express):
    if express==True:
        return True
    elif express==False:
        return False
    elif express==None:
        return None
    else:
        return 0
def factorial(num):
    a=1
    for i in range(1,num+1):
        a*=1
    return a

def sum(*num):
    res=0
    for ax in num:
        res+=ax
    return res

def exp2(num):
    return 2**num

def exp(num):
    return e()**num

def lnum(*num:int):
    e=[]
    for i in num:
       e.append(i)
    return e

def square2(x,y):
    return (x+y)*2

def square3(x,y):
    return x*y

def triangle2(x,y,z):
    return x+y+z

def triangle3(x,y):
    return (x*y)/2

def sin(x,x_0=0):
    term1 = x
    term2 = -(x ** 3 / 6.0)
    return term1 + term2

def cos(x, x_0=0):
    term1 = 1
    term2 = -(x ** 2 / 2.0)
    return term1 + term2

def tan(x):
    cos_x = cos(x)
    if abs(cos_x) < 1e-7:  # 设定一个较小的阈值来判断cos(x)是否接近于零
        print("ValueWarning: cos(x) is close to zero, may cause division by zero!")
        return float('inf') if cos_x > 0 else float('-inf')
    return sin(x) / cos_x

def pidiv2():
    return pi()/2

def extpidiv2():
    return extpi()/2

def trkpidiv2():
    return 1.5707963267948966

def acos(x, tol=1e-10, max_iter=100):
    def cos_approx(x):
        return 1 - x ** 2 / 2
    #使用牛顿-拉弗森法计算反余弦的近似值。

    #参数:
    #x -- 余弦值，范围应在[-1, 1]之间。
    #tol -- 近似解的容差，默认为1e-10。
    #max_iter -- 最大迭代次数，默认为100。

    #返回:
    #反余弦的近似值，单位为弧度。

    if x < -1 or x > 1:
        raise ValueError("x must be in the range [-1, 1].")

    if x == 1:
        return 0
    # 初始猜测值，当x接近1时，θ接近0；x接近-1时，θ接近π
    guess = 0 if x >= 0 else pi()  # π的近似值

    for _ in range(max_iter):
        # 牛顿迭代公式：x_n+1 = x_n - f(x_n)/f'(x_n)，其中f(θ) = cos(θ) - x
        # f'(θ) = -sin(θ)，但为了减少sin计算，我们使用cos(θ)的导数-sqrt(1-cos^2(θ))
        guess = guess - ((cos_approx(guess) - x) / (-sqrt(1 - x ** 2)))  # 使用cos的近似值

        # 检查是否达到容差要求
        if abs(cos_approx(guess) - x) < tol:
            break

    return guess


def asin(x, tol=1e-10, max_iter=100):
    def sin_approx(x):
        return x
    if x == 1:
        return 0
    #使用牛顿-拉弗森法计算反正弦的近似值。

    #参数:
    #x -- 正弦值，范围应在[-1, 1]之间。
    #tol -- 近似解的容差，默认为1e-10。
    #max_iter -- 最大迭代次数，默认为100。

    #返回:
    #反正弦的近似值，单位为弧度。

    if x < -1 or x > 1:
        raise ValueError("x must be in the range [-1, 1].")

    # 初始猜测值，当x接近0时，θ接近0；x接近1或-1时，θ接近π/2或-π/2
    guess = 0 if abs(x) < 1 else sin_approx(x) * 1.5707963267948966  # π/2的近似值

    for _ in range(max_iter):
        # 牛顿迭代公式：x_n+1 = x_n - f(x_n)/f'(x_n)，其中f(θ) = sin(θ) - x
        # f'(θ) = cos(θ)，但为了减少cos计算，我们可以直接利用sin^2 + cos^2 = 1的关系
        guess = guess - ((sin_approx(guess) - x) / sqrt(1 - x ** 2))  # 使用sin的近似值

        # 检查是否达到容差要求
        if abs(sin_approx(guess) - x) < tol:
            break

    return guess


def atan(x, tolerance=1e-10):
    def tan_approx(theta):
        return theta  # 这个近似只在θ接近0时有效，对于较大角度会非常不准确
    #使用弦割法计算反正切的近似值。

    #参数:
    #x -- 要计算反正切的值。
    #tolerance -- 计算结果的容差，默认为1e-10。

    #返回:
    #反正切的近似值，单位为弧度。

    if x == 0:
        return 0  # atan(0) = 0
    elif x > 0:
        a, b = -0.7853981633974483, 0.7853981633974483  # -π/4 和 π/4 的近似值
    else:
        a, b = 0.7853981633974483, -0.7853981633974483  # 对于负数，翻转a和b的值

    while (b - a) / 2 > tolerance:
        midpoint = (a + b) / 2
        if tan_approx(midpoint) < x:  # 使用tan的近似计算，此处需要自定义tan函数
            a = midpoint
        else:
            b = midpoint

    return (a + b) / 2

def ceil(number):
    return int(number) if number >= 0 else int(number) - ((number * 10) % 10 > 0)

def comb(n, k):
    # 初始化结果为1（因为从n个元素中选择0个或n个的组合都是1）
    result = 1

    # 当k大于n-k时，我们可以优化计算，因为C(n, k) == C(n, n-k)
    if k > n - k:
        k = n - k

    # 依次计算从n到n-k+1的乘积，然后除以从1到k的乘积
    for i in range(1, k + 1):
        result *= n - (k - i)
        result //= i  # 使用整除，确保结果始终是整数

    return result

def copysign(x, y):
    # 如果y是正数或者零，返回x的绝对值
    # 如果y是负数，返回x的相反数（即-x）
    return x if y >= 0 else -x

def phi():
    return 1.618

def floor(x):
    # 如果x已经是整数，直接返回x
    if x.is_integer():
        return int(x)
    # 如果x是负数，需要考虑它的小数部分
    elif x < 0:
        return int(x) if x == int(x) else int(x) - 1
    # 对于非负数，直接取整即可去掉小数部分
    else:
        return int(x)

def gcd(a, b):
    # 确保a和b都是非负整数
    if a<0 or b<0:
        return 0
    else:
        a, b = abs(a), abs(b)

def mul100(num):
    return num*100

def mul1000(num):
    return num*1000

def frexp(x):
    # 处理特殊情况
    if x == 0.0:
        return (0, 0)

    # 计算x的二进制表示，并分离出符号位、指数部分和尾数部分
    # Python没有直接操作浮点数二进制的方法，所以我们采用间接方式
    # 首先，获取x的指数（e）和尾数（m），使得 x = m * 2^e
    e = 0
    while x >= 2.0:
        x /= 2.0
        e += 1
    while x < 1.0:
        x *= 2.0
        e -= 1

    # 确保尾数在[0.5, 1)之间
    m = x * 2

    # 返回阶码（需要调整，因为上面的操作改变了阶码）和尾数
    # 注意这里的阶码是基于2的，且比IEEE 754标准中的阶码小1
    return (e - 1, m)


def fsum(iterable):

    #使用Kahan求和算法计算浮点数序列的和，以提高精度。

    #:param iterable: 浮点数的可迭代序列
    #:return: 浮点数序列的和，具有较高的精度

    sum = 0.0  # 总和
    c = 0.0  # 补偿项，用于修正误差
    for num in iterable:
        y = num - c  # 减去前一轮的误差
        t = sum + y  # 计算临时和
        c = (t - sum) - y  # 计算并存储新的误差
        sum = t  # 更新总和
    return sum


def lcm(a, b):

    #计算两个整数的最小公倍数（Least Common Multiple, LCM）。

    #:param a: 第一个整数
    #:param b: 第二个整数
    #:return: 两个整数的最小公倍数

    return abs(a * b) // gcd(a, b)


def lslcm(numbers):

    #计算一个整数列表的最小公倍数。

    #:param numbers: 整数列表
    #:return: 列表中所有整数的最小公倍数

    result = 1
    for num in numbers:
        result = lcm(result, num)
    return result

def ldexp(x,n):
    return x * (1 << n)

def modf(x):
    int_part = int(x)
    frac_part = x - int_part
    return frac_part, int_part

def pow10(x):return x ** 10
def pow2(x):return x ** 2
def pow3(x):return x ** 3
def pow4(x):return x ** 4
def pow5(x):return x ** 5
def powsub1(x):return x ** -1
def powsub2(x):return x ** -2
def powsub3(x):return x ** -3
def div10(x):return x / 10
def div2(x):return x / 2
def div3(x):return x / 3
def div5(x):return x / 5
def div100(x):return x / 100
def div1000(x):return x / 1000

def nextafter(x, direction):
    # 如果direction比x大，增加最小的正浮点数
    if direction > x:
        return x + float.fromhex('0x1p-1074')  # 这是float类型的最小正epsilon
    # 否则，如果direction比x小，减少最小的正浮点数
    else:
        return x - float.fromhex('0x1p-1074')  # 同样是最小的正epsilon

def doublepow(x,t):return x ** t ** t
def triblepow(x,t):return x ** t ** t ** t

def perm(n, m):
    # 计算n! 和 (n-m)!
    def factl(num):
        """计算阶乘"""
        result = 1
        for i in range(1, num + 1):
            result *= i
        return result
    n_factorial = factl(n)
    nm_factorial = factl(n - m)
    # 计算并返回排列数
    return n_factorial // nm_factorial


def remainder(dividend, divisor):

    #计算dividend除以divisor的余数。

    #参数:
    #dividend -- 被除数
    #divisor -- 除数

    #返回:
    #余数

    if divisor == 0:
        return 0
    remainder = dividend % divisor
    return remainder

def sumprod(list1, list2):
    return sum(x * y for x, y in zip(list1, list2))

def trunc(num):
    return int(num)

def differ(a, b):
    # 计算两个浮点数之间的差值
    difference = abs(a - b)
    return difference

def expm1(x):
    # 使用泰勒级数展开近似计算 e^x - 1
    # 这里只考虑了前三项，适用于x接近0的情况
    result = x + x ** 2 / 2 + x ** 3 / 6
    return result

def ln(x, epsilon=1e-10, max_iter=100):
    # 确保 x 是正数
    if x <= 0:
        return 0

    # 对于 x 接近 1 的情况，直接使用线性近似作为初始值
    if abs(x - 1) < 1:
        y = x - 1
    else:
        # 对于较大的 x，先计算其倒数的自然对数
        z = 1 / x
        y = -ln(z)

    # 牛顿迭代法
    for _ in range(max_iter):
        y_next = y - (y - x * pow(2.718282, -y)) / (1 + x * pow(2.718282, -y))
        if abs(y_next - y) < epsilon:  # 当迭代结果收敛时停止
            break
        y = y_next

    return y

def log1p(x):
    # 检查 x 是否在有效范围内
    if x < -1 or x >= 1:
        return 0

    # 泰勒级数展开前三项
    result = x - (x ** 2) / 2 + (x ** 3) / 3
    return result


def log2(x, epsilon=1e-10, max_iter=100):

    #计算以 2 为底 x 的对数，使用牛顿迭代法。

    #:param x: 要计算对数的正实数。
    #:param epsilon: 迭代停止的精度阈值，默认为 1e-10。
    #:param max_iter: 最大迭代次数，默认为 100。
    #:return: log2(x) 的近似值。

    if x <= 0:
        return 0

    # 初始化 y 为一个粗略估计（这里假设 x >= 1）
    y = x - 1 if x > 1 else 1

    for _ in range(max_iter):
        # 牛顿迭代公式
        y_next = y - (2 ** y - x) / (2 ** y * ln(2))

        # 如果达到足够精度，则停止迭代
        if abs(y_next - y) < epsilon:
            break

        y = y_next

    return y


def log10(x, epsilon=1e-10, max_iter=100):

    #计算以 10 为底 x 的对数，使用牛顿迭代法。

    #:param x: 要计算对数的正实数。
    #:param epsilon: 迭代停止的精度阈值，默认为 1e-10。
    #:param max_iter: 最大迭代次数，默认为 100。
    #:return: log10(x) 的近似值。

    if x <= 0:
        return 0

    # 初始化 y 为一个粗略估计（这里假设 x >= 1）
    y = x - 1 if x > 1 else 1

    for _ in range(max_iter):
        # 牛顿迭代公式，注意这里直接使用了 ln(10) 的近似值进行计算
        y_next = y - (10 ** y - x) / (10 ** y * ln(10))

        # 如果达到足够精度，则停止迭代
        if abs(y_next - y) < epsilon:
            break

        y = y_next

    return y


def eucl_dist(point1, point2):

    #计算两点间的欧氏距离。

    #:param point1: 第一个点的坐标，如 (x1, y1)。
    #:param point2: 第二个点的坐标，如 (x2, y2)。
    #:return: 两点间的欧氏距离。

    return sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))

def manh_dist(point1, point2):
    return sum(abs(p1 - p2) for p1, p2 in zip(point1, point2))

def cheb_dist(point1, point2):
    return max(abs(p1 - p2) for p1, p2 in zip(point1, point2))

def hypot(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return (dx ** 2 + dy ** 2) ** 0.5

def degrees(radians):
    pi_approx = 3.14159
    degrees = radians * 180 / pi_approx
    return degrees

def add_degrees(deg1, deg2):
    total_degrees = (deg1 + deg2) % 360  # 使用取模运算处理循环
    return total_degrees

def sub_degrees(deg1, deg2):
    total_degrees = (deg1 - deg2) % 360  # 使用取模运算处理循环
    return total_degrees

def mul_degrees(deg1, deg2):
    total_degrees = (deg1 * deg2) % 360  # 使用取模运算处理循环
    return total_degrees

def div_degrees(deg1, deg2):
    total_degrees = (deg1 / deg2) % 360  # 使用取模运算处理循环
    return total_degrees

def fdiv(x,y):
    c1=x/y
    c2=x%y
    return [c1,c2]

def radians(degrees):
    pi_approx = 3.14159
    radians = degrees * pi_approx / 180
    return radians

def intisvalid(var):
    if var==int:
        return True
    else:
        return False
def floatisvalid(var):
    if var==float:
        return True
    else:
        return False

def i():
    return -1**0.5

def nsqrt(y,x):
    return x**(1/y)

def fphi():
    return (1+5**0.5)/2

def silrad():
    return 1+2**0.5

def pythascon():
    return 2**0.5

def tetrat(x,powrange):
    for i in range(powrange):
        if i==1:
            pass
        else:
            x=x**x
    return x

def gelfondcon():
    return e()**pi()

def calatancon(b0:int=1001):
    a=1
    x=0
    for i in range(1,b0,2):
        if a==1:
            x=x+(1/i**2)
            a=0
        elif a==0:
            x=x-(1/i**2)
            a=1
        else:
            pass
    return x

def aperycon(b0:int=1001):
    x=0
    for i in range(1,b0):
        x=x+(1/i**3)
    return x

def walliscon():
    return pi()/2

def log(x,l=10, epsilon=1e-10, max_iter=100):

    #计算以 l 为底 x 的对数，使用牛顿迭代法。

    #:param x: 要计算对数的正实数。
    #:param epsilon: 迭代停止的精度阈值，默认为 1e-10。
    #:param max_iter: 最大迭代次数，默认为 100。
    #:return: log10(x) 的近似值。

    if x <= 0:
        return 0

    # 初始化 y 为一个粗略估计（这里假设 x >= 1）
    y = x - 1 if x > 1 else 1

    for _ in range(max_iter):
        # 牛顿迭代公式，注意这里直接使用了 ln(10) 的近似值进行计算
        y_next = y - (l ** y - x) / (l ** y * ln(l))

        # 如果达到足够精度，则停止迭代
        if abs(y_next - y) < epsilon:
            break

        y = y_next

    return y

def mathd_rec(true_positives, false_negatives):
    if true_positives + false_negatives == 0:
        # 防止除以0的情况
        return 0.0
    recall = true_positives / (true_positives + false_negatives)
    return recall

def cosh(x):
    def exp_approx(x, terms=100):
        result = 1.0
        term = 1.0
        for n in range(1, terms + 1):
            term *= x / n
            result += term
        return result

    ex = exp_approx(x)
    enx = exp_approx(-x)
    return (ex + enx) / 2.0

def sinh(x):
    def exp_approx(x, terms=100):
        result = 1.0
        term = 1.0
        for n in range(1, terms + 1):
            term *= x / n
            result += term
        return result
    
    ex = exp_approx(x)
    enx = exp_approx(-x)
    return (ex - enx) / 2.0

def tanh(x):
    return sinh(x) / cosh(x)

def subtype(num):
    return -num # 制造程序过于解读的关键（
    
def addtype(num):
    return +num # 制造程序过于解读的关键（

def autocalc(express):
    return eval(express)

def isnegative(num):
    if num<0:
        return True
    else:
        return False
    
def ispositive(num):
    if num>0:
        return True
    else:
        return False
    
def iszero(num):
    if num==0:
        return True
    else:
        return False
    
def zerotype():
    return 0

def format(*command):
    read=command
    a=0
    for i in range(len(read)):
        wsg=read[i]
        afterwsg=wsg.split()
        if afterwsg[0]=="c":
            if afterwsg[1]=="+":
                a=a+eval(afterwsg[2])
            elif afterwsg[1]=="-":
                a=a-eval(afterwsg[2])
            elif afterwsg[1]=="*":
                a=a*eval(afterwsg[2])
            elif afterwsg[1]=="/":
                a=a/eval(afterwsg[2])
            elif afterwsg[1]=="^":
                a=a**eval(afterwsg[2])
            elif afterwsg[1]=="&^":
                a=a**0.5
        elif afterwsg[0]=="e":
            break
        elif afterwsg[0]=="s":
            a=eval(afterwsg[1])
        elif afterwsg[0]=="f":
            if afterwsg[1]=="r":
                for j in range(int(afterwsg[2])):
                    if afterwsg[3]=="+":
                        a=a+eval(afterwsg[4])
                    elif afterwsg[3]=="-":
                        a=a-eval(afterwsg[4])
                    elif afterwsg[3]=="*":
                        a=a*eval(afterwsg[4])
                    elif afterwsg[3]=="/":
                        a=a/eval(afterwsg[4])
                    elif afterwsg[3]=="^":
                        a=a**eval(afterwsg[4])
                    elif afterwsg[3]=="&^":
                        a=a**0.5
            elif afterwsg[1]=="c":
                a=-a
        elif afterwsg[0]==":":
            pass
        else:
            raise SyntaxError(f"No command about '{afterwsg[0]}' ")
    return a

def draw(express:list=["x","x","x","x","x"],setof=[0,100,0.1]):
    import numpy as np
    import matplotlib.pyplot as plt
    #生成数据
    c=0
    x=np.arange(setof[0],setof[1],setof[2])#以0.1为单位，生成0到6的数据
    y1=eval(express[0])
    y2=eval(express[1])
    y3=eval(express[2])
    y4=eval(express[3])
    y5=eval(express[4])
    #绘制图形
    plt.rcParams['font.sans-serif']=['SimHei']#解决标题、坐标轴标签不能是中文的问题
    plt.rcParams['axes.unicode_minus']=False#标题等默认是英文输出
    plt.plot(x,y1,label="1")
    plt.plot(x,y2,label="2")
    plt.plot(x,y3,label="3")
    plt.plot(x,y4,label="4")
    plt.plot(x,y5,label="5")
    # plt.plot(x,y2,linestyle='--',label='cosx')#用虚线绘制
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Place')
    plt.legend()
    plt.show()
