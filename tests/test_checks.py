def test_no_basic_models_present(models):
    assert models.BasicModel.select().count() == 0
