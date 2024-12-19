import pygame
import math
import tkinter as tk
from tkinter import ttk, messagebox

# --- Constants ---
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# --- Predefined L-Systems ---
L_SYSTEMS = {
    "Tree": {
        "axiom": "F",
        "rules": {"F": "F[-F]F[+F]F"},
        "angle": 25,
        "iterations": 4,
        "line_length": 15,
        "start_x": 400, # Half of WIDTH constant
        "start_y": 600, # Equal to HEIGHT constant
        "thickness": 2,
        "description": "A simple tree-like structure where:\n- F: Draw forward\n- [: Save position\n- ]: Restore position\n- +: Turn right\n- -: Turn left"
    },
    "Koch Curve": {
        "axiom": "F",
        "rules": {"F": "F+F-F-F+F"},
        "angle": 90,
        "iterations": 3,
        "line_length": 5,
        "start_x": 50, # Adjust these values for proper display in screen
        "start_y": 300,
        "thickness": 2,
        "description": "The Koch curve is a fractal curve that creates intricate geometric patterns.\nEach line segment is replaced with four segments in a specific pattern."
    },
    "Sierpinski Triangle": {
        "axiom": "F-G-G",
        "rules": {
            "F": "F-G+F+G-F",
            "G": "GG"
        },
        "angle": 120,
        "iterations": 5,
        "line_length": 10,
        "start_x": 400, # Adjust these values for proper display in screen
        "start_y": 550,
        "thickness": 2,
        "description": "Creates a famous fractal triangle pattern made up of smaller triangles.\nUses two symbols (F and G) to create the recursive pattern."
    },
    "Dragon Curve": {
        "axiom": "FX",
        "rules": {
            "X": "X+YF+",
            "Y": "-FX-Y"
        },
        "angle": 90,
        "iterations": 11,
        "line_length": 8,
        "start_x": 450,
        "start_y": 250,
        "thickness": 2,
        "description": "A complex curve that resembles a dragon's tail.\nCreates intricate patterns through repeated folding."
    },
    "Quadratic Koch Island": {
        "axiom": "F-F-F-F",
        "rules": {"F": "F-F+F+FF-F-F+F"},
        "angle": 90,
        "iterations": 3,
        "line_length": 5,
        "start_x": 250, # Adjust these values for proper display in screen
        "start_y": 450,
        "thickness": 2,
        "description": "A fractal coastline that creates complex shapes through recursively\nreplacing line segments with square-like shapes.\nIt starts as a square."
    },
    "Plant (Stochastic)": {
        "axiom": "X",
        "rules": {
            "X": "F+[[X]-X]-F[-FX]+X",
            "F": "FF"
        },
        "angle": 25,
        "iterations": 6,
        "line_length": 8,
        "start_x": 400,
        "start_y": 600,
        "thickness": 2,
        "description": "This rule models a more complex, plant-like growth.\nThe brackets create branching structures,\nand each iteration adds more detail to the branches.\nThe 'X' serves as a placeholder for growth points."
    },
    "Bush": {
        "axiom": "F",
        "rules": {"F": "FF+[+F-F-F]-[-F+F+F]"},
        "angle": 22.5,
        "iterations": 4,
        "line_length": 12,
        "start_x": 400,
        "start_y": 600,
        "thickness": 2,
        "description": "Generates a bush-like structure with more consistent branching\non both sides, leading to a fuller shape.\nThe rule expands each segment into more branches,\nwith new branches symmetrically distributed."
    },
    "Penrose Tiling": {
        "axiom": "[X]++[X]++[X]++[X]++[X]",
        "rules": {
            "F": "",
            "W": "YF++ZF----XF[-YF----WF]++",
            "X": "+YF--ZF[---WF--XF]+",
            "Y": "-WF++XF[+++YF++ZF]-",
            "Z": "--YF++++WF[+ZF++++XF]--XF"
        },
        "angle": 36,
        "iterations": 5,
        "line_length": 25,
        "start_x": 420,
        "start_y": 320,
        "thickness": 2,
        "description": "This creates a non-periodic tiling of the plane,\nwhich is a pattern that does not repeat\nby simple translation.\nThe L-system is modified to ensure a non-periodic\nstructure."
    },
    "Hilbert Curve": {
        "axiom": "A",
        "rules": {
            "A": "-BF+AFA+FB-",
            "B": "+AF-BFB-FA+"
        },
        "angle": 90,
        "iterations": 5,
        "line_length": 15,
        "start_x": 75,
        "start_y": 500,
        "thickness": 2,
        "description": "Creates a space-filling curve.\nThis type of curve densely fills the space\nand is used to reduce dimensionality\nwhile preserving locality.\nCan create interesting geometrical figures if a drawing offset is set in each new iteration."
    },
    "Crystal": {
        "axiom": "F+F+F+F",
        "rules": {"F": "FF+F++F+F"},
        "angle": 90,
        "iterations": 3,
        "line_length": 20,
        "start_x": 100,
        "start_y": 300,
        "thickness": 2,
        "description": "Generates a geometric pattern resembling a crystal with a square base.\nRecursively creates a larger central structure surrounded by smaller, similar shapes."
    },
    "Gosper Curve (Flowsnake)": {
        "axiom": "F",
        "rules": {
            "F": "F-G--G+F++FF+G-",
            "G": "+F-GG--G-F++F+G"
        },
        "angle": 60,
        "iterations": 3,
        "line_length": 10,
        "start_x": 400,
        "start_y": 400,
        "thickness": 2,
        "description": "A variation of the Koch curve that produces a space-filling \"snowflake\" pattern.\nAlso known as the Gosper flowsnake. It creates a loop with hexagonal motifs."
    },
    "Lace": {
        "axiom": "W",
        "rules": {
            "W": "+++X-F-X+++" ,
            "X": "---W+F+W---"
        },
        "angle": 30,
        "iterations": 10,
        "line_length": 35,
        "start_x": 370,
        "start_y": 350,
        "thickness": 4,
        "description": "Creates a delicate, lace-like fractal pattern using only two very simple rules\nThe pattern consists of interweaving curves that fill the space in an intricate way."
    },
    "Hexagonal Gosper": {
        "axiom": "F-F-F-F-F-F",
        "rules": {"F": "F-F++F+F--F--F++"},
        "angle": 60,
        "iterations": 2,
        "line_length": 20,
        "start_x": 175,
        "start_y": 380,
        "thickness": 2,
        "description": "Creates a snowflake like curve in which each segment is replaced by\na new one containing some smaller hexagonal structures.\nIf you set the iterations number to 3 you'll see a small black\nhexagonal strcture in the middle."
    },
    "Board": {
        "axiom": "F+F+F+F",
        "rules": {
            "F": "FF+F-F+F+FF"
        },
        "angle": 90,
        "iterations": 4,
        "line_length": 15,
        "start_x": 250,
        "start_y": 500,
        "thickness": 2,
        "description": "Similar to \"Quadratic Koch Island\", but draws more dense figures that give a sense of solidity to the fractal.\nIt starts as a square."
    }
}

class LSystemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("L-System Renderer")
        self.root.geometry("800x800")
        
        # Initialize pygame at startup
        pygame.init()
        self.screen = None
        
        # Create and pack widgets
        self.create_widgets()
        
        # Selected system variables
        self.current_system = None
        
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="L-System Renderer", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Introduction text
        intro_text = """L-systems (Lindenmayer systems) are parallel rewriting systems that can model
        the growth patterns of plants and create various fractals. They consist of:
        • An axiom (initial state)
        • A set of rules that define how symbols are replaced
        • Geometric interpretation of the symbols"""
        
        intro = tk.Label(self.root, text=intro_text, justify=tk.LEFT, wraplength=550)
        intro.pack(pady=10, padx=20)
        
        # System selection
        system_frame = ttk.LabelFrame(self.root, text="Select L-System")
        system_frame.pack(fill="x", padx=20, pady=10)
        
        self.system_var = tk.StringVar()
        for system in L_SYSTEMS.keys():
            ttk.Radiobutton(system_frame, text=system, value=system, 
                          variable=self.system_var, command=self.update_description).pack(anchor="w", padx=10)
        
        # Description
        self.desc_text = tk.Text(self.root, height=12, wrap=tk.WORD)
        self.desc_text.pack(fill="x", padx=20, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Render", command=self.render_system).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.cleanup_and_quit).pack(side=tk.LEFT, padx=10)
            
    def update_description(self):
        system = self.system_var.get()
        if system in L_SYSTEMS:
            self.desc_text.delete(1.0, tk.END)
            selected_system = L_SYSTEMS[system]
            description = selected_system["description"]
            axiom = selected_system["axiom"]
            rules = selected_system["rules"]
            angle = selected_system["angle"]
            iterations = selected_system["iterations"]

            # Prepare detailed description
            detailed_description = f"Description:\n{description}\n\n"
            detailed_description += f"Axiom: {axiom}\n"
            detailed_description += "Rules:\n"
            for key, value in rules.items():
                detailed_description += f"  {key} -> {value}\n"
            detailed_description += f"Angle: {angle} degrees\n"
            detailed_description += f"Iterations: {iterations}\n"

            self.desc_text.insert(1.0, detailed_description)

    def render_system(self):
        system_name = self.system_var.get()
        if not system_name:
            messagebox.showwarning("Warning", "Please select an L-system first!")
            return
            
        system = L_SYSTEMS[system_name]
        
        # Create or reset pygame window
        if self.screen is None:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"L-System Renderer - {system_name}")
        
        # Generate and draw the L-system
        l_system_string = generate_l_system(system["axiom"], system["rules"], system["iterations"])
        
        # Clear screen
        self.screen.fill(WHITE)
        
        # Set up drawing parameters
        global angle_degrees
        angle_degrees = system["angle"]
        
        # Draw the L-system
        global screen  # Need this for the draw_l_system function
        screen = self.screen
        draw_l_system(l_system_string, system["start_x"], system["start_y"], 90, system["line_length"], system["thickness"])
        pygame.display.flip()
        
        # Handle pygame events
        self.handle_pygame_events()
    
    def handle_pygame_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen = None
                    pygame.display.quit()
                    return
            
            # Process Tkinter events to keep the GUI responsive
            self.root.update()
    
    def cleanup_and_quit(self):
        if self.screen is not None:
            pygame.display.quit()
        pygame.quit()
        self.root.quit()

def generate_l_system(axiom, rules, iterations):
    """Generates the L-system string after a given number of iterations."""
    l_system_string = axiom
    for _ in range(iterations):
        new_string = ""
        for char in l_system_string:
            if char in rules:
                new_string += rules[char]
            else:
                new_string += char
        l_system_string = new_string
    return l_system_string

def draw_l_system(l_system_string, x, y, angle, line_length, thickness):
    """Draws the L-system using turtle graphics."""
    stack = []  # Stack to store (x, y, angle)
    current_color = BROWN # Initialize color
    current_angle = angle  # Keep track of current angle

    for char in l_system_string:
        if char == "F" or char == "G":  # Both F and G draw forward
            # Calculate end point based on current_angle and line_length
            rad_angle = math.radians(current_angle)
            new_x = x + line_length * math.cos(rad_angle)
            new_y = y - line_length * math.sin(rad_angle)
            # Draw a line segment
            pygame.draw.line(screen, current_color, (int(x), int(y)), (int(new_x), int(new_y)), max(1, int(thickness)))
            # Update current position
            x, y = new_x, new_y
        elif char == "+":
            # Rotate counter-clockwise
            current_angle += angle_degrees
        elif char == "-":
            # Rotate clockwise
            current_angle -= angle_degrees
        elif char == "[":
            # Save current state (position and angle) onto the stack
            stack.append((x, y, current_angle, current_color, thickness))
            # Change the color for this branch
            current_color = GREEN
            # Thinner line for the branches
            thickness *= 0.8
        elif char == "]":
            # Restore previous state (position, angle, color, and thickness) from the stack
            x, y, current_angle, current_color, thickness = stack.pop()

# --- Main Program ---
if __name__ == "__main__":
    gui = LSystemGUI()
    gui.root.mainloop()