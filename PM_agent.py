"""
Project Management Agent using CrewAI Framework
This system uses multiple AI agents to manage projects collaboratively
"""

import os
from typing import List, Dict
from datetime import datetime
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

# Load environment variables from .env file
load_dotenv()

# Set up the Claude model
# Make sure to set your API key: export ANTHROPIC_API_KEY="your-api-key"
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",  # Using available Sonnet model
    temperature=0.1
)

# Define Agents
class ProjectManagementAgents:
    def __init__(self):
        self.llm = llm
    
    def project_planner(self):
        """Creates a project planning agent"""
        return Agent(
            role='Project Planner',
            goal='Create comprehensive project plans with clear objectives and milestones',
            backstory="""You are an experienced project planner with 10+ years 
            of experience in breaking down complex projects into manageable tasks. 
            You excel at identifying dependencies and creating realistic timelines.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def task_allocator(self):
        """Creates a task allocation agent"""
        return Agent(
            role='Task Allocator',
            goal='Efficiently allocate tasks based on team capabilities and availability',
            backstory="""You are a resource management specialist who understands 
            team dynamics and can match tasks with the right team members based 
            on their skills and workload.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def progress_monitor(self):
        """Creates a progress monitoring agent"""
        return Agent(
            role='Progress Monitor',
            goal='Track project progress and identify potential risks or delays',
            backstory="""You are a detail-oriented project monitor who tracks 
            progress, identifies bottlenecks, and suggests corrective actions 
            to keep projects on schedule.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def quality_reviewer(self):
        """Creates a quality review agent"""
        return Agent(
            role='Quality Reviewer',
            goal='Ensure project deliverables meet quality standards',
            backstory="""You are a quality assurance expert who reviews project 
            outputs and ensures they meet the defined standards and requirements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

# Define Tasks
class ProjectManagementTasks:
    def __init__(self):
        pass
    
    def create_project_plan(self, agent, project_description: str):
        """Task for creating a project plan"""
        return Task(
            description=f"""
            Create a detailed project plan for: {project_description}
            
            Your plan should include:
            1. Project objectives and scope
            2. Key milestones and deliverables
            3. Timeline with phases
            4. Required resources
            5. Success criteria
            6. Potential risks and mitigation strategies
            """,
            agent=agent,
            expected_output="A comprehensive project plan with all required elements"
        )
    
    def allocate_tasks(self, agent, project_plan: str, team_info: str):
        """Task for allocating tasks to team members"""
        return Task(
            description=f"""
            Based on the project plan and team information, allocate tasks:
            
            Project Plan: {project_plan}
            Team Information: {team_info}
            
            Create task assignments that consider:
            1. Team member skills and expertise
            2. Current workload and availability
            3. Task dependencies
            4. Priority levels
            5. Estimated effort for each task
            """,
            agent=agent,
            expected_output="Detailed task allocation with assignments and timelines"
        )
    
    def monitor_progress(self, agent, project_status: str):
        """Task for monitoring project progress"""
        return Task(
            description=f"""
            Analyze the current project status and provide insights:
            
            Current Status: {project_status}
            
            Your analysis should include:
            1. Overall progress assessment
            2. Completed vs pending tasks
            3. Identified bottlenecks or delays
            4. Risk assessment
            5. Recommended actions to stay on track
            """,
            agent=agent,
            expected_output="Progress report with analysis and recommendations"
        )
    
    def review_quality(self, agent, deliverables: str):
        """Task for reviewing project quality"""
        return Task(
            description=f"""
            Review the project deliverables for quality:
            
            Deliverables: {deliverables}
            
            Your review should assess:
            1. Completeness of deliverables
            2. Compliance with requirements
            3. Quality standards met
            4. Areas for improvement
            5. Final recommendations
            """,
            agent=agent,
            expected_output="Quality review report with detailed assessment"
        )

# Token Usage Tracker
class TokenUsageTracker:
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        self.session_history = []
    
    def add_usage(self, tokens_used: int, cost: float, operation: str):
        """Add token usage to tracker"""
        self.total_tokens += tokens_used
        self.total_cost += cost
        self.session_history.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'operation': operation,
            'tokens': tokens_used,
            'cost': cost
        })
    
    def get_summary(self):
        """Get usage summary"""
        return {
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost,
            'operations': len(self.session_history),
            'history': self.session_history
        }
    
    def format_summary(self):
        """Format usage summary for display"""
        summary = self.get_summary()
        history_text = "\n".join([
            f"• {item['timestamp']} - {item['operation']}: {item['tokens']} tokens (${item['cost']:.4f})"
            for item in summary['history'][-5:]  # Show last 5 operations
        ])
        
        return f"""
📊 **Token Usage Summary**
• Total Tokens Used: {summary['total_tokens']:,}
• Estimated Cost: ${summary['total_cost']:.4f}
• Operations: {summary['operations']}

🕒 **Recent Operations:**
{history_text}
        """

# PDF Report Generator
class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        self.normal_style = self.styles['Normal']
        self.normal_style.spaceAfter = 12
    
    def generate_project_report(self, project_data: Dict, token_usage: Dict) -> bytes:
        """Generate a comprehensive project management report as PDF"""
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build story (content)
        story = []
        
        # Title
        story.append(Paragraph("🚀 Project Management Report", self.title_style))
        story.append(Spacer(1, 20))
        
        # Report metadata
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<b>Generated:</b> {report_date}", self.normal_style))
        story.append(Spacer(1, 20))
        
        # Project Overview Section
        if 'project_description' in project_data:
            story.append(Paragraph("📋 Project Overview", self.heading_style))
            story.append(Paragraph(f"<b>Description:</b> {project_data['project_description']}", self.normal_style))
            
        if 'team_info' in project_data:
            story.append(Paragraph(f"<b>Team:</b> {project_data['team_info']}", self.normal_style))
            story.append(Spacer(1, 15))
        
        # Project Plan Section
        if 'project_plan' in project_data:
            story.append(Paragraph("🎯 Project Plan", self.heading_style))
            # Clean and format the project plan text
            plan_text = str(project_data['project_plan']).replace('\n', '<br/>')
            story.append(Paragraph(plan_text, self.normal_style))
            story.append(Spacer(1, 15))
        
        # Status Analysis Section
        if 'status_analysis' in project_data:
            story.append(Paragraph("📊 Status Analysis", self.heading_style))
            analysis_text = str(project_data['status_analysis']).replace('\n', '<br/>')
            story.append(Paragraph(analysis_text, self.normal_style))
            story.append(Spacer(1, 15))
        
        # Token Usage Section
        story.append(Paragraph("💰 Token Usage Summary", self.heading_style))
        
        # Create token usage table
        usage_data = [
            ['Metric', 'Value'],
            ['Total Tokens Used', f"{token_usage['total_tokens']:,}"],
            ['Estimated Cost', f"${token_usage['total_cost']:.4f}"],
            ['Operations Performed', str(token_usage['operations'])],
        ]
        
        usage_table = Table(usage_data, colWidths=[2*inch, 2*inch])
        usage_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(usage_table)
        story.append(Spacer(1, 15))
        
        # Operation History
        if token_usage['history']:
            story.append(Paragraph("🕒 Operation History", self.heading_style))
            
            history_data = [['Time', 'Operation', 'Tokens', 'Cost']]
            for item in token_usage['history'][-10:]:  # Last 10 operations
                history_data.append([
                    item['timestamp'],
                    item['operation'],
                    str(item['tokens']),
                    f"${item['cost']:.4f}"
                ])
            
            history_table = Table(history_data, colWidths=[1*inch, 2*inch, 1*inch, 1*inch])
            history_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            story.append(history_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Generated by AI-Powered Project Management System", 
                              ParagraphStyle('Footer', parent=self.normal_style, 
                                           alignment=TA_CENTER, fontSize=10, 
                                           textColor=colors.grey)))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

# Main Project Management System
class ProjectManagementSystem:
    def __init__(self):
        self.agents = ProjectManagementAgents()
        self.tasks = ProjectManagementTasks()
        self.token_tracker = TokenUsageTracker()
        self.pdf_generator = PDFReportGenerator()
        self.report_data = {}
    
    def _estimate_tokens_and_cost(self, text: str):
        """Estimate tokens and cost for Anthropic Claude"""
        # Rough estimation: ~4 characters per token for Claude
        estimated_tokens = len(text) // 4
        # Claude Sonnet pricing (approximate): $3 per 1M input tokens, $15 per 1M output tokens
        # Using average of $9 per 1M tokens for estimation
        estimated_cost = (estimated_tokens / 1_000_000) * 9.0
        return estimated_tokens, estimated_cost
    
    def run_project_planning(self, project_description: str, team_info: str):
        """Run the complete project planning workflow"""
        
        # Initialize agents
        planner = self.agents.project_planner()
        allocator = self.agents.task_allocator()
        monitor = self.agents.progress_monitor()
        
        # Create tasks
        planning_task = self.tasks.create_project_plan(
            planner, 
            project_description
        )
        
        allocation_task = self.tasks.allocate_tasks(
            allocator,
            project_description,
            team_info
        )
        
        # Create crew with sequential process
        crew = Crew(
            agents=[planner, allocator, monitor],
            tasks=[planning_task, allocation_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the workflow and track usage
        input_text = f"{project_description} {team_info}"
        result = crew.kickoff()
        
        # Store data for report generation
        self.report_data.update({
            'project_description': project_description,
            'team_info': team_info,
            'project_plan': result
        })
        
        # Estimate token usage
        result_text = str(result)
        tokens_used, cost = self._estimate_tokens_and_cost(input_text + result_text)
        self.token_tracker.add_usage(tokens_used, cost, "Project Planning")
        
        return result
    
    def analyze_project_status(self, project_status: str, deliverables: str):
        """Analyze current project status and quality"""
        
        # Initialize agents
        monitor = self.agents.progress_monitor()
        reviewer = self.agents.quality_reviewer()
        
        # Create tasks
        monitoring_task = self.tasks.monitor_progress(
            monitor,
            project_status
        )
        
        review_task = self.tasks.review_quality(
            reviewer,
            deliverables
        )
        
        # Create crew
        crew = Crew(
            agents=[monitor, reviewer],
            tasks=[monitoring_task, review_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the workflow and track usage
        input_text = f"{project_status} {deliverables}"
        result = crew.kickoff()
        
        # Store data for report generation
        self.report_data.update({
            'project_status': project_status,
            'deliverables': deliverables,
            'status_analysis': result
        })
        
        # Estimate token usage
        result_text = str(result)
        tokens_used, cost = self._estimate_tokens_and_cost(input_text + result_text)
        self.token_tracker.add_usage(tokens_used, cost, "Status Analysis")
        
        return result
    
    def generate_pdf_report(self) -> bytes:
        """Generate PDF report with current project data"""
        return self.pdf_generator.generate_project_report(
            self.report_data, 
            self.token_tracker.get_summary()
        )

# Streamlit Interface
def run_streamlit_app():
    """Create the Streamlit UI for the project management system"""
    
    # Initialize system in session state
    if "pm_system" not in st.session_state:
        st.session_state.pm_system = ProjectManagementSystem()
    
    system = st.session_state.pm_system
    
    # Page configuration
    st.set_page_config(
        page_title="🎯 Project Management AI System",
        page_icon="🚀",
        layout="wide"
    )
    
    # Header
    st.title("🚀 AI-Powered Project Management System")
    st.markdown("### 🤖 Using CrewAI Framework with Claude Sonnet Model")
    st.markdown("This system uses multiple AI agents working together to manage your projects efficiently.")
    st.divider()
    
    # API key check
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("⚠️ ANTHROPIC_API_KEY is not set. Please set it in your environment variables.")
        st.stop()
    
    # PDF Download Section (before tabs)
    if system.report_data:
        st.subheader("📄 Generate Final Report")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("📄 Generate PDF Report", type="secondary"):
                try:
                    pdf_bytes = system.generate_pdf_report()
                    report_filename = f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_bytes,
                        file_name=report_filename,
                        mime="application/pdf",
                        type="primary"
                    )
                    st.success("✅ PDF report generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")
        
        with col2:
            st.info("📊 Report includes:\n- Project overview\n- Generated plans\n- Status analysis\n- Token usage stats")
        
        st.divider()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Project Planning", "📊 Status Analysis", "💰 Token Usage", "🔄 Workflow Overview"])
    
    # Project Planning Tab
    with tab1:
        st.subheader("🎯 Create a new project plan with AI assistance")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            project_desc = st.text_area(
                "📝 Project Description",
                placeholder="Describe your project (e.g., 'Develop a mobile app for task management with user authentication and cloud sync')",
                height=150,
                key="project_desc"
            )
            
            team_info = st.text_area(
                "👥 Team Information", 
                placeholder="Describe your team (e.g., '2 developers, 1 designer, 1 QA tester, all available full-time')",
                height=100,
                key="team_info"
            )
            
            plan_button = st.button("🚀 Generate Project Plan", type="primary", key="plan_btn")
        
        with col2:
            st.markdown("**📊 Project Plan Output**")
            plan_output_container = st.empty()
            
            st.markdown("**💰 Token Usage**")
            plan_usage_container = st.empty()
        
        if plan_button and project_desc and team_info:
            with st.spinner("🤖 Planning with CrewAI agents..."):
                try:
                    result = system.run_project_planning(project_desc, team_info)
                    usage_summary = system.token_tracker.format_summary()
                    
                    plan_output_container.text_area(
                        "Project Plan Result",
                        value=f"✅ Project Planning Complete:\n\n{result}",
                        height=300,
                        disabled=True
                    )
                    
                    plan_usage_container.text_area(
                        "Token Usage",
                        value=usage_summary,
                        height=150,
                        disabled=True
                    )
                    
                    st.success("✅ Project planning completed successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error in planning: {str(e)}")
    
    # Status Analysis Tab
    with tab2:
        st.subheader("🔍 Analyze current project status and deliverables")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            status_info = st.text_area(
                "📈 Current Project Status",
                placeholder="Describe current status (e.g., 'Week 3: Backend API 70% complete, Frontend 40% complete, 2 days behind schedule')",
                height=150,
                key="status_info"
            )
            
            deliverables_info = st.text_area(
                "📦 Deliverables to Review",
                placeholder="List deliverables (e.g., 'User authentication module, Database schema, API documentation')",
                height=100,
                key="deliverables_info"
            )
            
            analyze_button = st.button("🔍 Analyze Status", type="primary", key="analyze_btn")
        
        with col2:
            st.markdown("**📊 Analysis Output**")
            analysis_output_container = st.empty()
            
            st.markdown("**💰 Token Usage**")
            analysis_usage_container = st.empty()
        
        if analyze_button and status_info and deliverables_info:
            with st.spinner("🤖 Analyzing with CrewAI agents..."):
                try:
                    result = system.analyze_project_status(status_info, deliverables_info)
                    usage_summary = system.token_tracker.format_summary()
                    
                    analysis_output_container.text_area(
                        "Analysis Result",
                        value=f"✅ Status Analysis Complete:\n\n{result}",
                        height=300,
                        disabled=True
                    )
                    
                    analysis_usage_container.text_area(
                        "Token Usage",
                        value=usage_summary,
                        height=150,
                        disabled=True
                    )
                    
                    st.success("✅ Status analysis completed successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error in analysis: {str(e)}")
    
    # Token Usage Tab
    with tab3:
        st.subheader("📊 Monitor your API token usage and costs")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🔄 Refresh Usage Stats", key="refresh_usage"):
                st.rerun()
        
        with col2:
            usage_summary = system.token_tracker.format_summary()
            st.text_area(
                "Current Session Usage",
                value=usage_summary,
                height=300,
                disabled=True
            )
        
        st.info("""
        ### 💡 About Token Usage
        - **Estimation Method**: Token usage is estimated based on text length (~4 chars per token)
        - **Cost Calculation**: Based on Claude Sonnet pricing (~$9 per 1M tokens average)
        - **Real-time Tracking**: Usage updates after each AI operation
        - **Session Based**: Counters reset when you restart the application
        """)
    
    # Workflow Overview Tab
    with tab4:
        st.subheader("🔄 Project Management Workflow")
        
        st.markdown("""
        #### 🎯 **Planning Phase**
        1. **Project Planner Agent** - Creates comprehensive project plan
        2. **Task Allocator Agent** - Assigns tasks to team members
        
        #### 📊 **Monitoring Phase**
        3. **Progress Monitor Agent** - Tracks progress and identifies risks
        4. **Quality Reviewer Agent** - Ensures deliverables meet standards
        
        #### 🔄 **Process Flow**
        ```
        Project Description → Planning → Task Allocation → Monitoring → Quality Review → Results
        ```
        
        #### 🤝 **Agent Collaboration**
        - Agents work sequentially, passing information between stages
        - Each agent specializes in their domain for optimal results
        - Results are aggregated into comprehensive reports
        """)
        
        st.subheader("💡 Example Inputs")
        
        with st.expander("E-commerce Website Example"):
            st.code("""
Project Description:
Develop an e-commerce website with product catalog, shopping cart, payment integration, and admin dashboard

Team Information:
3 full-stack developers, 1 UI/UX designer, 1 DevOps engineer, 2 QA testers
            """)
        
        with st.expander("Machine Learning Pipeline Example"):
            st.code("""
Project Description:
Create a machine learning pipeline for customer churn prediction with data preprocessing, model training, and deployment

Team Information:
2 data scientists, 1 ML engineer, 1 data engineer
            """)
    
    # Footer
    st.divider()
    st.markdown("*Built with CrewAI, Streamlit, and Claude Sonnet*")

# Main execution
if __name__ == "__main__":
    # Make sure to set your API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Please set your ANTHROPIC_API_KEY environment variable")
        print("Export it using: export ANTHROPIC_API_KEY='your-api-key'")
    
    # Launch the Streamlit interface
    run_streamlit_app()
