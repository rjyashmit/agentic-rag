from agents.query_planner import plan
from agents.retriever_agent import retrieve
from agents.context_builder import build_context
from agents.answer_agent import answer

def ask(query):
    plan(query)
    docs = retrieve(query)
    context = build_context(docs)
    return answer(context, query)