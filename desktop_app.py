'''
Author: Sarthak Pradhan
Date: 03/31/2023
Description: Desktop app to interface with openai to respond to queries and complete tasks
'''
import tkinter as tk
import json
import openai

# Create the main window
root = tk.Tk()
root.title("ChatGPT")


def generate_response(prompt):

    # Load the API key and organization name from the configuration file

    try:
        with open("settings.json") as f:
            settings = json.load(f)
            api_key = settings["api_key"]
            org_name = settings["org_name"]

    except:
        api_key = ""
        org_name = ""
    openai.api_key = api_key
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


# Define the send_message function
def send_message():

    input_text = input_box.get()
    response_text = generate_response(input_text)
    output_box.insert(tk.END, "You: " + input_text + "\n")
    output_box.insert(tk.END, "ChatGPT: " + response_text + "\n")
    input_box.delete(0, tk.END)


# Create the input box and send button
input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, padx=10, pady=10)
input_label = tk.Label(input_frame, text="Message:")
input_label.pack(side=tk.LEFT)
input_box = tk.Entry(input_frame, width=50)
input_box.pack(side=tk.LEFT)
send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

# Create the output box
output_frame = tk.Frame(root)
output_frame.pack(side=tk.TOP, padx=10, pady=10)
output_label = tk.Label(output_frame, text="ChatGPT:")
output_label.pack(side=tk.TOP)
output_box = tk.Text(output_frame, width=50, height=10)
output_box.pack(side=tk.TOP)


# Create the settings window
def open_settings():
    global settings_window
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    api_key_label = tk.Label(settings_window, text="API Key:")
    api_key_label.grid(row=0, column=0)
    api_key_entry = tk.Entry(settings_window)
    api_key_entry.grid(row=0, column=1)
    org_name_label = tk.Label(settings_window, text="Organization Name:")
    org_name_label.grid(row=1, column=0)
    org_name_entry = tk.Entry(settings_window)
    org_name_entry.grid(row=1, column=1)
    save_button = tk.Button(settings_window, text="Save",
                            command=lambda: save_settings(api_key_entry.get(), org_name_entry.get()))
    save_button.grid(row=2, column=1)


def save_settings(api_key, org_name):
    global settings_window
    settings = {"api_key": api_key, "org_name": org_name}
    with open("settings.json", "w") as f:
        json.dump(settings, f)
    settings_window.destroy()




# Create the settings button

settings_button = tk.Button(root, text="Settings", command=open_settings)
settings_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Start the main loop
root.mainloop()
