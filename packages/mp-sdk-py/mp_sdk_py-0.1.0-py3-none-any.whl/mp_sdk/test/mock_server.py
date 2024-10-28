from __future__ import annotations
from typing import List, Dict, Optional
from pathlib import Path
import os

from ..interfaces.server_interfaces import IServerInterface
from ..models.monitor_account import MonitorAccount
from ..models.parsed_transaction import ParsedTransaction
from ..models.payout_batch import PayoutBatch
from ..models.query_result import QueryResult
from ..models.node import Node
from ..models.upload_states import UploadNodeState
from ..models.register_node_info import RegisterNodeInfo
from ..models.enums import PayoutBatchState

class MockServerInterface(IServerInterface):
    """A mock implementation of server interface for testing"""
    def __init__(self, payout_file_path: Optional[str] = None):
        self.uploaded_transactions: List[ParsedTransaction] = []
        self.payout_batches: Dict[int, PayoutBatch] = {}
        self.batch_files: Dict[int, str] = {}
        self.payout_file_path = payout_file_path
        self._next_batch_id = 1

    def heart_beat(self, node_state: UploadNodeState) -> QueryResult[Node]:
        return QueryResult.success(Node(
            node_id="test_node",
            control_state=0,
            monitor_accounts=[]
        ))

    def upload_transactions(self, gateway: str, transactions: List[ParsedTransaction]) -> QueryResult[bool]:
        self.uploaded_transactions.extend(transactions)
        return QueryResult.success(True)

    def get_new_payout_batches(self, account: MonitorAccount) -> QueryResult[List[PayoutBatch]]:
        if self.payout_file_path and os.path.exists(self.payout_file_path):
            batch = PayoutBatch(
                id=self._next_batch_id,
                file_name=Path(self.payout_file_path).name,
                order_list="",
                error_order_list="",
                state=PayoutBatchState.Ready
            )
            self.payout_batches[batch.id] = batch
            self.batch_files[batch.id] = self.payout_file_path
            self._next_batch_id += 1
            return QueryResult.success([batch])
        return QueryResult.success([])

    def get_undone_payout_batches(self, account: MonitorAccount) -> QueryResult[List[PayoutBatch]]:
        undone_batches = [
            batch for batch in self.payout_batches.values()
            if batch.state not in [PayoutBatchState.Success, PayoutBatchState.UploadError, PayoutBatchState.CheckError]
        ]
        return QueryResult.success(undone_batches)

    def update_payout_batch_state(self, batch: PayoutBatch, new_state: PayoutBatchState) -> QueryResult[bool]:
        if batch.id in self.payout_batches:
            self.payout_batches[batch.id].state = new_state
            return QueryResult.success(True)
        return QueryResult.failure(f"Batch {batch.id} not found")

    def register_node(self, node_info: RegisterNodeInfo) -> QueryResult[bool]:
        return QueryResult.success(True)

    def get_batch_file(self, batch: PayoutBatch) -> QueryResult[str]:
        """Get the file content for a payout batch"""
        if batch.id in self.batch_files:
            try:
                with open(self.batch_files[batch.id], 'r') as f:
                    content = f.read()
                return QueryResult.success(content)
            except Exception as e:
                return QueryResult.failure(f"Failed to read batch file: {str(e)}")
        return QueryResult.failure(f"No file found for batch {batch.id}")