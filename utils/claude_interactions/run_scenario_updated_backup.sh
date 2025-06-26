#!/bin/bash

# Run Claude Module Interaction Scenarios

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "🎭 Claude Module Interaction Scenarios"
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
    echo -e "Classic Scenarios:"
    echo -e "  1. research_evolution   - Modules collaborate on research and learning"
    echo -e "  2. ui_improvement      - UI analysis and self-improvement"
    echo -e "  3. schema_negotiation  - Dynamic schema discovery and adaptation"
    echo -e "  4. conversational      - Interactive conversational orchestration"
    echo -e "  5. grand_collaboration - All modules work together on complex project"
    echo ""
    echo -e "Creative Scenarios:"
    echo -e "  6. symphony           - Parallel processing with synchronized harmony"
    echo -e "  7. detective          - Collaborative mystery solving"
    echo -e "  8. ecosystem          - Symbiotic module relationships"
    echo -e "  9. mirror             - Reflective transformation chain"
    echo ""
    echo -e "Stress Tests:"
    echo -e "  10. avalanche         - Cascading failure and recovery"
    echo -e "  11. contradiction     - Conflicting information handling"
    echo -e "  12. resource_strangler - Resource starvation testing"
    echo -e "  13. schema_shapeshifter - Dynamic schema evolution"
    echo -e "  14. security_breach   - Malicious input handling"
    echo ""
    echo -e "Collections:"
    echo -e "  all                  - Run all classic scenarios"
    echo -e "  creative             - Run all creative scenarios"
    echo -e "  stress               - Run all stress tests"
    echo -e "  everything           - Run ALL scenarios"
    echo ""
    echo "Usage: $0 <scenario_name>"
    echo "Example: $0 symphony"
    exit 1
fi

SCENARIO=$1

# Function to run a scenario
run_scenario() {
    local scenario_name=$1
    local script_name=$2
    local scenario_type=$3
    
    echo ""
    echo -e "Running ${scenario_type} scenario: ${scenario_name}"
    echo "----------------------------------------"
    
    case $scenario_type in
        "classic")
            python scenarios/${script_name}
            ;;
        "creative")
            python creative_scenarios/${script_name}
            ;;
        "stress")
            python stress_tests/${script_name}
            ;;
    esac
    
    echo ""
    echo -e "✅ Scenario complete!"
    echo ""
}

# Check if discovery service is running
check_discovery_service() {
    if ! curl -s http://localhost:8888/modules > /dev/null 2>&1; then
        echo -e "⚠️  Discovery service not running!"
        echo "Please start it in another terminal:"
        echo "  ./start_discovery_service.sh"
        echo ""
        read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
    fi
}

# Main execution
case $SCENARIO in
    # Classic scenarios
    research_evolution|research|1)
        check_discovery_service
        run_scenario "Research Evolution" "research_evolution.py" "classic"
        ;;
    
    ui_improvement|ui|2)
        check_discovery_service
        run_scenario "UI Self-Improvement" "ui_self_improvement.py" "classic"
        ;;
    
    schema_negotiation|schema|3)
        check_discovery_service
        run_scenario "Schema Negotiation" "schema_negotiation.py" "classic"
        ;;
    
    conversational|converse|4)
        check_discovery_service
        echo ""
        echo -e "Starting Conversational Interface"
        echo "----------------------------------------"
        python -c "
import asyncio
from orchestrator.task_orchestrator import ConversationalOrchestrator

async def interactive_session():
    async with ConversationalOrchestrator() as orchestrator:
        print('\n🤖 Claude Module Orchestrator')
        print('Type your requests in natural language. Type "exit" to quit.\n')
        
        while True:
            try:
                user_input = input('You: ')
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print('\nGoodbye! 👋')
                    break
                
                response = await orchestrator.converse(user_input)
                print(f"\nAssistant: {response['response']}\n")
                
            except KeyboardInterrupt:
                print('\n\nGoodbye! 👋')
                break
            except Exception as e:
                print(f'\n❌ Error: {e}\n')

asyncio.run(interactive_session())
"
        ;;
    
    grand_collaboration|grand|5)
        check_discovery_service
        run_scenario "Grand Collaboration" "grand_collaboration.py" "classic"
        ;;
    
    # Creative scenarios
    symphony|6)
        check_discovery_service
        run_scenario "The Symphony" "symphony_scenario.py" "creative"
        ;;
    
    detective|7)
        check_discovery_service
        run_scenario "The Detective" "detective_scenario.py" "creative"
        ;;
    
    ecosystem|8)
        check_discovery_service
        run_scenario "The Ecosystem" "ecosystem_scenario.py" "creative"
        ;;
    
    mirror|9)
        check_discovery_service
        run_scenario "The Mirror" "mirror_scenario.py" "creative"
        ;;
    
    # Stress tests
    avalanche|cascade|10)
        check_discovery_service
        run_scenario "The Avalanche" "avalanche_scenario.py" "stress"
        ;;
    
    contradiction|conflict|11)
        check_discovery_service
        run_scenario "The Contradiction" "contradiction_scenario.py" "stress"
        ;;
    
    resource_strangler|resource|12)
        check_discovery_service
        run_scenario "The Resource Strangler" "resource_strangler.py" "stress"
        ;;
    
    schema_shapeshifter|shapeshifter|13)
        check_discovery_service
        run_scenario "The Schema Shapeshifter" "schema_shapeshifter.py" "stress"
        ;;
    
    security_breach|security|14)
        check_discovery_service
        run_scenario "The Security Breach" "security_breach.py" "stress"
        ;;
    
    # Collections
    all)
        check_discovery_service
        run_scenario "Research Evolution" "research_evolution.py" "classic"
        run_scenario "UI Self-Improvement" "ui_self_improvement.py" "classic"
        run_scenario "Schema Negotiation" "schema_negotiation.py" "classic"
        run_scenario "Grand Collaboration" "grand_collaboration.py" "classic"
        echo -e "✅ All classic scenarios complete!"
        ;;
    
    creative)
        check_discovery_service
        run_scenario "The Symphony" "symphony_scenario.py" "creative"
        run_scenario "The Detective" "detective_scenario.py" "creative"
        run_scenario "The Ecosystem" "ecosystem_scenario.py" "creative"
        run_scenario "The Mirror" "mirror_scenario.py" "creative"
        echo -e "✅ All creative scenarios complete!"
        ;;
    
    stress)
        check_discovery_service
        echo -e "⚠️  WARNING: Running stress tests may cause temporary issues"
        read -p "Press Enter to continue..."
        run_scenario "The Avalanche" "avalanche_scenario.py" "stress"
        run_scenario "The Contradiction" "contradiction_scenario.py" "stress"
        run_scenario "The Resource Strangler" "resource_strangler.py" "stress"
        run_scenario "The Schema Shapeshifter" "schema_shapeshifter.py" "stress"
        run_scenario "The Security Breach" "security_breach.py" "stress"
        echo -e "✅ All stress tests complete!"
        ;;
    
    everything)
        check_discovery_service
        # Classic
        run_scenario "Research Evolution" "research_evolution.py" "classic"
        run_scenario "UI Self-Improvement" "ui_self_improvement.py" "classic"
        run_scenario "Schema Negotiation" "schema_negotiation.py" "classic"
        run_scenario "Grand Collaboration" "grand_collaboration.py" "classic"
        # Creative
        run_scenario "The Symphony" "symphony_scenario.py" "creative"
        run_scenario "The Detective" "detective_scenario.py" "creative"
        run_scenario "The Ecosystem" "ecosystem_scenario.py" "creative"
        run_scenario "The Mirror" "mirror_scenario.py" "creative"
        # Stress
        echo -e "⚠️  Starting stress tests..."
        run_scenario "The Avalanche" "avalanche_scenario.py" "stress"
        run_scenario "The Contradiction" "contradiction_scenario.py" "stress"
        run_scenario "The Resource Strangler" "resource_strangler.py" "stress"
        run_scenario "The Schema Shapeshifter" "schema_shapeshifter.py" "stress"
        run_scenario "The Security Breach" "security_breach.py" "stress"
        echo -e "✅ ALL scenarios complete!"
        ;;
    
    *)
        echo -e "Unknown scenario: $SCENARIO"
        echo "Run without arguments to see available scenarios"
        exit 1
        ;;
esac

# Show reports location
if [ -d "reports" ] && [ "$(ls -A reports)" ]; then
    echo ""
    echo -e "📊 Reports generated:"
    ls -la reports/*.json reports/*.md 2>/dev/null | tail -5
fi

# Show visualizations location
if [ -d "visualizations" ] && [ "$(ls -A visualizations)" ]; then
    echo ""
    echo -e "📈 Visualizations generated:"
    ls -la visualizations/*.png 2>/dev/null | tail -5
fi
