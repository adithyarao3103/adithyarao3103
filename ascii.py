from PIL import Image
import numpy as np

class NeofetchProfileGenerator:
    def __init__(self, image_path, profile_data):
        self.image_path = image_path
        self.profile_data = profile_data
        # Using detailed ASCII characters for better representation
        self.ascii_chars = '@%#*+=-:. '
        
    def image_to_ascii(self, width=40):
        """Convert image to ASCII art"""
        # Open and resize image
        img = Image.open(self.image_path)
        aspect_ratio = img.height / img.width
        height = int(width * aspect_ratio * 0.5)  # Multiply by 0.5 to account for terminal character spacing
        img = img.resize((width, height))
        
        # Convert to RGBA to handle transparency
        img = img.convert('RGBA')
        pixels = np.array(img)
        
        # Create alpha mask
        alpha = pixels[:, :, 3]
        # Convert to grayscale (only for non-transparent pixels)
        gray = np.dot(pixels[:, :, :3], [0.299, 0.587, 0.114])
        
        # Map pixels to ASCII characters
        ascii_img = []
        for i, row in enumerate(gray):
            ascii_row = ''
            for pixel, a in zip(row, alpha[i]):
                if a < 128:  # If pixel is mostly transparent
                    ascii_row += ' '
                else:
                    ascii_row += self.ascii_chars[int(pixel * len(self.ascii_chars) / 256)]
            ascii_img.append(ascii_row)
        
        return '\n'.join(ascii_img)
    
    def generate_svg(self):
        """Generate SVG with ASCII art and profile information"""
        ascii_art = self.image_to_ascii()
        ascii_lines = ascii_art.split('\n')
        
        # Calculate dimensions
        char_width = 8  # Approximate width of monospace character
        char_height = 16  # Approximate height of monospace character
        art_width = max(len(line) for line in ascii_lines) * char_width
        art_height = len(ascii_lines) * char_height
        
        # Add padding and calculate total dimensions
        padding = 20
        info_width = 300  # Width for profile info
        total_width = art_width + info_width + padding * 3
        total_height = max(art_height, len(self.profile_data) * 25) + padding * 2
        
        svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        @font-face {{
            font-family: 'Terminal';
            src: local('Courier New');
        }}
        .ascii-art {{ 
            font-family: 'Terminal', monospace; 
            font-size: 14px; 
            white-space: pre;
        }}
        .profile-info {{ 
            font-family: 'Terminal', monospace; 
            font-size: 14px; 
        }}
        .container {{ 
            fill: #2d2b27; 
        }}
        .text {{ 
            fill: #ffd7a7; 
        }}
        .label {{
            fill: #ffa94d;
        }}
        .separator {{
            fill: #ffc078;
        }}
    </style>
    
    <!-- Background -->
    <rect width="100%" height="100%" class="container"/>
    
    <!-- ASCII Art -->
    <text x="{padding}" y="{padding + char_height}" class="ascii-art text">'''
        
        # Add ASCII art lines
        for i, line in enumerate(ascii_lines):
            if i > 0:
                svg += f'\n        <tspan x="{padding}" dy="{char_height}">{line}</tspan>'
            else:
                svg += line
        
        svg += '</text>'
        
        # Calculate vertical center position for profile info
        info_total_height = len(self.profile_data) * 25  # Total height of all info lines
        info_start_y = (total_height - info_total_height) / 2  # Center vertically
        
        # Add profile information container
        info_x = art_width + padding * 2
        svg += f'''
    <!-- Profile Information -->
    <foreignObject x="{info_x}" y="{padding}" width="{info_width}" height="{total_height - padding * 2}">
        <div xmlns="http://www.w3.org/1999/xhtml" style="
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            font-family: 'Terminal', monospace;
            font-size: 14px;
            color: #ffd7a7;
        ">'''
        
        # Add profile information
        for key, value in self.profile_data.items():
            svg += f'''
            <div style="margin: 5px 0; white-space: normal; word-wrap: break-word;">
                <span style="color: #ffa94d;">{key}</span>
                <span style="color: #ffc078;"> → </span>
                <span>{value}</span>
            </div>'''
        
        svg += '''
        </div>
    </foreignObject>
</svg>'''
        
        return svg

def main():
    # Example profile data
    profile_data = {
        'Name': 'Adithya A Rao',
        'Job.Desc': 'Physics',
        'Uptime': '24 years',
        'Location': 'India',
        'Past': 'Theoretical and Computational QFT',
        'Pres.Learn': 'Deep Learning, Quantum Computing',
        'Prog.Lang': 'C++, Python, JavaScript, Julia',
        'Website': 'adithyarao3103.github.io',
        'Email': 'adithyarao3132001@gmail.com',
    }
    
    # Create generator instance
    generator = NeofetchProfileGenerator('photo.png', profile_data)
    
    # Generate SVG and save to file
    svg_content = generator.generate_svg()
    with open('github_profile.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)

if __name__ == '__main__':
    main()