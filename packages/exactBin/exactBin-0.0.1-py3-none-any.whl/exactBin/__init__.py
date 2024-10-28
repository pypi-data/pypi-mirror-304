class binVal:
    def __init__(self, val='0'):
        self.val=val
        self.isCorrect()
    def isCorrect(self):
        if type(self.val)!=str:raise TypeError('Value is not a string.')
        if len(self.val.split('.'))>2:raise Exception('Value must have 1 or less dots. Not '+str(len(self.val.split('.'))-1))
        for digit in self.val:
            if digit!='0' and digit!='1' and digit!='.':
                raise Exception('Value contains other character than: "0", "1", "."')
    def getFloat(self):
        self.isCorrect()
        try:
            precision=len(self.val.split('.')[1])
        except IndexError:
            precision=-1
        out=0
        for idx, digit in enumerate(self.val.replace('.', '')):
            out+=int(digit)*2**(len(self.val)-idx-precision-2)
        return(out)
    def setDecValue(self, number, precision=30, clip=True): #Function made using ChatGPT
        # Split the number into integer and fractional parts
        integer_part = int(number)
        fractional_part = number - integer_part
        # Convert the integer part to binary
        integer_binary = ""
        if integer_part == 0:
            integer_binary = "0"
        else:
            while integer_part > 0:
                integer_binary = str(integer_part % 2) + integer_binary
                integer_part //= 2
        # Convert the fractional part to binary
        fractional_binary = ""
        while len(fractional_binary) < precision and (fractional_part > 0 or not(clip)):
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_binary += str(bit)
            fractional_part -= bit
        # Combine integer and fractional parts
        if fractional_binary:
            self.val=f"{integer_binary}.{fractional_binary}"
        else:
            self.val=integer_binary