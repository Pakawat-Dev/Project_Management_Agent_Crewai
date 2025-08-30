# 🚀 AI-Powered Project Management System

A comprehensive project management system powered by CrewAI framework and Claude Sonnet, featuring multiple AI agents working collaboratively to manage projects efficiently.

## ✨ Features

### 🤖 Multi-Agent AI System
- **Project Planner Agent**: Creates comprehensive project plans with objectives, milestones, and timelines
- **Task Allocator Agent**: Efficiently allocates tasks based on team capabilities and availability
- **Progress Monitor Agent**: Tracks project progress and identifies potential risks or delays
- **Quality Reviewer Agent**: Ensures project deliverables meet quality standards

### 📊 Core Functionality
- **Project Planning**: Generate detailed project plans with AI assistance
- **Status Analysis**: Analyze current project status and deliverables
- **Token Usage Tracking**: Monitor API costs and usage in real-time
- **PDF Report Generation**: Create professional project reports

### 🎯 User Interface
- **Streamlit Web Interface**: Modern, responsive web application
- **Real-time Updates**: Live token usage and cost tracking
- **Professional Reports**: Generate and download comprehensive PDF reports
- **Interactive Workflow**: Easy-to-use tabs and forms

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Anthropic API key

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # Ensure you have PM_agent.py, requirements.txt, and .env files
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project directory:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
   
   Or set the environment variable directly:
   ```bash
   # Windows
   set ANTHROPIC_API_KEY=your_anthropic_api_key_here
   
   # Linux/Mac
   export ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run PM_agent.py
   ```

## 🚀 Usage

### Getting Started

1. **Launch the application**
   - Run `streamlit run PM_agent.py`
   - Open your browser to the provided URL (typically `http://localhost:8501`)

2. **Project Planning**
   - Navigate to the "📋 Project Planning" tab
   - Enter your project description and team information
   - Click "🚀 Generate Project Plan"
   - View the AI-generated comprehensive project plan

3. **Status Analysis**
   - Go to the "📊 Status Analysis" tab
   - Describe your current project status
   - List deliverables to review
   - Click "🔍 Analyze Status" for detailed analysis

4. **Generate Reports**
   - After running planning or analysis, the PDF generation section appears
   - Click "📄 Generate PDF Report"
   - Download your comprehensive project report

### Example Inputs

#### Project Planning Example
```
Project Description:
Develop an e-commerce website with product catalog, shopping cart, 
payment integration, and admin dashboard

Team Information:
3 full-stack developers, 1 UI/UX designer, 1 DevOps engineer, 2 QA testers
```

#### Status Analysis Example
```
Current Project Status:
Week 3: Backend API 70% complete, Frontend 40% complete, 2 days behind schedule

Deliverables to Review:
User authentication module, Database schema, API documentation
```

## 📋 System Architecture

### Agent Workflow
```
Project Description → Planning → Task Allocation → Monitoring → Quality Review → Results
```

### Agent Roles
1. **Project Planner**: Creates detailed project plans with milestones and timelines
2. **Task Allocator**: Matches tasks with team members based on skills and availability
3. **Progress Monitor**: Tracks progress and identifies bottlenecks
4. **Quality Reviewer**: Ensures deliverables meet defined standards

## 💰 Token Usage & Costs

### Cost Estimation
- **Model**: Claude Sonnet (via Anthropic API)
- **Estimation**: ~4 characters per token
- **Pricing**: ~$9 per 1M tokens (average of input/output costs)
- **Real-time Tracking**: Monitor usage and costs per operation

### Usage Features
- Session-based tracking
- Operation history with timestamps
- Cost breakdown per AI operation
- Refresh functionality for current stats

## 📄 PDF Reports

### Report Contents
- **Project Overview**: Description and team information
- **Project Plan**: Complete AI-generated project plan
- **Status Analysis**: Current status and quality assessment
- **Token Usage Summary**: Detailed usage statistics and costs
- **Operation History**: Timeline of AI operations

### Report Features
- Professional formatting with custom styling
- Automatic timestamp and metadata
- Structured tables for data presentation
- Download with automatic filename generation

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude access | Yes |

### Model Configuration
The system uses Claude Sonnet model with the following settings:
- **Model**: `claude-sonnet-4-20250514`
- **Temperature**: `0.1` (for consistent, focused responses)
- **Framework**: CrewAI with sequential processing

## 📁 Project Structure

```
project/
├── PM_agent.py           # Main application file
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── README.md            # This documentation
└── generated_reports/   # PDF reports (auto-created)
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ⚠️ ANTHROPIC_API_KEY is not set
   ```
   **Solution**: Ensure your API key is properly set in the `.env` file or environment variables

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'streamlit'
   ```
   **Solution**: Install dependencies with `pip install -r requirements.txt`

3. **PDF Generation Issues**
   ```
   Error generating PDF
   ```
   **Solution**: Ensure `reportlab` is installed and you have write permissions

### Performance Tips
- **Token Optimization**: Be concise in your project descriptions to reduce token usage
- **Session Management**: The system maintains state during your browser session
- **Report Generation**: Generate reports after completing both planning and analysis for comprehensive documentation

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Structure
- **Agent Classes**: Define AI agent roles and behaviors
- **Task Classes**: Specify tasks for each agent
- **System Class**: Orchestrates agents and manages data
- **UI Components**: Streamlit interface and interactions
- **PDF Generator**: Report creation and formatting

## 📝 License

This project is provided as-is for educational and development purposes.

## 🆘 Support

For issues, questions, or contributions:
1. Check the troubleshooting section above
2. Review the Anthropic API documentation
3. Ensure all dependencies are properly installed
4. Verify your API key has sufficient credits

## 🔄 Version History

- **v1.0**: Initial release with basic project planning
- **v1.1**: Added status analysis functionality
- **v1.2**: Implemented token usage tracking
- **v1.3**: Added PDF report generation
- **v1.4**: Enhanced Streamlit UI with professional styling

---

**Built with ❤️ using CrewAI, Streamlit, and Claude Sonnet**
