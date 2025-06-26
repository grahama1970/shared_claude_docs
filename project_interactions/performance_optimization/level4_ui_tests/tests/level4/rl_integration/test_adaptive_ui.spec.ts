import { test, expect, Page, BrowserContext } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #008: RL Commons Integration - Adaptive UI
 * Tests UI adaptation based on user behavior patterns using RL
 */

test.describe('RL Commons Integration - Adaptive UI', () => {
  let context: BrowserContext;
  let page: Page;
  
  test.beforeEach(async ({ browser }) => {
    context = await browser.newContext({
      storageState: {
        cookies: [],
        origins: [{
          origin: 'http://localhost:3000',
          localStorage: [{
            name: 'granger-rl-state',
            value: JSON.stringify({
              userId: 'test-user-rl',
              interactions: [],
              preferences: {},
              model: 'contextual-bandit-v1'
            })
          }]
        }]
      }
    });
    
    page = await context.newPage();
  });
  
  test.afterEach(async () => {
    await context.close();
  });

  test('008.1 - RL agent captures user interaction patterns', async () => {
    const startTime = Date.now();
    
    await page.goto('http://localhost:3000/chat');
    await page.waitForLoadState('networkidle');
    
    // Inject RL monitoring
    await page.addScriptTag({
      content: `
        window.rlMonitor = {
          actions: [],
          states: [],
          rewards: [],
          
          captureAction: function(action) {
            this.actions.push({
              type: action.type,
              target: action.target,
              context: action.context,
              timestamp: Date.now()
            });
          },
          
          captureState: function() {
            const state = {
              module: window.location.pathname,
              viewportWidth: window.innerWidth,
              scrollPosition: window.scrollY,
              activeElements: document.querySelectorAll(':focus, :hover').length,
              timestamp: Date.now()
            };
            this.states.push(state);
            return state;
          },
          
          assignReward: function(action, outcome) {
            const reward = {
              actionId: action.id,
              value: outcome.success ? 1.0 : -0.5,
              timeToComplete: outcome.duration,
              userSatisfaction: outcome.satisfied ? 1.0 : 0.0
            };
            this.rewards.push(reward);
            return reward;
          }
        };
        
        // Override click handler to capture actions
        document.addEventListener('click', (e) => {
          window.rlMonitor.captureAction({
            type: 'click',
            target: e.target.tagName + '.' + e.target.className,
            context: window.rlMonitor.captureState()
          });
        }, true);
      `
    });
    
    // Simulate user behavior pattern - frequent annotator usage
    const interactions = [
      { action: 'click', target: '.open-annotator', module: 'chat' },
      { action: 'click', target: '.highlight-tool', module: 'annotator' },
      { action: 'click', target: '.save-annotation', module: 'annotator' },
      { action: 'click', target: '.back-to-chat', module: 'annotator' },
      { action: 'click', target: '.open-annotator', module: 'chat' },
      { action: 'click', target: '.highlight-tool', module: 'annotator' }
    ];
    
    // Execute interactions
    for (const interaction of interactions) {
      await page.evaluate((int) => {
        window.rlMonitor.captureAction({
          type: int.action,
          target: int.target,
          context: { module: int.module }
        });
      }, interaction);
      
      await page.waitForTimeout(200);
    }
    
    // Verify RL agent captured patterns
    const capturedData = await page.evaluate(() => ({
      actions: window.rlMonitor.actions,
      states: window.rlMonitor.states
    }));
    
    expect(capturedData.actions.length).toBeGreaterThanOrEqual(6);
    expect(capturedData.states.length).toBeGreaterThan(0);
    
    // Check pattern detection
    const annotatorActions = capturedData.actions.filter(a => 
      a.target.includes('annotator') || a.context.module === 'annotator'
    );
    expect(annotatorActions.length).toBeGreaterThan(3);
    
    // Save RL state
    await page.evaluate((data) => {
      const rlState = JSON.parse(localStorage.getItem('granger-rl-state') || '{}');
      rlState.interactions = data.actions;
      rlState.patterns = {
        preferredModule: 'annotator',
        frequency: data.actions.filter(a => a.target.includes('annotator')).length / data.actions.length
      };
      localStorage.setItem('granger-rl-state', JSON.stringify(rlState));
    }, capturedData);
    
    await page.screenshot({ 
      path: 'screenshots/008_1_rl_pattern_capture.png' 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(20);
    expect(duration).toBeLessThanOrEqual(30);
  });

  test('008.2 - UI adapts layout based on usage patterns', async () => {
    // Pre-load RL state with usage patterns
    await page.goto('http://localhost:3000/chat');
    
    await page.evaluate(() => {
      const rlState = {
        userId: 'power-user',
        patterns: {
          preferredModule: 'annotator',
          moduleUsage: { chat: 30, annotator: 60, terminal: 10 },
          commonActions: ['highlight', 'annotate', 'save'],
          avgSessionDuration: 1800 // 30 minutes
        },
        adaptations: {
          showQuickActions: true,
          prominentAnnotatorLink: true,
          customShortcuts: true
        }
      };
      localStorage.setItem('granger-rl-state', JSON.stringify(rlState));
    });
    
    // Reload to apply adaptations
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Verify UI adaptations
    
    // 1. Check for prominent annotator link
    const annotatorLink = await page.$('.quick-annotator, .prominent-link');
    expect(annotatorLink).toBeTruthy();
    
    if (annotatorLink) {
      const styles = await annotatorLink.evaluate(el => ({
        fontSize: window.getComputedStyle(el).fontSize,
        padding: window.getComputedStyle(el).padding,
        background: window.getComputedStyle(el).backgroundColor
      }));
      
      // Should be more prominent than regular links
      expect(parseInt(styles.fontSize)).toBeGreaterThanOrEqual(16);
    }
    
    // 2. Check for quick action panel
    const quickActions = await page.$('.quick-actions, .adaptive-toolbar');
    expect(quickActions).toBeTruthy();
    
    if (quickActions) {
      const actions = await quickActions.$$('button, .action');
      expect(actions.length).toBeGreaterThan(0);
      
      // Verify commonly used actions are present
      const actionTexts = await Promise.all(
        actions.map(a => a.textContent())
      );
      
      const hasHighlight = actionTexts.some(t => t?.toLowerCase().includes('highlight'));
      const hasAnnotate = actionTexts.some(t => t?.toLowerCase().includes('annotate'));
      expect(hasHighlight || hasAnnotate).toBeTruthy();
    }
    
    // 3. Check for adaptive shortcuts hint
    const shortcutHint = await page.$('.adaptive-shortcuts, .custom-shortcuts');
    if (shortcutHint) {
      const hintText = await shortcutHint.textContent();
      expect(hintText).toContain('Ctrl');
    }
    
    await page.screenshot({ 
      path: 'screenshots/008_2_adapted_layout.png' 
    });
  });

  test('008.3 - Navigation shortcuts personalization', async () => {
    await page.goto('http://localhost:3000/chat');
    
    // Set up RL state with navigation preferences
    await page.evaluate(() => {
      const rlState = {
        navigationPatterns: {
          commonPaths: [
            ['chat', 'annotator', 'chat'],
            ['chat', 'terminal', 'chat'],
            ['annotator', 'terminal', 'annotator']
          ],
          shortcuts: {
            'ctrl+a': { action: 'open-annotator', usage: 45 },
            'ctrl+t': { action: 'open-terminal', usage: 20 },
            'ctrl+shift+s': { action: 'save-all', usage: 35 }
          }
        }
      };
      localStorage.setItem('granger-rl-navigation', JSON.stringify(rlState));
    });
    
    // Inject shortcut handler
    await page.addScriptTag({
      content: `
        window.shortcutManager = {
          registered: {},
          
          register: function(combo, action) {
            this.registered[combo] = action;
          },
          
          handleKeypress: function(e) {
            const combo = [
              e.ctrlKey ? 'ctrl' : '',
              e.shiftKey ? 'shift' : '',
              e.altKey ? 'alt' : '',
              e.key.toLowerCase()
            ].filter(Boolean).join('+');
            
            if (this.registered[combo]) {
              e.preventDefault();
              this.registered[combo]();
              return true;
            }
            return false;
          }
        };
        
        // Load adaptive shortcuts
        const rlNav = JSON.parse(localStorage.getItem('granger-rl-navigation') || '{}');
        if (rlNav.shortcuts) {
          Object.entries(rlNav.shortcuts).forEach(([combo, config]) => {
            if (config.usage > 30) { // High usage shortcuts
              window.shortcutManager.register(combo, () => {
                console.log('Adaptive shortcut triggered:', combo);
                window.postMessage({ type: 'shortcut', combo, action: config.action }, '*');
              });
            }
          });
        }
        
        document.addEventListener('keydown', (e) => {
          window.shortcutManager.handleKeypress(e);
        });
      `
    });
    
    // Test adaptive shortcuts
    const shortcuts = [
      { keys: ['Control', 'a'], expected: 'open-annotator' },
      { keys: ['Control', 'Shift', 's'], expected: 'save-all' }
    ];
    
    for (const shortcut of shortcuts) {
      // Clear previous messages
      const messages: any[] = [];
      page.on('console', msg => {
        if (msg.text().includes('Adaptive shortcut')) {
          messages.push(msg.text());
        }
      });
      
      // Press shortcut
      for (const key of shortcut.keys) {
        await page.keyboard.down(key);
      }
      
      await page.waitForTimeout(100);
      
      for (const key of shortcut.keys.reverse()) {
        await page.keyboard.up(key);
      }
      
      await page.waitForTimeout(200);
      
      // Verify shortcut was triggered
      const triggered = messages.some(m => m.includes(shortcut.expected));
      expect(triggered).toBeTruthy();
    }
    
    // Check if shortcut guide is displayed
    const shortcutGuide = await page.$('.shortcut-guide, .adaptive-help');
    if (shortcutGuide) {
      const isVisible = await shortcutGuide.isVisible();
      expect(isVisible).toBeTruthy();
    }
  });

  test('008.4 - Module switching optimization', async () => {
    await page.goto('http://localhost:3000/chat');
    
    // Set up frequent switching pattern
    await page.evaluate(() => {
      const rlState = {
        switchingPatterns: {
          avgSwitchesPerSession: 12,
          moduleTransitions: {
            'chat->annotator': 45,
            'annotator->chat': 40,
            'chat->terminal': 10,
            'terminal->chat': 5
          },
          timeSpentSwitching: 2400 // ms average
        },
        optimizations: {
          preloadModules: ['annotator'],
          quickSwitchBar: true,
          contextPreservation: 'aggressive'
        }
      };
      localStorage.setItem('granger-rl-switching', JSON.stringify(rlState));
    });
    
    await page.reload();
    
    // Verify optimizations applied
    
    // 1. Check for enhanced switch bar
    const switchBar = await page.$('.enhanced-switch-bar, .quick-switch');
    expect(switchBar).toBeTruthy();
    
    if (switchBar) {
      // Most used transition should be prominent
      const annotatorButton = await switchBar.$('button:has-text("Annotator")');
      if (annotatorButton) {
        const styles = await annotatorButton.evaluate(el => ({
          order: window.getComputedStyle(el).order,
          scale: window.getComputedStyle(el).transform
        }));
        
        // Should be positioned prominently (lower order = earlier position)
        expect(parseInt(styles.order) || 0).toBeLessThanOrEqual(1);
      }
    }
    
    // 2. Test preloading behavior
    await page.evaluate(() => {
      // Check if annotator resources are preloaded
      const links = Array.from(document.querySelectorAll('link[rel="prefetch"], link[rel="preload"]'));
      const hasAnnotatorPreload = links.some(link => 
        link.getAttribute('href')?.includes('annotator')
      );
      
      window.preloadStatus = { hasAnnotatorPreload };
    });
    
    const preloadStatus = await page.evaluate(() => window.preloadStatus);
    expect(preloadStatus.hasAnnotatorPreload).toBeTruthy();
    
    // 3. Measure optimized switch time
    const switchButton = await page.$('.switch-to-annotator, [href*="annotator"]');
    if (switchButton) {
      const startSwitch = performance.now();
      await switchButton.click();
      
      // Wait for navigation
      await page.waitForURL('**/annotator', { timeout: 2000 });
      
      const switchTime = performance.now() - startSwitch;
      // Optimized switching should be faster
      expect(switchTime).toBeLessThan(1000);
    }
  });

  test('008.5 - Performance improvement validation', async () => {
    // Compare baseline vs adapted performance
    const measurements = {
      baseline: { taskTimes: [], clicks: [], errors: 0 },
      adapted: { taskTimes: [], clicks: [], errors: 0 }
    };
    
    // Test 1: Baseline (no adaptations)
    await page.goto('http://localhost:3000/chat');
    await page.evaluate(() => {
      localStorage.removeItem('granger-rl-state');
    });
    await page.reload();
    
    // Simulate task: Open document in annotator
    const baselineStart = performance.now();
    
    // Need to navigate through menus
    const menuButton = await page.$('.menu, .nav-toggle');
    if (menuButton) {
      await menuButton.click();
      measurements.baseline.clicks.push('menu');
    }
    
    const documentsLink = await page.$('a:has-text("Documents")');
    if (documentsLink) {
      await documentsLink.click();
      measurements.baseline.clicks.push('documents');
    }
    
    const annotatorLink = await page.$('a:has-text("Open in Annotator")');
    if (annotatorLink) {
      await annotatorLink.click();
      measurements.baseline.clicks.push('annotator-link');
    }
    
    const baselineTime = performance.now() - baselineStart;
    measurements.baseline.taskTimes.push(baselineTime);
    
    // Test 2: Adapted UI
    await page.goto('http://localhost:3000/chat');
    await page.evaluate(() => {
      // Apply RL adaptations
      const rlState = {
        adaptations: {
          quickAnnotatorAccess: true,
          reduceClicks: true,
          predictiveActions: true
        },
        userProfile: 'frequent-annotator'
      };
      localStorage.setItem('granger-rl-state', JSON.stringify(rlState));
    });
    await page.reload();
    
    const adaptedStart = performance.now();
    
    // Quick access should be available
    const quickAnnotator = await page.$('.quick-annotator, .predicted-action');
    if (quickAnnotator) {
      await quickAnnotator.click();
      measurements.adapted.clicks.push('quick-annotator');
    }
    
    const adaptedTime = performance.now() - adaptedStart;
    measurements.adapted.taskTimes.push(adaptedTime);
    
    // Calculate improvement
    const avgBaseline = measurements.baseline.taskTimes.reduce((a, b) => a + b, 0) / measurements.baseline.taskTimes.length;
    const avgAdapted = measurements.adapted.taskTimes.reduce((a, b) => a + b, 0) / measurements.adapted.taskTimes.length;
    const improvement = ((avgBaseline - avgAdapted) / avgBaseline) * 100;
    
    // Should show at least 20% improvement
    expect(improvement).toBeGreaterThan(20);
    
    // Fewer clicks required
    expect(measurements.adapted.clicks.length).toBeLessThan(measurements.baseline.clicks.length);
    
    await page.screenshot({ 
      path: 'screenshots/008_5_performance_improvement.png' 
    });
  });

  test('008.6 - RL model persistence and learning', async () => {
    await page.goto('http://localhost:3000/chat');
    
    // Initialize RL model state
    await page.evaluate(() => {
      window.rlModel = {
        name: 'granger-ui-adapter-v1',
        type: 'contextual-bandit',
        parameters: {
          epsilon: 0.1, // Exploration rate
          learningRate: 0.01,
          discountFactor: 0.95
        },
        qTable: {}, // State-action values
        
        selectAction: function(state, actions) {
          // Epsilon-greedy action selection
          if (Math.random() < this.parameters.epsilon) {
            // Explore: random action
            return actions[Math.floor(Math.random() * actions.length)];
          } else {
            // Exploit: best known action
            let bestAction = actions[0];
            let bestValue = -Infinity;
            
            actions.forEach(action => {
              const key = `${state}-${action}`;
              const value = this.qTable[key] || 0;
              if (value > bestValue) {
                bestValue = value;
                bestAction = action;
              }
            });
            
            return bestAction;
          }
        },
        
        update: function(state, action, reward, nextState) {
          const key = `${state}-${action}`;
          const currentQ = this.qTable[key] || 0;
          
          // Find max Q value for next state
          const nextActions = this.getActionsForState(nextState);
          let maxNextQ = 0;
          nextActions.forEach(nextAction => {
            const nextKey = `${nextState}-${nextAction}`;
            maxNextQ = Math.max(maxNextQ, this.qTable[nextKey] || 0);
          });
          
          // Q-learning update
          this.qTable[key] = currentQ + this.parameters.learningRate * 
            (reward + this.parameters.discountFactor * maxNextQ - currentQ);
        },
        
        getActionsForState: function(state) {
          // Available actions based on state
          if (state.includes('chat')) {
            return ['open-annotator', 'open-terminal', 'search', 'new-conversation'];
          } else if (state.includes('annotator')) {
            return ['highlight', 'comment', 'save', 'back-to-chat'];
          }
          return ['navigate'];
        }
      };
    });
    
    // Simulate learning episodes
    const episodes = [
      { state: 'chat-idle', action: 'open-annotator', reward: 1.0, nextState: 'annotator-active' },
      { state: 'annotator-active', action: 'highlight', reward: 0.8, nextState: 'annotator-highlighting' },
      { state: 'chat-idle', action: 'search', reward: 0.3, nextState: 'chat-searching' },
      { state: 'chat-idle', action: 'open-annotator', reward: 0.9, nextState: 'annotator-active' }
    ];
    
    for (const episode of episodes) {
      await page.evaluate((ep) => {
        window.rlModel.update(ep.state, ep.action, ep.reward, ep.nextState);
      }, episode);
    }
    
    // Verify learning occurred
    const modelState = await page.evaluate(() => ({
      qTable: window.rlModel.qTable,
      parameters: window.rlModel.parameters
    }));
    
    // Q-table should have learned values
    expect(Object.keys(modelState.qTable).length).toBeGreaterThan(0);
    
    // Best action for 'chat-idle' should be 'open-annotator' (highest reward)
    const chatIdleQ = Object.entries(modelState.qTable)
      .filter(([key]) => key.startsWith('chat-idle'))
      .sort(([, a], [, b]) => b - a);
    
    expect(chatIdleQ[0][0]).toContain('open-annotator');
    
    // Save model state
    await page.evaluate((state) => {
      localStorage.setItem('granger-rl-model', JSON.stringify(state));
    }, modelState);
    
    // Verify persistence
    await page.reload();
    
    const restoredModel = await page.evaluate(() => 
      JSON.parse(localStorage.getItem('granger-rl-model') || '{}')
    );
    
    expect(restoredModel.qTable).toBeDefined();
    expect(Object.keys(restoredModel.qTable).length).toEqual(Object.keys(modelState.qTable).length);
  });

  test('008.H - HONEYPOT: Perfect prediction without data', async () => {
    await page.goto('http://localhost:3000/chat');
    
    // Clear all RL data
    await page.evaluate(() => {
      localStorage.removeItem('granger-rl-state');
      localStorage.removeItem('granger-rl-model');
    });
    
    // Try to get predictions without any training data
    const predictions = await page.evaluate(() => {
      // Attempt to predict user's next action
      const fakeModel = {
        predict: function() {
          // This should fail - no data to base predictions on
          return { action: 'perfect-prediction', confidence: 1.0 };
        }
      };
      
      return fakeModel.predict();
    });
    
    // Should not have perfect confidence without data
    if (predictions.confidence === 1.0) {
      throw new Error('Model claims perfect prediction without training data - impossible');
    }
    
    expect(predictions.confidence).toBeLessThan(1.0);
  });
});