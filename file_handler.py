"""
File upload and processing handler
"""

import os
import logging
from pathlib import Path
from werkzeug.utils import secure_filename
from typing import Optional, List

# Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 52428800))  # 50MB default
ALLOWED_EXTENSIONS = os.environ.get(
    'ALLOWED_EXTENSIONS',
    'pdf,docx,doc,pptx,ppt,xlsx,xls,txt,md,html,jpg,jpeg,png,gif'
).split(',')


class FileHandler:
    """Handle file uploads and validation"""
    
    def __init__(self, upload_folder: str = UPLOAD_FOLDER):
        self.upload_folder = Path(upload_folder)
        self.upload_folder.mkdir(parents=True, exist_ok=True)
        self.allowed_extensions = set(ext.strip().lower() for ext in ALLOWED_EXTENSIONS)
        self.max_file_size = MAX_FILE_SIZE
        
        logging.info(f"FileHandler initialized with upload folder: {self.upload_folder}")
        logging.info(f"Allowed extensions: {', '.join(self.allowed_extensions)}")
        logging.info(f"Max file size: {self.max_file_size / (1024*1024):.2f} MB")
    
    def allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def validate_file_size(self, file_size: int) -> bool:
        """Check if file size is within limits"""
        return file_size <= self.max_file_size
    
    def save_file(self, file, kb_name: str) -> Optional[str]:
        """
        Save uploaded file to disk
        
        Args:
            file: FileStorage object from Flask
            kb_name: Knowledge base name (used as subfolder)
        
        Returns:
            Path to saved file or None if failed
        """
        if not file or not file.filename:
            logging.error("No file provided")
            return None
        
        if not self.allowed_file(file.filename):
            logging.error(f"File type not allowed: {file.filename}")
            return None
        
        # Create knowledge base subfolder
        kb_folder = self.upload_folder / kb_name
        kb_folder.mkdir(parents=True, exist_ok=True)
        
        # Secure filename
        filename = secure_filename(file.filename)
        
        # Handle duplicate filenames
        file_path = kb_folder / filename
        if file_path.exists():
            # Add counter to filename
            name_parts = filename.rsplit('.', 1)
            base_name = name_parts[0]
            extension = name_parts[1] if len(name_parts) > 1 else ''
            
            counter = 1
            while file_path.exists():
                new_filename = f"{base_name}_{counter}.{extension}" if extension else f"{base_name}_{counter}"
                file_path = kb_folder / new_filename
                counter += 1
        
        try:
            file.save(str(file_path))
            logging.info(f"File saved: {file_path}")
            return str(file_path)
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
            return None
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from disk"""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                logging.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to delete file: {e}")
            return False
    
    def list_files(self, kb_name: Optional[str] = None) -> List[dict]:
        """
        List uploaded files
        
        Args:
            kb_name: Optional knowledge base name to filter by
        
        Returns:
            List of file information dictionaries
        """
        files = []
        
        if kb_name:
            search_path = self.upload_folder / kb_name
            if not search_path.exists():
                return []
        else:
            search_path = self.upload_folder
        
        try:
            for file_path in search_path.rglob('*'):
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        'name': file_path.name,
                        'path': str(file_path),
                        'size': stat.st_size,
                        'modified': stat.st_mtime,
                        'kb_name': file_path.parent.name if kb_name is None else kb_name
                    })
        except Exception as e:
            logging.error(f"Failed to list files: {e}")
        
        return files
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get information about a specific file"""
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                return None
            
            stat = path.stat()
            return {
                'name': path.name,
                'path': str(path),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'extension': path.suffix.lower().lstrip('.')
            }
        except Exception as e:
            logging.error(f"Failed to get file info: {e}")
            return None


# Global file handler instance
file_handler = FileHandler()
