# TodoHub - Progressive Web App

A modern, fully-featured Progressive Web App (PWA) for task management. Install it directly from your browser, works offline, and syncs locally with no account needed. Tasks are stored securely on your device using IndexedDB.

## 🎨 Features

### Core Task Management
- **Modern Dashboard**: Overview with task statistics and progress tracking
- **Task Management**: Add, edit, delete, and complete tasks
- **Priority System**: Automatic priority calculation based on due dates (OVERDUE, HIGH, MEDIUM, LOW)
- **Search Functionality**: Find tasks by name or description
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Beautiful UI**: Gradient cards, smooth animations, and modern styling

### PWA Features (NEW!)
- **🏠 Home Screen Installation**: Add TodoHub to your home screen with a single tap
- **📱 Native App Experience**: Runs in standalone mode without browser UI
- **⚡ Instant Loading**: Service Worker caches assets for lightning-fast startup
- **🔌 Offline Support**: Full functionality without internet connection
- **💾 Local Storage**: All data stored locally using IndexedDB - no cloud needed
- **🆔 Device Identification**: Automatic unique device ID for personalization
- **🔄 Background Updates**: Auto-updates Service Worker in the background
- **📤 Import/Export**: Backup and restore your tasks anytime

## 📱 Installation

### Web Browser
1. **Open in Chrome, Firefox, Safari, or Edge**
   - Navigate to `http://localhost:5000` (or your server URL)

2. **Install the App** (Choose one method)
   - **Android**: Look for "Install" button in navbar, or use browser menu → "Install app"
   - **iPhone/iPad**: Add to Home Screen via browser share menu
   - **Desktop**: Use browser menu → "Install app"

3. **Enjoy!** The app will run in full screen like a native app

## 📁 Project Structure

```
Todo App/
├── app.py                      # Flask backend (optional server routes)
├── manifest.json              # PWA manifest - installation config
├── todos.json                 # Local backup of tasks (empty on install)
├── requirements.txt           # Python dependencies
├── templates/
│   ├── base.html             # Base template with PWA support
│   ├── dashboard.html        # Dashboard/home page
│   ├── tasks.html            # Task list view
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css         # PWA-optimized styling
│   └── js/
│       ├── main.js           # PWA install & task management
│       ├── db.js             # IndexedDB database manager
│       └── service-worker.js # Offline & caching logic
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Modern web browser (Chrome 47+, Firefox 44+, Safari 11.1+, Edge 79+)

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access in Browser**
   - Open: `http://localhost:5000`
   - For remote access: `http://<your-ip>:5000`

4. **Install as App**
   - Click the **Install App** button in the navbar
   - Or use your browser's install prompt
   - The app will appear on your home screen!

## 🔧 How It Works

### Service Worker
The Service Worker handles:
- **Caching strategy**: Network-first for API, Cache-first for static assets
- **Offline detection**: Seamless fallback when internet is unavailable
- **Background updates**: Periodically checks for new versions
- **Push notifications ready**: Framework for future notifications

### IndexedDB Storage
All your tasks are stored locally in IndexedDB:
- **Persistent**: Data survives app closes and device reboots
- **Secure**: Only accessible to TodoHub app, not visible to other sites
- **Efficient**: Optimized for mobile devices
- **Syncable**: Export/import JSON for backup or device switching

### Device ID
- **Automatic generation**: Created on first app open
- **Permanent**: Stays same across app sessions
- **Personalization**: Enables future features like cloud sync
- **Export tracking**: Included in exported task files

## 📝 Usage Guide

### Adding Tasks
1. Tap **"Add Task"** in navbar
2. Fill in task name and due date (mm/dd/yyyy)
3. Add optional description
4. Tap **Save**

### Managing Tasks
- **Complete**: Tap task checkbox
- **Edit**: Click task name to view details, use edit button
- **Delete**: Move to Trash (soft delete)
- **Restore**: Recover from Deleted tab
- **Save**: Pin important tasks to Saved section
- **Search**: Use Search button to find tasks

### Exporting Data
```javascript
// In browser console:
const data = await todoDb.exportTasks();
// Download as JSON
```

### Importing Data
```javascript
// In browser console:
const file = /* your JSON file */;
await todoDb.importTasks(file);
```

## 🎨 Design & Customization

### Modern Styling
- Gradient backgrounds and cards
- Smooth transitions and animations
- Bootstrap 5.3 framework
- Mobile-first responsive design
- Safe area support for notches

### Color Scheme
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Success**: Green
- **Warning**: Orange
- **Danger**: Red

## 💾 Data & Privacy

**All data is stored locally on your device**
- No cloud storage
- No tracking
- No ads
- No account creation
- Works completely offline

### Data Storage Location
- **Browser**: IndexedDB (local database)
- **Backup**: `todos.json` (JSON format)
- **Export**: Manual download as JSON file

### Device Protection
- **Auto-locking**: Recommend setting phone auto-lock
- **Data encryption**: Browser handles via HTTPS
- **Device ID**: Used for organization, not tracking

## 🔄 Auto-cleanup (Optional)

Tasks can be automatically cleaned up:
- Completed tasks: Kept indefinitely in local storage
- Deleted tasks: Stored for reference, never auto-removed
- Manual management: You control data retention

## 🛠️ Development Commands

**Start development server:**
```bash
python app.py
```

**Access locally:**
```
http://localhost:5000
```

**Test offline (DevTools):**
1. Open DevTools (F12)
2. Application tab → Service Workers
3. Check "Offline" checkbox
4. App continues to work!

## 🔐 Security & Performance

### Service Worker Security
- ✅ HTTPS enforced in production
- ✅ Same-origin policy enforced
- ✅ CSP headers recommended
- ✅ Regular cache cleanup

### Performance Optimizations
- ✅ Service Worker caching
- ✅ Lazy-loaded assets
- ✅ IndexedDB for fast local storage
- ✅ Minimal bundle size

## 📱 Browser Support

| Browser | Desktop | Mobile | Notes |
|---------|---------|--------|-------|
| Chrome | ✅ 47+ | ✅ All | Full PWA support |
| Firefox | ✅ 44+ | ✅ All | Full PWA support |
| Safari | ✅ 11.1+ | ✅ 13+ | Limited standalone mode |
| Edge | ✅ 79+ | ✅ All | Full PWA support |
| Samsung Internet | - | ✅ All | Full PWA support |

## 🎯 Features by Platform

### Android
- Home screen icon
- Full screen mode
- App shelf integration
- Push notification ready
- Share to functionality

### iPhone/iPad
- Home screen icon
- Standalone mode
- Status bar management
- Gesture support

### Desktop
- App window
- Taskbar icon
- Keyboard shortcuts
- Native feel

## 🚀 Deployment

### Local Network
```bash
python app.py
# Access from other devices on network:
# http://<your-ip>:5000
```

### Production Deployment
1. Set `debug=False` in app.py
2. Configure for HTTPS (required for PWA)
3. Add security headers
4. Deploy to hosting service

### HTTPS Requirement
PWA features require HTTPS in production:
- Service Workers
- IndexedDB with persistent storage
- Installation prompts

## 🐛 Troubleshooting

### App Not Installing?
- Check browser is PWA-capable (see Browser Support table)
- Ensure HTTPS in production
- Clear browser cache and service worker
- Try incognito/private mode

### Data Not Persisting?
- Check IndexedDB in DevTools
- Clear site storage and reinstall
- Check browser storage permissions
- Enable persistent storage

### Offline Not Working?
- Verify Service Worker is registered (DevTools → Application)
- Check service worker scope
- Try hard refresh (Ctrl+Shift+R)
- Clear cache and reinstall

### Tasks Not Syncing?
- All data is local-only by design
- Export/import for multi-device use
- Manual backup recommended

## 📄 API Endpoints (Optional - for server use)

- `GET /` - Dashboard
- `GET /add` - Add task page
- `POST /api/task` - Create task (optional)
- `GET /api/task/<id>` - Get task (optional)

*Note: Modern TodoHub uses IndexedDB instead of server storage*

## 🎯 Future Enhancements

Potential features for future versions:
- Cloud sync (optional)
- Task sharing
- Recurring tasks
- Reminder notifications
- Dark mode
- Multiple task lists
- Collaboration

## 💡 Tips & Tricks

**Better Performance:**
- Remove old browsers' caches
- Keep app updated
- Limit task volume (10,000+ tasks OK)

**Data Safety:**
- Export tasks regularly
- Keep backup JSON copy
- Use unique device IDs same across devices

**Battery Optimization:**
- App uses minimal power (cached assets)
- No constant network polling
- No background drain

## 📄 License

Open source - Free for personal and commercial use

---

**TodoHub** - *Tasks Made Simple*  
**Version**: 3.0 (Progressive Web App)  
**Last Updated**: February 2026  
**Platform**: Cross-platform web, installable on any OS  
**Status**: Production Ready

*Built with ❤️ for productive teams and individuals*

