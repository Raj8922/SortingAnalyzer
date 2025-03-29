import ttkbootstrap as ttkb
import random
import time
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sorting algorithms (with timing included)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) - 1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def counting_sort(arr):
    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1
    count = [0] * range_of_elements
    output = [0] * len(arr)

    for i in range(len(arr)):
        count[arr[i] - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1

    for i in range(len(arr)):
        arr[i] = output[i]

# Function to generate random numbers
def generate_random_numbers(num_count, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(num_count)]

# Function to insert results in the Treeview table
def update_treeview(tree, algorithm_metrics):
    for row in tree.get_children():
        tree.delete(row)

    for algorithm, time_taken, space_complexity in algorithm_metrics:
        tree.insert("", "end", values=(algorithm, f"{time_taken:.6f}", space_complexity))

# Save the unsorted and sorted numbers to text files
def save_to_files(unsorted_numbers, sorted_numbers=None):
    with open("unsorted_numbers.txt", "w") as f:
        f.write("\n".join(map(str, unsorted_numbers)))

    if sorted_numbers:
        with open("sorted_numbers.txt", "w") as f:
            f.write("\n".join(map(str, sorted_numbers)))

# Function to create and show a Toplevel window with file content
def show_file_in_toplevel(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()

        top = Toplevel(win)
        top.title(f"Contents of {filename}")
        top.geometry("600x400")

        text_widget = Text(top, font=("Helvetica", 12), wrap=WORD)
        text_widget.pack(fill=BOTH, expand=True)
        text_widget.insert(INSERT, content)
        text_widget.config(state=DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"Could not read the file: {e}")

# Function to generate a graph of sorting times
def generate_graph():
    algorithms = [algorithm for algorithm, _, _ in algorithm_metrics]
    times = [time_taken for _, time_taken, _ in algorithm_metrics]

    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, times, color='skyblue')
    plt.xlabel('Time Taken (seconds)')
    plt.title('Sorting Algorithms Time Comparison')

    top = Toplevel(win)
    top.title("Sorting Algorithms Time Comparison")
    top.geometry("800x600")

    canvas = FigureCanvasTkAgg(plt.gcf(), top)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    canvas.draw()

# Function to generate a graph of space complexities
def generate_space_complexity_graph():
    algorithms = [algorithm for algorithm, _, _ in algorithm_metrics]
    space = [space_complexities[algorithm] for algorithm in algorithms]

    complexity_map = {
        "O(1)": 1,
        "O(log n)": 2,
        "O(n)": 3,
        "O(n log n)": 4,
        "O(k + n)": 5,
    }
    space_values = [complexity_map[s] for s in space]

    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, space_values, color='lightcoral')
    plt.xlabel('Space Complexity (Numerical Scale)')
    plt.title('Sorting Algorithms Space Complexity Comparison')

    top = Toplevel(win)
    top.title("Sorting Algorithms Space Complexity Comparison")
    top.geometry("800x600")

    canvas = FigureCanvasTkAgg(plt.gcf(), top)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    canvas.draw()

space_complexities = {
    "Selection Sort": "O(1)",
    "Quick Sort": "O(log n)",
    "Merge Sort": "O(n)",
    "Heap Sort": "O(1)",
    "Bubble Sort": "O(1)",
    "Insertion Sort": "O(1)",
    "Counting Sort": "O(k + n)"
}

def main():
    global algorithm_metrics
    fastest_algorithm = None

    try:
        num_count = int(entry_num_count.get())
        min_val = int(entry_min_val.get())
        max_val = int(entry_max_val.get())

        if num_count <= 0 or min_val >= max_val:
            raise ValueError("Number count must be positive and min value must be less than max value.")

    except ValueError as e:
        messagebox.showerror("Input Error", f"Error: {e}")
        return

    random_numbers_list = generate_random_numbers(num_count, min_val, max_val)
    save_to_files(random_numbers_list)

    algorithms = [
        ("Selection Sort", selection_sort),
        ("Quick Sort", quick_sort),
        ("Merge Sort", merge_sort),
        ("Heap Sort", heap_sort),
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Counting Sort", counting_sort),
    ]

    algorithm_metrics = []

    for name, sort_func in algorithms:
        arr_copy = random_numbers_list.copy()

        start_time = time.time()
        sorted_arr = sort_func(arr_copy)
        end_time = time.time()

        sort_time = end_time - start_time
        space_complexity = space_complexities[name]
        algorithm_metrics.append((name, sort_time, space_complexity))
        save_to_files(random_numbers_list, sorted_arr)

    fastest_algorithm = min(algorithm_metrics, key=lambda x: x[1])[0]
    update_treeview(tree, algorithm_metrics)
    fastest_label.config(text=f"Most Efficient Algorithm: {fastest_algorithm}")

win = Tk()
win.title('Sorting Algorithms')
win.attributes('-alpha', 0.9)
win['bg'] = 'light yellow'
win.geometry('800x600')

entry_num_count = StringVar()
entry_min_val = StringVar()
entry_max_val = StringVar()

label1 = Label(win, text="Sorting Algorithms Complexity", font=("Helvetica", 20, "bold"), bg="light yellow")
label1.place(relx=0.5, anchor='n')

label1 = Label(win, text="Number of element for Array : ", font=(15), bg="light yellow")
label1.place(x=100, y=50)

entery1 = Entry(win, font=(15), cursor="plus", justify="left", bd=3, textvariable=entry_num_count)
entery1.place(x=450, y=50)

label2 = Label(win, text="Minimum value of Array", font=(15), bg="light yellow")
label2.place(x=100, y=90)

entery2 = Entry(win, font=(15), cursor="plus", justify="left", bd=3, textvariable=entry_min_val)
entery2.place(x=450, y=90)

label3 = Label(win, text="Maximum value of Array", font=(15), bg="light yellow")
label3.place(x=100, y=130)

entery3 = Entry(win, font=(15), cursor="plus", justify="left", bd=3, textvariable=entry_max_val)
entery3.place(x=450, y=130)

generate_button = ttkb.Button(win, text="Generate and Sort", bootstyle="success", command=main, padding=(10, 5))
generate_button.place(x=100, y=180)

graph_button = ttkb.Button(win, text="Generate Time Complexity Graph", bootstyle="info", command=generate_graph, padding=(10, 5))
graph_button.place(x=100, y=230)

space_graph_button = ttkb.Button(win, text="Generate Space Complexity Graph", bootstyle="warning", command=generate_space_complexity_graph, padding=(10, 5))
space_graph_button.place(x=300, y=230)

unsorted_button = ttkb.Button(win, text="Show Unsorted Numbers", bootstyle="primary", command=lambda: show_file_in_toplevel("unsorted_numbers.txt"), padding=(10, 5))
unsorted_button.place(x=300, y=180)

sorted_button = ttkb.Button(win, text="Show Sorted Numbers", bootstyle="warning", command=lambda: show_file_in_toplevel("sorted_numbers.txt"), padding=(10, 5))
sorted_button.place(x=550, y=180)

col = ("algorithm", "time_taken", "space_complexity")
tree = ttk.Treeview(win, columns=col, show="headings", height=8)
tree.heading("algorithm", text="Algorithm")
tree.heading("time_taken", text="Time Taken (seconds)")
tree.heading("space_complexity", text="Space Complexity")

tree_scroll_y = Scrollbar(win, orient=VERTICAL, command=tree.yview)
tree_scroll_x = Scrollbar(win, orient=HORIZONTAL, command=tree.xview)
tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

tree.column("algorithm", width=250, anchor="center")
tree.column("time_taken", width=150, anchor="center")
tree.column("space_complexity", width=150, anchor="center")

tree.place(x=100, y=300, height=170, width=600)

fastest_label = Label(win, text="Most Efficient Algorithm for Array: Not calculated", font=("Helvetica", 18, "bold"), bg="light yellow")
fastest_label.place(x=100, y=500)

win.mainloop()
