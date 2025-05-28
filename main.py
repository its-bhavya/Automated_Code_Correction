from dotenv import load_dotenv
import os
import dspy

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

lm = dspy.LM("gemini/gemini-2.5-flash-preview-05-20", api_key=api_key)
dspy.configure(lm=lm)

