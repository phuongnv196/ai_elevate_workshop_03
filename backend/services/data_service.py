from datetime import datetime

class DataService:
    """Service class for data-related operations"""
    
    # Simulate database with a list
    data_entries = [
        {
            'id': 1,
            'title': 'Sample Data 1',
            'content': 'This is sample data content 1',
            'created_at': '2025-08-01T10:00:00',
            'category': 'general'
        },
        {
            'id': 2,
            'title': 'Sample Data 2',
            'content': 'This is sample data content 2',
            'created_at': '2025-08-01T11:00:00',
            'category': 'important'
        }
    ]
    
    @classmethod
    def get_all_data(cls):
        """Get all data entries"""
        return cls.data_entries
    
    @classmethod
    def get_data_by_id(cls, data_id):
        """Get data by ID"""
        for entry in cls.data_entries:
            if entry['id'] == data_id:
                return entry
        return None
    
    @classmethod
    def create_data(cls, data):
        """Create new data entry"""
        # Validate required fields
        required_fields = ['title', 'content']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Generate new ID
        new_id = max([entry['id'] for entry in cls.data_entries], default=0) + 1
        
        # Create new data entry
        new_entry = {
            'id': new_id,
            'title': data['title'],
            'content': data['content'],
            'created_at': datetime.now().isoformat(),
            'category': data.get('category', 'general')
        }
        
        cls.data_entries.append(new_entry)
        return new_entry
    
    @classmethod
    def update_data(cls, data_id, data):
        """Update data entry"""
        for i, entry in enumerate(cls.data_entries):
            if entry['id'] == data_id:
                # Update data
                if 'title' in data:
                    cls.data_entries[i]['title'] = data['title']
                if 'content' in data:
                    cls.data_entries[i]['content'] = data['content']
                if 'category' in data:
                    cls.data_entries[i]['category'] = data['category']
                
                cls.data_entries[i]['updated_at'] = datetime.now().isoformat()
                return cls.data_entries[i]
        return None
    
    @classmethod
    def delete_data(cls, data_id):
        """Delete data entry"""
        for i, entry in enumerate(cls.data_entries):
            if entry['id'] == data_id:
                cls.data_entries.pop(i)
                return True
        return False
    
    @classmethod
    def get_data_by_category(cls, category):
        """Get data by category"""
        return [entry for entry in cls.data_entries if entry['category'] == category]
