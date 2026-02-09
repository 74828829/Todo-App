# TodoHub PWA - Quick Start Guide

## What's New? 🎉

Your Todo App has been transformed into a **Progressive Web App (PWA)**! Here's what that means:

### ✨ New Features
- **📱 Home Screen Installation**: Add the app directly to your phone/tablet home screen
- **⚡ Works Offline**: Full functionality even without internet
- **💾 Local Storage**: All tasks stored safely on your device using IndexedDB
- **🚀 Instant Loading**: Service Worker caches everything for lightning-fast startup
- **🔌 No Sign-In**: Just start using it - no account creation needed
- **📤 Import/Export**: Backup and restore your tasks anytime

## Getting Started

### 1. Start the App
```bash
python app.py
```
Then open `http://localhost:5000` in your browser.

### 2. Install as an App

#### Android/Chrome:
- Look for the **"Install App"** button in the navbar
- Or tap the **⋮** menu → "Install app"
- App will appear on your home screen

#### iPhone/iPad/Safari:
- Tap the **Share** button
- Scroll down and tap **"Add to Home Screen"**
- Name it "TodoHub"
- Tap **Add**

#### Desktop (Chrome/Edge):
- Click the **Install** icon in the address bar
- Or use the **"Install App"** button in the navbar
- Window will open in standalone mode

### 3. Start Using!

The app will now:
- Run full-screen without browser UI
- Open instantly from your home screen
- Work completely offline
- Store all data locally on your device

## Understanding the PWA Structure

### Key Files

**manifest.json**
- Tells your device how to install the app
- Specifies app name, icons, colors
- Enables "Add to Home Screen"

**service-worker.js**
- Makes the app work offline
- Caches assets for fast loading
- Handles background updates

**db.js**
- Manages local data storage (IndexedDB)
- Handles all task CRUD operations
- Creates unique Device ID

**main.js (updated)**
- Manages install prompts
- Coordinates with service worker
- Handles task operations

## Local Storage System

### IndexedDB Database
All your tasks live in your browser's local database:
- **Persistent**: Survives app close and device restart
- **Private**: Only TodoHub can access it
- **Fast**: Optimized for mobile devices
- **Secure**: No cloud, no tracking, no ads

### Data Structure
```javascript
Task {
  id: number,              // Unique ID
  task: string,           // Task name
  due: string,            // Due date (mm/dd/yyyy)
  description: string,    // Optional details
  completed: boolean,     // Completion status
  completed_at: date,     // When completed
  deleted: boolean,       // Soft delete flag
  deleted_at: date,       // When deleted
  saved: boolean,         // Saved/starred status
  created_at: date,       // Created timestamp
  updated_at: date        // Last modified timestamp
}
```

### Device ID
- **Automatically generated** on first app open
- **Unique identifier** for your device
- **Persistent** across sessions
- **Included in exports** for backup tracking

## Data Management

### Export Your Data
```javascript
// In browser DevTools console:
const backup = await todoDb.exportTasks();
console.log(backup);
// Save as JSON for backup
```

### Import From Backup
```javascript
// Upload previously exported JSON file:
const file = /* your JSON file */;
await todoDb.importTasks(file);
```

### View All Tasks
```javascript
// In browser console:
const allTasks = await todoDb.getAllTasks();
console.log(allTasks);
```

### Get Statistics
```javascript
// In browser console:
const stats = await todoDb.getStats();
console.log(stats);
```

## Offline Functionality

### What Works Offline?
✅ View all tasks
✅ Add new tasks
✅ Edit existing tasks
✅ Mark tasks complete
✅ Delete tasks
✅ Search tasks
✅ All UI features

### What Needs Internet?
❌ Flask API routes (optional, treated as read-only if offline)
✅ Everything else is local-first!

## Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Best PWA support |
| Firefox | ✅ Full | Full PWA support |
| Safari | ✅ Partial | iOS 13+ recommended |
| Edge | ✅ Full | Full PWA support |
| Opera | ✅ Full | Full support |

## Troubleshooting

### App Won't Install?
1. Use a modern browser (Chrome 47+, Firefox 44+, etc.)
2. For HTTPS requirement: Ensure `https://` in production
3. Clear browser cache: Ctrl+Shift+Delete → Clear all
4. Try in incognito/private mode
5. Check DevTools → Application → Manifest

### Tasks Not Saving?
1. Check browser's IndexedDB quota
2. Open DevTools → Application → IndexedDB → TodoHub
3. Verify storage permission in browser settings
4. Try clearing site storage and reinstalling

### Worker Won't Register?
1. Check DevTools → Application → Service Workers
2. If offline, click "Offline" to toggle
3. Check browser console for errors
4. Hard refresh: Ctrl+Shift+R

### Data Lost Between Devices?
- **This is by design**: Each device has its own local storage
- **Solution**: Export from one device, import on another
- Use the export/import features to transfer data

## Security & Privacy

### Your Data is Your Own
- ✅ All data stays on your device
- ✅ No cloud storage
- ✅ No cloud syncing
- ✅ No tracking
- ✅ No ads
- ✅ No telemetry

### Storage Protection
1. Your browser handles encryption
2. Require phone lock screen for security
3. Keep browser updated
4. Use device passcode

## Tips & Tricks

### Performance
- Tasks load instantly from cache
- App starts in <1 second
- Minimal battery usage
- No background drain

### Backups
- Export monthly for safety
- Store backups in cloud (Google Drive, Dropbox, etc.)
- Keep multiple versions
- ImportJSON anytime to restore

### Multi-Device Usage
1. Export from Device A
2. Share export file
3. Import on Device B
4. Each device gets it own copy

### Home Screen Organization
- Create folder named "Productivity"
- Move TodoHub icon into it
- Pin folder to home screen
- Quick access anytime!

## Advanced Usage

### Check Service Worker Status
```javascript
navigator.serviceWorker.getRegistrations()
  .then(regs => {
    regs.forEach(reg => console.log(reg));
  });
```

### Force Update Check
```javascript
// Check for service worker updates:
navigator.serviceWorker.ready
  .then(reg => reg.update())
  .then(() => console.log('Updated'));
```

### View IndexedDB Contents
```javascript
// List all tasks:
const tasks = await todoDb.getAllTasks();
tasks.forEach(t => console.log(`${t.task} - Due: ${t.due}`));
```

### Get Device ID
```javascript
const deviceId = await todoDb.getDeviceId();
console.log('Your Device ID:', deviceId);
```

## Deployment

### Local Network
```bash
python app.py  # Default: localhost:5000
# Access from other devices:
http://<your-ip>:5000
```

### Production (HTTPS Required)
1. Deploy to HTTPS server
2. Update `manifest.json` URLs if needed
3. Service Workers require HTTPS
4. PWA installation works automatically

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## What Changed?

### Cleared Data
- ✅ `todos.json` is now empty
- ✅ Fresh start for all users
- ✅ New data goes to IndexedDB

### Added Files
- ✅ `manifest.json` - PWA configuration
- ✅ `service-worker.js` - Offline support
- ✅ `db.js` - IndexedDB management
- ✅ Updated `main.js` - Install prompts

### Updated Files
- ✅ `base.html` - PWA meta tags & install button
- ✅ `style.css` - PWA styling
- ✅ `app.py` - Added manifest & service-worker routes
- ✅ `README.md` - New PWA documentation

## Support & Help

If something's not working:

1. **Check browser console** (F12 → Console)
2. **Clear cache & service workers** (DevTools → Application)
3. **Hard refresh** (Ctrl+Shift+R)
4. **Check IndexedDB** (DevTools → Application → IndexedDB)
5. **Reinstall the app** from home screen

## Next Steps

- 🎯 Add the app to your home screen now!
- 📝 Start creating tasks locally
- 💾 Export your first backup
- 🎉 Enjoy offline task management!

---

**TodoHub PWA** is now ready to use! 🚀

All your tasks. On your device. Always available.
