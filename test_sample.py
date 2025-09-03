#!/usr/bin/env python3
"""
Test script for the sales analysis system
"""

from analysis_engine import analyze_call
from report_generator import generate_report
import json
from datetime import datetime

# Sample transcript for testing
SAMPLE_TRANSCRIPT = """
[00:01:30] Coach: Hi Sarah, thanks for joining me today. I'm excited to learn more about your fitness goals. Can you tell me a bit about where you are right now with your health and fitness?

[00:01:45] Sarah: Hi! Well, I've been struggling with my weight for about 3 years now. I gained about 30 pounds after having my second child and I just can't seem to get it off. I feel really uncomfortable in my clothes and I have no energy.

[00:02:15] Coach: I can hear the frustration in your voice. When you say you feel uncomfortable in your clothes, how is that affecting your daily life?

[00:02:25] Sarah: It's really affecting my confidence. I avoid social events, I don't want to be in photos with my kids. I feel like I'm not being the mom I want to be because I'm always tired and cranky.

[00:02:45] Coach: That sounds really tough, Sarah. You mentioned you've been dealing with this for 3 years - what have you tried in the past to address this?

[00:03:00] Sarah: I've tried so many diets - keto, Weight Watchers, intermittent fasting. I'll lose some weight but then I always gain it back plus more. I've also tried going to the gym but I never know what to do there.

[00:03:30] Coach: It sounds like you've put in a lot of effort but haven't found something sustainable. What do you think has been the biggest challenge in sticking with these approaches?

[00:03:45] Sarah: I think I just don't have the knowledge. I don't know how to eat properly or how to work out effectively. And when I don't see results quickly, I get discouraged and give up.

[00:04:15] Coach: That makes complete sense. Let me ask you this - what would your life look like if we could solve this problem? If you had the body and energy you want, how would that change things for you?

[00:04:30] Sarah: Oh wow, I would feel so much more confident. I'd want to go out with friends again, I'd be more present with my kids. I'd have energy to play with them and be the active mom I used to be.

[00:05:00] Coach: That sounds amazing, Sarah. Now, I have to ask - what do you think will happen if nothing changes? If you're still in the same place a year from now?

[00:05:15] Sarah: That's actually really scary to think about. I'm already feeling depressed about my body, and I worry it will just get worse. My kids are getting older and I don't want to miss out on their childhood because I'm too tired or self-conscious.

[00:05:45] Coach: I can see this is really important to you. Before I share how I might be able to help, I want to make sure you're in a place where you're ready to make some changes. Are you willing and able to commit to a structured program?

[00:06:00] Sarah: Yes, absolutely. I'm tired of trying to figure this out on my own.

[00:06:15] Coach: Great. And what about support at home? How does your husband feel about you investing in your health?

[00:06:25] Sarah: He's actually been encouraging me to find something that works. He sees how unhappy I am and wants me to feel good about myself again.

[00:06:45] Coach: Perfect. Let me show you how our program works. We focus on three key areas: sustainable nutrition that fits your lifestyle, effective workouts that don't require hours in the gym, and the mindset piece that helps you make this a permanent lifestyle change.

[00:07:15] Coach: Our clients typically see significant changes in the first 30 days - more energy, clothes fitting better, and most importantly, they finally understand how to maintain their results long-term.

[00:07:45] Coach: The investment for our 6-month transformation program is $2,997. You can pay in full today and save $500, making it $2,497, or we can set up a payment plan of $997 for 3 months.

[00:08:15] Sarah: That's more than I was expecting to spend. I'm not sure I can afford that right now.

[00:08:25] Coach: I understand that's a significant investment, Sarah. But let me ask you this - what's it worth to you to finally solve this problem permanently? To have the confidence and energy to be the mom you want to be?

[00:08:45] Sarah: You're right, it is important. But I'm just worried about the money.

[00:09:00] Coach: I get that. What if we did the 3-payment option? That's about $330 per month. Is that something that would work better for your budget?

[00:09:15] Sarah: Yes, I think I could make that work. When would I start?

[00:09:25] Coach: We can get you started this week. I'll send you all the onboarding materials today, and we'll schedule your first coaching call for this Friday. You're going to love this program, Sarah. I'm excited to help you get your confidence and energy back.

[00:09:45] Sarah: Okay, let's do it. I'm ready to finally make this change.
"""

def test_analysis():
    """Test the analysis engine with sample data"""
    print("Testing analysis engine...")
    
    # Analyze the sample transcript
    results = analyze_call(SAMPLE_TRANSCRIPT)
    
    # Print results
    print("\n=== ANALYSIS RESULTS ===")
    print(json.dumps(results, indent=2))
    
    # Generate report
    print("\nGenerating PDF report...")
    report_path = generate_report(
        meeting_title="Test Consultation - Sarah",
        created_at=datetime.now().isoformat(),
        transcript=SAMPLE_TRANSCRIPT,
        analysis_results=results
    )
    
    print(f"Report generated: {report_path}")
    
    return results, report_path

if __name__ == "__main__":
    test_analysis()

