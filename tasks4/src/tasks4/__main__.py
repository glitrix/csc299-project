"""
OpenAI Task Summarizer

This module uses the OpenAI Chat Completions API to summarize task descriptions
into short, concise phrases.
"""

import os
import sys
from openai import OpenAI


def get_openai_client():
    """Initialize and return OpenAI client."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key as an environment variable:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    return OpenAI(api_key=api_key)


def summarize_task(client, task_description):
    """
    Summarize a task description using OpenAI Chat Completions API.
    
    Args:
        client: OpenAI client instance
        task_description (str): The paragraph-length task description
        
    Returns:
        str: A short phrase summary of the task
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes task descriptions into short, concise phrases (3-8 words). Focus on the main action and objective."
                },
                {
                    "role": "user",
                    "content": f"Please summarize this task description into a short phrase: {task_description}"
                }
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error summarizing task: {str(e)}"


def get_sample_tasks():
    """Return a list of sample paragraph-length task descriptions."""
    return [
        """I need to develop a comprehensive web application for managing student course registrations at a university. The application should allow students to browse available courses, view course details including prerequisites and schedules, add courses to their cart, and complete the registration process. The system needs to handle enrollment limits, prevent conflicts in scheduling, verify that students meet prerequisites, and generate confirmation emails upon successful registration. Additionally, the application should provide an administrative interface for faculty to manage course information, view enrollment statistics, and export student rosters. The entire system should be built using modern web technologies with proper authentication, data validation, and responsive design for both desktop and mobile users.""",
        
        """Create a machine learning pipeline that can automatically categorize and prioritize customer support tickets based on their content, urgency level, and customer tier. The system should process incoming emails and chat messages, extract key information using natural language processing techniques, and assign appropriate categories such as technical issues, billing inquiries, feature requests, or complaints. The pipeline needs to integrate with our existing CRM system, maintain a feedback loop for continuous improvement of classification accuracy, and provide real-time dashboards for support managers to monitor ticket volumes and response times. The solution should also include automated routing of high-priority tickets to senior support staff and generate daily reports summarizing ticket trends and resolution statistics."""
    ]


def main():
    """Main function to process and summarize task descriptions."""
    print("OpenAI Task Summarizer")
    print("=" * 50)
    
    # Initialize OpenAI client
    client = get_openai_client()
    
    # Get sample task descriptions
    task_descriptions = get_sample_tasks()
    
    # Process each task description
    for i, task_description in enumerate(task_descriptions, 1):
        print(f"\nTask {i}:")
        print("-" * 20)
        print(f"Original description ({len(task_description)} characters):")
        print(f"{task_description[:100]}..." if len(task_description) > 100 else task_description)
        print()
        
        # Get summary from OpenAI
        print("Generating summary...")
        summary = summarize_task(client, task_description)
        
        print(f"Summary: {summary}")
        print()
    
    print("All task summaries completed!")


if __name__ == "__main__":
    main()