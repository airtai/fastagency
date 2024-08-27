import queue
import threading
import os
from  queue import Queue
from autogen import ConversableAgent, UserProxyAgent
from autogen.io.base import IOStream
from typing import Any

class Question:
    def __init__(self, question):
        self.question = question

    def __str__(self):
        return self.question

    def __repr__(self):
        return self.question


class InProcessIOStream(IOStream):
    def __init__(
        self
    ) -> None:
        """Initialize the IO class."""
        self._in_queue: Queue = Queue()  # type: ignore[type-arg]
        self._out_queue: Queue = Queue()  # type: ignore[type-arg]

    def print(
        self, *objects: Any, sep: str = " ", end: str = "\n", flush: bool = False
    ) -> None:
        r"""Print data to the output stream.

        Args:
            objects (any): The data to print.
            sep (str, optional): The separator between objects. Defaults to " ".
            end (str, optional): The end of the output. Defaults to "\n".
            flush (bool, optional): Whether to flush the output. Defaults to False.
        """
        xs = sep.join(map(str, objects)) + end
        print("stavljam u out queue", xs)
        self._out_queue.put(xs)

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        """Read a line from the input stream.

        Args:
            prompt (str, optional): The prompt to display. Defaults to "".
            password (bool, optional): Whether to read a password. Defaults to False.

        Returns:
            str: The line read from the input stream.

        """
        self._out_queue.put(Question(prompt))
        print ("waiting for in queue")
        answer =  self._in_queue.get()
        print (f'got the answer {answer}|')
        return answer


    def provide_input(self, input: str):
        print("provide_input")
        self._in_queue.put(input)
        print("provide_input done")

    def responseIsOver(self):
        self._out_queue.put("--game-over--")

    def getResponsesStream(self):
        def responsesGenerator():
            while True:
                try:
                    value = self._out_queue.get()
                    if value == "--game-over--":
                        break
                    # Question shold also end the generator
                    if isinstance(value, Question):
                        yield value
                        break
                    yield value
                except queue.Empty:
                    break
        return responsesGenerator


_ioStreams = []
def initiate_chat(message: str):
    def conversationWorker(io: InProcessIOStream):
        with IOStream.set_default(io):
            user_proxy = UserProxyAgent(
                name="user_proxy",
                human_input_mode="ALWAYS",
                is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
                code_execution_config={
                    "use_docker": False
                },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
            )
            cathy = ConversableAgent(
                "cathy",
                system_message="Your name is Cathy and you are a part of a duo of comedians.",
                llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
                human_input_mode="ALWAYS",  # Never ask for human input.
                #human_input_mode="NEVER",  # Never ask for human input.
            )

            joe = ConversableAgent(
                "joe",
                system_message="Your name is Joe and you are a part of a duo of comedians.",
                llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
                human_input_mode="NEVER",  # Never ask for human input.
            )
            result = user_proxy.initiate_chat(cathy, message=message, max_turns=3)
            io.responseIsOver()
            #what should I do with result?

    io = InProcessIOStream()
    thread = threading.Thread(target=conversationWorker, args=(io,))
    thread.start()
    ix = len(_ioStreams)
    _ioStreams.append(io)
    return ix

def getAutogen(ix):
    return _ioStreams[ix]

def getMoreResponses(userInput: str, autogenId: int):
    autogen = getAutogen(autogenId)
    autogen.provide_input(userInput)
    return autogen.getResponsesStream()
