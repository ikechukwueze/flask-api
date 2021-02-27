from api import app


#data for post requests
song_data = {'name':'Songstress', 'duration': 300}

podcast_data = { 'name':'Podcast Show', 'duration': 3000, 'host': 'Podcaster'}

audiobook_data = {'title':'The Story of John Smith', 'author': 'John Smith',
                    'narrator': 'John Smith', 'duration': 3000}


#data for put requests
song_data_edit = {'name':'Songster', 'duration': 400}

podcast_data_edit = { 'name':'Podcast No Show', 'duration': 4000, 'host': 'Podcaster'}

audiobook_data_edit = {'title':'The Story of Jane Smith', 'author': 'John Smith',
                    'narrator': 'Jane Smith', 'duration': 4000}



post_data_to_test = {'songs':song_data, 'podcasts':podcast_data, 'audiobooks':audiobook_data}
put_data_to_test = {'songs':song_data_edit, 'podcasts':podcast_data_edit, 'audiobooks':audiobook_data_edit}



mimetype = 'application/json'
headers = {'Content-Type': mimetype, 'Accept': mimetype}


audiofiles_to_test = ['songs', 'podcasts', 'audiobooks']
test_id = 5




def test_post_or_put():

    for audiofile, data in post_data_to_test.items():
        
        post_response = app.test_client().post('/api/{}'.format(audiofile), json=data, headers=headers)
        
        assert post_response.status_code == 200


    for audiofile, data in put_data_to_test.items():
        print(audiofile)
        put_response = app.test_client().put('/api/{}/{}'.format(audiofile, test_id), json=data, headers=headers)

        assert put_response.status_code == 200








def test_get_or_delete():

    for audiofile in audiofiles_to_test:

        get_all_response = app.test_client().get('/api/{}'.format(audiofile))
        assert get_all_response.status_code == 200
        assert get_all_response.content_type == mimetype

        total_num_of_before_delete = len(get_all_response.get_json())


        get_one_response = app.test_client().get('/api/{}/{}'.format(audiofile, test_id))
        assert get_one_response.status_code == 200
        assert get_one_response.get_json()['id'] == test_id


        delete_one_response = app.test_client().delete('/api/{}/{}'.format(audiofile, test_id))
        assert delete_one_response.status_code == 200
        
        n = len(app.test_client().get('/api/{}'.format(audiofile)).get_json())

        assert n == total_num_of_before_delete - 1





