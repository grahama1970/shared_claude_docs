#!/bin/bash

# Run Claude Module Interaction Scenarios

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎭 Claude Module Interaction Scenarios${NC}"
echo "======================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running installation..."
    ./install_dependencies.sh
fi

# Activate virtual environment
source .venv/bin/activate

# Check command line arguments
if [ $# -eq 0 ]; then
    echo ""
    echo "Available scenarios:"
    echo -e "  ${GREEN}1.${NC} research_evolution   - Modules collaborate on research and learning"
    echo -e "  ${GREEN}2.${NC} ui_improvement      - UI analysis and self-improvement"
    echo -e "  ${GREEN}3.${NC} schema_negotiation  - Dynamic schema discovery and adaptation"
    echo -e "  ${GREEN}4.${NC} conversational      - Interactive conversational orchestration"
    echo -e "  ${GREEN}5.${NC} grand_collaboration - All modules work together on complex project"
    echo -e "  ${GREEN}6.${NC} all                 - Run all scenarios"
    echo ""
    echo "Usage: $0 <scenario_name>"
    echo "Example: $0 research_evolution"
    exit 1
fi

SCENARIO=$1

# Function to run a scenario
run_scenario() {
    local scenario_name=$1
    local script_name=$2
    
    echo ""
    echo -e "${YELLOW}Running scenario: ${scenario_name}${NC}"
    echo "----------------------------------------"
    
    python scenarios/${script_name}
    
    echo ""
    echo -e "${GREEN}✅ Scenario complete!${NC}"
    echo ""
}

# Check if discovery service is running
check_discovery_service() {
    if ! curl -s http://localhost:8888/modules > /dev/null 2>&1; then
        echo -e "${RED}⚠️  Discovery service not running!${NC}"
        echo "Please start it in another terminal:"
        echo "  ./start_discovery_service.sh"
        echo ""
        read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
    fi
}

# Main execution
case $SCENARIO in
    research_evolution|research|1)
        check_discovery_service
        run_scenario "Research Evolution" "research_evolution.py"
        ;;
    
    ui_improvement|ui|2)
        check_discovery_service
        run_scenario "UI Self-Improvement" "ui_self_improvement.py"
        ;;
    
    schema_negotiation|schema|3)
        check_discovery_service
        run_scenario "Schema Negotiation" "schema_negotiation.py"
        ;;
    
    conversational|converse|4)
        check_discovery_service
        echo ""
        echo -e "${YELLOW}Starting Conversational Interface${NC}"
        echo "----------------------------------------"
        python -c "
import asyncio
from orchestrator.task_orchestrator import ConversationalOrchestrator

async def interactive_session():
    async with ConversationalOrchestrator() as orchestrator:
        print('\\n🤖 Claude Module Orchestrator')
        print('Type your requests in natural language. Type \"exit\" to quit.\\n')
        
        while True:
            try:
                user_input = input('You: ')
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print('\\nGoodbye! 👋')
                    break
                
                response = await orchestrator.converse(user_input)
                print(f\"\\nAssistant: {response['response']}\\n\")
                
            except KeyboardInterrupt:
                print('\\n\\nGoodbye! 👋')
                break
            except Exception as e:
                print(f'\\n❌ Error: {e}\\n')

asyncio.run(interactive_session())
"
        ;;
    
    grand_collaboration|grand|5)
        check_discovery_service
        run_scenario "Grand Collaboration" "grand_collaboration.py"
        ;;
    
    all|6)
        check_discovery_service
        run_scenario "Research Evolution" "research_evolution.py"
        run_scenario "UI Self-Improvement" "ui_self_improvement.py"
        run_scenario "Schema Negotiation" "schema_negotiation.py"
        run_scenario "Grand Collaboration" "grand_collaboration.py"
        echo -e "${GREEN}✅ All scenarios complete!${NC}"
        ;;
    
    *)
        echo -e "${RED}Unknown scenario: $SCENARIO${NC}"
        echo "Run without arguments to see available scenarios"
        exit 1
        ;;
esac

# Show reports location
if [ -d "reports" ] && [ "$(ls -A reports)" ]; then
    echo ""
    echo -e "${BLUE}📊 Reports generated:${NC}"
    ls -la reports/*.json reports/*.md 2>/dev/null | tail -5
fi

# Show visualizations location
if [ -d "visualizations" ] && [ "$(ls -A visualizations)" ]; then
    echo ""
    echo -e "${BLUE}📈 Visualizations generated:${NC}"
    ls -la visualizations/*.png 2>/dev/null | tail -5
fi