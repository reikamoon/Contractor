from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_animal_id = ObjectId('5d9e5bb44b55903e729d707f')
sample_animal = {
    'name': 'Mika',
    'species': 'Dog',
    'breed': 'Schnauzer',
    'color': 'Gray',
    'price': 'priceless',
    'image': '../static/images/schnauzerrz.jpg'

}
sample_form_data = {
    'name': sample_animal['name'],
    'species': sample_animal['species'],
    'image': '\n'.join(sample_animal['image'])
}

class AnimalTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the animals homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Dimitri', result.data)

    def test_new(self):
        """Test the new animal creation page."""
        result = self.client.get('/animals/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Add a Listing', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_animal(self, mock_find):
        """Test showing a single animal."""
        mock_find.return_value = sample_animal

        result = self.client.get(f'/animals/{sample_animal_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Mika', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_animal(self, mock_find):
        """Test editing a single animal."""
        mock_find.return_value = sample_animal

        result = self.client.get(f'edit/{sample_animal_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Mika', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_animal(self, mock_insert):
        """Test submitting a new animal."""
        result = self.client.post('/animals', data=sample_form_data)

        # After submitting, should redirect to that animal's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_animal)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_animal(self, mock_update):
        result = self.client.post(f'/animals/{sample_animal_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_animal_id}, {'$set': sample_animal})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_animal(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/animals/{sample_animal_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_animal_id})

if __name__ == '__main__':
    unittest_main()
