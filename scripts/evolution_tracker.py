"""
Evolution Tracker - Watch AI Self-Evolution in Real-Time

This script allows users to observe the AI platform's self-evolution process:
- Real-time evolution metrics
- Performance improvement tracking  
- Hypothesis generation monitoring
- Success/failure pattern analysis
- Visual evolution progress

Run this to see the future of AI - systems that improve themselves!
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import logging

class EvolutionTracker:
    """Track and display AI self-evolution in real-time"""
    
    def __init__(self, platform_path: str = "."):
        self.platform_path = Path(platform_path)
        self.evolution_log_path = self.platform_path / "logs" / "evolution.jsonl"
        self.logger = logging.getLogger("evolution_tracker")
        
    async def start_tracking(self):
        """Start real-time evolution tracking"""
        print("🔮 Evolution Tracker Started - Watching AI Self-Improvement")
        print("=" * 70)
        print("")
        
        # Initialize tracking state
        last_log_size = 0
        evolution_count = 0
        start_time = datetime.now()
        
        while True:
            try:
                # Check for new evolution events
                new_events = await self._check_for_new_evolution_events(last_log_size)
                
                if new_events:
                    evolution_count += len(new_events)
                    for event in new_events:
                        await self._display_evolution_event(event, evolution_count)
                    
                    # Update tracking state
                    if self.evolution_log_path.exists():
                        last_log_size = self.evolution_log_path.stat().st_size
                
                # Display periodic status
                await self._display_status_update(start_time, evolution_count)
                
                # Check every 10 seconds
                await asyncio.sleep(10)
                
            except KeyboardInterrupt:
                print("\n🛑 Evolution tracking stopped by user")
                await self._display_final_summary(start_time, evolution_count)
                break
            except Exception as e:
                print(f"❌ Tracking error: {e}")
                await asyncio.sleep(30)
    
    async def _check_for_new_evolution_events(self, last_size: int) -> List[Dict]:
        """Check for new evolution events since last check"""
        events = []
        
        if not self.evolution_log_path.exists():
            return events
        
        current_size = self.evolution_log_path.stat().st_size
        if current_size <= last_size:
            return events
        
        try:
            with open(self.evolution_log_path, "r") as f:
                # Skip to last position
                f.seek(last_size)
                
                # Read new lines
                for line in f:
                    if line.strip():
                        events.append(json.loads(line.strip()))
        
        except Exception as e:
            self.logger.error(f"Failed to read evolution log: {e}")
        
        return events
    
    async def _display_evolution_event(self, event: Dict, event_number: int):
        """Display a single evolution event"""
        timestamp = datetime.fromisoformat(event["timestamp"])
        time_str = timestamp.strftime("%H:%M:%S")
        
        print(f"🧬 Evolution Event #{event_number} [{time_str}]")
        print(f"   📊 Hypothesis: {event['hypothesis_id']}")
        print(f"   {'✅' if event['success'] else '❌'} Success: {event['success']}")
        print(f"   📈 Improvement: {event['improvement']:.1f}%")
        
        if event['success']:
            print(f"   🎉 The AI successfully improved itself!")
        else:
            print(f"   📚 The AI learned from this attempt")
        
        print("")
    
    async def _display_status_update(self, start_time: datetime, evolution_count: int):
        """Display periodic status updates"""
        runtime = datetime.now() - start_time
        runtime_str = str(runtime).split('.')[0]  # Remove microseconds
        
        # Check if we should show status (every minute)
        if int(time.time()) % 60 == 0:
            print(f"⏱️  Runtime: {runtime_str} | Evolution Attempts: {evolution_count}")
            
            # Show evolution summary if available
            summary_path = self.platform_path / "logs" / "evolution_summary.json"
            if summary_path.exists():
                try:
                    with open(summary_path) as f:
                        summary = json.load(f)
                    
                    success_rate = summary.get("evolution_success_rate", 0)
                    print(f"📊 Current Success Rate: {success_rate:.1f}%")
                    
                except Exception:
                    pass
            
            print("")
    
    async def _display_final_summary(self, start_time: datetime, evolution_count: int):
        """Display final tracking summary"""
        runtime = datetime.now() - start_time
        print("\n" + "=" * 70)
        print("🔬 EVOLUTION TRACKING SUMMARY")
        print("=" * 70)
        print(f"📅 Tracking Duration: {str(runtime).split('.')[0]}")
        print(f"🧬 Evolution Events Observed: {evolution_count}")
        
        # Load final summary if available
        summary_path = self.platform_path / "logs" / "evolution_summary.json"
        if summary_path.exists():
            try:
                with open(summary_path) as f:
                    summary = json.load(f)
                
                print(f"📊 Final Success Rate: {summary.get('evolution_success_rate', 0):.1f}%")
                print(f"🎯 Total Hypotheses Generated: {summary.get('hypotheses_generated', 0)}")
                print(f"📈 Performance Metrics Collected: {summary.get('performance_metrics_collected', 0)}")
                
            except Exception:
                pass
        
        print("\n🌟 Thank you for watching the future of AI - systems that evolve themselves!")

async def main():
    """Main function to start evolution tracking"""
    print("🚀 AI Self-Evolution Tracker")
    print("👀 Watch as the AI platform improves itself in real-time")
    print("")
    print("🔍 What you'll see:")
    print("   • Real-time self-improvement attempts")
    print("   • Performance optimization experiments") 
    print("   • Success/failure learning patterns")
    print("   • Autonomous architecture evolution")
    print("")
    print("⚡ Starting tracking... Press Ctrl+C to stop")
    print("")
    
    # Configure logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise
    
    # Start tracking
    tracker = EvolutionTracker()
    await tracker.start_tracking()

if __name__ == "__main__":
    asyncio.run(main())
