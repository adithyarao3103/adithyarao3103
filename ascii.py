from PIL import Image
import numpy as np
from typing import Dict, List

class NeofetchProfileGenerator:
    def __init__(self, image_path, profile_sections: Dict[str, Dict[str, str]]):
        self.image_path = image_path
        self.profile_sections = profile_sections
        self.ascii_chars = '@%#*+=-:. '
        
    def image_to_ascii(self, width=40):
        """Convert image to ASCII art"""
        img = Image.open(self.image_path)
        aspect_ratio = img.height / img.width
        # Adjust for character aspect ratio in monospace font
        height = int(width * aspect_ratio * 0.5)  # 0.5 compensates for character height/width ratio
        img = img.resize((width, height))
        
        img = img.convert('RGBA')
        pixels = np.array(img)
        
        alpha = pixels[:, :, 3]
        gray = np.dot(pixels[:, :, :3], [0.299, 0.587, 0.114])
        
        ascii_img = []
        for i, row in enumerate(gray):
            ascii_row = ''
            for pixel, a in zip(row, alpha[i]):
                if a < 128:
                    ascii_row += ' '
                else:
                    ascii_row += self.ascii_chars[int(pixel * len(self.ascii_chars) / 256)]
            ascii_img.append(ascii_row)
        
        return '\n'.join(ascii_img)
    
    def generate_svg(self):
        """Generate SVG with ASCII art and sectioned profile information"""
        ascii_art = self.image_to_ascii()
        ascii_lines = ascii_art.split('\n')
        
        # Adjust character dimensions for JetBrains Mono
        char_width = 8.5  # JetBrains Mono character width
        char_height = 17  # JetBrains Mono character height
        art_width = max(len(line) for line in ascii_lines) * char_width
        art_height = len(ascii_lines) * char_height
        
        padding = 20
        info_width = 400
        total_width = art_width + info_width + padding * 3
        
        # Calculate total height based on sections
        total_items = sum(len(section) for section in self.profile_sections.values())
        section_padding = 5
        total_height = max(
            art_height + padding * 2,
            total_items * 25 + (len(self.profile_sections) - 1) * section_padding + padding * 2
        )

        svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @font-face {{
            font-family: 'JetBrainsMono';
            src: url('https://cdn.jsdelivr.net/gh/JetBrains/JetBrainsMono/web/woff2/JetBrainsMono-Regular.woff2') format('woff2');
        }}
        .ascii-art, .profile-info, .section-title {{ 
            font-family: 'JetBrainsMono', monospace;
            font-size: 14px;
            letter-spacing: 0;
        }}
        .ascii-art {{
            white-space: pre;
            letter-spacing: 0;
        }}
        .container {{ 
            fill: #0d1117; 
        }}
        .text {{ 
            font-family: 'JetBrainsMono', monospace;
            fill: #c9d1d9; 
            font-size: 12px!important;
        }}
        .label {{
            fill: #58a6ff;
        }}
        .section-title {{
            fill: #58a6ff;
        }}
        .dots {{
            fill: #8b949e;
            opacity: 0.25;
            letter-spacing: 2px;
        }}
        .center-dot {{
            fill: #58a6ff;
        }}
    </style>
    
    <!-- Background -->
    <rect width="100%" height="100%" class="container"/>
    
    <!-- ASCII Art -->
    <text x="{padding}" y="{padding + char_height}" class="ascii-art text">'''
        
        # Add ASCII art lines with preserved spacing
        for i, line in enumerate(ascii_lines):
            if i > 0:
                svg += f'\n        <tspan x="{padding}" dy="{char_height}">{line}</tspan>'
            else:
                svg += line
        
        svg += '</text>'
        
        # Calculate vertical center position for profile info
        info_total_height = (
            total_items * 25 + 
            (len(self.profile_sections) - 1) * section_padding
        )
        info_start_y = (total_height - info_total_height) / 2
        
        info_x = art_width + padding * 2
        current_y = info_start_y

        # Process each section
        for section_title, section_data in self.profile_sections.items():
            # Add section title with continuous line
            svg += f'''
    <text x="{info_x}" y="{current_y}" class="section-title">- {section_title}</text>
    <line x1="{info_x + len(section_title) * char_width + 16}" y1="{current_y - 4}" 
          x2="{info_x + info_width}" y2="{current_y - 4}" 
          stroke="#58a6ff" stroke-width="1"/>'''
            current_y += 25

            # Add section data
            for key, value in section_data.items():
                dot_x = info_x
                label_x = dot_x + 15
                value_x = info_x + info_width
                
                # Calculate number of dots needed
                available_space = value_x - (label_x + len(key) * char_width + 10)
                dot_count = max(3, int(available_space / 6))  # Adjusted for dot spacing
                
                svg += f'''
    <circle cx="{dot_x + 4}" cy="{current_y - 4}" r="2.5" class="center-dot"/>
    <text x="{label_x}" y="{current_y}" class="profile-info">
        <tspan class="label">{key}</tspan>
        <tspan class="dots">{"." * dot_count}</tspan>
    </text>
    <text x="{value_x}" y="{current_y}" class="text" text-anchor="end">
        <tspan>{value}</tspan>
    </text>'''
                current_y += 25
            
            current_y += section_padding
        
        svg += '\n</svg>'
        return svg

def main():
    # Example profile data with sections
    profile_sections = {
        "@adithyarao3103": {
            "Name": "Adithya A Rao",
            "Job.Desc": "Physics",
            "Uptime": "24 years",
            "Location": "India"
        },
        "Background": {
            "Past": "Theoretical and Computational QFT",
            "Pres.Learn": "Deep Learning, Quantum Computing",
            "Prog.Lang": "C++, Python, JavaScript, Julia"
        },
        "Contact": {
            "Website": "adithyarao3103.github.io",
            "Email": "adithyarao3132001@gmail.com"
        }
    }
    
    generator = NeofetchProfileGenerator('photo.png', profile_sections)
    svg_content = generator.generate_svg()
    with open('github_profile.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)

if __name__ == '__main__':
    main()