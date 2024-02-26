from dash import Dash, html, dcc, Input, Output, State, callback
from gqlinterface import GqlInterface
from datetime import date, datetime
import inflect

inflectEngine = inflect.engine()

app = Dash(__name__)

message = ""
users = []
fitnessGql = None
try:
    fitnessGql = GqlInterface()
    users = fitnessGql.getUsers()
    message = "Found " + str(len(users)) + inflectEngine.plural("user", len(users)) + " in GQL"
except Exception as e:
    print("Unable to generate Users message: " + repr(e))
    message = 'Unable to load GQL'

app.layout = html.Div([
    html.Div(children=message),
    dcc.Dropdown([user.username for user in users], users[0].username, id='user'),
    dcc.Input(
            id="input_weight",
            type="number",
            placeholder="Weight",
        ),
    dcc.DatePickerSingle(
        id='date',
        min_date_allowed=date(2000, 1, 1),
        max_date_allowed=datetime.today(),
        initial_visible_month=datetime.today(),
        date=datetime.today()
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a weight')
])

@callback(
    Output('container-button-basic', 'children'),
    State('user', 'value'),
    State('input_weight', 'value'),
    State('date', 'date'),
    Input('submit-val', 'n_clicks'),
    prevent_initial_call=True
)
def update_output(user, weight, inputDate, n_clicks):
    selectedUser = None
    for i in users:
        if i.username == user:
            selectedUser = i
    fitnessGql.addWeight(selectedUser.id, weight, inputDate)
    return 'The user "{}" input a weight of {} on {}'.format(
        user,
        weight,
        inputDate
    )

if __name__ == '__main__':
    app.run(debug=True)