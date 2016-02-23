class Metric:
    i = 0
    def __init__(self, name):
        self._Name = name
        self._N = 0
        self._Sum = 0
        self._Max = None
        self._Min = None

    @property
    def Name(self):
        return self._Name

    @property
    def N(self):
        return self._N

    @property
    def Sum(self):
        return self._Sum

    @property
    def Avg(self):
        if self.N == 0:
            return None
        return round(self.Sum / self.N, 2)

    @property
    def Max(self):
        if self._Max is None:
            return None
        return round(self._Max, 2)

    @property
    def Min(self):
        if self._Min is None:
            return None
        return round(self._Min, 2)



    def addDataPoint(self, value):
        floatValue = float(value)
        if self._N == 0:
            self._Min = floatValue
            self._Max = floatValue

        self._N += 1
        self._Sum += floatValue

        if floatValue > self._Max:
            self._Max = floatValue
        if floatValue < self._Min:
            self._Min = floatValue


        
