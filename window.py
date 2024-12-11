import tkinter as tk

def create_window(number):
    # Create a window for each number
    root = tk.Tk()
    root.title(f"Project {number}")
    
    label = tk.Label(root, text=f"This is project {number}")
    label.pack(padx=20, pady=20)

    button = tk.Button(root, text="Close", command=root.quit)
    button.pack(padx=10, pady=10)

    root.mainloop()

# Example of how to run the window with a specific number
if __name__ == "__main__":
    import sys
    number = sys.argv[1]  # Take the number as a command-line argument
    create_window(number)