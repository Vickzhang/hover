"""
Useful subroutines for working with bokeh in general.
"""
from functools import wraps
from traceback import format_exc
from bokeh.models import PreText
from bokeh.layouts import column


def servable(title=None):
    """
    Parametrizes a decorator which returns a document handle to be passed to bokeh.

    Search "embed server" on bokeh.org to find more context.

    Example:

    ```python
    @servable()
    def dummy(*args, **kwargs):
        from hover.core.explorer import BokehCorpusAnnotator
        annotator = BokehCorpusAnnotator(*args, **kwargs)
        annotator.plot()

        return annotator.view()

    # in Jupyter
    from bokeh.io import show, output_notebook
    output_notebook()
    show(dummy(*args, **kwargs))

    # in <your-bokeh-app-dir>/main.py
    from bokeh.io import curdoc
    doc = curdoc()
    dummy(*args, **kwargs)(doc)

    # embedding a bokeh server
    from bokeh.server.server import Server
    app_dict = {
        'my-app': dummy(*args, **kwargs),
        'my-other-app': dummy(*args, **kwargs),
    }
    server = Server(app_dict)
    server.start()
    ```
    """

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            def handle(doc):
                """
                Note that the handle must create a brand new bokeh model every time it is called.

                Reference: https://github.com/bokeh/bokeh/issues/8579
                """
                spinner = PreText(text="loading...")
                layout = column(spinner)

                def progress():
                    spinner.text += "."

                def load():
                    try:
                        bokeh_model = func(*args, **kwargs)
                        # remove spinner and its update
                        try:
                            doc.remove_periodic_callback(progress)
                        except Exception:
                            pass
                        layout.children.append(bokeh_model)
                        layout.children.pop(0)
                    except Exception as e:
                        # exception handling
                        message = PreText(text=f"{type(e)}: {e}\n{format_exc()}")
                        layout.children.append(message)

                doc.add_root(layout)
                doc.add_periodic_callback(progress, 5000)
                doc.add_timeout_callback(load, 500)
                doc.title = title or func.__name__

            return handle

        return wrapped

    return wrapper
