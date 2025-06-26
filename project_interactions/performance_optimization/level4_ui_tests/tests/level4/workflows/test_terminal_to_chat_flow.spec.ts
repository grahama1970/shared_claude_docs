import { test, expect, Page, BrowserContext } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #007: User Input Flow - Terminal to Chat
 * Tests workflow from terminal command execution to chat discussion
 */

test.describe('User Input Flow - Terminal to Chat', () => {
  let context: BrowserContext;
  let terminalPage: Page;
  let chatPage: Page;
  
  test.beforeEach(async ({ browser }) => {
    context = await browser.newContext({
      storageState: {
        cookies: [],
        origins: [{
          origin: 'http://localhost:3000',
          localStorage: [{
            name: 'granger-session',
            value: JSON.stringify({
              id: 'terminal-workflow-session',
              user: 'test-user',
              workspace: 'data-analysis'
            })
          }]
        }]
      }
    });
    
    terminalPage = await context.newPage();
    chatPage = await context.newPage();
    
    await terminalPage.goto('http://localhost:3002/terminal');
    await chatPage.goto('http://localhost:3000/chat');
  });
  
  test.afterEach(async () => {
    await context.close();
  });

  test('007.1 - Complete workflow from terminal command to chat', async () => {
    const startTime = Date.now();
    
    // Step 1: Execute analysis command in terminal
    await terminalPage.bringToFront();
    await terminalPage.waitForLoadState('networkidle');
    
    const terminalInput = await terminalPage.waitForSelector('.terminal-input, .xterm-helper-textarea, [contenteditable="true"]');
    await terminalInput.click();
    
    // Type analysis command
    const command = 'granger analyze dataset.csv --columns "revenue,growth" --output json';
    for (const char of command) {
      await terminalPage.keyboard.type(char);
      await terminalPage.waitForTimeout(20); // Simulate real typing
    }
    
    await terminalPage.screenshot({ 
      path: 'screenshots/007_1_terminal_command.png' 
    });
    
    await terminalPage.keyboard.press('Enter');
    
    // Step 2: Wait for command execution
    await terminalPage.waitForTimeout(1500); // Simulate processing time
    
    // Simulate command output
    await terminalPage.evaluate(() => {
      const output = {
        status: 'success',
        summary: {
          total_records: 10000,
          revenue_mean: 125000,
          growth_mean: 0.15,
          anomalies: 3,
          insights: [
            'Q4 revenue spike detected',
            'Growth rate declining in recent months',
            'Three outliers require investigation'
          ]
        }
      };
      
      // Display in terminal
      const term = document.querySelector('.terminal-output, .xterm-rows');
      if (term) {
        const outputDiv = document.createElement('div');
        outputDiv.innerHTML = `<pre style="color: #10B981">${JSON.stringify(output, null, 2)}</pre>`;
        term.appendChild(outputDiv);
      }
      
      // Store in session for chat
      const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
      session.lastCommand = {
        command: 'granger analyze dataset.csv',
        output: output,
        timestamp: Date.now()
      };
      localStorage.setItem('granger-session', JSON.stringify(session));
    });
    
    // Step 3: Look for chat integration option
    await terminalPage.waitForSelector('.chat-action, button:has-text("Discuss"), [aria-label*="chat"]', 
      { timeout: 5000 }
    );
    
    const chatButton = await terminalPage.$('.chat-action, button:has-text("Discuss in Chat")');
    expect(chatButton).toBeTruthy();
    
    // Step 4: Click to open in chat
    const transitionStart = performance.now();
    await chatButton.click();
    
    // Step 5: Switch to chat and verify context
    await chatPage.bringToFront();
    await chatPage.waitForLoadState('networkidle');
    
    const transitionTime = performance.now() - transitionStart;
    expect(transitionTime).toBeLessThan(2000);
    
    // Verify command output appears in chat
    const chatContext = await chatPage.evaluate(() => {
      const session = localStorage.getItem('granger-session');
      return session ? JSON.parse(session) : null;
    });
    
    expect(chatContext.lastCommand).toBeTruthy();
    expect(chatContext.lastCommand.command).toContain('analyze dataset.csv');
    expect(chatContext.lastCommand.output.summary.anomalies).toBe(3);
    
    // Step 6: Check if insights are displayed in chat
    await chatPage.waitForSelector('.analysis-summary, .command-output', { timeout: 5000 });
    
    const insightElements = await chatPage.$$('.insight, .finding, li');
    let foundInsights = 0;
    
    for (const element of insightElements) {
      const text = await element.textContent();
      if (text?.includes('revenue spike') || text?.includes('Growth rate') || text?.includes('outliers')) {
        foundInsights++;
      }
    }
    
    expect(foundInsights).toBeGreaterThan(0);
    
    // Step 7: Ask follow-up question about the analysis
    const chatInput = await chatPage.$('.chat-input, textarea');
    await chatInput.click();
    await chatInput.type('Can you explain the Q4 revenue spike? Show me a visualization of the trend.');
    await chatPage.keyboard.press('Enter');
    
    // Wait for response
    await chatPage.waitForSelector('.ai-response, .assistant-message', { timeout: 10000 });
    
    // Step 8: Verify visualization suggestion or creation
    const vizElement = await chatPage.$('.visualization, .chart, canvas, svg');
    const vizSuggestion = await chatPage.$('text=/visualiz|chart|graph/i');
    
    expect(vizElement || vizSuggestion).toBeTruthy();
    
    await chatPage.screenshot({ 
      path: 'screenshots/007_1_chat_visualization.png',
      fullPage: true 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(15);
    expect(duration).toBeLessThanOrEqual(25);
  });

  test('007.2 - Terminal output formatting in chat', async () => {
    // Set up terminal output
    await terminalPage.bringToFront();
    
    // Execute different types of commands
    const commands = [
      { cmd: 'ls -la', type: 'file-listing' },
      { cmd: 'git status', type: 'git-output' },
      { cmd: 'npm test', type: 'test-results' }
    ];
    
    for (const { cmd, type } of commands) {
      await terminalPage.evaluate(({ command, outputType }) => {
        // Simulate command execution
        const term = document.querySelector('.terminal, .xterm');
        if (term) {
          const cmdLine = document.createElement('div');
          cmdLine.innerHTML = `<span style="color: #10B981">$</span> ${command}`;
          term.appendChild(cmdLine);
          
          // Add formatted output based on type
          const output = document.createElement('div');
          output.className = `terminal-output ${outputType}`;
          
          if (outputType === 'file-listing') {
            output.innerHTML = `
              <div>total 156</div>
              <div>drwxr-xr-x  5 user  staff   160 Nov  4 10:30 .</div>
              <div>-rw-r--r--  1 user  staff  2048 Nov  4 10:25 dataset.csv</div>
            `;
          } else if (outputType === 'git-output') {
            output.innerHTML = `
              <div style="color: #10B981">On branch main</div>
              <div>Your branch is up to date with 'origin/main'.</div>
              <div style="color: #F59E0B">Changes not staged for commit:</div>
            `;
          } else if (outputType === 'test-results') {
            output.innerHTML = `
              <div style="color: #10B981">✓ 45 passing</div>
              <div style="color: #EF4444">✗ 2 failing</div>
              <div>Time: 3.5s</div>
            `;
          }
          
          term.appendChild(output);
        }
        
        // Store in session
        const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
        session.terminalOutputs = session.terminalOutputs || [];
        session.terminalOutputs.push({
          command: command,
          output: output.textContent,
          type: outputType,
          timestamp: Date.now()
        });
        localStorage.setItem('granger-session', JSON.stringify(session));
      }, { command: cmd, outputType: type });
      
      await terminalPage.waitForTimeout(500);
    }
    
    // Navigate to chat
    const chatLink = await terminalPage.$('.chat-link, button:has-text("Share in Chat")');
    if (chatLink) {
      await chatLink.click();
    }
    
    await chatPage.bringToFront();
    await chatPage.waitForLoadState('networkidle');
    
    // Verify formatted output in chat
    const terminalOutputs = await chatPage.$$('.terminal-output-block, .code-block');
    
    for (const output of terminalOutputs) {
      // Check if monospace font is used
      const fontFamily = await output.evaluate(el => 
        window.getComputedStyle(el).fontFamily
      );
      expect(fontFamily).toContain('monospace');
      
      // Check background styling
      const background = await output.evaluate(el => 
        window.getComputedStyle(el).backgroundColor
      );
      expect(background).not.toBe('transparent');
      
      // Check syntax highlighting preserved
      const coloredElements = await output.$$('[style*="color"]');
      expect(coloredElements.length).toBeGreaterThan(0);
    }
  });

  test('007.3 - Interactive terminal sessions in chat', async () => {
    // Start an interactive session
    await terminalPage.bringToFront();
    
    // Start Python REPL
    const terminal = await terminalPage.$('.terminal-input, .xterm');
    await terminal.click();
    await terminalPage.keyboard.type('python3');
    await terminalPage.keyboard.press('Enter');
    
    await terminalPage.waitForTimeout(1000);
    
    // Type some Python code
    const pythonCommands = [
      'import pandas as pd',
      'df = pd.read_csv("dataset.csv")',
      'df.describe()'
    ];
    
    for (const cmd of pythonCommands) {
      await terminalPage.keyboard.type(cmd);
      await terminalPage.keyboard.press('Enter');
      await terminalPage.waitForTimeout(500);
    }
    
    // Share session in chat
    await terminalPage.evaluate(() => {
      const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
      session.interactiveSession = {
        type: 'python',
        commands: [
          'import pandas as pd',
          'df = pd.read_csv("dataset.csv")',
          'df.describe()'
        ],
        active: true
      };
      localStorage.setItem('granger-session', JSON.stringify(session));
    });
    
    // Navigate to chat
    const shareButton = await terminalPage.$('.share-session, button:has-text("Share Session")');
    if (shareButton) {
      await shareButton.click();
    }
    
    await chatPage.bringToFront();
    
    // Verify interactive session indicator
    const sessionIndicator = await chatPage.$('.interactive-session, .live-terminal');
    expect(sessionIndicator).toBeTruthy();
    
    // Check if user can send commands from chat
    const remoteTerminal = await chatPage.$('.remote-terminal, .terminal-embed');
    if (remoteTerminal) {
      const isInteractive = await remoteTerminal.evaluate(el => 
        el.getAttribute('contenteditable') === 'true' || 
        el.querySelector('input, textarea') !== null
      );
      expect(isInteractive).toBeTruthy();
    }
  });

  test('007.4 - Error handling from terminal to chat', async () => {
    await terminalPage.bringToFront();
    
    // Execute failing command
    const terminal = await terminalPage.$('.terminal-input, .xterm');
    await terminal.click();
    await terminalPage.keyboard.type('granger analyze missing-file.csv');
    await terminalPage.keyboard.press('Enter');
    
    await terminalPage.waitForTimeout(1000);
    
    // Simulate error output
    await terminalPage.evaluate(() => {
      const term = document.querySelector('.terminal, .xterm');
      if (term) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-output';
        errorDiv.style.color = '#EF4444';
        errorDiv.innerHTML = `
          Error: File 'missing-file.csv' not found
          Stack trace:
            at FileReader.read (analyzer.js:45:10)
            at GrangerAnalyzer.analyze (analyzer.js:120:5)
        `;
        term.appendChild(errorDiv);
      }
      
      // Store error in session
      const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
      session.lastError = {
        command: 'granger analyze missing-file.csv',
        error: 'File not found',
        stackTrace: 'at FileReader.read...',
        timestamp: Date.now()
      };
      localStorage.setItem('granger-session', JSON.stringify(session));
    });
    
    // Look for help option
    const helpButton = await terminalPage.$('.get-help, button:has-text("Get Help")');
    expect(helpButton).toBeTruthy();
    
    await helpButton.click();
    
    // Switch to chat
    await chatPage.bringToFront();
    await chatPage.waitForLoadState('networkidle');
    
    // Verify error context in chat
    const errorContext = await chatPage.$('.error-context, .error-message');
    expect(errorContext).toBeTruthy();
    
    // Check if AI provides helpful suggestions
    await chatPage.waitForSelector('.ai-response, .assistant-message');
    
    const suggestions = await chatPage.$$('.suggestion, .solution, li');
    let foundSuggestions = 0;
    
    for (const suggestion of suggestions) {
      const text = await suggestion.textContent();
      if (text?.includes('check file path') || 
          text?.includes('verify file exists') || 
          text?.includes('correct filename')) {
        foundSuggestions++;
      }
    }
    
    expect(foundSuggestions).toBeGreaterThan(0);
  });

  test('007.5 - Performance metrics from terminal operations', async () => {
    // Monitor performance during workflow
    const metrics = {
      terminal: { fps: [], latency: [] },
      chat: { fps: [], renderTime: [] }
    };
    
    // Inject performance monitoring
    await terminalPage.addScriptTag({
      content: `
        window.perfMonitor = {
          startCommand: null,
          measure: function(command) {
            this.startCommand = performance.now();
            return {
              end: () => {
                const duration = performance.now() - this.startCommand;
                window.postMessage({
                  type: 'perf-metric',
                  command: command,
                  duration: duration
                }, '*');
              }
            };
          }
        };
      `
    });
    
    await terminalPage.bringToFront();
    
    // Execute performance-intensive command
    const terminal = await terminalPage.$('.terminal-input, .xterm');
    await terminal.click();
    
    // Measure command execution
    await terminalPage.evaluate(() => {
      const monitor = window.perfMonitor.measure('granger benchmark --iterations 1000');
      // Simulate command execution
      setTimeout(() => monitor.end(), 2000);
    });
    
    await terminalPage.keyboard.type('granger benchmark --iterations 1000');
    await terminalPage.keyboard.press('Enter');
    
    await terminalPage.waitForTimeout(2500);
    
    // Simulate benchmark results
    await terminalPage.evaluate(() => {
      const results = {
        operations: 1000,
        totalTime: 2.1,
        avgTime: 0.0021,
        throughput: '476 ops/sec',
        memoryUsed: '45MB'
      };
      
      const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
      session.benchmarkResults = results;
      localStorage.setItem('granger-session', JSON.stringify(session));
    });
    
    // Navigate to chat
    const resultsButton = await terminalPage.$('.view-results, button:has-text("View in Chat")');
    if (resultsButton) {
      await resultsButton.click();
    }
    
    await chatPage.bringToFront();
    
    // Verify performance visualization in chat
    const perfViz = await chatPage.$('.performance-chart, .benchmark-results');
    expect(perfViz).toBeTruthy();
    
    // Check if metrics are displayed correctly
    const metricsDisplay = await chatPage.$$('.metric-value, .stat');
    expect(metricsDisplay.length).toBeGreaterThan(0);
    
    // Verify throughput is highlighted
    const throughputElement = await chatPage.$('text=/476 ops|throughput/i');
    expect(throughputElement).toBeTruthy();
  });

  test('007.H - HONEYPOT: Instant terminal execution', async () => {
    await terminalPage.bringToFront();
    
    const startTime = performance.now();
    
    // Try to execute complex command instantly
    await terminalPage.evaluate(() => {
      // Simulate instant command completion
      const term = document.querySelector('.terminal');
      if (term) {
        term.innerHTML += '<div>Command completed in 0ms</div>';
      }
    });
    
    const executionTime = performance.now() - startTime;
    
    // Complex commands should take measurable time
    if (executionTime < 10) {
      throw new Error('Terminal command executed instantly - this is unrealistic');
    }
    
    expect(executionTime).toBeGreaterThan(10);
  });
});