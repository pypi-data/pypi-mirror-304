from shared_kernel.exceptions.custom_exceptions import StatusTrackerException
from shared_kernel.interfaces.databus import DataBus
from shared_kernel.messaging import DataBusFactory
from shared_kernel.registries.service_event_registry import ServiceEventRegistry

service_event_registry = ServiceEventRegistry()


class StatusTracker:
    """
    A singleton StatusTracker class that ensures only one StatusTracker instance is created.

    Attributes:
        _instance (Optional[StatusTracker]): The single instance of the StatusTracker.
    """

    _instance = None

    def __new__(cls):
        """
        override __new__ to ensure singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super(StatusTracker, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance


    def _initialize(self):
        self.databus: DataBus = DataBusFactory.create_data_bus(
            bus_type="HTTP", config={}
        )


    def create_task(self, span_id, trace_id, entity_id, task, status):
        """Publishes a synchronous event to create a task"""
        try:
            payload = {
                "span_id": span_id,
                "trace_id": trace_id,
                "entity_id": entity_id,
                "task": task,
                "status": status,
            }
            response = self.databus.request_event(
                getattr(service_event_registry, "CREATE_TASK"), payload
            )
            return response

        except Exception as e:
            raise StatusTrackerException(e)


    def update_task(self, span_id, trace_id, entity_id, task, status):
        """Publishes a synchronous event to update a task"""
        try:
            payload = {
                "span_id": span_id,
                "trace_id": trace_id,
                "entity_id": entity_id,
                "task": task,
                "status": status,
            }
            response = self.databus.request_event(
                getattr(service_event_registry, "UPDATE_TASK"), payload
            )
            return response

        except Exception as e:
            raise StatusTrackerException(e)


    def mark_task_as_failure(self, span_id, trace_id, entity_id, task, failure_reason):
        """Publishes a synchronous event to mark a task as failure"""
        try:
            payload = {
                "span_id": span_id,
                "trace_id": trace_id,
                "entity_id": entity_id,
                "task": task,
                "failure_reason": failure_reason,
            }
            response = self.databus.request_event(
                getattr(service_event_registry, "MARK_TASK_AS_FAILURE"), payload
            )
            return response

        except Exception as e:
            raise StatusTrackerException(e)
        

    def set_tracking_payload(self, span_id, trace_id, entity_id, task, tracking_payload):
        """Publishes a synchronous event to set tracking payload"""
        try:
            payload = {
                "span_id": span_id,
                "trace_id": trace_id,
                "entity_id": entity_id,
                "task": task,
                "tracking_payload": tracking_payload,
            }
            response = self.databus.request_event(
                getattr(service_event_registry, "SET_TRACKING_PAYLOAD"), payload
            )
            return response

        except Exception as e:
            raise StatusTrackerException(e)
        
    
    def get_task(self, entity_id, task):
        """Publishes a synchronous event to retrieve a task"""
        try:
            payload = {
                "entity_id": entity_id,
                "task": task,
            }
            response = self.databus.request_event(
                getattr(service_event_registry, "GET_TASK"), payload
            )
            return response

        except Exception as e:
            raise StatusTrackerException(e)
