from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.query_result import QueryResult
from ..models.node import Node
from ..models.parsed_transaction import ParsedTransaction
from ..models.payout_batch import PayoutBatch
from ..models.register_node_info import RegisterNodeInfo
from ..models.upload_states import UploadNodeState
from ..models.enums import PayoutBatchState
from ..models.monitor_account import MonitorAccount

class IServerInterface(ABC):
    """服务器通信接口的抽象基类"""

    @abstractmethod
    def heart_beat(self, node_state: UploadNodeState) -> QueryResult[Node]:
        """节点心跳接口"""
        pass

    @abstractmethod
    def upload_transactions(self, gateway: str, transactions: List[ParsedTransaction]) -> QueryResult[bool]:
        """上传交易接口"""
        pass

    @abstractmethod
    def get_new_payout_batches(self, account: MonitorAccount) -> QueryResult[List[PayoutBatch]]:
        """获取新支付批次接口"""
        pass

    @abstractmethod
    def get_undone_payout_batches(self, account: MonitorAccount) -> QueryResult[List[PayoutBatch]]:
        """获取未完成支付批次接口"""
        pass

    @abstractmethod
    def update_payout_batch_state(self, batch: PayoutBatch, new_state: PayoutBatchState) -> QueryResult[bool]:
        """更新支付批次状态接口"""
        pass

    @abstractmethod
    def register_node(self, node_info: RegisterNodeInfo) -> QueryResult[bool]:
        """注册节点接口"""
        pass
