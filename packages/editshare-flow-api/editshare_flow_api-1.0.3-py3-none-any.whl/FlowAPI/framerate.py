"""Framerate module"""
import math


class FrameRate:
    def __init__(self, num=-1, den=-1, drop=False):
        self.num = num
        self.den = den
        self.drop = drop

    def __eq__(self, rhs):
        return self.num == rhs.num and self.den == rhs.den and self.drop == rhs.drop

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    def isNull(self):
        return self.den <= 0 or self.num <= 0

    def toString(self):
        return self.toFpsString()

    def toFpsString(self):
        result = "%3.4f" % (float(self.num) / self.den)
        while result.endswith("0") or result.endswith("."):
            result = result[: len(result) - 1]

        return result

    def toRationalString(self):
        result = "%i/%i" % (self.num, self.den)
        if (not self.isIntegerFrameRate()) and (not self.drop):
            result += " nd"

        return result

    def fps(self):
        if self.den == 0:
            return 0

        return self.num / self.den

    def isIntegerFrameRate(self):
        if self.den == 0 or self.num == 0:
            return False

        EPSILON = 0.001
        return math.fmod(self.num, self.den) < EPSILON

    def nearestWholeFps(self):
        result = self.num / self.den
        if not self.isIntegerFrameRate():
            result += 1

        return result

    def isDropFrame(self):
        return self.drop

    def __repr__(self):
        return "FrameRate: (%i, %i), drop: %s" % (self.num, self.den, self.drop)

    @staticmethod
    def fromRationalString(s):
        split = s.split("/")
        assert (
            len(split) == 2
        ), "FrameRate::fromRationalString: found a malformed string: %s" % (s)

        num = split[0]
        den = split[1]

        # check for drop frame
        drop = True
        if "nd" in den.lower():
            drop = False
            den = den.split(" ")[0]

        result = FrameRate(int(num), int(den))

        if drop and result.isIntegerFrameRate():
            drop = False

        result.drop = drop

        return result


# basic test cases
if __name__ == "__main__":
    pal = FrameRate(25, 1)
    ntsc = FrameRate(30000, 1001, True)
    print(pal, ntsc)
    print(pal.toFpsString(), pal.toRationalString())
    print(ntsc.toFpsString(), ntsc.toRationalString())

    print(FrameRate.fromRationalString("25/1"))
    print(FrameRate.fromRationalString("30000/1001"))
    print(FrameRate.fromRationalString("30000/1001 nd"))
