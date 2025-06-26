/**
 * StateManager.ts
 * 
 * Handles state preservation and restoration across UI switches.
 * Supports local storage, WebSocket sync, and IndexedDB persistence.
 */

import { EventEmitter } from 'events';

// Types
export type UITarget = 'chat' | 'annotator' | 'terminal';

export interface UIState {
  timestamp: number;
  ui: UITarget;
  sessionId: string;
  context: UIContext;
  auth: AuthState;
}

export interface UIContext {
  url: string;
  scrollPosition: number;
  activeElement?: string;
  formData: Record<string, any>;
  customData: Record<string, any>;
  files?: FileContext[];
  history?: HistoryItem[];
}

export interface AuthState {
  token: string;
  expiresAt: number;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

export interface FileContext {
  id: string;
  name: string;
  path: string;
  type: string;
  size: number;
  lastModified: number;
}

export interface HistoryItem {
  timestamp: number;
  action: string;
  details: Record<string, any>;
}

export interface StateStorageConfig {
  localStorageKey: string;
  indexedDBName: string;
  indexedDBVersion: number;
  stateExpiration: number; // milliseconds
  compressionEnabled: boolean;
}

// Default configuration
const DEFAULT_CONFIG: StateStorageConfig = {
  localStorageKey: 'granger_ui_state',
  indexedDBName: 'GrangerUIState',
  indexedDBVersion: 1,
  stateExpiration: 5 * 60 * 1000, // 5 minutes
  compressionEnabled: true
};

/**
 * Local storage wrapper for immediate state access
 */
class LocalStateStorage {
  constructor(private key: string) {}

  save(state: UIState): void {
    try {
      const compressed = this.compress(state);
      localStorage.setItem(this.key, compressed);
    } catch (error) {
      console.error('Failed to save state to localStorage:', error);
    }
  }

  load(): UIState | null {
    try {
      const compressed = localStorage.getItem(this.key);
      if (!compressed) return null;
      
      const state = this.decompress(compressed);
      
      // Check if state has expired
      if (Date.now() - state.timestamp > DEFAULT_CONFIG.stateExpiration) {
        this.clear();
        return null;
      }
      
      return state;
    } catch (error) {
      console.error('Failed to load state from localStorage:', error);
      return null;
    }
  }

  clear(): void {
    localStorage.removeItem(this.key);
  }

  private compress(state: UIState): string {
    if (DEFAULT_CONFIG.compressionEnabled) {
      return btoa(JSON.stringify(state));
    }
    return JSON.stringify(state);
  }

  private decompress(data: string): UIState {
    if (DEFAULT_CONFIG.compressionEnabled) {
      return JSON.parse(atob(data));
    }
    return JSON.parse(data);
  }
}

/**
 * IndexedDB storage for persistent state
 */
class IndexedDBStateStorage {
  private db: IDBDatabase | null = null;
  private readonly storeName = 'ui_states';

  constructor(
    private dbName: string,
    private version: number
  ) {
    this.init();
  }

  private async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };
      
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        
        if (!db.objectStoreNames.contains(this.storeName)) {
          const store = db.createObjectStore(this.storeName, { keyPath: 'sessionId' });
          store.createIndex('timestamp', 'timestamp', { unique: false });
          store.createIndex('ui', 'ui', { unique: false });
        }
      };
    });
  }

  async save(state: UIState): Promise<void> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      const request = store.put(state);
      
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async load(sessionId: string): Promise<UIState | null> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.storeName], 'readonly');
      const store = transaction.objectStore(this.storeName);
      const request = store.get(sessionId);
      
      request.onsuccess = () => {
        const state = request.result;
        if (state && Date.now() - state.timestamp <= DEFAULT_CONFIG.stateExpiration) {
          resolve(state);
        } else {
          resolve(null);
        }
      };
      request.onerror = () => reject(request.error);
    });
  }

  async getLatest(): Promise<UIState | null> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.storeName], 'readonly');
      const store = transaction.objectStore(this.storeName);
      const index = store.index('timestamp');
      const request = index.openCursor(null, 'prev');
      
      request.onsuccess = () => {
        const cursor = request.result;
        if (cursor) {
          const state = cursor.value;
          if (Date.now() - state.timestamp <= DEFAULT_CONFIG.stateExpiration) {
            resolve(state);
          } else {
            resolve(null);
          }
        } else {
          resolve(null);
        }
      };
      request.onerror = () => reject(request.error);
    });
  }

  async clear(): Promise<void> {
    if (!this.db) await this.init();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      const request = store.clear();
      
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }
}

/**
 * Main State Manager class
 */
export class StateManager extends EventEmitter {
  private localStorage: LocalStateStorage;
  private indexedDB: IndexedDBStateStorage;
  private currentSessionId: string;
  private config: StateStorageConfig;

  constructor(config: Partial<StateStorageConfig> = {}) {
    super();
    
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.localStorage = new LocalStateStorage(this.config.localStorageKey);
    this.indexedDB = new IndexedDBStateStorage(
      this.config.indexedDBName,
      this.config.indexedDBVersion
    );
    this.currentSessionId = this.generateSessionId();
  }

  /**
   * Save current UI state
   */
  async saveState(ui: UITarget): Promise<void> {
    const state = await this.captureCurrentState(ui);
    
    // Save to all storage layers
    this.localStorage.save(state);
    await this.indexedDB.save(state);
    
    // Emit event for WebSocket sync
    this.emit('state:saved', state);
  }

  /**
   * Restore UI state
   */
  async restoreState(): Promise<UIState | null> {
    // Try local storage first (fastest)
    let state = this.localStorage.load();
    
    // Fall back to IndexedDB
    if (!state) {
      state = await this.indexedDB.getLatest();
    }
    
    if (state) {
      await this.applyState(state);
      this.emit('state:restored', state);
    }
    
    return state;
  }

  /**
   * Get current session ID
   */
  getSessionId(): string {
    return this.currentSessionId;
  }

  /**
   * Clear all stored state
   */
  async clearState(): Promise<void> {
    this.localStorage.clear();
    await this.indexedDB.clear();
    this.emit('state:cleared');
  }

  /**
   * Capture current UI state
   */
  private async captureCurrentState(ui: UITarget): Promise<UIState> {
    const state: UIState = {
      timestamp: Date.now(),
      ui,
      sessionId: this.currentSessionId,
      context: await this.captureContext(),
      auth: await this.captureAuth()
    };
    
    // Capture UI-specific state
    const uiSpecificData = await this.captureUISpecificState(ui);
    state.context.customData = uiSpecificData;
    
    return state;
  }

  /**
   * Capture general context
   */
  private async captureContext(): Promise<UIContext> {
    return {
      url: window.location.href,
      scrollPosition: window.scrollY,
      activeElement: document.activeElement?.id,
      formData: this.captureFormData(),
      customData: {},
      files: await this.captureFileContext(),
      history: this.captureRecentHistory()
    };
  }

  /**
   * Capture form data
   */
  private captureFormData(): Record<string, any> {
    const formData: Record<string, any> = {};
    
    // Capture all form inputs
    document.querySelectorAll('input, textarea, select').forEach((element) => {
      const input = element as HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement;
      if (input.name || input.id) {
        const key = input.name || input.id;
        
        if (input.type === 'checkbox') {
          formData[key] = (input as HTMLInputElement).checked;
        } else if (input.type === 'radio') {
          if ((input as HTMLInputElement).checked) {
            formData[key] = input.value;
          }
        } else {
          formData[key] = input.value;
        }
      }
    });
    
    return formData;
  }

  /**
   * Capture UI-specific state
   */
  private async captureUISpecificState(ui: UITarget): Promise<Record<string, any>> {
    switch (ui) {
      case 'chat':
        return this.captureChatState();
      case 'annotator':
        return this.captureAnnotatorState();
      case 'terminal':
        return this.captureTerminalState();
      default:
        return {};
    }
  }

  /**
   * Capture chat-specific state
   */
  private captureChatState(): Record<string, any> {
    // This would be implemented based on the actual chat UI
    return {
      conversationId: (window as any).currentConversationId || null,
      messages: (window as any).conversationHistory || [],
      selectedModel: (window as any).selectedModel || 'claude-3',
      settings: (window as any).chatSettings || {}
    };
  }

  /**
   * Capture annotator-specific state
   */
  private captureAnnotatorState(): Record<string, any> {
    // This would be implemented based on the actual annotator UI
    return {
      documentId: (window as any).currentDocumentId || null,
      currentPage: (window as any).currentPage || 1,
      annotations: (window as any).unsavedAnnotations || [],
      viewport: {
        zoom: (window as any).zoomLevel || 1,
        position: (window as any).viewportPosition || { x: 0, y: 0 }
      }
    };
  }

  /**
   * Capture terminal-specific state
   */
  private captureTerminalState(): Record<string, any> {
    // This would be implemented based on the actual terminal UI
    return {
      workingDirectory: (window as any).cwd || '~',
      commandHistory: (window as any).commandHistory || [],
      environment: (window as any).environmentVars || {},
      activeProcesses: (window as any).activeProcesses || []
    };
  }

  /**
   * Capture file context
   */
  private async captureFileContext(): Promise<FileContext[]> {
    // This would capture any open or recently accessed files
    const files: FileContext[] = [];
    
    // Example implementation
    if ((window as any).openFiles) {
      (window as any).openFiles.forEach((file: any) => {
        files.push({
          id: file.id,
          name: file.name,
          path: file.path,
          type: file.type,
          size: file.size,
          lastModified: file.lastModified
        });
      });
    }
    
    return files;
  }

  /**
   * Capture recent history
   */
  private captureRecentHistory(): HistoryItem[] {
    // This would capture recent user actions
    return (window as any).activityHistory || [];
  }

  /**
   * Capture authentication state
   */
  private async captureAuth(): Promise<AuthState> {
    // This would integrate with your auth system
    return {
      token: (window as any).authToken || '',
      expiresAt: (window as any).authExpiry || Date.now() + 3600000,
      user: (window as any).currentUser || {
        id: '',
        email: '',
        name: ''
      }
    };
  }

  /**
   * Apply restored state
   */
  private async applyState(state: UIState): Promise<void> {
    // Restore scroll position
    window.scrollTo(0, state.context.scrollPosition);
    
    // Restore form data
    this.restoreFormData(state.context.formData);
    
    // Restore UI-specific state
    await this.restoreUISpecificState(state.ui, state.context.customData);
    
    // Focus previously active element
    if (state.context.activeElement) {
      const element = document.getElementById(state.context.activeElement);
      element?.focus();
    }
  }

  /**
   * Restore form data
   */
  private restoreFormData(formData: Record<string, any>): void {
    Object.entries(formData).forEach(([key, value]) => {
      const element = document.querySelector(`[name="${key}"], #${key}`) as HTMLInputElement;
      if (element) {
        if (element.type === 'checkbox') {
          element.checked = value;
        } else if (element.type === 'radio') {
          const radio = document.querySelector(`[name="${key}"][value="${value}"]`) as HTMLInputElement;
          if (radio) radio.checked = true;
        } else {
          element.value = value;
        }
      }
    });
  }

  /**
   * Restore UI-specific state
   */
  private async restoreUISpecificState(ui: UITarget, customData: Record<string, any>): Promise<void> {
    switch (ui) {
      case 'chat':
        await this.restoreChatState(customData);
        break;
      case 'annotator':
        await this.restoreAnnotatorState(customData);
        break;
      case 'terminal':
        await this.restoreTerminalState(customData);
        break;
    }
  }

  /**
   * Restore chat state
   */
  private async restoreChatState(data: Record<string, any>): Promise<void> {
    if (data.conversationId) {
      (window as any).loadConversation?.(data.conversationId);
    }
    if (data.selectedModel) {
      (window as any).selectModel?.(data.selectedModel);
    }
  }

  /**
   * Restore annotator state
   */
  private async restoreAnnotatorState(data: Record<string, any>): Promise<void> {
    if (data.documentId) {
      (window as any).loadDocument?.(data.documentId);
    }
    if (data.currentPage) {
      (window as any).navigateToPage?.(data.currentPage);
    }
    if (data.viewport) {
      (window as any).setViewport?.(data.viewport);
    }
  }

  /**
   * Restore terminal state
   */
  private async restoreTerminalState(data: Record<string, any>): Promise<void> {
    if (data.workingDirectory) {
      (window as any).changeDirectory?.(data.workingDirectory);
    }
    if (data.commandHistory) {
      (window as any).restoreHistory?.(data.commandHistory);
    }
  }

  /**
   * Generate unique session ID
   */
  private generateSessionId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Export singleton instance
export const stateManager = new StateManager();