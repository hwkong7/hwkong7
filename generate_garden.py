import json, os, urllib.request, datetime, html
from pathlib import Path

USER = "hwkong7"
COLORS = ["#FFF8F2", "#FCE5ED", "#F6B9D0", "#E88EAE", "#C7658D"]
QUERY = """query($login:String!) { user(login:$login) { contributionsCollection { contributionCalendar { weeks { contributionDays { date contributionCount contributionLevel } } } } } }"""


def main():
    token = os.environ["GITHUB_TOKEN"]
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "pink-garden-readme",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    weeks = result["data"]["user"]["contributionsCollection"]["contributionCalendar"][
        "weeks"
    ]
    levels = {
        "NONE": 0,
        "FIRST_QUARTILE": 1,
        "SECOND_QUARTILE": 2,
        "THIRD_QUARTILE": 3,
        "FOURTH_QUARTILE": 4,
    }
    width = 36 + len(weeks) * 14
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="150" viewBox="0 0 {width} 150" role="img" aria-label="{USER} GitHub contributions in strawberry milk and cream colors">',
        '<rect width="100%" height="100%" rx="12" fill="#FFFFFF"/>',
        '<text x="18" y="24" font-family="Arial,sans-serif" font-size="13" font-weight="600" fill="#8C526D">Strawberry Milk Contribution Garden</text>',
    ]
    for col, week in enumerate(weeks):
        for day in week["contributionDays"]:
            weekday = (datetime.date.fromisoformat(day["date"]).weekday() + 1) % 7
            x = 18 + col * 14
            y = 37 + weekday * 14
            level = levels[day["contributionLevel"]]
            lines.append(
                f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{COLORS[level]}"><title>{html.escape(day["date"])}: {day["contributionCount"]} contributions</title></rect>'
            )
    lines.append("</svg>")
    Path("assets").mkdir(exist_ok=True)
    Path("assets/pink-contributions.svg").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
