import mesop as me

from typing import Iterable
from examples.mesop_poc.data_model import State, ChatMessage
from examples.mesop_poc.fast_agency import getAutogen, initiate_chat, getMoreResponses, Question

def send_prompt_to_autogen(prompt: str) -> Iterable[str]:
    state = me.state(State)
    autogen = initiate_chat(prompt)
    state.autogen = autogen
    responses = getAutogen(autogen).getResponsesStream()
    for chunk in responses():
        if isinstance(chunk, Question):
            print("auto providing input - not")
            state = me.state(State)
            state.waitingForFeedback = True
            #getAutogen(autogen).provide_input("")
            #chunk = chunk.question
        yield chunk
    print("end of send prompt responoses -----------------")

def send_user_feedback_to_autogen(userResponse: str) -> Iterable[str]:
    state = me.state(State)
    #print("sending user response state je", state)
    print("sending user response state je", state.autogen)
    state.waitingForFeedback = False
    responses = getMoreResponses(userResponse, state.autogen)
    for chunk in responses():
        if isinstance(chunk, Question):
            print("auto providing input - not")
            state = me.state(State)
            state.waitingForFeedback = True
            #getAutogen(autogen).provide_input("") #uncomment this for autoreply
            #chunk = chunk.question
            yield chunk
        yield chunk
    print("end of send feedback responses -----------------")
