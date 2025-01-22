
def play_music():
    """Plays music from a predefined directory."""
    # Replace with the path to your music folder
    music_dir = "C:\\notjustmusic"  # Update this with your actual music folder path

    try:
        songs = os.listdir(music_dir)  # List all files in the music directory
        if not songs:
            speak("Your music folder is empty. Please add some songs and try again.")
            return

        # Ask if the user wants a specific song or a random one
        speak("Do you want to play a specific song or a random one?")
        choice = take_command()
        if choice is None:
            speak("I didn't catch your choice. Playing a random song.")
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song} for you.")
            return

        if "specific" in choice:
            speak("Please tell me the name of the song.")
            song_name = take_command()
            if song_name:
                for song in songs:
                    if song_name.lower() in song.lower():
                        os.startfile(os.path.join(music_dir, song))
                        speak(f"Playing {song_name} for you.")
                        return
                speak(f"I couldn't find the song {song_name} in your music folder.")
            else:
                speak("Sorry, I didn't catch the name of the song. Playing a random song.")
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))
                speak(f"Playing {song} for you.")
        elif "random" in choice:
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song} for you.")
        else:
            speak("I didn't understand your choice. Playing a random song.")
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))

    except Exception as e:
        speak("An error occurred while trying to play music.")
        print(f"Error: {e}")