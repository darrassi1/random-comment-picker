import random
import csv
import json
import re
from typing import List


class CommentPicker:
    def __init__(self):
        self.comments: List[str] = []

    # -----------------------------
    # LOADERS
    # -----------------------------
    def load_from_list(self, comments: List[str]):
        self.comments.extend(comments)

    def load_from_txt(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            self.comments.extend(lines)

    def load_from_csv(self, file_path: str, column_name: str):
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if column_name in row and row[column_name].strip():
                    self.comments.append(row[column_name].strip())

    def load_from_json(self, file_path: str, key: str):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                if key in item:
                    self.comments.append(item[key].strip())

    # -----------------------------
    # CLEANING
    # -----------------------------
    def remove_duplicates(self):
        self.comments = list(set(self.comments))

    def filter_by_keyword(self, keyword: str):
        self.comments = [c for c in self.comments if keyword.lower() in c.lower()]

    def remove_short_comments(self, min_length: int = 3):
        self.comments = [c for c in self.comments if len(c) >= min_length]

    def clean_special_characters(self):
        self.comments = [re.sub(r'[^\w\s]', '', c) for c in self.comments]

    # -----------------------------
    # RANDOM SELECTION
    # -----------------------------
    def pick_one(self) -> str:
        if not self.comments:
            raise ValueError("No comments available")
        return random.choice(self.comments)

    def pick_multiple(self, n: int) -> List[str]:
        if n > len(self.comments):
            raise ValueError("Not enough comments")
        return random.sample(self.comments, n)

    # -----------------------------
    # EXPORT
    # -----------------------------
    def save_results(self, results: List[str], file_path: str):
        with open(file_path, "w", encoding="utf-8") as f:
            for r in results:
                f.write(r + "\n")

    # -----------------------------
    # DEBUG
    # -----------------------------
    def stats(self):
        print(f"Total comments: {len(self.comments)}")


# -----------------------------
# USAGE EXAMPLE
# -----------------------------
if __name__ == "__main__":
    picker = CommentPicker()

    # Load comments
    picker.load_from_txt("comments.txt")
    # picker.load_from_csv("comments.csv", "comment")
    # picker.load_from_json("comments.json", "text")

    # Clean data
    picker.remove_duplicates()
    picker.remove_short_comments(5)
    picker.clean_special_characters()

    # Optional filter (e.g. giveaway keyword)
    # picker.filter_by_keyword("giveaway")

    picker.stats()

    # Pick winners
    winner = picker.pick_one()
    winners = picker.pick_multiple(3)

    print("\n🎉 Winner:")
    print(winner)

    print("\n🏆 Top 3 Winners:")
    for w in winners:
        print("-", w)

    # Save results
    picker.save_results(winners, "winners.txt")
