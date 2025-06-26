# ⚡ GRANGER Quick Start Guide for Claude Code

**Purpose**: Get up and running with GRANGER development quickly

---

## 🚀 Prerequisites

1. **System Requirements**
   - Ubuntu/WSL2 with Node.js 18+
   - Python 3.10+
   - pnpm (installed via curl)
   - Git

2. **Access Requirements**
   - SSH access to development server
   - Repository access

---

## 🏃 Quick Start Commands

### 1. Clone and Setup (if needed)
```bash
# Already exists at /home/graham/workspace/
cd /home/graham/workspace/
```

### 2. Install Dependencies
```bash
# UI Monorepo
cd granger-ui
source ~/.zshrc  # Load pnpm
pnpm install

# Individual modules (example)
cd ../experiments/chat
npm install
```

### 3. Start Development Environment
```bash
# Terminal 1: Start the Hub
cd /home/graham/workspace/central_command
python server.py

# Terminal 2: Start UI Development
cd /home/graham/workspace/granger-ui
pnpm dev

# Terminal 3: Start a Module (e.g., Chat)
cd /home/graham/workspace/experiments/chat
npm run dev
```

---

## 🎯 Common Development Tasks

### Adding a New UI Component
```bash
cd /home/graham/workspace/granger-ui/packages/ui-web/src/components
# Create YourComponent.tsx
# Update index.ts to export it
```

### Running Storybook
```bash
cd /home/graham/workspace/granger-ui/apps/storybook
pnpm dev
# Open http://localhost:6006
```

### Testing UI Components
```bash
cd /home/graham/workspace/granger-ui
pnpm test
```

### Building for Production
```bash
cd /home/graham/workspace/granger-ui
pnpm build
```

---

## 🔧 Module-Specific Commands

### Chat Interface
```bash
cd /home/graham/workspace/experiments/chat
npm run dev          # Development
npm run build        # Production build
npm run test         # Run tests
```

### Marker Ground Truth
```bash
cd /home/graham/workspace/experiments/marker_ground_truth
npm run dev          # Start both frontend and backend
npm run migrate      # Run database migrations
```

### ArXiv MCP
```bash
cd /home/graham/workspace/experiments/arxiv_mcp
python server.py     # Start MCP server
```

---

## 🐛 Troubleshooting

### Issue: pnpm not found
```bash
source ~/.zshrc
# or
export PATH="$HOME/.local/share/pnpm:$PATH"
```

### Issue: Port already in use
```bash
# Find process using port
lsof -i :8765
# Kill process
kill -9 <PID>
```

### Issue: Module not connecting to hub
1. Check hub is running: `curl http://localhost:8765/health`
2. Verify WebSocket URL in module config
3. Check firewall/network settings

### Issue: UI components not building
```bash
cd /home/graham/workspace/granger-ui
pnpm clean
pnpm install
pnpm build
```

---

## 📁 Important Files

### Configuration Files
- `/granger-ui/pnpm-workspace.yaml` - Monorepo config
- `/experiments/*/package.json` - Module dependencies
- `/.env` files - Environment variables

### Documentation
- `/shared_claude_docs/docs/` - All documentation
- `/shared_claude_docs/guides/` - Style guides
- Individual README.md files in each module

### Key Source Files
- `/central_command/server.py` - Hub implementation
- `/granger-ui/packages/ui-web/src/components/` - UI components
- `/experiments/*/src/` - Module source code

---

## 🎨 UI Development Workflow

1. **Create Component**
   ```tsx
   // In ui-web/src/components/NewComponent.tsx
   export const NewComponent = () => {
     return <div>New Component</div>;
   };
   ```

2. **Add Story**
   ```javascript
   // In storybook/stories/NewComponent.stories.js
   export default {
     title: "Components/NewComponent",
     component: NewComponent,
   };
   ```

3. **Test Component**
   ```bash
   pnpm test NewComponent
   ```

4. **Use in Module**
   ```tsx
   import { NewComponent } from "@granger/ui-web";
   ```

---

## 🔄 Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
git add .
git commit -m "feat: add new component"

# Push changes
git push origin feature/your-feature

# Create PR for review
```

---

## 📊 Monitoring Development

### Check Build Status
```bash
cd /home/graham/workspace/granger-ui
pnpm build:status
```

### View Logs
```bash
# Hub logs
tail -f /home/graham/workspace/central_command/logs/hub.log

# Module logs
tail -f /home/graham/workspace/experiments/chat/logs/app.log
```

### Performance Metrics
```bash
# Run performance tests
cd /home/graham/workspace/granger-ui
pnpm perf
```

---

## 🚦 Health Checks

### System Health
```bash
# Check all services
curl http://localhost:8765/health  # Hub
curl http://localhost:3000/health  # Chat
curl http://localhost:3001/health  # Marker
```

### Database Status
```bash
# Check SQLite databases
sqlite3 /home/graham/workspace/experiments/marker_ground_truth/data/markers.db ".tables"
```

---

## 📞 Getting Help

1. **Documentation**: `/shared_claude_docs/docs/`
2. **Code Examples**: Storybook at `http://localhost:6006`
3. **Logs**: Check module-specific log files
4. **Contact**: graham@granger-aerospace.com

---

## 🎯 Next Steps

1. Review the main overview document
2. Set up your development environment
3. Run the existing modules
4. Start implementing assigned tasks
5. Test thoroughly before committing

---

**Remember**: Always pull latest changes before starting work!
```bash
git pull origin main
pnpm install  # In case dependencies changed
```
'EOF'