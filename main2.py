#This code is for the second part of the project with additional features, use plot2.py file for visualization 

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import time
from visualization.plot2 import visualize  
from algorithms.astar import astar  
from environment.load_data import load_grid

# Load grid and initialize the app
grid = load_grid("data/map1.csv")
start = (0, 0)
goal = (4, 4)

app = dash.Dash(__name__)


previous_time = time.time()

# Function to move the obstacle when the user clicks on the grid
def move_obstacle(trace, points, selector):
    """Handle the obstacle movement by the user."""
    x_click, y_click = points.xs[0], points.ys[0]
    
   
    if grid[int(y_click)][int(x_click)] == 1:  
        grid[int(y_click)][int(x_click)] = 0  
    else:  
        grid[int(y_click)][int(x_click)] = 1
    
    
    path = astar(grid, start, goal)

    
    return visualize(grid, path, start=start, goal=goal)


# App Layout
app.layout = html.Div([
    dcc.Graph(id='grid-graph'),
    html.Div(id='output'),
    html.Div(id='time-output'),  
    html.Div(id='info-output'),  
    html.Label('Animation Speed:'),
    dcc.Slider(
        id='speed-slider',
        min=100,
        max=1000,
        step=100,
        value=500,
        marks={100: 'Fast', 1000: 'Slow'},
    )
])

# Callback to update the grid and path when an obstacle is clicked or goal is moved
@app.callback(
    [Output('grid-graph', 'figure'),
     Output('time-output', 'children'),
     Output('info-output', 'children')],
    [Input('grid-graph', 'clickData'),
     Input('speed-slider', 'value')]  
)
def update_grid(clickData, speed_value):
    global grid, goal, previous_time  
    info_message = ""

    # Reset the grid if the reset button is clicked
    if clickData:
        x_click = int(clickData['points'][0]['x'])
        y_click = int(clickData['points'][0]['y'])

        
        if grid[y_click][x_click] == 1:  
            grid[y_click][x_click] = 0  
        else:  
            grid[y_click][x_click] = 1

        
        if (x_click, y_click) != start:  
            goal = (x_click, y_click)  

    
    path = astar(grid, start, goal)

    # Handle case where no path is found
    if path is None or len(path) == 0:
        info_message = "No path found! Please try moving the obstacles or change start/goal position."
        path = []  

    # Ensure the path starts at the green point (start point)
    if path and path[0] != start:
        path = [start] + path  

    # Ensure the path ends at the red point (goal point)
    if path:
        goal_index = next((i for i, p in enumerate(path) if p == goal), None)
        if goal_index is not None:
            path = path[:goal_index + 1]  

    
    current_time = time.time()
    time_taken = round(current_time - previous_time, 2)
    previous_time = current_time  

    # Display time taken for the current step
    time_display = f"Time taken for the step: {time_taken} seconds"
    
    
    path_length = len(path) if path else 0
    info_message += f" Path length: {path_length} steps."

    # Return the updated grid visualization with the new path and time display
    return visualize(grid, path, start=start, goal=goal, speed=speed_value), time_display, info_message


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
