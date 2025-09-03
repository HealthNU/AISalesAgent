# Fitness Coaching Sales Analysis System

An automated system that analyzes your Fathom-recorded coaching consultations and provides detailed feedback to improve your sales performance.

## Features

- **Automated Analysis**: Receives Fathom webhooks and analyzes calls automatically
- **Comprehensive Scoring**: Evaluates 6 key sales categories with weighted scoring
- **Detailed Reports**: Generates professional PDF reports with actionable feedback
- **Email Delivery**: Automatically emails reports after each call
- **Payment Detection**: Identifies payment methods chosen (PIF, split pay, monthly)

## Scoring Categories

| Category | Weight | Focus Area |
|----------|--------|------------|
| Needs Discovery | 25% | Understanding client goals and current situation |
| Pain Point Exploration | 25% | Digging into client struggles and emotional impact |
| Consequence & Urgency | 15% | Communicating consequences of inaction |
| Obstacle Handling | 15% | Addressing concerns before the pitch |
| Objection Handling | 10% | Responding to client objections |
| Next Steps & Closing | 10% | Clear process and decision reinforcement |

## Quick Start

### 1. Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Test with sample data
python test_sample.py
```

### 2. Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Your email for receiving reports
USER_EMAIL=your-email@example.com

# Gmail configuration for sending reports
SENDER_EMAIL=your-gmail@gmail.com
SENDER_PASSWORD=your-gmail-app-password

# Fathom webhook secret (optional)
FATHOM_WEBHOOK_SECRET=your-webhook-secret
```

### 3. Deployment

See `deployment_guide.md` for detailed deployment instructions.

## File Structure

```
sales_agent_system/
├── app.py                 # Main Flask application
├── analysis_engine.py     # AI-powered analysis logic
├── report_generator.py    # PDF report generation
├── email_service.py       # Email sending functionality
├── test_sample.py         # Testing script with sample data
├── requirements.txt       # Python dependencies
├── deployment_guide.md    # Deployment instructions
└── reports/              # Generated PDF reports
```

## API Endpoints

- `POST /webhook` - Receives Fathom webhooks
- `GET /health` - Health check endpoint
- `POST /test` - Manual testing endpoint

## Sample Analysis Output

The system provides:

- **Overall Score**: 0-100 based on weighted categories
- **Category Breakdown**: Individual scores and feedback
- **Conversation Highlights**: What went well
- **Missed Opportunities**: Areas for improvement
- **Actionable Feedback**: Specific suggestions
- **Payment Detection**: Identified payment method

## Requirements

- Python 3.8+
- OpenAI API access
- Gmail account (for email reports)
- Fathom account with API access
- Hosting platform (Railway, Heroku, etc.)

## Cost Estimate

- **Hosting**: $5-10/month
- **AI Analysis**: ~$0.01-0.05 per call
- **Email**: Free (Gmail)

**Total**: $5-15/month for most coaching businesses

## Support

For technical issues:
1. Check application logs
2. Verify environment variables
3. Test individual components
4. Review deployment guide

## License

This project is created for fitness coaching businesses to improve their sales performance through automated analysis and feedback.

