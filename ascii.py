from PIL import Image
import numpy as np

class NeofetchProfileGenerator:
    def __init__(self, image_path, profile_data):
        self.image_path = image_path
        self.profile_data = profile_data
        self.ascii_chars = '@%#*+=-:. '
        
    def image_to_ascii(self, width=40):
        """Convert image to ASCII art"""
        # Open and resize image
        img = Image.open(self.image_path)
        aspect_ratio = img.height / img.width
        height = int(width * aspect_ratio * 0.5)  # Multiply by 0.5 to account for terminal character spacing
        img = img.resize((width, height))
        
        # Convert to grayscale
        img = img.convert('L')
        pixels = np.array(img)
        
        # Map pixels to ASCII characters
        ascii_img = []
        for row in pixels:
            ascii_row = ''
            for pixel in row:
                ascii_row += self.ascii_chars[pixel * len(self.ascii_chars) // 256]
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
        total_width = art_width + 300 + padding * 3  # 300px for profile info
        total_height = max(art_height, len(self.profile_data) * 25) + padding * 2
        
        svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{total_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .ascii-art {{ font-family: monospace; font-size: 14px; white-space: pre; }}
        .profile-info {{ font-family: Arial, sans-serif; font-size: 14px; }}
        .container {{ fill: #282a36; }}
        .text {{ fill: #f8f8f2; }}
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
        
        svg += '''</text>
    
    <!-- Profile Information -->'''
        
        # Add profile information
        info_x = art_width + padding * 2
        info_y = padding + 20
        
        for key, value in self.profile_data.items():
            svg += f'''
    <text x="{info_x}" y="{info_y}" class="profile-info text">
        <tspan style="fill: #ff79c6">{key}</tspan>: {value}
    </text>'''
            info_y += 25
        
        svg += '\n</svg>'
        return svg

def main():
    # Example profile data
    profile_data = {
        'Name': 'John Doe',
        'Age': '25',
        'Email': 'john@example.com',
        'Location': 'San Francisco, CA',
        'Occupation': 'Software Engineer',
        'Languages': 'Python, JavaScript, Rust',
        'Interests': 'Open Source, AI, Gaming',
        'GitHub': '@johndoe'
    }
    
    # Create generator instance
    generator = NeofetchProfileGenerator('photo.png', profile_data)
    
    # Generate SVG and save to file
    svg_content = generator.generate_svg()
    with open('github_profile.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)

if __name__ == '__main__':
    main()