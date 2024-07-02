import tkinter as tk
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import customtkinter
import matplotlib.pyplot as plt
from datetime import date, timedelta



def fetch_time_spent():
    selected_date = date_entry.get()

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host = "localhost", 
        username="root", 
        password="", 
        database="")
    cursor = conn.cursor()

    
    query = "SELECT app_name, time FROM time_spent WHERE date = %s ORDER BY time DESC;"
    cursor.execute(query, (selected_date,))
    app_data = cursor.fetchall()

    clear_results()
    
    # Extract the app names and times from the retrieved data
    app_names = [app_name for app_name, _ in app_data]
    times = [time for _, time in app_data]


    # Create a bar graph
    fig = plt.figure(figsize=(8, 6))
    plt.barh(app_names, times)
    plt.xlabel('App Name')
    plt.ylabel('Time (minutes)')
    plt.title('Time Spent on Apps')
    plt.xticks(rotation=90)

    # Embed the graph in the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Close the database connection
    cursor.close()
    conn.close()


def clear_results():
    for widget in result_frame.winfo_children():
        widget.destroy()

def show_calendar():
    top = tk.Toplevel(window)

    cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=20)

    def set_date():
        selected_date = cal.get_date()
        date_entry.delete(0, tk.END)
        date_entry.insert(0, selected_date)
        top.destroy()

        fetch_time_spent()

    select_button = customtkinter.CTkButton(master=top, text="Select Date", command=set_date)
    select_button.pack(pady=10)
    
    

# Create the main window
window = customtkinter.CTk()
window.title("Time Monitoring App")
window.geometry("800x600")
window.config(bg="white")



# Date selection
date_label = customtkinter.CTkLabel(master=window, text="Select Date:", bg_color="white")
date_label.grid(row=0, column=0, padx=10, pady=0, sticky="e")

date_entry = customtkinter.CTkEntry(master=window)
date_entry.insert(0, date.today()-timedelta(days=1))
date_entry.grid(row=0, column=1, padx=10, pady=0, sticky="w")

calendar_button = customtkinter.CTkButton(master=window, text="Calendar", command=show_calendar, width=8, height=1)
calendar_button.grid(row=0, column=2, padx=10, pady=0, sticky="w")


# Frame to display the results
result_frame = customtkinter.CTkFrame(master=window,width=600, height=500, bg_color="white")
result_frame.grid(row=2, column=0, columnspan=5)
result_frame.grid_rowconfigure(0, weight=1)
result_frame.grid_columnconfigure(0, weight=1)

# Center-align all elements
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(3, weight=1)

fetch_time_spent()

# Run the GUI main loop
window.mainloop()
