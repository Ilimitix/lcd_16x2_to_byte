import tkinter as tk

# Callback function for clicking on a primary square
def primary_square_click(event):
    # Toggle the state of the primary square (0 becomes 1 and vice versa)
    if event.widget["bg"] == "white":
        event.widget.configure(bg="black")
    else:
        event.widget.configure(bg="white")

# Function to convert a block to a sequence of bytes
def convert_block_to_bytes(block):
    bytes_block = []
    for square in primary_squares[block]:
        if square["bg"] == "black":
            bytes_block.append(1)
        else:
            bytes_block.append(0)
    return bytes_block

# Function to convert a block to a formatted byte string
def convert_block_to_byte_string(block):
    bytes_block = convert_block_to_bytes(block)
    byte_string = "byte \"name\"[8] = {\n"  # Always display [8]
    for i in range(0, len(bytes_block), 5):
        line_bytes = bytes_block[i:i+5]
        line_str = ''.join(str(bit) for bit in line_bytes)
        byte_string += "B" + line_str + ",\n"
    byte_string += "};"
    return byte_string

# Conversion and display function for a specific block
def convert_and_display_block(block, text):
    byte_string = convert_block_to_byte_string(block)
    text.configure(state="normal")
    text.delete("1.0", tk.END)
    text.insert(tk.END, byte_string)
    text.configure(state="disabled")

# Function to clear the content of a block
def clear_block(block):
    for square in primary_squares[block]:
        square.configure(bg="white")

# Create the main window
window = tk.Tk()
window.title("LCD 16x2 to Byte Converter")

# Create a frame to hold the header
header_frame = tk.Frame(window)
header_frame.pack(pady=10)

# Create a label for the header
header_label = tk.Label(header_frame, text="Ilimitix", font=("Arial", 14, "bold"), fg="blue")
header_label.pack()

# Create a label for the date
date_label = tk.Label(header_frame, text="Date: 2023-05-26", font=("Arial", 12))
date_label.pack()

# Create a label for the program description
description_label = tk.Label(window, text="This program converts the state of each block in an LCD 16x2 display to a byte sequence.", font=("Arial", 12))
description_label.pack(pady=10)

# Create a frame to hold the grid
grid_frame = tk.Frame(window)
grid_frame.pack()

# Create a list to store the blocks
blocks = []

# Create a list to store the primary squares of each block
primary_squares = []

# Create two rows of eight blocks
for i in range(2):
    # Create eight blocks in each row
    for j in range(8):
        # Create a container for the block and buttons
        container = tk.Frame(grid_frame)
        container.grid(row=i, column=j, padx=5, pady=5)

        # Create the "Conv" button above for the first row and below for the second row
        if i == 0:
            convert_button = tk.Button(container, text="Conv", command=lambda b=i*8+j: convert_and_display_block(b, result_text))
            convert_button.pack(side="top", pady=5)
        else:
            convert_button = tk.Button(container, text="Conv", command=lambda b=i*8+j: convert_and_display_block(b, result_text))
            convert_button.pack(side="bottom", pady=5)

        # Create the "/" button to clear the block
        clear_button = tk.Button(container, text="/", command=lambda b=i*8+j: clear_block(b))
        clear_button.pack(side="top" if i == 0 else "bottom", pady=5)

        # Create the primary squares in the block
        primary_squares_block = []
        for k in range(8):
            row = tk.Frame(container)
            row.pack()

            # Create the primary squares in each row
            for l in range(5):
                square = tk.Frame(row, width=20, height=20, bg="white", borderwidth=1, relief="solid")
                square.pack(side="left", padx=2, pady=2)
                square.bind("<Button-1>", primary_square_click)
                primary_squares_block.append(square)

        primary_squares.append(primary_squares_block)
        blocks.append(container)

# Create a text area to display the result
result_text = tk.Text(window, width=40, height=10, state="disabled")
result_text.pack(pady=10)

# Start the main application loop
window.mainloop()
