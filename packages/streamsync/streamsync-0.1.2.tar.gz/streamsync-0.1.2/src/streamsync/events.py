import io
import traceback
from contextlib import redirect_stdout
from streamsync.types import StreamsyncEvent
from streamsync.core import Evaluator, EventDeserialiser, StreamsyncState
from streamsync.sessions import StreamsyncSession
import streamsync
import streamsyncuserapp
import logging

# class EventHandler:
#     def __init__(self, session: StreamsyncSession):
#         self.session = session 
#         self.session_state = session.session_state
#         self.deser = EventDeserialiser(self.session_state)
#         self.evaluator = Evaluator(self.session_state)

#     def _handle_binding(self, event_type, target_component, payload):
#         if not target_component.binding:
#             return
#         binding = target_component.binding
#         if binding["eventType"] != event_type:
#             return
#         self.evaluator.set_state(binding["stateRef"], payload)

#     def _call_handler_callable(self, event_type, target_component, instance_path, payload):
#         if not target_component.handlers:
#             return
#         handler = target_component.handlers.get(event_type)
#         if not handler:
#             return

#         if not hasattr(streamsyncuserapp, handler):
#             raise ValueError(
#                 f"""Invalid handler. Couldn't find the handler "{ handler }".""")
#         callable_handler = getattr(streamsyncuserapp, handler)

#         if not callable(callable_handler):
#             raise ValueError(
#                 "Invalid handler. The handler isn't a callable object.")

#         arg_names = callable_handler.__code__.co_varnames
#         args = []
#         for arg_name in arg_names:
#             if arg_name == "state":
#                 args.append(self.session_state)
#             elif arg_name == "payload":
#                 args.append(payload)
#             elif arg_name == "context":
#                 context = self.evaluator.get_context_data(instance_path)
#                 args.append(context)
#             elif arg_name == "session":
#                 context = self.evaluator.get_context_data(instance_path)
#                 args.append(context)

#         result = None
#         with redirect_stdout(io.StringIO()) as f:
#             result = callable_handler(*args)
#         captured_stdout = f.getvalue()
#         if captured_stdout:
#             self.session_state.add_log_entry(
#                 "info",
#                 "Stdout message",
#                 captured_stdout
#             )
#         return result

#     def handle(self, ev: StreamsyncEvent):
#         event_type = ev["type"]
#         ok = True

#         try:
#             self.deser.transform(ev)
#         except BaseException:
#             ok = False
#             self.session_state.add_notification(
#                 "error", "Error", f"A deserialisation error occurred when handling event '{ event_type }'.")
#             self.session_state.add_log_entry("error", "Deserialisation Failed",
#                                              f"The data sent might be corrupt. A runtime exception was raised when deserialising event '{ event_type }'.", traceback.format_exc())
            
#         result = None
#         try:
#             event_type = ev["type"]
#             instance_path = ev["instancePath"]
#             target_id = instance_path[-1]["componentId"]
#             target_component = streamsync.component_manager.components[target_id]
#             payload = ev.get("payload")

#             self._handle_binding(event_type, target_component, payload)
#             result = self._call_handler_callable(event_type, target_component, instance_path, payload)
#         except BaseException:
#             ok = False
#             self.session_state.add_notification("error", "Runtime Error", f"An error occurred when processing event '{ event_type }'.",
#                                                 )
#             self.session_state.add_log_entry("error", "Runtime Exception",
#                                              f"A runtime exception was raised when processing event '{ event_type }'.", traceback.format_exc())

#         return {"ok": ok, "result": result}
