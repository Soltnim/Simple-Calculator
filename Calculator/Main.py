import pygame
import sys

# Initialize Pygame
pygame.init()
WIDTH = 1200
HEIGHT = 680
image = pygame.image.load("Assets\\Button0.png")
image_width, image_height = image.get_size()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Calculator')

currentEquation = "0"
displayedEquation = "0"

def buttonPress(buttonId:str):
    global currentEquation, displayedEquation, currentPos
    if buttonId == "=":
        try:
            displayedEquation = str(eval(currentEquation.replace("^", "**")))
            if displayedEquation.endswith(".0"):
                displayedEquation = str(int(float(displayedEquation)))
            currentEquation = displayedEquation
        except Exception as e:
            displayedEquation = "Error"
            currentEquation = "0"
            currentPos = 1
    elif buttonId == "c":
        displayedEquation = "0"
        currentEquation = "0"
        currentPos = 1
    else:
        if displayedEquation == "0" or displayedEquation == "Error":
            displayedEquation = buttonId
            currentEquation = buttonId.replace("÷", "/").replace("x", "*")
        else:
            currentPos += 1
            currentEquation = currentEquation[:currentPos] + buttonId.replace("÷", "/").replace("x", "*") + currentEquation[currentPos:]
            displayedEquation = displayedEquation[:currentPos-1] + buttonId + displayedEquation[currentPos-1:]



class Button:
    def __init__(self, image, pos, buttonId):
        self.cmd = buttonId
        self.width, self.height = image.get_size()
        self.x, self.y = pos
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def show(self):
        display.blit(self.image, (self.x, self.y))
    def setPos(self, x, y):
        self.x = x
        self.y = y

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    buttonPress(self.cmd)

def showButtons():
    for button in Buttons:
        button.show()
def buttonClickEvents(event):
    for button in Buttons:
        button.click(event)

def displayEquation():
    toDisplay = displayedEquation[:currentPos] + "_" + displayedEquation[currentPos:] if displayedEquation != "Error" else displayedEquation
    text = font.render(toDisplay, True, (0, 0, 0))
    textRect = text.get_rect(center=(WIDTH - text.get_width()//2- 50, 80))
    display.blit(text, textRect)

def checkKeys(event):
    global currentPos, currentEquation, displayedEquation
    keys = {pygame.K_0:"0", pygame.K_1:"1", pygame.K_2:"2", pygame.K_3:"3", pygame.K_4:"4", pygame.K_5:"5", pygame.K_6:"6", pygame.K_7:"7", pygame.K_8:"8", pygame.K_9:"9", pygame.K_MINUS:"-", pygame.K_PLUS:"+", pygame.K_PERIOD:".", pygame.K_ASTERISK:"*", pygame.K_EQUALS:"=", pygame.K_LEFTBRACKET:"(", pygame.K_RIGHTBRACKET:")", pygame.K_SLASH:"/", pygame.K_c:"c", pygame.K_RETURN:"="}
    for key in keys:
        if event.key == key:
            buttonPress(keys[key])
    if event.key == pygame.K_LEFT:
        if currentPos > 0:
            currentPos -= 1
    if event.key == pygame.K_RIGHT:
        if currentPos < len(currentEquation):
            currentPos += 1
    if event.key == pygame.K_BACKSPACE:
        currentEquation = currentEquation[:currentPos-1] + currentEquation[currentPos:]
        displayedEquation = displayedEquation[:currentPos-1] + displayedEquation[currentPos:]
        currentPos -= 1
    if event.key == pygame.K_DELETE:
        currentEquation = currentEquation[:currentPos] + currentEquation[currentPos+1:]
        displayedEquation = displayedEquation[:currentPos] + displayedEquation[currentPos+1:]
    
font_size = 60
font = pygame.font.SysFont("timesnewroman", font_size)
currentPos = 1
symbols = "=+.0c^-123÷x456)(789"
clock = pygame.time.Clock()
buttonImages = [pygame.image.load(f"Assets\\Button{number}.png") for number in symbols]
buttonImagesResized = [pygame.transform.scale(buttonImages[i], (200, 100)) for i in range(len(symbols))]
Buttons = [Button(buttonImagesResized[len(symbols)-i-1], ((40+(i%5)*205), (220+(i//5)*105)), symbols[len(symbols)-i-1]) for i in range(len(symbols)-1, -1, -1)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            buttonClickEvents(event)

        if event.type == pygame.KEYDOWN:
            checkKeys(event)

    display.fill((255, 255, 255))
    showButtons()
    displayEquation()
    pygame.display.flip()
    clock.tick(30)
