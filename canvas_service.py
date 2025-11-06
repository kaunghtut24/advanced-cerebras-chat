"""
Interactive Canvas Service for Cerebras Chat
Provides HTML/CSS/JS rendering and preview capabilities
"""

import re
from typing import Dict, Any, Optional, Tuple
import html as html_module

class CanvasService:
    """Service for handling interactive canvas operations"""
    
    def __init__(self):
        """Initialize canvas service"""
        self.templates = {
            'basic': self._get_basic_template(),
            'chart': self._get_chart_template(),
            'form': self._get_form_template(),
            'animation': self._get_animation_template()
        }
    
    def _get_basic_template(self) -> str:
        """Get basic HTML template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canvas Preview</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
        }
    </style>
</head>
<body>
    <h1>Hello, Canvas!</h1>
    <p>Edit the HTML, CSS, and JavaScript to create your interactive content.</p>
</body>
</html>"""
    
    def _get_chart_template(self) -> str:
        """Get chart template with Chart.js"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chart Example</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
        }
        #chartContainer {
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div id="chartContainer">
        <canvas id="myChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>"""
    
    def _get_form_template(self) -> str:
        """Get interactive form template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        #result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f0f0f0;
            border-radius: 4px;
            display: none;
        }
    </style>
</head>
<body>
    <h1>Contact Form</h1>
    <form id="contactForm">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" required>
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" required>
        </div>
        <div class="form-group">
            <label for="message">Message:</label>
            <textarea id="message" rows="4" required></textarea>
        </div>
        <button type="submit">Submit</button>
    </form>
    <div id="result"></div>
    <script>
        document.getElementById('contactForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            const result = document.getElementById('result');
            result.innerHTML = `<h3>Form Submitted!</h3>
                <p><strong>Name:</strong> ${name}</p>
                <p><strong>Email:</strong> ${email}</p>
                <p><strong>Message:</strong> ${message}</p>`;
            result.style.display = 'block';
        });
    </script>
</body>
</html>"""
    
    def _get_animation_template(self) -> str:
        """Get animation template"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animation Example</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        }
        .box {
            width: 100px;
            height: 100px;
            background-color: #fff;
            border-radius: 10px;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-100px);
            }
        }
    </style>
</head>
<body>
    <div class="box"></div>
</body>
</html>"""
    
    def validate_html(self, html_content: str) -> Tuple[bool, Optional[str]]:
        """
        Validate HTML content for security issues
        
        Args:
            html_content: HTML content to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for dangerous patterns
        dangerous_patterns = [
            r'<script[^>]*>.*?document\.cookie',
            r'<script[^>]*>.*?localStorage',
            r'<script[^>]*>.*?sessionStorage',
            r'<iframe[^>]*src=["\'](?!https?://)',
            r'javascript:',
            r'on\w+\s*=',  # Inline event handlers
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, html_content, re.IGNORECASE | re.DOTALL):
                return False, f"Potentially dangerous pattern detected: {pattern}"
        
        return True, None
    
    def create_preview(self, html: str = "", css: str = "", js: str = "") -> Dict[str, Any]:
        """
        Create a preview HTML document from separate HTML, CSS, and JS
        
        Args:
            html: HTML content
            css: CSS content
            js: JavaScript content
            
        Returns:
            Dictionary containing preview HTML and metadata
        """
        # Combine into full HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canvas Preview</title>
    <style>
        {css}
    </style>
</head>
<body>
    {html}
    <script>
        {js}
    </script>
</body>
</html>"""
        
        # Validate
        is_valid, error_msg = self.validate_html(full_html)
        
        if not is_valid:
            return {
                'success': False,
                'error': error_msg,
                'preview_html': None
            }
        
        return {
            'success': True,
            'error': None,
            'preview_html': full_html
        }
    
    def get_template(self, template_name: str) -> Optional[str]:
        """
        Get a template by name
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template HTML or None if not found
        """
        return self.templates.get(template_name)
    
    def list_templates(self) -> list:
        """Get list of available templates"""
        return list(self.templates.keys())

# Global canvas service instance
canvas_service = CanvasService()

