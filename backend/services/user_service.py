class UserService:
    """Service class for user-related operations"""
    
    # Simulate database with a list (trong thực tế sẽ kết nối với database)
    users = [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'age': 30},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25},
        {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35}
    ]
    
    @classmethod
    def get_all_users(cls):
        """Get all users"""
        return cls.users
    
    @classmethod
    def get_user_by_id(cls, user_id):
        """Get user by ID"""
        for user in cls.users:
            if user['id'] == user_id:
                return user
        return None
    
    @classmethod
    def create_user(cls, user_data):
        """Create new user"""
        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Generate new ID
        new_id = max([user['id'] for user in cls.users], default=0) + 1
        
        # Create new user
        new_user = {
            'id': new_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'age': user_data.get('age', 0)
        }
        
        cls.users.append(new_user)
        return new_user
    
    @classmethod
    def update_user(cls, user_id, user_data):
        """Update user"""
        for i, user in enumerate(cls.users):
            if user['id'] == user_id:
                # Update user data
                if 'name' in user_data:
                    cls.users[i]['name'] = user_data['name']
                if 'email' in user_data:
                    cls.users[i]['email'] = user_data['email']
                if 'age' in user_data:
                    cls.users[i]['age'] = user_data['age']
                return cls.users[i]
        return None
    
    @classmethod
    def delete_user(cls, user_id):
        """Delete user"""
        for i, user in enumerate(cls.users):
            if user['id'] == user_id:
                cls.users.pop(i)
                return True
        return False
