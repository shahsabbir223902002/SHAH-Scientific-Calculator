import pygame
import math

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 420, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHAH Scientific Calculator")

# ---------------- STATES ----------------
dark_mode = False
angle_mode = "DEG"
memory = 0.0
expression = ""

# ---------------- COLORS ----------------
def theme():
    return {
        "bg": (30, 30, 30) if dark_mode else (235, 235, 235),
        "display": (0, 0, 0) if dark_mode else (255, 255, 255),
        "text": (0, 255, 120) if dark_mode else (0, 0, 0),
        "btn": (60, 60, 60) if dark_mode else (200, 200, 200),
        "border": (120, 120, 120) if dark_mode else (90, 90, 90)
    }

# ---------------- FONTS ----------------
font = pygame.font.SysFont("Consolas", 20)
display_font = pygame.font.SysFont("Consolas", 30)


# ---------------- TITLE ANIMATION ----------------
title_font = pygame.font.SysFont("Consolas", 24, bold=True)
title_x = 20
title_dir = 1


# ---------------- MATH FUNCTIONS ----------------
def sin_func(x):
    return math.sin(math.radians(x)) if angle_mode == "DEG" else math.sin(x)

def cos_func(x):
    return math.cos(math.radians(x)) if angle_mode == "DEG" else math.cos(x)

def tan_func(x):
    return math.tan(math.radians(x)) if angle_mode == "DEG" else math.tan(x)

def root_func(x, n):
    return x ** (1 / n)

# ---------------- SAFE CALCULATE ----------------
def calculate(exp):
    try:
        exp = exp.replace("^", "**")
        allowed = {
            "sin": sin_func,
            "cos": cos_func,
            "tan": tan_func,
            "sqrt": math.sqrt,
            "root": root_func,
            "log": math.log10,
            "ln": math.log,
            "pi": math.pi,
            "e": math.e
        }
        return str(eval(exp, {"__builtins__": None}, allowed))
    except:
        return "Error"

# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, t):
        pygame.draw.rect(screen, t["btn"], self.rect, border_radius=6)
        pygame.draw.rect(screen, t["border"], self.rect, 2, border_radius=6)
        txt = font.render(self.text, True, t["text"])
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------------- BUTTON LAYOUT ----------------
layout = [
    ["MC","MR","M+","M-"],
    ["sin","cos","tan","^"],
    ["√","ⁿ√","ln","/"],
    ["7","8","9","*"],
    ["4","5","6","-"],
    ["1","2","3","+"],
    ["0",".","=","C"],
    ["(",")","MODE","THEME"]
]

buttons = []
bw, bh = 90, 55
for r, row in enumerate(layout):
    for c, txt in enumerate(row):
        buttons.append(Button(20 + c*bw, 160 + r*bh, bw-10, bh-10, txt))

# ---------------- INPUT HANDLER ----------------
def handle_input(value):
    global expression, memory, angle_mode, dark_mode

    if value == "=":
        while expression.count("(") > expression.count(")"):
            expression += ")"
        expression = calculate(expression)

    elif value == "C":
        expression = ""

    elif value == "MODE":
        angle_mode = "RAD" if angle_mode == "DEG" else "DEG"

    elif value == "THEME":
        dark_mode = not dark_mode

    elif value == "M+":
        try: memory += float(calculate(expression))
        except: pass

    elif value == "M-":
        try: memory -= float(calculate(expression))
        except: pass

    elif value == "MR":
        expression += str(memory)

    elif value == "MC":
        memory = 0.0

    elif value == "√":
        expression += "sqrt("

    elif value == "ⁿ√":
        expression += "root("

    elif value in ["sin","cos","tan","ln"]:
        expression += value + "("

    else:
        if len(expression) < 40:
            expression += value

# ---------------- MAIN LOOP ----------------
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    t = theme()
    screen.fill(t["bg"])

    # ----- Animated Title -----
    title_x += 0.4 * title_dir
    if title_x > 40 or title_x < 20:
        title_dir *= -1

    title_color = (0, 255, 120) if dark_mode else (0, 120, 200)
    title_text = title_font.render("SHAH Scientific Calculator", True, title_color)
    screen.blit(title_text, (title_x, 5))

    # ----- Display -----
    pygame.draw.rect(screen, t["display"], (20, 40, 380, 80), border_radius=8)
    pygame.draw.rect(screen, t["border"], (20, 40, 380, 80), 2)

    screen.blit(display_font.render(expression[-20:], True, t["text"]), (30, 65))
    screen.blit(font.render(angle_mode, True, t["text"]), (350, 125))

    # ----- Buttons -----
    for b in buttons:
        b.draw(t)

    # ----- Events -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                if b.clicked(event.pos):
                    handle_input(b.text)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                handle_input("=")
            elif event.key == pygame.K_BACKSPACE:
                expression = expression[:-1]
            else:
                expression += event.unicode

    pygame.display.update()

pygame.quit()

