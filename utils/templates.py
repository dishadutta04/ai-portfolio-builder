def get_color_schemes():
    """Return predefined color schemes"""
    return {
        "Modern Gradient": {
            "primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "secondary": "#667eea",
            "accent": "#764ba2"
        },
        "Minimalist": {
            "primary": "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)",
            "secondary": "#4a5568",
            "accent": "#718096"
        },
        "Creative Bold": {
            "primary": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "secondary": "#f093fb",
            "accent": "#f5576c"
        },
        "Professional Dark": {
            "primary": "linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%)",
            "secondary": "#203a43",
            "accent": "#2c5364"
        },
        "Elegant Light": {
            "primary": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
            "secondary": "#fcb69f",
            "accent": "#ffecd2"
        },
        "Cyberpunk Neon": {
            "primary": "linear-gradient(135deg, #00f5ff 0%, #ff00ff 100%)",
            "secondary": "#00f5ff",
            "accent": "#ff00ff"
        },
        "Nature Green": {
            "primary": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
            "secondary": "#11998e",
            "accent": "#38ef7d"
        },
        "Sunset Orange": {
            "primary": "linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)",
            "secondary": "#ff6e7f",
            "accent": "#bfe9ff"
        }
    }

def get_font_pairs():
    """Return font pairing information"""
    return {
        "Poppins & Roboto": {
            "heading": "Poppins",
            "body": "Roboto",
            "url": "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto:wght@300;400;500&display=swap"
        },
        "Montserrat & Open Sans": {
            "heading": "Montserrat",
            "body": "Open Sans",
            "url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Open+Sans:wght@300;400;500&display=swap"
        },
        "Playfair & Source Sans": {
            "heading": "Playfair Display",
            "body": "Source Sans Pro",
            "url": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Sans+Pro:wght@300;400;500&display=swap"
        },
        "Inter & Lora": {
            "heading": "Inter",
            "body": "Lora",
            "url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:wght@400;500&display=swap"
        },
        "Space Grotesk & DM Sans": {
            "heading": "Space Grotesk",
            "body": "DM Sans",
            "url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Sans:wght@400;500&display=swap"
        }
    }
