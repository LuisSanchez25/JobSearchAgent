from __future__ import annotations

import os
import sqlite3
import re
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# -------------------------------------------------
# loading the resources once 
#--------------------------------------------------


#------------------------------------
# Page
#------------------------------------

st.set_page_config(page_title="Personal Job Search",
                   page_icon="[?]", layout="wide")
 
st.title("Job Filter Search")
st.caption("Here I will select which jobs I will or won't apply to"
           "If I reject applying for a job I must write a reason why"
           "The LLM model can then take this info into account for"
           "future recomendations.")

# Here I will add the descriptions of the jobs I was looking at including location
# Pay if available, Maybe try to collect some data on who they hire? And apply ort reject
# Also need the application URL

# Here is the apply or reject buttom

will_apply = 5

left, right = st.columns(2)

if left.button("Apply"):
    will_apply = 1
    st.write("Good luck on this application!")
if right.button("Reject", type="primary"):
    will_apply = 0
    st.write("Please provide a reason on the field bellow to make better recomendation in the future")

st.text_input("Reason for declining the job")