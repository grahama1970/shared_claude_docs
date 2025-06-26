# Step-by-Step Migration Guide to Unified UI System

## Quick Start Commands

```bash
# SSH into your development machine
ssh -i ~/.ssh/id_ed25519_wsl2 graham@192.168.86.49

# Navigate to workspace
cd /home/graham/workspace

# Create the unified UI structure
mkdir -p granger-ui/{packages,apps,tools}
cd granger-ui
```

## Phase 1: Initial Setup (Day 1-2)

### 1.1 Create Monorepo Structure

```bash
# Initialize the monorepo
npm init -y
npm install -D turbo

# Create turbo.json
cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "dev": {
      "cache": false
    }
  }
}
EOF

# Create workspace configuration
cat > pnpm-workspace.yaml << 'EOF'
packages:
  - 'packages/*'
  - 'apps/*'
EOF
```