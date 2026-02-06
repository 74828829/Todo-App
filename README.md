# TodoHub - Modern Flask Web Application

A sleek, modern web-based todo application built with Flask. Features a beautiful responsive design with gradient themes, real-time task management, and comprehensive task tracking.

## 🎨 Features

- **Modern Dashboard**: Overview with task statistics and progress tracking
- **Task Management**: Add, edit, delete, and complete tasks
- **Priority System**: Automatic priority calculation based on due dates (OVERDUE, HIGH, MEDIUM, LOW)
- **Search Functionality**: Find tasks by name or description
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Beautiful UI**: Gradient cards, smooth animations, and modern styling
- **Real-time Updates**: AJAX-powered actions without page reloads

## 📁 Project Structure

```
Todo App/
├── app.py                 # Main Flask application
├── main.py                # Original CLI version (kept for reference)
├── todos.json            # Task data storage
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── dashboard.html   # Dashboard/home page
│   ├── tasks.html       # Task list view
│   ├── add_task.html    # Add task form
│   ├── edit_task.html   # Edit task form
│   └── search.html      # Search results
└── static/
    ├── css/
    │   └── style.css    # Modern styling with gradients
    └── js/
        └── main.js      # JavaScript utilities
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Web App**
   - Open your browser and navigate to: `http://localhost:5000`
   - The app will start in development mode with debug enabled

## 📝 Usage

### Routes

- **`/`** - Dashboard with statistics and recent tasks
- **`/tasks`** - View all tasks with filters
- **`/add`** - Add a new task
- **`/edit/<id>`** - Edit an existing task
- **`/search`** - Search tasks by keyword
- **`/api/stats`** - JSON API for task statistics

### Date Format
All dates must be in **mm/dd/yyyy** format (e.g., 02/14/2026)

### Priority Levels
- **OVERDUE** - Task is past due date
- **HIGH** - Due within 3 days
- **MEDIUM** - Due within 7 days
- **LOW** - Due more than 7 days away

## 🎨 Design Features

### Modern Styling
- Gradient backgrounds and cards
- Smooth transitions and animations
- Bootstrap 5.3 framework
- Custom CSS with CSS variables

### Color Scheme
- Primary: Purple gradient (#667eea → #764ba2)
- Success: Green gradient (#43e97b → #38f9d7)
- Warning: Orange gradient (#fa709a → #fee140)
- Danger: Red gradient (#f5576c → #f093fb)

### UI Components
- Responsive navbar with gradient
- Stat cards with hover effects
- Task list with inline actions
- Modal search dialog
- Form controls with validation feedback

## 💾 Data Storage

Tasks are stored in `todos.json` with the following structure:

```json
[
  {
    "task": "Task name",
    "due": "mm/dd/yyyy",
    "description": "Task description",
    "completed": false,
    "completed_at": null
  }
]
```

## 🔄 Auto-cleanup

Tasks completed more than 2 days ago are automatically removed when:
- The app starts
- A task is marked as complete

## 🛠️ Development

### File Descriptions

**app.py** - Flask application with all routes and business logic:
- Task CRUD operations
- Priority calculation
- Task cleanup
- JSON API endpoints

**style.css** - Comprehensive styling featuring:
- CSS Grid and Flexbox layouts
- Gradient animations
- Responsive breakpoints
- Custom scrollbar styling

**base.html** - Navigation and layout template with:
- Bootstrap navbar
- Search modal
- Footer
- Navigation links

## 📱 Responsive Breakpoints

- **Desktop**: Full layout with all features
- **Tablet**: Optimized spacing and button sizes
- **Mobile**: Single-column layout with touch-friendly controls

## 🔐 Security Notes

Currently runs in development mode. For production:
1. Set `debug=False` in app.py
2. Use environment variables for configuration
3. Add proper authentication
4. Implement CSRF protection
5. Validate all user inputs server-side

## 🎯 Future Enhancements

- User authentication and accounts
- Task categories/tags
- Recurring tasks
- Task reminders/notifications
- Dark mode toggle
- Data export (CSV, PDF)
- Task sharing and collaboration

## 📄 License

This project is open source and available for personal use.

---

**Author**: Jonathan  
**Version**: 2.0 (Web Edition)  
**Status**: Active Development  
**Last Updated**: February 2026
