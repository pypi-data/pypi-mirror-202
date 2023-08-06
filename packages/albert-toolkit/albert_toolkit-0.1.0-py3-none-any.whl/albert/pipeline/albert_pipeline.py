from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator
from albert.session import AlbertSession
from typing import Any


class PipelineConfig:
    def __init__(self, session: AlbertSession, params={}) -> None:
        self.params = params
        self.session = session

    def set_param(self, name: str, value: Any) -> None:
        self.params[name] = value

    def get_param(self, name: str) -> Any:
        if name.lower() == "session":
            return self.session

        if name in self.params:
            return self.params[name]

        raise KeyError(f"unknown pipeline parameter {name}")


class AlbertPipeline(Pipeline):
    def __init__(self, config: PipelineConfig, steps, *, memory=None, verbose=False):
        super().__init__(steps, memory=memory, verbose=verbose)
        self.config = config

        def _recurse_pipeline_config(head: Pipeline):
            for idx, tname, t in head._iter():
                if isinstance(head, FeatureUnion):
                    # Feature Union returns tuples of name, object, weight
                    t = tname
                    tname = idx
                    idx = 0

                if isinstance(t, AlbertPipeline) and t != self:
                    raise TypeError(
                        "AlbertPipeline is intended only as the parent pipeline, use standard"
                        " sklearn pipelines when nesting"
                    )

                if hasattr(t, "_set_albert_config"):
                    print(f"Configuring {tname} with albert config object")
                    t._set_albert_config(self.config)

                if hasattr(t, "_iter"):
                    _recurse_pipeline_config(t)

        _recurse_pipeline_config(self)

    def run(self):
        return self.transform(None)


class AlbertConfigurableBaseEstimator(BaseEstimator):
    def __init__(self) -> None:
        super().__init__()
        self.config = None

    def _set_albert_config(self, config: PipelineConfig):
        self.config = config
