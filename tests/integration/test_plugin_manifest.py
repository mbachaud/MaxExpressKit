"""Sanity checks on .claude-plugin/plugin.json + hooks/hooks.json."""
import json
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_MANIFEST = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_MANIFEST = PLUGIN_ROOT / ".claude-plugin" / "marketplace.json"


def test_plugin_manifest_exists():
    assert PLUGIN_MANIFEST.is_file()


def test_plugin_manifest_has_required_fields():
    data = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    # Required by Claude Code plugin loader.
    for field in ["name", "description"]:
        assert field in data, f"missing {field}"
    assert data["name"] == "maxexpresskit"


def test_marketplace_manifest_lists_plugin():
    data = json.loads(MARKETPLACE_MANIFEST.read_text(encoding="utf-8"))
    assert "plugins" in data
    plugins = data["plugins"]
    assert any(p["name"] == "maxexpresskit" for p in plugins)


def test_hooks_json_is_valid():
    data = json.loads((PLUGIN_ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    assert "hooks" in data
    # All hook commands reference scripts that exist.
    for _event, entries in data.get("hooks", {}).items():
        for entry in entries:
            for h in entry.get("hooks", []):
                cmd = h.get("command", "")
                # Extract path between the quotes after CLAUDE_PLUGIN_ROOT.
                if "${CLAUDE_PLUGIN_ROOT}" in cmd:
                    rel = cmd.split("${CLAUDE_PLUGIN_ROOT}", 1)[1].strip("/").strip('"').strip()
                    rel = rel.split(" ", 1)[0].strip('"')
                    assert (PLUGIN_ROOT / rel).is_file(), f"hook script missing: {rel}"


def test_all_skills_have_frontmatter():
    skills_dir = PLUGIN_ROOT / "skills"
    for skill_md in skills_dir.rglob("SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{skill_md} missing frontmatter"
        assert "name:" in text[:300]
        assert "description:" in text[:600]


def test_all_agents_have_frontmatter():
    agents_dir = PLUGIN_ROOT / "agents"
    for md in agents_dir.glob("*.md"):
        text = md.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{md} missing frontmatter"


def test_all_commands_have_frontmatter():
    commands_dir = PLUGIN_ROOT / "commands"
    for md in commands_dir.glob("*.md"):
        text = md.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{md} missing frontmatter"
