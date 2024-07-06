from app import create_app, socketio
import matplotlib
matplotlib.use('Agg')

app = create_app()

if __name__ == '__main__':
    socketio.run(app , debug=True)
    