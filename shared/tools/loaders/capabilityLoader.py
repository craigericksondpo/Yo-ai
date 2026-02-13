# capabilityLoader.py

# Universal Capability Loader (Skill Bundle Model)
# This loader
# •	indexes skills
# •	indexes capability bundles
# •	indexes artifacts
# •	resolves all artifact references
# •	produces a unified capability object per skill
# •	is reusable across all agent classes


class CapabilityLoader:

    def __init__(self, card):
        self.card = card

        # Index skills by name
        self.skills = {
            s["name"]: s
            for s in card.get("skills", [])
        }

        # Index capability bundles by name
        self.capability_bundles = {
            c["name"]: c
            for c in card.get("x-capabilities", [])
        }

        # Index artifacts by name
        self.artifacts = {
            a["name"]: a
            for a in card.get("x-artifacts", [])
        }


    def load(self):
        loaded = {}

        for skill_name, skill in self.skills.items():
            bundle = self.capability_bundles.get(skill_name)

            if not bundle:
                # Skill exists but no extended capability bundle
                loaded[skill_name] = {
                    "skill": skill,
                    "artifacts": []
                }
                continue

            resolved_artifacts = []

            for ref in bundle.get("artifacts", []):
                artifact_name = ref["name"]
                artifact = self.artifacts.get(artifact_name)

                if artifact:
                    resolved_artifacts.append({
                        "artifactType": ref["artifactType"],
                        "name": artifact_name,
                        "version": artifact.get("version"),
                        "schema": artifact.get("schema"),
                        "description": artifact.get("description")
                    })

            loaded[skill_name] = {
                "skill": skill,
                "artifacts": resolved_artifacts
            }

        return loaded
