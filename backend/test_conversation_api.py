"""
Test script for Conversation API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000/api/conversation"

def test_conversation_api():
    """Test all conversation API endpoints"""
    
    print("🧪 Testing Conversation API")
    print("=" * 50)
    
    # Test 1: Get all conversations (should be empty initially)
    print("\n1. Getting all conversations...")
    response = requests.get(f"{BASE_URL}/conversations")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Create a new conversation
    print("\n2. Creating a new conversation...")
    create_data = {"title": "Test AI Conversation"}
    response = requests.post(f"{BASE_URL}/conversations", json=create_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if result.get("success"):
        conversation_id = result["conversation"]["id"]
        print(f"✅ Created conversation with ID: {conversation_id}")
        
        # Test 3: Get messages (should be empty)
        print(f"\n3. Getting messages for conversation {conversation_id}...")
        response = requests.get(f"{BASE_URL}/conversations/{conversation_id}/messages")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 4: Send a chat message (Note: Requires OPENAI_API_KEY)
        print(f"\n4. Sending a chat message...")
        chat_data = {"message": "Hello! Can you tell me about the latest technology trends?"}
        try:
            response = requests.post(f"{BASE_URL}/conversations/{conversation_id}/chat", json=chat_data)
            print(f"Status: {response.status_code}")
            result = response.json()
            if result.get("success"):
                print(f"✅ Chat successful!")
                print(f"AI Response: {result.get('response', 'No response')}")
            else:
                print(f"⚠️ Chat failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"⚠️ Chat request failed: {str(e)}")
            print("Note: This may fail if OPENAI_API_KEY is not configured")
        
        # Test 5: Update conversation title
        print(f"\n5. Updating conversation title...")
        update_data = {"title": "Updated Test Conversation"}
        response = requests.put(f"{BASE_URL}/conversations/{conversation_id}", json=update_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 6: Get all conversations again (should show our updated conversation)
        print("\n6. Getting all conversations again...")
        response = requests.get(f"{BASE_URL}/conversations")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 7: Delete the conversation
        print(f"\n7. Deleting conversation {conversation_id}...")
        response = requests.delete(f"{BASE_URL}/conversations/{conversation_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 8: Verify deletion
        print("\n8. Verifying deletion...")
        response = requests.get(f"{BASE_URL}/conversations")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n" + "=" * 50)
    print("🏁 Conversation API testing completed!")

if __name__ == "__main__":
    try:
        test_conversation_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
