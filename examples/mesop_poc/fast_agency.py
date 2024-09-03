import queue
import threading
import os
import re
from  queue import Queue
from autogen import ConversableAgent, UserProxyAgent
from autogen.io.base import IOStream
from autogen.agentchat import ChatResult
from typing import Any

from fastagency.core import Chatable, ConsoleIO, IOMessage

class AutogenOutputElement:
    def __init__(self, text):
        self.text = text

    def plain_text(self):
        t = self.text
        t = re.sub(r"\x1b\[0m", "", t)
        t = re.sub(r"\x1b\[1m", "", t)
        t = re.sub(r"\x1b\[4m", "", t)
        t = re.sub(r"\x1b\[30m", "", t)
        t = re.sub(r"\x1b\[31m", "", t)
        t = re.sub(r"\x1b\[32m", "", t)
        t = re.sub(r"\x1b\[33m", "", t)
        t = re.sub(r"\x1b\[34m", "", t)
        t = re.sub(r"\x1b\[35m", "", t)
        t = re.sub(r"\x1b\[36m", "", t)
        t = re.sub(r"\x1b\[37m", "", t)
        return t

    def __str__(self):
        return f'{self.__class__.__name__}({self.plain_text()})'

    def __repr__(self):
        return str(self)

class Question(AutogenOutputElement):
    def __init__(self, question):
        super().__init__(question)


class AnswerFragment(AutogenOutputElement):
    def __init__(self, fragment):
        super().__init__(fragment)



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
        print("stavljam u out queue", AnswerFragment(xs))
        self._out_queue.put(AnswerFragment(xs))

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

    def responseIsOver(self, chatResult: ChatResult):
        self._out_queue.put(chatResult)

    def getResponsesStream(self):
        def responsesGenerator():
            while True:
                value = self._out_queue.get()
                if isinstance(value, ChatResult):
                    break
                # Question shold also end the generator
                if isinstance(value, Question):
                    yield value
                    break
                yield value
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
            #print("##### result of chat is..", result)
            io.responseIsOver(result)
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
