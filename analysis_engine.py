import openai
import json
import os
from typing import Dict, Any

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
    base_url=os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
)

def analyze_call(transcript: str) -> Dict[str, Any]:
    """
    Analyze a sales call transcript using OpenAI API
    
    Args:
        transcript (str): The formatted transcript text
        
    Returns:
        Dict containing analysis results with scores and feedback
    """
    
    system_prompt = """You are a sales coaching expert specializing in fitness coaching. Your task is to analyze a transcript of a sales call and evaluate the coach's performance based on a provided sales framework and scoring rubric. Your analysis should be objective, insightful, and actionable.

The coach follows this sales framework:
- Where are they now?: Understand current situation
- Clarify & Label: Clarify issues and label them  
- Overview Past Experiences: Discuss past attempts and what worked/didn't
- Sell the Vacation: Paint a picture of the desired outcome
- Explain away their concerns: Address potential obstacles
- Reinforce their decision: Reassure them after they commit

Scoring Categories (weights):
- Needs Discovery (25 points): Did the coach effectively uncover the client's goals, struggles, and current situation?
- Pain Point Exploration (25 points): How well did the coach dig into the client's pain points and their impact?
- Consequence & Urgency (15 points): Did the coach effectively communicate consequences of inaction and create urgency?
- Obstacle Handling (15 points): How well did the coach address potential obstacles and concerns before the pitch?
- Objection Handling (10 points): How effectively did the coach handle objections after the pitch?
- Next Steps & Closing (10 points): How clearly were next steps outlined and buying decision reinforced?

For each category, provide:
1. Score (1-10)
2. Conversation highlights (what went well)
3. Missed opportunities (what could be improved)
4. Actionable feedback (specific suggestions)

Also detect if a payment method was mentioned (PIF/Pay In Full, split pay, monthly payments) and factor this into the Next Steps & Closing score.

Return your analysis as a JSON object with this structure:
{
  "overall_score": 85,
  "categories": {
    "needs_discovery": {
      "score": 8,
      "highlights": ["Specific examples..."],
      "missed_opportunities": ["Specific examples..."],
      "feedback": ["Specific suggestions..."]
    },
    // ... other categories
  },
  "payment_detected": "PIF",
  "summary": "Overall assessment of the call..."
}"""

    user_prompt = f"""Please analyze this fitness coaching sales call transcript:

{transcript}

Provide a detailed analysis following the scoring rubric and return the results in the specified JSON format."""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        # Parse the JSON response
        analysis_text = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            start_idx = analysis_text.find('{')
            end_idx = analysis_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = analysis_text[start_idx:end_idx]
                analysis_results = json.loads(json_str)
            else:
                # Fallback: create structured response from text
                analysis_results = parse_text_analysis(analysis_text)
                
        except json.JSONDecodeError:
            # Fallback: create structured response from text
            analysis_results = parse_text_analysis(analysis_text)
        
        return analysis_results
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        return {
            "error": str(e),
            "overall_score": 0,
            "categories": {},
            "summary": "Analysis failed due to an error."
        }

def parse_text_analysis(text: str) -> Dict[str, Any]:
    """
    Fallback function to parse text analysis into structured format
    """
    return {
        "overall_score": 50,  # Default score
        "categories": {
            "needs_discovery": {
                "score": 5,
                "highlights": ["Analysis parsing failed"],
                "missed_opportunities": ["Unable to parse detailed analysis"],
                "feedback": ["Please review the raw analysis text"]
            },
            "pain_point_exploration": {
                "score": 5,
                "highlights": ["Analysis parsing failed"],
                "missed_opportunities": ["Unable to parse detailed analysis"],
                "feedback": ["Please review the raw analysis text"]
            },
            "consequence_urgency": {
                "score": 5,
                "highlights": ["Analysis parsing failed"],
                "missed_opportunities": ["Unable to parse detailed analysis"],
                "feedback": ["Please review the raw analysis text"]
            },
            "obstacle_handling": {
                "score": 5,
                "highlights": ["Analysis parsing failed"],
                "missed_opportunities": ["Unable to parse detailed analysis"],
                "feedback": ["Please review the raw analysis text"]
            },
            "objection_handling": {
                "score": 5,
                "highlights": ["Analysis parsing failed"],
                "missed_opportunities": ["Unable to parse detailed analysis"],
                "feedback": ["Please review the raw analysis text"]
            },
            "next_steps_closing": {
                "score": 5,
                "highlights": ["Analysis parsing failed"],
                "missed_opportunities": ["Unable to parse detailed analysis"],
                "feedback": ["Please review the raw analysis text"]
            }
        },
        "payment_detected": "Unknown",
        "summary": f"Raw analysis text: {text[:500]}...",
        "raw_analysis": text
    }

