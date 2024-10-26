"""
Tests onnxml Normalizer converter
"""
import unittest
import warnings

import numpy as np
import torch
from sklearn.preprocessing import Normalizer

from hummingbird.ml._utils import onnx_ml_tools_installed, onnx_runtime_installed, lightgbm_installed
from hummingbird.ml import convert

if onnx_runtime_installed():
    import onnxruntime as ort
if onnx_ml_tools_installed():
    from onnxmltools import convert_sklearn
    from onnxmltools.convert.common.data_types import FloatTensorType as FloatTensorType_onnx


class TestONNXNormalizer(unittest.TestCase):
    def _test_normalizer_converter(self, norm):
        warnings.filterwarnings("ignore")
        X = np.array([[1, 2, 3], [4, 3, 0], [0, 1, 4], [0, 5, 6]], dtype=np.float32)

        # Create SKL model for testing
        model = Normalizer(norm=norm)
        model.fit(X)

        # Create ONNX-ML model
        onnx_ml_model = convert_sklearn(model, initial_types=[("float_input", FloatTensorType_onnx(X.shape))])

        # Create ONNX model by calling converter
        onnx_model = convert(onnx_ml_model, "onnx", X)

        # Get the predictions for the ONNX-ML model
        session = ort.InferenceSession(onnx_ml_model.SerializeToString())
        output_names = [session.get_outputs()[i].name for i in range(len(session.get_outputs()))]
        inputs = {session.get_inputs()[0].name: X}
        onnx_ml_pred = session.run(output_names, inputs)[0]

        # Get the predictions for the ONNX model
        onnx_pred = onnx_model.transform(X)

        return onnx_ml_pred, onnx_pred

    @unittest.skipIf(
        not (onnx_ml_tools_installed() and onnx_runtime_installed()), reason="ONNXML test requires ONNX, ORT and ONNXMLTOOLS"
    )
    def test_onnx_normalizer_l1(self, rtol=1e-06, atol=1e-06):
        onnx_ml_pred, onnx_pred = self._test_normalizer_converter("l1")

        # Check that predicted values match
        np.testing.assert_allclose(onnx_ml_pred, onnx_pred, rtol=rtol, atol=atol)

    @unittest.skipIf(
        not (onnx_ml_tools_installed() and onnx_runtime_installed()), reason="ONNXML test requires ONNX, ORT and ONNXMLTOOLS"
    )
    def test_onnx_normalizer_l2(self, rtol=1e-06, atol=1e-06):
        onnx_ml_pred, onnx_pred = self._test_normalizer_converter("l2")

        # Check that predicted values match
        np.testing.assert_allclose(onnx_ml_pred, onnx_pred, rtol=rtol, atol=atol)

    @unittest.skipIf(
        not (onnx_ml_tools_installed() and onnx_runtime_installed()), reason="ONNXML test requires ONNX, ORT and ONNXMLTOOLS"
    )
    def test_onnx_normalizer_max(self, rtol=1e-06, atol=1e-06):
        onnx_ml_pred, onnx_pred = self._test_normalizer_converter("max")

        # Check that predicted values match
        np.testing.assert_allclose(onnx_ml_pred, onnx_pred, rtol=rtol, atol=atol)

    @unittest.skipIf(
        not (onnx_ml_tools_installed() and onnx_runtime_installed()), reason="ONNXML test requires ONNX, ORT and ONNXMLTOOLS"
    )
    def test_onnx_normalizer_converter_raises_rt(self):
        warnings.filterwarnings("ignore")
        X = np.array([[1, 2, 3], [4, 3, 0], [0, 1, 4], [0, 5, 6]], dtype=np.float32)
        model = Normalizer(norm="l1")
        model.fit(X)

        # generate test input
        onnx_ml_model = convert_sklearn(model, initial_types=[("float_input", FloatTensorType_onnx(X.shape))])
        onnx_ml_model.graph.node[0].attribute[0].s = "".encode()

        self.assertRaises(RuntimeError, convert, onnx_ml_model, "onnx", X)


if __name__ == "__main__":
    unittest.main()
