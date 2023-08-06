"""Entity Type linter methods and functions."""

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from configparser import ConfigParser

from cxlint.common import Common
from cxlint.rules.entity_types import EntityTypeRules
from cxlint.resources.types import EntityType, LintStats


class EntityTypes:
    """Entity Type linter methods and functions."""

    def __init__(self, verbose: bool, config: ConfigParser, console):
        self.verbose = verbose
        self.console = console
        self.config = config
        self.agent_id = Common.load_agent_id(config)
        self.disable_map = Common.load_message_controls(config)
        self.lang_code_filter = Common.load_lang_code_filter(config)
        self.naming_conventions = Common.load_naming_conventions(config)
        self.rules = EntityTypeRules(console, self.disable_map)

    @staticmethod
    def build_entity_type_path_list(agent_local_path: str):
        """Builds a list of dirs, each representing an Entity Type directory.

        Ex: /path/to/agent/entityTypes/<entity_type_dir>

        This dir path can then be used to find the next level of information
        in the directory by appending the appropriate next dir structures like:
        - <entity_type_name>.json, for the Entity Type object
        - /entities, for the Entities dir
        """
        root_dir = agent_local_path + "/entityTypes"

        entity_type_paths = []

        for entity_type_dir in os.listdir(root_dir):
            entity_type_dir_path = f"{root_dir}/{entity_type_dir}"
            entity_type_paths.append(entity_type_dir_path)

        return entity_type_paths

    @staticmethod
    def build_lang_code_paths(etype: EntityType):
        """Builds dict of lang codes and file locations.

        The language_codes and paths for each file are stored in a dictionary
        inside of the Entity Type dataclass. This dict is accessed later to
        lint each file and provide reporting based on each language code.
        """
        root_dir = etype.dir_path + "/entities"

        for lang_file in os.listdir(root_dir):
            lang_code = lang_file.split(".")[0]
            lang_code_path = f"{root_dir}/{lang_file}"
            etype.entities[lang_code] = {"file_path": lang_code_path}

    @staticmethod
    def gather_entity_type_metadata(etype: EntityType):
        """Extract metadata for Entity Type for later processing."""
        metadata_file = etype.dir_path + f"/{etype.display_name}.json"

        with open(metadata_file, "r", encoding="UTF-8") as etype_file:
            etype.data = json.load(etype_file)
            etype.resource_id = etype.data.get("name", None)
            etype.kind = etype.data.get("kind", None)

            etype_file.close()

    def lint_language_codes(self, etype: EntityType, stats: LintStats):
        """Executes all Entity based linter rules."""

        for lang_code in etype.entities:
            ent_file_path = Common.get_file_based_on_lang_code_filter(
                etype, lang_code, self.lang_code_filter
            )

            if ent_file_path:
                with open(ent_file_path, "r", encoding="UTF-8") as ent_file:
                    data = json.load(ent_file)
                    entities = data.get("entities", None)
                    etype.entities[lang_code]["entities"] = entities

                    stats = self.rules.run_entity_type_rules(
                        etype, lang_code, stats)

                    ent_file.close()

        return stats

    def lint_entities(self, etype: EntityType, stats: LintStats):
        """Lint the Entity files inside of an Entity Type."""
        if "entities" in os.listdir(etype.dir_path):
            self.build_lang_code_paths(etype)
            stats = self.lint_language_codes(etype, stats)

        else:
            pass
            # TODO pmarlow: Add rule for Entity Type missing Entities

        return stats

    def lint_entity_type(self, etype: EntityType, stats: LintStats):
        """Lint a Single Entity Type dir and all subdirectories."""

        etype.display_name = Common.parse_filepath(
            etype.dir_path, "entity_type"
        )

        self.gather_entity_type_metadata(etype)
        stats = self.lint_entities(etype, stats)

        return stats

    def lint_entity_types_directory(self, agent_local_path: str):
        """Linting the Entity Types dir in the JSON Package structure."""
        start_message = f'{"#" * 10} Begin Entity Types Directory Linter'
        self.console.log(start_message)

        stats = LintStats()

        # Create a list of all Flow paths to iter through
        entity_type_paths = self.build_entity_type_path_list(agent_local_path)
        stats.total_entity_types = len(entity_type_paths)

        # linting starts here
        for entity_type_path in entity_type_paths:
            etype = EntityType()
            etype.verbose = self.verbose
            etype.agent_id = self.agent_id
            etype.dir_path = entity_type_path
            etype.naming_pattern = self.naming_conventions.get(
                "entity_type_name", None)
            stats = self.lint_entity_type(etype, stats)

        header = "-" * 20
        rating = Common.calculate_rating(
            stats.total_issues, stats.total_inspected
        )

        end_message = (
            f"\n{header}\n{stats.total_entity_types} Entity Types "
            f"linted. \n{stats.total_issues} issues found out of "
            f"{stats.total_inspected} inspected."
            f"\nYour Agent Entity Types rated at {rating:.2f}/10\n\n"
        )
        self.console.log(end_message)
