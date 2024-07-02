import time
from datetime import date, timedelta
import sys
import win32gui
import mysql.connector


time_spent_on_apps = {}

def get_active_windows():
    active_windows = []
    toplist = []

    win32gui.EnumWindows(lambda hWnd, param: toplist.append((hWnd, win32gui.GetWindowText(hWnd))), None)

    for (hwnd, title) in toplist:
        if win32gui.IsWindowVisible(hwnd) and title != '':
            active_windows.append(title)
    active_windows = set(active_windows)
    active_windows = list(active_windows)
    active_windows.remove('Windows Input Experience')
    active_windows.remove('Program Manager')

    return active_windows

def update_database(time_spent_on_apps):

    current_date = date.today()-timedelta(days=1)
    connection = mysql.connector.connect(
        host = "localhost", 
        username="root", 
        password="password", 
        database="time_monitor")
    cursor = connection.cursor()
    query = "INSERT INTO time_spent (date, app_name, time) VALUES (%s, %s, %s)"
    for app_name, minutes in time_spent_on_apps.items():
        values = (current_date, app_name, minutes)
        cursor.execute(query, values)
           
    connection.commit() 
    cursor.close()
    connection.close()

def main():
    global time_spent_on_apps
    
    # start_time = 22  # 9 am
    # end_time = 25   # 11 pm
    today_date = date.today()
    
    #list of apps for manual checking   
    list_of_apps_to_confirm = ['YouTube', 'uTorrent', 'Chess', 'Windows PowerShell']

    while True:

        current_time = time.localtime().tm_hour  # Get the current hour

        other_checker = False
        confirm_app_checker = False
            
        # Check if the current time is within the desired range
        # if start_time <= current_time < end_time:

        active_windows = get_active_windows()
        for i in range(len(active_windows)):
            
            for app in range(0, len(list_of_apps_to_confirm)):
                if list_of_apps_to_confirm[app] in active_windows[i]:
                    time_spent_on_apps.setdefault(list_of_apps_to_confirm[app], 0)
                    time_spent_on_apps[list_of_apps_to_confirm[app]] += 1
                    confirm_app_checker = True

            if ( not confirm_app_checker ):
                if ('-' in active_windows[i]):
                    split_values = str(active_windows[i]).split('-')
                    extracted_value = split_values[-1].strip()
                    time_spent_on_apps.setdefault(extracted_value, 0)
                    time_spent_on_apps[extracted_value] += 1
                else:
                    if not other_checker:
                        time_spent_on_apps.setdefault('Others', 0)
                        time_spent_on_apps['Others'] += 1
                        other_checker = True
                            
        confirm_app_checker = False
        other_checker = False
        
        if date.today() != today_date:
            update_database(time_spent_on_apps)      
            time_spent_on_apps = {}
            today_date = date.today()
        
        # Wait for 1 minute before checking again
        time.sleep(60)
          
main()