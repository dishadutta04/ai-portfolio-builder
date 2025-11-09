from openai import OpenAI
import google.generativeai as genai
import streamlit as st

def test_api_key(api_key, provider, model):
    """Test if API key is valid"""
    try:
        if "OpenAI" in provider:
            client = OpenAI(api_key=api_key)
            client.models.list()  # Test OpenAI API
            return True, "API key is valid"
        else:
            genai.configure(api_key=api_key)
            test_model = genai.GenerativeModel(model)  # Use the provided model
            response = test_model.generate_content("Hello")  # Simple test prompt
            return True, "API key is valid"
    except Exception as e:
        return False, f"API key validation failed: {str(e)}"

def generate_portfolio_html(data, api_key, provider, model):
    """Generate complete portfolio HTML using AI"""

    # Create comprehensive prompt
    prompt = f"""
    Create a STUNNING, PROFESSIONAL, and FULLY RESPONSIVE portfolio website as a single HTML file with inline CSS and JavaScript.

    ## Personal Information:
    - Name: {data['personal']['name']}
    - Title: {data['personal']['title']}
    - Bio: {data['personal']['bio']}
    - Email: {data['personal']['email']}
    - Phone: {data['personal']['phone']}
    - Location: {data['personal']['location']}

    ## Social Links:
    - GitHub: {data['social']['github']}
    - LinkedIn: {data['social']['linkedin']}
    - Twitter: {data['social']['twitter']}
    - Website: {data['social']['website']}

    ## Skills:
    - Technical: {data['skills']['technical']}
    - Soft Skills: {data['skills']['soft']}
    - Tools: {data['skills']['tools']}

    ## Projects:
    {chr(10).join([f"### {p['name']}\n- Tech: {p['technologies']}\n- Description: {p['description']}\n- URL: {p['url']}\n- Date: {p['date']}" for p in data['projects']]) if data['projects'] else "No projects listed"}

    ## Experience:
    {chr(10).join([f"### {e['title']} at {e['company']}\n- Duration: {e['duration']}\n- Location: {e['location']}\n- Description: {e['description']}" for e in data['experience']]) if data['experience'] else "No experience listed"}

    ## Education:
    {chr(10).join([f"### {ed['degree']}\n- Institution: {ed['institution']}\n- Year: {ed['year']}\n- GPA: {ed['gpa']}" for ed in data['education']]) if data['education'] else "No education listed"}

    ## Certifications:
    {data['certifications'] if data['certifications'] else "No certifications listed"}

    ## Design Requirements:
    - Theme: {data['design']['theme']}
    - Layout: {data['design']['layout']}
    - Fonts: {data['design']['fonts']}
    - Animations: {', '.join(data['design']['animations'])}
    - Primary Color: {data['design']['color_scheme']['primary']}
    - Secondary Color: {data['design']['color_scheme']['secondary']}

    ## Features to Include:
    - Contact Form: {data['options']['contact_form']}
    - Resume Download Button: {data['options']['resume_button']}
    - Testimonials: {data['options']['testimonials']}
    - SEO Optimized: {data['options']['seo']}
    - Google Analytics Ready: {data['options']['analytics']}

    ## Technical Requirements:
    1. Create a COMPLETE single HTML file with inline CSS and JavaScript
    2. Make it FULLY RESPONSIVE (mobile, tablet, desktop)
    3. Use the specified color scheme and fonts
    4. Include smooth scroll behavior
    5. Add hover effects and animations as specified
    6. Use Font Awesome icons (via CDN)
    7. Include meta tags for SEO with proper title, description, keywords
    8. Add smooth transitions between sections
    9. Make navigation sticky/fixed on scroll
    10. Include a hero section with gradient background matching the theme
    11. Use CSS Grid/Flexbox for modern, responsive layouts
    12. Add scroll-triggered animations using Intersection Observer
    13. Include social media icons with proper links
    14. Make all buttons and links beautifully styled with hover effects
    15. Add a professional footer with copyright and links
    16. Use CSS variables for easy theming
    17. Make the contact form functional with FormSpree or EmailJS integration
    18. Add smooth page transitions and loading states
    19. Include proper semantic HTML5
    20. Ensure WCAG accessibility compliance

    ## Style Guidelines:
    - Use the {data['design']['theme']} color palette with gradients
    - Apply {data['design']['fonts']} font pairing from Google Fonts
    - Implement {data['design']['layout']} layout structure
    - Include these animations: {', '.join(data['design']['animations'])}
    - Professional spacing, shadows, rounded corners, and transitions
    - Use placeholder images from placeholder.com or unsplash

    ## CRITICAL REQUIREMENTS:
    - Start DIRECTLY with <!DOCTYPE html>
    - End with </html>
    - Do NOT include markdown code blocks (```)
    - Do NOT include explanations or comments outside the HTML
    - Make it production-ready and visually stunning
    - Ensure all sections flow naturally
    - Test all interactive elements work properly

    Generate ONLY the complete, production-ready HTML code now.
    """

    try:
        if "OpenAI" in provider:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert web developer and designer who creates stunning, modern, responsive portfolio websites. Generate complete, production-ready HTML with inline CSS and JavaScript."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=16000
            )
            html_content = response.choices[0].message.content
        else:
            genai.configure(api_key=api_key)
            ai_model = genai.GenerativeModel(model)
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 16000,
            }
            response = ai_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            html_content = response.text

        # Clean the response
        html_content = html_content.strip()

        # Remove markdown code blocks if present
        if html_content.startswith('```html'):
            html_content = html_content[7:]
        elif html_content.startswith('```'):
            html_content = html_content[3:]

        if html_content.endswith('```'):
            html_content = html_content[:-3]

        # Ensure it starts with DOCTYPE
        if not html_content.strip().startswith('<!DOCTYPE'):
            if '<!DOCTYPE' in html_content:
                html_content = html_content[html_content.index('<!DOCTYPE'):]

        return html_content.strip()

    except Exception as e:
        raise Exception(f"Error generating portfolio: {str(e)}")
