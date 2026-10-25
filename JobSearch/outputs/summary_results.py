import pandas as pd
import os

print(os.getcwd())

file = pd.read_csv('./JobSearch/outputs/test1_output_file.csv')

REVIEW_COLS = ["site", "query", "title", "company", "location",
               "is_remote", "date_posted", "min_amount", "max_amount", "job_url"]

file[REVIEW_COLS].to_csv("./JobSearch/outputs/jobs_review.csv", index=False)

print(file["site"].value_counts())
print(file["location"].value_counts())
print(file["title"].value_counts().head(30))