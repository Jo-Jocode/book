import os
import yaml

INPUT_DIR = "team/team_info"     # folder containing individual md files
OUTPUT_FILE = "team/team.md"     # output overview file


def read_person(filepath):
    """Read an individual .md file and extract frontmatter + body."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---"):
        _, frontmatter, body = content.split("---", 2)
        data = yaml.safe_load(frontmatter)
        data["body"] = body.strip()
        return data
    return None


def generate_card(person):
    """Generate HTML for a neat horizontal person card."""
    # No leading/trailing newlines to avoid Markdown indentation
    return f"""<div class="team-card">
<img src="https://files.mude.citg.tudelft.nl/{person['photo']}" alt="{person['name']}">
<div class="team-info">
<h3>{person['name']}</h3>
<p><em>{person['role']}</em></p>
<p>{person['body']}</p>
<a href="mailto:{person['email']}">Email</a>
</div>
</div>"""


def main():
    # Collect all people
    people = []
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".md"):
            person = read_person(os.path.join(INPUT_DIR, filename))
            if person:
                people.append(person)

    # Group by role
    grouped = {}
    for p in people:
        role = p["role"]
        grouped.setdefault(role, []).append(p)

    # Sort roles alphabetically
    grouped = dict(sorted(grouped.items()))

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # Add responsive Flexbox CSS at top
        f.write("""<style>
.team-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin: 0;
  padding: 0;
}
.team-card {
  flex: 1 1 calc(33.333% - 15px);
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
  margin: 0;
}
.team-card img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}
.team-info {
  text-align: left;
  font-size: 0.9em;
}
.team-info h3 {
  margin: 0;
  font-size: 1.05em;
}
.team-info p {
  margin: 2px 0;
}
/* Responsive: 2 per row on tablets, 1 per row on mobile */
@media (max-width: 900px) {
  .team-card { flex: 1 1 calc(50% - 15px); }
}
@media (max-width: 600px) {
  .team-card { flex: 1 1 100%; }
}
</style>\n""")

        f.write("# Our Team\n\n")

        for role, members in grouped.items():
            f.write(f"## {role}\n\n")
            f.write('<div class="team-container">')
            # No extra newlines between cards
            for m in members:
                f.write(generate_card(m))
            f.write('</div>\n\n---\n\n')

    print(f"✅ Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
