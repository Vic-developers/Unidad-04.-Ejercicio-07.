import pytest

from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.model import build_model


@pytest.mark.parametrize("kind", ["logistic", "tree"])
def test_predictions_are_binary(kind):
    train, test = temporal_split(load_data())
    model = build_model(kind).fit(features(train), train.target)
    prediction = model.predict(features(test))
    assert set(prediction) <= {0, 1}
