def plan(query):
    if "summary" in query.lower():
        return "summarize"
    return "qa"