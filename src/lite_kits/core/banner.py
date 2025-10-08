from rich.console import Console
from rich.text import Text
from rich.live import Live
import time
import sys

console = Console()

BANNER = """
██╗     ██╗████████╗███████╗      ██╗  ██╗██╗████████╗███████╗
██║     ██║╚══██╔══╝██╔════╝      ██║ ██╔╝██║╚══██╔══╝██╔════╝
██║     ██║   ██║   █████╗  █████╗█████╔╝ ██║   ██║   ███████╗
██║     ██║   ██║   ██╔══╝  ╚════╝██╔═██╗ ██║   ██║   ╚════██║
███████╗██║   ██║   ███████╗      ██║  ██╗██║   ██║   ███████║
╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝
"""

TAGLINE = "Lightweight enhancement kits for spec-driven development."

RAINBOW_STOPS = [
    (255,   0,   0),   # Red
    (255, 127,   0),   # Orange
    (255, 255,   0),   # Yellow
    (0,   255,   0),   # Green
    (0,     0, 255),   # Blue
    (75,    0, 130),   # Indigo
    (148,   0, 211),   # Violet
    (255, 105, 180),   # Pink
]

def interpolate_multi_color(stops, steps):
    gradient = []
    n_segments = len(stops) - 1
    steps_per_segment = steps // n_segments
    for i in range(n_segments):
        start = stops[i]
        end = stops[i+1]
        for j in range(steps_per_segment):
            t = j / steps_per_segment
            r = int(start[0] + (end[0] - start[0]) * t)
            g = int(start[1] + (end[1] - start[1]) * t)
            b = int(start[2] + (end[2] - start[2]) * t)
            gradient.append(f"#{r:02X}{g:02X}{b:02X}")
    gradient.append(f"#{stops[-1][0]:02X}{stops[-1][1]:02X}{stops[-1][2]:02X}")
    return gradient

def get_diagonal_steps(text=BANNER):
    lines = text.strip().split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    return height + width - 2

def apply_diagonal_gradient(text=BANNER, offset=0, steps_override=None):
    lines = text.strip().split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    steps = steps_override if steps_override else height + width - 2
    gradient = interpolate_multi_color(RAINBOW_STOPS, steps + 1)
    result = Text()
    for line_idx, line in enumerate(lines):
        for char_idx, char in enumerate(line):
            diag_idx = line_idx + char_idx + offset
            color_idx = min(diag_idx, len(gradient) - 1)
            color = gradient[color_idx]
            result.append(char, style=f"bold {color}")
        result.append('\n')
    return result

def typewriter_effect(text=TAGLINE, delay=0.03, cursor_blink_rate=0.4, blink_cycles=2):
    """Display retro terminal typewriter animation with dim text via ANSI codes."""
    DIM = '\033[2m'
    RESET = '\033[0m'
    for i in range(len(text) + 1):
        sys.stdout.write('\r' + DIM + text[:i] + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    for _ in range(blink_cycles):
        sys.stdout.write('\r' + DIM + text + '█' + RESET)
        sys.stdout.flush()
        time.sleep(cursor_blink_rate)
        sys.stdout.write('\r' + DIM + text + ' ' + RESET)
        sys.stdout.flush()
        time.sleep(cursor_blink_rate)
    sys.stdout.write('\n')


def diagonal_reveal_banner(text=BANNER, steps_override=None, fps=56):
    """Reveal the banner diagonally from top-left to bottom-right, with gradient following the reveal."""
    console.print()
    lines = text.strip().split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)
    steps = steps_override if steps_override else height + width - 2
    gradient = interpolate_multi_color(RAINBOW_STOPS, steps + 1)

    # Prepare a matrix of characters and their diagonal indices
    char_matrix = []
    diag_indices = []
    for line_idx, line in enumerate(lines):
        row = []
        diag_row = []
        for char_idx, char in enumerate(line):
            row.append(char)
            diag_row.append(line_idx + char_idx)
        char_matrix.append(row)
        diag_indices.append(diag_row)

    # Reveal animation
    try:
        with Live(console=console, refresh_per_second=fps, transient=True) as live:
            for reveal_diag in range(steps + 1):
                result = Text()
                for line_idx, row in enumerate(char_matrix):
                    for char_idx, char in enumerate(row):
                        diag_idx = diag_indices[line_idx][char_idx]
                        if diag_idx <= reveal_diag:
                            color = gradient[min(diag_idx, len(gradient)-1)]
                            result.append(char, style=f"bold {color}")
                        else:
                            result.append(" ")
                    result.append('\n')
                live.update(result)
                time.sleep(1.0 / fps)
    except KeyboardInterrupt:
        pass

    # Show final static gradient
    result = Text()
    for line_idx, row in enumerate(char_matrix):
        for char_idx, char in enumerate(row):
            diag_idx = diag_indices[line_idx][char_idx]
            color = gradient[min(diag_idx, len(gradient)-1)]
            result.append(char, style=f"bold {color}")
        result.append('\n')
    console.print(result)
    typewriter_effect()
    console.print()

def show_status_banner(kits_installed=["git", "project", "multiagent"]):
    console.print()
    steps = get_diagonal_steps()
    gradient_text = apply_diagonal_gradient(offset=0, steps_override=steps)
    console.print(gradient_text)
    console.print(f"{TAGLINE}\n", style="dim")
    if kits_installed:
        console.print("Installed kits:", style="bold")
        kit_icons = {
            "git": "🔧",
            "project": "🎯",
            "multiagent": "🤝"
        }
        for kit in kits_installed:
            icon = kit_icons.get(kit, "📦")
            console.print(f"  {icon} {kit}-kit", style="green")
    else:
        console.print("No kits installed", style="dim yellow")
    console.print()

def show_loading_spinner(message="Loading kits..."):
    console.print()
    with console.status(f"[bold bright_cyan]{message}", spinner="dots"):
        time.sleep(1.5)
    console.print("[green]✓ Done![/green]")
    console.print()

if __name__ == "__main__":
    console.clear()
    console.print("[bold yellow]\nDemo 1: Loading Spinner[/bold yellow]")
    show_loading_spinner()
    time.sleep(1)
    console.print("[bold yellow]Demo 2: Diagonal Reveal Animation[/bold yellow]")
    diagonal_reveal_banner()
    time.sleep(1)
    console.print("[bold yellow]Demo 3: Status Banner[/bold yellow]")
    show_status_banner()
