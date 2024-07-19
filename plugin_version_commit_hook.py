import argparse
import tomllib
from monkeytypes import AgentPluginManifest
import yaml
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    if (
        "manifest.yaml" in args.filenames
        or "manifest.yml" in args.filenames
        or "pyproject.toml" in args.filenames
    ):
        pyproject_version = read_pyproject_toml_version()
        agent_plugin_manifest_version = read_agent_plugin_manifest_version(args.filenames)

        if pyproject_version != agent_plugin_manifest_version:
            print(
                "AgentPluginManifest version does not match pyproject.toml version: "
                f"{agent_plugin_manifest_version} != {pyproject_version}"
            )
            exit(1)


def read_agent_plugin_manifest_version(filenames) -> str:
    for filename in filenames:
        if filename in ["manifest.yaml", "manifest.yml"]:
            if Path(filename).exists():
                with open(filename, "r") as f:
                    return AgentPluginManifest(**yaml.safe_load(f)).version

    raise FileNotFoundError("Neither manifest.yaml nor manifest.yml was found")

def read_pyproject_toml_version() -> str:
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"].strip(" v")


if __name__ == "__main__":
    main()
