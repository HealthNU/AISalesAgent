# Sales Agent System - Deployment Guide

## Overview

This guide will help you deploy your automated sales analysis system that integrates with Fathom to analyze your coaching consultations and provide detailed feedback reports.

## System Components

1. **Flask Web Application** - Receives webhooks from Fathom
2. **Analysis Engine** - Uses AI to analyze call transcripts
3. **Report Generator** - Creates professional PDF reports
4. **Email Service** - Sends reports to your email

## Deployment Options

### Option 1: Railway (Recommended - Easy Setup)

Railway is a simple platform that can host your application for about $5-10/month.

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy Your App**
   - Upload your `sales_agent_system` folder to GitHub
   - Connect Railway to your GitHub repository
   - Railway will automatically detect it's a Python app

3. **Set Environment Variables in Railway**
   ```
   USER_EMAIL=your-email@example.com
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-gmail@gmail.com
   SENDER_PASSWORD=your-gmail-app-password
   ```

4. **Get Your Webhook URL**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Your webhook endpoint will be: `https://your-app.railway.app/webhook`

### Option 2: Heroku (Alternative)

Similar to Railway but slightly more complex setup.

### Option 3: DigitalOcean App Platform

Good for more advanced users, costs about $5/month.

## Email Setup (Gmail)

To send reports via email, you'll need to set up Gmail App Passwords:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `SENDER_PASSWORD` environment variable

## Fathom Integration

1. **Get Fathom API Key**:
   - Log into Fathom
   - Go to Settings → Integrations → API
   - Generate an API key

2. **Create Webhook in Fathom**:
   - Use the Fathom API or contact their support
   - Set webhook URL to: `https://your-deployed-app.com/webhook`
   - Enable: transcript, summary, action_items

## Testing Your Deployment

1. **Health Check**: Visit `https://your-app.com/health`
2. **Manual Test**: Send POST request to `https://your-app.com/test` with transcript data

## Costs Breakdown

- **Hosting**: $5-10/month (Railway/Heroku)
- **AI Analysis**: ~$0.01-0.05 per call (OpenAI API usage)
- **Email**: Free (using Gmail)

**Total**: About $5-15/month depending on call volume

## Troubleshooting

### Common Issues:

1. **Email not sending**: Check Gmail app password and 2FA setup
2. **Webhook not receiving**: Verify Fathom webhook URL is correct
3. **Analysis failing**: Check OpenAI API credits and model availability

### Logs and Monitoring:

- Railway/Heroku provide built-in logging
- Check application logs for error messages
- Monitor email delivery status

## Security Notes

- Never commit API keys or passwords to GitHub
- Use environment variables for all sensitive data
- Consider adding webhook signature verification for production use

## Support

If you encounter issues:
1. Check the application logs first
2. Verify all environment variables are set correctly
3. Test individual components (email, analysis) separately
4. Contact the deployment platform support if needed

