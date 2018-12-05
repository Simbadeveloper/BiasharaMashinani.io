def test_app(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert  response.status_code!= 400

def test_home(test_client):
    business = test_client.get('/businesses')
    assert business.status_code == 200

def test_about(test_client):
    business = test_client.get('/about')
    assert business.status_code == 200

def test_register(test_client):
    business = test_client.get('/register')
    assert business.status_code == 200

def test_login(test_client):
    business = test_client.get('/login')
    assert business.status_code == 200

def test_logout(test_client):
    business = test_client.get('/logout')
    assert business.status_code == 302
    assert business.status_code != 200
def test_account(test_client):
    business = test_client.get('/account')
    assert business.status_code == 302

def test_new_post(test_client):
    business = test_client.get('/businesses/new')
    assert business.status_code == 302

def test_post(test_client):
    business = test_client.get('/businesses/2')
    assert business.status_code == 200

def test_update_post(test_client):
    business = test_client.get('/business/2/update')
    assert business.status_code == 302

def test_delete_post(test_client):
    business = test_client.get('/businesses/2/delete')
    assert business.status_code == 405