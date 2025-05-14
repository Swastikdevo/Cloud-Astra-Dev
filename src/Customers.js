```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await axios.get('/api/customers');
      setCustomers(response.data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const addCustomer = async () => {
    if (newCustomer.name && newCustomer.email) {
      const response = await axios.post('/api/customers', newCustomer);
      setCustomers([...customers, response.data]);
      setNewCustomer({ name: '', email: '' });
    }
  };

  return (
    <div>
      {loading ? <p>Loading...</p> : (
        <div>
          <h1>Customer List</h1>
          <ul>
            {customers.map((customer) => (
              <li key={customer.id}>{customer.name} - {customer.email}</li>
            ))}
          </ul>
          <h2>Add New Customer</h2>
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={newCustomer.name}
            onChange={handleInputChange}
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={newCustomer.email}
            onChange={handleInputChange}
          />
          <button onClick={addCustomer}>Add</button>
        </div>
      )}
    </div>
  );
};

export default CustomerManagement;
```