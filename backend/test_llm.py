from services.llm_service import generate_answer

answer = generate_answer(
    "What is the CGPA?",
    "CGPA: 8.93"
)

print(answer)