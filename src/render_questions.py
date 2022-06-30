from utils import questionnaire


if __name__ == "__main__":
    out = ["# Rendered list of questions", "", ""]
    for q in questionnaire._list_questions():
        out.append(f"# {q}")
        data = questionnaire._get_question(q)
        if "image" in data:
            out.append(f"![{q}]({data['image']})")
        if "question" in data:
            out.append(f"## {data['question']}")
        for opt in data["options"]:
            if data["correct"] == opt:
                out.append(f"* **CORRECT: {opt}**")
            else:
                out.append(f"* {opt}")
    with open("QUESTIONS.md", "w") as f:
        f.write("\n".join(out))
