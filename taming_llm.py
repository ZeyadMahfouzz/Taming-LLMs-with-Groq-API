import os
import time
from dotenv import load_dotenv
import groq

load_dotenv()

class LLMClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = groq.Client(api_key=self.api_key)
        self.model = "llama3-70b-8192"
    
    def complete(self, prompt, max_tokens=1000, temperature=0.7):
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
        prompt = f"""
        # Analysis Report
        ## Input Text
        {text}
        ## Question
        3
        {question}
        ## Analysis
        """
        return prompt
    def extract_section(completion, section_start, section_end=None):
        start_idx = completion.find(section_start)
        if start_idx == -1:
            return None
        start_idx += len(section_start)
        if section_end is None:
            return completion[start_idx:].strip()
        end_idx = completion.find(section_end, start_idx)
        if end_idx == -1:
            return completion[start_idx:].strip()
        return completion[start_idx:end_idx].strip()
    def stream_until_marker(prompt, stop_marker, max_tokens=1000):
        pass

    def classify_with_confidence(text, categories, confidence_threshold=0.8):
        prompt = f"""
        Classify the following text into exactly one of these categories: {', '.join(categories)}.
        4
        Response format:
        1. CATEGORY: [one of: {', '.join(categories)}]
        2. CONFIDENCE: [high|medium|low]
        3. REASONING: [explanation]
        Text to classify:
        {text}
        """
   
        response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0,
        logprobs=True,
        top_logprobs=5
        )
        
        completion = response.choices[0].message.content
        category = extract_section(completion, "1. CATEGORY: ", "\n")
        
        if confidence_score > confidence_threshold:
            return {
            "category": category,
            "confidence": confidence_score,
            "reasoning": extract_section(completion, "3. REASONING: ")
            }
        else:
            return {
            "category": "uncertain",
            "confidence": confidence_score,
            "reasoning": "Confidence below threshold"
            }
