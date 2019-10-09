import signal
import sys
import os
import struct
import fcntl
import termios
import shutil

from contextlib import contextmanager 

class Redraw(Exception):
    pass

class Response:
    pass

class Plaintext(Response):
    def __init__(self, lines):
        self.lines = []
        if isinstance(lines, str):
            lines = (lines,)
        for line in lines:
            self.lines.extend(line.splitlines())
    def render(self, width, height):
        return self.lines

class Document(Response):
    def __init__(self, obj):
        self.obj = obj
    def render(self, width, height):
        return self.obj.to_ansi(width=width, height=height)

class Console:
    def __init__(self, stdin, stdout, stderr):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.buf = ""

    def print(self,  *args, end="\r\n",**kwargs):
        print(*args, end=end, file=self.stdout, **kwargs)

    def flush(self):
        self.stdout.flush()

    def resize(self):
        s = struct.pack('HHHH', 0, 0, 0, 0)
        t = fcntl.ioctl(self.stdout.fileno(), termios.TIOCGWINSZ, s)
        self.height, self.width, height_px, width_px = struct.unpack('HHHH', t)

    def render(self, obj):
        self.stdout.write("\x1b[H\x1b[J")
        lines = obj.render(self.width, self.height)
        self.stdout.write("\r\n".join(line[:self.width] for line in lines))
        self.stdout.flush()

    def get_buf(self, size):
        # fix me, pastebuf > readbuf gives utf8 errors
        if not self.buf:
            self.buf = self.stdin.read()

        if self.buf:
            if not size:
                buf, self.buf = self.buf, ""
            else:
                buf, self.buf = self.buf[:size], self.buf[size:]
            return buf

    def peek(self):
        if not self.buf:
            self.buf = self.stdin.read()
        return self.buf

    def get_event(self):
        buf = self.get_buf(1)
        if not buf:
            return None
        if buf == "\x1b":
            p = self.peek()
            if p.startswith("\x1b"):
                return Event("escape", None)

            line = self.get_buf(2)
                
            if not line:
                return Event("escape", None)
            if line == "\x1b":
                return Event("escape", None)

            if line == "[A" or line == "OA":
                return Event("up", None)
            elif line == "[B" or line == "OB":
                return Event("down", None)
            elif line == "[C" or line == "OC":
                return Event("right", None)
            elif line == "[D" or line == "OD":
                return Event("left", None)
            elif line == "[M":
                # mouse event
                modifier, x, y = [ord(x) for x in self.get_buf(3)]
                x -= 32
                y -= 32
                if modifier & 96 == 96:
                    if modifier  & 1:
                        action = "scroll-down"
                    else:
                        action = "scroll-up"
                elif modifier & 64:
                    action = [
                        "left-drag",
                        "middle-drag",
                        "right-drag",
                        "move", 
                    ][modifier & 3]
                else:
                    action = [
                        "left-click",
                        "middle-click",
                        "right-click",
                        "mouse-up", 
                    ][modifier & 3]

                attrs = {
                    'action': action,
                    'x': x,
                    'y':y,
                    'meta': (modifier &8 == 4),
                    'ctrl': (modifier &16 == 16),
                    'shift': (modifier &4 == 4),
                }
                # selection mode 
                # if action == "left-click":
                #    sys.stdout.write('\x1b[1;1;1;25~')
                return Event("mouse", attrs)
            elif line == "[2":
                # paste event
                line = self.get_buf(3)
                if line == "00~":
                    line = self.get_buf(None)
                    if "\x1B[201~" not in line:
                        raise Exception('missing')
                    pos = line.find("\x1B[201~")
                    e = Event("paste", line[:pos])
                    self.buf = line[pos+6:]
                    return e
                return Event('unknown', buf+line)
            else:
                return Event('unknown', buf+line)
        elif buf == "\x1A": # ^Z
            return Event("suspend", None)
        elif buf == "\x03": # ^C
            return Event("interrupt", None)
        else:
            return Event("text", buf)
        
class LineConsole(Console):
    width = 80
    height = 24
    def resize(self):
        self.width, self.height = shutil.get_terminal_size((self.width, self.height))

    def render(self, obj):
        lines = obj.render(self.width, self.height)
        out = "\r\n".join(lines)
        self.stdout.write(out)
        if not out.endswith("\n"):
            self.stdout.write("\n")
        self.stdout.flush()

    def get_event(self):
        return None

class Event:
    def __init__(self, name, value):
        self.name = name
        self.value = value

@contextmanager
def tty(stdin, stdout, stderr, bracketed_paste=True):
    fd = stdin.fileno()

    # [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
    
    old_term = termios.tcgetattr(fd)
    new_term = termios.tcgetattr(fd)
    
    new_term[0] &= ~( 
        termios.BRKINT | # break conditions send SIGINT
        termios.ICRNL |    # Transform ^M into \n
        termios.INPCK |    # Parity checks
        termios.ISTRIP |   # 8bit
        termios.IXON |     # ^S ^Q
        0
    )
    # linux: new_term[0] &= termios.IUTF8

    new_term[1] &= ~(termios.OPOST); # Turn \n into \r\n in output
    new_term[2] |= (termios.CS8);    # 8 Bit wide
    new_term[3] &= ~(
        termios.ECHO |  # Echo characters
        termios.ICANON | # When set, line at a time, when cleared, Byte at a type
        termios.IEXTEN | # ^O ^V Special keys
        termios.ISIG | # ^C ^Z 
        0
    )
    # Dont wait for input
    new_term[-1][termios.VMIN] = 0
    new_term[-1][termios.VTIME] = 1

    def resizeHandler(signum, frame):
        raise Redraw()

    def resumeHandler(signum, frame):
        set_term()

    def stopHandler(signum, frame):
        clear_term()
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)
        os.kill(0, signal.SIGTSTP)
        signal.signal(signal.SIGTSTP, stopHandler)

    def set_term():
        stdout.buffer.write(b"\x1B[?2004h") # bracketed paste
        stdout.buffer.write(b'\x1B[?1005h') # utf-8 mouse mode
        stdout.buffer.write(b'\x1B[?1003h') # any tracking
        stdout.buffer.write(b'\x1B[?1049h') # alt screen
        stdout.buffer.write(b'\x1B[?1h') # DECCKM keyboard mode
        stdout.buffer.flush()

        termios.tcsetattr(fd, termios.TCSADRAIN, new_term)

        stdout.flush()

    def clear_term():
        termios.tcsetattr(fd, termios.TCSADRAIN, old_term)
        stdout.buffer.write(b"\x1B[?2004l") # bracketed paste
        stdout.buffer.write(b'\x1b[?1003l')
        stdout.buffer.write(b'\x1b[?1005l')
        stdout.buffer.write(b'\x1b[?1049l')
        stdout.buffer.write(b'\x1b[?1l')
        stdout.buffer.flush()

    try:
        signal.signal(signal.SIGWINCH, resizeHandler)
        signal.signal(signal.SIGCONT, resumeHandler)
        signal.signal(signal.SIGTSTP, stopHandler)
        set_term()

        yield Console(stdin, stdout, stderr)
    finally:
        clear_term()

class Box:
    def render(self, width, height):
        width = width-5 or 80
        height = height*2 or 24
        output = ["     +"+("-"*(width-10))+"+"]
        for _ in range(height-2):
            output.append("     |"+(" "*(width-10))+"| "+ str(_))
        output.append("     +"+("-"*(width-10))+"+")
        return output

class Viewport:
    def __init__(self, obj, line=0):
        self.obj = obj
        self.width, self.height = None, None
        self.buf = []
        self.line = line

    def render(self, width, height):
        if self.width != width or self.height != height:
            self.width, self.height = width, height
            self.buf = self.obj.render(width, height)
            self.line = min(self.line, len(self.buf))

        return self.buf[self.line:self.line+height]

    def up(self, n=1):
        if self.line > 0:
            self.line = max(0, self.line -n) 
            return True
        else:
            self.line = 0
            return False

    def down(self, n=1):
        top = max(0, len(self.buf) - self.height)
        if self.line < top:
            self.line = min(self.line +n, top)
            return True
        else:
            self.line = top
            return False


def pager(obj, *, use_tty=True):
    if use_tty and sys.stdin.isatty() and sys.stdout.isatty():
        with tty(sys.stdin, sys.stdout, sys.stderr) as console:
            running = True
            viewport = Viewport(obj, 0)
            while running:
                try:
                    console.resize()
                    console.render(viewport)
                    while running:
                        e = console.get_event()
                        if e:
                            if e.name == "interrupt":
                                console.print()
                                running = False
                                break
                            elif e.name == "text" and e.value == "q":
                                running = False
                                break
                            elif e.name == "suspend":
                                os.kill(0, signal.SIGTSTP)
                                break
                            elif e.name == "up":
                                if viewport.up():
                                    console.render(viewport)
                            elif e.name == "down":
                                if viewport.down():
                                    console.render(viewport)
                            elif e.name == "text" and e.value == "\x00":
                                if viewport.up(console.height):
                                    console.render(viewport)
                            elif e.name == "text" and e.value == " ":
                                if viewport.down(console.height):
                                    console.render(viewport)
                            else:
                                console.print("\r", e.name, repr(e.value), end="")
                                console.flush()
                                
                                
                except Redraw:
                    pass
    else:
        console = LineConsole(sys.stdin, sys.stdout, sys.stderr)
        console.resize()
        console.render(obj)

def main(name, argv=None, env=None):
    if name != '__main__': return

    argv = sys.argv[1:] if argv is not None else argv
    env = os.environ if env is not None else os.environ

    obj = Box()
    pager(obj)


main(__name__)
