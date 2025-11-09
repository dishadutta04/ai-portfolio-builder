import streamlit as st
import time
from datetime import datetime
from utils.ai_generator import generate_portfolio_html, test_api_key
from utils.templates import get_color_schemes, get_font_pairs
import base64
import json

# Page configuration
st.set_page_config(
    page_title="AI Portfolio Builder - Create Stunning Portfolios",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.95;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .step-indicator {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .preview-container {
        border: 3px solid #667eea;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .info-box {
        background: #f0f4ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
    }
    
    .animated-gradient {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# Initialize session state
if 'portfolio_html' not in st.session_state:
    st.session_state.portfolio_html = None
if 'generation_step' not in st.session_state:
    st.session_state.generation_step = 0
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'education' not in st.session_state:
    st.session_state.education = []
if 'experience' not in st.session_state:
    st.session_state.experience = []
if 'certifications' not in st.session_state:
    st.session_state.certifications = []

# Header
st.markdown("""
<div class="main-header animated-gradient">
    <h1>🎨 AI-Powered Portfolio Builder</h1>
    <p>Create a stunning, professional portfolio in minutes using AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - API Configuration
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    
    ai_provider = st.selectbox(
        "Choose AI Provider",
        ["OpenAI (GPT-4/3.5)", "Google Gemini"],
        help="Select your preferred AI service"
    )
    
    if "OpenAI" in ai_provider:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys",
            key="openai_key"
        )
        model_choice = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
            help="GPT-4o produces better results but costs more"
        )
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey",
            key="gemini_key"
        )
        model_choice = st.selectbox(
            "Model",
            ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"],
            help="Pro model produces better results. Flash is fast and balanced. Lite is fastest and cheapest."
        )
    
    # Manual API Key Test Button (instead of automatic testing)
    if api_key:
        col1, col2 = st.columns([2, 1])
        with col1:
            test_button = st.button("🔍 Test API Key", use_container_width=True)
        with col2:
            if 'api_valid' in st.session_state and st.session_state.api_valid:
                st.success("✅")
            elif 'api_valid' in st.session_state and not st.session_state.api_valid:
                st.error("❌")
        
        # Only test when button is clicked
        if test_button:
            with st.spinner("Testing API key..."):
                is_valid, message = test_api_key(api_key, ai_provider, model_choice)
                st.session_state.api_valid = is_valid
                if is_valid:
                    st.success("✅ API Key Valid!")
                else:
                    st.error(f"❌ {message}")
    else:
        st.info("👆 Enter your API key above")
        # Reset validation state when key is cleared
        if 'api_valid' in st.session_state:
            del st.session_state.api_valid
    
    st.markdown("---")
    st.markdown("### 📊 Features")
    st.markdown("""
    - ✨ AI-Powered Generation
    - 🎨 Multiple Themes
    - 📱 Fully Responsive
    - 🚀 One-Click Download
    - 🔄 Real-time Preview
    - 🎯 SEO Optimized
    """)

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Personal Info", "💼 Experience & Education", "🎨 Design & Generate", "👀 Preview & Download"])

with tab1:
    st.markdown('<div class="step-indicator">Step 1: Personal Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name *", placeholder="John Doe")
        professional_title = st.text_input("Professional Title *", placeholder="Full Stack Developer | AI Engineer")
        email = st.text_input("Email Address", placeholder="john.doe@example.com")
        phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
        location = st.text_input("Location", placeholder="San Francisco, CA")
    
    with col2:
        github = st.text_input("GitHub Username", placeholder="johndoe")
        linkedin = st.text_input("LinkedIn Username", placeholder="johndoe")
        twitter = st.text_input("Twitter/X Username", placeholder="@johndoe")
        website = st.text_input("Personal Website", placeholder="https://johndoe.com")
        portfolio_url = st.text_input("Behance/Dribbble", placeholder="behance.net/johndoe")
    
    st.markdown("### 📖 About Me")
    bio = st.text_area(
        "Professional Bio *",
        placeholder="Write a compelling summary about yourself, your expertise, passion, and what makes you unique...",
        height=150,
        help="This will be the first thing visitors see. Make it count!"
    )
    
    st.markdown("### 🛠️ Skills & Technologies")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Technical Skills**")
        technical_skills = st.text_area(
            "Technical Skills",
            placeholder="Python, JavaScript, React, Node.js, Docker, AWS",
            height=100,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**Soft Skills**")
        soft_skills = st.text_area(
            "Soft Skills",
            placeholder="Leadership, Communication, Problem Solving, Team Collaboration",
            height=100,
            label_visibility="collapsed"
        )
    
    with col3:
        st.markdown("**Tools & Platforms**")
        tools = st.text_area(
            "Tools",
            placeholder="Git, VS Code, Figma, Jira, Slack",
            height=100,
            label_visibility="collapsed"
        )

with tab2:
    st.markdown('<div class="step-indicator">Step 2: Professional Background</div>', unsafe_allow_html=True)
    
    # Projects Section
    st.markdown("### 🚀 Projects")
    
    num_projects = st.number_input("Number of Projects", min_value=0, max_value=10, value=2)
    
    projects = []
    for i in range(num_projects):
        with st.expander(f"Project {i+1}", expanded=(i==0)):
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                project_name = st.text_input(f"Project Name", key=f"pname_{i}", placeholder="AI Chatbot")
                project_tech = st.text_input(f"Technologies Used", key=f"ptech_{i}", placeholder="Python, OpenAI, Streamlit")
            with pcol2:
                project_url = st.text_input(f"Project URL/GitHub", key=f"purl_{i}", placeholder="github.com/user/project")
                project_date = st.text_input(f"Date", key=f"pdate_{i}", placeholder="Jan 2024 - Present")
            
            project_desc = st.text_area(
                f"Project Description",
                key=f"pdesc_{i}",
                placeholder="Describe the project, your role, impact, and key achievements...",
                height=100
            )
            
            if project_name:
                projects.append({
                    "name": project_name,
                    "description": project_desc,
                    "technologies": project_tech,
                    "url": project_url,
                    "date": project_date
                })
    
    st.markdown("---")
    
    # Experience Section
    st.markdown("### 💼 Work Experience")
    
    num_experience = st.number_input("Number of Positions", min_value=0, max_value=10, value=2)
    
    experiences = []
    for i in range(num_experience):
        with st.expander(f"Position {i+1}", expanded=(i==0)):
            ecol1, ecol2 = st.columns(2)
            with ecol1:
                job_title = st.text_input(f"Job Title", key=f"jtitle_{i}", placeholder="Senior Software Engineer")
                company = st.text_input(f"Company", key=f"company_{i}", placeholder="Tech Corp Inc.")
            with ecol2:
                job_location = st.text_input(f"Location", key=f"jloc_{i}", placeholder="Remote")
                job_duration = st.text_input(f"Duration", key=f"jdur_{i}", placeholder="Jan 2022 - Present")
            
            job_desc = st.text_area(
                f"Responsibilities & Achievements",
                key=f"jdesc_{i}",
                placeholder="• Led a team of 5 developers\n• Increased performance by 40%\n• Implemented CI/CD pipeline",
                height=100
            )
            
            if job_title:
                experiences.append({
                    "title": job_title,
                    "company": company,
                    "location": job_location,
                    "duration": job_duration,
                    "description": job_desc
                })
    
    st.markdown("---")
    
    # Education Section
    st.markdown("### 🎓 Education")
    
    num_education = st.number_input("Number of Degrees", min_value=0, max_value=5, value=1)
    
    education = []
    for i in range(num_education):
        with st.expander(f"Education {i+1}", expanded=(i==0)):
            edcol1, edcol2 = st.columns(2)
            with edcol1:
                degree = st.text_input(f"Degree", key=f"degree_{i}", placeholder="Bachelor of Science in Computer Science")
                institution = st.text_input(f"Institution", key=f"inst_{i}", placeholder="Stanford University")
            with edcol2:
                grad_year = st.text_input(f"Graduation Year", key=f"grad_{i}", placeholder="2020")
                gpa = st.text_input(f"GPA (Optional)", key=f"gpa_{i}", placeholder="3.8/4.0")
            
            if degree:
                education.append({
                    "degree": degree,
                    "institution": institution,
                    "year": grad_year,
                    "gpa": gpa
                })
    
    st.markdown("---")
    
    # Certifications
    st.markdown("### 🏆 Certifications & Awards")
    certifications = st.text_area(
        "List your certifications and awards",
        placeholder="• AWS Certified Solutions Architect\n• Google Cloud Professional\n• Hackathon Winner 2023",
        height=100
    )

with tab3:
    st.markdown('<div class="step-indicator">Step 3: Design & Generate</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Theme Selection")
        theme = st.selectbox(
            "Choose Theme",
            ["Modern Gradient", "Minimalist", "Creative Bold", "Professional Dark", 
             "Elegant Light", "Cyberpunk Neon", "Nature Green", "Sunset Orange"],
            help="Select a color scheme for your portfolio"
        )
        
        color_schemes = get_color_schemes()
        selected_scheme = color_schemes.get(theme, color_schemes["Modern Gradient"])
        
        st.markdown(f"""
        <div style="background: {selected_scheme['primary']}; padding: 20px; border-radius: 10px; color: white;">
            <strong>Primary Color</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        layout_style = st.selectbox(
            "Layout Style",
            ["Single Page Scroll", "Multi-Section with Tabs", "Grid Layout", "Side Navigation"],
            help="Choose how your portfolio is structured"
        )
    
    with col2:
        st.markdown("### ✍️ Typography")
        font_pair = st.selectbox(
            "Font Pairing",
            ["Poppins & Roboto", "Montserrat & Open Sans", "Playfair & Source Sans", 
             "Inter & Lora", "Space Grotesk & DM Sans"],
            help="Select fonts for headings and body text"
        )
        
        animations = st.multiselect(
            "Animations & Effects",
            ["Fade In", "Slide In", "Parallax Scrolling", "Hover Effects", 
             "Typing Animation", "Particle Background"],
            default=["Fade In", "Hover Effects"],
            help="Add interactive elements to your portfolio"
        )
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Additional Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        include_contact_form = st.checkbox("Include Contact Form", value=True)
        include_resume_download = st.checkbox("Resume Download Button", value=True)
    
    with col2:
        include_testimonials = st.checkbox("Testimonials Section", value=False)
        include_blog = st.checkbox("Blog/Articles Section", value=False)
    
    with col3:
        seo_optimize = st.checkbox("SEO Optimization", value=True)
        analytics = st.checkbox("Google Analytics Ready", value=True)
    
    st.markdown("---")
    
    # Generate Button
    if not api_key:
        st.warning("⚠️ Please enter your API key in the sidebar to generate your portfolio.")
    else:
        if st.button("🚀 Generate My Portfolio", use_container_width=True, type="primary"):
            # Validation
            if not full_name or not professional_title or not bio:
                st.error("❌ Please fill in all required fields (Name, Title, Bio) in Step 1")
            else:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Preparing data
                status_text.markdown("### 🔄 Preparing your information...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                # Compile all data
                portfolio_data = {
                    "personal": {
                        "name": full_name,
                        "title": professional_title,
                        "bio": bio,
                        "email": email,
                        "phone": phone,
                        "location": location
                    },
                    "social": {
                        "github": github,
                        "linkedin": linkedin,
                        "twitter": twitter,
                        "website": website,
                        "portfolio": portfolio_url
                    },
                    "skills": {
                        "technical": technical_skills,
                        "soft": soft_skills,
                        "tools": tools
                    },
                    "projects": projects,
                    "experience": experiences,
                    "education": education,
                    "certifications": certifications,
                    "design": {
                        "theme": theme,
                        "layout": layout_style,
                        "fonts": font_pair,
                        "animations": animations,
                        "color_scheme": selected_scheme
                    },
                    "options": {
                        "contact_form": include_contact_form,
                        "resume_button": include_resume_download,
                        "testimonials": include_testimonials,
                        "blog": include_blog,
                        "seo": seo_optimize,
                        "analytics": analytics
                    }
                }
                
                # Step 2: Connecting to AI
                status_text.markdown("### 🤖 Connecting to AI service...")
                progress_bar.progress(40)
                time.sleep(0.5)
                
                # Step 3: Generating HTML
                status_text.markdown("### ✨ AI is crafting your portfolio...")
                progress_bar.progress(60)
                
                try:
                    html_content = generate_portfolio_html(
                        portfolio_data, 
                        api_key, 
                        ai_provider, 
                        model_choice
                    )
                    
                    # Step 4: Optimizing
                    status_text.markdown("### 🎨 Applying final touches...")
                    progress_bar.progress(85)
                    time.sleep(0.5)
                    
                    # Step 5: Complete
                    progress_bar.progress(100)
                    status_text.markdown("### ✅ Your portfolio is ready!")
                    time.sleep(0.5)
                    
                    st.session_state.portfolio_html = html_content
                    
                    st.markdown("""
                    <div class="success-message">
                        🎉 Portfolio Generated Successfully! Check the Preview & Download tab.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error generating portfolio: {str(e)}")
                    status_text.empty()
                    progress_bar.empty()

with tab4:
    st.markdown('<div class="step-indicator">Step 4: Preview & Download</div>', unsafe_allow_html=True)
    
    if st.session_state.portfolio_html:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download HTML
            b64 = base64.b64encode(st.session_state.portfolio_html.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="portfolio.html" style="text-decoration: none;"><button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 30px; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; width: 100%;">💾 Download HTML</button></a>'
            st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            # Copy to clipboard button
            if st.button("📋 Copy HTML Code", use_container_width=True):
                st.code(st.session_state.portfolio_html[:500] + "...", language="html")
                st.success("Code preview shown above!")
        
        with col3:
            # Generate new version
            if st.button("🔄 Generate New Version", use_container_width=True):
                st.session_state.portfolio_html = None
                st.rerun()
        
        st.markdown("---")
        
        # Preview
        st.markdown("### 👀 Live Preview")
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.components.v1.html(st.session_state.portfolio_html, height=600, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show file info
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>File Size</h3>
                <h2>{len(st.session_state.portfolio_html) / 1024:.1f} KB</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Generated</h3>
                <h2>{datetime.now().strftime('%H:%M')}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Status</h3>
                <h2>✅ Ready</h2>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Generate your portfolio in the 'Design & Generate' tab to see the preview here!")
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Next Steps After Generation:</h3>
            <ul>
                <li>✅ Preview your portfolio in real-time</li>
                <li>💾 Download as a single HTML file</li>
                <li>🚀 Deploy to GitHub Pages, Netlify, or Vercel</li>
                <li>✏️ Customize further if needed</li>
                <li>📱 Test on different devices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; opacity: 0.7;">
    <p>Made with ❤️ by Disha</p>
""", unsafe_allow_html=True)
