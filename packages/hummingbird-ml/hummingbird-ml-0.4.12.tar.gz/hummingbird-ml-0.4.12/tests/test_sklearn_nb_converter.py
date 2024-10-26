"""
Tests sklearn Naive Bayes model (BernoulliNB, GaussianNB, MultinomialNB) converters.
"""
import unittest
import warnings

import numpy as np
import torch
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB

import hummingbird.ml
from hummingbird.ml._utils import tvm_installed


class TestSklearnNBClassifier(unittest.TestCase):

    # BernoulliNB test function to be parameterized
    def _test_bernoulinb_classifer(
        self, num_classes, alpha=1.0, binarize=None, fit_prior=False, class_prior=None, labels_shift=0, backend="torch"
    ):
        model = BernoulliNB(alpha=alpha, binarize=binarize, fit_prior=fit_prior, class_prior=class_prior)
        np.random.seed(0)
        if binarize is None:
            X = np.random.randint(2, size=(100, 200))
        else:
            X = np.random.rand(100, 200)
        X = np.array(X, dtype=np.float32)
        y = np.random.randint(num_classes, size=100) + labels_shift

        model.fit(X, y)
        torch_model = hummingbird.ml.convert(model, backend, X)
        self.assertTrue(torch_model is not None)
        np.testing.assert_allclose(model.predict_proba(X), torch_model.predict_proba(X), rtol=1e-6, atol=1e-5)

    # BernoulliNB binary
    def test_bernoulinb_classifer_bi(self):
        self._test_bernoulinb_classifer(2)

    # BernoulliNB multi-class
    def test_bernoulinb_classifer_multi(self):
        self._test_bernoulinb_classifer(3)

    # BernoulliNB multi-class w/ modified alpha
    def test_bernoulinb_classifer_multi_alpha(self):
        self._test_bernoulinb_classifer(3, alpha=0.5)

    #  BernoulliNB multi-class w/ binarize
    def test_bernoulinb_classifer_multi_binarize(self):
        self._test_bernoulinb_classifer(3, binarize=0.5)

    #  BernoulliNB multi-class w/ fit prior
    def test_bernoulinb_classifer_multi_fit_prior(self):
        self._test_bernoulinb_classifer(3, fit_prior=True)

    #  BernoulliNB multi-class w/ class prior
    def test_bernoulinb_classifer_multi_class_prior(self):
        np.random.seed(0)
        class_prior = np.random.rand(3)
        self._test_bernoulinb_classifer(3, class_prior=class_prior)

    # BernoulliNB multi-class w/ labels shift
    def test_bernoulinb_classifer_multi_labels_shift(self):
        self._test_bernoulinb_classifer(3, labels_shift=3)

    # Test TVM backend
    # BernoulliNB binary
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_bernoulinb_classifer_bi_tvm(self):
        self._test_bernoulinb_classifer(2, backend="tvm")

    # BernoulliNB multi-class
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_bernoulinb_classifer_multi_tvm(self):
        self._test_bernoulinb_classifer(3, backend="tvm")

    # BernoulliNB multi-class w/ modified alpha
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_bernoulinb_classifer_multi_alpha_tvm(self):
        self._test_bernoulinb_classifer(3, alpha=0.5, backend="tvm")

    #  BernoulliNB multi-class w/ binarize
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_bernoulinb_classifer_multi_binarize_tvm(self):
        self._test_bernoulinb_classifer(3, binarize=0.5, backend="tvm")

    #  BernoulliNB multi-class w/ fit prior
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_bernoulinb_classifer_multi_fit_prior_tvm(self):
        self._test_bernoulinb_classifer(3, fit_prior=True, backend="tvm")

    #  BernoulliNB multi-class w/ class prior
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_bernoulinb_classifer_multi_class_prior_tvm(self, backend="tvm"):
        np.random.seed(0)
        class_prior = np.random.rand(3)
        self._test_bernoulinb_classifer(3, class_prior=class_prior)

    # BernoulliNB multi-class w/ labels shift
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_bernoulinb_classifer_multi_labels_shift_tvm(self, backend="tvm"):
        self._test_bernoulinb_classifer(3, labels_shift=3)

    # MultinomialNB test function to be parameterized
    def _test_multinomialnb_classifer(
        self, num_classes, alpha=1.0, fit_prior=False, class_prior=None, labels_shift=0, backend="torch"
    ):
        model = MultinomialNB(alpha=alpha, fit_prior=fit_prior, class_prior=class_prior)
        np.random.seed(0)
        X = np.random.rand(100, 200)
        X = np.array(X, dtype=np.float32)
        y = np.random.randint(num_classes, size=100) + labels_shift

        model.fit(X, y)
        torch_model = hummingbird.ml.convert(model, backend, X)
        self.assertTrue(torch_model is not None)
        np.testing.assert_allclose(model.predict_proba(X), torch_model.predict_proba(X), rtol=1e-6, atol=1e-5)

    # MultinomialNB binary
    def test_multinomialnb_classifer_bi(self):
        self._test_multinomialnb_classifer(2)

    # MultinomialNB multi-class
    def test_multinomialnb_classifer_multi(self):
        self._test_multinomialnb_classifer(3)

    # MultinomialNB multi-class w/ modified alpha
    def test_multinomialnb_classifer_multi_alpha(self):
        self._test_multinomialnb_classifer(3, alpha=0.5)

    #  MultinomialNB multi-class w/ fir prior
    def test_multinomialnb_classifer_multi_fit_prior(self):
        self._test_multinomialnb_classifer(3, fit_prior=True)

    #  MultinomialNB multi-class w/ class prior
    def test_multinomialnb_classifer_multi_class_prior(self):
        np.random.seed(0)
        class_prior = np.random.rand(3)
        self._test_multinomialnb_classifer(3, class_prior=class_prior)

    # BernoulliNB multi-class w/ labels shift
    def test_multinomialnb_classifer_multi_labels_shift(self):
        self._test_multinomialnb_classifer(3, labels_shift=3)

    # TVM Backend
    # MultinomialNB binary
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_multinomialnb_classifer_bi_tvm(self):
        self._test_multinomialnb_classifer(2, backend="tvm")

    # MultinomialNB multi-class
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_multinomialnb_classifer_multi_tvm(self):
        self._test_multinomialnb_classifer(3, backend="tvm")

    # MultinomialNB multi-class w/ modified alpha
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_multinomialnb_classifer_multi_alpha_tvm(self):
        self._test_multinomialnb_classifer(3, alpha=0.5, backend="tvm")

    #  MultinomialNB multi-class w/ fir prior
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_multinomialnb_classifer_multi_fit_prior_tvm(self):
        self._test_multinomialnb_classifer(3, fit_prior=True, backend="tvm")

    #  MultinomialNB multi-class w/ class prior
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_multinomialnb_classifer_multi_class_prior_tvm(self):
        np.random.seed(0)
        class_prior = np.random.rand(3)
        self._test_multinomialnb_classifer(3, class_prior=class_prior, backend="tvm")

    # BernoulliNB multi-class w/ labels shift
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_multinomialnb_classifer_multi_labels_shift_tvm(self):
        self._test_multinomialnb_classifer(3, labels_shift=3, backend="tvm")

    # GaussianNB test function to be parameterized
    def _test_gaussiannb_classifer(self, num_classes, priors=None, var_smoothing=1e-9, labels_shift=0, backend="torch"):
        model = GaussianNB(priors=priors, var_smoothing=var_smoothing)
        np.random.seed(0)
        X = np.random.rand(100, 200)
        X = np.array(X, dtype=np.float32)
        y = np.random.randint(num_classes, size=100) + labels_shift

        model.fit(X, y)
        torch_model = hummingbird.ml.convert(model, backend, X)
        self.assertTrue(torch_model is not None)
        np.testing.assert_allclose(model.predict_proba(X), torch_model.predict_proba(X), rtol=1e-5, atol=1e-5)

    # GaussianNB binary
    def test_gaussiannb_classifer_bi(self):
        self._test_gaussiannb_classifer(2)

    # GaussianNB multi-class
    def test_gaussiannb_classifer_multi(self):
        self._test_gaussiannb_classifer(3)

    #  GaussianNB multi-class w/ class prior
    def test_gaussiannb_classifer_multi_class_prior(self):
        np.random.seed(0)
        priors = np.random.rand(3)
        priors = priors / np.sum(priors)
        self._test_gaussiannb_classifer(3, priors=priors)

    # GaussianNB multi-class w/ modified var_smoothing
    def test_gaussiannb_classifer_multi_alpha(self):
        self._test_gaussiannb_classifer(3, var_smoothing=1e-2)

    # GaussianNB multi-class w/ labels shift
    def test_gaussiannb_classifer_multi_labels_shift(self):
        self._test_gaussiannb_classifer(3, labels_shift=3)

    # TVM Backend
    # GaussianNB binary
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_gaussiannb_classifer_bi_tvm(self):
        self._test_gaussiannb_classifer(2, backend="tvm")

    # GaussianNB multi-class
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_gaussiannb_classifer_multi_tvm(self):
        self._test_gaussiannb_classifer(3, backend="tvm")

    #  GaussianNB multi-class w/ class prior
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_gaussiannb_classifer_multi_class_prior_tvm(self):
        np.random.seed(0)
        priors = np.random.rand(3)
        priors = priors / np.sum(priors)
        self._test_gaussiannb_classifer(3, priors=priors, backend="tvm")

    # GaussianNB multi-class w/ modified var_smoothing
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_gaussiannb_classifer_multi_alpha_tvm(self):
        self._test_gaussiannb_classifer(3, var_smoothing=1e-2, backend="tvm")

    # GaussianNB multi-class w/ labels shift
    @unittest.skipIf(not (tvm_installed()), reason="TVM tests require TVM")
    def test_gaussiannb_classifer_multi_labels_shift_tvm(self):
        self._test_gaussiannb_classifer(3, labels_shift=3, backend="tvm")


if __name__ == "__main__":
    unittest.main()
