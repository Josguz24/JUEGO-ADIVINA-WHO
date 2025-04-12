import pygame
import random
import sys
from pygame.locals import *

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Adivina Quién - Marvel Edition")

# Cargar imágenes de fondo y elementos visuales
try:
    background = pygame.image.load("marvel_bg.jpg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    logo = pygame.image.load("marvel_logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (logo.get_width()//2, logo.get_height()//2))
except:
    # Si no hay imágenes, usar fondos de color
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 20, 40))
    logo = None

# Colores mejorados
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 200)  # Con transparencia
RED = (236, 29, 36)      # Rojo Marvel
BLUE = (0, 70, 140)      # Azul Marvel
GOLD = (255, 215, 0)     # Oro para detalles
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50, 200)
LIGHT_BLUE = (100, 150, 255)
DARK_RED = (180, 0, 0)
GREEN = (0, 150, 0)

# Gradientes para botones
def create_gradient(width, height, start_color, end_color, horizontal=True):
    gradient = pygame.Surface((width, height), pygame.SRCALPHA)
    if horizontal:
        for x in range(width):
            ratio = x / width
            r = start_color[0] + (end_color[0] - start_color[0]) * ratio
            g = start_color[1] + (end_color[1] - start_color[1]) * ratio
            b = start_color[2] + (end_color[2] - start_color[2]) * ratio
            pygame.draw.line(gradient, (int(r), int(g), int(b)), (x, 0), (x, height))
    else:
        for y in range(height):
            ratio = y / height
            r = start_color[0] + (end_color[0] - start_color[0]) * ratio
            g = start_color[1] + (end_color[1] - start_color[1]) * ratio
            b = start_color[2] + (end_color[2] - start_color[2]) * ratio
            pygame.draw.line(gradient, (int(r), int(g), int(b)), (0, y), (width, y))
    return gradient

# Fuentes mejoradas
try:
    font_title = pygame.font.Font("BebasNeue-Regular.ttf", 72)
    font_question = pygame.font.Font("Roboto-Medium.ttf", 32)
    font_button = pygame.font.Font("Roboto-Medium.ttf", 28)
    font_character = pygame.font.Font("Roboto-Regular.ttf", 22)
    font_feedback = pygame.font.Font("Roboto-Bold.ttf", 36)
except:
    font_title = pygame.font.SysFont('Arial', 72, bold=True)
    font_question = pygame.font.SysFont('Arial', 32, bold=True)
    font_button = pygame.font.SysFont('Arial', 28)
    font_character = pygame.font.SysFont('Arial', 22)
    font_feedback = pygame.font.SysFont('Arial', 36, bold=True)

# Lista completa de personajes
avengers = [
    "Iron Man", "Captain America", "Thor", "Hulk", "Black Widow", 
    "Hawkeye", "Spider-Man", "Black Panther", "Doctor Strange",
    "Captain Marvel", "Scarlet Witch", "Ant-Man", "Wasp",
    "Star-Lord", "Gamora", "Drax", "Rocket Raccoon", 
    "Groot", "Loki", "Thanos", "Ultron", "Vulture", "Hela", 
    "Shuri", "Mantis", "Nebula"
]

# Características de los personajes (mejoradas)
personajes_data = {
    "Iron Man": {
        "Género": "Masculino", "Poder": "Tecnológico", "Armadura": True, 
        "Vuelo": True, "Color": "Rojo/Dorado", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Tony Stark", "Primera aparición": 1963
    },
    "Captain America": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": True, 
        "Vuelo": False, "Color": "Azul", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Steve Rogers", "Primera aparición": 1941
    },
    "Thor": {
        "Género": "Masculino", "Poder": "Mágico", "Armadura": False, 
        "Vuelo": True, "Color": "Rojo", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Asgard", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Thor Odinson", "Primera aparición": 1962
    },
    "Hulk": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": False, 
        "Vuelo": False, "Color": "Verde", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": False, "Equipo": "Vengadores",
        "Alias": "Bruce Banner", "Primera aparición": 1962
    },
    "Black Widow": {
        "Género": "Femenino", "Poder": "Físico", "Armadura": False, 
        "Vuelo": False, "Color": "Negro", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Natasha Romanoff", "Primera aparición": 1964
    },
    "Hawkeye": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": False, 
        "Vuelo": False, "Color": "Morado", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Clint Barton", "Primera aparición": 1964
    },
    "Spider-Man": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": False, 
        "Vuelo": False, "Color": "Rojo/Azul", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": False, "Equipo": "Vengadores",
        "Alias": "Peter Parker", "Primera aparición": 1962
    },
    "Black Panther": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": True, 
        "Vuelo": False, "Color": "Negro", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Wakanda", "Arma": True, "Equipo": "Vengadores",
        "Alias": "T'Challa", "Primera aparición": 1966
    },
    "Doctor Strange": {
        "Género": "Masculino", "Poder": "Mágico", "Armadura": False, 
        "Vuelo": True, "Color": "Azul/Rojo", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Stephen Strange", "Primera aparición": 1963
    },
    "Captain Marvel": {
        "Género": "Femenino", "Poder": "Energético", "Armadura": True, 
        "Vuelo": True, "Color": "Rojo/Azul", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Carol Danvers", "Primera aparición": 1968
    },
    "Scarlet Witch": {
        "Género": "Femenino", "Poder": "Mágico", "Armadura": False, 
        "Vuelo": True, "Color": "Rojo", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Wanda Maximoff", "Primera aparición": 1964
    },
    "Ant-Man": {
        "Género": "Masculino", "Poder": "Tecnológico", "Armadura": True, 
        "Vuelo": False, "Color": "Rojo", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Scott Lang", "Primera aparición": 1962
    },
    "Wasp": {
        "Género": "Femenino", "Poder": "Tecnológico", "Armadura": True, 
        "Vuelo": True, "Color": "Amarillo/Negro", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Hope van Dyne", "Primera aparición": 1963
    },
    "Star-Lord": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": True, 
        "Vuelo": False, "Color": "Rojo", "Películas": "Guardianes de la Galaxia", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Guardianes de la Galaxia",
        "Alias": "Peter Quill", "Primera aparición": 1976
    },
    "Gamora": {
        "Género": "Femenino", "Poder": "Físico", "Armadura": False, 
        "Vuelo": False, "Color": "Verde", "Películas": "Guardianes de la Galaxia", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Guardianes de la Galaxia",
        "Alias": "Gamora", "Primera aparición": 1975
    },
    "Drax": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": False, 
        "Vuelo": False, "Color": "Verde", "Películas": "Guardianes de la Galaxia", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Guardianes de la Galaxia",
        "Alias": "Drax el Destructor", "Primera aparición": 1975
    },
    "Rocket Raccoon": {
        "Género": "Masculino", "Poder": "Tecnológico", "Armadura": False, 
        "Vuelo": False, "Color": "Gris", "Películas": "Guardianes de la Galaxia", 
        "Villano": False, "Origen": "Tierra", "Arma": True, "Equipo": "Guardianes de la Galaxia",
        "Alias": "Rocket", "Primera aparición": 1976
    },
    "Groot": {
        "Género": "Masculino", "Poder": "Mágico", "Armadura": False, 
        "Vuelo": False, "Color": "Madera", "Películas": "Guardianes de la Galaxia", 
        "Villano": False, "Origen": "Tierra", "Arma": False, "Equipo": "Guardianes de la Galaxia",
        "Alias": "Groot", "Primera aparición": 1960
    },
    "Loki": {
        "Género": "Masculino", "Poder": "Mágico", "Armadura": True, 
        "Vuelo": False, "Color": "Verde", "Películas": "Vengadores", 
        "Villano": True, "Origen": "Asgard", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Loki Laufeyson", "Primera aparición": 1962
    },
    "Thanos": {
        "Género": "Masculino", "Poder": "Físico", "Armadura": True, 
        "Vuelo": False, "Color": "Púrpura", "Películas": "Vengadores", 
        "Villano": True, "Origen": "Titán", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Thanos", "Primera aparición": 1968
    },
    "Ultron": {
        "Género": "No binario", "Poder": "Tecnológico", "Armadura": True, 
        "Vuelo": True, "Color": "Plateado", "Películas": "Vengadores", 
        "Villano": True, "Origen": "Inteligencia Artificial", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Ultron", "Primera aparición": 1968
    },
    "Vulture": {
        "Género": "Masculino", "Poder": "Tecnológico", "Armadura": True, 
        "Vuelo": True, "Color": "Verde", "Películas": "Vengadores", 
        "Villano": True, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Adrian Toomes", "Primera aparición": 1962
    },
    "Hela": {
        "Género": "Femenino", "Poder": "Mágico", "Armadura": True, 
        "Vuelo": False, "Color": "Negro", "Películas": "Vengadores", 
        "Villano": True, "Origen": "Asgard", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Hela", "Primera aparición": 1964
    },
    "Shuri": {
        "Género": "Femenino", "Poder": "Tecnológico", "Armadura": False, 
        "Vuelo": False, "Color": "Negro", "Películas": "Vengadores", 
        "Villano": False, "Origen": "Wakanda", "Arma": False, "Equipo": "Vengadores",
        "Alias": "Shuri", "Primera aparición": 2005
    },
    "Mantis": {
        "Género": "Femenino", "Poder": "Mágico", "Armadura": False, 
        "Vuelo": False, "Color": "Verde", "Películas": "Guardianes de la Galaxia", 
        "Villano": False, "Origen": "Tierra", "Arma": False, "Equipo": "Guardianes de la Galaxia",
        "Alias": "Mantis", "Primera aparición": 1973
    },
    "Nebula": {
        "Género": "Femenino", "Poder": "Tecnológico", "Armadura": True, 
        "Vuelo": False, "Color": "Azul", "Películas": "Vengadores", 
        "Villano": True, "Origen": "Tierra", "Arma": True, "Equipo": "Vengadores",
        "Alias": "Nebula", "Primera aparición": 1985
    }
}

# Preguntas disponibles (mejoradas)
preguntas = [
    ("¿Es de género masculino?", "Género", "Masculino", "gender"),
    ("¿Es de género femenino?", "Género", "Femenino", "gender"),
    ("¿Tiene poderes mágicos?", "Poder", "Mágico", "magic"),
    ("¿Usa tecnología avanzada?", "Poder", "Tecnológico", "tech"),
    ("¿Tiene poderes físicos sobrehumanos?", "Poder", "Físico", "strength"),
    ("¿Tiene poderes energéticos?", "Poder", "Energético", "energy"),
    ("¿Usa armadura o traje especial?", "Armadura", True, "armor"),
    ("¿Puede volar?", "Vuelo", True, "flight"),
    ("¿Su traje es principalmente rojo?", "Color", "Rojo", "color"),
    ("¿Su traje es principalmente azul?", "Color", "Azul", "color"),
    ("¿Su traje es principalmente negro?", "Color", "Negro", "color"),
    ("¿Aparece en películas de los Vengadores?", "Películas", "Vengadores", "movies"),
    ("¿Es un villano?", "Villano", True, "villain"),
    ("¿Es parte de los Guardianes de la Galaxia?", "Equipo", "Guardianes de la Galaxia", "team"),
    ("¿Proviene de otro planeta?", "Origen", "Otro planeta", "origin"),
    ("¿Usa armas especiales?", "Arma", True, "weapons"),
    ("¿Tiene habilidades de curación?", "Poder", "Regeneración", "healing"),
    ("¿Es un humano normal sin superpoderes?", "Poder", "Humano normal", "human"),
    ("¿Tiene un alias secreto?", "Alias", True, "alias"),
    ("¿Apareció por primera vez antes de 1970?", "Primera aparición", "Antiguo", "era")
]

# Sistema de ponderación de preguntas
question_weights = {i: 1 for i in range(len(preguntas))}

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=RED, 
                 text_color=WHITE, border_radius=10, icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.icon = icon
        self.is_hovered = False
        self.shadow = pygame.Surface((width+6, height+6), pygame.SRCALPHA)
        self.shadow.fill((0, 0, 0, 100))
        
    def draw(self, surface):
        # Dibujar sombra
        if self.is_hovered:
            surface.blit(self.shadow, (self.rect.x-3, self.rect.y-3))
        
        # Dibujar botón
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=self.border_radius)
        
        # Dibujar texto
        text_surf = font_button.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Si hay icono, ajustar posición del texto
        if self.icon:
            icon_rect = self.icon.get_rect(center=(self.rect.x + 30, self.rect.centery))
            surface.blit(self.icon, icon_rect)
            text_rect.x += 20
        
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                # Efecto de clic
                self.rect.y += 2
                pygame.display.flip()
                pygame.time.delay(100)
                self.rect.y -= 2
                return True
        return False

class CharacterCard:
    def __init__(self, name):
        self.name = name
        self.rect = pygame.Rect(0, 0, 200, 250)
        self.selected = False
        self.hovered = False
        self.shadow = pygame.Surface((210, 260), pygame.SRCALPHA)
        self.shadow.fill((0, 0, 0, 100))
        
        # Crear imagen de personaje (simulada)
        self.card_surface = pygame.Surface((200, 250), pygame.SRCALPHA)
        self.update_card()
        
    def update_card(self):
        self.card_surface.fill((0, 0, 0, 0))
        
        # Fondo de la tarjeta
        bg_color = GOLD if self.selected else (50, 50, 70)
        pygame.draw.rect(self.card_surface, bg_color, (0, 0, 200, 250), border_radius=10)
        pygame.draw.rect(self.card_surface, BLACK, (0, 0, 200, 250), 2, border_radius=10)
        
        # Dibujar "imagen" del personaje (simulada)
        color_personaje = personajes_data[self.name]["Color"].split("/")[0]
        color_map = {
            "Rojo": (200, 0, 0), "Azul": (0, 0, 200), "Verde": (0, 150, 0),
            "Negro": (30, 30, 30), "Dorado": (205, 175, 0), "Morado": (128, 0, 128),
            "Amarillo": (200, 200, 0), "Madera": (110, 50, 0),
            "Plateado": (180, 180, 180), "Púrpura": (100, 0, 100),
            "Azul/Rojo": (0, 0, 200), "Rojo/Azul": (200, 0, 0),
            "Amarillo/Negro": (200, 200, 0), "Rojo/Dorado": (200, 0, 0)
        }
        color_rgb = color_map.get(color_personaje, (100, 100, 100))
        
        # Dibujar imagen del personaje (simulada)
        pygame.draw.rect(self.card_surface, color_rgb, (20, 20, 160, 160), border_radius=5)
        
        # Dibujar efecto de imagen de cómic
        for _ in range(10):
            x, y = random.randint(20, 180), random.randint(20, 180)
            w, h = random.randint(5, 20), random.randint(5, 20)
            pygame.draw.rect(self.card_surface, (color_rgb[0]+50, color_rgb[1]+50, color_rgb[2]+50), 
                            (x, y, w, h), border_radius=2)
        
        # Dibujar iniciales
        initials = "".join([word[0] for word in self.name.split()])
        text_surf = font_question.render(initials, True, WHITE)
        text_rect = text_surf.get_rect(center=(100, 100))
        self.card_surface.blit(text_surf, text_rect)
        
        # Dibujar nombre del personaje
        name_parts = self.name.split()
        for i, part in enumerate(name_parts):
            text_surf = font_character.render(part, True, WHITE)
            text_rect = text_surf.get_rect(center=(100, 200 + i*30))
            self.card_surface.blit(text_surf, text_rect)
        
        # Efecto de selección
        if self.selected:
            pygame.draw.rect(self.card_surface, (255, 255, 255, 50), (0, 0, 200, 250), border_radius=10)
        
    def draw(self, surface):
        # Dibujar sombra si está hovered
        if self.hovered and not self.selected:
            surface.blit(self.shadow, (self.rect.x-5, self.rect.y-5))
        
        # Dibujar tarjeta
        surface.blit(self.card_surface, self.rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def check_click(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                # Efecto de clic
                self.rect.y += 5
                pygame.display.flip()
                pygame.time.delay(100)
                self.rect.y -= 5
                return True
        return False

def reorganizar_tarjetas(personajes_posibles, character_cards):
    cards_visibles = [card for card in character_cards if card.name in personajes_posibles]
    num_personajes = len(cards_visibles)
    
    if num_personajes == 0:
        return []
    
    # Calcular disposición óptima
    max_columnas = min(6, num_personajes)
    filas = (num_personajes + max_columnas - 1) // max_columnas
    
    # Calcular tamaño de tarjeta basado en la cantidad
    ancho_tarjeta = 200 if num_personajes <= 6 else 180
    alto_tarjeta = 250 if num_personajes <= 6 else 230
    
    espacio_horizontal = (WIDTH - (max_columnas * (ancho_tarjeta + 20))) // 2
    espacio_vertical = max(50, (HEIGHT - 200 - (filas * (alto_tarjeta + 20))) // 2)

    for i, card in enumerate(cards_visibles):
        fila = i // max_columnas
        columna = i % max_columnas
        card.rect = pygame.Rect(
            espacio_horizontal + columna * (ancho_tarjeta + 20),
            150 + espacio_vertical + fila * (alto_tarjeta + 20),
            ancho_tarjeta,
            alto_tarjeta
        )
        card.update_card()
    
    return cards_visibles

def get_best_question(personajes_posibles, preguntas):
    if len(personajes_posibles) <= 1:
        return None
        
    # Crear lista de preguntas con sus pesos
    weighted_questions = []
    for i, question in enumerate(preguntas):
        weight = question_weights.get(i, 1)
        weighted_questions.append((question, weight))
    
    # Ordenar preguntas por peso (las más efectivas primero)
    weighted_questions.sort(key=lambda x: x[1], reverse=True)
    sorted_questions = [q[0] for q in weighted_questions]
    
    best_question = None
    best_score = float('inf')
    
    # Tomar las primeras 5 preguntas ordenadas por peso para evaluar
    for question in sorted_questions[:5]:
        categoria = question[1]
        valor = question[2]
        
        try:
            count_yes = sum(1 for p in personajes_posibles if personajes_data[p][categoria] == valor)
            count_no = len(personajes_posibles) - count_yes
            
            if count_yes > 0 and count_no > 0:
                current_score = abs(count_yes - count_no)
                
                if current_score < best_score:
                    best_score = current_score
                    best_question = question
                    
                    if best_score == 0:
                        break
        except KeyError:
            continue
    
    # Si no encontramos en las primeras 5, buscar en el resto
    if best_question is None:
        for question in sorted_questions[5:]:
            categoria = question[1]
            valor = question[2]
            
            try:
                count_yes = sum(1 for p in personajes_posibles if personajes_data[p][categoria] == valor)
                count_no = len(personajes_posibles) - count_yes
                
                if count_yes > 0 and count_no > 0:
                    current_score = abs(count_yes - count_no)
                    
                    if current_score < best_score:
                        best_score = current_score
                        best_question = question
                        
                        if best_score == 0:
                            break
            except KeyError:
                continue
    
    # Actualizar pesos (aumentar peso de preguntas efectivas)
    if best_question is not None:
        question_index = preguntas.index(best_question)
        question_weights[question_index] = min(question_weights.get(question_index, 1) + 0.5, 5)
    
    return best_question if best_question else random.choice(preguntas)

def draw_text_with_outline(text, font, text_color, outline_color, surface, x, y):
    text_surf = font.render(text, True, outline_color)
    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        surface.blit(text_surf, (x + dx, y + dy))
    text_surf = font.render(text, True, text_color)
    surface.blit(text_surf, (x, y))

def main_game():
    global question_weights
    question_weights = {i: 1 for i in range(len(preguntas))}  # Resetear pesos
    
    personajes_posibles = avengers.copy()
    character_cards = [CharacterCard(name) for name in avengers]
    cards_visibles = reorganizar_tarjetas(personajes_posibles, character_cards)
    
    current_question = get_best_question(personajes_posibles, preguntas)
    feedback = f"Quedan {len(personajes_posibles)} personajes posibles"
    game_over = False
    guessing = False
    guessed_character = None
    
    # Crear botones con iconos
    try:
        yes_icon = pygame.image.load("yes_icon.png").convert_alpha()
        yes_icon = pygame.transform.scale(yes_icon, (30, 30))
        no_icon = pygame.image.load("no_icon.png").convert_alpha()
        no_icon = pygame.transform.scale(no_icon, (30, 30))
        restart_icon = pygame.image.load("restart_icon.png").convert_alpha()
        restart_icon = pygame.transform.scale(restart_icon, (30, 30))
        guess_icon = pygame.image.load("guess_icon.png").convert_alpha()
        guess_icon = pygame.transform.scale(guess_icon, (30, 30))
    except:
        yes_icon = no_icon = restart_icon = guess_icon = None
    
    yes_btn = Button(WIDTH//2 - 160, HEIGHT - 120, 140, 60, "Sí", GREEN, (0, 180, 0), icon=yes_icon)
    no_btn = Button(WIDTH//2 + 20, HEIGHT - 120, 140, 60, "No", RED, DARK_RED, icon=no_icon)
    restart_btn = Button(WIDTH - 180, HEIGHT - 70, 160, 60, "Reiniciar", DARK_GRAY, GRAY, icon=restart_icon)
    guess_btn = Button(WIDTH//2 - 80, HEIGHT - 120, 160, 60, "Adivinar", GOLD, (255, 180, 0), BLACK, icon=guess_icon)
    
    # Crear gradiente para el panel de pregunta
    question_panel = pygame.Surface((WIDTH-100, 80), pygame.SRCALPHA)
    pygame.draw.rect(question_panel, (0, 0, 0, 180), (0, 0, WIDTH-100, 80), border_radius=10)
    pygame.draw.rect(question_panel, GOLD, (0, 0, WIDTH-100, 80), 2, border_radius=10)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Dibujar fondo
        screen.blit(background, (0, 0))
        
        # Dibujar logo si existe
        if logo:
            screen.blit(logo, (WIDTH - logo.get_width() - 20, 20))
        
        # Dibujar título con efecto
        title_text = "ADIVINA QUIÉN - MARVEL"
        draw_text_with_outline(title_text, font_title, RED, BLACK, screen, WIDTH//2 - font_title.size(title_text)[0]//2, 30)
        
        # Dibujar panel de pregunta
        screen.blit(question_panel, (50, 80))
        
        if not game_over:
            if current_question:
                question_text = current_question[0]
                # Ajustar texto si es muy largo
                if len(question_text) > 40:
                    parts = question_text.split()
                    lines = []
                    current_line = ""
                    for part in parts:
                        if len(current_line + part) < 35:
                            current_line += part + " "
                        else:
                            lines.append(current_line)
                            current_line = part + " "
                    lines.append(current_line)
                    
                    for i, line in enumerate(lines):
                        text_surf = font_question.render(line, True, WHITE)
                        text_rect = text_surf.get_rect(center=(WIDTH//2, 100 + i*30))
                        screen.blit(text_surf, text_rect)
                else:
                    text_surf = font_question.render(question_text, True, WHITE)
                    text_rect = text_surf.get_rect(center=(WIDTH//2, 110))
                    screen.blit(text_surf, text_rect)
            else:
                text_surf = font_question.render("¡No hay más preguntas disponibles!", True, GOLD)
                text_rect = text_surf.get_rect(center=(WIDTH//2, 110))
                screen.blit(text_surf, text_rect)
        else:
            if guessed_character:
                text_surf = font_question.render(f"¡Pensaste en {guessed_character}!", True, GOLD)
                text_rect = text_surf.get_rect(center=(WIDTH//2, 110))
                screen.blit(text_surf, text_rect)
                
                # Mostrar información del personaje
                info = personajes_data.get(guessed_character, {})
                info_texts = [
                    f"Alias: {info.get('Alias', 'Desconocido')}",
                    f"Poder: {info.get('Poder', 'Desconocido')}",
                    f"Equipo: {info.get('Equipo', 'Desconocido')}"
                ]
                
                for i, text in enumerate(info_texts):
                    text_surf = font_character.render(text, True, WHITE)
                    screen.blit(text_surf, (WIDTH//2 - 150, 150 + i*30))
            else:
                text_surf = font_question.render("¡No pude adivinar tu personaje!", True, RED)
                text_rect = text_surf.get_rect(center=(WIDTH//2, 110))
                screen.blit(text_surf, text_rect)
        
        # Dibujar feedback con efecto
        if feedback:
            feedback_panel = pygame.Surface((font_feedback.size(feedback)[0] + 40, 50), pygame.SRCALPHA)
            pygame.draw.rect(feedback_panel, (0, 0, 0, 180), (0, 0, feedback_panel.get_width(), 50), border_radius=10)
            pygame.draw.rect(feedback_panel, GOLD if game_over else BLUE, (0, 0, feedback_panel.get_width(), 50), 2, border_radius=10)
            
            screen.blit(feedback_panel, (WIDTH//2 - feedback_panel.get_width()//2, HEIGHT - 180))
            
            color = GOLD if game_over else WHITE
            text_surf = font_feedback.render(feedback, True, color)
            text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT - 155))
            screen.blit(text_surf, text_rect)
        
        # Dibujar tarjetas de personajes visibles
        for card in cards_visibles:
            card.check_hover(mouse_pos)
            card.draw(screen)
        
        # Dibujar botones
        if not game_over:
            if current_question:
                yes_btn.draw(screen)
                no_btn.draw(screen)
                yes_btn.check_hover(mouse_pos)
                no_btn.check_hover(mouse_pos)
            else:
                guess_btn.draw(screen)
                guess_btn.check_hover(mouse_pos)
        
        restart_btn.draw(screen)
        restart_btn.check_hover(mouse_pos)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if not game_over:
                if current_question:
                    if yes_btn.is_clicked(mouse_pos, event):
                        categoria = current_question[1]
                        valor = current_question[2]
                        personajes_posibles = [p for p in personajes_posibles if personajes_data[p][categoria] == valor]
                        feedback = f"Quedan {len(personajes_posibles)} personajes posibles"
                        cards_visibles = reorganizar_tarjetas(personajes_posibles, character_cards)
                        current_question = get_best_question(personajes_posibles, preguntas)
                        
                    elif no_btn.is_clicked(mouse_pos, event):
                        categoria = current_question[1]
                        valor = current_question[2]
                        personajes_posibles = [p for p in personajes_posibles if personajes_data[p][categoria] != valor]
                        feedback = f"Quedan {len(personajes_posibles)} personajes posibles"
                        cards_visibles = reorganizar_tarjetas(personajes_posibles, character_cards)
                        current_question = get_best_question(personajes_posibles, preguntas)
                else:
                    if guess_btn.is_clicked(mouse_pos, event):
                        game_over = True
                        if len(personajes_posibles) == 1:
                            guessed_character = personajes_posibles[0]
                            feedback = f"¡Correcto! Pensaste en {guessed_character}"
                        else:
                            feedback = "¡No pude adivinar tu personaje!"
            
            if restart_btn.is_clicked(mouse_pos, event):
                return True
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return False

def main_menu():
    # Crear gradiente para el fondo del menú
    menu_bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(menu_bg, (0, 0, 50, 200), (0, 0, WIDTH, HEIGHT))
    
    # Crear efecto de partículas
    particles = []
    for _ in range(50):
        particles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'speed': random.uniform(0.5, 2),
            'size': random.randint(1, 3),
            'color': random.choice([RED, BLUE, GOLD, WHITE])
        })
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Dibujar fondo
        screen.blit(background, (0, 0))
        screen.blit(menu_bg, (0, 0))
        
        # Dibujar partículas
        for p in particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
            p['y'] -= p['speed']
            if p['y'] < 0:
                p['y'] = HEIGHT
                p['x'] = random.randint(0, WIDTH)
        
        # Dibujar logo si existe
        if logo:
            screen.blit(logo, (WIDTH//2 - logo.get_width()//2, 50))
        
        # Título con efecto
        title_text = "ADIVINA QUIÉN"
        subtitle_text = "Edición Marvel"
        
        draw_text_with_outline(title_text, font_title, RED, BLACK, screen, 
                            WIDTH//2 - font_title.size(title_text)[0]//2, HEIGHT//4)
        draw_text_with_outline(subtitle_text, font_question, WHITE, BLACK, screen, 
                            WIDTH//2 - font_question.size(subtitle_text)[0]//2, HEIGHT//4 + 80)
        
        # Panel de instrucciones
        instrucciones_panel = pygame.Surface((600, 220), pygame.SRCALPHA)
        pygame.draw.rect(instrucciones_panel, (0, 0, 0, 180), (0, 0, 600, 220), border_radius=15)
        pygame.draw.rect(instrucciones_panel, GOLD, (0, 0, 600, 220), 2, border_radius=15)
        screen.blit(instrucciones_panel, (WIDTH//2 - 300, HEIGHT//2 - 50))
        
        # Instrucciones
        instrucciones = [
            "1. Piensa en un personaje de Marvel",
            "2. Responde las preguntas con Sí o No",
            "3. Intentaré adivinar tu personaje",
            "4. ¡Diviértete con el universo Marvel!"
        ]
        
        for i, instruccion in enumerate(instrucciones):
            text_surf = font_button.render(instruccion, True, WHITE)
            text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + i*40 - 30))
            screen.blit(text_surf, text_rect)
        
        # Botones
        try:
            play_icon = pygame.image.load("play_icon.png").convert_alpha()
            play_icon = pygame.transform.scale(play_icon, (30, 30))
            exit_icon = pygame.image.load("exit_icon.png").convert_alpha()
            exit_icon = pygame.transform.scale(exit_icon, (30, 30))
        except:
            play_icon = exit_icon = None
        
        start_btn = Button(WIDTH//2 - 150, HEIGHT - 180, 300, 70, "COMENZAR JUEGO", RED, DARK_RED, icon=play_icon)
        quit_btn = Button(WIDTH//2 - 150, HEIGHT - 90, 300, 70, "SALIR", DARK_GRAY, GRAY, icon=exit_icon)
        
        start_btn.check_hover(mouse_pos)
        quit_btn.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if start_btn.is_clicked(mouse_pos, event):
                while main_game():
                    pass
                return
                
            if quit_btn.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
        
        start_btn.draw(screen)
        quit_btn.draw(screen)
        
        # Texto de créditos
        credits_text = "© 2023 Adivina Quién Marvel - Todos los derechos reservados"
        text_surf = font_character.render(credits_text, True, (150, 150, 150))
        screen.blit(text_surf, (WIDTH//2 - text_surf.get_width()//2, HEIGHT - 30))
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main_menu()
    pygame.quit()