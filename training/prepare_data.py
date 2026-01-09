import json
import random
import pandas as pd
from pathlib import Path
import gc

# Raw data ka path aur output directory
# File name change kiya hai - interview_questions.json (plural)
RAW_PATH = "../data/raw/interview_questions.json"
OUT_DIR = "../data/processed"

# Output directory banaye agar nahi hai to
Path(OUT_DIR).mkdir(exist_ok=True)

# Generic answers jo candidates dete hain jab unko pata nahi hota
GENERIC_ANSWERS = [
    "I am not sure about this.",
    "I would try my best.",
    "This depends on the situation.",
    "I need to think about this.",
    "Let me consider this carefully."
]

print("Loading JSON file...")
# Large file ko load karo - yeh thoda time lega
with open(RAW_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total questions loaded: {len(data)}")

rows = []
total_processed = 0

# Har question ke liye different types ke answers generate karo
# Large dataset hai to progress dikhate raho
for idx, item in enumerate(data):
    q = item.get("question", "")
    ideal = item.get("ideal_answer", "")
    keywords_list = item.get("keywords", [])
    keywords = " ".join(keywords_list) if keywords_list else ""
    
    # Agar question ya ideal_answer empty hai to skip karo
    if not q or not ideal:
        continue
    
    # Ideal answer - yeh perfect answer hai, isko 1.0 score milega
    rows.append([q, ideal, ideal, 1.0])
    
    # Truncated answer - ideal answer ka aadha part, thoda kam score
    if len(ideal) > 20:  # Minimum length check
        rows.append([q, ideal, ideal[:len(ideal)//2], 0.7])
    
    # Keyword-based answer - sirf keywords, medium score
    if keywords:
        rows.append([q, ideal, keywords, 0.6])
    
    # Generic answer - jo candidates dete hain, low score
    rows.append([q, ideal, random.choice(GENERIC_ANSWERS), 0.3])
    
    total_processed += 1
    
    # Progress dikhao har 100k questions pe
    if (idx + 1) % 100000 == 0:
        print(f"Processed {idx + 1} questions, generated {len(rows)} rows so far...")
        # Memory management - agar rows zyada ho jaye to flush karo
        if len(rows) > 1000000:
            # Partial save karo taaki memory free ho
            temp_df = pd.DataFrame(rows, columns=["question", "ideal_answer", "candidate_answer", "label"])
            temp_df = temp_df.sample(frac=1).reset_index(drop=True)
            # Append to file instead of keeping in memory
            if not Path(f"{OUT_DIR}/train_temp.csv").exists():
                temp_df.to_csv(f"{OUT_DIR}/train_temp.csv", index=False, mode='w')
            else:
                temp_df.to_csv(f"{OUT_DIR}/train_temp.csv", index=False, mode='a', header=False)
            rows = []
            gc.collect()

print(f"Total questions processed: {total_processed}")
print(f"Total rows generated: {len(rows)}")

# Final rows ko DataFrame mein convert karo
if rows:
    final_df = pd.DataFrame(rows, columns=["question", "ideal_answer", "candidate_answer", "label"])
    
    # Agar temp file hai to usko bhi load karo
    if Path(f"{OUT_DIR}/train_temp.csv").exists():
        print("Loading temporary file and combining...")
        temp_df = pd.read_csv(f"{OUT_DIR}/train_temp.csv")
        final_df = pd.concat([temp_df, final_df], ignore_index=True)
        # Temp file delete karo
        Path(f"{OUT_DIR}/train_temp.csv").unlink()
    
    print("Shuffling data...")
    # Data ko shuffle karo taaki random order mein ho
    final_df = final_df.sample(frac=1).reset_index(drop=True)
    
    print("Splitting into train and validation...")
    split = int(0.9 * len(final_df))
    
    # 90% training, 10% validation mein split karo
    train_df = final_df[:split]
    val_df = final_df[split:]
    
    print(f"Saving train.csv with {len(train_df)} rows...")
    train_df.to_csv(f"{OUT_DIR}/train.csv", index=False)
    
    print(f"Saving val.csv with {len(val_df)} rows...")
    val_df.to_csv(f"{OUT_DIR}/val.csv", index=False)
    
    print(f"Data prepared successfully!")
    print(f"Training samples: {len(train_df)}")
    print(f"Validation samples: {len(val_df)}")
    print(f"Total samples: {len(final_df)}")
else:
    print("No rows generated. Please check the input file.")
