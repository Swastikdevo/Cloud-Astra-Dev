```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newCustomer, setNewCustomer] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('https://api.example.com/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
    };

    fetchCustomers();
  }, []);

  const addCustomer = () => {
    if (newCustomer) {
      const updatedCustomers = [...customers, newCustomer];
      setCustomers(updatedCustomers);
      setNewCustomer('');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        value={newCustomer}
        onChange={(e) => setNewCustomer(e.target.value)}
        placeholder="Add new customer"
      />
      <button onClick={addCustomer}>Add</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>{customer}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```