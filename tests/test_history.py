def test_no_basic_models_present(models):
    assert models.BasicModel.select().count() == 0

def test_create_basic_model(models):
    m = models.BasicModel.create(foo='YAY', bar=42)
    assert m.versions.count() == 1
    assert m.history().select().count() == 0

def test_update_basic_model(models):
    m = models.BasicModel.create(foo='YAY', bar=42)
    m.foo = 'HUZZAH!'
    m.save()
    assert m.versions.count() == 2
    changes = m.versions[0].changes
    assert 'foo' in changes
    assert 'bar' not in changes

def test_delete_basic_model(models):
    m = models.BasicModel.create(foo='YAY', bar=42)
    m.delete_instance()
    assert models.BasicModel.select().count() == 0
    assert models.BasicModel.history().select().count() == 1

def test_create_fk_model(models):
    r = models.ReferencedModel.create(lol='happy days and jubilations!')
    m = models.FKModel.create(ref=r)
    assert r.haha.count() == 1
    assert m.versions.count() == 1
    assert m.history().select().count() == 0
    assert r.haha_history.count() == 0

def test_update_fk_model(models):
    pass

def test_delete_fk_model(models):
    pass

