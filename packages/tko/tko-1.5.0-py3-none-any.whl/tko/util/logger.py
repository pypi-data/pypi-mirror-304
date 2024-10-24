from __future__ import annotations
import csv
import hashlib
import datetime
from tko.settings.settings import Settings
import enum
import os

from abc import ABC, abstractmethod


class LogAction(enum.Enum):
    NONE = 'NONE'
    OPEN = 'OPEN'
    DOWN = 'DOWN'
    FREE = 'FREE' 
    TEST = 'TEST' # CORRECT|WRONG|COMPILE|RUNTIME
    SELF = 'SELF' # int
    QUIT = 'QUIT'


class ActionData:
    def __init__(self, timestamp: str, action_value: str, task: str = "", payload: str = ""):
        self.timestamp = timestamp
        self.action_value: str = action_value
        self.task_key = task
        self.payload = payload
        self.hash = ""

    def action_self_same_task(self, other: ActionData):
        if self.action_value != LogAction.SELF.value:
            return False
        if other.action_value != LogAction.SELF.value:
            return False
        return self.task_key == other.task_key

    def __str__(self):
        return f'{self.timestamp}, {self.action_value}, {self.task_key}, {self.payload}'

    @staticmethod
    def generate_hash(action_data: ActionData, last_hash: str):
        comprimento = 6
        input_str = str(action_data) + last_hash
        hash_completo = hashlib.sha256(input_str.encode()).hexdigest()
        return hash_completo[:comprimento]  # Retorna os primeiros 'comprimento' caracteres do hash

class LoggerStore(ABC):
    @abstractmethod
    def push_to_file(self, action_data: ActionData, last_hash: str):
        pass

    @abstractmethod
    def set_log_file(self, path: str):
        pass

    @abstractmethod
    def get_log_file(self) -> str | None:
        pass

    @abstractmethod
    def get_action_entries(self) -> list[ActionData]:
        pass

    @abstractmethod
    def get_last_hash(self) -> str:
        pass

class LoggerFS(LoggerStore):

    def __init__(self, settings: Settings):
        self.log_file: str | None = None
        self.settings = settings
    
    def set_log_file(self, log_file: str):
        self.log_file = log_file
        return self
    
    def get_log_file(self) -> str | None:
        return self.log_file
    
    def row_to_action_data(self, row: list[str]) -> ActionData:
        hash = row[0]
        timestamp = row[1]
        action_value = row[2]
        task = row[3]
        payload = row[4]
        action_data = ActionData(timestamp, action_value, task, payload)
        action_data.hash = hash
        return action_data

    def push_to_file(self, action_data: ActionData, last_hash: str):
        log_file = self.get_log_file()
        if log_file is None:
            return
        action_data.hash = ActionData.generate_hash(action_data, last_hash)
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        with open(log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            ad = action_data
            writer.writerow([ad.hash, ad.timestamp, ad.action_value, ad.task_key, ad.payload])
            return ad.hash

    def get_action_entries(self) -> list[ActionData]:
        log_file = self.get_log_file()
        if log_file is None:
            return []
        if not os.path.exists(log_file):
            return []
        with open(log_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            return [self.row_to_action_data(row) for row in rows]

    def get_last_hash(self) -> str:
        return self.get_action_entries()[-1].hash if len(self.get_action_entries()) > 0 else ""

class LoggerMemory(LoggerStore):
    def __init__(self):
        self.entries: list[ActionData] = []

    def set_log_file(self, path: str):
        return self
    
    def get_log_file(self) -> str | None:
        return None

    def push_to_file(self, action_data: ActionData, last_hash: str):
        action_data.hash = ActionData.generate_hash(action_data, last_hash)
        self.entries.append(action_data)
        return action_data.hash

    def get_action_entries(self) -> list[ActionData]:
        return self.entries

    def get_last_hash(self) -> str:
        return self.entries[-1].hash if len(self.entries) > 0 else ""

class Logger:
    instance: None | Logger = None
    COMP_ERROR = "COMP"
    FREE_EXEC = "FREE"

    @staticmethod
    def get_instance() -> Logger:
        if Logger.instance is None:
            raise Exception("Logger not initialized")
        return Logger.instance

    def __init__(self, logger_store: LoggerStore):
        self.last_hash: str | None = None
        self.cached_action: ActionData | None = None
        self.fs = logger_store

    def set_log_file(self, log_file: str):
        self.fs.set_log_file(log_file)
        return self

    def check_log_file_integrity(self) -> list[str]:
        entries = self.fs.get_action_entries()
        if len(entries) == 0:
            return []
        hash = entries[0].hash
        output: list[str] = []

        for i in range(1, len(entries)):
            calculated_hash = ActionData.generate_hash(entries[i], hash)
            if calculated_hash != entries[i].hash:
                output.append(f"Hash mismatch line {i + 1}: {str(entries[i])}")
            hash = calculated_hash
        return output

    def store_in_cached(self, action_data: ActionData) -> bool:
        if self.cached_action is None and action_data.action_value == LogAction.SELF.value:
            return True
        if self.cached_action is not None and self.cached_action.action_self_same_task(action_data):
            return True
        return False

    def record_compilation_error(self, task_key: str):
        self.record_other_event(LogAction.TEST, task_key, self.COMP_ERROR)
    
    def record_test_result(self, task_key: str, result: int):
        self.record_other_event(LogAction.TEST, task_key, str(result) + "%")

    def record_freerun(self, task_key: str):
        self.record_other_event(LogAction.FREE, task_key)

    def record_other_event(self, action: LogAction, task_key: str = "", payload: str = ""):
        action_data = ActionData(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), action.value, task_key, payload)
        self.record_action_data(action_data)

    def get_last_hash(self) -> str:
        if self.last_hash is None:
            self.last_hash = self.fs.get_last_hash()
        return self.last_hash

    def record_action_data(self, action_data: ActionData):
        if self.store_in_cached(action_data):
            self.cached_action = action_data
            return
        
        if self.cached_action is not None:
            self.last_hash = self.fs.push_to_file(self.cached_action, self.get_last_hash())
            self.cached_action = None
        
        if self.store_in_cached(action_data):
            self.cached_action = action_data
        else:
            self.last_hash = self.fs.push_to_file(action_data, self.get_last_hash())
