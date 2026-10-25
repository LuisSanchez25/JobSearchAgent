import time
import pandas as pd
from jobspy import scrape_jobs
from datetime import datetime


today = datetime.now()
search_terms = ['"data scientist"', '"machine learning engineer"', '"research scientist"']
frames = []

US = {"US", "USA", "United States"}

def location_ok(row, allowed_states={"CA"}, remote_ok=True):
    parts = [p.strip() for p in str(row["location"] or "").split(",")]
    country = parts[-1] if parts else ""
    state = parts[1] if len(parts) >= 3 else ""
    if remote_ok and row["is_remote"] == True and country in US:
        return True
    return state in allowed_states

for term in search_terms:
    df = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
        search_term=term,
        location="Sunnyvale, CA",
        distance=25,
        results_wanted=20,
        hours_old=72,
        country_indeed="USA",
    )
    df["query"] = term          # remember which search found it
    frames.append(df)
    time.sleep(10)              # be gentle; the boards block bursts

jobs = pd.concat(frames, ignore_index=True)
jobs = jobs.drop_duplicates(subset="job_url")
print(len(jobs))
jobs = jobs[jobs.apply(location_ok, axis=1)]

jobs.to_csv(f'./JobSearch/outputs/test_{today.year}_{today.month}_{today.day}_output_file.csv', index=False)

## Need this for now to check for errors ##
REVIEW_COLS = ["site", "query", "title", "company", "location",
               "is_remote", "date_posted", "min_amount", "max_amount", "job_url"]

jobs[REVIEW_COLS].to_csv(f"./JobSearch/outputs/test_{today.year}_{today.month}_{today.day}_jobs_review.csv", index=False)