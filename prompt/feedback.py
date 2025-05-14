def get_fallback_feedback(questions, answers, role):
    feedback = []
    for i, (q, a) in enumerate(zip(questions, answers), 1):
        feedback.append(f"Q{i} Feedback: Generic response received.\nRating: 6/10\nImprovement: Try to provide more depth and clarity.")
    return "\n\n".join(feedback)