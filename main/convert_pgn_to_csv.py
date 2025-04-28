import chess.pgn
import csv

pgn_file_path = r"C:\Users\James\OneDrive\Desktop\GitHub\group4_project\raw_data\lichess_db_standard_rated_2017-04.pgn"
output_csv_path = "filtered_chess_games.csv"

def is_valid_game(headers, elo_threshold=200):
    try:
        # Filter: Event must be classical
        if headers.get("Event") != "Rated Classical game":
            return False

        # Filter: No draws
        if headers.get("Result") == "1/2-1/2":
            return False

        # Filter: Rating differences within bounds
        white_elo = int(headers.get("WhiteElo", 0))
        black_elo = int(headers.get("BlackElo", 0))
        if abs(white_elo - black_elo) > elo_threshold:
            return False

        # Filter: No major rating shifts (no newcomers)
        white_diff = int(headers.get("WhiteRatingDiff", 0))
        black_diff = int(headers.get("BlackRatingDiff", 0))
        if abs(white_diff) > 50 or abs(black_diff) > 50:
            return False

        return True

    except (ValueError, TypeError):
        return False  # Skip if parsing fails

# Open PGN and CSV files
with open(pgn_file_path, "r", encoding="utf-8") as pgn_file, \
     open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:

    fieldnames = ["Event", "White", "Black", "Result",
                  "WhiteElo", "BlackElo", "WhiteRatingDiff",
                  "BlackRatingDiff", "Opening", "TimeControl", "Moves"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    kept_count = 0  # To track how many games are kept

    while True:
        try:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            headers = game.headers

            if not is_valid_game(headers):
                continue

            moves_str = game.accept(
                chess.pgn.StringExporter(headers=False, variations=False, comments=False)
            ).strip()

            row = {
                "Event": headers.get("Event"),
                "White": headers.get("White"),
                "Black": headers.get("Black"),
                "Result": headers.get("Result"),
                "WhiteElo": headers.get("WhiteElo"),
                "BlackElo": headers.get("BlackElo"),
                "WhiteRatingDiff": headers.get("WhiteRatingDiff"),
                "BlackRatingDiff": headers.get("BlackRatingDiff"),
                "Opening": headers.get("Opening"),
                "TimeControl": headers.get("TimeControl"),
                "Moves": moves_str,
            }

            writer.writerow(row)
            kept_count += 1

            if kept_count % 1000 == 0:
                
                print(f"Saved {kept_count} games...")

        except Exception as e:
            
            print(f"Skipping game due to error: {e}")
            
            continue

print(f"Processed all games, kept {kept_count} valid ones.")
