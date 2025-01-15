import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import pyautogui

# Função para capturar a screenshot
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")  # Salva a imagem em um arquivo
    return "screenshot.png"

# Função para atualizar a imagem no plot
def update_plot(frame):
    img_path = capture_screenshot()
    img = Image.open(img_path)  # Abre a nova imagem
    ax.clear()  # Limpa o gráfico atual
    ax.imshow(img)  # Plota a nova imagem
    ax.axis('off')  # Remove os eixos

# Configuração inicial do matplotlib
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update_plot, interval=5000)  # Atualiza a cada 5000ms (5s)

# Exibe o gráfico
plt.show()
