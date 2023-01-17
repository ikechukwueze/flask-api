import datetime
from dataclasses import dataclass
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True





app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_database.db'
db = SQLAlchemy(app)



#database models
@dataclass
class songs(db.Model):
    id: int
    name: str
    duration: int
    uploaded_time: str

    

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, db.CheckConstraint('duration > 0'), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)





@dataclass
class podcasts(db.Model):
    id: int
    name: str
    duration: int
    uploaded_time: str
    host: str
    participants: str


    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, db.CheckConstraint('duration > 0'), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    host = db.Column(db.String(100), nullable=False)
    participants = db.relationship('podcast_participants', backref='podcast')



    

#podcast participants table
@dataclass
class podcast_participants(db.Model):
    id: int
    name: str
    podcast_id: int

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))

    #podcast participant constraint
    def __init__(self, *args, **kwargs):
        
        pod_participants = self.query.filter_by(podcast_id=kwargs['podcast_id']).count()
        
        if pod_participants < 10:
            super().__init__(*args, **kwargs)
        else:
            raise Exception('number of participants exceeded')
        




@dataclass
class audiobooks(db.Model):
    id: int
    title: str
    author: str
    narrator: str
    duration: int
    uploaded_time: str


    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, db.CheckConstraint('duration > 0'), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)







audioFileTypes = ('songs', 'podcasts', 'audiobooks')



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')



@app.route('/api/<string:audioFileType>', methods=['POST'])
@app.route('/api/<string:audioFileType>/<string:audioFileID>', methods=['PUT'])
def post_or_put(audioFileType, audioFileID=None):
    
    if audioFileType in audioFileTypes:
        data    = request.get_json()
        method  = request.method

        response = create_or_update(audioFileType, method, data, audioFileID)

        if response is None:
            return '', 500
        else:
            return jsonify(response), 200
    
    else:
        return '', 400



#function to create or update resource
def create_or_update(audioFileType, method, data, audioFileID=None):

    try:
        if audioFileType == 'songs':
            name = data['name']
            duration = data['duration']

            
            if method == 'PUT':
                resource            = songs.query.get(audioFileID)
                resource.name       = name
                resource.duration   = duration

            elif method == 'POST':
                resource = songs(name=name, duration=duration)
                db.session.add(resource)
            
            db.session.commit()
            
        
        elif audioFileType == 'podcasts':
            name        = data['name']
            duration    = data['duration']
            host        = data['host']
            


            if method == 'PUT':
                resource            = podcasts.query.get(audioFileID)
                resource.name       = name
                resource.duration   = duration
                resource.host       = host


            elif method == 'POST':
                resource = podcasts(name=name, duration=duration, host=host)
                db.session.add(resource)
            
            db.session.commit()
            


        elif audioFileType == 'audiobooks':
            title       = data['title']
            author      = data['author']
            duration    = data['duration']
            narrator    = data['narrator']


            if method == 'PUT':
                resource            = audiobooks.query.get(audioFileID)
                resource.title      = title
                resource.duration   = duration
                resource.author     = author
                resource.narrator   = narrator

            elif method == 'POST':
                resource = audiobooks(title=title, duration=duration, author=author, narrator=narrator)
                db.session.add(resource)

            db.session.commit()
        
        return resource
    
    except:
        return None






@app.route('/api/<string:audioFileType>', methods=['GET'])
@app.route('/api/<string:audioFileType>/<int:audioFileID>', methods=['GET', 'DELETE'])
def get_or_delete(audioFileType, audioFileID=None):
    
    if audioFileType in audioFileTypes:

        if request.method == 'GET':

            if audioFileType == 'songs':
                if audioFileID is None:
                    resource = songs.query.all()
                else:
                    resource = songs.query.get(audioFileID)
                    

            
            elif audioFileType == 'podcasts':
                if audioFileID is None:
                    resource = podcasts.query.all()
                else:
                    resource = podcasts.query.get(audioFileID)


            elif audioFileType == 'audiobooks':
                if audioFileID is None:
                    resource = audiobooks.query.all()
                else:
                    resource = audiobooks.query.get(audioFileID)

            
            if resource is None:
                return '', 400
            else:
                return jsonify(resource), 200
            

        
        if request.method == 'DELETE':

            if audioFileType == 'songs':
                resource = songs.query.filter_by(id=audioFileID)

            elif audioFileType == 'podcasts':
                resource = podcasts.query.filter_by(id=audioFileID)

            elif audioFileType == 'audiobooks':
                resource = audiobooks.query.filter_by(id=audioFileID)

            if resource is None:
                return '', 400
            else:
                resource.delete()
                db.session.commit()
                return '', 200
    
    else:
        return "<p>The resource could not be found.</p>", 400






if __name__ == '__main__':
    app.run()
