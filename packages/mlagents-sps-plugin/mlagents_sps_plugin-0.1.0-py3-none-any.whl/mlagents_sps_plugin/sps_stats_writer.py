# mlagents_sps_plugin/sps_stats_writer.py

from typing import List, Dict, NamedTuple, Any, Optional
import time
import os
from mlagents.trainers.stats import StatsWriter, StatsSummary, StatsAggregationMethod, ConsoleWriter, StatsReporter
from mlagents.trainers.settings import RunOptions
from mlagents.trainers.stats import TensorboardWriter
from mlagents_envs.logging_util import get_logger

logger = get_logger(__name__)

class SPSStatsWriter(StatsWriter):
    def __init__(
        self,
        run_options: RunOptions,
    ):  
        self.step_count = None  # Set to None to detect the first call
        self.last_log_time = time.time()
        # Get the Tensorboard writer from StatsReporter
        self.tensorboard_writer = None
    
    def write_stats(
        self, category: str, values: Dict[str, StatsSummary], step: int
    ) -> None:
        """
        Calculate and log Steps Per Second (SPS) to TensorBoard and console.
        """
        current_time = time.time()

        # Detect first call and initialize step count and log time
        if self.step_count is None:
            self.step_count = step
            self.last_log_time = current_time
            return  # Skip logging for the first call

        # Calculate elapsed time and steps
        elapsed_time = current_time - self.last_log_time
        steps_since_last_log = step - self.step_count

        if steps_since_last_log > 0 and elapsed_time >= 10.0:
            sps = steps_since_last_log / elapsed_time
            
            if self.tensorboard_writer is None:
                self.tensorboard_writer = next(writer for writer in StatsReporter.writers if isinstance(writer, TensorboardWriter))
            self.tensorboard_writer.write_stats(category, {"Steps Per Second": StatsSummary(sps, StatsAggregationMethod.AVERAGE)}, step)
            
            logger.info(f"{category}. Steps Per Second: {sps:.2f}.")

            # Reset counters for next interval
            self.step_count = step
            self.last_log_time = current_time
            

def get_sps_stats_writer(run_options: RunOptions):
    """
    Plugin registration function to initialize and return SPSStatsWriter.
    """
    return [SPSStatsWriter(run_options)]