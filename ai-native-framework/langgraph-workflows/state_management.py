#!/usr/bin/env python3
"""
LangGraph State Management Engine
=================================

Advanced state management for complex workflows with persistence,
recovery, and distributed state coordination.

Author: Enterprise AI Platform Team
Version: 2.0.0
Date: September 2025
"""

import asyncio
import json
import pickle
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, TypedDict, Type
from dataclasses import dataclass, asdict
from pathlib import Path
from contextlib import asynccontextmanager
import hashlib

# State management imports with fallbacks
try:
    from langgraph.checkpoint.base import BaseCheckpointSaver
    from langgraph.checkpoint.sqlite import SqliteSaver
    LANGGRAPH_CHECKPOINT_AVAILABLE = True
except ImportError:
    LANGGRAPH_CHECKPOINT_AVAILABLE = False
    logging.warning("LangGraph checkpoint modules not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StateType(TypedDict):
    """Base state type for all workflows"""
    workflow_id: str
    execution_id: str
    current_step: str
    status: str
    created_at: str
    updated_at: str
    metadata: Dict[str, Any]

@dataclass
class StateSnapshot:
    """Immutable state snapshot"""
    workflow_id: str
    execution_id: str
    step_name: str
    state_data: Dict[str, Any]
    timestamp: datetime
    checksum: str
    parent_snapshot_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """Calculate state checksum for integrity verification"""
        state_str = json.dumps(self.state_data, sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "workflow_id": self.workflow_id,
            "execution_id": self.execution_id,
            "step_name": self.step_name,
            "state_data": self.state_data,
            "timestamp": self.timestamp.isoformat(),
            "checksum": self.checksum,
            "parent_snapshot_id": self.parent_snapshot_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StateSnapshot':
        """Create from dictionary"""
        return cls(
            workflow_id=data["workflow_id"],
            execution_id=data["execution_id"],
            step_name=data["step_name"],
            state_data=data["state_data"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            checksum=data["checksum"],
            parent_snapshot_id=data.get("parent_snapshot_id")
        )

class StateTransition:
    """Represents a state transition"""
    
    def __init__(self, from_step: str, to_step: str, condition: str = None, 
                 metadata: Dict[str, Any] = None):
        self.from_step = from_step
        self.to_step = to_step
        self.condition = condition
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_step": self.from_step,
            "to_step": self.to_step,
            "condition": self.condition,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }

class StateManager:
    """Advanced state management for LangGraph workflows"""
    
    def __init__(self, database_path: str = "state_management.db",
                 enable_compression: bool = True,
                 max_snapshots: int = 1000):
        self.database_path = database_path
        self.enable_compression = enable_compression
        self.max_snapshots = max_snapshots
        self.active_states = {}  # In-memory cache
        self.state_history = {}  # Execution history
        self.transition_log = []  # State transition log
        
        self._initialize_database()
        self._load_active_states()
        
        logger.info(f"StateManager initialized with database: {database_path}")
    
    def _initialize_database(self):
        """Initialize SQLite database for state persistence"""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS state_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id TEXT NOT NULL,
                    execution_id TEXT NOT NULL,
                    step_name TEXT NOT NULL,
                    state_data TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    checksum TEXT NOT NULL,
                    parent_snapshot_id TEXT,
                    compressed BOOLEAN DEFAULT FALSE,
                    INDEX(workflow_id),
                    INDEX(execution_id),
                    INDEX(timestamp)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS state_transitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT NOT NULL,
                    from_step TEXT NOT NULL,
                    to_step TEXT NOT NULL,
                    condition TEXT,
                    metadata TEXT,
                    timestamp TEXT NOT NULL,
                    INDEX(execution_id),
                    INDEX(timestamp)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workflow_metadata (
                    workflow_id TEXT PRIMARY KEY,
                    execution_count INTEGER DEFAULT 0,
                    last_execution TEXT,
                    total_snapshots INTEGER DEFAULT 0,
                    metadata TEXT
                )
            """)
            
            conn.commit()
    
    def _load_active_states(self):
        """Load active states from database"""
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT DISTINCT workflow_id, execution_id 
                FROM state_snapshots 
                WHERE timestamp > datetime('now', '-1 day')
                ORDER BY timestamp DESC
            """)
            
            for workflow_id, execution_id in cursor.fetchall():
                try:
                    latest_state = self.get_latest_state(execution_id)
                    if latest_state:
                        self.active_states[execution_id] = latest_state
                except Exception as e:
                    logger.warning(f"Failed to load state for {execution_id}: {e}")
    
    async def save_state(self, snapshot: StateSnapshot) -> str:
        """Save state snapshot to persistent storage"""
        snapshot_id = f"{snapshot.execution_id}_{snapshot.step_name}_{int(datetime.now().timestamp())}"
        
        try:
            # Serialize state data
            state_json = json.dumps(snapshot.state_data)
            
            # Compress if enabled and data is large
            if self.enable_compression and len(state_json) > 1024:
                state_data = self._compress_data(state_json)
                compressed = True
            else:
                state_data = state_json
                compressed = False
            
            # Save to database
            with sqlite3.connect(self.database_path) as conn:
                conn.execute("""
                    INSERT INTO state_snapshots 
                    (workflow_id, execution_id, step_name, state_data, timestamp, 
                     checksum, parent_snapshot_id, compressed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    snapshot.workflow_id,
                    snapshot.execution_id,
                    snapshot.step_name,
                    state_data,
                    snapshot.timestamp.isoformat(),
                    snapshot.checksum,
                    snapshot.parent_snapshot_id,
                    compressed
                ))
                conn.commit()
            
            # Update in-memory cache
            self.active_states[snapshot.execution_id] = snapshot
            
            # Update workflow metadata
            await self._update_workflow_metadata(snapshot.workflow_id)
            
            logger.debug(f"State snapshot saved: {snapshot_id}")
            return snapshot_id
            
        except Exception as e:
            logger.error(f"Failed to save state snapshot: {e}")
            raise
    
    def get_latest_state(self, execution_id: str) -> Optional[StateSnapshot]:
        """Get the latest state for an execution"""
        # Check in-memory cache first
        if execution_id in self.active_states:
            return self.active_states[execution_id]
        
        # Query database
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT workflow_id, execution_id, step_name, state_data, 
                       timestamp, checksum, parent_snapshot_id, compressed
                FROM state_snapshots 
                WHERE execution_id = ?
                ORDER BY timestamp DESC 
                LIMIT 1
            """, (execution_id,))
            
            row = cursor.fetchone()
            if row:
                workflow_id, exec_id, step_name, state_data, timestamp, checksum, parent_id, compressed = row
                
                # Decompress if needed
                if compressed:
                    state_json = self._decompress_data(state_data)
                else:
                    state_json = state_data
                
                state_dict = json.loads(state_json)
                
                snapshot = StateSnapshot(
                    workflow_id=workflow_id,
                    execution_id=exec_id,
                    step_name=step_name,
                    state_data=state_dict,
                    timestamp=datetime.fromisoformat(timestamp),
                    checksum=checksum,
                    parent_snapshot_id=parent_id
                )
                
                # Cache for future access
                self.active_states[execution_id] = snapshot
                return snapshot
        
        return None
    
    def get_state_history(self, execution_id: str, limit: int = 50) -> List[StateSnapshot]:
        """Get state history for an execution"""
        snapshots = []
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT workflow_id, execution_id, step_name, state_data, 
                       timestamp, checksum, parent_snapshot_id, compressed
                FROM state_snapshots 
                WHERE execution_id = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (execution_id, limit))
            
            for row in cursor.fetchall():
                workflow_id, exec_id, step_name, state_data, timestamp, checksum, parent_id, compressed = row
                
                # Decompress if needed
                if compressed:
                    state_json = self._decompress_data(state_data)
                else:
                    state_json = state_data
                
                state_dict = json.loads(state_json)
                
                snapshot = StateSnapshot(
                    workflow_id=workflow_id,
                    execution_id=exec_id,
                    step_name=step_name,
                    state_data=state_dict,
                    timestamp=datetime.fromisoformat(timestamp),
                    checksum=checksum,
                    parent_snapshot_id=parent_id
                )
                
                snapshots.append(snapshot)
        
        return snapshots
    
    async def restore_state(self, execution_id: str, step_name: str = None) -> Optional[StateSnapshot]:
        """Restore state to a specific step or latest"""
        if step_name:
            # Restore to specific step
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute("""
                    SELECT workflow_id, execution_id, step_name, state_data, 
                           timestamp, checksum, parent_snapshot_id, compressed
                    FROM state_snapshots 
                    WHERE execution_id = ? AND step_name = ?
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """, (execution_id, step_name))
                
                row = cursor.fetchone()
                if row:
                    workflow_id, exec_id, step_name, state_data, timestamp, checksum, parent_id, compressed = row
                    
                    if compressed:
                        state_json = self._decompress_data(state_data)
                    else:
                        state_json = state_data
                    
                    state_dict = json.loads(state_json)
                    
                    snapshot = StateSnapshot(
                        workflow_id=workflow_id,
                        execution_id=exec_id,
                        step_name=step_name,
                        state_data=state_dict,
                        timestamp=datetime.fromisoformat(timestamp),
                        checksum=checksum,
                        parent_snapshot_id=parent_id
                    )
                    
                    # Update active state
                    self.active_states[execution_id] = snapshot
                    return snapshot
        else:
            # Restore to latest
            return self.get_latest_state(execution_id)
        
        return None
    
    async def log_transition(self, execution_id: str, transition: StateTransition):
        """Log a state transition"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                conn.execute("""
                    INSERT INTO state_transitions 
                    (execution_id, from_step, to_step, condition, metadata, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    execution_id,
                    transition.from_step,
                    transition.to_step,
                    transition.condition,
                    json.dumps(transition.metadata),
                    transition.timestamp.isoformat()
                ))
                conn.commit()
            
            # Add to in-memory log
            self.transition_log.append((execution_id, transition))
            
            logger.debug(f"Transition logged: {transition.from_step} -> {transition.to_step}")
            
        except Exception as e:
            logger.error(f"Failed to log transition: {e}")
    
    def get_transition_history(self, execution_id: str) -> List[StateTransition]:
        """Get transition history for an execution"""
        transitions = []
        
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute("""
                SELECT from_step, to_step, condition, metadata, timestamp
                FROM state_transitions 
                WHERE execution_id = ?
                ORDER BY timestamp ASC
            """, (execution_id,))
            
            for row in cursor.fetchall():
                from_step, to_step, condition, metadata_json, timestamp = row
                metadata = json.loads(metadata_json) if metadata_json else {}
                
                transition = StateTransition(
                    from_step=from_step,
                    to_step=to_step,
                    condition=condition,
                    metadata=metadata
                )
                transition.timestamp = datetime.fromisoformat(timestamp)
                transitions.append(transition)
        
        return transitions
    
    async def cleanup_old_states(self, retention_days: int = 7):
        """Clean up old state snapshots"""
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        with sqlite3.connect(self.database_path) as conn:
            # Count snapshots to be deleted
            cursor = conn.execute("""
                SELECT COUNT(*) FROM state_snapshots 
                WHERE timestamp < ?
            """, (cutoff_date.isoformat(),))
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Delete old snapshots
                conn.execute("""
                    DELETE FROM state_snapshots 
                    WHERE timestamp < ?
                """, (cutoff_date.isoformat(),))
                
                # Delete old transitions
                conn.execute("""
                    DELETE FROM state_transitions 
                    WHERE timestamp < ?
                """, (cutoff_date.isoformat(),))
                
                conn.commit()
                logger.info(f"Cleaned up {count} old state snapshots")
        
        # Clean up in-memory cache
        expired_executions = []
        for execution_id, snapshot in self.active_states.items():
            if snapshot.timestamp < cutoff_date:
                expired_executions.append(execution_id)
        
        for execution_id in expired_executions:
            del self.active_states[execution_id]
    
    async def _update_workflow_metadata(self, workflow_id: str):
        """Update workflow metadata"""
        with sqlite3.connect(self.database_path) as conn:
            # Get current counts
            cursor = conn.execute("""
                SELECT COUNT(DISTINCT execution_id) as exec_count,
                       COUNT(*) as snapshot_count,
                       MAX(timestamp) as last_execution
                FROM state_snapshots 
                WHERE workflow_id = ?
            """, (workflow_id,))
            
            row = cursor.fetchone()
            if row:
                exec_count, snapshot_count, last_execution = row
                
                conn.execute("""
                    INSERT OR REPLACE INTO workflow_metadata 
                    (workflow_id, execution_count, last_execution, total_snapshots)
                    VALUES (?, ?, ?, ?)
                """, (workflow_id, exec_count, last_execution, snapshot_count))
                conn.commit()
    
    def _compress_data(self, data: str) -> bytes:
        """Compress state data"""
        import gzip
        return gzip.compress(data.encode('utf-8'))
    
    def _decompress_data(self, data: bytes) -> str:
        """Decompress state data"""
        import gzip
        return gzip.decompress(data).decode('utf-8')
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get state management statistics"""
        stats = {
            "active_states": len(self.active_states),
            "total_snapshots": 0,
            "total_workflows": 0,
            "total_executions": 0,
            "database_size": 0
        }
        
        try:
            # Get database size
            db_path = Path(self.database_path)
            if db_path.exists():
                stats["database_size"] = db_path.stat().st_size
            
            with sqlite3.connect(self.database_path) as conn:
                # Total snapshots
                cursor = conn.execute("SELECT COUNT(*) FROM state_snapshots")
                stats["total_snapshots"] = cursor.fetchone()[0]
                
                # Total workflows
                cursor = conn.execute("SELECT COUNT(DISTINCT workflow_id) FROM state_snapshots")
                stats["total_workflows"] = cursor.fetchone()[0]
                
                # Total executions
                cursor = conn.execute("SELECT COUNT(DISTINCT execution_id) FROM state_snapshots")
                stats["total_executions"] = cursor.fetchone()[0]
                
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        
        return stats

class DistributedStateManager(StateManager):
    """Distributed state manager for multi-node deployments"""
    
    def __init__(self, node_id: str, database_path: str = "distributed_state.db",
                 sync_interval: int = 30):
        self.node_id = node_id
        self.sync_interval = sync_interval
        self.peer_nodes = {}
        self.last_sync = datetime.now()
        
        super().__init__(database_path)
        self._start_sync_task()
    
    def _start_sync_task(self):
        """Start background sync task"""
        asyncio.create_task(self._sync_loop())
    
    async def _sync_loop(self):
        """Background synchronization loop"""
        while True:
            try:
                await asyncio.sleep(self.sync_interval)
                await self._sync_with_peers()
            except Exception as e:
                logger.error(f"Sync error: {e}")
    
    async def _sync_with_peers(self):
        """Synchronize state with peer nodes"""
        # Implementation would depend on the distributed architecture
        # This is a placeholder for distributed sync logic
        logger.debug(f"Syncing state from node {self.node_id}")
        self.last_sync = datetime.now()

# Example usage and testing
async def main():
    """Demonstrate state management capabilities"""
    print("🗄️ LangGraph State Management Demo")
    print("=" * 40)
    
    # Initialize state manager
    state_manager = StateManager("demo_state.db")
    
    # Create sample workflow state
    initial_state = {
        "workflow_id": "demo_workflow",
        "execution_id": "exec_001",
        "current_step": "initialize",
        "status": "running",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "metadata": {
            "user_id": "user123",
            "priority": "high",
            "project": "demo_project"
        },
        "data": {
            "input_value": 42,
            "processed_count": 0,
            "results": []
        }
    }
    
    # Create initial snapshot
    snapshot1 = StateSnapshot(
        workflow_id="demo_workflow",
        execution_id="exec_001",
        step_name="initialize",
        state_data=initial_state,
        timestamp=datetime.now(),
        checksum=""
    )
    
    # Save initial state
    snapshot_id = await state_manager.save_state(snapshot1)
    print(f"✅ Initial state saved: {snapshot_id}")
    
    # Simulate state progression
    steps = ["validate_input", "process_data", "generate_results", "finalize"]
    
    for i, step in enumerate(steps):
        # Update state
        updated_state = initial_state.copy()
        updated_state["current_step"] = step
        updated_state["updated_at"] = datetime.now().isoformat()
        updated_state["data"]["processed_count"] = i + 1
        updated_state["data"]["results"].append(f"result_{i+1}")
        
        # Create snapshot
        snapshot = StateSnapshot(
            workflow_id="demo_workflow",
            execution_id="exec_001",
            step_name=step,
            state_data=updated_state,
            timestamp=datetime.now(),
            checksum="",
            parent_snapshot_id=snapshot_id
        )
        
        # Save state
        snapshot_id = await state_manager.save_state(snapshot)
        
        # Log transition
        if i > 0:
            transition = StateTransition(
                from_step=steps[i-1],
                to_step=step,
                condition=f"step_{i}_complete",
                metadata={"processing_time": 0.5}
            )
            await state_manager.log_transition("exec_001", transition)
        
        print(f"✅ State saved for step: {step}")
        
        # Small delay to simulate processing
        await asyncio.sleep(0.1)
    
    # Demonstrate state retrieval
    print(f"\n📊 State Management Results:")
    
    # Get latest state
    latest_state = state_manager.get_latest_state("exec_001")
    if latest_state:
        print(f"📍 Latest Step: {latest_state.step_name}")
        print(f"📈 Processed Count: {latest_state.state_data['data']['processed_count']}")
    
    # Get state history
    history = state_manager.get_state_history("exec_001")
    print(f"📚 Total Snapshots: {len(history)}")
    
    # Get transition history
    transitions = state_manager.get_transition_history("exec_001")
    print(f"🔄 Total Transitions: {len(transitions)}")
    
    # Get statistics
    stats = state_manager.get_statistics()
    print(f"\n📈 Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Demonstrate state restoration
    print(f"\n🔄 Demonstrating State Restoration:")
    restored_state = await state_manager.restore_state("exec_001", "process_data")
    if restored_state:
        print(f"✅ Restored to step: {restored_state.step_name}")
        print(f"📊 Restored processed count: {restored_state.state_data['data']['processed_count']}")

if __name__ == "__main__":
    asyncio.run(main())
