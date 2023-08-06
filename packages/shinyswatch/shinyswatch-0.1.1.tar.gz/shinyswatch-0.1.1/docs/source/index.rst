.. shinyswatch package
.. ===================

.. Module contents
.. ---------------

.. .. automodule:: shinyswatch
..    :members:
..    :undoc-members:
..    :show-inheritance:



API Reference Intro
===================

.. shinylive-editor::

    import shinyswatch
    from shiny import *

    app_ui = ui.page_fluid(
      shinyswatch.theme("darkly"),
      ui.input_slider("n", "Value of n", min=1, max=10, value=5),
      ui.output_text("n2")
    )

    def server(input: Inputs, output: Outputs, session: Session) -> None:
        @output
        @render.text
        def n2():
            return f"The value of n*2 is {input.n() * 2}"

    app = App(app_ui, server)


API Reference
=============

.. currentmodule:: shinyswatch

.. autosummary::
    :toctree: reference/

    theme
