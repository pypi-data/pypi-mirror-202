# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from logging import NOTSET
from unittest import TestCase
from unittest.mock import patch

from azure.monitor.opentelemetry.util.configurations import (
    LOGGING_EXPORT_INTERVAL_MS_ENV_VAR,
    SAMPLING_RATIO_ENV_VAR,
    _get_configurations,
)


class TestUtil(TestCase):
    def test_get_configurations(self):
        configurations = _get_configurations(
            connection_string="test_cs",
            exclude_instrumentations="test_exclude_instrumentations",
            disable_logging="test_disable_logging",
            disable_metrics="test_disable_metrics",
            disable_tracing="test_disable_tracing",
            instrumentations=["test_instrumentation"],
            logging_level="test_logging_level",
            logger_name="test_logger_name",
            resource="test_resource",
            sampling_ratio="test_sample_ratio",
            tracing_export_interval_ms=10000,
            logging_export_interval_ms=10000,
            metric_readers=("test_readers"),
            views=("test_view"),
            instrumentation_config="test_instrumentation_config",
            credential="test_credential",
        )

        self.assertEqual(configurations["connection_string"], "test_cs")
        self.assertEqual(
            configurations["exclude_instrumentations"],
            "test_exclude_instrumentations",
        )
        self.assertEqual(
            configurations["disable_logging"], "test_disable_logging"
        )
        self.assertEqual(
            configurations["disable_metrics"], "test_disable_metrics"
        )
        self.assertEqual(
            configurations["disable_tracing"], "test_disable_tracing"
        )
        self.assertEqual(configurations["logging_level"], "test_logging_level")
        self.assertEqual(configurations["logger_name"], "test_logger_name")
        self.assertEqual(configurations["resource"], "test_resource")
        self.assertEqual(configurations["sampling_ratio"], "test_sample_ratio")
        self.assertEqual(configurations["tracing_export_interval_ms"], 10000)
        self.assertEqual(configurations["logging_export_interval_ms"], 10000)
        self.assertEqual(configurations["metric_readers"], ("test_readers"))
        self.assertEqual(configurations["views"], ("test_view"))
        self.assertEqual(
            configurations["instrumentation_config"],
            ("test_instrumentation_config"),
        )
        self.assertEqual(configurations["credential"], ("test_credential"))

    @patch.dict("os.environ", {}, clear=True)
    def test_get_configurations_defaults(self):
        configurations = _get_configurations()

        self.assertTrue("connection_string" not in configurations)
        self.assertEqual(configurations["exclude_instrumentations"], [])
        self.assertEqual(configurations["disable_logging"], False)
        self.assertEqual(configurations["disable_metrics"], False)
        self.assertEqual(configurations["disable_tracing"], False)
        self.assertEqual(configurations["logging_level"], NOTSET)
        self.assertEqual(configurations["logger_name"], "")
        self.assertTrue("resource" not in configurations)
        self.assertEqual(configurations["sampling_ratio"], 1.0)
        self.assertEqual(configurations["tracing_export_interval_ms"], None)
        self.assertEqual(configurations["logging_export_interval_ms"], 5000)
        self.assertEqual(configurations["metric_readers"], [])
        self.assertEqual(configurations["views"], ())
        self.assertEqual(configurations["instrumentation_config"], {})

    def test_get_configurations_validation(self):
        self.assertRaises(
            ValueError, _get_configurations, logging_export_interval_ms=-0.5
        )
        self.assertRaises(
            ValueError, _get_configurations, logging_export_interval_ms=-1
        )

    @patch.dict(
        "os.environ",
        {
            LOGGING_EXPORT_INTERVAL_MS_ENV_VAR: "10000",
            SAMPLING_RATIO_ENV_VAR: "0.5",
        },
        clear=True,
    )
    def test_get_configurations_env_vars(self):
        configurations = _get_configurations()

        self.assertTrue("connection_string" not in configurations)
        self.assertEqual(configurations["exclude_instrumentations"], [])
        self.assertEqual(configurations["disable_logging"], False)
        self.assertEqual(configurations["disable_metrics"], False)
        self.assertEqual(configurations["disable_tracing"], False)
        self.assertEqual(configurations["logging_level"], NOTSET)
        self.assertEqual(configurations["logger_name"], "")
        self.assertTrue("resource" not in configurations)
        self.assertEqual(configurations["sampling_ratio"], 0.5)
        self.assertEqual(configurations["tracing_export_interval_ms"], None)
        self.assertEqual(configurations["logging_export_interval_ms"], 5000)
        self.assertEqual(configurations["metric_readers"], [])
        self.assertEqual(configurations["views"], ())
        self.assertEqual(configurations["instrumentation_config"], {})

    @patch.dict(
        "os.environ",
        {
            LOGGING_EXPORT_INTERVAL_MS_ENV_VAR: "Ten Thousand",
            SAMPLING_RATIO_ENV_VAR: "Half",
        },
        clear=True,
    )
    def test_get_configurations_env_vars_validation(self):
        configurations = _get_configurations()

        self.assertTrue("connection_string" not in configurations)
        self.assertEqual(configurations["exclude_instrumentations"], [])
        self.assertEqual(configurations["disable_logging"], False)
        self.assertEqual(configurations["disable_metrics"], False)
        self.assertEqual(configurations["disable_tracing"], False)
        self.assertEqual(configurations["logging_level"], NOTSET)
        self.assertEqual(configurations["logger_name"], "")
        self.assertTrue("resource" not in configurations)
        self.assertEqual(configurations["sampling_ratio"], 1.0)
        self.assertEqual(configurations["tracing_export_interval_ms"], None)
        self.assertEqual(configurations["logging_export_interval_ms"], 5000)
        self.assertEqual(configurations["metric_readers"], [])
        self.assertEqual(configurations["views"], ())
        self.assertEqual(configurations["instrumentation_config"], {})
