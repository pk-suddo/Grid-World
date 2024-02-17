class WorldSimulation:
    """
    Sets up a grid world simulation with agent and leaf, where the leaf can either be an obstacle or passable.
    """
    def __init__(self, height, width, interaction='passable'):
        self.height = height
        self.width = width
        self.player = "A"
        self.obstacle = "L"
        self.area = [["-" for _ in range(width)] for _ in range(height)]
        self.interaction_mode = interaction
        self.player_loc = (2, 2)
        self.obstacle_loc = (2, 3)
        self.setup_world()

    # Initializes the game world by placing the player and obstacle in their respective starting locations on the grid.
    def setup_world(self):
        self.area[self.player_loc[0]][self.player_loc[1]] = self.player
        self.area[self.obstacle_loc[0]][self.obstacle_loc[1]] = self.obstacle

# Renders the current state of the grid to the console, displaying the positions of the player, obstacle, and empty spaces.
    def display_grid(self):
        for line in self.area:
            print(" ".join(line))
        print("\n")


    # Processes a movement command by updating the player's position based on the specified direction. It checks for
    # boundary limits, handles interactions with obstacles, and updates the grid to reflect the new player position.
    def navigate(self, move):
        direction_map = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
        delta_x, delta_y = direction_map[move]
        current_x, current_y = self.player_loc
        new_x, new_y = current_x + delta_x, current_y + delta_y

        if 0 <= new_x < self.height and 0 <= new_y < self.width:
            self.handle_movement_or_interaction(new_x, new_y, delta_x, delta_y)
        self.area[current_x][current_y] = "-"

    # Decides whether to move the player or interact with the obstacle based on the obstacle's current state
    # (passable or an obstacle) and the intended move direction.
    def handle_movement_or_interaction(self, new_x, new_y, delta_x, delta_y):
        if self.area[new_x][new_y] == self.obstacle and self.interaction_mode == 'obstacle':
            self.push_obstacle(new_x, new_y, delta_x, delta_y)
        elif self.area[new_x][new_y] == "-" or (self.area[new_x][new_y] == self.obstacle and self.interaction_mode == 'passable'):
            self.area[new_x][new_y] = self.player
            self.player_loc = (new_x, new_y)

    # Attempts to push the obstacle in the direction of the player's movement. If the push would move the obstacle off
    # the grid, it removes the obstacle from the game.
    def push_obstacle(self, x, y, dx, dy):
        next_x, next_y = x + dx, y + dy
        if 0 <= next_x < self.height and 0 <= next_y < self.width:
            self.area[next_x][next_y] = self.obstacle
            self.obstacle_loc = (next_x, next_y)
        else:
            self.obstacle_loc = None
        self.area[x][y] = self.player
        self.player_loc = (x, y)

    # Wrappers for navigating the player in specific directions using the general navigate method.
    def move_up(self): self.navigate('N')
    def move_down(self): self.navigate('S')
    def move_right(self): self.navigate('E')
    def move_left(self): self.navigate('W')

# Demonstrating the 'passable' leaf interaction mode
print("Demonstrating Leaf as Passable")
simulation_passable = WorldSimulation(5, 5, 'passable')
simulation_passable.display_grid()
simulation_passable.move_right()  # Move the agent right through the leaf
simulation_passable.display_grid()

# Demonstrating additional movements
simulation_passable.move_down()
simulation_passable.move_left()
simulation_passable.move_up()
simulation_passable.display_grid()  # Show the final state with leaf as passable

# Reinitializing for 'obstacle' mode
print("\nDemonstrating Leaf as an Obstacle")
simulation_obstacle = WorldSimulation(5, 5, 'obstacle')
simulation_obstacle.display_grid()
simulation_obstacle.move_right()  # Move the agent right, pushing the leaf if it's an obstacle
simulation_obstacle.display_grid()

# Attempt to push the leaf off the grid
simulation_obstacle.move_right()
simulation_obstacle.display_grid()  # Show the final state with leaf as an obstacle
