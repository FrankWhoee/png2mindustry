from queue import Queue
import math
from PIL import Image
from numpy import asarray
import numpy as np

# image_path = input("Path for image: ")
# display_size = input("Display size? (l/s): ")
# while (display_size != "l") and (display_size != "s"):
#     print("Invalid input for display size. must be l or s.")
#     display_size = input("Display size? (l/s): ")
# output_path = input("Output save location?: ")

image_path = "idealflag.png"

image = Image.open(image_path)
data = asarray(image)


def get_neighbours(graph, node):
    output = []
    if not node[0] == 0:
        output.append((node[0] - 1, node[1]))
    if not node[1] == 0:
        output.append((node[0], node[1] - 1))
    if not node[0] == graph.shape[0] - 1:
        output.append((node[0] + 1, node[1]))
    if not node[1] == graph.shape[1] - 1:
        output.append((node[0], node[1] + 1))
    return output


def within_threshold(reference, colour, threshold):
    # Euclidean calculation for distance between colour, using the pythagorean theorem
    colour_distance = math.sqrt(
        ((int(reference[0]) - int(colour[0])) ** 2) + ((int(reference[1]) - int(colour[1])) ** 2 )+ ((int(reference[2]) - int(colour[2])) ** 2))
    # Since threshold is 0 < x < 1, we express the distance as a percentage. ~441.67 is the maximum distance a colour
    # can have. The higher the threshold, the more colours we accept. A threshold of 1 would include all colours and a
    # threshold of 0 would include none.
    return (colour_distance / 441.67295593006) <= threshold


def find_blotch(start, graph, threshold, output_array):
    # Simple breadth first search. Frontier expands until it can no longer find colours within the threshold to the
    # start colour. Marks a given 2d array with the start colour. Goal is to simplify the array so it can be
    # described with less information.
    frontier = Queue()
    reached = set()
    frontier.put(start)
    reached.add(start)

    while not frontier.empty():
        current = frontier.get()
        for next in get_neighbours(graph, current):
            if next not in reached and within_threshold(graph[start[0]][start[1]], graph[next[0]][next[1]], threshold):
                frontier.put(next)
                reached.add(next)
                output_array[next[0]][next[1]] = graph[start[0]][start[1]]
    return output_array



# def convert_array_to_commands(input_array):
# Converts a given input 2d array to list of commands in Mindustry.
print(data[0][0])
output = np.full(data.shape, 255)
print(output[0][0])
img = Image.fromarray(output, 'RGBA')
img.show()
output = find_blotch((0, 0), data, 0.1, output)
for i in range(output.shape[0]):
    string = ""
    for k in range(output.shape[1]):
        if output[i][k][0] == 255 and output[i][k][1] == 255 and output[i][k][2] == 255:
            string += "w "
        elif output[i][k][0] == 255 and output[i][k][1] == 0 and output[i][k][2] == 0:
            string += "r "
        elif output[i][k][0] == 0 and output[i][k][1] == 0 and output[i][k][2] == 255:
            string += "b "
    print(string)
print(data)
print("----------------------")
print(output)

