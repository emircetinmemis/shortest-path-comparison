"""
This script is used for visualizing the given graph and its path in PNG and SVG formats.
"""
from Constants import (
    VISUAL_SVG_OUTPUT_PATH,
    VISUAL_PNG_OUTPUT_PATH,
)
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

def visualize(number_of_cities:int, nodes_to_be_colored:list=[]) -> None :
    """
    Visualizes the path in a given graph. The graph is a list of nodes and edges. The nodes are the cities and the edges are the paths between the cities.
    @params:
        number_of_cities: The number of cities in the graph.
        nodes_to_be_colored: The nodes that are to be colored in the graph.
    """
    
    weights_to_be_colored = list(zip(nodes_to_be_colored, nodes_to_be_colored[1:]))

    vertical_inpad = 6
    horizontal_inpad = 6

    max_cities_horizontally = int(number_of_cities/2) + (1 if number_of_cities % 2 == 1 else 0) 
    max_cities_vertically = (0 if number_of_cities == 0 else 1 if number_of_cities == 1 else 2)

    canvas_padding = 10
    city_locations = []
    city_radius = 30

    canvas_width = 2*canvas_padding + (max_cities_horizontally-1)*vertical_inpad*city_radius + 2*city_radius
    canvas_height = 2*canvas_padding + (max_cities_vertically-1)*horizontal_inpad*city_radius + 2*city_radius

    for i in range(number_of_cities) :
        if i == 0 :
            x_location = city_radius+canvas_padding
            y_location = city_radius+canvas_padding
            current_location = (x_location,y_location)
            city_locations.append(current_location)
        else :
            if i % 2 == 0 :
                previousX = city_locations[i-2][0]
                x_location = previousX + vertical_inpad*city_radius
                y_location = city_locations[i-2][1]
                current_location = (x_location,y_location)
                city_locations.append(current_location)
            else :
                previousX = city_locations[i-1][0]
                x_location = previousX
                y_location = city_locations[i-1][1] + horizontal_inpad*city_radius
                current_location = (x_location,y_location)
                city_locations.append(current_location)
                
    svg_city_circles = "    <!-- City Circles -->\n"
    for count, current_location in enumerate(city_locations) :
        current_node_id = count+1
        if current_node_id in nodes_to_be_colored :
            svg_city_circles += f"    <ellipse stroke=\"black\" stroke-width=\"1\" cx=\"{current_location[0]}\" cy=\"{current_location[1]}\" rx=\"30\" ry=\"30\" style=\"fill: rgb(255, 255, 255); stroke: rgb(255, 0, 0); stroke-width: 14px;\"/>\n"
        else :
            svg_city_circles += f"    <ellipse stroke=\"black\" stroke-width=\"1\" cx=\"{current_location[0]}\" cy=\"{current_location[1]}\" rx=\"30\" ry=\"30\" style=\"fill: rgb(255, 255, 255);\"/>\n"

    city_labels = "    <!-- City Labels -->\n"
    for count, current_location in enumerate(city_locations) :
        city_labels += f"    <text x=\"{current_location[0]}\" y=\"{current_location[1]+horizontal_inpad}\" font-family=\"Times New Roman\" font-size=\"20\" style=\"white-space: pre; text-anchor: middle; dominant-baseline: middle;\">{count+1}</text>\n"

    svgStart = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    svgSetting = f"<svg width=\"{canvas_width}\" height=\"{canvas_height}\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\">"
    svgEnd = "</svg>"

    edges = "\n    <!-- Edges -->\n"
    for i in range(number_of_cities) :
        for j in range(number_of_cities) :
            if i != j and abs(i-j) <= 3:
                current_path = (i+1, j+1)
                if current_path in weights_to_be_colored :
                    edges += f"    <line x1=\"{city_locations[i][0]}\" y1=\"{city_locations[i][1]}\" x2=\"{city_locations[j][0]}\" y2=\"{city_locations[j][1]}\" style=\"stroke: rgb(255, 0, 0); stroke-width: 10px;\"/>\n"
                else :
                    edges += f"    <line x1=\"{city_locations[i][0]}\" y1=\"{city_locations[i][1]}\" x2=\"{city_locations[j][0]}\" y2=\"{city_locations[j][1]}\" stroke=\"black\" stroke-width=\"1\"/>\n"
                

    edge_labels = "    <!-- Edge Labels -->\n"
    for i in range(number_of_cities) :
        for j in range(number_of_cities) :
            if i != j and abs(i-j) <= 3:
                edge_labels += f"    <text x=\"{(city_locations[i][0]+city_locations[j][0])/2}\" y=\"{(city_locations[i][1]+city_locations[j][1])/2+horizontal_inpad}\" font-family=\"Times New Roman\" font-size=\"20\" style=\"white-space: pre; text-anchor: middle; dominant-baseline: middle;\">{i+j+2}</text>\n"

    edge_label_circles = "    <!-- Edge Label Circles -->\n"
    for i in range(number_of_cities) :
        for j in range(number_of_cities) :
            if i != j and abs(i-j) <= 3:
                current_path = (i+1, j+1)
                if current_path in weights_to_be_colored : 
                    edge_label_circles += f"    <ellipse stroke=\"black\" stroke-width=\"1\" cx=\"{((city_locations[i][0]+city_locations[j][0])/2)}\" cy=\"{((city_locations[i][1]+city_locations[j][1])/2)}\" rx=\"15\" ry=\"15\" style=\"fill: rgb(255, 255, 255); stroke-dasharray: 2px; stroke: rgb(255, 0, 0); stroke-width: 12px;\"/>\n"
                else :
                    edge_label_circles += f"    <ellipse stroke=\"black\" stroke-width=\"1\" cx=\"{((city_locations[i][0]+city_locations[j][0])/2)}\" cy=\"{((city_locations[i][1]+city_locations[j][1])/2)}\" rx=\"15\" ry=\"15\" style=\"fill: rgb(255, 255, 255); stroke-dasharray: 2px;\"/>\n"

    def create_svg(args) :
        svg = ""
        for arg in args :
            svg += arg
            svg += "\n"

        return svg

    svg = create_svg([svgStart, svgSetting, edges, svg_city_circles, city_labels, edge_label_circles, edge_labels, svgEnd])

    with open(VISUAL_SVG_OUTPUT_PATH, "w") as file :
        file.write(svg)

    drawing = svg2rlg(VISUAL_SVG_OUTPUT_PATH)
    renderPM.drawToFile(drawing, VISUAL_PNG_OUTPUT_PATH, fmt="PNG", dpi=250)