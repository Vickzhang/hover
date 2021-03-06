from hover.recipes import simple_annotator, linked_annotator
from bokeh.io import curdoc


def test_simple_annotator(mini_supervisable_text_dataset_embedded):
    dataset = mini_supervisable_text_dataset_embedded.copy()
    doc = curdoc()
    simple_annotator(dataset)(doc)


def test_linked_annotator(mini_supervisable_text_dataset_embedded):
    dataset = mini_supervisable_text_dataset_embedded.copy()
    doc = curdoc()
    linked_annotator(dataset)(doc)
