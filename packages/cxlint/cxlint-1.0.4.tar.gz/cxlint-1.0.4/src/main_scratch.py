# pylint: skip-file

"""Testing"""

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

from cxlint import CxLint

if __name__ == "__main__":
    agent_local_path = "data/agent"
    agent_id = 'projects/prebuilt-components-qa/locations/global/agents/872bd829-3ff6-4a3f-a242-cc5fa769a56c'
    gcs_path = 'gs://pmarlow_dev_agents/demo_agent_json.zip'

    naming_conventions = {
        "agent_name": ".*",
        "flow_name": ".*",
        "intent_head_name": "head_intent.*",
        "intent_confirmation_name": ".*",
        "intent_escalation_name": ".*",
        "intent_generic_name": ".*",
        "entity_type_name": ".*",
        "page_generic_name": ".*",
        "page_with_form_name": ".*",
        "page_with_webhook_name": ".*",
        "test_case_name": ".*",
        "webhook_name": ".*"
        }

    cxlint = CxLint(
        agent_id=agent_id,
        naming_conventions=naming_conventions,
        load_gcs=True,
        # agent_type='chat',
        # language_code=['en'],
        # resource_filter=["flows"],
        # flow_include_list=['Steering'],
        # intent_include_pattern='sup'
        output_file="/Users/pmarlow/eng/cxlint/data/logs.txt",
    )

    agent_file = cxlint.gcs.download_gcs(gcs_path, agent_local_path)
    cxlint.gcs.unzip(agent_file, agent_local_path)

    cxlint.lint_agent(agent_local_path)
