# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional, Union

from azureml.train.automl.constants import HTSConstants
from azureml.train.automl.automlconfig import AutoMLConfig

from .pipeline_parameters import InferencePipelineParameters, TrainPipelineParameters


class HTSTrainParameters(TrainPipelineParameters):
    """
    Parameters for HTS train pipeline.

    :param automl_settings: The dict containing automl settings or ``AutoMLConfig`` object.
    :type automl_settings: azureml.train.automl.automlconfig.AutoMLConfig or dict
    :param hierarchy_column_names: The hierarchy column names.
    :type hierarchy_column_names: list(str)
    :param training_level: The HTS training level.
    :type training_level: str
    :param enable_engineered_explanations: The switch controls engineered explanations.
    :type enable_engineered_explanations: bool
    """
    def __init__(
            self,
            automl_settings: Union[AutoMLConfig, Dict[str, Any]],
            hierarchy_column_names: List[str],
            training_level: str,
            enable_engineered_explanations: Optional[bool] = False
    ):
        super(HTSTrainParameters, self).__init__(automl_settings)

        self.enable_engineered_explanations = enable_engineered_explanations
        self.hierarchy_column_names = hierarchy_column_names
        self.training_level = training_level
        self._modify_automl_settings()

    def validate(self, run_invocation_timeout):
        """
        Validates the supplied parameters.

        :param run_invocation_timeout: Specifies timeout for each AutoML run.
        :type run_invocation_timeout: int
        """
        super(HTSTrainParameters, self).validate(run_invocation_timeout)

    def _modify_automl_settings(self):
        self.automl_settings[HTSConstants.HIERARCHY] = self.hierarchy_column_names
        self.automl_settings[HTSConstants.TRAINING_LEVEL] = self.training_level


class HTSInferenceParameters(InferencePipelineParameters):
    """
    Parameters for HTS inference pipeline.

    :param hierarchy_forecast_level: The hts forecast level.
    :type: str
    :param allocation_method: The allocation methods. We currently support `'average_historical_proportions'` and
        `'proportions_of_historical_average'`.
    :type: str
    """

    def __init__(
            self,
            hierarchy_forecast_level: str,
            allocation_method: Optional[str] = HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE,
    ):
        super(HTSInferenceParameters, self).__init__()

        self.hierarchy_forecast_level = hierarchy_forecast_level
        self.allocation_method = allocation_method

    def validate(self):
        """Validates the supplied parameters."""
        super(HTSInferenceParameters, self).validate()
