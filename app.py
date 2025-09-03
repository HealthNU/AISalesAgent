from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import threading
from analysis_engine import analyze_call
from report_generator import generate_report
from email_service import send_report_email

app = Flask(__name__)

# Configuration
WEBHOOK_SECRET = os.environ.get('FATHOM_WEBHOOK_SECRET', 'your-webhook-secret')
USER_EMAIL = os.environ.get('USER_EMAIL', 'your-email@example.com')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming webhooks from Fathom"""
    try:
        # Verify webhook signature (optional but recommended)
        # signature = request.headers.get('X-Fathom-Signature')
        # if not verify_signature(request.data, signature, WEBHOOK_SECRET):
        #     return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse the webhook payload
        data = request.get_json()
        
        # Check if this is a meeting completion event with transcript
        if not data.get('transcript'):
            return jsonify({'message': 'No transcript found, skipping analysis'}), 200
        
        # Process the meeting data in a background thread
        thread = threading.Thread(target=process_meeting, args=(data,))
        thread.start()
        
        return jsonify({'message': 'Webhook received, processing started'}), 200
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def process_meeting(meeting_data):
    """Process the meeting data and generate analysis report"""
    try:
        # Extract meeting information
        meeting_title = meeting_data.get('meeting_title', 'Unknown Meeting')
        transcript = meeting_data.get('transcript', [])
        created_at = meeting_data.get('created_at', datetime.now().isoformat())
        
        # Convert transcript to text format
        transcript_text = format_transcript(transcript)
        
        # Analyze the call
        print(f"Starting analysis for meeting: {meeting_title}")
        analysis_results = analyze_call(transcript_text)
        
        # Generate PDF report
        print("Generating PDF report...")
        report_path = generate_report(meeting_title, created_at, transcript_text, analysis_results)
        
        # Send email with report
        print("Sending email report...")
        send_report_email(USER_EMAIL, meeting_title, report_path)
        
        print(f"Analysis complete for meeting: {meeting_title}")
        
    except Exception as e:
        print(f"Error processing meeting: {str(e)}")

def format_transcript(transcript):
    """Convert Fathom transcript format to readable text"""
    if isinstance(transcript, list):
        formatted_lines = []
        for entry in transcript:
            speaker = entry.get('speaker', {}).get('display_name', 'Unknown')
            text = entry.get('text', '')
            timestamp = entry.get('timestamp', '')
            formatted_lines.append(f"[{timestamp}] {speaker}: {text}")
        return '\n'.join(formatted_lines)
    else:
        return str(transcript)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/test', methods=['POST'])
def test_analysis():
    """Test endpoint for manual analysis (for development/testing)"""
    try:
        data = request.get_json()
        transcript = data.get('transcript', '')
        
        if not transcript:
            return jsonify({'error': 'No transcript provided'}), 400
        
        # Analyze the call
        analysis_results = analyze_call(transcript)
        
        return jsonify({
            'message': 'Analysis complete',
            'results': analysis_results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

