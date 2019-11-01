from app import app, db
from app.models import IgAccount, IgData

@app.shell_context_processor
def make_shell_context():
    return {'db':db,
            'IgAccount':IgAccount,
            'IgData':IgData}
