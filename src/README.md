# Mergington High School Activities

A comprehensive web application for managing extracurricular activities at Mergington High School. Built with FastAPI and MongoDB, this system allows students to discover and join activities while providing teachers with administrative capabilities.

## Features

### For Students
- **Browse Activities**: View all available extracurricular activities with detailed information
- **Advanced Search & Filtering**: Search activities by name and filter by:
  - Day of the week (Monday through Saturday)
  - Time slots (start/end times)
  - Activity categories
- **Detailed Scheduling**: See specific meeting days, times, and duration for each activity
- **Participant Information**: View current enrollment and maximum capacity
- **Activity Registration**: Sign up for and unregister from activities (with teacher approval)
- **Responsive Design**: Optimized for desktop and mobile devices

### For Teachers/Administrators
- **Secure Authentication**: Login system with password hashing and session management
- **Student Management**: Approve student registrations and unregistrations for activities
- **Activity Management**: Administrative access to manage school activities
- **Participant Tracking**: Monitor student enrollment across all activities

### Activity Categories
- **Academic**: Chess Club, Math Club, Programming Class, Debate Team
- **Sports**: Soccer Team, Basketball Team, Morning Fitness
- **Arts**: Art Club, Drama Club
- **STEM**: Weekend Robotics Workshop, Science Olympiad

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: MongoDB with PyMongo
- **Authentication**: Argon2 password hashing
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Server**: Uvicorn ASGI server

## API Endpoints

### Activities
- `GET /activities/` - Retrieve all activities with optional filtering by day, start_time, end_time
- `GET /activities/days` - Get available activity days
- `POST /activities/{activity_name}/signup` - Sign up a student for an activity (requires teacher authentication)
- `POST /activities/{activity_name}/unregister` - Remove a student from an activity (requires teacher authentication)

### Authentication
- `POST /auth/login` - Teacher login with username and password
- `GET /auth/check-session` - Validate session by username

### Static Files
- `GET /` - Redirects to main application
- `GET /static/*` - Serves frontend assets

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   uvicorn app:app --reload
   ```

3. **Access the Application**:
   Open your browser to `http://localhost:8000`

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).
