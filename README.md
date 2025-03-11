# README: Taming LLMs with Groq API

## Project Overview
This project implements a content classification and analysis tool using the Groq API. The tool utilizes structured prompts, confidence analysis, and prompt strategy comparisons to optimize model behavior and extract meaningful insights from text data.

## Features
- **Basic Completion:** Generates AI responses to structured prompts.
- **Structured Completions:** Uses predefined formats with recognizable start and end markers.
- **Streaming Responses:** Implements controlled text generation with predefined stopping points.
- **Text Classification:** Assigns categories to input text using structured prompts.
- **Confidence Analysis:** Utilizes logprob data to filter low-confidence classifications.
- **Prompt Strategy Comparison:** Evaluates different prompting techniques for classification accuracy and response consistency.

## Installation
### Prerequisites
Ensure you have Python installed and set up a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```
### Install Dependencies
Run the following command to install required packages:
```bash
pip install -r requirments.txt
```

### API Key Setup
Create a `.env` file in the project root and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Usage
### Running the Model
Execute the main script:
```bash
python taming_llm.py
```
### Example Classification
```python
from taming_llm import classify_with_confidence
text = "The product is amazing! Highly recommended."
categories = ["Positive", "Negative", "Neutral"]
result = classify_with_confidence(text, categories)
print(result)
```

## File Structure
```
📂 Taming_LLMs_Project
├── taming_llm.py  # Main script
├── .env           # API key storage
├── requirements.txt  # Dependencies
└── README.md      # Documentation
```

## Challenges and Solutions
| Challenge                   | Solution                                              |
|-----------------------------|-------------------------------------------------------|
| API rate limits             | Implemented retry logic                               |
| Confidence threshold tuning | Adjusted logprob filtering for optimal classification |
| Accuracy vs. speed tradeoff | Used structured prompts for balance                   |
