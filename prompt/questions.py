import random

QUESTION_BANK = {
    "python": [
        "What are Python's key features?",
        "Explain list vs tuple.",
        "What are Python decorators?",
        "Explain the GIL (Global Interpreter Lock).",
        "How does memory management work in Python?",
    ],
    "javascript": [
        "Explain 'hoisting' in JavaScript.",
        "What is closure?",
        "Difference between var, let, and const?",
        "What is event delegation?",
        "Explain the call stack and event loop.",
    ],
    "react": [
        "What are React hooks?",
        "What is the virtual DOM?",
        "Difference between useEffect and useLayoutEffect?",
        "Explain React’s reconciliation process.",
        "What is memoization in React?",
    ],
    "node": [
        "What is event-driven programming?",
        "Explain Node.js architecture.",
        "What is the difference between process.nextTick() and setImmediate()?",
        "What is a stream in Node.js?",
        "How does clustering work in Node?",
    ],
    "express": [
        "What is middleware in Express.js?",
        "How does routing work in Express?",
        "What is the use of next() in Express?",
        "Difference between PUT and PATCH?",
        "How to handle errors globally in Express?",
    ],
    "sql": [
        "What is the difference between WHERE and HAVING?",
        "What is normalization?",
        "Explain JOIN types in SQL.",
        "What is a primary key vs foreign key?",
        "What is a subquery?",
    ],
    "powerbi": [
        "What is DAX in Power BI?",
        "Difference between a dashboard and a report?",
        "What are slicers?",
        "Explain relationships in Power BI.",
        "How do you optimize large datasets in Power BI?",
    ],
    "java": [
        "Explain OOP principles in Java.",
        "What is the difference between == and equals()?",
        "What is JVM, JRE, and JDK?",
        "What is multithreading in Java?",
        "Explain garbage collection in Java.",
    ],
    "sap": [
        "What is SAP HANA?",
        "Explain the difference between OLAP and OLTP.",
        "What is a transaction code in SAP?",
        "How does SAP integrate with other systems?",
        "What is ABAP in SAP?",
    ],
}

def get_fallback_questions(role):
    role_key = role.lower().strip()
    for key in QUESTION_BANK:
        if key in role_key:
            return "\n".join(random.sample(QUESTION_BANK[key], 5))

    return "Sorry, I couldn't find fallback questions for that role."