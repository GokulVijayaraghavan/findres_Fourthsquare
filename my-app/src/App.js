import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Container, Form, Button } from 'react-bootstrap';

function App() {
  const [airbnbName, setAirbnbName] = useState('');
  const [suburb, setSuburb] = useState('');
  const [inputId, setInputId] = useState('');
  const [response, setResponse] = useState(0);
  const [restaurants, setRestaurants] = useState([]);
  const [latitude, setLatitude] = useState(0);
  const [longitude, setLongitude] = useState(0);
  const [visibleCount, setVisibleCount] = useState(10);

  const loadMoreRestaurants = () => {
    setVisibleCount((prevCount) => prevCount + 10);
  };

  useEffect(() => {
    if (response === 4) {
      console.log(latitude, longitude);
      axios
        .post('http://localhost:5000/api/restaurants', { latitude, longitude })
        .then((response) => setRestaurants(response.data))
        .catch((error) => console.log('Error:', error));
      console.log(restaurants);
    }
  }, [response]);

  const handleAirbnbNameSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/search_airbnb', {
        name: airbnbName,
      });

      const data = response.data;
      setResponse(data.response);
      setLatitude(data.latitude);
      setLongitude(data.longitude);
      console.log(data);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  const handleSuburbSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/search_airbnb', {
        name: airbnbName,
        suburb,
      });

      const data = response.data;
      setResponse(data.response);
      setLatitude(data.latitude);
      setLongitude(data.longitude);
      console.log(data);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  const handleInputIdSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/search_airbnb', {
        id: inputId,
      });

      const data = response.data;
      setResponse(data.response);
      setLatitude(data.latitude);
      setLongitude(data.longitude);
      console.log(data);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  const resetForm = () => {
    setAirbnbName('');
    setSuburb('');
    setInputId('');
    setResponse(0);
    setRestaurants([]);
    setLatitude(0);
    setLongitude(0);
  };

  const handleOk = () => {
    resetForm();
    alert('No matching Airbnb found.');
  };

  return (
    <div className="App">
      <Container className="d-flex align-items-center justify-content-center mx-auto my-auto vh=100">
          {response === 0 && (
            <div className="d-flex text-center mx-auto my-auto">
              <Form onSubmit={handleAirbnbNameSubmit}>
                <h3>Find the restaurants near your location</h3>
                <Form.Group controlId="airbnbName">
                  <Form.Label>Airbnb Name:</Form.Label>
                  <Form.Control
                    type="text"
                    value={airbnbName}
                    onChange={(e) => setAirbnbName(e.target.value)}
                  />
                </Form.Group>
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
            </div>
          )}

          {response === 1 && (
            <div className="text-center">
              <p>Please enter the suburb so that we can locate the exact Airbnb location.</p>
              <Form onSubmit={handleSuburbSubmit}>
                <Form.Group controlId="suburb">
                  <Form.Label>Suburb:</Form.Label>
                  <Form.Control
                    type="text"
                    value={suburb}
                    onChange={(e) => setSuburb(e.target.value)}
                  />
                </Form.Group>
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
              <Button variant="secondary" onClick={resetForm}>
                Go back
              </Button>
            </div>
          )}

          {response === 2 && (
            <div className="text-center">
              <Form onSubmit={handleInputIdSubmit}>
                <Form.Group controlId="inputId">
                  <Form.Label>Input ID:</Form.Label>
                  <Form.Control
                    type="text"
                    value={inputId}
                    onChange={(e) => setInputId(e.target.value)}
                  />
                </Form.Group>
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
              <Button variant="secondary" onClick={resetForm}>
                Go back
              </Button>
            </div>
          )}

          {response === 3 && (
            <div className="text-center">
              <p>There is no Airbnb for the given input.</p>
              <Button variant="primary" onClick={handleOk}>
                OK
              </Button>
            </div>
          )}

          {response === 4 && (
            <div>
              <h1>Restaurants</h1>

              <div>
                {restaurants.slice(0, visibleCount).map((restaurant) => (
                  <div key={restaurant._id} className="restaurant-box">
                    <Card
                      style={{ width: '40rem', borderWidth: '2px', borderColor: 'gray' }}
                      bg="light"
                      text="dark"
                      className="mb-4"
                    >
                      <Card.Body>
                        <Card.Header style={{ backgroundColor: 'lightblue' }} className="text-black font-40px d-flex justify-content-between text-center fontWeight: bold">
                          <span>{restaurant.name} </span>
                          <span>{restaurant.distance} miles</span>
                        </Card.Header>
                        <Card.Text>
                          Cuisine: {restaurant.cuisine}
                        </Card.Text>
                        <Card.Text>
                          Address: {restaurant.address.building} {restaurant.address.street}, {restaurant.address.zipcode}
                        </Card.Text>
                        <Card.Text>
                          Rating: {restaurant.averagerating}
                        </Card.Text>

                      </Card.Body>
                    </Card>
                  </div>
                ))}
              </div>

              <div className="text-center mt-10">
                {visibleCount < restaurants.length && (
                  <Button variant="primary" onClick={loadMoreRestaurants}>
                    Load More
                  </Button>
                )}
                <Button variant="secondary" onClick={resetForm} className="ms-2">
                  Go back
                </Button>
              </div>
            </div>
          )}

      </Container>
    </div>
      );
}

export default App;
