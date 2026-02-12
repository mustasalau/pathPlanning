import pygame
from typing import List, Tuple
import argparse


class Cell:
    def __init__(self, row: int, col: int, width: int, height: int):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * height
        self.width = width
        self.height = height
        self.color = (0, 0, 0)  # black background by default
        # A* pathfinding attributes
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')
        self.parent = None

    def get_pos(self) -> Tuple[int, int]:
        return self.row, self.col

    def is_clicked(self) -> bool:
        return self.color != (0, 0, 0)

    def make_clicked(self):
        self.color = (255, 255, 255)  # will use for obstacles. 
    def make_start(self):
        self.color = (0, 255, 0)  # green

    def make_goal(self):
        self.color = (0, 0, 255)  # blue

    def is_start(self) -> bool:
        return self.color == (0, 255, 0)

    def is_goal(self) -> bool:
        return self.color == (0, 0, 255)
    
    def is_obstacle(self) -> bool:
        return self.color == (255, 255, 255)

    def reset(self):
        self.color = (0, 0, 0)

    def draw(self, win: pygame.Surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, rect)

    def h_cost(self, other: 'Cell') -> float:
        # Using Manhattan distance as cost
        return abs(self.row - other.row) + abs(self.col - other.col)
    
    def g_cost(self, other: 'Cell') -> float:
        # Cost to move from self to other
        # If the cell is adjacent (not diagonal), cost is 1, else cost is sqrt(2)
        if (self.row == other.row and abs(self.col - other.col) == 1) or (self.col == other.col and abs(self.row - other.row) == 1):
            return 1.0
        return 1.414  # sqrt(2) for diagonal movement

    def f_cost(self, other: 'Cell') -> float:
        return self.g_cost(other) + self.h_cost(other)




def create_grid(rows: int, cols: int, width: int, height: int) -> Tuple[List[List[Cell]], int, int]:
    """Create an RxC grid of Cell objects sized to the given window width/height.
    Returns (grid, node_width, node_height).
    """
    node_w = width // cols
    node_h = height // rows
    grid: List[List[Cell]] = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            grid[r].append(Cell(r, c, node_w, node_h))
    return grid, node_w, node_h


def draw_grid(win: pygame.Surface, grid: List[List[Cell]], rows: int, cols: int, width: int, height: int, slider_ratio: float = 0.5, info_mode: bool = False):
    win.fill((0, 0, 0))  # black background

    # prepare a small font for info mode
    try:
        font = pygame.font.SysFont(None, 12)
        small_font = pygame.font.SysFont(None, 10)
    except Exception:
        font = None
        small_font = None

    for row in grid:
        for node in row:
            node.draw(win)
            # draw numeric info if enabled
            if info_mode and font is not None:
                # prepare display strings (empty if not set)
                g_text = '' if node.g == float('inf') else f"{node.g:.1f}"
                h_text = '' if node.h == float('inf') else f"{node.h:.1f}"
                f_text = '' if node.f == float('inf') else f"{node.f:.1f}"

                # determine if cell is "big enough" for full info (g top-left, h top-right, f center)
                if node.width >= 36 and node.height >= 20 and (g_text or h_text or f_text):
                    # center f
                    if f_text:
                        surf_f = font.render(f_text, True, (220, 220, 220))
                        rect_f = surf_f.get_rect()
                        rect_f.center = (node.x + node.width // 2, node.y + node.height // 2)
                        win.blit(surf_f, rect_f)

                    # top-left g
                    if g_text:
                        surf_g = small_font.render(g_text, True, (200, 200, 200)) if small_font else font.render(g_text, True, (200, 200, 200))
                        rect_g = surf_g.get_rect()
                        rect_g.topleft = (node.x + 2, node.y + 1)
                        win.blit(surf_g, rect_g)

                    # top-right h
                    if h_text:
                        surf_h = small_font.render(h_text, True, (200, 200, 200)) if small_font else font.render(h_text, True, (200, 200, 200))
                        rect_h = surf_h.get_rect()
                        rect_h.topright = (node.x + node.width - 2, node.y + 1)
                        win.blit(surf_h, rect_h)

                else:
                    # fall back to a single centered value (prefer f, then g)
                    text = ''
                    if f_text:
                        text = f_text
                    elif g_text:
                        text = g_text

                    if text and node.width > 18 and node.height > 12:
                        surf = font.render(text, True, (220, 220, 220))
                        rect = surf.get_rect()
                        rect.center = (node.x + node.width // 2, node.y + node.height // 2)
                        win.blit(surf, rect)

    # draw subtle grid lines
    line_color = (40, 40, 40)
    node_h = height // rows
    node_w = width // cols
    for r in range(rows + 1):
        pygame.draw.line(win, line_color, (0, r * node_h), (width, r * node_h))
    for c in range(cols + 1):
        pygame.draw.line(win, line_color, (c * node_w, 0), (c * node_w, height))

    # Draw a simple slider at bottom to control search speed
    slider_w = 200
    slider_h = 10
    slider_x = 20
    slider_y = height - 30
    slider_bg = pygame.Rect(slider_x, slider_y, slider_w, slider_h)
    pygame.draw.rect(win, (80, 80, 80), slider_bg)

    # knob
    knob_x = slider_x + int(slider_ratio * slider_w)
    knob_w = 10
    knob_h = 18
    knob_rect = pygame.Rect(knob_x - knob_w // 2, slider_y - 4, knob_w, knob_h)
    pygame.draw.rect(win, (200, 200, 200), knob_rect)

    # label above the slider to indicate purpose
    try:
        label_font = pygame.font.SysFont(None, 18)
        label = label_font.render("Search speed", True, (200, 200, 200))
        label_rect = label.get_rect()
        label_rect.topleft = (slider_x, slider_y - 22)
        win.blit(label, label_rect)
    except Exception:
        pass

    # Draw an "Info mode" checkbox to the right of the slider
    checkbox_size = 16
    checkbox_x = slider_x + slider_w + 30
    checkbox_y = slider_y - 4
    checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, checkbox_size, checkbox_size)
    pygame.draw.rect(win, (200, 200, 200), checkbox_rect, 2)  # border
    if info_mode:
        # draw inner filled box when enabled
        inner = checkbox_rect.inflate(-6, -6)
        pygame.draw.rect(win, (200, 200, 200), inner)

    try:
        chk_font = pygame.font.SysFont(None, 16)
        chk_label = chk_font.render("Info mode", True, (200, 200, 200))
        chk_rect = chk_label.get_rect()
        chk_rect.midleft = (checkbox_x + checkbox_size + 8, checkbox_y + checkbox_size // 2)
        win.blit(chk_label, chk_rect)
    except Exception:
        pass

    pygame.display.update()


def get_clicked_pos(pos: Tuple[int, int], rows: int, cols: int, width: int, height: int) -> Tuple[int, int]:
    x, y = pos
    node_w = width // cols
    node_h = height // rows
    col = x // node_w
    row = y // node_h
    col = min(max(col, 0), cols - 1)
    row = min(max(row, 0), rows - 1)
    return row, col


def visual():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    ROWS, COLS = 60, 70
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid Click Demo")

    grid, _, _ = create_grid(ROWS, COLS, WIDTH, HEIGHT)

    # track start and goal nodes (Cell objects)
    start = None
    goal = None

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        draw_grid(WIN, grid, ROWS, COLS, WIDTH, HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)
                node = grid[row][col]

                if event.button == 1:  # left click
                    # first left click sets start (green)
                    if start is None and not node.is_goal():
                        start = node
                        start.make_start()
                    # second left click sets goal (blue)
                    elif goal is None and node != start:
                        goal = node
                        goal.make_goal()
                    else:
                        # regular left-click marking (white) for other nodes
                        if node != start and node != goal:
                            node.make_clicked()

                elif event.button == 3:  # right click
                    # if right-clicking start or goal, remove them
                    if node == start:
                        start.reset()
                        start = None
                    elif node == goal:
                        goal.reset()
                        goal = None
                    else:
                        node.reset()

    pygame.quit()
    return grid

def findStart_End(grid): 
    start = None
    goal = None
    for row in grid:
        for node in row:
            if node.is_start():
                start = node
            elif node.is_goal():
                goal = node
    return start, goal
def get_neighbors(grid, cell):
    """Get all valid neighbors of a cell (8-directional movement)"""
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    
    # Check all 8 directions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:  # Skip the cell itself
                continue
            
            new_row = cell.row + dr
            new_col = cell.col + dc
            
            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbor = grid[new_row][new_col]
                # Don't add obstacles as neighbors
                if not neighbor.is_obstacle():
                    neighbors.append(neighbor)
    
    return neighbors


def astar_search(grid, start, goal, win, rows, cols, width, height, delay_ms=10, slider_ratio: float = 0.5, info_mode: bool = False):
    """Perform A* search and visualize the process

    When info_mode is True, numeric details (g/h/f and neighbor tentative scores)
    are printed to the terminal to help debugging/learning.
    """
    if start is None or goal is None:
        print("Please set both start and goal nodes!")
        return None

    # Initialize start node
    start.g = 0
    start.h = start.h_cost(goal)
    start.f = start.g + start.h

    open_set = {start}
    closed_set = set()

    iter_count = 0
    if info_mode:
        print(f"A* start: start=({start.row},{start.col}) goal=({goal.row},{goal.col})")

    while open_set:
        iter_count += 1
        # Find node with lowest f cost
        current = min(open_set, key=lambda n: (n.f, n.h))

        # Info output for current node
        if info_mode:
            g = current.g if current.g != float('inf') else None
            h = current.h if current.h != float('inf') else None
            f = current.f if current.f != float('inf') else None
            print(f"Iter {iter_count}: current=({current.row},{current.col}) g={g} h={h} f={f} open={len(open_set)} closed={len(closed_set)}")

        # Check if we reached the goal
        if current == goal:
            if info_mode:
                print("Path found! Reconstructing path...")
            return reconstruct_path(current)

        # Move current from open to closed
        open_set.remove(current)
        closed_set.add(current)

        # Visualize the search (optional - can be removed for speed)
        if current != start and current != goal:
            current.color = (255, 165, 0)  # Orange for visited
        # pass the current slider_ratio and info_mode so the UI stays consistent
        draw_grid(win, grid, rows, cols, width, height, slider_ratio, info_mode)
        pygame.time.delay(delay_ms)  # controlled delay

        # Check all neighbors
        neighbors = get_neighbors(grid, current)
        for neighbor in neighbors:
            if neighbor in closed_set:
                if info_mode:
                    print(f"  Neighbor ({neighbor.row},{neighbor.col}) in closed set; skipping")
                continue

            # Calculate tentative g score
            tentative_g = current.g + current.g_cost(neighbor)

            if info_mode:
                old_g = neighbor.g if neighbor.g != float('inf') else None
                print(f"  Neighbor ({neighbor.row},{neighbor.col}) tentative_g={tentative_g:.2f} old_g={old_g}")

            # If this path to neighbor is better than any previous one
            if neighbor not in open_set:
                open_set.add(neighbor)
                neighbor.h = neighbor.h_cost(goal)
                if info_mode:
                    print(f"    Added to open set with h={neighbor.h:.2f}")
            elif tentative_g >= neighbor.g:
                if info_mode:
                    print("    Not a better path; skipping")
                continue  # This is not a better path

            # This path is the best so far, record it
            neighbor.parent = current
            neighbor.g = tentative_g
            neighbor.f = neighbor.g + neighbor.h

            if info_mode:
                print(f"    Updated neighbor ({neighbor.row},{neighbor.col}) g={neighbor.g:.2f} h={neighbor.h:.2f} f={neighbor.f:.2f}")

            # Visualize open set (optional)
            if neighbor != start and neighbor != goal:
                neighbor.color = (0, 255, 255)  # Cyan for open set

    print("No path found!")
    return None


def reconstruct_path(goal_node):
    """Reconstruct the path from goal to start"""
    path = []
    current = goal_node
    while current is not None:
        path.append(current)
        current = current.parent
    path.reverse()
    return path



def main():
    parser = argparse.ArgumentParser(description='A* visualization')
    parser.add_argument('--rows', type=int, default=60, help='number of rows')
    parser.add_argument('--cols', type=int, default=70, help='number of columns')
    args = parser.parse_args()

    # Allow user to optionally enter grid size interactively; press Enter to accept defaults
    try:
        rows_input = input(f"Enter number of rows [{args.rows}]: ").strip()
        cols_input = input(f"Enter number of columns [{args.cols}]: ").strip()
        ROWS = int(rows_input) if rows_input else args.rows
        COLS = int(cols_input) if cols_input else args.cols
    except Exception:
        # If input isn't available or invalid, fall back to provided args
        ROWS = args.rows
        COLS = args.cols

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding Visualization")

    grid, _, _ = create_grid(ROWS, COLS, WIDTH, HEIGHT)

    # track start and goal nodes (Cell objects)
    start = None
    goal = None

    # slider state: ratio 0..1 where 1.0 is fastest (0 ms delay)
    slider_ratio = 0.5
    adjusting_slider = False

    # info mode toggle
    info_mode = False

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        draw_grid(WIN, grid, ROWS, COLS, WIDTH, HEIGHT, slider_ratio, info_mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # check slider area first
                slider_w = 200
                slider_x = 20
                slider_y = HEIGHT - 30
                slider_rect = pygame.Rect(slider_x, slider_y, slider_w, 10)
                # checkbox rect (same position used in draw_grid)
                checkbox_size = 16
                checkbox_x = slider_x + slider_w + 30
                checkbox_y = slider_y - 4
                checkbox_rect = pygame.Rect(checkbox_x, checkbox_y, checkbox_size, checkbox_size)

                if checkbox_rect.collidepoint(pos):
                    # toggle info mode
                    info_mode = not info_mode
                    continue

                if slider_rect.collidepoint(pos):
                    adjusting_slider = True
                    slider_ratio = (pos[0] - slider_x) / slider_w
                    slider_ratio = min(max(slider_ratio, 0.0), 1.0)
                    continue

                row, col = get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)
                node = grid[row][col]

                if event.button == 1:  # left click
                    # first left click sets start (green)
                    if start is None and not node.is_goal():
                        start = node
                        start.make_start()
                    # second left click sets goal (blue)
                    elif goal is None and node != start:
                        goal = node
                        goal.make_goal()
                    else:
                        # regular left-click marking (white) for obstacles
                        if node != start and node != goal:
                            node.make_clicked()

                elif event.button == 3:  # right click
                    # if right-clicking start or goal, remove them
                    if node == start:
                        start.reset()
                        start = None
                    elif node == goal:
                        goal.reset()
                        goal = None
                    else:
                        node.reset()

            if event.type == pygame.MOUSEBUTTONUP:
                # stop adjusting slider when mouse released
                adjusting_slider = False

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                buttons = pygame.mouse.get_pressed()
                # adjust slider if dragging
                if adjusting_slider:
                    slider_w = 200
                    slider_x = 20
                    slider_ratio = (pos[0] - slider_x) / slider_w
                    slider_ratio = min(max(slider_ratio, 0.0), 1.0)
                    continue

                # dragging to add/remove obstacles
                if buttons[0]:  # left button held
                    row, col = get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)
                    node = grid[row][col]
                    if node != start and node != goal:
                        node.make_clicked()
                elif buttons[2]:  # right button held
                    row, col = get_clicked_pos(pos, ROWS, COLS, WIDTH, HEIGHT)
                    node = grid[row][col]
                    if node != start and node != goal:
                        node.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    # compute delay_ms from slider_ratio (1.0 -> 0ms, 0.0 -> 200ms)
                    delay_ms = int((1.0 - slider_ratio) * 200)
                    print("Running A* algorithm... delay_ms=", delay_ms)
                    # pass slider_ratio and info_mode so astar doesn't redraw slider at default
                    path = astar_search(grid, start, goal, WIN, ROWS, COLS, WIDTH, HEIGHT, delay_ms=delay_ms, slider_ratio=slider_ratio, info_mode=info_mode)
                    
                    # Visualize the final path
                    if path:
                        for cell in path:
                            if cell != start and cell != goal:
                                cell.color = (255, 0, 255)  # Magenta for path
                        draw_grid(WIN, grid, ROWS, COLS, WIDTH, HEIGHT, slider_ratio, info_mode)
                        print(f"Path length: {len(path)} cells")
                
                if event.key == pygame.K_c:
                    # Clear the grid
                    start = None
                    goal = None
                    grid, _, _ = create_grid(ROWS, COLS, WIDTH, HEIGHT)
                    print("Grid cleared!")

    pygame.quit()


if __name__ == "__main__":
    main()