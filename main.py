from Utilities import safe_start, safe_stop, visualize
from Algorithms import AStar, Dijkstra, MyGraph
import timeit
from Constants import RUN_CONFIG_FILE_PATH, SAVE_TIME_PLOT_PATH, SAVE_ITER_PLOT_PATH
import argparse
import json
import keyboard
from matplotlib import pyplot as plt

def execute(number_of_cities:int, start_city:int, destination_city:int) -> dict:
    """
    Function, executes one times for a given case, and returns the results.
    @params :
        number_of_cities    -   Required    :   The number of cities. (int)
        start_city          -   Required    :   The start city. (int)
        destination_city    -   Required    :   The destination city. (int)
    @return :
        A dictionary, containing the results of the execution. (dict)
    """

    graph_object = MyGraph(number_of_cities)
    graph_object.generate_graph()
    graph = graph_object.graph

    dijkstra_object = Dijkstra()
    start_of_dijkstra = timeit.default_timer()
    dijkstra_result = dijkstra_object.solve(graph, start_city, destination_city)
    end_of_dijkstra = timeit.default_timer()
    dijkstra_time = (round((end_of_dijkstra - start_of_dijkstra) * 10 ** 6, 3))

    a_star_object = AStar()
    start_of_a_star = timeit.default_timer()
    a_star_result = a_star_object.solve(graph, start_city, destination_city)
    end_of_a_star = timeit.default_timer()
    a_star_time = (round((end_of_a_star - start_of_a_star) * 10 ** 6, 3))

    state = (dijkstra_result[1] == a_star_result[1])

    return {
        "number_of_cities" : number_of_cities,
        "start_city" : start_city,
        "destination_city" : destination_city,
        "simulate_correct" : state,

        "dijkstra_time" : dijkstra_time,
        "dijkstra_path" : dijkstra_result[1],
        "dijkstra_cost" : dijkstra_result[2],
        "dijkstra_iterations" : dijkstra_result[3],

        "a_star_time" : a_star_time,
        "a_star_path" : a_star_result[1],
        "a_star_cost" : a_star_result[2],
        "a_star_iterations" : a_star_result[3],
    }

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r") -> None:
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  :   iterable object (Iterable)
        prefix      - Optional  :   prefix string (Str)
        suffix      - Optional  :   suffix string (Str)
        decimals    - Optional  :   positive number of decimals in percent complete (Int)
        length      - Optional  :   character length of bar (Int)
        fill        - Optional  :   bar fill character (Str)
        printEnd    - Optional  :   end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

def simulate(number_of_cities:int, is_continuously_generated:bool, start_city:int, destination_city:int) -> list:
    """
    Function, simulates the execution of the script for a given case.
    @params :
        number_of_cities            -   Required    :   The number of cities. (int)
        is_continuously_generated   -   Required    :   If this flag is set, the script will generate test cases continuously from 1 to N. (bool)
        start_city                  -   Required    :   The start city. (int)
        destination_city            -   Required    :   The destination city. (int)
    @return : 
        data                        -   Required    :   The result of the simulation. (list)
    """

    print("\n*** Simulation started.")
    data = []

    if not is_continuously_generated:
        data.append(execute(number_of_cities, start_city, destination_city))
    else:
        iterable = [i for i in range(1, number_of_cities + 1, 1)]
        for number_of_cities in progressBar(iterable, prefix = 'Simulating:', suffix = 'Complete', length = 50):
            try :
                data.append(execute(number_of_cities, 1, number_of_cities))
            except :
                print(f"** Error occured while generating test case {number_of_cities}. Program will skip this amount.")
            if keyboard.is_pressed("ESC") and keyboard.is_pressed("C") and keyboard.is_pressed("L") and keyboard.is_pressed("S") :
                print("** User stopped generating test cases. Program will now continue by results.")
                break

    return data

def visualize_data(result:list, number_of_cities:int, will_visualize_data:bool) -> str:
    """
    Method, visualizes the given data.
    @params :
        result                  -   Required    :   The result of the simulation. (list)
        number_of_cities        -   Required    :   The number of cities. (int)
        will_visualize_data     -   Required    :   If this flag is set, the script will visualize the data. (bool)
    @return :
        feedback                -   Required    :   The feedback of the visualization. (2*str)
    """

    if not will_visualize_data:
        return "No data visualization done."
    
    fb1 = visualize("Dijkstra", number_of_cities, result["dijkstra_path"])
    fb2 = visualize("AStar", number_of_cities, result["a_star_path"])

    return fb1, fb2

def plot_data(data:list, will_plot_data:bool, is_continuously_generated) -> str:
    """
    Method, that takes the dict results of executions. And creates two plots about Dijkstra VS AStar. In case of aXb, where a is y axis, and b is x axis.
    First, it plots : time X number of cities.
    Second, it plots : iterations X number of cities.
    After that, it saves the plots.
    @params :
        data                -   Required    :   The result of the simulation. (list)
        will_plot_data      -   Required    :   If this flag is set, the script will plot the data. (bool)
    @return :
        feedback            -   Required    :   The feedback of the plotting. (str)
    """

    if not will_plot_data or not is_continuously_generated:
        return "No data plotting done."

    # timeXcities

    plt.figure(figsize=(10, 10))
    plt.plot([i["number_of_cities"] for i in data], [i["dijkstra_time"] for i in data], label="Dijkstra")
    plt.plot([i["number_of_cities"] for i in data], [i["a_star_time"] for i in data], label="AStar")
    plt.xlabel("Number of Cities")
    plt.ylabel("Time (s)")
    plt.title("Time X Number of Cities")
    plt.legend()
    plt.tight_layout()
    plt.savefig(SAVE_TIME_PLOT_PATH)
    plt.close()

    # iterationsXcities
    plt.figure(figsize=(10, 10))
    plt.plot([i["number_of_cities"] for i in data], [max(i["dijkstra_iterations"].values()) for i in data], label="Dijkstra")
    plt.plot([i["number_of_cities"] for i in data], [max(i["a_star_iterations"].values()) for i in data], label="AStar")
    plt.xlabel("Number of Cities")
    plt.ylabel("Iterations")
    plt.title("Iterations X Number of Cities")
    plt.legend()
    plt.tight_layout()
    plt.savefig(SAVE_ITER_PLOT_PATH)
    plt.close()

    return "Data plotted successfully."
    

def main(number_of_cities:int, is_continuously_generated:bool, start_city:int, destination_city:int, will_save_data:bool, will_plot_data:bool, will_visualize_data:bool) -> None:
    """
    Main function of the script, IT drives through thw the program acording to the given parameters.
    @params :
        number_of_cities            -   Required    :   The number of cities. (int)
        is_continuously_generated   -   Required    :   If this flag is set, the script will generate test cases continuously from 1 to N. (bool)
        start_city                  -   Required    :   The start city. (int)
        destination_city            -   Required    :   The destination city. (int)
        will_save_data              -   Required    :   If this flag is set, the script will save the results in a file. (bool)
        will_plot_data              -   Required    :   If this flag is set, the script will plot the results. (bool)
    @return : 
        None
    """

    data = simulate(number_of_cities, is_continuously_generated, start_city, destination_city)

    fb = visualize_data(data[-1], number_of_cities, will_visualize_data)
    print("*** Visualization Output. ->", fb)
    
    fb = plot_data(data, will_plot_data, is_continuously_generated)
    print("*** Plotting Output. ->", fb)

if __name__ == "__main__":
    
    safe_start()

    parser = argparse.ArgumentParser(description="This script is used to compare the performance of the two well-known shortest path finder algorithms.")
    parser.add_argument("-n", "--number-of-cities", type=int, help="The number of cities in the graph.", required=False)
    parser.add_argument("-c", "--continuously-generate", type=int, help="If this flag is set, the script will generate test cases continuously from 1 to N.", required=False, default=False)
    parser.add_argument("-st", "--start-city", type=int, help="The start city.", required=False)
    parser.add_argument("-dt", "--destination-city", type=int, help="The destination city.", required=False)
    parser.add_argument("-s", "--save-to-file", type=int, help="If this flag is set, the results will be saved to a file.", required=False, default=False)
    parser.add_argument("-p", "--plot-results", type=int, help="If this flag is set, the results will be plotted.", required=False, default=False)
    args = parser.parse_args()

    number_of_cities = args.number_of_cities
    is_continuously_generated = args.continuously_generate
    start_city = args.start_city
    destination_city = args.destination_city
    will_save_data = args.save_to_file
    will_plot_data = args.plot_results

    if number_of_cities is None:
        with open(RUN_CONFIG_FILE_PATH, "r") as infile:
            configFile = json.load(infile)
        number_of_cities = configFile["number_of_cities"]
        is_continuously_generated = configFile["is_continuously_generated"]
        start_city = configFile["start_city"]
        destination_city = configFile["destination_city"]
        will_save_data = configFile["will_save_data"]
        will_plot_data = configFile["will_plot_data"]
    else:
        with open(RUN_CONFIG_FILE_PATH, "w") as outfile:
            json.dump({
                "number_of_cities": number_of_cities,
                "is_continuously_generated": is_continuously_generated,
                "start_city": start_city,
                "destination_city": destination_city,
                "will_save_data": will_save_data,
                "will_plot_data": will_plot_data
            }, outfile)

    will_visualize_data = (number_of_cities<=20)

    main(int(number_of_cities), bool(is_continuously_generated), int(start_city), int(destination_city), bool(will_save_data), bool(will_plot_data), bool(will_visualize_data))

    safe_stop()
