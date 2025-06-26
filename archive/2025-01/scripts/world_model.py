"""World Model compatibility wrapper"""
import sys
sys.path.insert(0, "/home/graham/workspace/experiments/world_model/src")

try:
    from world_model import WorldModel, SystemState
except ImportError:
    # Create minimal functionality if import fails
    class SystemState:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class WorldModel:
        def __init__(self):
            self.states = {}
            self.state_counter = 0
        
        def update_state(self, state):
            if not state:
                raise ValueError("Empty state not allowed")
            self.state_counter += 1
            return {"id": f"state_{self.state_counter}", "status": "tracked"}
        
        def process_request(self, request):
            """Handle state tracker interaction"""
            action = request.get("action", "")
            
            if action == "update_state":
                return self.update_state(request.get("event", {}))
            elif action == "predict_next_state":
                return {"horizon": request.get("horizon", 5), "predictions": []}
            elif action == "get_state_history":
                return {"states": list(self.states.values())[:request.get("limit", 10)]}
            
            return {"status": "unknown_action"}

__all__ = ["WorldModel", "SystemState"]
