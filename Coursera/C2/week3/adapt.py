class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)
        lights = []
        obstacles = []
        for i in range(len(grid)):
            for x in range(len(grid[i])):
                if grid[i][x] == 1:
                    lights.append((x, i))
                elif grid[i][x] == -1:
                    obstacles.append((x, i))

        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        return self.adaptee.generate_lights()


# class System:
#     def __init__(self):
#         self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
#         self.map[5][7] = 1 # Источники света
#         self.map[5][2] = -1 # Стены
    
#     def get_lightening(self, light_mapper):
#         self.lightmap = light_mapper.lighten(self.map)


# class Light:
#     def __init__(self, dim):
#         self.dim = dim # (ширина, высота)
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
#         self.lights = []
#         self.obstacles = []
        
#     def set_dim(self, dim):
#         self.dim = dim
#         self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
    
#     def set_lights(self, lights): # устанавливает массив источников света
#         self.lights = lights
#         self.generate_lights()
    
#     def set_obstacles(self, obstacles): # устанавливает массив препятствий
#         self.obstacles = obstacles
#         self.generate_lights()
        
#     def generate_lights(self): # рассчитывает освещенность с учетом источников и препятствий
#         return self.grid.copy()

# a = System()
# for i in range(len(a.map)):
#     print(a.map[i])

# b = MappingAdapter('asd')
# b.lighten(a.grid)
