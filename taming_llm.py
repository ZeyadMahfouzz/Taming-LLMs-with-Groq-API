import os
import time
from dotenv import load_dotenv
import groq

class LLMClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = groq.Client(api_key=self.api_key)
        self.model = "llama3-70b-8192"

    def complete(self, prompt, max_tokens=1000, temperature=0.7):
        """Generates a response from the LLM based on the provided prompt."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None

def create_structured_prompt(text, question):
    """Creates a structured prompt for content analysis."""
    return f"""
    # Analysis Report
    ## Input Text
    {text}
    ## Question
    {question}
    ## Analysis
    """

def extract_section(completion, section_start, section_end=None):
    """Extracts content between section_start and section_end."""
    start_idx = completion.find(section_start)
    if start_idx == -1:
        return None
    start_idx += len(section_start)
    if section_end is None:
        return completion[start_idx:].strip()
    end_idx = completion.find(section_end, start_idx)
    return completion[start_idx:end_idx].strip() if end_idx != -1 else completion[start_idx:].strip()

def stream_until_marker(client, prompt, stop_marker, max_tokens=1000):
    """Streams a completion and stops at a given marker."""
    response = ""
    for chunk in client.client.chat.completions.create(
        model=client.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        stream=True
    ):
        response += chunk.choices[0].delta.content
        if stop_marker in response:
            break
    return response.split(stop_marker)[0]

def classify_with_confidence(client, text, categories, confidence_threshold=0.8):
    """Classifies text into a category with confidence analysis."""
    prompt = f"""
    Classify the following text into exactly one of these categories: {', '.join(categories)}.
    
    Response format:
    1. CATEGORY: [one of: {', '.join(categories)}]
    2. CONFIDENCE: [high|medium|low]
    3. REASONING: [explanation]
    
    Text to classify:
    {text}
    """
    response = client.complete(prompt, max_tokens=500, temperature=0)
    if not response:
        return None
    category = extract_section(response, "1. CATEGORY: ", "\n")
    confidence = extract_section(response, "2. CONFIDENCE: ", "\n")
    
    confidence_score = {"high": 0.9, "medium": 0.6, "low": 0.3}.get(confidence.lower(), 0)
    
    if confidence_score > confidence_threshold:
        return {
            "category": category,
            "confidence": confidence_score,
            "reasoning": extract_section(response, "3. REASONING: ")
        }
    return {"category": "uncertain", "confidence": confidence_score, "reasoning": "Confidence below threshold"}

def compare_prompt_strategies(client, texts, categories):
    """Compares different prompt strategies on classification tasks."""
    strategies = {
        "basic": lambda text: f"Classify this text into one of these categories: {', '.join(categories)}.\n\nText: {text}",
        "structured": lambda text: f"""
        Classification Task
        Categories: {', '.join(categories)}
        Text: {text}
        Classification: """,
        "few_shot": lambda text: f"""
        Here are some examples of text classification:
        
        Example 1:
        Text: "The product arrived damaged and customer service was unhelpful."
        Classification: Negative
        
        Example 2:
        Text: "While delivery was slow, the quality exceeded my expectations."
        Classification: Mixed
        
        Example 3:
        Text: "Absolutely love this! Best purchase I've made all year."
        Classification: Positive
        
        Now classify this text:
        Text: "{text}"
        Classification: """
    }

    results = {}
    for strategy_name, prompt_func in strategies.items():
        strategy_results = []
        for text in texts:
            prompt = prompt_func(text)
            result = classify_with_confidence(client, text, categories)
            if result:
                strategy_results.append(result)
        results[strategy_name] = strategy_results

    return results

if __name__ == "__main__":
    client = LLMClient()

    print("\n-----------------Part 1: Normal Completion testing-----------------\n")
    prompt = "Describe the role of photosynthesis in the Earth's ecosystem."
    response = client.complete(prompt)
    print("Completion Response:\n", response)


    print("\n-----------------Part 2: Structured Completion and Section Extraction-----------------\n")
    text = "Quantum computing leverages quantum mechanics to perform computations much faster than classical computers for certain problems."
    question = "How does quantum computing differ from classical computing?"
    structured_prompt = create_structured_prompt(text, question)
    completion = client.complete(structured_prompt)
    analysis = extract_section(completion, "## Analysis", None)
    print("Extracted Analysis:\n", analysis)


    print("\n-----------------Part 3: Streaming Completion with Stop Marker-----------------\n")
    prompt = "Provide a brief overview of the history of artificial intelligence. Conclude your response with 'END'."
    stop_marker = "END"
    response = stream_until_marker(client, prompt, stop_marker)
    print("Streamed Response:\n", response)


    print("\n-----------------Part 4: Classification with Confidence Analysis-----------------\n")
    categories = ["Positive", "Negative", "Neutral"]
    text = "The user experience of the app is frustrating, and the interface is not intuitive."
    result = classify_with_confidence(client, text, categories)
    print("Classification Result:\n", result)


    print("\n-----------------Part 5: Prompt Strategy Comparison-----------------\n")
    texts = [
        "This laptop is incredibly fast and lightweight. Highly recommend!",
        "The screen resolution is disappointing, and the colors seem off.",
        "The product is decent, but the price is too high for what it offers."
    ]
    categories = ["Positive", "Negative", "Neutral"]
    results = compare_prompt_strategies(client, texts, categories)
    for strategy, outputs in results.items():
        print(f"Strategy: {strategy}")
        for i, res in enumerate(outputs):
            print(f"  Text: {texts[i]}")
            print(f"  Category: {res['category']}, Confidence: {res['confidence']}")

