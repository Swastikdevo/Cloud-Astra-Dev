```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await axios.get('/api/customers');
      setCustomers(response.data);
    };
    fetchCustomers();
  }, []);

  const handleAddCustomer = async () => {
    const response = await axios.post('/api/customers', { name: newCustomer });
    setCustomers([...customers, response.data]);
    setNewCustomer('');
  };

  const handleDeleteCustomer = async (id) => {
    await axios.delete(`/api/customers/${id}`);
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={(e) => setNewCustomer(e.target.value)} 
        placeholder="Add new customer"
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name}
            <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```