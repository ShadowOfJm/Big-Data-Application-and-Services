import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Generate sample data for course table
course_data = {
    'id': range(1, 101),  # 100 courses
    'course_name': [
        f"Course {i}" for i in range(1, 101)
    ],
    'category': [
        random.choice(['Programming', 'Data Science', 'Web Development', 'Machine Learning', 
                      'Mobile Development', 'Cloud Computing', 'DevOps', 'Database', 
                      'Cybersecurity', 'Artificial Intelligence'])
        for _ in range(100)
    ],
    'level': [
        random.choice(['Beginner', 'Intermediate', 'Advanced']) 
        for _ in range(100)
    ],
    'duration': [
        random.randint(10, 200)  # Duration in hours
        for _ in range(100)
    ],
    'price': [
        round(random.uniform(10.0, 200.0), 2)
        for _ in range(100)
    ],
    'instructor': [
        f"Instructor {random.randint(1, 50)}"
        for _ in range(100)
    ],
    'avg_rating': [
        round(random.uniform(3.0, 5.0), 1)
        for _ in range(100)
    ],
    'enrollment_count': [
        random.randint(10, 10000)
        for _ in range(100)
    ]
}

# Generate sample data for learning_record table
learning_record_data = {
    'id': range(1, 501),  # 500 learning records
    'user_id': [
        random.randint(1, 100)
        for _ in range(500)
    ],
    'course_id': [
        random.randint(1, 100)
        for _ in range(500)
    ],
    'watch_duration': [
        random.randint(0, 200)  # Watch duration in minutes
        for _ in range(500)
    ],
    'completion_rate': [
        round(random.uniform(0.0, 1.0), 2)
        for _ in range(500)
    ],
    'last_watch_time': [
        (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S')
        for _ in range(500)
    ],
    'quiz_score': [
        round(random.uniform(0.0, 100.0), 1)
        for _ in range(500)
    ],
    'study_duration': [
        random.randint(0, 500)  # Study duration in minutes
        for _ in range(500)
    ]
}

# Create DataFrames
course_df = pd.DataFrame(course_data)
learning_record_df = pd.DataFrame(learning_record_data)

# Save to CSV files
course_df.to_csv('course.csv', index=False)
learning_record_df.to_csv('learning_record.csv', index=False)

print("CSV files generated successfully!")
print(f"Course table: {len(course_df)} rows")
print(f"Learning record table: {len(learning_record_df)} rows")

# Display first few rows of each table
print("\nFirst 5 rows of course table:")
print(course_df.head())

print("\nFirst 5 rows of learning_record table:")
print(learning_record_df.head())