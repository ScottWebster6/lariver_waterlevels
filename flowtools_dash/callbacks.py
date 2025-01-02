#For modularity and clarity's sake, callbacks are defined here per
#https://stackoverflow.com/questions/62102453/how-to-define-callbacks-in-separate-files-plotly-dash
'''
def get_callbacks(app):
    @app.callback([Output("figure1", "figure")],
                  [Input("child1", "value")])
    def callback1(figure):
        return

    @app.callback([Output("figure2", "figure")],
                  [Input("child2", "value")])
    def callback2(figure):
        return

'''
