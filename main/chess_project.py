import chess.pgn
import pandas as pd

# File path to your PGN file
pgn_file_path = r"C:\Users\James\OneDrive\Desktop\GitHub\group3_project\raw_data\lichess_db_standard_rated_2013-01.pgn"
output_csv_path = "chess_games.csv"

# List to store game data
games = []




# Open the PGN file and process games
with open(pgn_file_path, "r", encoding="utf-8") as pgn_file:
    while True:
        try:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # End of file

            headers = game.headers
            moves_uci = " ".join([move.uci() for move in game.mainline_moves()])  # Extract UCI moves

            games.append({
                "Event": headers.get("Event"),
                "Site": headers.get("Site"),
                "White": headers.get("White"),
                "Black": headers.get("Black"),
                "Result": headers.get("Result"),
                "UTCDate": headers.get("UTCDate"),
                "UTCTime": headers.get("UTCTime"),
                "WhiteElo": headers.get("WhiteElo"),
                "BlackElo": headers.get("BlackElo"),
                "WhiteRatingDiff": headers.get("WhiteRatingDiff"),
                "BlackRatingDiff": headers.get("BlackRatingDiff"),
                "ECO": headers.get("ECO"),
                "Opening": headers.get("Opening"),
                "TimeControl": headers.get("TimeControl"),
                "Termination": headers.get("Termination"),
                "Moves": moves_uci,  # Store UCI moves as a single string
            })

        except Exception as e:
            print(f"Error parsing game: {e}")
            continue  # Skip problematic games

# Convert to a pandas DataFrame
df = pd.DataFrame(games)

# Save to CSV
df.to_csv(output_csv_path, index=False, encoding="utf-8")

# Display DataFrame info
print(df.info())
print(df.head())

print(f"PGN conversion complete. Data saved to {output_csv_path}")
