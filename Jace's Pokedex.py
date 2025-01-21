import tkinter as tk
from tkinter import messagebox
import requests

def show_pokedex():
    welcome_frame.pack_forget()
    pokedex_frame.pack(expand=True)

def get_data():
    pokemon = pokemon_entry.get()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        name = data['name'].capitalize()
        abilities = ", ".join([ability['ability']['name'] for ability in data['abilities']])
        types = ", ".join([t['type']['name'].capitalize() for t in data['types']])
        species_url = data['species']['url']

        species_response = requests.get(species_url)
        species_response.raise_for_status()
        species_data = species_response.json()
        description = species_data['flavor_text_entries'][0]['flavor_text'].replace("\n", " ")

        pokemon_name_label.config(text=f"Name: {name}")
        pokemon_abilities_label.config(text=f"Abilities: {abilities}")
        pokemon_type_label.config(text=f"Type: {types}")
        pokemon_description_label.config(text=f"Description: {description}")

    except requests.exceptions.HTTPError as errh:
        messagebox.showerror("HTTP Error", f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        messagebox.showerror("Connection Error", f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        messagebox.showerror("Timeout Error", f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Request Error", f"Something went wrong: {err}")
    except KeyError:
        messagebox.showerror("Error", f"Could not find data for Pokémon '{pokemon}'.")

def close_app():
    root.destroy()

root = tk.Tk()
root.title("Jace's Pokedex")
root.geometry("360x640")
root.resizable(False, False)
root.config(bg="#f1f1f1")

welcome_frame = tk.Frame(root, bg="#f1f1f1")
welcome_frame.pack(expand=True)

welcome_label = tk.Label(welcome_frame, text="Welcome to Jace's Pokedex", font=("Arial", 18), bg="#f1f1f1")
welcome_label.pack(pady=100)

start_button = tk.Button(welcome_frame, text="Start", font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, relief="solid", command=show_pokedex)
start_button.pack(pady=20, ipadx=40, ipady=10)

pokedex_frame = tk.Frame(root, bg="#f1f1f1")

pokemon_label = tk.Label(pokedex_frame, text="Pokémon Name", font=("Arial", 16), bg="#f1f1f1")
pokemon_label.pack(pady=20)

pokemon_entry = tk.Entry(pokedex_frame, font=("Arial", 14), bd=0, relief="solid", width=20, justify="center")
pokemon_entry.pack(pady=10)

clear_button = tk.Button(pokedex_frame, text="Clear", font=("Arial", 14), bg="#ff6347", fg="white", bd=0, relief="solid", command=lambda: pokemon_entry.delete(0, tk.END))
clear_button.pack(pady=10, ipadx=20, ipady=5)

get_data_button = tk.Button(pokedex_frame, text="Get Data", font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, relief="solid", command=get_data)
get_data_button.pack(pady=10, ipadx=20, ipady=5)

pokemon_name_label = tk.Label(pokedex_frame, text="Name: N/A", font=("Arial", 14), bg="#f1f1f1")
pokemon_name_label.pack(pady=10)

pokemon_abilities_label = tk.Label(pokedex_frame, text="Abilities: N/A", font=("Arial", 14), bg="#f1f1f1")
pokemon_abilities_label.pack(pady=10)

pokemon_type_label = tk.Label(pokedex_frame, text="Type: N/A", font=("Arial", 14), bg="#f1f1f1")
pokemon_type_label.pack(pady=10)

pokemon_description_label = tk.Label(pokedex_frame, text="Description: N/A", font=("Arial", 14), bg="#f1f1f1", wraplength=300)
pokemon_description_label.pack(pady=10)

close_button = tk.Button(pokedex_frame, text="Close", font=("Arial", 14), bg="#d32f2f", fg="white", bd=0, relief="solid", command=close_app)
close_button.pack(pady=20, ipadx=20, ipady=5)

root.mainloop()
