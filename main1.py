# This code is for the first part of the project. Use plot1.py for visualization

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from visualization.plot1 import visualize  
from algorithms.astar import astar  
from environment.load_data import load_grid
import random
import time


grid = load_grid("data/map1.csv")
start = (0, 0)
goal = (4, 4)

app = dash.Dash(__name__)

previous_time = time.time()


def move_obstacle(trace, points, selector):
    """Handle the obstacle movement by the user."""
    # Get the position where the user clicked (in grid coordinates)
    x_click, y_click = points.xs[0], points.ys[0]
    
    # Update the grid
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
    html.Div(id='time-output')  
])


@app.callback(
    Output('grid-graph', 'figure'),
    Output('time-output', 'children'),
    Input('grid-graph', 'clickData')
)
def update_grid(clickData):
    global grid, goal, previous_time  
    if clickData:
        x_click = int(clickData['points'][0]['x'])
        y_click = int(clickData['points'][0]['y'])

       
        if grid[y_click][x_click] == 1: 
            grid[y_click][x_click] = 0  
        else:  
            grid[y_click][x_click] = 1

        
        if (x_click, y_click) != start: 
            goal = (x_click, y_click)  

    # Recalculate the path after moving the obstacle or goal
    path = astar(grid, start, goal)

    
    if path and path[0] != start:
        path = [start] + path  

    # Ensure the path ends at the red point (goal point)
    if path:
        goal_index = next((i for i, p in enumerate(path) if p == goal), None)
        if goal_index is not None:
            path = path[:goal_index + 1]  

    # Calculate time for each step
    current_time = time.time()
    time_taken = round(current_time - previous_time, 2)
    previous_time = current_time 

    # Display time taken for the current step
    time_display = f"Time taken for the step: {time_taken} seconds"

    
    return visualize(grid, path, start=start, goal=goal), time_display


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
