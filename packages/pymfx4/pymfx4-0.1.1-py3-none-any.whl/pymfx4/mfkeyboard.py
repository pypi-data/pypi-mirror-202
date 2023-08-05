"""Provides aliases, attributes and functions for simulating key-press events in the MFX_4 Terminal."""

class keyboard:
    """Provides aliases, attributes and functions for simulating key-press events in the MFX_4 Terminal."""

    def InputNumber(number):
        lst = []
        for n in str(number):
            i = ord(n) - ord('0')
        v = keyboard.Numbers[i]
        lst.append(v)
        return lst

    F1 = 91
    F2 = 92
    F3 = 93
    F4 = 94

    F1 = 1
    F2 = 2
    F3 = 3
    F4 = 4

    # Numbers = [47, 67, 68, 69, 75, 76, 77, 83, 84, 85]
    Numbers = [0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39]

    Null = Numbers[0]
    Eins = Numbers[1]
    Zwei = Numbers[2]
    Drei = Numbers[3]
    Vier = Numbers[4]
    Fuenf = Numbers[5]
    Sechs = Numbers[6]
    Sieben = Numbers[7]
    Acht = Numbers[8]
    Neun = Numbers[9]

    Alphabet = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88]
    A = Alphabet[0]
    B = Alphabet[1]
    C = Alphabet[2]
    D = Alphabet[3]
    E = Alphabet[4]
    F = Alphabet[5]
    G = Alphabet[6]
    H = Alphabet[7]
    I = Alphabet[8]
    J = Alphabet[9]
    K = Alphabet[10]
    L = Alphabet[11]
    M = Alphabet[12]
    N = Alphabet[13]
    O = Alphabet[14]
    P = Alphabet[15]
    Q = Alphabet[16]
    R = Alphabet[17]
    S = Alphabet[18]
    T = Alphabet[19]
    U = Alphabet[20]
    V = Alphabet[21]
    W = Alphabet[22]
    X = Alphabet[23]

    DEL = 8

    PRINT = 95
    LEFT = 89
    UP = 90
    RIGHT = 45
    DOWN = 42
    BLANK = 32
    SPECIALCHAR = 32
    STOP = 13

    # keys_all =[item for sublist in [F1,F2,F3,F4,Numbers,Alphabet,PRINT,LEFT,UP,RIGHT,DOWN,BLANK,SPECIALCHAR,STOP] for item in sublist]  #flatten list
    # keys_fkeysandnumeric  = [item for sublist in [F1,F2,F3,F4,Numbers] for item in sublist]  #flatten list
    KeysToDesc = {
        F1: "F1",
        F2: "F2",
        F3: "F3",
        F4: "F4",

        A: "A",
        B: "B",
        Numbers[1]: "1_C",
        Numbers[2]: "2_D",
        Numbers[3]: "3_E",
        F: "F",
        G: "G",
        H: "H",
        I: "I",
        J: "J",
        Numbers[4]: "4_K",
        Numbers[5]: "5_L",
        Numbers[6]: "6_M",
        N: "N",
        O: "O",
        P: "P",
        Q: "Q",
        R: "R",
        Numbers[7]: "7_S",
        Numbers[8]: "8_T",
        Numbers[9]: "9_U",
        V: "V",
        W: "W",
        X: "X",
        PRINT: "PRINT",
        LEFT: "LEFT",
        UP: "UP",
        Numbers[0]: "0",
        DOWN: "DOWN",
        RIGHT: "RIGHT",
        SPECIALCHAR: "SPECIALCHAR_BLANK",
        STOP: "STOP"
    }

    thelist = []

    @staticmethod
    def getKeyFromIndex(keyindex):
        return keyboard.keys[keyindex]

    @staticmethod
    def getDescFromKey(keybyte):
        try:
            ord(keybyte)
            return keyboard.KeysToDesc[keybyte]
        except:
            pass
        return keyboard.KeysToDesc[bytes([keybyte])]
