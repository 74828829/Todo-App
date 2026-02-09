/**
 * IndexedDB Manager for TodoHub
 * Handles all local persistent storage with offline support
 */

const DB_NAME = 'TodoHub';
const DB_VERSION = 1;
const STORE_NAME = 'tasks';
const SETTINGS_STORE = 'settings';

class TodoDatabase {
  constructor() {
    this.db = null;
    this.initialized = false;
  }

  /**
   * Initialize the database
   */
  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onerror = () => {
        console.error('Failed to open IndexedDB');
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        this.initialized = true;
        console.log('IndexedDB initialized successfully');
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Create tasks object store
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          const taskStore = db.createObjectStore(STORE_NAME, { autoIncrement: true });
          taskStore.createIndex('completed', 'completed', { unique: false });
          taskStore.createIndex('deleted', 'deleted', { unique: false });
          taskStore.createIndex('saved', 'saved', { unique: false });
          taskStore.createIndex('due', 'due', { unique: false });
          console.log('Tasks object store created');
        }

        // Create settings object store
        if (!db.objectStoreNames.contains(SETTINGS_STORE)) {
          db.createObjectStore(SETTINGS_STORE, { keyPath: 'key' });
          console.log('Settings object store created');
        }
      };
    });
  }

  /**
   * Get or create device ID (permanent identifier for this device)
   */
  async getDeviceId() {
    try {
      const setting = await this.getSetting('deviceId');
      if (setting) {
        return setting.value;
      }

      // Generate new device ID
      const deviceId = this._generateDeviceId();
      await this.saveSetting('deviceId', deviceId);
      return deviceId;
    } catch (error) {
      console.error('Error getting device ID:', error);
      return null;
    }
  }

  /**
   * Generate a unique device ID
   */
  _generateDeviceId() {
    // Use timestamp + random string for uniqueness
    const timestamp = Date.now().toString(36);
    const randomStr = Math.random().toString(36).substr(2, 9);
    return `device_${timestamp}_${randomStr}`;
  }

  /**
   * Save a setting to settings store
   */
  async saveSetting(key, value) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([SETTINGS_STORE], 'readwrite');
      const store = transaction.objectStore(SETTINGS_STORE);
      const request = store.put({ key, value, timestamp: Date.now() });

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
    });
  }

  /**
   * Get a setting from settings store
   */
  async getSetting(key) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([SETTINGS_STORE], 'readonly');
      const store = transaction.objectStore(SETTINGS_STORE);
      const request = store.get(key);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
    });
  }

  /**
   * Add a new task
   */
  async addTask(taskData) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);

      const task = {
        ...taskData,
        id: Date.now(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        completed: false,
        completed_at: null,
        deleted: false,
        deleted_at: null,
        saved: false,
        saved_at: null
      };

      const request = store.add(task);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        console.log('Task added:', task);
        resolve(task);
      };
    });
  }

  /**
   * Get all tasks
   */
  async getAllTasks() {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.getAll();

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        const tasks = request.result.sort((a, b) => b.id - a.id);
        resolve(tasks);
      };
    });
  }

  /**
   * Get task by ID
   */
  async getTask(id) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([STORE_NAME], 'readonly');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.get(id);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
    });
  }

  /**
   * Update a task
   */
  async updateTask(id, updates) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const getRequest = store.get(id);

      getRequest.onsuccess = () => {
        const task = getRequest.result;
        if (!task) {
          reject(new Error('Task not found'));
          return;
        }

        const updatedTask = {
          ...task,
          ...updates,
          id: task.id,
          created_at: task.created_at,
          updated_at: new Date().toISOString()
        };

        const updateRequest = store.put(updatedTask);
        updateRequest.onerror = () => reject(updateRequest.error);
        updateRequest.onsuccess = () => {
          console.log('Task updated:', updatedTask);
          resolve(updatedTask);
        };
      };

      getRequest.onerror = () => reject(getRequest.error);
    });
  }

  /**
   * Delete a task (soft delete - marks as deleted)
   */
  async deleteTask(id) {
    return this.updateTask(id, {
      deleted: true,
      deleted_at: new Date().toISOString()
    });
  }

  /**
   * Permanently delete a task
   */
  async permanentlyDeleteTask(id) {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.delete(id);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        console.log('Task permanently deleted:', id);
        resolve(true);
      };
    });
  }

  /**
   * Toggle task completion status
   */
  async toggleTaskCompletion(id) {
    const task = await this.getTask(id);
    if (!task) throw new Error('Task not found');

    return this.updateTask(id, {
      completed: !task.completed,
      completed_at: !task.completed ? new Date().toISOString() : null
    });
  }

  /**
   * Toggle task saved status
   */
  async toggleTaskSaved(id) {
    const task = await this.getTask(id);
    if (!task) throw new Error('Task not found');

    return this.updateTask(id, {
      saved: !task.saved,
      saved_at: !task.saved ? new Date().toISOString() : null
    });
  }

  /**
   * Get tasks by status
   */
  async getTasksByStatus(completed, deleted, saved) {
    const allTasks = await this.getAllTasks();
    return allTasks.filter(task =>
      task.completed === completed &&
      task.deleted === deleted &&
      task.saved === saved
    );
  }

  /**
   * Search tasks
   */
  async searchTasks(query) {
    const allTasks = await this.getAllTasks();
    const lowerQuery = query.toLowerCase();
    return allTasks.filter(task =>
      (task.task && task.task.toLowerCase().includes(lowerQuery)) ||
      (task.description && task.description.toLowerCase().includes(lowerQuery))
    );
  }

  /**
   * Clear all tasks (destructive)
   */
  async clearAllTasks() {
    return new Promise((resolve, reject) => {
      if (!this.db) {
        reject(new Error('Database not initialized'));
        return;
      }

      const transaction = this.db.transaction([STORE_NAME], 'readwrite');
      const store = transaction.objectStore(STORE_NAME);
      const request = store.clear();

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        console.log('All tasks cleared');
        resolve(true);
      };
    });
  }

  /**
   * Export all tasks as JSON
   */
  async exportTasks() {
    const tasks = await this.getAllTasks();
    return {
      version: '1.0',
      exported_at: new Date().toISOString(),
      device_id: await this.getDeviceId(),
      tasks: tasks
    };
  }

  /**
   * Import tasks from JSON (merge with existing)
   */
  async importTasks(taskData) {
    if (!Array.isArray(taskData)) {
      throw new Error('Invalid task data format');
    }

    for (const task of taskData) {
      // Check if task with same id exists
      const existing = await this.getTask(task.id);
      if (!existing) {
        await this.addTask(task);
      } else {
        await this.updateTask(task.id, task);
      }
    }
  }

  /**
   * Get statistics
   */
  async getStats() {
    const tasks = await this.getAllTasks();
    const pending = tasks.filter(t => !t.completed && !t.deleted && !t.saved).length;
    const completed = tasks.filter(t => t.completed && !t.deleted).length;
    const saved = tasks.filter(t => t.saved && !t.deleted).length;
    const deleted = tasks.filter(t => t.deleted).length;
    const total = tasks.filter(t => !t.deleted).length;

    return {
      total,
      pending,
      completed,
      saved,
      deleted,
      tasks_per_status: {
        pending,
        completed,
        saved,
        deleted
      }
    };
  }
}

// Create global database instance
const todoDb = new TodoDatabase();
