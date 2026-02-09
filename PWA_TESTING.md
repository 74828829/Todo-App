# TodoHub PWA - Testing & Verification Guide

## Quick Verification (5 minutes)

### 1. Start the Server
```bash
cd "c:\Users\jonat\Todo App"
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### 2. Open in Browser
- Navigate to: `http://localhost:5000`
- Should see: TodoHub home page with empty task list

### 3. Check Install Button
- Look at top navbar (right side)
- Should see: Green **"Download Install App"** button
- Button should NOT appear if app already installed

### 4. Click Install Button
- Button opens beautiful modal dialog
- Modal shows: Icon, description, action buttons
- Click: "Install TodoHub"
- Browser should prompt for installation

### 5. Verify Installation
- Complete the browser installation
- App closes and reinstalls
- App launches in full-screen standalone mode
- Install button should now be hidden

## Detailed Testing Checklist

### ✅ PWA Files Verification

**Check all files exist:**
```powershell
# In PowerShell, from Todo App directory:
ls manifest.json          # Should exist
ls static/js/db.js        # Should exist
ls static/js/service-worker.js  # Should exist
ls todos.json             # Should exist (empty)
```

**Expected results:**
```
manifest.json (2 KB)
todos.json (5 bytes)
static/js/db.js (25 KB)
static/js/service-worker.js (8 KB)
```

### ✅ Manifest Verification

Open in browser: `http://localhost:5000/manifest.json`

Expected response:
```json
{
  "name": "TodoHub - Tasks Made Simple",
  "short_name": "TodoHub",
  "display": "standalone",
  "theme_color": "#4a5568",
  "icons": [...]
}
```

### ✅ Service Worker Verification

**In Browser DevTools:**
1. Press F12 to open DevTools
2. Go to **Application** tab
3. Click **Service Workers** in left menu
4. Should show: Status ✓ with URL `/service-worker.js`
5. Checkbox next to it should be **checked**

**Test offline:**
1. Check the **Offline** checkbox in Service Workers
2. Tasks page should still load
3. Uncheck **Offline** to go back online

### ✅ IndexedDB Verification

**In Browser DevTools:**
1. Open **Application** tab
2. Expand **Storage → IndexedDB**
3. Click **TodoHub** database
4. Should see two stores:
   - `tasks` (empty initially)
   - `settings` (contains device ID)

**Check Device ID:**
1. Right-click on `settings` store
2. Select "Clear" or view entries
3. Should have one entry with key: `"deviceId"`

**In Console:**
```javascript
// Check database initialization
await todoDb.init();
// Expected: "IndexedDB initialized successfully"

// Get device ID
const id = await todoDb.getDeviceId();
console.log(id);
// Expected: "device_[timestamp]_[random]"

// Get statistics
const stats = await todoDb.getStats();
console.log(stats);
// Expected: { total: 0, pending: 0, completed: 0, ... }
```

### ✅ Install Button Verification

**Visual Check:**
1. Page should load completely
2. Top navbar: Look for green Download icon
3. Text should say: "Install App"
4. Button should be in the right side of navbar

**Click Behavior:**
1. Click the "Install App" button
2. Modal dialog should appear
3. Modal has:
   - Large download icon (blue/purple)
   - Title: "Get TodoHub on Your Home Screen"
   - Description text
   - "Install TodoHub" button (primary)
   - "Not Now" button (secondary)

**Install Success:**
1. Click "Install TodoHub" button
2. Browser installation prompt appears
3. Confirm installation
4. App launches in standalone mode
5. Install button disappears

### ✅ Task Management Tests

**Add Task:**
1. Click "Add Task" button in navbar
2. Fill in: Task name, Due date (mm/dd/yyyy), Description
3. Click Save
4. Verify task appears in IndexedDB:
   ```javascript
   const tasks = await todoDb.getAllTasks();
   console.log(tasks[0]);
   ```

**Complete Task:**
1. Click checkbox next to task
2. Task should show as completed in UI
3. Verify in IndexedDB:
   ```javascript
   const task = await todoDb.getTask(taskId);
   console.log(task.completed); // Should be true
   ```

**Edit Task:**
1. Click on task to view details
2. Click Edit button
3. Modify and save
4. Verify changes in IndexedDB

**Delete Task:**
1. Click delete button on task
2. Task should move to Deleted section
3. Verify in IndexedDB:
   ```javascript
   const task = await todoDb.getTask(taskId);
   console.log(task.deleted); // Should be true
   ```

**Save/Star Task:**
1. Click bookmark/star icon
2. Task should appear in Saved section
3. Verify in IndexedDB:
   ```javascript
   const task = await todoDb.getTask(taskId);
   console.log(task.saved); // Should be true
   ```

### ✅ Offline Functionality Test

**Prepare:**
1. Add 3-4 test tasks
2. Open DevTools → Application → Service Workers
3. Check the **Offline** checkbox

**Verify Offline Works:**

| Action | Expected | Verify |
|--------|----------|--------|
| View tasks | Still visible | ✓ Pass |
| Add task | Creates task locally | Check IndexedDB |
| Edit task | Updates locally | Check modified_at |
| Complete task | Completes locally | Check completed: true |
| Delete task | Deletes locally | Check deleted: true |
| Search | Finds in cache | Filter works |
| Navigate pages | All pages load | No connection errors |

### ✅ Data Persistence Test

**Test Browser Close:**
1. Add 5 test tasks
2. Close the browser completely
3. Reopen: `http://localhost:5000`
4. Tasks should still be there
5. Verify in IndexedDB - data intact

**Test Device Restart (Desktop):**
1. Add tasks
2. Restart computer
3. Reopen browser to `http://localhost:5000`
4. Tasks persist (IndexedDB is persistent)

### ✅ Export/Import Tests

**Export Data:**
```javascript
// In console:
const backup = await todoDb.exportTasks();
console.log(backup);
// Should show:
// {
//   version: "1.0",
//   exported_at: "2026-02-09T...",
//   device_id: "device_...",
//   tasks: [...]
// }

// Save as file
const json = JSON.stringify(backup, null, 2);
const blob = new Blob([json], {type: 'application/json'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'tasks-backup.json';
a.click();
```

**Clear Database (Testing):**
```javascript
// WARNING: Destructive!
await todoDb.clearAllTasks();
// All tasks deleted
```

**Import Data:**
```javascript
// After clearing, import backup:
await todoDb.importTasks(backup.tasks);
// Tasks restored
```

### ✅ Service Worker Caching Test

**In DevTools:**
1. Go to **Application → Caches**
2. Expand **todohub-v1** cache
3. Should see cached files:
   - /
   - /static/css/style.css
   - /static/js/main.js
   - /static/js/db.js
   - Bootstrap CSS/JS files
   - Bootstrap Icons

**Monitor Network:**
1. Open **Network** tab
2. Go offline (DevTools → Service Workers → Offline)
3. Refresh page (Ctrl+R)
4. All assets load from cache (Size column shows "from ServiceWorker")
5. No network errors

### ✅ Priority Calculation Test

```javascript
// In console, test priority logic:

// Task due today - should be HIGH
const today = new Date().toISOString().split('T')[0];
console.log(calculatePriority(today)); // Should be HIGH

// Task due in 2 days - should be HIGH
const in2Days = new Date(Date.now() + 2*86400000).toISOString().split('T')[0];
console.log(calculatePriority(in2Days)); // Should be HIGH

// Task due in 5 days - should be MEDIUM
const in5Days = new Date(Date.now() + 5*86400000).toISOString().split('T')[0];
console.log(calculatePriority(in5Days)); // Should be MEDIUM

// Task overdue - should be OVERDUE
const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
console.log(calculatePriority(yesterday)); // Should be OVERDUE
```

### ✅ Responsive Design Test

**Mobile Viewport:**
1. DevTools → Responsive Design Mode (Ctrl+Shift+M)
2. Set to iPhone 12 or similar
3. Verify:
   - Navbar collapses ✓
   - Install button hides text, shows icon only ✓
   - All buttons are touch-friendly ✓
   - Form inputs are large enough ✓

**Tablet Viewport:**
1. Set to iPad or similar
2. Verify layout adjusts but uses more space ✓
3. Install button visible with text ✓

**Desktop Viewport:**
1. Set to Desktop (1920x1080)
2. Full layout visible ✓
3. All features accessible ✓

### ✅ Browser Compatibility Test

**Test in Different Browsers:**

| Browser | Should Work | Priority |
|---------|------------|----------|
| Chrome | ✓ Full PWA | Primary |
| Firefox | ✓ Full PWA | Primary |
| Edge | ✓ Full PWA | High |
| Safari | ✓ Partial | Medium |
| Opera | ✓ Good | Low |

**Chrome Test:**
- Install button appears ✓
- Installation prompt works ✓
- Service worker registers ✓
- Offline mode works ✓

**Firefox Test:**
- Install button appears ✓
- Installation prompt works ✓
- Service worker registers ✓
- IndexedDB works ✓

**Safari Test (Mac/iOS):**
- IndexedDB works ✓
- Service worker limited ✓
- Offline partial ✓
- Add to Home Screen option available ✓

## Performance Testing

### Load Time Benchmark

**First Visit (Cold Load):**
- Measure: Time from URL entry to fully loaded
- Expected: 2-3 seconds
- Use DevTools → Network tab

**Subsequent Visit (Warm Load):**
- Expected: <500ms (cached)
- Monitor Network tab sizes

**Offline Load:**
- Expected: <200ms
- All from cache

### Storage Impact

**Check Storage Usage:**
```javascript
// In console:
if (navigator.storage && navigator.storage.estimate) {
  const estimate = await navigator.storage.estimate();
  console.log('Storage usage:');
  console.log('Usage:', estimate.usage, 'bytes');
  console.log('Quota:', estimate.quota, 'bytes');
  console.log('Percentage:', 
    ((estimate.usage / estimate.quota) * 100).toFixed(2) + '%');
}
```

## Security Testing

### CORS & Origin Testing
```javascript
// Different origin requests should fail
fetch('https://example.com/api/data')
  .catch(e => console.log('Blocked:', e)); // Should be blocked
```

### Storage Isolation Testing
- Open in Private/Incognito window
- Add tasks
- Close private window
- Reopen private window
- Previous tasks gone (storage isolated) ✓

## Troubleshooting During Tests

### Issue: Install Button Not Appearing
1. Check if browser supports PWAs
2. Verify manifest.json is accessible
3. Check console for CORS errors
4. Try incognito mode
5. Clear browser cache

### Issue: Service Worker Not Registering
1. Check `navigator.serviceWorker` in console
2. Verify HTTPS in production
3. Check console for registration errors
4. Clear browser cache
5. Hard refresh (Ctrl+Shift+R)

### Issue: IndexedDB Not Working
1. Check if browser allows IndexedDB
2. Verify storage permissions
3. Check IndexedDB quota
4. Try clearing site storage
5. Check browser privacy settings

### Issue: Tasks Not Persisting
1. Check IndexedDB is available
2. Verify storage quota not exceeded
3. Check no JavaScript errors in console
4. Test `todoDb.addTask()` in console
5. Verify `updated_at` timestamp

## Quick Test Commands (Console)

```javascript
// Quick verification script
async function quickTest() {
  console.log('=== TodoHub PWA Quick Test ===');
  
  // 1. Check service worker
  const sw = await navigator.serviceWorker.getRegistrations();
  console.log('Service Workers:', sw.length > 0 ? '✓' : '✗');
  
  // 2. Check database
  try {
    await todoDb.init();
    console.log('Database:', '✓');
  } catch(e) {
    console.log('Database:', '✗', e.message);
  }
  
  // 3. Check device ID
  const deviceId = await todoDb.getDeviceId();
  console.log('Device ID:', deviceId ? '✓' : '✗');
  
  // 4. Check stats
  const stats = await todoDb.getStats();
  console.log('Stats:', stats);
  
  // 5. Test add task
  const testTask = await todoDb.addTask({
    task: 'Test Task',
    due: '02/14/2026',
    description: 'Testing'
  });
  console.log('Add Task:', testTask ? '✓' : '✗', testTask);
  
  // 6. Test get tasks
  const allTasks = await todoDb.getAllTasks();
  console.log('Total Tasks:', allTasks.length);
  
  // 7. Check manifest
  const manifest = await fetch('/manifest.json').then(r => r.json());
  console.log('Manifest:', manifest.name);
  
  console.log('=== Test Complete ===');
}

// Run it:
quickTest();
```

## Success Criteria

Your PWA is **working correctly** if all these pass:

- ✅ App loads at http://localhost:5000
- ✅ Install button appears in navbar
- ✅ Manifest.json is accessible
- ✅ Service Worker registers (DevTools → Service Workers)
- ✅ IndexedDB stores created (DevTools → IndexedDB)
- ✅ Device ID generated (Settings store)
- ✅ Tasks persist after browser close
- ✅ Offline mode works (DevTools → Offline)
- ✅ Priority calculation correct
- ✅ Install button launches installation
- ✅ App runs in standalone mode
- ✅ No console errors

## Next Steps

1. ✅ Run all tests above
2. ✅ Verify all checkmarks
3. ✅ Fix any failing tests
4. ✅ Test on real mobile device
5. ✅ Try on different browsers
6. ✅ Deploy to production (HTTPS)
7. ✅ Install on home screen
8. ✅ Test offline functionality
9. ✅ Share with users

---

**Testing Date**: February 9, 2026  
**Version**: 3.0 (PWA)  
**Tested Browser**: Chrome, Firefox (results may vary)  
**Status**: Ready for verification

Happy testing! 🧪
