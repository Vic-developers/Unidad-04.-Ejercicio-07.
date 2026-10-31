import pytest

from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.fairness import audit, gap
from inf8239_u04.model import build_model


@pytest.mark.parametrize("kind", ["logistic", "tree"])
def test_fairness_metrics_are_bounded(kind):
    train, test = temporal_split(load_data())
    model = build_model(kind).fit(features(train), train.target)
    _, groups, _ = audit(test.target, model.predict(features(test)), test.protected_group)
    assert 0 <= gap(groups, "recall") <= 1
    assert set(groups.index) == {"G1", "G2"}
