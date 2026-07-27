def main():
    weather_data = {
        "London": "Cloudy",
        "Paris": "Sunny",
        "Tokyo": "Rainy",
        "New York": "Windy",
    }

    print("Weather App")
    print("Type a city name or 'list' or 'exit'.")

    while True:
        try:
            command = input("> ").strip().lower()
        except EOFError:
            break

        if command == "list":
            for city, condition in weather_data.items():
                print(f"{city}: {condition}")
        elif command == "exit":
            print("Goodbye!")
            break
        elif command in weather_data:
            print(f"{command}: {weather_data[command]}")
        else:
            print("City not found.")


if __name__ == "__main__":
    main()
