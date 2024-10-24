# local
from .framerate import FrameRate


INVALID_DISPLAY_TIMECODE = "--:--:--:--"
INVALID_FULL_TIMECODE = "--:--:--:--:--"

# Timecode formats
FormatTimecode = 0
FormatAvid = 1
FormatDuration = 2
FormatFull = 3

class Timecode:
    """Class to wrap a FLOW timecode"""

    

    def __init__(self, h=0, m=0, s=0, f=0, fr=FrameRate()):
        self.frameRate = fr
        self.hours = h
        self.minutes = m
        self.seconds = s
        self.frames = f

        # ensure the passed values are sane
        self.hours %= 24
        assert (
            self.minutes <= 59
            and self.seconds <= 59
            and self.frames < self.frameRate.nearestWholeFps()
        ), "Timecode: invalid initial values for timecode: %s, %s, %s, %s, %s" % (
            h,
            m,
            s,
            f,
            fr,
        )

    def __isub__(self, rhs):
        if isinstance(rhs, Timecode):
            self = self.fromFrameCount(
                self.totalFrames() - rhs.totalFrames(), self.frameRate
            )
        elif type(rhs) == int:
            self = self.fromFrameCount(self.totalFrames() - 1, self.frameRate)

        return self

    def __sub__(self, rhs):
        result = self
        result -= rhs

        return result

    def __iadd__(self, rhs):
        if isinstance(rhs, Timecode):
            self = self.fromFrameCount(
                self.totalFrames() + rhs.totalFrames(), self.frameRate
            )
        elif type(rhs) == int:
            self = self.fromFrameCount(self.totalFrames() + 1, self.frameRate)

        return self

    def __add__(self, rhs):
        result = self
        result += rhs
        return result

    def __eq__(self, rhs):
        return (
            self.frameRate == rhs.frameRate
            and self.hours == rhs.hours
            and self.minutes == rhs.minutes
            and self.seconds == rhs.seconds
            and self.frames == rhs.frames
        )

    def setFrameRate(self, fr):
        assert isinstance(fr, FrameRate), "Timecode::setFrameRate: passed non framerate"
        self.frameRate = fr

    def isNull(self):
        return self.frameRate.isNull()

    def toString(self, fmt=FormatTimecode):
        if fmt == FormatTimecode or fmt == FormatFull:
            if (
                self.hours >= 0
                and self.minutes >= 0
                and self.seconds >= 0
                and self.frames >= 0
            ):
                tc_string = "%02i:%02i:%02i:%02i" % (
                    self.hours,
                    self.minutes,
                    self.seconds,
                    self.frames,
                )

                if fmt == FormatFull:
                    tc_string += ":" + self.frameRate.toRationalString()
                return tc_string
            else:
                return INVALID_DISPLAY_TIMECODE
        elif fmt == FormatAvid:
            # separators from apiMXFixer.h:
            sep = "/"
            # 25fps
            if self.frameRate.num == 30000:
                if self.frameRate.isDropFrame():
                    sep = ";"  # 30 fps drop frame
                else:
                    sep = ":"  # 30 fps non drop frame
            elif self.frameRate.num == 24:
                sep = "+"
                # 24 fps

            return "%02i:%02i:%02i%s%02i" % (
                self.hours,
                self.minutes,
                self.seconds,
                sep,
                self.frames,
            )
        elif fmt == FormatDuration:
            # as a duration.  not interested in frames but want
            # to round to nearest second.
            h = self.hours
            m = self.minutes
            s = self.seconds
            if self.frames > self.frameRate.fps() / 2:
                s += 1

            if s > 59:
                s = 0
                m += 1

            if m > 59:
                m = 0
                h += 1

            chunks = []
            if h > 0:
                chunks += "%ih" % (h)
            if m > 0:
                chunks += "%im" % (m)

            chunks += "%is" % (s)

            return chunks.join(" ")

    @staticmethod
    def fromString(s, fr=None):

        result = Timecode()

        if not s:
            return result

        if s == INVALID_DISPLAY_TIMECODE or s == INVALID_FULL_TIMECODE:
            return result

        chunks = s.split(":")
        assert len(chunks) > 3, "Timecode::fromString: string is invalid: %s" % (s)

        hours = int(chunks[0])
        minutes = int(chunks[1])
        seconds = int(chunks[2])
        frames = int(chunks[3])

        if len(chunks) == 5:
            fr = FrameRate.fromRationalString(chunks[4])

        if not fr:
            return result

        if hours >= 0 and minutes >= 0 and seconds >= 0 and frames >= 0:
            result = Timecode(hours, minutes, seconds, frames, fr)

        return result

    @staticmethod
    def fromFrameCount(total, fr):
        if fr.den <= 0:
            return Timecode()

        if total < 0:
            total += (
                Timecode(23, 59, 59, fr.nearestWholeFps() - 1, fr).totalFrames() + 1
            )

        framerate = fr.nearestWholeFps()
        if fr.isDropFrame():
            # \todo: modify for other dropframe rates
            d = total / 17982
            m = total % 17982
            total += 18 * d + 2 * ((m - 2) / 1798)

        totalAsSeconds = total / framerate

        h = int(totalAsSeconds / 3600)
        m = int((totalAsSeconds - h * 3600) / 60)
        s = int(totalAsSeconds - m * 60 - h * 3600)
        f = int(total - (((h * 60) + m) * 60 + s) * framerate)

        return Timecode(h, m, s, f, fr)

    @staticmethod
    def diff(a, b):
        assert isinstance(a, Timecode) and isinstance(
            b, Timecode
        ), "Timecode::diff: parameters must be instances of Timecode"

        if a.frameRate != b.frameRate:
            return 0

        if a == b:
            return 0

        delta = (b - a).totalFrames()
        frames_in_half_day = (
            Timecode(
                11, 59, 59, a.frameRate.nearestWholeFps() - 1, a.frameRate
            ).totalFrames()
            + 1
        )

        if delta == frames_in_half_day:
            if a.hours > b.hours:
                return -delta
            return delta

        # some magic to make use of existing handling of -ve frame
        # count numbers in from frame count
        modifier = 1
        if delta > frames_in_half_day:
            modifier = -1
            delta = -delta

        return Timecode.fromFrameCount(delta, a.frameRate).totalFrames() * modifier

    @staticmethod
    def sequential(a, b):
        assert isinstance(a, Timecode) and isinstance(
            b, Timecode
        ), "Timecode::sequential: parameters must be instances of Timecode"
        return Timecode.diff(a, b) == 1

    def totalFrames(self):
        if self.isNull():
            return 0

        correction = 0
        fr = self.frameRate.nearestWholeFps()

        if self.frameRate.isDropFrame():
            totalMinutes = self.hours * 60 + self.minutes

            # \todo: modify for other dropframe rates
            correction = 2 * (totalMinutes - totalMinutes / 10)

        return (
            (((self.hours * 60) + self.minutes) * 60 + self.seconds) * fr
            + self.frames
            - correction
        )

    def __repr__(self):
        return "Timecode: %s -> %i %i %i %i %s %i" % (
            self.toString(),
            self.hours,
            self.minutes,
            self.seconds,
            self.frames,
            self.frameRate,
            self.totalFrames(),
        )


# basic test cases
if __name__ == "__main__":
    a = Timecode(1, 2, 3, 4, FrameRate(25, 1))
    b = Timecode(1, 2, 3, 5, FrameRate(25, 1))

    print(a)
    print(b)

    print("sequential: %s" % (Timecode.sequential(a, b)))
    print("diff: %s" % (Timecode.diff(a, b)))

    b -= 1
    assert a != b

    c = a + b
    print(a)
    print(b)
    print(c)

    a += b
    print(a)

    d = Timecode(0, 0, 0, 0, FrameRate(30000, 1001))
    e = Timecode(0, 0, 0, 0, FrameRate(30000, 1001))
    f = e - d
    print(d)
    print(e)
    print(f)
